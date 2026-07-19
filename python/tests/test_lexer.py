import pytest

from polish_notation.core.lexer import Token, tokenize


class TestTokenize:
    def test_tokenize_basic_addition(self):
        """Prueba tokenización básica de suma."""
        tokens = tokenize("A + B")
        print(tokens)
        expected = [
            Token("IDENTIFIER", "A"),
            Token("OPERATOR", "+"),
            Token("IDENTIFIER", "B"),
        ]
        print(expected)
        assert tokens == expected

    def test_tokenize_with_spaces(self):
        """Prueba tokenización ignorando espacios."""
        tokens = tokenize(" A + B ")
        expected = [
            Token("IDENTIFIER", "A"),
            Token("OPERATOR", "+"),
            Token("IDENTIFIER", "B"),
        ]
        assert tokens == expected

    def test_tokenize_numbers(self):
        """Prueba tokenización con números enteros y flotantes."""
        tokens = tokenize("1 + 2.5")
        expected = [
            Token("NUMBER", "1"),
            Token("OPERATOR", "+"),
            Token("NUMBER", "2.5"),
        ]
        assert tokens == expected

    def test_tokenize_parentheses(self):
        """Prueba tokenización con paréntesis."""
        tokens = tokenize("(A + B)")
        expected = [
            Token("LPAREN", "("),
            Token("IDENTIFIER", "A"),
            Token("OPERATOR", "+"),
            Token("IDENTIFIER", "B"),
            Token("RPAREN", ")"),
        ]
        assert tokens == expected

    def test_tokenize_power(self):
        """Prueba tokenización con operador de potencia."""
        tokens = tokenize("A ^ B")
        expected = [
            Token("IDENTIFIER", "A"),
            Token("OPERATOR", "^"),
            Token("IDENTIFIER", "B"),
        ]
        assert tokens == expected

    def test_tokenize_complex_expression(self):
        """Prueba tokenización de expresión compleja."""
        tokens = tokenize("(A + B) * C ^ D - E")
        expected = [
            Token("LPAREN", "("),
            Token("IDENTIFIER", "A"),
            Token("OPERATOR", "+"),
            Token("IDENTIFIER", "B"),
            Token("RPAREN", ")"),
            Token("OPERATOR", "*"),
            Token("IDENTIFIER", "C"),
            Token("OPERATOR", "^"),
            Token("IDENTIFIER", "D"),
            Token("OPERATOR", "-"),
            Token("IDENTIFIER", "E"),
        ]
        assert tokens == expected

    def test_empty_expression(self):
        """Prueba que lance error para expresión vacía."""
        with pytest.raises(ValueError, match="vacía"):
            tokenize("")

    def test_invalid_character(self):
        """Prueba que lance error para caracter no reconocido."""
        with pytest.raises(ValueError, match="no reconocido"):
            tokenize("A + B @")

    def test_invalid_character_at_start(self):
        """Prueba que lance error para caracter no reconocido al inicio."""
        with pytest.raises(ValueError, match="no reconocido"):
            tokenize("@A + B")

    def test_invalid_character_at_end(self):
        """Prueba que lance error para caracter no reconocido al final."""
        with pytest.raises(ValueError, match="no reconocido"):
            tokenize("A + B@")

    def test_tokenize_assignment(self):
        """Prueba tokenización con operador de asignación."""
        tokens = tokenize("A = B + C")
        expected = [
            Token("IDENTIFIER", "A"),
            Token("ASSIGN", "="),
            Token("IDENTIFIER", "B"),
            Token("OPERATOR", "+"),
            Token("IDENTIFIER", "C"),
        ]
        assert tokens == expected

    def test_tokenize_multiple_assignment(self):
        """Prueba tokenización con asignaciones múltiples."""
        tokens = tokenize("A = B = C")
        expected = [
            Token("IDENTIFIER", "A"),
            Token("ASSIGN", "="),
            Token("IDENTIFIER", "B"),
            Token("ASSIGN", "="),
            Token("IDENTIFIER", "C"),
        ]
        assert tokens == expected
