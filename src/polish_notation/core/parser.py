from typing import List, Optional

from .lexer import Token, tokenize
from .models import ASTNode, BinaryOp, Identifier, Number


class Parser:
    def __init__(self, tokens: List[Token]):
        """
        Inicializa el analizador con una lista de tokens.

        Args:
            tokens: Lista de tokens obtenidos del lexer.

        Raises:
            ValueError: Si la lista de tokens está vacía.
        """
        if not tokens:
            raise ValueError("La expresión no puede estar vacía")
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> ASTNode:
        """
        Analiza los tokens y construye un AST.

        Returns:
            ASTNode: Raíz del árbol de sintaxis abstracta.

        Raises:
            ValueError: Si la expresión tiene errores sintácticos.
        """
        result = self.expression()
        # Validar que se consumieron todos los tokens
        if self.pos < len(self.tokens):
            raise ValueError(f"Tokens inesperados al final de la expresión: {self.tokens[self.pos :]}")
        return result

    def expression(self) -> ASTNode:
        """
        Inicia el análisis de la expresión completa.

        Returns:
            ASTNode: El nodo raíz del AST de la expresión.
        """
        return self.additive()

    def additive(self) -> ASTNode:
        """
        Analiza expresiones con operadores aditivos (+ y -).

        Maneja la asociatividad izquierda de estos operadores.

        Returns:
            ASTNode: El nodo del AST para la expresión aditiva.
        """
        node = self.multiplicative()
        while True:
            token = self.current()
            if not token or token.type != "OPERATOR" or token.value not in "+-":
                break
            op = token.value
            self.advance()
            right = self.multiplicative()
            node = BinaryOp(node, op, right)
        return node

    def multiplicative(self) -> ASTNode:
        """
        Analiza expresiones con operadores multiplicativos (* y /).

        Maneja la asociatividad izquierda de estos operadores.

        Returns:
            ASTNode: El nodo del AST para la expresión multiplicativa.
        """
        node = self.power()
        while True:
            token = self.current()
            if not token or token.type != "OPERATOR" or token.value not in "*/":
                break
            op = token.value
            self.advance()
            right = self.power()
            node = BinaryOp(node, op, right)
        return node

    def power(self) -> ASTNode:
        """
        Analiza expresiones con operador de potencia (^).

        Maneja la asociatividad derecha del operador de potencia.

        Returns:
            ASTNode: El nodo del AST para la expresión de potencia.
        """
        node = self.primary()
        token = self.current()
        if token and token.type == "OPERATOR" and token.value == "^":
            op = token.value
            self.advance()
            right = self.power()  # Right associative
            node = BinaryOp(node, op, right)
        return node

    def primary(self) -> ASTNode:
        """
        Analiza elementos primarios de la expresión.

        Puede ser un número, identificador o una expresión entre paréntesis.

        Returns:
            ASTNode: El nodo del AST para el elemento primario.

        Raises:
            ValueError: Si hay un token inesperado o paréntesis sin cerrar.
        """
        token = self.current()
        if not token:
            raise ValueError("Fin inesperado de la entrada")
        if token.type == "LPAREN":
            self.advance()  # Skip '('
            node = self.expression()
            token = self.current()
            if not token or token.type != "RPAREN":
                raise ValueError("Paréntesis de cierre faltante")
            self.advance()  # Skip ')'
            return node
        elif token.type == "NUMBER":
            value = float(token.value) if "." in token.value else int(token.value)
            self.advance()
            return Number(value)
        elif token.type == "IDENTIFIER":
            name = token.value
            self.advance()
            return Identifier(name)
        else:
            raise ValueError(f"Token inesperado: {token}")

    def current(self) -> Optional[Token]:
        """
        Retorna el token actual en la posición del analizador.

        Returns:
            Token o None: El token actual, o None si se llegó al final.
        """
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        """
        Avanza la posición del analizador al siguiente token.
        """
        self.pos += 1


def parse_expression(expression: str) -> ASTNode:
    """
    Función de conveniencia para analizar una expresión matemática.

    Tokeniza la expresión y construye el AST correspondiente.

    Args:
        expression: La expresión matemática como cadena de texto.

    Returns:
        ASTNode: La raíz del árbol de sintaxis abstracta.

    Raises:
        ValueError: Si hay errores léxicos o sintácticos en la expresión.
    """
    tokens = tokenize(expression)
    parser = Parser(tokens)
    return parser.parse()
