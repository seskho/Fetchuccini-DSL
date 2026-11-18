"""HTTP acotado a orígenes permitidos y sockets fijados a IP públicas.

El adaptador usa el punto de extensión ConnectionCls de urllib3 2.8.0.
Cada socket resuelve una sola vez y conecta al sockaddr validado, manteniendo
el hostname original para Host, SNI y verificación de certificado TLS.
"""

import ipaddress
import socket
import time
from urllib.parse import urljoin, urlsplit

import requests
from requests.adapters import HTTPAdapter
from urllib3.connection import HTTPConnection, HTTPSConnection
from urllib3.connectionpool import HTTPConnectionPool, HTTPSConnectionPool
from urllib3.exceptions import NewConnectionError

from .errors import FetchucciniRuntimeError


DEFAULT_ALLOWED_ORIGINS = (
    "http://books.toscrape.com", "https://books.toscrape.com",
)
REDIRECT_STATUSES = {301, 302, 303, 307, 308}


def _public_ip(value):
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        return False
    if isinstance(address, ipaddress.IPv6Address):
        # IPv6 site-local está obsoleto, pero is_global puede devolver True.
        if address.is_site_local:
            return False
        if address.ipv4_mapped is not None:
            return _public_ip(str(address.ipv4_mapped))
        if address.sixtofour is not None and not _public_ip(str(address.sixtofour)):
            return False
        # Teredo incluye direcciones encapsuladas que complican la política.
        if address.teredo is not None:
            return False
    return address.is_global and not (
        address.is_multicast or address.is_unspecified or address.is_reserved
        or address.is_loopback or address.is_private or address.is_link_local
    )


def _origin(url):
    """Normalizar origen sin hacer DNS ni permitir credenciales o controles."""
    try:
        if any(ord(character) < 33 or ord(character) == 127 for character in url):
            raise ValueError("la URL contiene espacios o controles")
        parsed = urlsplit(url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("se requiere HTTP/HTTPS y hostname")
        if parsed.username is not None or parsed.password is not None:
            raise ValueError("no se admiten credenciales en la URL")
        hostname = parsed.hostname.encode("idna").decode("ascii").lower()
        if "%" in hostname or "\\" in hostname:
            raise ValueError("hostname no admitido")
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        if port not in {80, 443}:
            raise ValueError("solo se admiten los puertos 80 y 443")
        try:
            ipaddress.ip_address(hostname)
        except ValueError:
            pass
        else:
            if not _public_ip(hostname):
                raise ValueError("el destino no es una IP pública")
        return parsed.scheme, hostname, port
    except (ValueError, UnicodeError) as error:
        raise FetchucciniRuntimeError(f"URL HTTP no admitida: {error}", "R01") from error


def _connect_public(connection):
    """Conectar directamente a una IP validada, sin una segunda resolución."""
    try:
        addresses = socket.getaddrinfo(
            connection._dns_host, connection.port, socket.AF_UNSPEC, socket.SOCK_STREAM,
        )
    except OSError as error:
        raise NewConnectionError(connection, f"No se pudo resolver el hostname: {error}") from error
    if not addresses or any(not _public_ip(item[4][0]) for item in addresses):
        raise FetchucciniRuntimeError(
            "DNS resolvió un destino no público; conexión bloqueada antes de abrir el socket.", "R01",
        )
    last_error = None
    for family, socktype, protocol, _, sockaddr in addresses:
        sock = None
        try:
            sock = socket.socket(family, socktype, protocol)
            timeout = connection.timeout
            if timeout is not None and not isinstance(timeout, (int, float)):
                timeout = socket.getdefaulttimeout()
            sock.settimeout(timeout)
            for option in connection.socket_options or ():
                sock.setsockopt(*option)
            if connection.source_address:
                sock.bind(connection.source_address)
            # sockaddr contiene una IP numérica proveniente de la única resolución.
            sock.connect(sockaddr)
            peer = sock.getpeername()[0]
            if not _public_ip(peer) or ipaddress.ip_address(peer) != ipaddress.ip_address(sockaddr[0]):
                raise FetchucciniRuntimeError("La IP efectiva no coincide con la IP pública aprobada.", "R01")
            return sock
        except FetchucciniRuntimeError:
            if sock is not None:
                sock.close()
            raise
        except OSError as error:
            last_error = error
            if sock is not None:
                sock.close()
    raise NewConnectionError(connection, f"No se pudo conectar: {last_error}") from last_error


class PublicHTTPConnection(HTTPConnection):
    def _new_conn(self):
        return _connect_public(self)


class PublicHTTPSConnection(HTTPSConnection):
    def _new_conn(self):
        return _connect_public(self)


class PublicHTTPConnectionPool(HTTPConnectionPool):
    ConnectionCls = PublicHTTPConnection


class PublicHTTPSConnectionPool(HTTPSConnectionPool):
    ConnectionCls = PublicHTTPSConnection


class PublicAddressAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        super().init_poolmanager(connections, maxsize, block=block, **pool_kwargs)
        # Copia por instancia: no modificar los pools globales de otras aplicaciones.
        self.poolmanager.pool_classes_by_scheme = {
            "http": PublicHTTPConnectionPool, "https": PublicHTTPSConnectionPool,
        }

    def proxy_manager_for(self, proxy, **proxy_kwargs):
        raise FetchucciniRuntimeError("No se permiten proxies en el cliente HTTP de Fetchuccini.", "R01")


class RequestsHttpClient:
    """Cliente reemplazable; fetch(url) devuelve HTML y nunca exporta archivos.

    total_timeout es un plazo cooperativo comprobado entre operaciones; no
    interrumpe getaddrinfo del sistema ni reemplaza los timeouts de socket.
    """

    def __init__(
        self, *, allowed_origins=DEFAULT_ALLOWED_ORIGINS, timeout=(5, 10),
        max_bytes=5 * 1024 * 1024, max_redirects=3, total_timeout=30,
    ):
        self.allowed_origins = frozenset(_origin(url) for url in allowed_origins)
        self.timeout = timeout
        self.max_bytes = max_bytes
        self.max_redirects = max_redirects
        self.total_timeout = total_timeout

    def _validate_destination(self, url):
        if _origin(url) not in self.allowed_origins:
            raise FetchucciniRuntimeError(
                "El origen no está autorizado. Por defecto solo se permite Books to Scrape; "
                "otro origen requiere configurar allowed_origins explícitamente en la API.", "R01",
            )

    def fetch(self, url):
        started = time.monotonic()
        current = url
        with requests.Session() as session:
            # Ignora proxies de entorno y .netrc; nunca importa sesiones privadas.
            session.trust_env = False
            adapter = PublicAddressAdapter(max_retries=0)
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            session.headers.update({
                "User-Agent": "Fetchuccini/0.2 (UPC; static HTML academic demo)",
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Encoding": "identity",
                "Connection": "close",
            })
            for redirect_count in range(self.max_redirects + 1):
                if time.monotonic() - started > self.total_timeout:
                    raise FetchucciniRuntimeError("Se superó el plazo total de descarga.", "R01")
                self._validate_destination(current)
                try:
                    # Los redirects se procesan manualmente para validar cada destino.
                    with session.get(current, timeout=self.timeout, stream=True, allow_redirects=False) as response:
                        if response.status_code in REDIRECT_STATUSES:
                            location = response.headers.get("Location")
                            if not location:
                                raise FetchucciniRuntimeError("Redirección sin cabecera Location.", "R01")
                            if redirect_count >= self.max_redirects:
                                raise FetchucciniRuntimeError("Se superó el límite de redirecciones.", "R01")
                            current = urljoin(current, location)
                            self._validate_destination(current)
                            session.cookies.clear()
                            continue
                        response.raise_for_status()
                        if not 200 <= response.status_code < 300:
                            raise FetchucciniRuntimeError(f"Respuesta HTTP no exitosa: {response.status_code}.", "R01")
                        declared_length = response.headers.get("Content-Length")
                        if declared_length:
                            try:
                                excessive = int(declared_length) > self.max_bytes
                            except ValueError:
                                excessive = False
                            if excessive:
                                raise FetchucciniRuntimeError("El HTML supera el tamaño máximo permitido.", "R01")
                        chunks = []
                        size = 0
                        for chunk in response.iter_content(chunk_size=65536):
                            size += len(chunk)
                            if size > self.max_bytes:
                                raise FetchucciniRuntimeError("El HTML supera el tamaño máximo permitido.", "R01")
                            if time.monotonic() - started > self.total_timeout:
                                raise FetchucciniRuntimeError("Se superó el plazo total de descarga.", "R01")
                            chunks.append(chunk)
                        if time.monotonic() - started > self.total_timeout:
                            raise FetchucciniRuntimeError("Se superó el plazo total de descarga.", "R01")
                        content = b"".join(chunks)
                        # Beautiful Soup detecta meta charset cuando no hay charset HTTP.
                        encoding = requests.utils.get_encoding_from_headers(response.headers)
                        if not encoding or (
                            encoding.lower() == "iso-8859-1"
                            and "charset=" not in response.headers.get("Content-Type", "").lower()
                        ):
                            from bs4 import UnicodeDammit
                            return UnicodeDammit(content, is_html=True).unicode_markup or ""
                        return content.decode(encoding, errors="replace")
                except FetchucciniRuntimeError:
                    raise
                except (requests.RequestException, OSError, LookupError, UnicodeError) as error:
                    raise FetchucciniRuntimeError(f"No se pudo obtener el HTML: {error}", "R01") from error
        raise FetchucciniRuntimeError("No se obtuvo una respuesta HTML.", "R01")
