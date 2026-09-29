# WebFetch (FetchUccini) 🌐🔍

> **Lenguaje de Dominio Específico (DSL) declarativo para la extracción automatizada y estructurada de datos web (Web Scraping).**

---

## 📌 Información del Proyecto

* **Institución:** Universidad Peruana de Ciencias Aplicadas (UPC)
* **Carrera:** Ciencias de la Computación
* **Curso:** Teoría de Compiladores (1ACC0218)
* **Sección:** 13962
* **Profesor:** Marco Antonio Sobrevilla Cabezudo
* **Ciclo:** 2026-2
* **Startup:** WebFetch
* **Producto:** FetchUccini
* **Entregable:** Hito 1 - Trabajo Parcial

---

## 👥 Integrantes del Equipo

| Apellidos y Nombres | Rol / Contribución |
| :--- | :--- |
| **Diaz Orihuela, Jose Andres** | Análisis Semántico & Driver |
| **Garcia Hernandez, Alejandro Jhoshua** | Construcciones del Lenguaje & Gramática |
| **Landauro La Rosa, Ian Joshua** | Construcciones del Lenguaje & Pruebas |
| **Meza Dagnino, Francesco Andre** | Analizador Léxico & Analizador Sintáctico |

---

## 📖 Descripción y Motivación

Tradicionalmente, la extracción de datos web (*web scraping*) se realiza de manera imperativa mediante lenguajes como Python o JavaScript, requiriendo la escritura manual de peticiones HTTP, parseo del árbol DOM, manejo de bucles y serialización a JSON o CSV. Este enfoque es propenso a errores y genera código repetitivo.

**WebFetch** es un DSL de naturaleza declarativa inspirado en la simplicidad de SQL. Permite definir de forma concisa **qué** datos extraer, **de dónde** y **cómo filtrarlos o guardarlos**, reduciendo complejas rutinas a consultas claras y directas compuestas por 4 cláusulas fundamentales:

1. **`FETCH`**: Especifica la URL origen de la extracción.
2. **`EXTRACT`**: Define el conjunto de campos mediante alias, funciones de extracción (`text`, `attr("href")`, `regex("...")`) y selectores CSS/XPath.
3. **`WHERE`**: Permite filtrar los resultados extraídos mediante condiciones relacionales (`==`, `!=`, `<`, `<=`, `>`, `>=`) y operadores lógicos (`AND`, `OR`).
4. **`EXPORT`**: Determina el formato de salida (`JSON` o `CSV`) y la ruta del archivo destino (terminando con punto y coma `;`).

### Ejemplo de Consulta WebFetch:
```sql
FETCH "https://books.toscrape.com/"
EXTRACT {
    titulo: text FROM "h1",
    enlace: attr("href") FROM "a.product",
    precio: regex("[0-9.]+") FROM ".price"
}
WHERE precio >= 10.00 AND precio <= 50.00
EXPORT AS JSON TO "resultados_libros.json";
```

---

## 📂 Estructura del Repositorio

```text
WebFetch/
│
├── docs/                               # Documentación y artefactos de entrega
│   ├── Teoría_de_Compiladores_TP_WebFetch.pdf  # Informe académico (máx. 5 páginas + carátula)
│   └── Presentacion_Hito1.pdf          # Diapositivas de la sustentación
│
├── grammar/                            # Especificaciones formales en ANTLR4
│   ├── WebFetchLexer.g4                # Analizador léxico (expresiones regulares y tokens)
│   └── WebFetchParser.g4               # Analizador sintáctico (gramáticas libres de contexto)
│
├── src/                                # Código fuente del compilador
│   ├── semantic/
│   │   ├── __init__.py
│   │   └── semantic_checker.py         # Analizador semántico (detección de errores lógicos)
│   └── driver.py                       # Driver principal ejecutable (análisis léxico, sintáctico y semántico)
│
├── tests/                              # Casos de prueba para validación
│   ├── valid/                          # Consultas válidas según la especificación
│   │   ├── 01_consulta_basica.wf
│   │   ├── 02_extraccion_multiple.wf
│   │   └── 03_filtro_complejo.wf
│   └── invalid/                        # Consultas con errores intencionales
│       ├── 04_error_sintactico.wf      # Violación sintáctica (falta de delimitadores/tokens)
│       ├── 05_error_campo_duplicado.wf # Error semántico 1: alias duplicado en EXTRACT
│       └── 06_error_campo_no_declarado.wf # Error semántico 2: campo no declarado en WHERE
│
├── .gitignore                          # Exclusión de archivos generados y temporales
├── requirements.txt                    # Dependencias del proyecto
└── README.md                           # Documentación principal del repositorio
```

---

## ⚙️ Requisitos e Instalación

### Prerrequisitos:
* **Python** 3.10 o superior.
* **Java Development Kit (JDK)** 17 o superior (para generar los parsers con la herramienta ANTLR4).

### Instalación de dependencias:
```bash
pip install -r requirements.txt
```

---

## 🚀 Guía de Ejecución

### 1. Compilación de Gramáticas ANTLR4:
Para generar las clases del lexer y parser en Python a partir de los archivos `.g4`:
```bash
antlr4 -Dlanguage=Python3 -visitor -no-listener grammar/WebFetchLexer.g4 grammar/WebFetchParser.g4 -o src/generated
```

### 2. Ejecución de Consultas con el Driver:
Para analizar una consulta fuente (`.wf`):
```bash
# Probar caso válido
python src/driver.py tests/valid/01_consulta_basica.wf

# Probar caso con error semántico
python src/driver.py tests/invalid/05_error_campo_duplicado.wf
```
