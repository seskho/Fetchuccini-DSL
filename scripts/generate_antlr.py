"""Regenera o verifica ANTLR 4.13.2, normalizando sus artefactos a LF."""

import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
VERSION = "4.13.2"
JAR_NAME = f"antlr-{VERSION}-complete.jar"
JAR_URL = f"https://www.antlr.org/download/{JAR_NAME}"
JAR_SHA256 = "eae2dfa119a64327444672aff63e9ec35a20180dc5b8090b7a6ab85125df4d76"
ARTIFACTS = ("FetchucciniLexer.py", "FetchucciniParser.py", "FetchucciniParserVisitor.py")


def obtain_jar(path: Path) -> Path:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Descargando {JAR_URL}")
        with urlopen(JAR_URL, timeout=30) as response:
            data = response.read(5_000_001)
        if hashlib.sha256(data).hexdigest() != JAR_SHA256:
            raise ValueError("El JAR descargado no coincide con el SHA-256 de ANTLR 4.13.2")
        path.write_bytes(data)
    if hashlib.sha256(path.read_bytes()).hexdigest() != JAR_SHA256:
        raise ValueError(f"El JAR {path} no coincide con ANTLR 4.13.2")
    return path.resolve()


def generate(jar: Path, destination: Path) -> None:
    # Los nombres relativos fijan la cabecera generada, independientemente del checkout.
    command = [
        "java", "-jar", str(jar), "-Dlanguage=Python3", "-visitor", "-no-listener",
        "-Werror", "-encoding", "UTF-8", "-Xexact-output-dir", "-o", str(destination),
        "FetchucciniLexer.g4", "FetchucciniParser.g4",
    ]
    subprocess.run(command, cwd=ROOT / "grammar", check=True)
    # Java usa el salto de línea del sistema; LF permite comparar entre plataformas.
    for name in ARTIFACTS:
        artifact = destination / name
        artifact.write_bytes(artifact.read_bytes().replace(b"\r\n", b"\n"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Comparar bytes sin modificar los artefactos")
    parser.add_argument("--jar", type=Path, default=ROOT / ".antlr" / JAR_NAME)
    args = parser.parse_args()
    try:
        jar = obtain_jar(args.jar)
        with tempfile.TemporaryDirectory(prefix="fetchuccini-antlr-") as temporary:
            destination = Path(temporary)
            generate(jar, destination)
            generated_dir = ROOT / "src" / "generated"
            if args.check:
                mismatches = [
                    name for name in ARTIFACTS
                    if not (generated_dir / name).exists()
                    or (generated_dir / name).read_bytes() != (destination / name).read_bytes()
                ]
                if mismatches:
                    print("Artefactos desactualizados: " + ", ".join(mismatches))
                    return 1
                print("ANTLR 4.13.2: los tres artefactos coinciden byte por byte con las gramáticas.")
            else:
                generated_dir.mkdir(parents=True, exist_ok=True)
                for name in ARTIFACTS:
                    shutil.copyfile(destination / name, generated_dir / name)
                print("ANTLR 4.13.2: lexer, parser y visitor regenerados.")
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"No se pudo regenerar ANTLR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
