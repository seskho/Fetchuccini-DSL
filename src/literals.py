"""Decodificación compartida de los literales STRING definidos por el lexer."""


_ESCAPES = {
    "b": "\b", "t": "\t", "n": "\n", "f": "\f", "r": "\r",
    '"': '"', "'": "'", "\\": "\\",
}


def decode_string(token_text: str) -> str:
    """Interpreta solo ESC_SEQ de la gramática y conserva el texto Unicode."""
    if len(token_text) < 2 or token_text[0] != '"' or token_text[-1] != '"':
        raise ValueError("Se esperaba un literal STRING entre comillas dobles")
    content = token_text[1:-1]
    result = []
    index = 0
    while index < len(content):
        character = content[index]
        if character == "\\":
            index += 1
            if index >= len(content) or content[index] not in _ESCAPES:
                raise ValueError("Secuencia de escape no admitida por STRING")
            character = _ESCAPES[content[index]]
        result.append(character)
        index += 1
    return "".join(result)
