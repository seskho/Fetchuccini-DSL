import sys
import os

from antlr4 import FileStream, CommonTokenStream, Token
from antlr4.error.ErrorListener import ErrorListener

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.generated.FetchucciniLexer import FetchucciniLexer
from src.generated.FetchucciniParser import FetchucciniParser
from src.semantic.semantic_checker import FetchucciniSemanticChecker

class SyntaxErrorCollector(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        sym = offendingSymbol.text if offendingSymbol else "?"
        self.errors.append(f"Linea {line}:{column} cerca de '{sym}': {msg}")

def run_compiler(file_path: str, verbose: bool = False) -> bool:
    if not os.path.exists(file_path):
        print(f"Error: no se encontro el archivo '{file_path}'")
        return False

    print(f"Procesando {file_path}...")
    input_stream = FileStream(file_path, encoding='utf-8')

    # Analisis lexico
    lexer = FetchucciniLexer(input_stream)
    lexer_errors = SyntaxErrorCollector()
    lexer.removeErrorListeners()
    lexer.addErrorListener(lexer_errors)

    token_stream = CommonTokenStream(lexer)
    token_stream.fill()

    if lexer_errors.errors:
        print("Errores lexicos:")
        for err in lexer_errors.errors:
            print(f"  {err}")
        return False

    if verbose:
        print("\nTokens:")
        for token in token_stream.tokens:
            if token.type != Token.EOF:
                name = lexer.symbolicNames[token.type] or str(token.type)
                print(f"  {name:<15} {token.text}")
        print()

    # Analisis sintactico
    parser = FetchucciniParser(token_stream)
    parser_errors = SyntaxErrorCollector()
    parser.removeErrorListeners()
    parser.addErrorListener(parser_errors)

    tree = parser.program()

    if parser_errors.errors:
        print("Errores sintacticos:")
        for err in parser_errors.errors:
            print(f"  {err}")
        return False

    # Analisis semantico
    checker = FetchucciniSemanticChecker()
    checker.visit(tree)

    if checker.errors:
        print("Errores semanticos:")
        for err in checker.errors:
            print(f"  {err}")
        return False

    print("Compilacion exitosa.")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python src/driver.py <archivo.wf> [--verbose]")
        sys.exit(1)

    file_to_run = sys.argv[1]
    is_verbose = "--verbose" in sys.argv
    success = run_compiler(file_to_run, is_verbose)
    sys.exit(0 if success else 1)

