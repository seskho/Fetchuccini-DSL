lexer grammar FetchucciniLexer;

// PALABRAS CLAVE 
KW_FETCH: 'FETCH';
KW_EXTRACT: 'EXTRACT';
KW_FROM: 'FROM';
KW_WHERE: 'WHERE';
KW_EXPORT: 'EXPORT';
KW_AS: 'AS';
KW_TO: 'TO';
KW_JSON: 'JSON';
KW_CSV: 'CSV';
KW_TEXT: 'text';
KW_ATTR: 'attr';
KW_REGEX: 'regex';

// OPERADORES LÓGICOS
OP_AND: 'AND';
OP_OR: 'OR';

// OPERADORES RELACIONALES
OP_EQ: '==';
OP_NEQ: '!=';
OP_LE: '<=';
OP_GE: '>=';
OP_LT: '<';
OP_GT: '>';

// DELIMITADORES Y SIGNOS DE PUNTUACIÓN

LBRACE: '{';
RBRACE: '}';
LPAREN: '(';
RPAREN: ')';
COLON: ':';
COMMA: ',';
SEMICOLON: ';';

// IDENTIFICADORES Y LITERALES
ID: [a-zA-Z_] [a-zA-Z0-9_]*;
NUMBER: [0-9]+ ('.' [0-9]+)?;
STRING: '"' ( ESC_SEQ | ~["\\\r\n])* '"';

fragment ESC_SEQ: '\\' [btnfr"'\\];

// TOKENS DE DESCARTE 
WS: [ \t\r\n]+ -> skip;
COMMENT: '--' ~[\r\n]* -> skip;
