"""Orquestación del backend usando únicamente un plan independiente de ANTLR."""

from dataclasses import dataclass
from pathlib import Path

from src.output_paths import resolve_output_path, validate_export_path

from .errors import FetchucciniRuntimeError
from .exporter import export_records
from .extractor import extract_records
from .filter_engine import evaluate_filter
from .http_client import RequestsHttpClient


@dataclass(frozen=True)
class ExecutionResult:
    found_count: int
    filtered_count: int
    exported_count: int
    output_path: Path
    records: list

    @property
    def discarded_count(self):
        return self.found_count - self.filtered_count


def execute_plan(plan, output_dir=None, http_client=None, html=None):
    # Rechazar destinos inseguros aun cuando alguien entregue una IR manual.
    try:
        validate_export_path(plan.export_path, plan.export_format)
        resolve_output_path(plan.export_path, output_dir)
    except (OSError, ValueError) as error:
        raise FetchucciniRuntimeError(f"Destino de exportación inválido: {error}", "R04") from error
    if html is None:
        client = http_client if http_client is not None else RequestsHttpClient()
        try:
            html = client.fetch(plan.source_url)
        except FetchucciniRuntimeError:
            raise
        except (OSError, ValueError) as error:
            raise FetchucciniRuntimeError(f"No se pudo obtener el HTML: {error}", "R01") from error
    records = extract_records(plan, html)
    retained = [
        record for index, record in enumerate(records, start=1)
        if evaluate_filter(plan.filter_expression, record, plan.fields, index)
    ]
    destination = export_records(plan, retained, output_dir)
    return ExecutionResult(len(records), len(retained), len(retained), destination, retained)
