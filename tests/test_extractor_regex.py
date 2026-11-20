"""Las expresiones regulares reciben texto original, incluidos sus espacios."""

from src.ir.models import ExecutionPlan, FieldPlan
from src.runtime.extractor import extract_records


def test_regex_preserves_whitespace_and_returns_first_entire_match():
    html = '<p>Primera  línea\n  código 123\nSegunda  línea\n  código 456</p>'
    plan = ExecutionPlan(
        "https://books.toscrape.com/", None,
        (
            FieldPlan("texto", "text", "p"),
            FieldPlan("coincidencia", "regex", "p", r"línea\n\s{2}código ([0-9]+)"),
        ),
        None, "JSON", "datos.json",
    )
    assert extract_records(plan, html) == [{
        "texto": "Primera línea código 123 Segunda línea código 456",
        "coincidencia": "línea\n  código 123",
    }]
