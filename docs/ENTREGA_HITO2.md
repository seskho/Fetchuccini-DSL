# Entrega técnica del Hito 2

Este documento reúne el inventario del cambio, los comandos de demostración y el material que puede utilizarse para preparar el informe universitario. La evidencia detallada de ejecución está en [ESTADO_HITO2.md](ESTADO_HITO2.md).

## A. Archivos existentes modificados

| Archivo | Motivo |
| --- | --- |
| `grammar/FetchucciniLexer.g4` | Añadir KW_EACH, KW_NUMBER y KW_STRING conservando el léxico anterior. |
| `grammar/FetchucciniParser.g4` | Admitir EACH opcional y anotaciones de tipo manteniendo la precedencia lógica. |
| `src/generated/FetchucciniLexer.py` | Regeneración automática con ANTLR 4.13.2. |
| `src/generated/FetchucciniParser.py` | Regeneración automática conforme al parser actualizado. |
| `src/generated/FetchucciniParserVisitor.py` | Regeneración automática del Visitor con las nuevas reglas. |
| `src/semantic/semantic_checker.py` | Ampliar Symbol/SymbolTable y verificar S01-S08 con ubicación y fase. |
| `src/driver.py` | Integrar compilación/ejecución, HTML local y opciones conservando la tupla histórica. |
| `requirements.txt` | Fijar dependencias HTTP, HTML, selectores y pruebas, además de ANTLR. |
| `.gitignore` | Excluir outputs y conservar su marcador `.gitkeep`. |
| `README.md` | Documentar sintaxis, instalación, ejecución, errores, pruebas, arquitectura y alcance del Hito 2. |

Las nueve consultas del Hito 1 y `tests/run_tests.py` se mantienen sin cambios. Los módulos ANTLR se regeneraron con la herramienta; no se editaron a mano. Los PDF de referencia permanecen intactos.

## B. Archivos nuevos

| Grupo | Archivos |
| --- | --- |
| Compilación | `src/compiler.py`: API de compilación, diagnósticos y resultados. |
| Cadenas y salidas | `src/literals.py`, `src/output_paths.py`. |
| IR | `src/ir/__init__.py`, `src/ir/models.py`, `src/ir/plan_builder.py`. |
| Runtime | `src/runtime/__init__.py`, `src/runtime/errors.py`, `src/runtime/http_client.py`, `src/runtime/html_parser.py`, `src/runtime/extractor.py`, `src/runtime/type_conversion.py`, `src/runtime/filter_engine.py`, `src/runtime/exporter.py`, `src/runtime/execution_engine.py`. |
| Regeneración | `scripts/generate_antlr.py`; `.gitattributes` fija finales de línea para artefactos generados. |
| Ejemplos | `examples/books_demo.wf`, `examples/books_json.wf`, `examples/catalogo_local.wf`. |
| Fixture | `tests/fixtures/catalogo.html`. |
| S01-S04 | `tests/invalid/S01_alias_duplicado.wf`, `S02_campo_no_declarado.wf`, `S03_url_invalida.wf`, `S04_selector_invalido.wf`. |
| S05-S08 | `tests/invalid/S05_regex_invalida.wf`, `S06_atributo_vacio.wf`, `S07_extension_incompatible.wf`, `S08_tipos_incompatibles.wf`. |
| Suite | `pytest.ini`, `tests/conftest.py`, `tests/test_frontend.py`, `tests/test_driver.py`, `tests/test_runtime.py`, `tests/test_extractor_regex.py`, `tests/test_http_client.py`, `tests/test_output_paths.py`, `tests/test_integration_live.py`. |
| Documentación | `docs/ARQUITECTURA_HITO2.md`, `docs/GRAMATICA_HITO2.md`, `docs/SEMANTICA_HITO2.md`, `docs/PLAN_VALIDACION_HITO2.md`, `docs/ESTADO_HITO2.md`, `docs/ENTREGA_HITO2.md`. |
| Directorio de resultados | `outputs/.gitkeep`. Los resultados JSON/CSV son archivos reales ignorados por Git. |

El entorno `.venv`, el JAR almacenado en `.antlr/` y los resultados generados son recursos locales de ejecución, no código fuente nuevo que deba incluirse en un commit.

## C. Funcionalidades implementadas

Fetchuccini valida una consulta completa antes de ejecutarla. Puede seleccionar registros con EACH, extraer texto/atributos/regex dentro de cada registro, convertir NUMBER, filtrar con operadores relacionales y AND/OR y generar JSON o CSV reales. Las consultas anteriores usan AUTO y conservan su aceptación.

Los errores se separan por fase: IO de entrada, léxico, sintáctico, semántico y runtime. Las comparaciones conocidas incompatibles se rechazan en compilación; las conversiones imposibles dependientes del HTML indican campo y registro al ejecutar. None siempre produce falso en comparación, incluso con `!=`, y se serializa como null o celda vacía.

El runtime consume la IR, permite un cliente simulado y aplica una política HTTP restringida con IP efectiva verificada. Las salidas permanecen bajo outputs. No se ejecutan expresiones mediante código dinámico.

## D. Resultados de pruebas

La regresión original aprobó **9/9 antes y después**. La suite local aprobó **209 pruebas, 0 fallidas**, con la integración externa excluida del comando normal. La integración real se ejecutó por separado y aprobó **1 prueba, 0 fallidas**. La regeneración ANTLR coincidió en los tres módulos, `pip check` no reportó incompatibilidades y `compileall` terminó con código 0.

```powershell
.\.venv\Scripts\python.exe tests/run_tests.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts/generate_antlr.py --check
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m compileall -q src scripts tests
.\.venv\Scripts\python.exe -m pytest -q -s -m integration --run-live
```

No quedaron pruebas bloqueadas al finalizar. El problema inicial del alias `python` de Windows se resolvió con el entorno virtual. La prueba real no establece cantidades fijas de libros como condición de éxito.

## E. Comandos exactos de demostración

Desde la raíz del repositorio, en PowerShell. Estos comandos usan directamente el intérprete del entorno para evitar el alias de Microsoft Store.

```powershell
# 1. Validar una consulta del Hito 1
.\.venv\Scripts\python.exe src/driver.py tests/valid/01_consulta_basica.wf

# 2. Mostrar tokens (--verbose también muestra símbolos y plan)
.\.venv\Scripts\python.exe src/driver.py tests/valid/01_consulta_basica.wf --tokens
.\.venv\Scripts\python.exe src/driver.py tests/valid/01_consulta_basica.wf --verbose

# 3. Validar EACH sin HTTP ni exportación
.\.venv\Scripts\python.exe src/driver.py examples/books_demo.wf --validate-only

# 4. Detectar S05; debe finalizar con código 1
.\.venv\Scripts\python.exe src/driver.py tests/invalid/S05_regex_invalida.wf

# 5. Extraer el catálogo local y generar JSON
.\.venv\Scripts\python.exe src/driver.py examples/catalogo_local.wf --execute --html tests/fixtures/catalogo.html

# 6. Extraer la página real de Books to Scrape y generar CSV
.\.venv\Scripts\python.exe src/driver.py examples/books_demo.wf --execute

# 7. Generar JSON real; escribe outputs/libros.json
.\.venv\Scripts\python.exe src/driver.py examples/books_json.wf --execute

# 8. Generar CSV reproducible desde HTML local; escribe outputs/libros.csv
.\.venv\Scripts\python.exe src/driver.py examples/books_demo.wf --execute --html tests/fixtures/catalogo.html

# 9. Ejecutar toda la suite local y la regresión histórica
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe tests/run_tests.py

# Integración externa optativa y correspondencia de ANTLR
.\.venv\Scripts\python.exe -m pytest -q -s -m integration --run-live
.\.venv\Scripts\python.exe scripts/generate_antlr.py --check
```

La demostración local observó 3 encontrados, 2 conservados y 2 exportados. La web real observada el 17 de noviembre de 2026 produjo 20 encontrados, 7 conservados, 13 descartados y 7 exportados. Una ejecución posterior puede obtener otros valores; debe informarse lo observado.

Los comandos que usan el mismo destino reemplazan su contenido al completar una nueva exportación. Así, ejecutar la variante local después de la real vuelve a escribir `outputs/libros.csv` con los dos registros del fixture.

## F. Estado y Hito 3

El núcleo solicitado del Hito 2 está implementado y probado. Los límites operativos son HTML estático, un origen por consulta, orígenes HTTP autorizados, float finito, plazo HTTP cooperativo y regex sin timeout individual. No quedan componentes parciales del núcleo ni bloqueos técnicos activos.

Las funcionalidades expresamente aplazadas siguen pendientes: LIMIT, ORDER BY, JOIN, GROUP BY, agregaciones, subconsultas, múltiples FETCH, EACH anidados, XPath, paginación, autenticación, JavaScript, funciones de usuario, aritmética general y LLVM. No se añadieron durante este avance.

Para el Hito 3 se recomienda acordar con el docente la alternativa de generación de código, completar el informe y la evidencia de validación y preparar presentación/video. La IR actual no se presenta como una sustitución formal de LLVM aprobada por el profesor.

## G. Observaciones para actualizar el informe del Hito 1

El informe histórico se conserva. Para elaborar un documento nuevo, los cambios se corresponden con sus secciones reales:

| Sección histórica | Cambio para el informe del Hito 2 |
| --- | --- |
| 1. Problemática y Motivación | Conservar el problema; explicar cómo EACH asocia campos de una tarjeta y evita combinar datos de distintos productos. |
| 2. Objetivos | Ampliar de front-end preliminar a semántica completa, IR, ejecución controlada, exportación y validación por niveles. |
| 3. Construcciones / 3.1 Alcance | Pasar de cuatro a cinco construcciones; añadir EACH y AS STRING/NUMBER y separar capacidad reconocida de ejecución real. |
| 4. Analizador Léxico | Añadir los tres tokens reservados: 33 terminales significativos frente a los 30 históricos; distinguir KW_NUMBER de NUMBER y KW_STRING de STRING. |
| 5. Analizador Sintáctico | Actualizar orden global, reglas opcionales y derivaciones; mantener AND > OR y mostrar correspondencia con ANTLR. |
| 6. Analizador Semántico Preliminar | Renombrar como análisis semántico del Hito 2; sustituir dos reglas por S01-S08, tipos y acumulación con código/fase/posición. |
| Estrategia de tabla de símbolos | Corregir la descripción histórica de un conjunto de alias: el código de partida ya usaba Symbol/SymbolTable sobre dict; ahora incorpora tipos y metadatos. |
| Anexo A. Ejemplos | Mantener los ejemplos anteriores y añadir EACH, campos anotados y consulta completa local/Books. |
| Anexo B. Léxico | Actualizar tabla y fuente `.g4`; documentar escapes y decodificación Unicode. |
| Anexo C. GLC | Incorporar EachOpt y TypeOpt, con sus alternativas vacías y la estructura global. |
| Anexo D. Derivaciones | Ajustar los pasos de consultas históricas para las opciones vacías; añadir una derivación con EACH y tipo. |
| Anexo E. Parser ANTLR4 | Usar la gramática actual y el comando reproducible de generación 4.13.2. |
| Anexo F. Semántica y pruebas | Incluir ocho fixtures, fases esperadas, pruebas locales y resultados observados. |
| Nuevas secciones | Arquitectura, IR, runtime, plan de validación, resultados, límites y pendientes del Hito 3. |

Pueden documentarse los resultados realmente ejecutados de [ESTADO_HITO2.md](ESTADO_HITO2.md), las salidas locales y reales observadas y las propiedades específicas cubiertas por tests. No debe presentarse el conteo de la web como constante ni atribuir al sistema soporte para XPath, JavaScript, paginación o LLVM.

El enunciado académico requiere para Hito 2 gramática actualizada, al menos seis errores semánticos, arquitectura y plan de validación conservando lo anterior. Esta implementación documenta ocho reglas. La generación intermedia sin LLVM para el Hito 3 depende de la consulta al docente indicada en el enunciado; no se asume su aprobación.

Los cambios permanecen sin commit ni push en el checkout original. El hecho de trabajar en la rama `main` no implicó publicar o fusionar modificaciones.
