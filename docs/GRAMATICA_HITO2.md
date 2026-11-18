# Gramática de Fetchuccini para el Hito 2

## Fuente de verdad y cambios

La sintaxis implementada está en `grammar/FetchucciniLexer.g4` y `grammar/FetchucciniParser.g4`. Se conserva el lenguaje del Hito 1 y se añaden selección de registros con EACH, anotación del tipo de un campo y agrupación lógica con paréntesis.

| Elemento | Hito 1 | Hito 2 |
| --- | --- | --- |
| Consulta | FETCH EXTRACT WHERE? EXPORT | FETCH EACH? EXTRACT WHERE? EXPORT |
| Campo | Alias, extractor y selector | Los mismos, con tipo opcional. |
| Tipos | Sin anotación | AS STRING, AS NUMBER; AUTO interno por omisión. |
| Lógica | AND con mayor precedencia que OR | Conservada; paréntesis para cambiar la agrupación. |
| Extractores | text, attr y regex | Conservados. |
| Terminación | Punto y coma obligatorio | Conservada. |

## Léxico

Se añaden antes de `ID`:

```antlr
KW_EACH   : 'EACH';
KW_NUMBER : 'NUMBER';
KW_STRING : 'STRING';
```

`KW_NUMBER` identifica el nombre del tipo y `NUMBER` un literal numérico. De igual forma, `KW_STRING` representa el nombre del tipo y `STRING` un literal entre comillas. Se mantienen las palabras reservadas, operadores y delimitadores anteriores. El lexer tiene 35 reglas de token, incluidas WS y COMMENT; se emiten 33 tipos de token significativos, frente a los 30 del Hito 1.

Los identificadores usan `[a-zA-Z_][a-zA-Z0-9_]*`. Los números son enteros o decimales sin signo, con al menos un dígito a cada lado del punto. No se incorporan exponentes ni operaciones aritméticas. Las palabras clave son sensibles a mayúsculas.

Las cadenas conservan los escapes del Hito 1: `\b`, `\t`, `\n`, `\f`, `\r`, `\"`, `\'` y `\\`. Su decodificación explícita conserva los caracteres Unicode literales. Una regex que necesite la secuencia `\d` debe usar dos barras en el código DSL: `regex("\\d+")`. Un escape inexistente se detecta en el lexer; no se interpreta silenciosamente.

Los espacios en blanco y los comentarios iniciados con `--` se descartan. Las cadenas no admiten saltos de línea sin escape.

## Reglas del parser

La estructura actualizada es:

```antlr
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
    : KW_TEXT
    | KW_ATTR LPAREN STRING RPAREN
    | KW_REGEX LPAREN STRING RPAREN
    ;

whereClause
    : KW_WHERE condition
    ;

condition
    : conditionAnd (OP_OR conditionAnd)*
    ;

conditionAnd
    : conditionPrimary (OP_AND conditionPrimary)*
    ;

conditionPrimary
    : comparison
    | LPAREN condition RPAREN
    ;

comparison
    : left=expression relOp right=expression
    ;

expression
    : ID | NUMBER | STRING
    ;

relOp
    : OP_EQ | OP_NEQ | OP_LT | OP_LE | OP_GT | OP_GE
    ;

exportClause
    : KW_EXPORT KW_AS format KW_TO path=STRING SEMICOLON
    ;

format
    : KW_JSON | KW_CSV
    ;
```

Este fragmento omite únicamente las etiquetas de alternativas y algunos nombres de tokens auxiliares de los extractores; los archivos `.g4` contienen la versión exacta usada para generar Python.

## Forma equivalente de las extensiones en GLC

Las nuevas opciones pueden escribirse sin los operadores EBNF `?`:

```text
Query ::= FetchClause EachOpt ExtractClause WhereOpt ExportClause
EachOpt ::= EachClause | ε
EachClause ::= KW_EACH STRING
FieldDef ::= ID COLON Extractor KW_FROM STRING TypeOpt
TypeOpt ::= KW_AS Type | ε
Type ::= KW_NUMBER | KW_STRING
```

La omisión de EACH deriva `EachOpt ⇒ ε`, y la omisión del tipo deriva `TypeOpt ⇒ ε`. Por eso toda consulta del Hito 1 mantiene una derivación equivalente y sus campos reciben AUTO durante el análisis.

Una derivación local más a la izquierda para un campo anotado es:

```text
FieldDef
⇒ ID COLON Extractor KW_FROM STRING TypeOpt
⇒ ID COLON KW_REGEX LPAREN STRING RPAREN KW_FROM STRING TypeOpt
⇒ ID COLON KW_REGEX LPAREN STRING RPAREN KW_FROM STRING KW_AS Type
⇒ ID COLON KW_REGEX LPAREN STRING RPAREN KW_FROM STRING KW_AS KW_NUMBER
```

La instancia de lexemas `precio: regex("[0-9.]+") FROM ".price" AS NUMBER` utiliza esa secuencia terminal. Las cuatro derivaciones históricas del informe siguen describiendo el subconjunto sin EACH ni anotación; para el informe nuevo deben actualizarse las reglas globales e introducir las opciones vacías correspondientes.

## Precedencia y cortocircuito

`condition` combina unidades `conditionAnd` mediante OR. Cada unidad interna combina comparaciones mediante AND. Así, `A OR B AND C` tiene estructura `Or(A, And(B, C))`. El constructor de la IR conserva esa estructura y el runtime la recorre con cortocircuito.

Se admite agrupación lógica con paréntesis anidados mediante `conditionPrimary`. Así, `(A OR B) AND C` produce `And(Or(A, B), C)`. Sin paréntesis, se conserva AND > OR. Los grupos deben contener condiciones completas; no se admiten grupos vacíos ni paréntesis alrededor de operandos aislados.

## Ejemplos válidos

Consulta compatible con el Hito 1:

```text
FETCH "https://example.com"
EXTRACT { titulo: text FROM "h1" }
EXPORT AS JSON TO "datos.json";
```

Consulta con EACH y tipos:

```text
FETCH "https://books.toscrape.com/"
EACH "article.product_pod"
EXTRACT {
    titulo: attr("title") FROM "h3 a" AS STRING,
    precio: regex("[0-9.]+") FROM ".price_color" AS NUMBER
}
WHERE precio >= 10 AND precio < 25
EXPORT AS CSV TO "catalogo/libros.csv";
```

Validez sintáctica o semántica no garantiza autorización HTTP: la lista de orígenes permitidos pertenece al runtime.

## Ejemplos inválidos y fase correspondiente

| Entrada o fragmento | Fase | Motivo |
| --- | --- | --- |
| `EACH "article" FETCH "https://example.com" ...` | Sintáctica | EACH aparece antes de FETCH. |
| Dos cláusulas EACH | Sintáctica | La regla admite como máximo una. |
| `EXTRACT {}` | Sintáctica | `fieldList` exige al menos un campo. |
| `titulo: text FROM "h1" AS BOOLEAN` | Sintáctica | Tipo no incluido en `typeAnnotation`. |
| `WHERE (precio < 10` | Sintáctica | Falta cerrar el grupo lógico. |
| Falta el `;` final | Sintáctica | EXPORT debe terminar la consulta. |
| `FETCH "ftp://example.com" ...` | Semántica, S03 | La estructura usa STRING, pero el esquema no está admitido. |
| `EACH "div["` | Semántica, S04 | Es una cadena válida, pero un selector inválido. |

## Regeneración y correspondencia

```powershell
python scripts/generate_antlr.py
python scripts/generate_antlr.py --check
```

El script descarga o utiliza el JAR oficial 4.13.2, comprueba su SHA-256 y genera lexer, parser y visitor para Python. La opción `--check` compara los tres módulos generados byte por byte contra los archivos versionados; no modifica el código versionado. Requiere Java y un JAR disponible localmente o conectividad para la descarga inicial.

Las pruebas separan reconocimiento léxico, estructura sintáctica, validaciones semánticas y construcción de IR. No se usa un fallo sintáctico para demostrar un diagnóstico S01-S08.
