"""
Ejecutor automatizado de pruebas para el compilador Fetchuccini (Hito 1).

Verifica que:
1. Las consultas válidas pasen exitosamente todas las etapas (léxica, sintáctica y semántica).
2. Las consultas inválidas sean rechazadas exactamente en la fase esperada:
   - Errores léxicos en fase 'lexical'.
   - Errores sintácticos en fase 'syntax'.
   - Errores semánticos en fase 'semantic'.
"""

import os
import sys

# Asegurar importación de módulos internos desde la raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.driver import run_compiler

TEST_CASES = [
    # -------------------------------------------------------------
    # Casos Válidos
    # -------------------------------------------------------------
    {
        "file": os.path.join("tests", "valid", "01_consulta_basica.wf"),
        "expected_success": True,
        "expected_phase": "none",
        "description": "01 Consulta básica (FETCH, EXTRACT text, EXPORT JSON)"
    },
    {
        "file": os.path.join("tests", "valid", "02_extraccion_multiple.wf"),
        "expected_success": True,
        "expected_phase": "none",
        "description": "02 Extracción múltiple (text, attr, regex) con WHERE numérico y CSV"
    },
    {
        "file": os.path.join("tests", "valid", "03_filtro_complejo.wf"),
        "expected_success": True,
        "expected_phase": "none",
        "description": "03 Filtro conjuntivo con operador AND"
    },
    {
        "file": os.path.join("tests", "valid", "04_filtro_or.wf"),
        "expected_success": True,
        "expected_phase": "none",
        "description": "04 Filtro disyuntivo con operador OR"
    },
    {
        "file": os.path.join("tests", "valid", "05_precedencia_logica.wf"),
        "expected_success": True,
        "expected_phase": "none",
        "description": "05 Precedencia lógica combinando AND y OR (AND > OR)"
    },
    # -------------------------------------------------------------
    # Casos Inválidos
    # -------------------------------------------------------------
    {
        "file": os.path.join("tests", "invalid", "04_error_sintactico.wf"),
        "expected_success": False,
        "expected_phase": "syntax",
        "description": "04 Error sintáctico (falta llave '}' y terminador ';')"
    },
    {
        "file": os.path.join("tests", "invalid", "05_error_campo_duplicado.wf"),
        "expected_success": False,
        "expected_phase": "semantic",
        "description": "05 Error semántico: alias duplicado en EXTRACT"
    },
    {
        "file": os.path.join("tests", "invalid", "06_error_campo_no_declarado.wf"),
        "expected_success": False,
        "expected_phase": "semantic",
        "description": "06 Error semántico: campo en WHERE no declarado en EXTRACT"
    },
    {
        "file": os.path.join("tests", "invalid", "07_error_lexico.wf"),
        "expected_success": False,
        "expected_phase": "lexical",
        "description": "07 Error léxico: carácter no reconocido ('@')"
    },
]

def main():
    print("\n" + "=" * 70)
    print(" SUITE DE PRUEBAS AUTOMATIZADAS - COMPILADOR FETCHUCCINI (HITO 1)")
    print("=" * 70 + "\n")

    passed_count = 0
    total_count = len(TEST_CASES)

    for i, test in enumerate(TEST_CASES, 1):
        file_path = test["file"]
        desc = test["description"]
        expected_success = test["expected_success"]
        expected_phase = test["expected_phase"]

        print(f"[{i}/{total_count}] Probando: {desc}")
        print(f"      Archivo: {file_path}")

        # Ejecutar compilador sin imprimir todo el verbose
        # Redirigir stdout temporalmente para un reporte limpio
        success, failed_phase = run_compiler(file_path, verbose=False)

        is_passed = (success == expected_success) and (failed_phase == expected_phase)

        if is_passed:
            passed_count += 1
            print(f"      >>> RESULTADO: PASS (Fase detectada: '{failed_phase}')\n")
        else:
            print(f"      >>> RESULTADO: FAIL")
            print(f"          Esperado: exito={expected_success}, fase={expected_phase}")
            print(f"          Obtenido: exito={success}, fase={failed_phase}\n")

    print("=" * 70)
    print(f" RESUMEN DE PRUEBAS: {passed_count}/{total_count} PASARON.")
    print("=" * 70 + "\n")

    if passed_count == total_count:
        print("[SUCCESS] Todas las pruebas pasaron satisfactoriamente.\n")
        sys.exit(0)
    else:
        print(f"[ERROR] {total_count - passed_count} prueba(s) fallaron.\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
