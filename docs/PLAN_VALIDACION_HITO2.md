# Plan de validación de Fetchuccini para el Hito 2

## Objetivos y criterio general

Comprobar que las consultas del Hito 1 conservan su comportamiento, que EACH y los tipos se reconocen correctamente, que S01-S08 se detectan en la fase correspondiente y que la IR puede ejecutarse sobre HTML controlado para producir archivos JSON y CSV verificables.

La aceptación exige pruebas reproducibles sin internet. Una integración externa complementa esa evidencia cuando se ejecuta explícitamente; la disponibilidad o los cambios de una página no determinan la aprobación de la suite local.

## Entorno y entradas

- Python 3.10 o superior y dependencias fijadas en `requirements.txt`.
- Java y el JAR ANTLR 4.13.2 para verificar correspondencia de artefactos.
- Cinco consultas válidas y cuatro inválidas del Hito 1, preservadas.
- Ocho archivos semánticos nuevos en `tests/invalid/S01_...` a `S08_...`.
- HTML ficticio `tests/fixtures/catalogo.html`, con tres productos y datos conocidos.
- Consultas `examples/catalogo_local.wf`, `examples/books_demo.wf` y `examples/books_json.wf`.
- Directorios temporales para exportaciones de las pruebas; no se depende de resultados anteriores.

La suite normal excluye la prueba marcada `integration` salvo que se indique `--run-live`. El cliente real se reemplaza por simulaciones en las pruebas de extracción, filtros, fallos de HTTP y controles de conexión.

## Niveles y matriz de validación

| Nivel / archivo | Entradas principales | Resultado esperado y aceptación |
| --- | --- | --- |
| Regresión, `tests/run_tests.py` | Las nueve consultas originales. | Cinco éxitos y cuatro rechazos en su fase histórica; 9/9. |
| Lexer, `tests/test_frontend.py` | EACH, NUMBER y STRING como palabras clave; identificadores, comentarios, Unicode, operadores y escapes. | Tokens correctos y descarte de comentarios; las cadenas se decodifican sin corromper Unicode o regex. |
| Parser, `tests/test_frontend.py` | EACH opcional, anotaciones presentes/ausentes y WHERE opcional. | Consultas válidas producen plan; orden incorrecto, EACH repetido, tipos inexistentes, EXTRACT vacío o falta de `;` fallan en sintaxis. |
| Semántica, `tests/test_frontend.py` | Un archivo completo por S01-S08 y variaciones de URL/tipos/selectores. | Código exacto, fase semantic y ubicación; ningún plan en caso de fallo. |
| Acumulación semántica | Consulta que incumple ocho reglas independientes. | Se reportan S01-S08 sin errores derivados por tipos de campos no declarados. |
| Tabla de símbolos | Campos con mecanismos, tipos y posiciones; reutilización del checker. | Metadatos correctos, primera declaración conservada y estado reiniciado por consulta. |
| IR, `tests/test_frontend.py` | Consulta completa con campos text/attr/regex y OR combinado con AND. | URL, EACH, campos, argumentos, tipos, filtro y destino idénticos al programa; OR contiene un AND interno. |
| Extracción, `tests/test_runtime.py` | Fixture local y cliente simulado. | Asociación correcta de campos por producto, texto normalizado, primer elemento y primera coincidencia regex completa. |
| Regex y espacios, `tests/test_extractor_regex.py` | Texto con saltos de línea y varios espacios, usando text y regex sobre el mismo elemento. | Solo text normaliza; regex aplica el patrón al texto original y devuelve la primera coincidencia completa. |
| Ausencias | CSS sin coincidencia, atributo ausente y regex sin coincidencia. | None, sin error gramatical; todas las comparaciones con None son falsas. |
| Tipos runtime | NUMBER válido, texto AUTO, valores inválidos, NaN e infinito. | Números finitos, conversiones temporales de AUTO y error R02 con campo/registro cuando no se puede convertir. |
| Lógica runtime | AND, OR y expresiones con resultados que dependen de la precedencia. | Evaluación AND > OR, agrupación con paréntesis anidados, orden de registros conservado y cortocircuito real. |
| JSON | Registros con texto Unicode, números y ausencias. | Lista de objetos UTF-8, números JSON y null. |
| CSV | Datos con comas, comillas, Unicode y ausencias. | Encabezados en orden, una fila por registro, comillas correctas y celdas vacías para None. |
| Resultados vacíos | EACH sin coincidencias y filtros sin registros conservados. | JSON válido vacío y CSV con encabezados. |
| Rutas, `tests/test_output_paths.py` | Rutas POSIX/Windows, traversal, unidades, UNC, caracteres inválidos, enlaces y junctions. | Rechazo de destinos inseguros, admisión de subdirectorios relativos y ninguna escritura exterior. |
| Fallos de disco | Error de permisos simulado durante exportación. | Fase runtime, R04; no se presenta como S07. |
| HTTP, `tests/test_http_client.py` | Respuestas, conexión, DNS y sockets simulados. | Timeouts, errores HTTP, tamaño, redirecciones, origen autorizado, rechazo de direcciones no públicas y verificación del peer. |
| Driver, `tests/test_driver.py` | Validación, ejecución local, opciones CLI y errores por fase. | Sin HTTP/archivos al validar o fallar compilación; tupla histórica conservada, runtime separado y conteos correctos. |
| Independencia del directorio actual | Driver ejecutado desde directorio temporal. | Importaciones y validación correctas; salida predeterminada asociada a la raíz del proyecto. |
| Artefactos ANTLR | Gramáticas actuales y JAR 4.13.2 verificado. | Tres módulos Python idénticos byte por byte tras regeneración temporal. |
| Integración optativa, `tests/test_integration_live.py` | Books to Scrape real. | Existen registros, precios conservados <25 y CSV coherente con los registros; sin cantidades de libros fijadas. |

## Procedimiento reproducible

Desde la raíz del repositorio, usando el entorno virtual:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe tests/run_tests.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts/generate_antlr.py --check
```

Si se desea aislar un nivel:

```powershell
python -m pytest tests/test_frontend.py -q
python -m pytest tests/test_runtime.py tests/test_extractor_regex.py tests/test_driver.py -q
python -m pytest tests/test_http_client.py tests/test_output_paths.py -q
```

La verificación ANTLR requiere Java y JAR oficial. El script puede descargar el JAR en `.antlr/` o recibir `--jar RUTA`; verifica su SHA-256. La falta de estas herramientas debe registrarse como bloqueo de esa comprobación concreta, no como prueba aprobada.

La integración real se ejecuta por separado, una vez aprobada la prueba con fixture:

```powershell
python -m pytest -q -m integration --run-live
python src/driver.py examples/books_demo.wf --execute
```

Para ver también los conteos impresos por la integración, se añade `-s` al comando de pytest. El archivo de la prueba se crea en un directorio temporal; el comando del driver escribe `outputs/libros.csv`.

## Criterios de aceptación

1. Las nueve pruebas originales pasan sin eliminar ni modificar sus consultas o expectativas.
2. EACH y tipos opcionales se aceptan; las formas sintácticamente incorrectas se rechazan en sintaxis.
3. Cada fixture S01-S08 produce exactamente su diagnóstico, con código, fase y posición.
4. La IR es estructurada, independiente de ANTLR y conserva la precedencia.
5. La ejecución sobre el fixture obtiene tres registros y la consulta de libros con precio <25 conserva y exporta dos; son cantidades del catálogo ficticio, no de la web.
6. Se comprueban text, attr, regex, NUMBER, AUTO, ausencias y cortocircuito.
7. JSON y CSV se vuelven a leer y sus datos coinciden con los registros esperados.
8. Un fallo de compilación no llama al cliente HTTP ni crea salidas; los fallos de runtime tienen una fase distinta.
9. La política de destinos de red y rutas de archivo supera los casos simulados; se documentan sus límites.
10. `--check` confirma correspondencia exacta entre gramáticas y módulos generados.
11. Se registran comandos, cantidades, fallos y bloqueos reales en el estado de entrega.

## Riesgos y límites de la evidencia

El fixture controla los resultados y permite detectar regresiones; no representa todas las estructuras HTML existentes. Los mocks permiten comprobar decisiones sobre DNS, sockets y fallos difíciles de reproducir, pero no equivalen a probar todas las redes o sistemas operativos. Los enlaces/junctions se prueban con los mecanismos disponibles en el sistema utilizado.

Los límites de red evitan acceso libre a destinos arbitrarios; el cliente no ejecuta JavaScript. Las regex aceptadas por Python pueden ser costosas con patrones adversariales y no disponen de un timeout individual; se espera código DSL local de confianza y HTML limitado en tamaño. La resolución DNS de sistema no tiene un plazo duro controlado por el runtime. Las rutas de salida se validan y se resuelven, pero no se asume un sistema de archivos modificado hostilmente por otro proceso durante la escritura.

Los resultados finales y cualquier desviación de este plan se documentan en [ESTADO_HITO2.md](ESTADO_HITO2.md).


## Extensiones de validación

Verificar literales negativos y su distinción de comentarios, ejecución con umbrales negativos, ubicación de errores en EXTRACT y WHERE, exportación de IR con nodos/precedencia/posiciones y ausencia de HTTP. Rechazar destinos IR fuera de outputs y extensiones distintas de JSON; un error de compilación no debe generar IR.
