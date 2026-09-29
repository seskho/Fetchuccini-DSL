parser grammar FetchucciniParser;

options {
    tokenVocab = FetchucciniLexer;
}

// ==========================================
// Regla inicial del programa
// ==========================================
program
    : query EOF
    ;

// ==========================================
// Estructura de una consulta Fetchuccini
// ==========================================
query
    : fetchClause extractClause whereClause? exportClause
    ;

// ==========================================
// 1. Cláusula FETCH
// ==========================================
fetchClause
    : KW_FETCH url=STRING
    ;

// ==========================================
// 2. Cláusula EXTRACT
// ==========================================
extractClause
    : KW_EXTRACT LBRACE fieldList RBRACE
    ;

fieldList
    : fieldDef (COMMA fieldDef)*
    ;

fieldDef
    : alias=ID COLON extractor KW_FROM selector=STRING
    ;

extractor
    : KW_TEXT                             # TextExtractor
    | KW_ATTR LPAREN attrName=STRING RPAREN # AttrExtractor
    | KW_REGEX LPAREN pattern=STRING RPAREN # RegexExtractor
    ;

// ==========================================
// 3. Cláusula WHERE (Opcional)
// Precedencia: AND tiene mayor prioridad que OR
// ==========================================
whereClause
    : KW_WHERE condition
    ;

condition
    : condition OP_OR condition          # OrCondition
    | condition OP_AND condition         # AndCondition
    | LPAREN condition RPAREN            # GroupCondition
    | comparison                         # RelationalCondition
    ;

comparison
    : left=expression op=(OP_EQ | OP_NEQ | OP_LT | OP_LE | OP_GT | OP_GE) right=expression
    ;

expression
    : ID                                  # IdExpr
    | NUMBER                              # NumberExpr
    | STRING                              # StringExpr
    ;

// ==========================================
// 4. Cláusula EXPORT
// ==========================================
exportClause
    : KW_EXPORT KW_AS format KW_TO path=STRING SEMICOLON
    ;

format
    : KW_JSON
    | KW_CSV
    ;
