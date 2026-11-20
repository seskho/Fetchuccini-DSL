from pathlib import Path
import socket

import pytest

from src.compiler import compile_source


def pytest_addoption(parser):
    parser.addoption("--run-live", action="store_true", default=False,
                     help="Ejecutar la integración HTTP real marcada integration")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-live"):
        return
    normal = [item for item in items if "integration" not in item.keywords]
    external = [item for item in items if "integration" in item.keywords]
    items[:] = normal
    config.hook.pytest_deselected(items=external)


@pytest.fixture(autouse=True)
def block_network_in_normal_suite(request, monkeypatch):
    """Una prueba local que intente usar red por accidente debe fallar."""
    if request.node.get_closest_marker("integration") is None:
        def blocked(*args, **kwargs):
            raise AssertionError("La suite normal no permite DNS ni conexiones reales.")
        monkeypatch.setattr(socket, "getaddrinfo", blocked)
        monkeypatch.setattr(socket.socket, "connect", blocked)


@pytest.fixture
def catalog_html():
    return (Path(__file__).parent / "fixtures" / "catalogo.html").read_text(encoding="utf-8")


@pytest.fixture
def make_plan():
    def build(fields='titulo: text FROM "h3 a"', where="", each='EACH "article.product_pod"',
              export_format="JSON", path=None):
        destination = path or ("datos." + export_format.lower())
        source = (f'FETCH "https://books.toscrape.com/"\n{each}\n'
                  f'EXTRACT {{ {fields} }}\n{where}\n'
                  f'EXPORT AS {export_format} TO "{destination}";')
        result = compile_source(source)
        assert result.success, [str(error) for error in result.diagnostics]
        return result.plan
    return build
