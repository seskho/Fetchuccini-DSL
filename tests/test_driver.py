import runpy
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

from src.driver import main, run_compiler
from src.runtime.errors import FetchucciniRuntimeError

ROOT = Path(__file__).resolve().parents[1]
LEGACY_CASES = runpy.run_path(str(ROOT / "tests" / "run_tests.py"))["TEST_CASES"]


@pytest.mark.parametrize("case", LEGACY_CASES, ids=lambda case: case["description"])
def test_hito1_unchanged_regressions(case):
    assert run_compiler(str(ROOT / case["file"])) == (case["expected_success"], case["expected_phase"])


def test_validate_has_no_http_or_files(tmp_path):
    client = Mock()
    result = run_compiler(str(ROOT / "examples/books_demo.wf"), output_dir=tmp_path, http_client=client)
    assert result == (True, "none")
    client.fetch.assert_not_called()
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("fixture", ["07_error_lexico.wf", "04_error_sintactico.wf", "S05_regex_invalida.wf"])
def test_compile_failure_prevents_http(fixture, tmp_path):
    client = Mock()
    result = run_compiler(str(ROOT / "tests/invalid" / fixture), execute=True,
                          output_dir=tmp_path, http_client=client)
    assert result[0] is False
    assert result[1] in {"lexical", "syntax", "semantic"}
    client.fetch.assert_not_called()
    assert not list(tmp_path.iterdir())


def test_runtime_failure_has_separate_phase(tmp_path):
    client = Mock()
    client.fetch.side_effect = FetchucciniRuntimeError("HTTP simulado falló")
    assert run_compiler(str(ROOT / "examples/books_demo.wf"), execute=True,
                        output_dir=tmp_path, http_client=client) == (False, "runtime")


def test_local_html_execution_and_counts(tmp_path, capsys):
    assert run_compiler(str(ROOT / "examples/catalogo_local.wf"), execute=True,
                        html_file=ROOT / "tests/fixtures/catalogo.html", output_dir=tmp_path) == (True, "none")
    assert (tmp_path / "catalogo/productos.json").exists()
    output = capsys.readouterr().out
    assert "encontrados: 3" in output and "WHERE: 2" in output and "exportados: 2" in output


def test_verbose_and_tokens_remain_available(capsys):
    assert run_compiler(str(ROOT / "examples/books_demo.wf"), verbose=True) == (True, "none")
    output = capsys.readouterr().out
    assert "KW_EACH" in output and "KW_NUMBER" in output and "Plan:" in output


def test_missing_query_and_missing_html_report_different_phases(tmp_path):
    assert run_compiler(str(tmp_path / "missing.wf")) == (False, "io")
    assert run_compiler(str(ROOT / "examples/books_demo.wf"), execute=True,
                        html_file=tmp_path / "missing.html", output_dir=tmp_path) == (False, "runtime")


@pytest.mark.parametrize("flags", [["--execute", "--validate-only"], ["--html", "x.html"]])
def test_cli_rejects_conflicting_modes(flags):
    with pytest.raises(SystemExit) as caught:
        main([str(ROOT / "examples/books_demo.wf"), *flags])
    assert caught.value.code == 2


def test_cli_works_outside_project_cwd(tmp_path):
    result = subprocess.run(
        [sys.executable, str(ROOT / "src/driver.py"), str(ROOT / "examples/books_demo.wf"),
         "--validate-only", "--tokens"], cwd=tmp_path, capture_output=True, encoding="utf-8",
    )
    assert result.returncode == 0, result.stderr
    assert "KW_EACH" in result.stdout and "Modo validación" in result.stdout
    assert not list(tmp_path.iterdir())
