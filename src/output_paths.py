"""Política común de destinos de exportación, sin crear archivos al compilar."""

import re
from pathlib import Path, PurePosixPath, PureWindowsPath

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs"
_RESERVED = {"CON", "PRN", "AUX", "NUL"} | {
    f"{prefix}{number}" for prefix in ("COM", "LPT") for number in range(1, 10)
}


def validate_export_path(path: str, export_format: str) -> None:
    """Rechaza rutas no portables o capaces de salir de outputs (S07)."""
    if export_format not in {"JSON", "CSV"}:
        raise ValueError("Solo se permiten los formatos JSON y CSV.")
    if not path or not path.strip():
        raise ValueError("El destino de exportación no puede estar vacío.")
    windows_path = PureWindowsPath(path)
    normalized = path.replace("\\", "/")
    if windows_path.drive or windows_path.root or PurePosixPath(normalized).is_absolute():
        raise ValueError("El destino debe ser relativo al directorio outputs/.")
    parts = normalized.split("/")
    for part in parts:
        if part in {"", ".", ".."}:
            raise ValueError("La ruta no admite segmentos vacíos, '.' ni traversal '..'.")
        if part.endswith((" ", ".")) or re.search(r'[<>:"|?*\x00-\x1f\x7f]', part):
            raise ValueError("La ruta contiene caracteres o terminaciones no admitidos.")
        if part.split(".", 1)[0].upper() in _RESERVED:
            raise ValueError("La ruta utiliza un nombre de dispositivo reservado.")
    expected_suffix = "." + export_format.lower()
    if PurePosixPath(normalized).suffix.lower() != expected_suffix:
        raise ValueError(f"El formato {export_format} requiere la extensión {expected_suffix}.")


def resolve_output_path(path: str, output_dir=None) -> Path:
    """Resuelve y comprueba enlaces existentes antes de la escritura del runtime."""
    root = Path(output_dir) if output_dir is not None else DEFAULT_OUTPUT_DIR
    if root.is_symlink() or (hasattr(root, "is_junction") and root.is_junction()):
        raise ValueError("El directorio de salida no puede ser un enlace o junction.")
    root = root.resolve()
    suffix = PurePosixPath(path.replace("\\", "/")).suffix.lower()
    validate_export_path(path, {".json": "JSON", ".csv": "CSV"}.get(suffix, ""))
    destination = (root / Path(*path.replace("\\", "/").split("/"))).resolve()
    if not destination.is_relative_to(root):
        raise ValueError("El destino resuelto sale del directorio de salida.")
    return destination
