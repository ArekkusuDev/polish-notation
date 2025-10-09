import pytest

from polish_notation.core.models import Assignment, BinaryOp, Identifier, Number
from polish_notation.core.parser import parse_expression


class TestParseExpression:
    def test_parse_single_number(self):
        ast = parse_expression("42")
        assert isinstance(ast, Number)
        assert ast.value == 42

    def test_parse_single_identifier(self):
        ast = parse_expression("A")
        assert isinstance(ast, Identifier)
        assert ast.name == "A"

    def test_parse_expression(self):
        ast = parse_expression("A * B + 999")
        assert isinstance(ast, BinaryOp)
        assert ast.op == "+"
        assert isinstance(ast.right, Number) and ast.right.value == 999
        assert isinstance(ast.left, BinaryOp)
        assert ast.left.op == "*"
        assert isinstance(ast.left.left, Identifier) and ast.left.left.name == "A"
        assert isinstance(ast.left.right, Identifier) and ast.left.right.name == "B"

    def test_parse_empty_expression(self):
        with pytest.raises(ValueError, match="vacía"):
            parse_expression("")

    def test_parse_assignment(self):
        """Prueba análisis de asignación simple."""
        ast = parse_expression("A = B + C")
        assert isinstance(ast, Assignment)
        assert isinstance(ast.target, Identifier)
        assert ast.target.name == "A"
        assert isinstance(ast.value, BinaryOp)
        assert ast.value.op == "+"
        assert isinstance(ast.value.left, Identifier) and ast.value.left.name == "B"
        assert isinstance(ast.value.right, Identifier) and ast.value.right.name == "C"

    def test_parse_chained_assignment(self):
        """Prueba análisis de asignaciones encadenadas (asociatividad derecha)."""
        ast = parse_expression("A = B = C")
        assert isinstance(ast, Assignment)
        assert ast.target.name == "A"
        assert isinstance(ast.value, Assignment)
        assert ast.value.target.name == "B"
        assert isinstance(ast.value.value, Identifier)
        assert ast.value.value.name == "C"

    def test_parse_assignment_with_expression(self):
        """Prueba asignación con expresión compleja."""
        ast = parse_expression("X = A * B + C")
        assert isinstance(ast, Assignment)
        assert ast.target.name == "X"
        assert isinstance(ast.value, BinaryOp)
        assert ast.value.op == "+"

    def test_invalid_assignment_target(self):
        """Prueba que falle cuando el lado izquierdo no es un identificador."""
        with pytest.raises(ValueError, match="identificador"):
            parse_expression("(A + B) = C")

        with pytest.raises(ValueError, match="identificador"):
            parse_expression("5 = A")
