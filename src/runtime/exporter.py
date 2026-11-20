"""Serialización UTF-8 a archivos reales dentro del directorio de salida."""

import csv
import json
import os
import tempfile

from src.output_paths import resolve_output_path, validate_export_path

from .errors import FetchucciniRuntimeError


def export_records(plan, records, output_dir=None):
    temporary = None
    try:
        validate_export_path(plan.export_path, plan.export_format)
        destination = resolve_output_path(plan.export_path, output_dir)
        destination.parent.mkdir(parents=True, exist_ok=True)
        # Revalidar tras crear directorios evita aceptar enlaces ya existentes.
        destination = resolve_output_path(plan.export_path, output_dir)
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=destination.parent,
            prefix=".fetchuccini-", suffix=".tmp", delete=False,
        ) as stream:
            temporary = stream.name
            if plan.export_format == "JSON":
                json.dump(records, stream, ensure_ascii=False, indent=2, allow_nan=False)
                stream.write("\n")
            else:
                writer = csv.DictWriter(stream, fieldnames=[field.alias for field in plan.fields])
                writer.writeheader()
                writer.writerows(records)
        destination = resolve_output_path(plan.export_path, output_dir)
        os.replace(temporary, destination)
        temporary = None
        return destination
    except (OSError, ValueError, TypeError) as error:
        raise FetchucciniRuntimeError(f"No se pudo exportar el resultado: {error}", "R04") from error
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except OSError:
                pass
