"""Conversión numérica explícita y diferida para campos AUTO."""

import math

from .errors import FetchucciniRuntimeError


def to_number(value, *, field=None, record_index=None):
    """NUMBER usa float finito; rechaza NaN/Infinity en HTML o comparaciones."""
    try:
        number = float(value)
        if not math.isfinite(number):
            raise ValueError("valor no finito")
        return number
    except (ValueError, TypeError, OverflowError) as error:
        raise FetchucciniRuntimeError(
            f"El valor {value!r} no puede convertirse a NUMBER finito.",
            "R02", field=field, record_index=record_index,
        ) from error


def convert_field(value, field, record_index):
    if value is None:
        return None
    if field.declared_type == "NUMBER":
        return to_number(value, field=field.alias, record_index=record_index)
    return str(value)
