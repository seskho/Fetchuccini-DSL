"""CLI de Fetchuccini: validación por defecto y ejecución explícita del plan."""

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.compiler import compile_file
from src.generated.FetchucciniLexer import FetchucciniLexer
from src.runtime.errors import FetchucciniRuntimeError
from src.runtime.execution_engine import execute_plan


def run_compiler(file_path: str, verbose: bool = False, *, execute: bool = False,
                 tokens: bool = False, html_file=None, output_dir=None,
                 http_client=None) -> tuple[bool, str]:
    """Conserva (éxito, fase); los argumentos nuevos son opcionales y nombrados."""
    result = compile_file(file_path)
    if tokens or verbose:
        print("Tokens (línea:columna, tipo, texto):")
        for token in result.tokens:
            name = FetchucciniLexer.symbolicNames[token.type]
            print(f"  {token.line}:{token.column} {name:<15} {token.text!r}")
    if not result.success:
        for diagnostic in result.diagnostics:
            print(diagnostic)
        return False, result.phase

    print("[OK] Consulta válida: análisis léxico, sintáctico, semántico y plan intermedio.")
    if verbose:
        print(f"Campos: {result.symbol_table.names()}")
        print(f"Plan: {result.plan!r}")
    if not execute:
        print("Modo validación: no se ejecutó la consulta.")
        return True, "none"

    try:
        html = Path(html_file).read_text(encoding="utf-8") if html_file else None
        execution = execute_plan(result.plan, output_dir=output_dir,
                                 http_client=http_client, html=html)
    except FetchucciniRuntimeError as error:
        print(error)
        return False, "runtime"
    except (OSError, UnicodeError) as error:
        print(f"[R_IO] Error runtime al leer HTML local: {error}")
        return False, "runtime"
    print(f"[OK] Registros encontrados: {execution.found_count}; "
          f"conservados tras WHERE: {execution.filtered_count}; "
          f"descartados: {execution.discarded_count}; "
          f"exportados: {execution.exported_count}.")
    print(f"Archivo: {execution.output_path}")
    return True, "none"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Compilador y runtime de Fetchuccini, Hito 2")
    parser.add_argument("file", help="Consulta .wf en UTF-8")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--validate-only", action="store_true", help="Validar sin ejecutar (predeterminado)")
    mode.add_argument("--execute", action="store_true", help="Ejecutar y exportar en outputs/")
    parser.add_argument("--verbose", action="store_true", help="Mostrar tokens, símbolos y plan")
    parser.add_argument("--tokens", action="store_true", help="Mostrar tokens reconocidos")
    parser.add_argument("--html", metavar="ARCHIVO", help="Ejecutar con HTML local, sin HTTP")
    args = parser.parse_args(argv)
    if args.html and not args.execute:
        parser.error("--html requiere --execute")
    success, _ = run_compiler(args.file, args.verbose, execute=args.execute,
                             tokens=args.tokens, html_file=args.html)
    return 0 if success else 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
