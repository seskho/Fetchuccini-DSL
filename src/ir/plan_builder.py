"""Traduce un árbol ya validado a un plan sin dependencias de ANTLR."""

from src.generated.FetchucciniParser import FetchucciniParser
from src.generated.FetchucciniParserVisitor import FetchucciniParserVisitor
from src.ir.models import (
    AndExpression, Comparison, ExecutionPlan, FieldPlan, Identifier,
    NumberLiteral, OrExpression, StringLiteral,
)
from src.literals import decode_string


class PlanBuilder(FetchucciniParserVisitor):
    def visitProgram(self, ctx):
        return self.visit(ctx.query())

    def visitQuery(self, ctx):
        each = ctx.eachClause()
        where = ctx.whereClause()
        export = ctx.exportClause()
        return ExecutionPlan(
            source_url=decode_string(ctx.fetchClause().url.text),
            each_selector=decode_string(each.selector.text) if each else None,
            fields=tuple(self.visit(field) for field in ctx.extractClause().fieldList().fieldDef()),
            filter_expression=self.visit(where.condition()) if where else None,
            export_format=export.format_().getText(),
            export_path=decode_string(export.path.text),
        )

    def visitFieldDef(self, ctx):
        extractor = ctx.extractor()
        argument = None
        if isinstance(extractor, FetchucciniParser.AttrExtractorContext):
            argument = decode_string(extractor.attrName.text).strip()
        elif isinstance(extractor, FetchucciniParser.RegexExtractorContext):
            argument = decode_string(extractor.pattern.text)
        annotation = ctx.typeAnnotation()
        return FieldPlan(
            alias=ctx.alias.text,
            extractor_type=extractor.start.text,
            selector=decode_string(ctx.selector.text),
            extractor_argument=argument,
            declared_type=annotation.stop.text if annotation else "AUTO",
            line=ctx.alias.line,
            column=ctx.alias.column,
        )

    def visitCondition(self, ctx):
        operands = tuple(self.visit(child) for child in ctx.conditionAnd())
        return operands[0] if len(operands) == 1 else OrExpression(operands)

    def visitConditionAnd(self, ctx):
        operands = tuple(self.visit(child) for child in ctx.comparison())
        return operands[0] if len(operands) == 1 else AndExpression(operands)

    def visitComparison(self, ctx):
        return Comparison(
            left=self.visit(ctx.left), operator=ctx.relOp().getText(),
            right=self.visit(ctx.right), line=ctx.start.line, column=ctx.start.column,
        )

    def visitIdExpr(self, ctx):
        return Identifier(ctx.ID().getText())

    def visitNumberExpr(self, ctx):
        return NumberLiteral(float(ctx.NUMBER().getText()))

    def visitStringExpr(self, ctx):
        return StringLiteral(decode_string(ctx.STRING().getText()))


def build_plan(tree) -> ExecutionPlan:
    """Construye la IR después de comprobar que no existen errores de compilación."""
    return PlanBuilder().visit(tree)
