# Fetchuccini-DSL

> **Lenguaje de Dominio Específico (DSL) declarativo orientado a la extracción estructurada de información web (Web Scraping).**

---

## 📌 Información del Proyecto

- **Institución:** Universidad Peruana de Ciencias Aplicadas (UPC)
- **Carrera:** Ciencias de la Computación
- **Curso:** Teoría de Compiladores (1ACC0218)
- **Sección:** 13962
- **Profesor:** Marco Antonio Sobrevilla Cabezudo
- **Ciclo:** 2026-2
- **Startup:** WebFetch
- **Producto / Lenguaje:** Fetchuccini
- **Entregable:** Hito 1 - Trabajo Parcial

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

Tradicionalmente, la extracción automatizada de datos web suele implementarse mediante lenguajes imperativos de propósito general como Python o JavaScript. Esto obliga a programar manualmente peticiones HTTP, procesamiento del DOM, bucles de iteración y serialización a formatos como JSON o CSV, generando código repetitivo y propenso a fallas.

**Fetchuccini** es un lenguaje de dominio específico (DSL) de carácter declarativo inspirado en la simplicidad de SQL. Permite definir concisamente **qué** datos extraer, **de dónde** y **cómo filtrarlos o exportarlos**, reduciendo complejas rutinas a consultas directas estructuradas en cuatro construcciones principales:

1. **`FETCH`**: Define la fuente web de la consulta mediante una URL (`STRING`).
2. **`EXTRACT`**: Define los campos a extraer utilizando un alias (`ID`), un mecanismo de extracción y un selector CSS/XPath (`STRING`):
   - `text`: Extrae el contenido textual de un elemento.
   - `attr("nombre")`: Extrae el valor de un atributo HTML (ej. `href`, `src`).
   - `regex("patron")`: Extrae coincidencias mediante una expresión regular.
3. **`WHERE`** *(opcional)*: Filtra los resultados mediante comparaciones relacionales (`==`, `!=`, `<`, `<=`, `>`, `>=`) y operadores lógicos (`AND`, `OR`).
   - **Precedencia lógica:** El operador `AND` posee mayor precedencia que `OR`.
4. **`EXPORT`**: Define el formato de serialización (`JSON` o `CSV`) y la ruta del archivo de destino, finalizando obligatoriamente con punto y coma (`;`).

### Ejemplo de Consulta Válida:
```sql
FETCH "https://prueba.com/tienda"
EXTRACT {
    titulo: text FROM "h1",
    enlace: attr("href") FROM "a.producto",
    precio: regex("[0-9.]+") FROM ".precio"
}
WHERE precio >= 10 AND precio <= 50
EXPORT AS JSON TO "resultados.json";
```

---

## 🎯 Alcance del Hito 1 y Limitaciones

El Hito 1 corresponde a la implementación completa del **Front-End** del compilador:
- ✅ **Analizador Léxico (Lexer):** Reconocimiento de 30 tokens terminales, descarte de espacios en blanco (`WS`) y comentarios (`COMMENT`).
- ✅ **Analizador Sintáctico (Parser):** Validación de la estructura no ambigua de consultas respetando la jerarquía `FETCH → EXTRACT → WHERE? → EXPORT` y la precedencia `AND > OR`.
- ✅ **Analizador Semántico Preliminar:** Detección y reporte con línea y columna de:
  1. *Campos duplicados* dentro del bloque `EXTRACT`.
  2. *Campos no declarados* evaluados en la cláusula `WHERE`.
- ✅ **Driver y Suite de Pruebas:** Ejecución secuencial y verificación automatizada.

**Limitaciones actuales (Fuera del alcance de Hito 1):**
- No se ejecutan peticiones HTTP reales a la red ni scraping en vivo.
- No se realiza la generación física de archivos JSON/CSV en disco (esto corresponde al Back-End en etapas posteriores).
- No se admiten múltiples URLs en una sola consulta, agregaciones ni subconsultas.

---

## 📂 Estructura del Repositorio

```text
WebFetch/
│
├── docs/                               # Documentación y artefactos de entrega
│   └── .gitkeep                        # (Informe final en PDF)
│
├── grammar/                            # Especificaciones formales en ANTLR4
│   ├── FetchucciniLexer.g4             # Analizador léxico (expresiones regulares y tokens)
│   └── FetchucciniParser.g4            # Analizador sintáctico (gramáticas libres de contexto)
│
├── src/                                # Código fuente del compilador
│   ├── generated/                      # Clases generadas automáticamente por ANTLR4
│   │   ├── FetchucciniLexer.py
│   │   ├── FetchucciniParser.py
│   │   ├── FetchucciniParserVisitor.py
│   │   └── __init__.py
│   ├── semantic/                       # Analizador semántico preliminar
│   │   ├── __init__.py
│   │   └── semantic_checker.py         # Visitor que valida las 2 reglas semánticas
│   ├── driver.py                       # Driver principal ejecutable por CLI
│   └── __init__.py
│
├── tests/                              # Suite de pruebas del compilador
│   ├── run_tests.py                    # Ejecutor automatizado de toda la suite
│   ├── valid/                          # Casos de prueba que deben compilar con éxito
│   │   ├── 01_consulta_basica.wf
│   │   ├── 02_extraccion_multiple.wf
│   │   ├── 03_filtro_complejo.wf
│   │   ├── 04_filtro_or.wf
│   │   └── 05_precedencia_logica.wf
│   └── invalid/                        # Casos con errores intencionales para cada etapa
│       ├── 04_error_sintactico.wf      # Violación sintáctica (falta delimitador)
│       ├── 05_error_campo_duplicado.wf # Error semántico 1: alias duplicado en EXTRACT
│       ├── 06_error_campo_no_declarado.wf # Error semántico 2: campo no declarado en WHERE
│       └── 07_error_lexico.wf          # Error léxico: carácter no reconocido
│
├── .gitignore                          # Exclusión de entornos virtuales y temporales
├── requirements.txt                    # Dependencia fijada: antlr4-python3-runtime==4.13.2
└── README.md                           # Documentación principal
```

---

## ⚙️ Requisitos e Instalación

### Prerrequisitos:
- **Python** 3.10 o superior.
- **Java Development Kit (JDK)** 17 o superior (necesario únicamente si se desea regenerar las gramáticas con la herramienta ANTLR4).

### Instalación de dependencias:
```bash
pip install -r requirements.txt
```

---

## 🚀 Guía de Ejecución

### 1. Ejecutar una consulta con el Driver:
El script `src/driver.py` ejecuta de forma secuencial las fases léxica, sintáctica y semántica:

```bash
# Probar una consulta válida:
python src/driver.py tests/valid/01_consulta_basica.wf

# Probar con visualización de tokens reconocidos:
python src/driver.py tests/valid/01_consulta_basica.wf --verbose

# Probar la detección de errores (ej. semántico):
python src/driver.py tests/invalid/05_error_campo_duplicado.wf
```

### 2. Ejecutar la Suite Automatizada de Pruebas:
Para verificar que todos los casos válidos e inválidos se comporten exactamente según lo especificado:

```bash
python tests/run_tests.py
```

### 3. Regenerar Gramáticas ANTLR4 (Opcional):
Los archivos en `src/generated/` ya se encuentran provistos en el repositorio. Si se modifica alguna gramática en `grammar/`, se pueden regenerar con:

```bash
antlr4 -Dlanguage=Python3 -visitor -no-listener -o src/generated grammar/FetchucciniLexer.g4 grammar/FetchucciniParser.g4
```
