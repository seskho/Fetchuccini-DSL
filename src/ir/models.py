"""Plan y expresiones tipadas que intercambian el front-end y el runtime."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple, Union


@dataclass(frozen=True)
class Identifier:
    name: str


@dataclass(frozen=True)
class StringLiteral:
    value: str


@dataclass(frozen=True)
class NumberLiteral:
    value: float


Operand = Union[Identifier, StringLiteral, NumberLiteral]


@dataclass(frozen=True)
class Comparison:
    left: Operand
    operator: str
    right: Operand
    line: int = 0
    column: int = 0


@dataclass(frozen=True)
class AndExpression:
    operands: Tuple[FilterExpression, ...]


@dataclass(frozen=True)
class OrExpression:
    operands: Tuple[FilterExpression, ...]


FilterExpression = Union[Comparison, AndExpression, OrExpression]


@dataclass(frozen=True)
class FieldPlan:
    alias: str
    extractor_type: str
    selector: str
    extractor_argument: Optional[str] = None
    declared_type: str = "AUTO"
    line: int = 0
    column: int = 0


@dataclass(frozen=True)
class ExecutionPlan:
    source_url: str
    each_selector: Optional[str]
    fields: Tuple[FieldPlan, ...]
    filter_expression: Optional[FilterExpression]
    export_format: str
    export_path: str
