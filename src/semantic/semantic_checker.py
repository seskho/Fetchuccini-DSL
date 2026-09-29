from typing import List, Set
from src.generated.FetchucciniParser import FetchucciniParser
from src.generated.FetchucciniParserVisitor import FetchucciniParserVisitor

class SemanticError:
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"Linea {self.line}:{self.column} - {self.message}"

class FetchucciniSemanticChecker(FetchucciniParserVisitor):
    def __init__(self):
        super().__init__()
        self.symbol_table: Set[str] = set()
        self.errors: List[SemanticError] = []
        self._in_where: bool = False

    def visitFieldDef(self, ctx: FetchucciniParser.FieldDefContext):
        alias_token = ctx.alias
        alias_name = alias_token.text

        # Campo duplicado en EXTRACT
        if alias_name in self.symbol_table:
            self.errors.append(
                SemanticError(
                    f"El campo '{alias_name}' ya fue definido en EXTRACT",
                    alias_token.line,
                    alias_token.column
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

            # Campo no definido en EXTRACT
            if field_name not in self.symbol_table:
                self.errors.append(
                    SemanticError(
                        f"El campo '{field_name}' no existe en EXTRACT",
                        token.line,
                        token.column
                    )
                )

        return self.visitChildren(ctx)

