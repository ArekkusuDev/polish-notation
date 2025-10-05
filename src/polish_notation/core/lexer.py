import re
from typing import List


class Token:
    def __init__(self, type_: str, value: str) -> None:
        self.type = type_
        self.value = value

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"

    def __hash__(self) -> int:
        return hash((self.type, self.value))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value

        return False


def tokenize(expression: str) -> List[Token]:
    """
    Convierte una expresión matemática infija en una lista de tokens léxicos.

    Args:
        expression: Expresión matemática en notación infija que puede contener
                   números, identificadores, operadores y paréntesis.

    Returns:
        Lista ordenada de tokens que representan la expresión tokenizada.

    Raises:
        ValueError: Si la expresión está vacía o contiene caracteres no válidos
                   que no corresponden a ningún patrón de token definido.

    Examples:
        >>> tokenize("A + B * 2")
        [Token(IDENTIFIER, 'A'), Token(OPERATOR, '+'), Token(IDENTIFIER, 'B'),
         Token(OPERATOR, '*'), Token(NUMBER, '2')]

        >>> tokenize("(x - 1) / 2")
        [Token(LPAREN, '('), Token(IDENTIFIER, 'x'), Token(OPERATOR, '-'),
         Token(NUMBER, '1'), Token(RPAREN, ')'), Token(OPERATOR, '/'),
         Token(NUMBER, '2')]
    """
    if not expression.strip():
        raise ValueError("La expresión no puede estar vacía")

    # Definición de patrones de tokens basada en la gramática de expresiones matemáticas
    # Se utiliza orden específico para evitar conflictos entre patrones similares
    token_spec = [
        ("NUMBER", r"\d+(\.\d+)?"),  # Números enteros y decimales
        ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),  # Variables y funciones
        ("OPERATOR", r"[+\-*/^]"),  # Operadores aritméticos con precedencia
        ("LPAREN", r"\("),  # Paréntesis izquierdo para agrupación
        ("RPAREN", r"\)"),  # Paréntesis derecho para agrupación
        ("SKIP", r"[ \t]+"),  # Espacios en blanco que se ignoran
    ]

    # Compilación de la expresión regular combinada para mayor eficiencia
    token_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec)
    tokens: List[Token] = []
    last_end = 0

    for match in re.finditer(token_regex, expression):
        # Asegura que no hay caracteres inválidos entre tokens
        # Esto previene errores de tokenización que podrían pasar desapercibidos
        if match.start() != last_end:
            invalid_char = expression[last_end : match.start()]
            raise ValueError(f"Caracter no reconocido: '{invalid_char}' en posición {last_end}")

        kind = match.lastgroup
        value = match.group()

        if kind is None or kind == "SKIP":
            last_end = match.end()
            continue

        tokens.append(Token(kind, value))
        last_end = match.end()

    # Asegura que toda la expresión fue tokenizada
    # Importante para detectar caracteres inválidos al final de la expresión
    if last_end < len(expression):
        invalid_char = expression[last_end:]
        raise ValueError(f"Caracter no reconocido: '{invalid_char}' en posición {last_end}")

    return tokens
