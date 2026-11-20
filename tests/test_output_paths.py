import os
from dataclasses import replace

import pytest

from src.output_paths import resolve_output_path, validate_export_path
from src.runtime.errors import FetchucciniRuntimeError
from src.runtime.execution_engine import execute_plan


@pytest.mark.parametrize("path", [
    "../datos.json", "sub/../../datos.json", r"..\datos.json", "/datos.json",
    r"C:\datos.json", r"C:datos.json", r"\\servidor\share\datos.json",
    "datos.json:secreto", "", "datos.csv", "a//datos.json", "./datos.json",
    "a/./datos.json", "CON.json", "a/NUL.json", "a /datos.json", "datos.json ",
    "datos\x00.json", "datos\n.json", "?.json",
])
def test_unsafe_or_incompatible_path(path):
    with pytest.raises(ValueError):
        validate_export_path(path, "JSON")


@pytest.mark.parametrize("path", ["datos.json", "sub/catálogo.json", r"sub\datos.json", "DATOS.JSON"])
def test_valid_nested_path_is_confined_without_creation(path, tmp_path):
    validate_export_path(path, "JSON")
    resolved = resolve_output_path(path, tmp_path)
    assert resolved.is_relative_to(tmp_path.resolve())
    assert not resolved.exists()


def _directory_link(target, link):
    if os.name == "nt":
        import _winapi
        _winapi.CreateJunction(str(target), str(link))
    else:
        link.symlink_to(target, target_is_directory=True)


def test_symlink_or_windows_junction_cannot_escape_output(make_plan, catalog_html, tmp_path):
    root = tmp_path / "outputs"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    _directory_link(outside, root / "escape")
    plan = replace(make_plan(), export_path="escape/datos.json")
    with pytest.raises(FetchucciniRuntimeError):
        execute_plan(plan, root, html=catalog_html)
    assert not (outside / "datos.json").exists()


def test_output_root_cannot_itself_be_a_link(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    root = tmp_path / "outputs"
    _directory_link(outside, root)
    with pytest.raises(ValueError):
        resolve_output_path("datos.json", root)
