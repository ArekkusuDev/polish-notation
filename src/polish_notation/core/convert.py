from collections.abc import Mapping
from typing import List

from .lexer import tokenize
from .models import ASTNode, BinaryOp, Identifier, Number
from .parser import parse_expression


def _is_operand(token: str) -> bool:
    """
    Verifica si el token es un operando válido (número o identificador).
    """
    # Validar números flotantes
    try:
        float(token)
        return True
    except ValueError:
        pass

    # Validar identificadores (letras y dígitos, comenzando con letra)
    return token.isidentifier()


def infix_to_postfix(tokens: List[str]) -> str:
    """
    Convierte tokens infijos a postfijos usando el algoritmo Shunting Yard.
    Nota: Los paréntesis se procesan pero no se incluyen en la salida.

    Raises:
        ValueError: Si hay paréntesis desbalanceados o tokens inválidos.
    """
    output: List[str] = []
    operators: List[str] = []
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}

    for token in tokens:
        if _is_operand(token):
            output.append(token)
        elif token in precedence:
            # Manejar asociatividad derecha para ^
            while (
                operators
                and operators[-1] != "("
                and precedence.get(operators[-1], 0) >= precedence[token]
                and not (token == "^" and operators[-1] == "^")
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


def convert_to_postfix(expression: str) -> str:
    tokens = tokenize(expression)
    token_values = [t.value for t in tokens]
    return infix_to_postfix(token_values)


def convert_to_prefix(expression: str) -> str:
    ast = parse_expression(expression)
    return ast_to_prefix(ast)


def extract_variables(expression: str) -> list[str]:
    """
    Extrae todas las variables únicas de una expresión infija.

    Las variables se identifican como tokens de tipo IDENTIFIER y se retornan
    en orden lexicográfico para mantener consistencia en la interfaz de usuario.

    Args:
        expression: Expresión matemática en notación infija.

    Returns:
        Lista ordenada de nombres de variables únicas encontradas.

    Examples:
        >>> extract_variables("A + B")
        ['A', 'B']
        >>> extract_variables("A + B * C ^ D - E")
        ['A', 'B', 'C', 'D', 'E']
        >>> extract_variables("2 + 3 * 4")  # Sin variables
        []
    """
    tokens = tokenize(expression)
    # Usar set para eliminar duplicados, luego ordenar alfabéticamente
    variables = {token.value for token in tokens if token.type == "IDENTIFIER"}
    return sorted(variables)


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
    stack: List[float] = []
    tokens = postfix.split()

    for token in tokens:
        if token in variables:
            stack.append(variables[token])
        elif token.replace(".", "", 1).replace("-", "", 1).isdigit():
            # Soporte para números flotantes y negativos
            stack.append(float(token))
        elif token in "+-*/^":
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
        elif token.isidentifier():
            # Es una variable válida pero no está en el diccionario
            raise KeyError(f"Variable '{token}' no definida en el diccionario de valores")
        else:
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
