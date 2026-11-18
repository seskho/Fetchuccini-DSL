"""Casos de aceptación del backend con HTML controlado y HTTP simulado."""

import csv
import json
from dataclasses import replace
from unittest.mock import Mock

import pytest

from src.compiler import compile_file
from src.ir.models import Comparison, Identifier, NumberLiteral, StringLiteral
from src.runtime.errors import FetchucciniRuntimeError
from src.runtime.execution_engine import execute_plan
from src.runtime.extractor import extract_records
from src.runtime.filter_engine import evaluate_filter


FIELDS = ('titulo: text FROM "h3 a" AS STRING, '
          'enlace: attr("href") FROM "h3 a", '
          'precio: regex("[0-9.]+") FROM ".price_color" AS NUMBER, '
          'disponibilidad: text FROM ".availability"')


def test_simulated_http_extract_filter_and_json(make_plan, catalog_html, tmp_path):
    plan = make_plan(FIELDS, 'WHERE precio >= 10 AND precio < 25', path="catalogo/datos.json")
    client = Mock()
    client.fetch.return_value = catalog_html
    result = execute_plan(plan, tmp_path, http_client=client)
    client.fetch.assert_called_once_with("https://books.toscrape.com/")
    assert (result.found_count, result.filtered_count, result.exported_count) == (3, 2, 2)
    assert result.discarded_count == 1
    assert result.records == [
        {"titulo": 'Álgebra, "edición" nueva', "enlace": "uno.html", "precio": 12.5,
         "disponibilidad": "En stock"},
        {"titulo": "Cuentos", "enlace": None, "precio": 20.0, "disponibilidad": "En stock"},
    ]
    assert json.loads(result.output_path.read_text(encoding="utf-8")) == result.records
    assert "Álgebra" in result.output_path.read_text(encoding="utf-8")


def test_csv_order_quoting_unicode_and_empty_cell(make_plan, catalog_html, tmp_path):
    plan = make_plan(FIELDS, export_format="CSV")
    result = execute_plan(plan, tmp_path, html=catalog_html)
    with result.output_path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.reader(stream))
    assert rows[0] == ["titulo", "enlace", "precio", "disponibilidad"]
    assert rows[1] == ['Álgebra, "edición" nueva', "uno.html", "12.5", "En stock"]
    assert rows[3][1] == ""
    assert len(rows) == 4


def test_first_match_without_each(make_plan, catalog_html):
    plan = make_plan(FIELDS, each="")
    records = extract_records(plan, catalog_html)
    assert len(records) == 1
    assert records[0]["precio"] == 12.5


def test_missing_selector_attribute_and_regex(make_plan, catalog_html):
    plan = make_plan('ausente: text FROM ".missing", atributo: attr("src") FROM "h3 a", '
                     'regex_vacia: regex("XYZ") FROM "h3 a", '
                     'opcional: text FROM ".missing" AS NUMBER')
    assert extract_records(plan, catalog_html) == [
        {"ausente": None, "atributo": None, "regex_vacia": None, "opcional": None}
    ] * 3


def test_regex_returns_entire_first_match_and_attr_list(make_plan, catalog_html):
    plan = make_plan('numero: regex("([0-9]+)[.][0-9]+") FROM ".price_color", '
                     'clases: attr("class") FROM ".price_color"')
    records = extract_records(plan, catalog_html)
    assert records[0] == {"numero": "12.50", "clases": "price_color"}


@pytest.mark.parametrize("export_format,expected", [("JSON", "[]"), ("CSV", "titulo")])
def test_empty_each_exports_valid_document(make_plan, catalog_html, tmp_path, export_format, expected):
    plan = make_plan(each='EACH ".missing"', export_format=export_format)
    result = execute_plan(plan, tmp_path, html=catalog_html)
    assert (result.found_count, result.filtered_count, result.exported_count) == (0, 0, 0)
    assert result.output_path.read_text(encoding="utf-8").strip() == expected


@pytest.mark.parametrize("where,titles", [
    ('WHERE categoria == "Libros" AND precio < 15', ['Álgebra, "edición" nueva']),
    ('WHERE categoria == "Viajes" OR precio == 20', ["Guía del Perú", "Cuentos"]),
    ('WHERE categoria == "Libros" OR precio > 25 AND stock == "Agotado"',
     ['Álgebra, "edición" nueva', "Guía del Perú", "Cuentos"]),
])
def test_filters_and_actual_precedence(make_plan, catalog_html, tmp_path, where, titles):
    fields = FIELDS + ', categoria: text FROM ".cat", stock: text FROM ".availability"'
    result = execute_plan(make_plan(fields, where), tmp_path, html=catalog_html)
    assert [record["titulo"] for record in result.records] == titles


@pytest.mark.parametrize("where,count", [
    ('WHERE titulo == "inexistente" AND precio > 10', 0),
    ('WHERE titulo != "inexistente" OR precio > 10', 3),
])
def test_boolean_short_circuit_skips_bad_auto_conversion(make_plan, catalog_html, tmp_path, where, count):
    plan = make_plan('titulo: text FROM "h3 a", precio: text FROM "h3 a"', where)
    assert execute_plan(plan, tmp_path, html=catalog_html).filtered_count == count


@pytest.mark.parametrize("operator,expected", [
    ("==", False), ("!=", True), ("<", True), ("<=", True), (">", False), (">=", False),
])
def test_all_numeric_operators_with_auto(operator, expected):
    expression = Comparison(Identifier("precio"), operator, NumberLiteral(20.0))
    assert evaluate_filter(expression, {"precio": "12.50"}) is expected


@pytest.mark.parametrize("operator", ["==", "!=", "<", "<=", ">", ">="])
def test_none_is_false_on_either_side(operator):
    expression = Comparison(Identifier("x"), operator, Identifier("y"))
    assert evaluate_filter(expression, {"x": None, "y": 10}) is False
    assert evaluate_filter(expression, {"x": 10, "y": None}) is False


def test_auto_strings_compare_textually_and_preserve_original(make_plan, catalog_html):
    plan = make_plan('precio: regex("[0-9.]+") FROM ".price_color"')
    records = extract_records(plan, catalog_html)
    assert records[0]["precio"] == "12.50"
    expression = Comparison(Identifier("precio"), "==", StringLiteral("12.50"))
    assert evaluate_filter(expression, records[0], plan.fields)
    assert evaluate_filter(Comparison(Identifier("precio"), "==", NumberLiteral(12.5)), records[0])
    assert records[0]["precio"] == "12.50"


def test_numeric_convertible_string_literal(make_plan, catalog_html, tmp_path):
    plan = make_plan('precio: regex("[0-9.]+") FROM ".price_color" AS NUMBER',
                     'WHERE precio < "25.00"')
    assert execute_plan(plan, tmp_path, html=catalog_html).filtered_count == 2


@pytest.mark.parametrize("value", ["no es número", "NaN", "Infinity", "1e9999"])
def test_number_conversion_failure_reports_field_and_record(make_plan, tmp_path, value):
    plan = make_plan('precio: text FROM ".price" AS NUMBER', each='EACH "article"')
    html = f'<article><p class="price">10</p></article><article><p class="price">{value}</p></article>'
    with pytest.raises(FetchucciniRuntimeError) as caught:
        execute_plan(plan, tmp_path, html=html)
    assert caught.value.phase == "runtime"
    assert caught.value.field == "precio"
    assert caught.value.record_index == 2
    assert not (tmp_path / "datos.json").exists()


def test_bad_auto_comparison_preserves_previous_export(make_plan, catalog_html, tmp_path):
    destination = tmp_path / "datos.json"
    destination.write_text("resultado anterior", encoding="utf-8")
    plan = make_plan('precio: text FROM "h3 a"', "WHERE precio > 10")
    with pytest.raises(FetchucciniRuntimeError, match="registro 1"):
        execute_plan(plan, tmp_path, html=catalog_html)
    assert destination.read_text(encoding="utf-8") == "resultado anterior"


def test_simulated_http_failure_does_not_export(make_plan, tmp_path):
    client = Mock()
    client.fetch.side_effect = FetchucciniRuntimeError("HTTP 503", "R01")
    with pytest.raises(FetchucciniRuntimeError, match="HTTP 503"):
        execute_plan(make_plan(), tmp_path, http_client=client)
    assert not list(tmp_path.iterdir())


def test_export_disk_permission_failure_is_runtime(make_plan, catalog_html, tmp_path, monkeypatch):
    def denied(*args, **kwargs):
        raise PermissionError("disco de prueba sin permisos")
    monkeypatch.setattr("src.runtime.exporter.tempfile.NamedTemporaryFile", denied)
    with pytest.raises(FetchucciniRuntimeError, match="sin permisos") as caught:
        execute_plan(make_plan(), tmp_path, html=catalog_html)
    assert caught.value.code == "R04"


def test_runtime_rechecks_untrusted_plan_before_http(make_plan, tmp_path):
    plan = replace(make_plan(), export_path="../escape.json")
    client = Mock()
    with pytest.raises(FetchucciniRuntimeError):
        execute_plan(plan, tmp_path, http_client=client)
    client.fetch.assert_not_called()


def test_exact_books_example_on_fixture(catalog_html, tmp_path):
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    compiled = compile_file(root / "examples" / "books_demo.wf")
    assert compiled.success
    result = execute_plan(compiled.plan, tmp_path, html=catalog_html)
    assert (result.found_count, result.filtered_count, result.exported_count) == (3, 2, 2)
    assert [row["precio"] for row in result.records] == [12.5, 20.0]
