"""Extracción de campos relativa a cada contexto EACH."""

import re

import soupsieve

from .errors import FetchucciniRuntimeError
from .html_parser import parse_html
from .type_conversion import convert_field


def extract_field(context, field, record_index):
    element = context.select_one(field.selector)
    if element is None:
        return None
    if field.extractor_type == "attr":
        value = element.get(field.extractor_argument.strip())
        # Beautiful Soup representa atributos como class mediante listas.
        if isinstance(value, list):
            value = " ".join(value)
    else:
        if field.extractor_type == "text":
            value = " ".join(element.get_text(" ", strip=True).split())
        elif field.extractor_type == "regex":
            # Conservar espacios y saltos originales para patrones como \s{2}
            # o \n; únicamente el extractor text normaliza los espacios.
            match = re.search(field.extractor_argument, element.get_text())
            value = match.group(0) if match else None
        else:
            raise FetchucciniRuntimeError(
                f"Extractor desconocido: {field.extractor_type!r}.", "R03",
                field=field.alias, record_index=record_index,
            )
    return convert_field(value, field, record_index)


def extract_records(plan, html):
    try:
        document = parse_html(html)
        contexts = document.select(plan.each_selector) if plan.each_selector else [document]
        return [
            {field.alias: extract_field(context, field, index) for field in plan.fields}
            for index, context in enumerate(contexts, start=1)
        ]
    except (soupsieve.SelectorSyntaxError, re.error) as error:
        # El compilador evita este caso; también se protege el uso directo de IR.
        raise FetchucciniRuntimeError(f"Selector o regex inválido en el plan: {error}", "R03") from error
