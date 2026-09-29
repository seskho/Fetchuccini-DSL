lexer grammar FetchucciniLexer;

// ==========================================
// 1. PALABRAS CLAVE (Keywords)
// ==========================================
KW_FETCH    : 'FETCH' ;
KW_EXTRACT  : 'EXTRACT' ;
KW_FROM     : 'FROM' ;
KW_WHERE    : 'WHERE' ;
KW_EXPORT   : 'EXPORT' ;
KW_AS       : 'AS' ;
KW_TO       : 'TO' ;
KW_JSON     : 'JSON' ;
KW_CSV      : 'CSV' ;
KW_TEXT     : 'text' ;
KW_ATTR     : 'attr' ;
KW_REGEX    : 'regex' ;

// ==========================================
// 2. OPERADORES LÓGICOS
// ==========================================
OP_AND      : 'AND' ;
OP_OR       : 'OR' ;

// ==========================================
// 3. OPERADORES RELACIONALES
// (Declarar primero los operadores compuestos de dos caracteres)
// ==========================================
OP_EQ       : '==' ;
OP_NEQ      : '!=' ;
OP_LE       : '<=' ;
OP_GE       : '>=' ;
OP_LT       : '<' ;
OP_GT       : '>' ;

// ==========================================
// 4. DELIMITADORES Y SIGNOS DE PUNTUACIÓN
// ==========================================
LBRACE      : '{' ;
RBRACE      : '}' ;
LPAREN      : '(' ;
RPAREN      : ')' ;
COLON       : ':' ;
COMMA       : ',' ;
SEMICOLON   : ';' ;

// ==========================================
// 5. IDENTIFICADORES Y LITERALES
// ==========================================
// Identificador: comienza con letra o guion bajo, seguido de alfanuméricos
ID          : [a-zA-Z_] [a-zA-Z0-9_]* ;

// Literales numéricos enteros o con parte decimal
NUMBER      : [0-9]+ ('.' [0-9]+)? ;

// Literales de cadena con soporte para secuencias de escape estándar
STRING      : '"' ( ESC_SEQ | ~["\\\r\n] )* '"' ;

// Fragmento auxiliar para secuencias de escape en strings
fragment ESC_SEQ 
            : '\\' [btnfr"'\\] ;

// ==========================================
// 6. TOKENS DE DESCARTE (Skip Rules)
// ==========================================
// Espacios en blanco, tabulaciones y saltos de línea
WS          : [ \t\r\n]+ -> skip ;

// Comentarios de una sola línea (estilo SQL: -- ...)
COMMENT     : '--' ~[\r\n]* -> skip ;
