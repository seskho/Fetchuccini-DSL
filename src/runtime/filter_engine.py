"""Intérprete de nodos WHERE con precedencia conservada en la IR."""

import operator

from src.ir.models import (
    AndExpression, Comparison, Identifier, NumberLiteral, OrExpression, StringLiteral,
)

from .errors import FetchucciniRuntimeError
from .type_conversion import to_number


OPERATORS = {
    "==": operator.eq, "!=": operator.ne,
    "<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge,
}


def _operand(expression, record, field_types):
    if isinstance(expression, Identifier):
        if expression.name not in record:
            raise FetchucciniRuntimeError(
                "Identificador ausente del registro.", "R03", field=expression.name,
            )
        return record[expression.name], field_types.get(expression.name, "AUTO"), expression.name
    if isinstance(expression, NumberLiteral):
        return expression.value, "NUMBER", None
    if isinstance(expression, StringLiteral):
        return expression.value, "STRING", None
    raise FetchucciniRuntimeError("Operando desconocido en el plan.", "R03")


def evaluate_filter(expression, record, fields=(), record_index=1):
    """Evalúa con cortocircuito; un índice de registro comienza en 1."""
    field_types = {field.alias: field.declared_type for field in fields}

    def evaluate(node):
        try:
            return evaluate_node(node)
        except FetchucciniRuntimeError as error:
            if error.line is None and isinstance(node, Comparison):
                error.line, error.column = node.line, node.column
            if error.record_index is None:
                error.record_index = record_index
            raise

    def evaluate_node(node):
        if node is None:
            return True
        if isinstance(node, AndExpression):
            return all(evaluate(operand) for operand in node.operands)
        if isinstance(node, OrExpression):
            return any(evaluate(operand) for operand in node.operands)
        if not isinstance(node, Comparison) or node.operator not in OPERATORS:
            raise FetchucciniRuntimeError("Expresión desconocida en el plan.", "R03")
        left, left_type, left_field = _operand(node.left, record, field_types)
        right, right_type, right_field = _operand(node.right, record, field_types)
        if left is None or right is None:
            return False
        numeric = node.operator in {"<", "<=", ">", ">="} or (
            isinstance(left, (int, float)) or isinstance(right, (int, float))
        )
        if numeric:
            # Un literal de cadena puede convertirse para un operador de orden;
            # la anotación AS STRING de un campo siempre prohíbe ese uso.
            equality = node.operator in {"==", "!="}
            if (
                left_type == "STRING" and (left_field is not None or equality)
                or right_type == "STRING" and (right_field is not None or equality)
            ):
                raise FetchucciniRuntimeError(
                    "Una comparación numérica no admite operandos STRING explícitos.",
                    "R02", field=left_field or right_field, record_index=record_index,
                )
            left = to_number(left, field=left_field, record_index=record_index)
            right = to_number(right, field=right_field, record_index=record_index)
        elif not isinstance(left, str) or not isinstance(right, str):
            raise FetchucciniRuntimeError(
                "Los operandos de igualdad tienen tipos incompatibles.", "R02",
                field=left_field or right_field, record_index=record_index,
            )
        return OPERATORS[node.operator](left, right)

    return evaluate(expression)
