"""
Módulo de análisis semántico preliminar para Fetchuccini (Hito 1).

Implementa:
- Symbol: Entrada individual de la tabla de símbolos.
- SymbolTable: Tabla hash para gestión de declaraciones y consultas O(1).
- FetchucciniSemanticChecker: Visitor de validación semántica sobre el parse tree.
- SemanticError: Excepción que representa errores semánticos con línea y columna.
"""

from .semantic_checker import (
    Symbol,
    SymbolTable,
    FetchucciniSemanticChecker,
    SemanticError,
)

__all__ = [
    "Symbol",
    "SymbolTable",
    "FetchucciniSemanticChecker",
    "SemanticError",
]
