"""Integración externa optativa: nunca depende de cantidades fijas del servidor."""

import csv
from pathlib import Path

import pytest

from src.compiler import compile_file
from src.runtime.execution_engine import execute_plan


@pytest.mark.integration
def test_books_to_scrape_real(tmp_path):
    root = Path(__file__).resolve().parents[1]
    compiled = compile_file(root / "examples/books_demo.wf")
    assert compiled.success
    result = execute_plan(compiled.plan, tmp_path)
    assert result.found_count > 0
    assert result.filtered_count <= result.found_count
    assert result.exported_count == len(result.records)
    assert all(row["precio"] < 25 and isinstance(row["precio"], float) for row in result.records)
    with result.output_path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == result.exported_count
    print(f"Books real: {result.found_count} encontrados, {result.filtered_count} conservados, "
          f"{result.exported_count} exportados")
