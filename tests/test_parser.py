import pytest

from polish_notation.core.models import BinaryOp, Identifier, Number
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
