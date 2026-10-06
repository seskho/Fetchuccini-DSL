"""
Driver principal del compilador Fetchuccini (Hito 1 - Trabajo Parcial).

Ejecuta en orden secuencial:
  1. Análisis Léxico (FetchucciniLexer)
  2. Análisis Sintáctico (FetchucciniParser)
  3. Análisis Semántico Preliminar (FetchucciniSemanticChecker)

Detiene la ejecución inmediatamente si alguna etapa reporta errores.
"""

import sys
import os
from typing import Tuple

# Asegurar codificación utf-8 en terminales
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from antlr4 import FileStream, CommonTokenStream, Token
from antlr4.error.ErrorListener import ErrorListener

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.generated.FetchucciniLexer import FetchucciniLexer
from src.generated.FetchucciniParser import FetchucciniParser
from src.semantic.semantic_checker import FetchucciniSemanticChecker


class LexerErrorCollector(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Linea {line}:{column} -> {msg}")


class ParserErrorCollector(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        sym = offendingSymbol.text if offendingSymbol else "?"
        self.errors.append(f"Linea {line}:{column} cerca de '{sym}' -> {msg}")


def run_compiler(file_path: str, verbose: bool = False) -> Tuple[bool, str]:
    """
    Ejecuta el pipeline completo de compilación.
    Retorna una tupla (éxito, fase_fallida).
    Fases posibles en caso de fallo: 'io', 'lexical', 'syntax', 'semantic'.
    En caso de éxito: (True, 'none').
    """
    if not os.path.exists(file_path):
        print(f"[-] Error: no se encontro el archivo '{file_path}'")
        return False, "io"

    print("=" * 65)
    print(f"[*] Compilador Fetchuccini (Hito 1 - UPC)")
    print(f"[*] Procesando archivo: {file_path}")
    print("=" * 65)

    input_stream = FileStream(file_path, encoding='utf-8')

    # -------------------------------------------------------------
    # 1. ANÁLISIS LÉXICO
    # -------------------------------------------------------------
    print("\n[1/3] Ejecutando Analizador Lexico...")
    lexer = FetchucciniLexer(input_stream)
    lexer_errors = LexerErrorCollector()
    lexer.removeErrorListeners()
    lexer.addErrorListener(lexer_errors)

    token_stream = CommonTokenStream(lexer)
    token_stream.fill()

    if lexer_errors.errors:
        print("[-] Fallo el Analisis Lexico:")
        for err in lexer_errors.errors:
            print(f"   {err}")
        return False, "lexical"

    token_count = len(token_stream.tokens) - 1  # descartar EOF
    print(f"   [OK] Analisis Lexico completado exitosamente ({token_count} tokens identificados).")

    if verbose:
        print("\n   --- Lista de Tokens generados ---")
        for token in token_stream.tokens:
            if token.type != Token.EOF:
                token_name = lexer.symbolicNames[token.type] or str(token.type)
                print(f"   * {token_name:<15} : '{token.text}'")

    # -------------------------------------------------------------
    # 2. ANÁLISIS SINTÁCTICO
    # -------------------------------------------------------------
    print("\n[2/3] Ejecutando Analizador Sintactico...")
    parser = FetchucciniParser(token_stream)
    parser_errors = ParserErrorCollector()
    parser.removeErrorListeners()
    parser.addErrorListener(parser_errors)

    tree = parser.program()

    if parser_errors.errors:
        print("[-] Fallo el Analisis Sintactico:")
        for err in parser_errors.errors:
            print(f"   {err}")
        return False, "syntax"

    print("   [OK] Analisis Sintactico completado exitosamente (Arbol sintactico construido sin ambiguedades).")

    # -------------------------------------------------------------
    # 3. ANÁLISIS SEMÁNTICO PRELIMINAR
    # -------------------------------------------------------------
    print("\n[3/3] Ejecutando Analizador Semantico Preliminar...")
    checker = FetchucciniSemanticChecker()
    checker.check(tree)

    if checker.errors:
        print(f"[-] Fallo el Analisis Semantico ({len(checker.errors)} error(es) detectado(s)):")
        for err in checker.errors:
            print(f"   {err}")
        return False, "semantic"

    print(f"   [OK] Analisis Semantico completado exitosamente (0 errores logicos).")
    print(f"   Campos registrados en la tabla de simbolos: {checker.symbol_table.names()}")

    print("\n" + "=" * 65)
    print("[SUCCESS] COMPILACION EXITOSA: La consulta es valida lexica, sintactica y semanticamente.")
    print("=" * 65 + "\n")
    return True, "none"


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python src/driver.py <ruta_archivo.wf> [--verbose]")
        sys.exit(1)

    file_to_run = sys.argv[1]
    is_verbose = "--verbose" in sys.argv
    success, _ = run_compiler(file_to_run, is_verbose)
    sys.exit(0 if success else 1)
