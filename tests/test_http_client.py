"""Transporte HTTP simulado: ninguna prueba abre conexiones de red reales."""

import socket
from unittest.mock import Mock

import pytest
import requests

from src.runtime import http_client as http
from src.runtime.errors import FetchucciniRuntimeError


class FakeResponse:
    def __init__(self, status=200, headers=None, chunks=None):
        self.status_code = status
        self.headers = requests.structures.CaseInsensitiveDict(headers or {})
        self.chunks = [b"<h1>Hola</h1>"] if chunks is None else chunks
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.closed = True

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")

    def iter_content(self, chunk_size):
        assert chunk_size == 65536
        yield from self.chunks


class FakeSession:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []
        self.mounts = {}
        self.headers = {}
        self.cookies = Mock()
        self.trust_env = True
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.closed = True

    def mount(self, prefix, adapter):
        self.mounts[prefix] = adapter

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        return response


@pytest.mark.parametrize("address", [
    "127.0.0.1", "0.0.0.0", "10.0.0.1", "172.16.0.1", "192.168.0.1",
    "169.254.169.254", "100.64.0.1", "192.0.2.1", "224.0.0.1",
    "::1", "::", "fe80::1", "fec0::1", "fc00::1", "ff02::1", "::ffff:127.0.0.1",
])
def test_non_public_addresses_are_rejected(address):
    assert not http._public_ip(address)


@pytest.mark.parametrize("connection_class", [http.PublicHTTPConnection, http.PublicHTTPSConnection])
def test_dns_private_or_mixed_response_opens_no_socket(monkeypatch, connection_class):
    answers = [
        (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443)),
        (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.0.0.1", 443)),
    ]
    monkeypatch.setattr(http.socket, "getaddrinfo", Mock(return_value=answers))
    factory = Mock()
    monkeypatch.setattr(http.socket, "socket", factory)
    with pytest.raises(FetchucciniRuntimeError, match="no público"):
        connection_class("books.toscrape.com", port=443, timeout=1)._new_conn()
    factory.assert_not_called()


@pytest.mark.parametrize("connection_class", [http.PublicHTTPConnection, http.PublicHTTPSConnection])
def test_socket_pins_the_only_dns_resolution(monkeypatch, connection_class):
    sockaddr = ("93.184.216.34", 443)
    dns = Mock(return_value=[(socket.AF_INET, socket.SOCK_STREAM, 6, "", sockaddr)])
    sock = Mock()
    sock.getpeername.return_value = sockaddr
    monkeypatch.setattr(http.socket, "getaddrinfo", dns)
    monkeypatch.setattr(http.socket, "socket", Mock(return_value=sock))
    connection = connection_class("books.toscrape.com", port=443, timeout=1)
    assert connection._new_conn() is sock
    dns.assert_called_once_with("books.toscrape.com", 443, socket.AF_UNSPEC, socket.SOCK_STREAM)
    sock.connect.assert_called_once_with(sockaddr)
    sock.settimeout.assert_called_once_with(1)
    # HTTPS conserva host original para la verificación TLS de urllib3.
    assert connection.host == "books.toscrape.com"


@pytest.mark.parametrize("peer", ["10.0.0.1", "8.8.8.8"])
def test_different_effective_peer_is_rejected_and_closed(monkeypatch, peer):
    dns = Mock(return_value=[(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))])
    sock = Mock()
    sock.getpeername.return_value = (peer, 443)
    monkeypatch.setattr(http.socket, "getaddrinfo", dns)
    monkeypatch.setattr(http.socket, "socket", Mock(return_value=sock))
    with pytest.raises(FetchucciniRuntimeError, match="IP efectiva"):
        http.PublicHTTPConnection("books.toscrape.com", port=443, timeout=1)._new_conn()
    sock.close.assert_called_once()


def test_adapter_uses_both_public_connection_classes_and_disallows_proxy():
    adapter = http.PublicAddressAdapter()
    for scheme, expected in [("http", http.PublicHTTPConnection), ("https", http.PublicHTTPSConnection)]:
        pool = adapter.poolmanager.connection_from_url(f"{scheme}://books.toscrape.com")
        assert pool.ConnectionCls is expected
    with pytest.raises(FetchucciniRuntimeError, match="proxies"):
        adapter.proxy_manager_for("http://localhost:8080")
    adapter.close()


@pytest.mark.parametrize("url", [
    "file:///etc/passwd", "ftp://books.toscrape.com", "http://localhost",
    "http://127.0.0.1", "http://169.254.169.254", "https://example.com",
    "https://books.toscrape.com:8080", "https://user:secret@books.toscrape.com",
    "https://books.toscrape.com\n.evil.example",
])
def test_blocked_urls_make_no_get(monkeypatch, url):
    session = FakeSession([])
    monkeypatch.setattr(http.requests, "Session", lambda: session)
    with pytest.raises(FetchucciniRuntimeError):
        http.RequestsHttpClient().fetch(url)
    assert session.calls == []
    assert session.closed


def test_http_configuration_timeout_user_agent_and_cleanup(monkeypatch):
    response = FakeResponse()
    session = FakeSession([response])
    monkeypatch.setattr(http.requests, "Session", lambda: session)
    assert http.RequestsHttpClient(timeout=(2, 3)).fetch("https://books.toscrape.com/") == "<h1>Hola</h1>"
    assert session.calls == [
        ("https://books.toscrape.com/", {"timeout": (2, 3), "stream": True, "allow_redirects": False})
    ]
    assert session.trust_env is False
    assert "Fetchuccini" in session.headers["User-Agent"]
    assert session.headers["Connection"] == "close"
    assert all(isinstance(adapter, http.PublicAddressAdapter) for adapter in session.mounts.values())
    assert session.closed and response.closed


@pytest.mark.parametrize("response", [
    FakeResponse(404), FakeResponse(500), requests.Timeout("timeout"),
    requests.ConnectionError("connection failed"), FakeResponse(304),
])
def test_http_errors_are_runtime_and_close_session(monkeypatch, response):
    session = FakeSession([response])
    monkeypatch.setattr(http.requests, "Session", lambda: session)
    with pytest.raises(FetchucciniRuntimeError) as captured:
        http.RequestsHttpClient().fetch("https://books.toscrape.com/")
    assert captured.value.code == "R01" and captured.value.phase == "runtime"
    assert session.closed


@pytest.mark.parametrize("response", [
    FakeResponse(headers={"Content-Length": "11"}),
    FakeResponse(chunks=[b"12345", b"678901"]),
])
def test_declared_and_streamed_size_limits(monkeypatch, response):
    session = FakeSession([response])
    monkeypatch.setattr(http.requests, "Session", lambda: session)
    with pytest.raises(FetchucciniRuntimeError, match="tamaño máximo"):
        http.RequestsHttpClient(max_bytes=10).fetch("https://books.toscrape.com/")
    assert response.closed


@pytest.mark.parametrize("location", ["http://localhost/private", "https://evil.example/", "http://169.254.169.254/latest/"])
def test_every_redirect_destination_is_validated_before_get(monkeypatch, location):
    response = FakeResponse(302, {"Location": location})
    session = FakeSession([response])
    monkeypatch.setattr(http.requests, "Session", lambda: session)
    with pytest.raises(FetchucciniRuntimeError):
        http.RequestsHttpClient().fetch("https://books.toscrape.com/")
    assert len(session.calls) == 1
    assert response.closed


def test_relative_redirect_allowed_and_cookies_cleared(monkeypatch):
    session = FakeSession([FakeResponse(302, {"Location": "/catalogue/"}), FakeResponse()])
    monkeypatch.setattr(http.requests, "Session", lambda: session)
    assert http.RequestsHttpClient().fetch("https://books.toscrape.com/") == "<h1>Hola</h1>"
    assert [call[0] for call in session.calls] == ["https://books.toscrape.com/", "https://books.toscrape.com/catalogue/"]
    session.cookies.clear.assert_called_once()


def test_redirect_limit_and_missing_location(monkeypatch):
    session = FakeSession([FakeResponse(302, {"Location": "/"}) for _ in range(3)])
    monkeypatch.setattr(http.requests, "Session", lambda: session)
    with pytest.raises(FetchucciniRuntimeError, match="límite de redirecciones"):
        http.RequestsHttpClient(max_redirects=2).fetch("https://books.toscrape.com/")
    assert len(session.calls) == 3
    session = FakeSession([FakeResponse(302)])
    with pytest.raises(FetchucciniRuntimeError, match="sin cabecera Location"):
        http.RequestsHttpClient().fetch("https://books.toscrape.com/")


def test_total_deadline_checked_during_body(monkeypatch):
    response = FakeResponse()
    session = FakeSession([response])
    monkeypatch.setattr(http.requests, "Session", lambda: session)
    monkeypatch.setattr(http.time, "monotonic", Mock(side_effect=[0, 0, 31]))
    with pytest.raises(FetchucciniRuntimeError, match="plazo total"):
        http.RequestsHttpClient(total_timeout=30).fetch("https://books.toscrape.com/")
    assert response.closed


@pytest.mark.parametrize("headers,body", [
    ({"Content-Type": "text/html; charset=utf-8"}, "Español".encode("utf-8")),
    ({"Content-Type": "text/html"}, '<meta charset="utf-8">Español'.encode("utf-8")),
])
def test_character_encoding_from_http_or_html(monkeypatch, headers, body):
    session = FakeSession([FakeResponse(headers=headers, chunks=[body])])
    monkeypatch.setattr(http.requests, "Session", lambda: session)
    assert "Español" in http.RequestsHttpClient().fetch("https://books.toscrape.com/")


def test_additional_origin_requires_explicit_api_configuration(monkeypatch):
    session = FakeSession([FakeResponse()])
    monkeypatch.setattr(http.requests, "Session", lambda: session)
    assert http.RequestsHttpClient(allowed_origins=["https://example.com"]).fetch("https://example.com/")


def test_connect_failure_closes_socket_before_public_fallback(monkeypatch):
    addresses = [
        (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443)),
        (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("8.8.8.8", 443)),
    ]
    first, second = Mock(), Mock()
    first.connect.side_effect = socket.timeout("connect timeout")
    second.getpeername.return_value = ("8.8.8.8", 443)
    monkeypatch.setattr(http.socket, "getaddrinfo", Mock(return_value=addresses))
    monkeypatch.setattr(http.socket, "socket", Mock(side_effect=[first, second]))
    connection = http.PublicHTTPSConnection("books.toscrape.com", port=443, timeout=1)
    assert connection._new_conn() is second
    first.close.assert_called_once()
    second.connect.assert_called_once_with(("8.8.8.8", 443))


def test_stream_failure_closes_response_and_is_runtime(monkeypatch):
    class BrokenResponse(FakeResponse):
        def iter_content(self, chunk_size):
            yield b"partial"
            raise requests.ConnectionError("stream interrupted")
    response = BrokenResponse()
    session = FakeSession([response])
    monkeypatch.setattr(http.requests, "Session", lambda: session)
    with pytest.raises(FetchucciniRuntimeError, match="stream interrupted"):
        http.RequestsHttpClient().fetch("https://books.toscrape.com/")
    assert response.closed and session.closed
