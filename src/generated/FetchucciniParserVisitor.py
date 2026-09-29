# Generated from grammar/FetchucciniParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .FetchucciniParser import FetchucciniParser
else:
    from FetchucciniParser import FetchucciniParser

# This class defines a complete generic visitor for a parse tree produced by FetchucciniParser.

class FetchucciniParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FetchucciniParser#program.
    def visitProgram(self, ctx:FetchucciniParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#query.
    def visitQuery(self, ctx:FetchucciniParser.QueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#fetchClause.
    def visitFetchClause(self, ctx:FetchucciniParser.FetchClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#extractClause.
    def visitExtractClause(self, ctx:FetchucciniParser.ExtractClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#fieldList.
    def visitFieldList(self, ctx:FetchucciniParser.FieldListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#fieldDef.
    def visitFieldDef(self, ctx:FetchucciniParser.FieldDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#TextExtractor.
    def visitTextExtractor(self, ctx:FetchucciniParser.TextExtractorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#AttrExtractor.
    def visitAttrExtractor(self, ctx:FetchucciniParser.AttrExtractorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#RegexExtractor.
    def visitRegexExtractor(self, ctx:FetchucciniParser.RegexExtractorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#whereClause.
    def visitWhereClause(self, ctx:FetchucciniParser.WhereClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#RelationalCondition.
    def visitRelationalCondition(self, ctx:FetchucciniParser.RelationalConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#GroupCondition.
    def visitGroupCondition(self, ctx:FetchucciniParser.GroupConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#OrCondition.
    def visitOrCondition(self, ctx:FetchucciniParser.OrConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#AndCondition.
    def visitAndCondition(self, ctx:FetchucciniParser.AndConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#comparison.
    def visitComparison(self, ctx:FetchucciniParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#IdExpr.
    def visitIdExpr(self, ctx:FetchucciniParser.IdExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#NumberExpr.
    def visitNumberExpr(self, ctx:FetchucciniParser.NumberExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#StringExpr.
    def visitStringExpr(self, ctx:FetchucciniParser.StringExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#exportClause.
    def visitExportClause(self, ctx:FetchucciniParser.ExportClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FetchucciniParser#format.
    def visitFormat(self, ctx:FetchucciniParser.FormatContext):
        return self.visitChildren(ctx)



del FetchucciniParser