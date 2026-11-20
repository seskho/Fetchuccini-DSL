# Semántica de Fetchuccini para el Hito 2

## Objetivo, fases y diagnósticos

El análisis semántico valida el significado de una consulta que ya superó lexer y parser. Sus ocho reglas se implementan en `FetchucciniSemanticChecker`, reutilizando las clases `Symbol` y `SymbolTable` del Hito 1.

Cada `SemanticError` expone `code`, `message`, `line`, `column` y `phase="semantic"`. Las líneas comienzan en 1 y las columnas en 0, conforme a ANTLR. El formato visible es:

```text
[S05] Error semántico en línea 3, columna 18: La expresión regular del campo 'precio' no es válida: ...
```

La ubicación corresponde al token relevante de la consulta real. Los ejemplos de mensaje de este documento describen su contenido; la posición y el detalle de las bibliotecas dependen de cada entrada. La suite comprueba el código concreto y los metadatos.

Se acumulan errores independientes. Un identificador inexistente produce S02 y no provoca además un S08 derivado de no conocer su tipo. No se ejecuta HTTP, extracción ni exportación si alguna fase de compilación falla.

## S01. Alias duplicado

**Justificación y regla:** cada columna de salida necesita una identidad inequívoca. Un alias se declara una sola vez dentro de EXTRACT; la tabla conserva la primera declaración.

```text
EXTRACT {
    titulo: text FROM "h1",
    titulo: text FROM "h2"
}
```

Mensaje esperado: `[S01] ... El campo 'titulo' ya fue definido en EXTRACT`. La posición señala el segundo alias.

Prueba asociada: `tests/invalid/S01_alias_duplicado.wf`, comprobada por `test_semantic_fixture_reports_exact_code_and_location` en `tests/test_frontend.py`. También se conservan el caso duplicado y la interfaz histórica del Hito 1.

## S02. Campo no declarado en WHERE

**Justificación y regla:** WHERE solo puede resolver columnas existentes en el registro. Todo identificador usado en cualquiera de los dos operandos debe haberse declarado en EXTRACT.

```text
EXTRACT { titulo: text FROM "h1" }
WHERE precio > 10
```

Mensaje esperado: `[S02] ... El campo 'precio' no existe en EXTRACT`. La posición señala el identificador no declarado.

Prueba asociada: `tests/invalid/S02_campo_no_declarado.wf`, comprobada por el test parametrizado de diagnósticos. La visita verifica también el reinicio del checker entre consultas.

## S03. URL no admitida

**Justificación y regla:** FETCH describe una fuente web HTTP o HTTPS con hostname válido y, cuando corresponde, puerto entre 1 y 65535. No se admiten credenciales, espacios ni caracteres de control. Los nombres de dominio se validan por etiquetas y admiten IDNA; las direcciones IP deben ser sintácticamente válidas.

```text
FETCH "ftp://example.com"
```

Mensaje esperado: `[S03] ... FETCH requiere una URL HTTP o HTTPS con hostname válido`.

Prueba asociada: `tests/invalid/S03_url_invalida.wf`. Las pruebas adicionales incluyen hostname ausente, etiquetas inválidas, IPv4 inválida y puertos incorrectos.

Esta comprobación no resuelve DNS ni realiza conexiones. Una URL como `http://localhost` tiene sintaxis válida, pero el cliente HTTP la rechaza en ejecución por su destino o por no pertenecer a un origen autorizado. Son responsabilidades distintas.

## S04. Selector CSS inválido

**Justificación y regla:** la selección debe poder compilarse con Soup Sieve, motor utilizado también para ejecutar los selectores. Se valida el selector de EACH y cada selector de EXTRACT.

```text
EACH "article.product_pod"
EXTRACT { titulo: text FROM "div[" }
```

Mensaje esperado: `[S04] ... El selector CSS del campo 'titulo' no es válido: ...`. Para EACH, se identifica esa cláusula.

Prueba asociada: `tests/invalid/S04_selector_invalido.wf`. Se incluyen también EACH inválido y selector vacío. Un selector CSS válido que no encuentre elementos no es un error: produce cero registros en EACH o `None` en un campo.

## S05. Expresión regular inválida

**Justificación y regla:** el patrón de `regex(...)`, una vez decodificada la cadena DSL, debe compilar con `re.compile`. Se detecta antes de obtener HTML.

```text
EXTRACT { precio: regex("[0-9") FROM ".price" }
```

Mensaje esperado: `[S05] ... La expresión regular del campo 'precio' no es válida: ...`.

Prueba asociada: `tests/invalid/S05_regex_invalida.wf`. La suite prueba por separado una regex válida sin coincidencias y el escape de barras; ninguno se utiliza como falso ejemplo de S05.

## S06. Nombre de atributo vacío

**Justificación y regla:** `attr(...)` necesita un nombre de atributo utilizable. Se decodifica la cadena y se eliminan espacios externos; el resultado no puede estar vacío.

```text
EXTRACT { enlace: attr("   ") FROM "a" }
```

Mensaje esperado: `[S06] ... El nombre de atributo del campo 'enlace' está vacío`.

Prueba asociada: `tests/invalid/S06_atributo_vacio.wf`, más la variante formada por espacios en `tests/test_frontend.py`. Que un atributo válido no exista en el elemento produce `None` durante la extracción.

## S07. Formato, extensión o ruta incompatibles

**Justificación y regla:** el contrato de salida debe ser coherente y permanecer dentro de outputs. JSON requiere `.json` y CSV `.csv`, sin distinguir mayúsculas de la extensión. El nombre debe ser relativo y seguro en Windows y POSIX.

```text
EXPORT AS JSON TO "datos.csv";
```

Mensaje esperado: `[S07] ... El formato JSON requiere la extensión .json.`

También se rechazan `../datos.json`, rutas absolutas, unidades de Windows, UNC, segmentos vacíos o `.`, caracteres de control, flujos alternativos y nombres reservados como `CON.json`. Los subdirectorios relativos válidos se crean solo al ejecutar.

Prueba asociada: `tests/invalid/S07_extension_incompatible.wf`; `tests/test_output_paths.py` amplía la cobertura de rutas. Los enlaces o junctions que existan al ejecutar se resuelven de nuevo y no pueden desviar la escritura fuera de la raíz autorizada. Un error de permisos o disco se reporta como R04 del runtime, no como S07.

## S08. Tipos incompatibles en una comparación

**Justificación y regla:** no deben aceptarse operaciones cuya incompatibilidad ya puede demostrarse durante la compilación. La tabla de símbolos distingue STRING, NUMBER y AUTO.

```text
EXTRACT { titulo: text FROM "h1" AS STRING }
WHERE titulo > 10
```

Mensaje esperado: `[S08] ... El operador '>' requiere operandos numéricos o convertibles; no admite campos AS STRING`.

Para `<`, `<=`, `>` y `>=` se permiten NUMBER, AUTO y literales STRING convertibles a número finito. Un campo declarado STRING se rechaza, aunque sus datos pudieran parecer numéricos. Para `==` y `!=`, dos tipos conocidos distintos STRING/NUMBER se rechazan; AUTO pospone la decisión hasta disponer de datos. Un literal NUMBER fuera del rango finito también produce S08.

Prueba asociada: `tests/invalid/S08_tipos_incompatibles.wf`. Las pruebas adicionales verifican comparación de campos AUTO con literales numéricos, literales convertibles en ordenamientos, igualdad incompatible y desbordamiento.

## Extracción, conversión y ausencias

| Situación | Resultado |
| --- | --- |
| Sin EACH | El documento completo es un contexto. |
| EACH con N coincidencias | N registros, manteniendo el orden del HTML. |
| EACH sin coincidencias | Lista vacía. |
| `text` | Texto del primer elemento, con espacios normalizados. |
| `attr("nombre")` | Atributo del primer elemento; los atributos multivalor se unen con espacios. |
| `regex("patrón")` | Primera coincidencia completa sobre el texto original sin normalizar espacios ni saltos; no solo un grupo capturado. |
| Selector sin coincidencia, atributo ausente o regex sin coincidencia | `None`. |
| Campo NUMBER ausente | `None`; no se intenta convertirlo. |
| Campo NUMBER presente | `float` finito o error R02. |
| Campo STRING o AUTO presente | Texto. |

Los errores de conversión indican campo e índice del registro, empezando en 1. Una conversión fallida detiene la ejecución antes de reemplazar una exportación anterior.

En comparaciones, AUTO se convierte temporalmente a número cuando el otro valor es numérico o el operador requiere ordenamiento numérico. Si ambos valores se comparan como cadenas mediante `==` o `!=`, se usa igualdad textual. La conversión temporal no cambia el dato exportado.

| Operación con `None` en cualquier operando | Resultado |
| --- | --- |
| `==`, `!=`, `<`, `<=`, `>`, `>=` | Falso. |
| Serialización JSON | `null`. |
| Serialización CSV | Celda vacía. |

No se incorpora un literal NULL. El error semántico describe lo que se conoce por el programa; el error runtime describe incompatibilidades que dependen del HTML recibido.

## Evaluación lógica

AND posee mayor precedencia que OR y ambos evalúan de izquierda a derecha con cortocircuito. Un AND deja de evaluar al primer falso; un OR, al primer verdadero. Esto evita conversiones de operandos que no son necesarias para decidir la condición completa.

La precedencia se preserva en nodos de la IR. No se concatena código ni se utilizan `eval()` o `exec()` para procesar expresiones del usuario.

## Evidencia y alcance

Los ocho archivos S01-S08 son consultas completas sintácticamente válidas. La prueba parametrizada exige exactamente el código esperado y la fase semántica. Un caso adicional concentra ocho errores independientes para comprobar su acumulación segura.

Los resultados de ejecución se registran en [ESTADO_HITO2.md](ESTADO_HITO2.md); el procedimiento para reproducirlos está en [PLAN_VALIDACION_HITO2.md](PLAN_VALIDACION_HITO2.md).
