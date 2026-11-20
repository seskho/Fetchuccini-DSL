"""Representación JSON del plan con etiquetas explícitas y versión de formato."""

from dataclasses import fields, is_dataclass, replace

from src.runtime.exporter import export_records


def plan_to_dict(plan):
    def encode(value):
        if is_dataclass(value):
            return {"node": type(value).__name__,
                    **{field.name: encode(getattr(value, field.name)) for field in fields(value)}}
        if isinstance(value, (tuple, list)):
            return [encode(item) for item in value]
        return value

    return {"ir_version": 1, "plan": encode(plan)}


def export_plan(plan, path, output_dir=None):
    """Escribe JSON atómico bajo outputs, con las mismas restricciones de rutas."""
    destination = replace(plan, export_path=path, export_format="JSON")
    return export_records(destination, plan_to_dict(plan), output_dir)
