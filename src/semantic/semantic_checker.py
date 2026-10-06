"""
Analizador semántico preliminar para el lenguaje Fetchuccini (Hito 1 - Trabajo Parcial).

Sigue el diseño de los Laboratorios 4 y 5 del curso con una Tabla de Símbolos (Hash Table)
formal mediante las clases Symbol y SymbolTable.

Verifica las dos reglas semánticas especificadas en el informe:
  1. Campo duplicado: un alias no puede declararse más de una vez dentro de EXTRACT.
  2. Campo no declarado: todo identificador utilizado en WHERE debe haber sido declarado
     previamente en EXTRACT.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from src.generated.FetchucciniParser import FetchucciniParser
from src.generated.FetchucciniParserVisitor import FetchucciniParserVisitor


class SemanticError(Exception):
    """Representa un error semántico con mensaje y ubicación en el código fuente."""

    def __init__(self, message: str, line: int, column: int):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"[Error Semantico] Linea {self.line}:{self.column} -> {self.message}"


@dataclass
class Symbol:
    """Representa la entrada de un identificador en la tabla de símbolos."""
    name: str
    extractor_type: str
    line: int
    column: int


class SymbolTable:
    """
    Tabla de símbolos basada en una tabla hash (dict de Python).
    Encapsula el registro y consulta de los alias declarados en EXTRACT.
    """

    def __init__(self):
        # Tabla hash subyacente: clave -> Symbol
        self.symbols: Dict[str, Symbol] = {}

    def declare(self, name: str, extractor_type: str, line: int, column: int) -> None:
        """
        Inserta un nuevo símbolo en la tabla hash.
        Lanza SemanticError si el identificador ya existe (colisión / duplicado).
        """
        if name in self.symbols:
            raise SemanticError(
                f"El campo '{name}' ya fue definido en EXTRACT",
                line,
                column
            )
        self.symbols[name] = Symbol(name, extractor_type, line, column)

    def lookup(self, name: str, line: int, column: int) -> Symbol:
        """
        Busca un símbolo en la tabla hash en O(1).
        Lanza SemanticError si el identificador no ha sido declarado.
        """
        if name not in self.symbols:
            raise SemanticError(
                f"El campo '{name}' no existe en EXTRACT",
                line,
                column
            )
        return self.symbols[name]

    def contains(self, name: str) -> bool:
        return name in self.symbols

    def names(self) -> List[str]:
        return sorted(list(self.symbols.keys()))

    def clear(self) -> None:
        self.symbols.clear()


class FetchucciniSemanticChecker(FetchucciniParserVisitor):
    """
    Visitor de ANTLR4 para validar las reglas semánticas preliminares de Fetchuccini
    utilizando una SymbolTable formal.
    """

    def __init__(self):
        super().__init__()
        self.symbol_table: SymbolTable = SymbolTable()
        self.errors: List[SemanticError] = []
        self._in_where: bool = False

    def reset(self):
        """Reinicia el estado interno del analizador para permitir múltiples ejecuciones."""
        self.symbol_table.clear()
        self.errors.clear()
        self._in_where = False

    def check(self, tree) -> List[SemanticError]:
        """Ejecuta el análisis semántico sobre el árbol y retorna la lista de errores encontrados."""
        self.reset()
        self.visit(tree)
        return self.errors

    def visitFieldDef(self, ctx: FetchucciniParser.FieldDefContext):
        alias_token = ctx.alias
        alias_name = alias_token.text
        line = alias_token.line
        col = alias_token.column

        # Identificar mecanismo de extracción ('text', 'attr', 'regex')
        extractor_type = "unknown"
        extractor_ctx = ctx.extractor()
        if isinstance(extractor_ctx, FetchucciniParser.TextExtractorContext):
            extractor_type = "text"
        elif isinstance(extractor_ctx, FetchucciniParser.AttrExtractorContext):
            extractor_type = "attr"
        elif isinstance(extractor_ctx, FetchucciniParser.RegexExtractorContext):
            extractor_type = "regex"

        # Registrar en la tabla de símbolos (manejo de error 1: alias duplicado)
        try:
            self.symbol_table.declare(alias_name, extractor_type, line, col)
        except SemanticError as err:
            self.errors.append(err)

        return self.visitChildren(ctx)

    def visitWhereClause(self, ctx: FetchucciniParser.WhereClauseContext):
        self._in_where = True
        res = self.visitChildren(ctx)
        self._in_where = False
        return res

    def visitIdExpr(self, ctx: FetchucciniParser.IdExprContext):
        if self._in_where:
            token = ctx.ID().getSymbol()
            field_name = token.text
            line = token.line
            col = token.column

            # Consultar en la tabla de símbolos (manejo de error 2: identificador no declarado)
            try:
                self.symbol_table.lookup(field_name, line, col)
            except SemanticError as err:
                self.errors.append(err)

        return self.visitChildren(ctx)
