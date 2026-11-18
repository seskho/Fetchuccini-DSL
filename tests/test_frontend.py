"""Regresión, gramática, diagnósticos y contratos del plan intermedio."""

from pathlib import Path

from antlr4 import CommonTokenStream, InputStream
import pytest

from src.compiler import compile_file, compile_source
from src.generated.FetchucciniLexer import FetchucciniLexer
from src.generated.FetchucciniParser import FetchucciniParser
from src.ir.models import AndExpression, Comparison, Identifier, NumberLiteral, OrExpression, StringLiteral
from src.literals import decode_string
from src.semantic.semantic_checker import FetchucciniSemanticChecker, SymbolTable


ROOT = Path(__file__).resolve().parents[1]


def query(fields='titulo: text FROM "h1"', where="", each="", url="https://example.com", path="datos.json"):
    return (f'FETCH "{url}"\n{each}\nEXTRACT {{ {fields} }}\n'
            f'{where}\nEXPORT AS JSON TO "{path}";')


@pytest.mark.parametrize("filename", [
    "01_consulta_basica.wf", "02_extraccion_multiple.wf", "03_filtro_complejo.wf",
    "04_filtro_or.wf", "05_precedencia_logica.wf",
])
def test_hito1_valid_regression(filename):
    result = compile_file(ROOT / "tests" / "valid" / filename)
    assert result.success and result.phase == "none" and result.plan is not None
    assert all(field.declared_type == "AUTO" for field in result.plan.fields)


@pytest.mark.parametrize("filename,phase", [
    ("04_error_sintactico.wf", "syntax"),
    ("05_error_campo_duplicado.wf", "semantic"),
    ("06_error_campo_no_declarado.wf", "semantic"),
    ("07_error_lexico.wf", "lexical"),
])
def test_hito1_invalid_regression(filename, phase):
    result = compile_file(ROOT / "tests" / "invalid" / filename)
    assert not result.success and result.phase == phase and result.plan is None


def test_lexer_keywords_comments_literals_and_operators():
    lexer = FetchucciniLexer(InputStream('EACH NUMBER STRING each 25.00 "José" -- comentario\n<= >= != == < >'))
    stream = CommonTokenStream(lexer)
    stream.fill()
    tokens = [(lexer.symbolicNames[token.type], token.text) for token in stream.tokens[:-1]]
    assert tokens[:6] == [
        ("KW_EACH", "EACH"), ("KW_NUMBER", "NUMBER"), ("KW_STRING", "STRING"),
        ("ID", "each"), ("NUMBER", "25.00"), ("STRING", '"José"'),
    ]
    assert [name for name, _ in tokens[6:]] == ["OP_LE", "OP_GE", "OP_NEQ", "OP_EQ", "OP_LT", "OP_GT"]


def test_string_escapes_keep_unicode_and_regex_backslash():
    assert decode_string(r'"José \\d+ \"libro\"\n\t\b\f\r\'"') == 'José \\d+ "libro"\n\t\b\f\r\''
    result = compile_source(query(fields=r'precio: regex("\\d+\\.\\d+") FROM ".price"'))
    assert result.success
    assert result.plan.fields[0].extractor_argument == r"\d+\.\d+"


@pytest.mark.parametrize("fields,each,types", [
    ('titulo: text FROM "h1"', "", ["AUTO"]),
    ('titulo: text FROM "h1" AS STRING', 'EACH "article"', ["STRING"]),
    ('precio: regex("[0-9.]+") FROM ".price" AS NUMBER', 'EACH "article"', ["NUMBER"]),
    ('titulo: text FROM "h1" AS STRING, precio: text FROM ".price" AS NUMBER, enlace: attr("href") FROM "a"', "", ["STRING", "NUMBER", "AUTO"]),
])
def test_optional_each_and_types(fields, each, types):
    result = compile_source(query(fields=fields, each=each))
    assert result.success
    assert [field.declared_type for field in result.plan.fields] == types
    assert result.plan.each_selector == ("article" if each else None)
    assert result.plan.filter_expression is None


@pytest.mark.parametrize("source", [
    'EACH "article" FETCH "https://example.com" EXTRACT { a: text FROM "h1" } EXPORT AS JSON TO "a.json";',
    query(each='EACH "article" EACH "section"'),
    query(fields=""),
    query(fields='a: text FROM "h1" AS AUTO'),
    query(fields='a: text FROM "h1" AS BOOLEAN'),
    query(fields='a: text FROM "h1" AS'),
    query(fields='a: text FROM "h1",'),
    query(where='WHERE ()'),
    query(where='WHERE (titulo == "a"'),
    query(where='WHERE titulo == "a")'),
    query(where='WHERE (titulo == "a" OR)'),
    query(where='WHERE (titulo) == "a"'),
    query()[:-1],
    query() + ' FETCH "https://example.com"',
])
def test_invalid_syntax_is_not_semantic_evidence(source):
    result = compile_source(source)
    assert not result.success and result.phase == "syntax"
    assert result.plan is None


@pytest.mark.parametrize("code,filename", [
    ("S01", "S01_alias_duplicado.wf"),
    ("S02", "S02_campo_no_declarado.wf"),
    ("S03", "S03_url_invalida.wf"),
    ("S04", "S04_selector_invalido.wf"),
    ("S05", "S05_regex_invalida.wf"),
    ("S06", "S06_atributo_vacio.wf"),
    ("S07", "S07_extension_incompatible.wf"),
    ("S08", "S08_tipos_incompatibles.wf"),
])
def test_semantic_fixture_reports_exact_code_and_location(code, filename):
    result = compile_file(ROOT / "tests" / "invalid" / filename)
    assert result.phase == "semantic" and not result.success and result.plan is None
    assert [error.code for error in result.diagnostics] == [code]
    error = result.diagnostics[0]
    assert error.phase == "semantic" and error.line >= 1 and error.column >= 0
    assert f"[{code}]" in str(error) and "semántico" in str(error)


@pytest.mark.parametrize("url", [
    "ftp://example.com", "file:///tmp/data.html", "https://", "https:///example.com",
    "https://bad_host.com", "https://-bad.com", "https://bad-.com", "https://example..com",
    "https://example.com:abc", "https://example.com:70000", "https://example.com:0",
    "https://999.300.1.1", "https://example.com a", "https://user:password@example.com", "https://example.com../",
])
def test_invalid_url_is_semantic_without_dns(url):
    result = compile_source(query(url=url))
    assert result.phase == "semantic"
    assert [error.code for error in result.diagnostics] == ["S03"]


@pytest.mark.parametrize("url", [
    "http://example.com", "https://example.com:443/path?q=2", "https://münich.example/",
    "https://example.com./", "http://localhost", "https://8.8.8.8/", "https://[2001:4860:4860::8888]/",
])
def test_valid_url_syntax_does_not_imply_runtime_permission(url):
    result = compile_source(query(url=url))
    assert result.success and result.plan.source_url == url


@pytest.mark.parametrize("fields,where,expected", [
    ('a: text FROM "h1" AS STRING', "WHERE a > 10", "S08"),
    ('a: text FROM "h1" AS STRING', "WHERE a < \"20\"", "S08"),
    ('a: text FROM "h1" AS STRING', "WHERE a == 10", "S08"),
    ('a: text FROM "h1" AS NUMBER', 'WHERE a != "10"', "S08"),
    ('a: text FROM "h1"', "WHERE a >= 10", None),
    ('a: text FROM "h1"', 'WHERE a == "diez"', None),
    ('a: text FROM "h1" AS NUMBER', 'WHERE a > "10"', None),
    ('a: text FROM "h1"', 'WHERE a > "diez"', "S08"),
    ('a: text FROM "h1"', 'WHERE "2" < "10"', None),
    ('a: text FROM "h1"', 'WHERE a < "NaN"', "S08"),
])
def test_known_types_and_auto_comparison_policy(fields, where, expected):
    result = compile_source(query(fields=fields, where=where))
    assert result.success == (expected is None)
    assert [error.code for error in result.diagnostics] == ([] if expected is None else [expected])


def test_number_literal_overflow_is_reported_before_ir():
    result = compile_source(query(where="WHERE titulo > " + "9" * 400))
    assert result.phase == "semantic" and result.plan is None
    assert [error.code for error in result.diagnostics] == ["S08"]


@pytest.mark.parametrize("pattern", ["a{999999999999999999999999999999999999999}", "(" * 1000])
def test_regex_compilation_limits_are_semantic_errors(pattern):
    result = compile_source(query(fields=f'a: regex("{pattern}") FROM "h1"'))
    assert result.phase == "semantic" and result.plan is None
    assert [error.code for error in result.diagnostics] == ["S05"]


@pytest.mark.parametrize("each,fields,code", [
    ('EACH "div["', 'a: text FROM "h1"', "S04"),
    ('EACH ""', 'a: text FROM "h1"', "S04"),
    ("", 'a: attr("   ") FROM "a"', "S06"),
    ("", 'a: text FROM "//h1"', "S04"),
])
def test_each_selector_and_attribute_validation(each, fields, code):
    result = compile_source(query(fields=fields, each=each))
    assert result.phase == "semantic" and [error.code for error in result.diagnostics] == [code]


def test_selector_compilation_recursion_limit_is_reported_before_runtime():
    selector = ":is(" * 1000 + "h1" + ")" * 1000
    result = compile_source(query(each=f'EACH "{selector}"'))
    assert result.phase == "semantic" and result.plan is None
    assert [error.code for error in result.diagnostics] == ["S04"]


def test_all_semantic_rules_accumulate_without_cascading_undeclared_type_error():
    source = query(
        url="ftp://example.com", each='EACH "div["',
        fields='titulo: regex("[") FROM "h1" AS STRING, titulo: attr(" ") FROM "h2"',
        where="WHERE ausente > 10 OR titulo > 10", path="datos.csv",
    )
    result = compile_source(source)
    assert result.phase == "semantic"
    assert {error.code for error in result.diagnostics} == {f"S{number:02}" for number in range(1, 9)}
    assert len(result.diagnostics) == 8


def test_symbol_table_keeps_first_declaration_and_checker_resets():
    table = SymbolTable()
    table.declare("precio", "regex", 2, 4, "NUMBER", ".price", "[0-9.]+")
    assert table.lookup("precio", 9, 0).declared_type == "NUMBER"
    assert table.names() == ["precio"] and table.contains("precio")
    checker = FetchucciniSemanticChecker()
    first = FetchucciniParser(CommonTokenStream(FetchucciniLexer(InputStream(query(where="WHERE ausente > 1"))))).program()
    second = FetchucciniParser(CommonTokenStream(FetchucciniLexer(InputStream(query(fields='otro: text FROM "h2" AS STRING'))))).program()
    assert [error.code for error in checker.check(first)] == ["S02"]
    assert checker.check(second) == []
    assert checker.symbol_table.names() == ["otro"]


def test_ir_preserves_query_fields_arguments_types_and_precedence():
    result = compile_source(query(
        fields='categoria: text FROM ".cat" AS STRING, precio: regex("[0-9.]+") FROM ".price" AS NUMBER, enlace: attr("href") FROM "a"',
        each='EACH "article"', where='WHERE categoria == "Libros" OR precio >= 10 AND precio <= 50',
        path="catalogo/datos.json",
    ))
    assert result.success
    plan = result.plan
    assert plan.source_url == "https://example.com" and plan.each_selector == "article"
    assert [(field.alias, field.extractor_type, field.selector, field.extractor_argument, field.declared_type) for field in plan.fields] == [
        ("categoria", "text", ".cat", None, "STRING"),
        ("precio", "regex", ".price", "[0-9.]+", "NUMBER"),
        ("enlace", "attr", "a", "href", "AUTO"),
    ]
    assert plan.export_format == "JSON" and plan.export_path == "catalogo/datos.json"
    expression = plan.filter_expression
    assert isinstance(expression, OrExpression)
    left, right = expression.operands
    assert isinstance(left, Comparison) and left.left == Identifier("categoria")
    assert left.operator == "==" and left.right == StringLiteral("Libros")
    assert isinstance(right, AndExpression)
    assert [(node.left, node.operator, node.right) for node in right.operands] == [
        (Identifier("precio"), ">=", NumberLiteral(10.0)),
        (Identifier("precio"), "<=", NumberLiteral(50.0)),
    ]


@pytest.mark.parametrize("where", [
    'WHERE (titulo == "a" OR titulo == "b") AND titulo != "c"',
    'WHERE (((titulo == "a" OR titulo == "b"))) AND (titulo != "c")',
])
def test_parentheses_override_precedence_in_ir(where):
    result = compile_source(query(where=where))
    assert result.success
    expression = result.plan.filter_expression
    assert isinstance(expression, AndExpression)
    assert isinstance(expression.operands[0], OrExpression)
    assert len(expression.operands[0].operands) == 2
    assert isinstance(expression.operands[1], Comparison)


@pytest.mark.parametrize("where,code", [
    ('WHERE ((ausente == "a"))', 'S02'),
    ('WHERE ((titulo > 10))', 'S08'),
])
def test_parentheses_preserve_semantic_validation(where, code):
    result = compile_source(query(fields='titulo: text FROM "h1" AS STRING', where=where))
    assert result.phase == "semantic" and result.plan is None
    assert [error.code for error in result.diagnostics] == [code]
