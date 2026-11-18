"""Errores de ejecución separados de las fases de compilación."""


class FetchucciniRuntimeError(Exception):
    phase = "runtime"

    def __init__(self, message, code="R01", *, field=None, record_index=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.field = field
        self.record_index = record_index

    def __str__(self):
        location = ""
        if self.field is not None:
            location += f"; campo '{self.field}'"
        if self.record_index is not None:
            location += f"; registro {self.record_index}"
        return f"[{self.code}] Error de ejecución (fase runtime{location}): {self.message}"
