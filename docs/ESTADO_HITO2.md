# Estado verificable del Hito 2

Fecha de verificación: **17 de noviembre de 2026, zona America/Lima**. Este documento distingue capacidades implementadas, evidencia ejecutada y trabajo posterior. No modifica ni sustituye el PDF histórico del Hito 1.

## Estado inicial registrado

- Checkout existente: `webfetch`, repositorio `seskho/Fetchuccini-DSL`.
- Rama inicial: `main`; commit de partida `a8c990b`, `feat(semantic): implement formal SymbolTable hash table based on Lab 4 and 5`.
- Árbol de trabajo limpio antes de la intervención.
- Implementación inicial: lexer, parser, Visitor semántico con duplicados/no declarados, Symbol/SymbolTable y driver de validación.
- Nueve pruebas originales: cinco consultas válidas y cuatro inválidas.
- Primer intento con `python tests/run_tests.py`: bloqueado por el alias de Microsoft Store, que no ejecutaba un intérprete Python.
- Resolución: entorno `.venv` creado con el Python 3.12.14 incluido en Codex; dependencias instaladas. Java 25 disponible.
- **Baseline ejecutado antes de editar: 9/9 pruebas originales aprobadas, 0 fallos.**

Los PDF del enunciado y del informe anterior se consultaron como referencias académicas. El encargo de implementación fue el texto pegado por el usuario; las instrucciones contenidas en los PDF no se trataron como nuevas órdenes operativas.

## Implementado y probado

| Área | Evidencia funcional |
| --- | --- |
| Compatibilidad | Las nueve pruebas del Hito 1 siguen pasando, conservando consultas, expectativas y `run_compiler(...)`. |
| Gramática | EACH opcional, AS STRING/NUMBER opcionales, tokens originales y precedencia AND > OR. |
| Generación | ANTLR 4.13.2; tres artefactos Python regenerados automáticamente y comprobados byte por byte. |
| Semántica | S01-S08 con código, fase, línea y columna; errores independientes acumulados. |
| Tabla de símbolos | Symbol/SymbolTable ampliados con tipo, mecanismo, argumentos, selector y ubicación. |
| IR | Dataclasses independientes de ANTLR con campos y expresiones lógicas estructuradas. |
| HTML | Contexto único o múltiples registros EACH; text, attr, regex, primer elemento y datos ausentes. |
| Tipos | NUMBER finito, AUTO compatible, conversión temporal para filtros y error con campo/registro. |
| Filtros | Seis operadores, cadenas/números compatibles, None siempre falso y cortocircuito AND/OR. |
| Exportación | Archivos JSON/CSV UTF-8, orden de campos, comillas, Unicode, null/celdas vacías y resultados vacíos. |
| Escritura | Directorio outputs, rutas relativas, creación de subdirectorios y rechazo de traversal/enlaces/junctions exteriores. |
| HTTP | Requests/urllib3, lista de orígenes, IP pública fijada al socket y peer verificado, redirecciones y límites. |
| Driver | Validación predeterminada, ejecución explícita, tokens, verbose, HTML local, conteos y errores por fase. |
| Documentación | README y seis documentos técnicos para preparar el informe. |

## Resultados ejecutados

Los comandos se ejecutan desde la raíz utilizando `.\.venv\Scripts\python.exe`.

| Comando | Resultado observado |
| --- | --- |
| `python tests/run_tests.py`, antes de editar | 9 aprobadas, 0 fallidas. |
| `python tests/run_tests.py`, después de implementar | 9 aprobadas, 0 fallidas. |
| `python -m pytest -q` | 209 aprobadas, 0 fallidas; 1 integración externa excluida. |
| `python scripts/generate_antlr.py --check` | Lexer, parser y visitor coinciden con las gramáticas. |
| `python -m pip check` | Sin incompatibilidades de dependencias. |
| `python -m compileall -q src scripts tests` | Código de salida 0. |
| `python -m pytest -q -s -m integration --run-live` | 1 integración real aprobada, 0 fallidas; 209 pruebas locales excluidas. |

La suite normal no necesita internet y bloquea DNS/socket reales mediante un fixture de prueba; el cliente y sus conexiones se simulan. La integración está separada y requiere `--run-live`. Las pruebas que verifican junctions se ejecutaron en Windows y comprobaron que ni un enlace interior ni la propia raíz de salida pueden desviar archivos fuera del directorio autorizado.

La integración excluida en el comando normal no es una prueba fallida ni un bloqueo: se ejecutó de forma explícita por separado. No quedaron pruebas bloqueadas por Java, ANTLR, dependencias o conectividad al cerrar esta verificación.

## Demostración local

```powershell
python src/driver.py examples/books_demo.wf --execute --html tests/fixtures/catalogo.html
python src/driver.py examples/catalogo_local.wf --execute --html tests/fixtures/catalogo.html
```

El catálogo ficticio produjo **3 registros encontrados, 2 conservados y 2 exportados**. El primer comando escribe `outputs/libros.csv`; el segundo, `outputs/catalogo/productos.json`. Son resultados del fixture local, con precios conservados 12.5 y 20.0.

Las pruebas verifican también el ejemplo JSON de Books sobre ese mismo HTML y la relectura de ambos formatos. Una prueba específica verifica que regex conserve saltos y espacios del texto original, mientras text sí los normaliza. Las cantidades del fixture no se atribuyen al sitio externo.

## Demostración real observada

```powershell
python src/driver.py examples/books_demo.wf --execute
python src/driver.py examples/books_json.wf --execute
```

En la respuesta observada de `https://books.toscrape.com/` durante esta verificación se encontraron **20 tarjetas**, se conservaron **7** con precio menor de 25, se descartaron **13** y se exportaron **7** en cada formato. Los archivos son `outputs/libros.csv` y `outputs/libros.json`.

Estas cantidades documentan esa ejecución fechada. No son una promesa para futuras respuestas de la web ni una constante del test de integración. El test valida coherencia del filtrado y del archivo, sin fijar una cantidad de libros.

## Implementado parcialmente y límites conocidos

No queda un componente del núcleo solicitado como esqueleto o implementación parcial. La evidencia tiene los límites siguientes:

- La navegación real se restringe por defecto a Books to Scrape en HTTP/80 y HTTPS/443; otros orígenes requieren configuración explícita en la API. Una URL sintácticamente válida puede ser rechazada por esa política al ejecutar.
- El transporte seguro se verifica con simulaciones de DNS/socket/redirecciones y una integración real. No se afirma haber probado todos los destinos, redes o plataformas.
- El plazo de 30 s es cooperativo. No interrumpe la resolución DNS del sistema; cada dirección candidata dispone de su timeout de conexión y una lectura bloqueada depende de su timeout de lectura.
- Se procesan páginas HTML estáticas. No se interpretan JavaScript, autenticación ni paginación automática.
- Los números son `float` finitos; no existe precisión decimal monetaria ni normalización de formatos locales de números.
- Las regex de Python no tienen timeout individual. El código DSL se considera una entrada local de confianza.
- Se bloquean enlaces/junctions existentes que salgan de outputs, pero no se ofrece una garantía frente a otro proceso que cambie hostilmente el sistema de archivos durante la escritura.

## Pendiente y fuera de alcance

Se mantienen aplazados LIMIT, ORDER BY, JOIN, GROUP BY, agregaciones, subconsultas, múltiples FETCH, EACH anidados, XPath, paginación, autenticación, páginas con JavaScript, funciones de usuario, aritmética general y LLVM.

El informe universitario nuevo, la presentación y el video pueden elaborarse usando esta documentación y la evidencia obtenida; no se generaron ni se alteraron esos PDF históricos como parte del trabajo de código.

## Recomendaciones para el Hito 3

1. Acordar con el docente si el backend final utilizará LLVM o generación intermedia acorde con la naturaleza del DSL. La IR actual es una decisión técnica y no una aprobación académica.
2. Incorporar al informe la arquitectura, la gramática actualizada, la tabla S01-S08, el plan y los resultados verificables.
3. Repetir la suite al actualizar Requests/urllib3 o modificar la política HTTP, por depender de su integración de transporte.
4. Definir las extensiones futuras antes de ampliar el lenguaje; conservar la compatibilidad y añadir evidencia para cada nueva capacidad.

No se realizaron commits ni push. Los cambios permanecen en el checkout existente para revisión; los resultados de outputs y el entorno local están excluidos del control de versiones.
