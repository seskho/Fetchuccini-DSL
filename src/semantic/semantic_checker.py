"""Visitor semántico de Fetchuccini: tabla de símbolos y reglas S01-S08."""

from dataclasses import dataclass
import ipaddress
import math
import re
from typing import Dict, List, Optional
from urllib.parse import urlsplit

import soupsieve

from src.generated.FetchucciniParser import FetchucciniParser
from src.generated.FetchucciniParserVisitor import FetchucciniParserVisitor
from src.literals import decode_string
from src.output_paths import validate_export_path


class SemanticError(Exception):
    """Error con código estable, fase y posición (columna desde cero de ANTLR)."""

    phase = "semantic"

    def __init__(self, message: str, line: int, column: int, code: str = "S01"):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.code = code

    def __str__(self) -> str:
        return (
            f"[{self.code}] Error semántico en línea {self.line}, "
            f"columna {self.column}: {self.message}"
        )


@dataclass
class Symbol:
    """Entrada de un alias; conserva los argumentos posicionales del Hito 1."""

    name: str
    extractor_type: str
    line: int
    column: int
    declared_type: str = "AUTO"
    selector: Optional[str] = None
    extractor_argument: Optional[str] = None


class SymbolTable:
    """Tabla hash de alias, reutilizada y ampliada desde el Hito 1."""

    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}

    def declare(
        self, name: str, extractor_type: str, line: int, column: int,
        declared_type: str = "AUTO", selector: Optional[str] = None,
        extractor_argument: Optional[str] = None,
    ) -> None:
        if name in self.symbols:
            raise SemanticError(f"El campo '{name}' ya fue definido en EXTRACT", line, column, "S01")
        self.symbols[name] = Symbol(
            name, extractor_type, line, column, declared_type, selector, extractor_argument,
        )

    def lookup(self, name: str, line: int, column: int) -> Symbol:
        if name not in self.symbols:
            raise SemanticError(f"El campo '{name}' no existe en EXTRACT", line, column, "S02")
        return self.symbols[name]

    def contains(self, name: str) -> bool:
        return name in self.symbols

    def names(self) -> List[str]:
        return sorted(self.symbols)

    def clear(self) -> None:
        self.symbols.clear()


def validate_source_url(value: str) -> None:
    """Comprueba sintaxis HTTP(S), hostname y puerto sin resolver DNS ni conectar."""
    if any(character.isspace() or ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError("La URL no puede contener espacios ni caracteres de control")
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError as error:
        raise ValueError("La URL contiene un hostname o puerto inválido") from error
    if parsed.scheme not in {"http", "https"} or not hostname:
        raise ValueError("FETCH requiere una URL HTTP o HTTPS con hostname válido")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("FETCH no admite credenciales en la URL")
    if port is not None and not 1 <= port <= 65535:
        raise ValueError("La URL contiene un puerto fuera del rango 1-65535")
    try:
        ipaddress.ip_address(hostname)
        return
    except ValueError:
        pass
    # Un literal con apariencia IPv4 no debe eludir la comprobación como dominio.
    if re.fullmatch(r"[0-9.]+", hostname):
        raise ValueError("La dirección IPv4 de FETCH no es válida")
    try:
        # Se permite un punto DNS final, pero no varios segmentos vacíos.
        domain = hostname[:-1] if hostname.endswith(".") else hostname
        ascii_hostname = domain.encode("idna").decode("ascii")
    except UnicodeError as error:
        raise ValueError("El hostname de FETCH no es válido") from error
    labels = ascii_hostname.split(".")
    if len(ascii_hostname) > 253 or any(
        not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", label)
        for label in labels
    ):
        raise ValueError("El hostname de FETCH no es válido")


class FetchucciniSemanticChecker(FetchucciniParserVisitor):
    """Acumula errores independientes antes de permitir la construcción del plan."""

    def __init__(self):
        super().__init__()
        self.symbol_table = SymbolTable()
        self.errors: List[SemanticError] = []
        self._in_where = False

    def reset(self):
        self.symbol_table.clear()
        self.errors.clear()
        self._in_where = False

    def check(self, tree) -> List[SemanticError]:
        self.reset()
        self.visit(tree)
        return self.errors

    def _error(self, code, message, token):
        self.errors.append(SemanticError(message, token.line, token.column, code))

    def _validate_selector(self, token, description):
        try:
            soupsieve.compile(decode_string(token.text))
        except (soupsieve.SelectorSyntaxError, OverflowError, RecursionError) as error:
            self._error("S04", f"El selector CSS {description} no es válido: {error}", token)

    def visitFetchClause(self, ctx):
        try:
            validate_source_url(decode_string(ctx.url.text))
        except ValueError as error:
            self._error("S03", str(error), ctx.url)
        return self.visitChildren(ctx)

    def visitEachClause(self, ctx):
        self._validate_selector(ctx.selector, "de EACH")
        return self.visitChildren(ctx)

    def visitFieldDef(self, ctx):
        extractor = ctx.extractor()
        extractor_type = extractor.start.text
        argument = None
        if isinstance(extractor, FetchucciniParser.AttrExtractorContext):
            argument = decode_string(extractor.attrName.text).strip()
            if not argument:
                self._error("S06", f"El nombre de atributo del campo '{ctx.alias.text}' está vacío", extractor.attrName)
        elif isinstance(extractor, FetchucciniParser.RegexExtractorContext):
            argument = decode_string(extractor.pattern.text)
            try:
                re.compile(argument)
            except (re.error, OverflowError, RecursionError) as error:
                self._error("S05", f"La expresión regular del campo '{ctx.alias.text}' no es válida: {error}", extractor.pattern)
        annotation = ctx.typeAnnotation()
        declared_type = annotation.stop.text if annotation else "AUTO"
        try:
            self.symbol_table.declare(
                ctx.alias.text, extractor_type, ctx.alias.line, ctx.alias.column,
                declared_type, decode_string(ctx.selector.text), argument,
            )
        except SemanticError as error:
            self.errors.append(error)
        self._validate_selector(ctx.selector, f"del campo '{ctx.alias.text}'")
        return self.visitChildren(ctx)

    def visitWhereClause(self, ctx):
        self._in_where = True
        result = self.visitChildren(ctx)
        self._in_where = False
        return result

    def visitIdExpr(self, ctx):
        if self._in_where:
            token = ctx.ID().getSymbol()
            try:
                self.symbol_table.lookup(token.text, token.line, token.column)
            except SemanticError as error:
                self.errors.append(error)
        return self.visitChildren(ctx)

    def _expression_type(self, ctx):
        if isinstance(ctx, FetchucciniParser.IdExprContext):
            symbol = self.symbol_table.symbols.get(ctx.ID().getText())
            return symbol.declared_type if symbol else None
        if isinstance(ctx, FetchucciniParser.NumberExprContext):
            return "NUMBER"
        return "STRING"

    def _numeric_compatible(self, ctx, data_type):
        if isinstance(ctx, FetchucciniParser.StringExprContext):
            try:
                return math.isfinite(float(decode_string(ctx.STRING().getText())))
            except ValueError:
                return False
        return data_type in {"AUTO", "NUMBER"}

    def visitNumberExpr(self, ctx):
        if not math.isfinite(float(ctx.NUMBER().getText())):
            self._error("S08", "El literal NUMBER excede el rango numérico finito admitido", ctx.start)
        return self.visitChildren(ctx)

    def visitComparison(self, ctx):
        self.visitChildren(ctx)
        left_type = self._expression_type(ctx.left)
        right_type = self._expression_type(ctx.right)
        if left_type is None or right_type is None:
            return None  # S02 ya describe el identificador; evita errores derivados.
        operator = ctx.relOp().getText()
        if operator in {"<", "<=", ">", ">="}:
            if not self._numeric_compatible(ctx.left, left_type) or not self._numeric_compatible(ctx.right, right_type):
                self._error("S08", f"El operador '{operator}' requiere operandos numéricos o convertibles; no admite campos AS STRING", ctx.relOp().start)
        elif left_type != "AUTO" and right_type != "AUTO" and left_type != right_type:
            self._error("S08", f"Tipos incompatibles en '{operator}': {left_type} y {right_type}", ctx.relOp().start)
        return None

    def visitExportClause(self, ctx):
        try:
            validate_export_path(decode_string(ctx.path.text), ctx.format_().getText())
        except ValueError as error:
            self._error("S07", str(error), ctx.path)
        return self.visitChildren(ctx)
