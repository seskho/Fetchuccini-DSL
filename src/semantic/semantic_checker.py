"""
Analizador semántico preliminar para el lenguaje Fetchuccini (Hito 1 - Trabajo Parcial).

Verifica las dos reglas semánticas especificadas en el informe:
  1. Campo duplicado: un alias no puede declararse más de una vez dentro de EXTRACT.
  2. Campo no declarado: todo identificador utilizado en WHERE debe haber sido declarado
     previamente en EXTRACT.
"""

from typing import List, Set
from src.generated.FetchucciniParser import FetchucciniParser
from src.generated.FetchucciniParserVisitor import FetchucciniParserVisitor


class SemanticError:
    """Representa un error semántico con mensaje y ubicación en el código fuente."""

    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"[Error Semantico] Linea {self.line}:{self.column} -> {self.message}"


class FetchucciniSemanticChecker(FetchucciniParserVisitor):
    """
    Visitor de ANTLR4 para validar las reglas semánticas preliminares de Fetchuccini.
    """

    def __init__(self):
        super().__init__()
        self.symbol_table: Set[str] = set()
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

        # Error Semántico 1: alias duplicado en EXTRACT
        if alias_name in self.symbol_table:
            self.errors.append(
                SemanticError(
                    f"El campo '{alias_name}' ya fue definido en EXTRACT",
                    alias_token.line,
                    alias_token.column,
                )
            )
        else:
            self.symbol_table.add(alias_name)

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

            # Error Semántico 2: identificador en WHERE no declarado en EXTRACT
            if field_name not in self.symbol_table:
                self.errors.append(
                    SemanticError(
                        f"El campo '{field_name}' no existe en EXTRACT",
                        token.line,
                        token.column,
                    )
                )

        return self.visitChildren(ctx)
