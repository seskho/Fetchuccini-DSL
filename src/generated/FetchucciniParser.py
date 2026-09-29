# Generated from grammar/FetchucciniParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,32,110,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,1,0,1,0,
        1,0,1,1,1,1,1,1,3,1,33,8,1,1,1,1,1,1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,
        3,1,4,1,4,1,4,5,4,48,8,4,10,4,12,4,51,9,4,1,5,1,5,1,5,1,5,1,5,1,
        5,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,3,6,68,8,6,1,7,1,7,1,7,1,8,
        1,8,1,8,1,8,1,8,1,8,3,8,79,8,8,1,8,1,8,1,8,1,8,1,8,1,8,5,8,87,8,
        8,10,8,12,8,90,9,8,1,9,1,9,1,9,1,9,1,10,1,10,1,10,3,10,99,8,10,1,
        11,1,11,1,11,1,11,1,11,1,11,1,11,1,12,1,12,1,12,0,1,16,13,0,2,4,
        6,8,10,12,14,16,18,20,22,24,0,2,1,0,15,20,1,0,8,9,105,0,26,1,0,0,
        0,2,29,1,0,0,0,4,36,1,0,0,0,6,39,1,0,0,0,8,44,1,0,0,0,10,52,1,0,
        0,0,12,67,1,0,0,0,14,69,1,0,0,0,16,78,1,0,0,0,18,91,1,0,0,0,20,98,
        1,0,0,0,22,100,1,0,0,0,24,107,1,0,0,0,26,27,3,2,1,0,27,28,5,0,0,
        1,28,1,1,0,0,0,29,30,3,4,2,0,30,32,3,6,3,0,31,33,3,14,7,0,32,31,
        1,0,0,0,32,33,1,0,0,0,33,34,1,0,0,0,34,35,3,22,11,0,35,3,1,0,0,0,
        36,37,5,1,0,0,37,38,5,30,0,0,38,5,1,0,0,0,39,40,5,2,0,0,40,41,5,
        21,0,0,41,42,3,8,4,0,42,43,5,22,0,0,43,7,1,0,0,0,44,49,3,10,5,0,
        45,46,5,26,0,0,46,48,3,10,5,0,47,45,1,0,0,0,48,51,1,0,0,0,49,47,
        1,0,0,0,49,50,1,0,0,0,50,9,1,0,0,0,51,49,1,0,0,0,52,53,5,28,0,0,
        53,54,5,25,0,0,54,55,3,12,6,0,55,56,5,3,0,0,56,57,5,30,0,0,57,11,
        1,0,0,0,58,68,5,10,0,0,59,60,5,11,0,0,60,61,5,23,0,0,61,62,5,30,
        0,0,62,68,5,24,0,0,63,64,5,12,0,0,64,65,5,23,0,0,65,66,5,30,0,0,
        66,68,5,24,0,0,67,58,1,0,0,0,67,59,1,0,0,0,67,63,1,0,0,0,68,13,1,
        0,0,0,69,70,5,4,0,0,70,71,3,16,8,0,71,15,1,0,0,0,72,73,6,8,-1,0,
        73,74,5,23,0,0,74,75,3,16,8,0,75,76,5,24,0,0,76,79,1,0,0,0,77,79,
        3,18,9,0,78,72,1,0,0,0,78,77,1,0,0,0,79,88,1,0,0,0,80,81,10,4,0,
        0,81,82,5,14,0,0,82,87,3,16,8,5,83,84,10,3,0,0,84,85,5,13,0,0,85,
        87,3,16,8,4,86,80,1,0,0,0,86,83,1,0,0,0,87,90,1,0,0,0,88,86,1,0,
        0,0,88,89,1,0,0,0,89,17,1,0,0,0,90,88,1,0,0,0,91,92,3,20,10,0,92,
        93,7,0,0,0,93,94,3,20,10,0,94,19,1,0,0,0,95,99,5,28,0,0,96,99,5,
        29,0,0,97,99,5,30,0,0,98,95,1,0,0,0,98,96,1,0,0,0,98,97,1,0,0,0,
        99,21,1,0,0,0,100,101,5,5,0,0,101,102,5,6,0,0,102,103,3,24,12,0,
        103,104,5,7,0,0,104,105,5,30,0,0,105,106,5,27,0,0,106,23,1,0,0,0,
        107,108,7,1,0,0,108,25,1,0,0,0,7,32,49,67,78,86,88,98
    ]

class FetchucciniParser ( Parser ):

    grammarFileName = "FetchucciniParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'FETCH'", "'EXTRACT'", "'FROM'", "'WHERE'", 
                     "'EXPORT'", "'AS'", "'TO'", "'JSON'", "'CSV'", "'text'", 
                     "'attr'", "'regex'", "'AND'", "'OR'", "'=='", "'!='", 
                     "'<='", "'>='", "'<'", "'>'", "'{'", "'}'", "'('", 
                     "')'", "':'", "','", "';'" ]

    symbolicNames = [ "<INVALID>", "KW_FETCH", "KW_EXTRACT", "KW_FROM", 
                      "KW_WHERE", "KW_EXPORT", "KW_AS", "KW_TO", "KW_JSON", 
                      "KW_CSV", "KW_TEXT", "KW_ATTR", "KW_REGEX", "OP_AND", 
                      "OP_OR", "OP_EQ", "OP_NEQ", "OP_LE", "OP_GE", "OP_LT", 
                      "OP_GT", "LBRACE", "RBRACE", "LPAREN", "RPAREN", "COLON", 
                      "COMMA", "SEMICOLON", "ID", "NUMBER", "STRING", "WS", 
                      "COMMENT" ]

    RULE_program = 0
    RULE_query = 1
    RULE_fetchClause = 2
    RULE_extractClause = 3
    RULE_fieldList = 4
    RULE_fieldDef = 5
    RULE_extractor = 6
    RULE_whereClause = 7
    RULE_condition = 8
    RULE_comparison = 9
    RULE_expression = 10
    RULE_exportClause = 11
    RULE_format = 12

    ruleNames =  [ "program", "query", "fetchClause", "extractClause", "fieldList", 
                   "fieldDef", "extractor", "whereClause", "condition", 
                   "comparison", "expression", "exportClause", "format" ]

    EOF = Token.EOF
    KW_FETCH=1
    KW_EXTRACT=2
    KW_FROM=3
    KW_WHERE=4
    KW_EXPORT=5
    KW_AS=6
    KW_TO=7
    KW_JSON=8
    KW_CSV=9
    KW_TEXT=10
    KW_ATTR=11
    KW_REGEX=12
    OP_AND=13
    OP_OR=14
    OP_EQ=15
    OP_NEQ=16
    OP_LE=17
    OP_GE=18
    OP_LT=19
    OP_GT=20
    LBRACE=21
    RBRACE=22
    LPAREN=23
    RPAREN=24
    COLON=25
    COMMA=26
    SEMICOLON=27
    ID=28
    NUMBER=29
    STRING=30
    WS=31
    COMMENT=32

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def query(self):
            return self.getTypedRuleContext(FetchucciniParser.QueryContext,0)


        def EOF(self):
            return self.getToken(FetchucciniParser.EOF, 0)

        def getRuleIndex(self):
            return FetchucciniParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = FetchucciniParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 26
            self.query()
            self.state = 27
            self.match(FetchucciniParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QueryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def fetchClause(self):
            return self.getTypedRuleContext(FetchucciniParser.FetchClauseContext,0)


        def extractClause(self):
            return self.getTypedRuleContext(FetchucciniParser.ExtractClauseContext,0)


        def exportClause(self):
            return self.getTypedRuleContext(FetchucciniParser.ExportClauseContext,0)


        def whereClause(self):
            return self.getTypedRuleContext(FetchucciniParser.WhereClauseContext,0)


        def getRuleIndex(self):
            return FetchucciniParser.RULE_query

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuery" ):
                return visitor.visitQuery(self)
            else:
                return visitor.visitChildren(self)




    def query(self):

        localctx = FetchucciniParser.QueryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_query)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 29
            self.fetchClause()
            self.state = 30
            self.extractClause()
            self.state = 32
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 31
                self.whereClause()


            self.state = 34
            self.exportClause()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FetchClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.url = None # Token

        def KW_FETCH(self):
            return self.getToken(FetchucciniParser.KW_FETCH, 0)

        def STRING(self):
            return self.getToken(FetchucciniParser.STRING, 0)

        def getRuleIndex(self):
            return FetchucciniParser.RULE_fetchClause

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFetchClause" ):
                return visitor.visitFetchClause(self)
            else:
                return visitor.visitChildren(self)




    def fetchClause(self):

        localctx = FetchucciniParser.FetchClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_fetchClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.match(FetchucciniParser.KW_FETCH)
            self.state = 37
            localctx.url = self.match(FetchucciniParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExtractClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_EXTRACT(self):
            return self.getToken(FetchucciniParser.KW_EXTRACT, 0)

        def LBRACE(self):
            return self.getToken(FetchucciniParser.LBRACE, 0)

        def fieldList(self):
            return self.getTypedRuleContext(FetchucciniParser.FieldListContext,0)


        def RBRACE(self):
            return self.getToken(FetchucciniParser.RBRACE, 0)

        def getRuleIndex(self):
            return FetchucciniParser.RULE_extractClause

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExtractClause" ):
                return visitor.visitExtractClause(self)
            else:
                return visitor.visitChildren(self)




    def extractClause(self):

        localctx = FetchucciniParser.ExtractClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_extractClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            self.match(FetchucciniParser.KW_EXTRACT)
            self.state = 40
            self.match(FetchucciniParser.LBRACE)
            self.state = 41
            self.fieldList()
            self.state = 42
            self.match(FetchucciniParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FieldListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def fieldDef(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FetchucciniParser.FieldDefContext)
            else:
                return self.getTypedRuleContext(FetchucciniParser.FieldDefContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(FetchucciniParser.COMMA)
            else:
                return self.getToken(FetchucciniParser.COMMA, i)

        def getRuleIndex(self):
            return FetchucciniParser.RULE_fieldList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFieldList" ):
                return visitor.visitFieldList(self)
            else:
                return visitor.visitChildren(self)




    def fieldList(self):

        localctx = FetchucciniParser.FieldListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_fieldList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.fieldDef()
            self.state = 49
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==26:
                self.state = 45
                self.match(FetchucciniParser.COMMA)
                self.state = 46
                self.fieldDef()
                self.state = 51
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FieldDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.alias = None # Token
            self.selector = None # Token

        def COLON(self):
            return self.getToken(FetchucciniParser.COLON, 0)

        def extractor(self):
            return self.getTypedRuleContext(FetchucciniParser.ExtractorContext,0)


        def KW_FROM(self):
            return self.getToken(FetchucciniParser.KW_FROM, 0)

        def ID(self):
            return self.getToken(FetchucciniParser.ID, 0)

        def STRING(self):
            return self.getToken(FetchucciniParser.STRING, 0)

        def getRuleIndex(self):
            return FetchucciniParser.RULE_fieldDef

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFieldDef" ):
                return visitor.visitFieldDef(self)
            else:
                return visitor.visitChildren(self)




    def fieldDef(self):

        localctx = FetchucciniParser.FieldDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_fieldDef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 52
            localctx.alias = self.match(FetchucciniParser.ID)
            self.state = 53
            self.match(FetchucciniParser.COLON)
            self.state = 54
            self.extractor()
            self.state = 55
            self.match(FetchucciniParser.KW_FROM)
            self.state = 56
            localctx.selector = self.match(FetchucciniParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExtractorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FetchucciniParser.RULE_extractor

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class RegexExtractorContext(ExtractorContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FetchucciniParser.ExtractorContext
            super().__init__(parser)
            self.pattern = None # Token
            self.copyFrom(ctx)

        def KW_REGEX(self):
            return self.getToken(FetchucciniParser.KW_REGEX, 0)
        def LPAREN(self):
            return self.getToken(FetchucciniParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(FetchucciniParser.RPAREN, 0)
        def STRING(self):
            return self.getToken(FetchucciniParser.STRING, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRegexExtractor" ):
                return visitor.visitRegexExtractor(self)
            else:
                return visitor.visitChildren(self)


    class TextExtractorContext(ExtractorContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FetchucciniParser.ExtractorContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def KW_TEXT(self):
            return self.getToken(FetchucciniParser.KW_TEXT, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTextExtractor" ):
                return visitor.visitTextExtractor(self)
            else:
                return visitor.visitChildren(self)


    class AttrExtractorContext(ExtractorContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FetchucciniParser.ExtractorContext
            super().__init__(parser)
            self.attrName = None # Token
            self.copyFrom(ctx)

        def KW_ATTR(self):
            return self.getToken(FetchucciniParser.KW_ATTR, 0)
        def LPAREN(self):
            return self.getToken(FetchucciniParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(FetchucciniParser.RPAREN, 0)
        def STRING(self):
            return self.getToken(FetchucciniParser.STRING, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttrExtractor" ):
                return visitor.visitAttrExtractor(self)
            else:
                return visitor.visitChildren(self)



    def extractor(self):

        localctx = FetchucciniParser.ExtractorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_extractor)
        try:
            self.state = 67
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [10]:
                localctx = FetchucciniParser.TextExtractorContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 58
                self.match(FetchucciniParser.KW_TEXT)
                pass
            elif token in [11]:
                localctx = FetchucciniParser.AttrExtractorContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 59
                self.match(FetchucciniParser.KW_ATTR)
                self.state = 60
                self.match(FetchucciniParser.LPAREN)
                self.state = 61
                localctx.attrName = self.match(FetchucciniParser.STRING)
                self.state = 62
                self.match(FetchucciniParser.RPAREN)
                pass
            elif token in [12]:
                localctx = FetchucciniParser.RegexExtractorContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 63
                self.match(FetchucciniParser.KW_REGEX)
                self.state = 64
                self.match(FetchucciniParser.LPAREN)
                self.state = 65
                localctx.pattern = self.match(FetchucciniParser.STRING)
                self.state = 66
                self.match(FetchucciniParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhereClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_WHERE(self):
            return self.getToken(FetchucciniParser.KW_WHERE, 0)

        def condition(self):
            return self.getTypedRuleContext(FetchucciniParser.ConditionContext,0)


        def getRuleIndex(self):
            return FetchucciniParser.RULE_whereClause

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhereClause" ):
                return visitor.visitWhereClause(self)
            else:
                return visitor.visitChildren(self)




    def whereClause(self):

        localctx = FetchucciniParser.WhereClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_whereClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self.match(FetchucciniParser.KW_WHERE)
            self.state = 70
            self.condition(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FetchucciniParser.RULE_condition

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class RelationalConditionContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FetchucciniParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def comparison(self):
            return self.getTypedRuleContext(FetchucciniParser.ComparisonContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelationalCondition" ):
                return visitor.visitRelationalCondition(self)
            else:
                return visitor.visitChildren(self)


    class GroupConditionContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FetchucciniParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(FetchucciniParser.LPAREN, 0)
        def condition(self):
            return self.getTypedRuleContext(FetchucciniParser.ConditionContext,0)

        def RPAREN(self):
            return self.getToken(FetchucciniParser.RPAREN, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGroupCondition" ):
                return visitor.visitGroupCondition(self)
            else:
                return visitor.visitChildren(self)


    class OrConditionContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FetchucciniParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def condition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FetchucciniParser.ConditionContext)
            else:
                return self.getTypedRuleContext(FetchucciniParser.ConditionContext,i)

        def OP_OR(self):
            return self.getToken(FetchucciniParser.OP_OR, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrCondition" ):
                return visitor.visitOrCondition(self)
            else:
                return visitor.visitChildren(self)


    class AndConditionContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FetchucciniParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def condition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FetchucciniParser.ConditionContext)
            else:
                return self.getTypedRuleContext(FetchucciniParser.ConditionContext,i)

        def OP_AND(self):
            return self.getToken(FetchucciniParser.OP_AND, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndCondition" ):
                return visitor.visitAndCondition(self)
            else:
                return visitor.visitChildren(self)



    def condition(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = FetchucciniParser.ConditionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 16
        self.enterRecursionRule(localctx, 16, self.RULE_condition, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 78
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23]:
                localctx = FetchucciniParser.GroupConditionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 73
                self.match(FetchucciniParser.LPAREN)
                self.state = 74
                self.condition(0)
                self.state = 75
                self.match(FetchucciniParser.RPAREN)
                pass
            elif token in [28, 29, 30]:
                localctx = FetchucciniParser.RelationalConditionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 77
                self.comparison()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 88
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 86
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
                    if la_ == 1:
                        localctx = FetchucciniParser.OrConditionContext(self, FetchucciniParser.ConditionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_condition)
                        self.state = 80
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 81
                        self.match(FetchucciniParser.OP_OR)
                        self.state = 82
                        self.condition(5)
                        pass

                    elif la_ == 2:
                        localctx = FetchucciniParser.AndConditionContext(self, FetchucciniParser.ConditionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_condition)
                        self.state = 83
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 84
                        self.match(FetchucciniParser.OP_AND)
                        self.state = 85
                        self.condition(4)
                        pass

             
                self.state = 90
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ComparisonContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.left = None # ExpressionContext
            self.op = None # Token
            self.right = None # ExpressionContext

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FetchucciniParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(FetchucciniParser.ExpressionContext,i)


        def OP_EQ(self):
            return self.getToken(FetchucciniParser.OP_EQ, 0)

        def OP_NEQ(self):
            return self.getToken(FetchucciniParser.OP_NEQ, 0)

        def OP_LT(self):
            return self.getToken(FetchucciniParser.OP_LT, 0)

        def OP_LE(self):
            return self.getToken(FetchucciniParser.OP_LE, 0)

        def OP_GT(self):
            return self.getToken(FetchucciniParser.OP_GT, 0)

        def OP_GE(self):
            return self.getToken(FetchucciniParser.OP_GE, 0)

        def getRuleIndex(self):
            return FetchucciniParser.RULE_comparison

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparison" ):
                return visitor.visitComparison(self)
            else:
                return visitor.visitChildren(self)




    def comparison(self):

        localctx = FetchucciniParser.ComparisonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_comparison)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91
            localctx.left = self.expression()
            self.state = 92
            localctx.op = self._input.LT(1)
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 2064384) != 0)):
                localctx.op = self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 93
            localctx.right = self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FetchucciniParser.RULE_expression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class StringExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FetchucciniParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(FetchucciniParser.STRING, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringExpr" ):
                return visitor.visitStringExpr(self)
            else:
                return visitor.visitChildren(self)


    class IdExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FetchucciniParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(FetchucciniParser.ID, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdExpr" ):
                return visitor.visitIdExpr(self)
            else:
                return visitor.visitChildren(self)


    class NumberExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FetchucciniParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUMBER(self):
            return self.getToken(FetchucciniParser.NUMBER, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumberExpr" ):
                return visitor.visitNumberExpr(self)
            else:
                return visitor.visitChildren(self)



    def expression(self):

        localctx = FetchucciniParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_expression)
        try:
            self.state = 98
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [28]:
                localctx = FetchucciniParser.IdExprContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 95
                self.match(FetchucciniParser.ID)
                pass
            elif token in [29]:
                localctx = FetchucciniParser.NumberExprContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 96
                self.match(FetchucciniParser.NUMBER)
                pass
            elif token in [30]:
                localctx = FetchucciniParser.StringExprContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 97
                self.match(FetchucciniParser.STRING)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExportClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.path = None # Token

        def KW_EXPORT(self):
            return self.getToken(FetchucciniParser.KW_EXPORT, 0)

        def KW_AS(self):
            return self.getToken(FetchucciniParser.KW_AS, 0)

        def format_(self):
            return self.getTypedRuleContext(FetchucciniParser.FormatContext,0)


        def KW_TO(self):
            return self.getToken(FetchucciniParser.KW_TO, 0)

        def SEMICOLON(self):
            return self.getToken(FetchucciniParser.SEMICOLON, 0)

        def STRING(self):
            return self.getToken(FetchucciniParser.STRING, 0)

        def getRuleIndex(self):
            return FetchucciniParser.RULE_exportClause

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExportClause" ):
                return visitor.visitExportClause(self)
            else:
                return visitor.visitChildren(self)




    def exportClause(self):

        localctx = FetchucciniParser.ExportClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_exportClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 100
            self.match(FetchucciniParser.KW_EXPORT)
            self.state = 101
            self.match(FetchucciniParser.KW_AS)
            self.state = 102
            self.format_()
            self.state = 103
            self.match(FetchucciniParser.KW_TO)
            self.state = 104
            localctx.path = self.match(FetchucciniParser.STRING)
            self.state = 105
            self.match(FetchucciniParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FormatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_JSON(self):
            return self.getToken(FetchucciniParser.KW_JSON, 0)

        def KW_CSV(self):
            return self.getToken(FetchucciniParser.KW_CSV, 0)

        def getRuleIndex(self):
            return FetchucciniParser.RULE_format

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFormat" ):
                return visitor.visitFormat(self)
            else:
                return visitor.visitChildren(self)




    def format_(self):

        localctx = FetchucciniParser.FormatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_format)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            _la = self._input.LA(1)
            if not(_la==8 or _la==9):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[8] = self.condition_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def condition_sempred(self, localctx:ConditionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 3)
         




