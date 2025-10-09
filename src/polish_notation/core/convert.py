import re
from collections.abc import Mapping
from functools import lru_cache
from typing import List, Tuple

from .lexer import tokenize
from .models import ASTNode, BinaryOp, Identifier, Number
from .parser import parse_expression

type Quadruples = List[Tuple[str, str, str, str]]
type Triples = List[Tuple[str, str, str]]

_PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
_RIGHT_ASSOCIATIVE = {"^"}
_NUMBER_PATTERN = re.compile(r"^-?\d+(\.\d+)?$")


def _is_operand(token: str) -> bool:
    """
    Verifica si el token es un operando válido (número o identificador).
    """
    return bool(_NUMBER_PATTERN.match(token)) or token.isidentifier()


def infix_to_postfix(tokens: List[str]) -> str:
    """
    Convierte tokens infijos a postfijos usando el algoritmo Shunting Yard.
    Nota: Los paréntesis se procesan pero no se incluyen en la salida.

    Raises:
        ValueError: Si hay paréntesis desbalanceados o tokens inválidos.
    """
    output: List[str] = []
    operators: List[str] = []

    for token in tokens:
        if _is_operand(token):
            output.append(token)
        elif token in _PRECEDENCE:
            # Manejar asociatividad derecha para ^
            while (
                operators
                and operators[-1] != "("
                and _PRECEDENCE.get(operators[-1], 0) >= _PRECEDENCE[token]
                and token not in _RIGHT_ASSOCIATIVE
            ):  # ^ es asociativo derecho
                output.append(operators.pop())
            operators.append(token)
        elif token == "(":
            operators.append(token)
        elif token == ")":
            # Validar que hay operadores antes de acceder
            if not operators:
                raise ValueError("Paréntesis de cierre sin apertura correspondiente")
            while operators and operators[-1] != "(":
                output.append(operators.pop())
            if not operators or operators[-1] != "(":
                raise ValueError("Paréntesis de cierre sin apertura correspondiente")
            operators.pop()
        else:
            raise ValueError(f"Token inválido: {token}")

    if "(" in operators:
        raise ValueError("Paréntesis de apertura sin cierre correspondiente")

    while operators:
        output.append(operators.pop())

    return " ".join(output)


def ast_to_prefix(node: ASTNode) -> str:
    """
    Convierte un AST a notación prefija.
    """
    parts: List[str] = []

    def _traverse(n: ASTNode) -> None:
        if isinstance(n, Number):
            parts.append(str(n.value))
        elif isinstance(n, Identifier):
            parts.append(n.name)
        elif isinstance(n, BinaryOp):
            parts.append(n.op)
            _traverse(n.left)
            _traverse(n.right)
        else:
            raise ValueError(f"Tipo de nodo desconocido: {type(n)}")

    _traverse(node)
    return " ".join(parts)


def ast_to_quadruples(node: ASTNode) -> Quadruples:
    """Generates quadruples from an AST."""
    quads: Quadruples = []
    temp_counter = 0

    def new_temp():
        nonlocal temp_counter
        temp_counter += 1
        return f"T{temp_counter}"

    def traverse(n: ASTNode) -> str:
        if isinstance(n, Number):
            return str(n.value)
        if isinstance(n, Identifier):
            return n.name
        if isinstance(n, BinaryOp):
            left = traverse(n.left)
            right = traverse(n.right)
            result = new_temp()
            quads.append((n.op, left, right, result))
            return result
        raise TypeError(f"Unknown node type: {type(n)}")

    traverse(node)
    return quads


def ast_to_triples(node: ASTNode) -> Triples:
    """Generates triples from an AST."""
    triples: Triples = []

    def traverse(n: ASTNode) -> str:
        if isinstance(n, Number):
            return str(n.value)
        if isinstance(n, Identifier):
            return n.name
        if isinstance(n, BinaryOp):
            left = traverse(n.left)
            right = traverse(n.right)
            # The "result" of a triple is its index in the list
            result_index = len(triples) + 1
            triples.append((n.op, left, right))
            return f"({result_index})"  # Pointer to the result
        raise TypeError(f"Unknown node type: {type(n)}")

    traverse(node)
    return triples


def convert_to_postfix(expression: str) -> str:
    tokens = tokenize(expression)
    token_values = [t.value for t in tokens]
    return infix_to_postfix(token_values)


def convert_to_prefix(expression: str) -> str:
    ast = parse_expression(expression)
    return ast_to_prefix(ast)


@lru_cache(maxsize=128)
def extract_variables(expression: str) -> Tuple[str, ...]:
    """
    Extrae todas las variables únicas de una expresión infija.

    Las variables se identifican como tokens de tipo IDENTIFIER y se retornan
    en orden para mantener consistencia en la interfaz de usuario.

    Args:
        expression: Expresión matemática en notación infija.

    Returns:
        Lista ordenada de nombres de variables únicas encontradas.

    Examples:
        >>> extract_variables("A + B")
        ('A', 'B')
        >>> extract_variables("A + B * C ^ D - E")
        ('A', 'B', 'C', 'D', 'E')
        >>> extract_variables("2 + 3 * 4")  # Sin variables
        ()
    """
    tokens = tokenize(expression)
    # Usar set para eliminar duplicados, luego ordenar alfabéticamente
    variables = {token.value for token in tokens if token.type == "IDENTIFIER"}
    return tuple(sorted(variables))


def evaluate_postfix(postfix: str, variables: Mapping[str, float | int]) -> float:
    """
    Evalúa una expresión en notación postfija usando evaluación basada en pila.
    La expresión puede o no contener variables, o una combinación de variables y números fijos.

    Args:
        postfix: Expresión en notación postfija como cadena (ej. "A B +").
        variables: Diccionario con valores para variables (ej. {"A": 1.0, "B": 2.0}).

    Returns:
        Resultado numérico de la evaluación.

    Raises:
        ValueError: Si hay tokens inválidos, operadores insuficientes o división por cero.
        KeyError: Si una variable usada en la expresión no está en el diccionario.

    Examples:
        >>> evaluate_postfix("A B +", {"A": 1, "B": 2})
        3.0
        >>> evaluate_postfix("A B C * +", {"A": 1, "B": 2, "C": 3})
        7.0
    """
    OPERATORS = {"+", "-", "*", "/", "^"}
    stack: List[float] = []
    tokens = postfix.split()

    for token in tokens:
        if token in OPERATORS:
            if len(stack) < 2:
                raise ValueError(f"Operador '{token}' requiere al menos dos operandos")
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                if b == 0:
                    raise ValueError("División por cero")
                stack.append(a / b)
            elif token == "^":
                stack.append(a**b)
        elif token in variables:
            stack.append(float(variables[token]))
        else:
            try:
                stack.append(float(token))
            except ValueError:
                if token.isidentifier():
                    raise KeyError(f"Variable '{token}' no definida")
                raise ValueError(f"Token inválido: '{token}'")

    if len(stack) != 1:
        raise ValueError("Expresión postfija malformada: operandos restantes en la pila")

    return stack[0]


def evaluate_expression(expression: str, variable_values: Mapping[str, float | int]) -> float:
    """
    Evalúa una expresión infija sustituyendo variables por valores dados.

    Convierte primero la expresión a notación postfija y luego la evalúa,
    demostrando el flujo completo: infix → postfix → resultado.

    Args:
        expression: Expresión matemática en notación infija (ej. "A + B * C").
        variable_values: Diccionario con valores para cada variable.

    Returns:
        Resultado numérico de la evaluación.

    Raises:
        ValueError: Si hay errores sintácticos o semánticos en la expresión.
        KeyError: Si falta alguna variable requerida en variable_values.

    Examples:
        >>> evaluate_expression("A + B", {"A": 1, "B": 2})
        3.0
        >>> evaluate_expression("(A + B) * C", {"A": 1, "B": 2, "C": 3})
        9.0
    """
    # Validar que todas las variables necesarias tienen valores
    required_vars = extract_variables(expression)
    missing_vars = [var for var in required_vars if var not in variable_values]
    if missing_vars:
        raise KeyError(f"Faltan valores para las variables: {', '.join(missing_vars)}")

    postfix = convert_to_postfix(expression)
    return evaluate_postfix(postfix, variable_values)
