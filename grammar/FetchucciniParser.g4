parser grammar FetchucciniParser;

options {
    tokenVocab = FetchucciniLexer;
}

program
    : query EOF
    ;

query
    : fetchClause eachClause? extractClause whereClause? exportClause
    ;

fetchClause
    : KW_FETCH url=STRING
    ;

eachClause
    : KW_EACH selector=STRING
    ;

extractClause
    : KW_EXTRACT LBRACE fieldList RBRACE
    ;

fieldList
    : fieldDef (COMMA fieldDef)*
    ;

fieldDef
    : alias=ID COLON extractor KW_FROM selector=STRING typeAnnotation?
    ;

typeAnnotation
    : KW_AS (KW_NUMBER | KW_STRING)
    ;

extractor
    : KW_TEXT                               # TextExtractor
    | KW_ATTR LPAREN attrName=STRING RPAREN # AttrExtractor
    | KW_REGEX LPAREN pattern=STRING RPAREN # RegexExtractor
    ;

whereClause
    : KW_WHERE condition
    ;

condition
    : conditionAnd (OP_OR conditionAnd)*
    ;

conditionAnd
    : comparison (OP_AND comparison)*
    ;

comparison
    : left=expression relOp right=expression
    ;

relOp
    : OP_EQ
    | OP_NEQ
    | OP_LT
    | OP_LE
    | OP_GT
    | OP_GE
    ;

expression
    : ID        # IdExpr
    | NUMBER    # NumberExpr
    | STRING    # StringExpr
    ;

exportClause
    : KW_EXPORT KW_AS format KW_TO path=STRING SEMICOLON
    ;

format
    : KW_JSON
    | KW_CSV
    ;
