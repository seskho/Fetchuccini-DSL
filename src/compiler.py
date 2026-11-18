"""Front-end reusable: compila texto o archivos sin realizar HTTP ni exportar."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from antlr4 import CommonTokenStream, InputStream, Token
from antlr4.error.ErrorListener import ErrorListener

from src.generated.FetchucciniLexer import FetchucciniLexer
from src.generated.FetchucciniParser import FetchucciniParser
from src.ir.models import ExecutionPlan
from src.ir.plan_builder import build_plan
from src.semantic.semantic_checker import FetchucciniSemanticChecker


@dataclass(frozen=True)
class Diagnostic:
    code: str
    phase: str
    message: str
    line: int = 1
    column: int = 0

    def __str__(self):
        return (f"[{self.code}] Error {self.phase} en línea {self.line}, "
                f"columna {self.column}: {self.message}")


@dataclass
class CompilationResult:
    success: bool
    phase: str
    diagnostics: list = field(default_factory=list)
    plan: ExecutionPlan | None = None
    tokens: list = field(default_factory=list)
    symbol_table: Any = None


class ErrorCollector(ErrorListener):
    def __init__(self, phase: str, code: str):
        super().__init__()
        self.phase = phase
        self.code = code
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(Diagnostic(self.code, self.phase, msg, line, column))


def compile_source(source: str) -> CompilationResult:
    """Detiene cada fase fallida; solo construye IR tras validación semántica."""
    lexer = FetchucciniLexer(InputStream(source))
    lexical = ErrorCollector("lexical", "L01")
    lexer.removeErrorListeners()
    lexer.addErrorListener(lexical)
    stream = CommonTokenStream(lexer)
    stream.fill()
    tokens = [token for token in stream.tokens if token.type != Token.EOF]
    if lexical.errors:
        return CompilationResult(False, "lexical", lexical.errors, tokens=tokens)

    parser = FetchucciniParser(stream)
    syntax = ErrorCollector("syntax", "P01")
    parser.removeErrorListeners()
    parser.addErrorListener(syntax)
    tree = parser.program()
    if syntax.errors:
        return CompilationResult(False, "syntax", syntax.errors, tokens=tokens)

    checker = FetchucciniSemanticChecker()
    errors = checker.check(tree)
    if errors:
        return CompilationResult(False, "semantic", errors, tokens=tokens,
                                 symbol_table=checker.symbol_table)
    return CompilationResult(True, "none", plan=build_plan(tree), tokens=tokens,
                             symbol_table=checker.symbol_table)


def compile_file(file_path) -> CompilationResult:
    try:
        source = Path(file_path).read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        return CompilationResult(False, "io", [Diagnostic("IO01", "io", str(error))])
    return compile_source(source)
