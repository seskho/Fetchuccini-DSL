"""
Módulo de análisis semántico preliminar para Fetchuccini (Hito 1).

Este módulo implementa las validaciones semánticas del lenguaje:
1. Detección de alias duplicados en el bloque EXTRACT.
2. Detección de identificadores en WHERE que no hayan sido declarados en EXTRACT.
"""

from .semantic_checker import FetchucciniSemanticChecker, SemanticError

__all__ = ["FetchucciniSemanticChecker", "SemanticError"]
