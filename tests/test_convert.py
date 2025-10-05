import pytest

from polish_notation.core.convert import (
    convert_to_postfix,
    convert_to_prefix,
    evaluate_expression,
    evaluate_postfix,
    extract_variables,
)


class TestPostfixConversion:
    def test_basic_addition(self):
        assert convert_to_postfix("A + B") == "A B +"

    def test_precedence(self):
        assert convert_to_postfix("A + B * C") == "A B C * +"

    def test_parentheses(self):
        assert convert_to_postfix("(A + B) * C ^ D - E") == "A B + C D ^ * E -"

    def test_right_associativity_power(self):
        assert convert_to_postfix("A ^ B ^ C") == "A B C ^ ^"

    def test_complex_expression(self):
        expr = "A + B * (C ^ D - E) ^ (F + G * H) - I"
        expected = "A B C D ^ E - F G H * + ^ * + I -"
        assert convert_to_postfix(expr) == expected

    def test_unmatched_parentheses(self):
        with pytest.raises(ValueError, match="Paréntesis"):
            convert_to_postfix("((A + B) * C")

    def test_invalid_token(self):
        with pytest.raises(ValueError, match="no reconocido"):
            convert_to_postfix("A + B & C")


class TestPreefixConversion:
    def test_basic_addition(self):
        assert convert_to_prefix("A + B") == "+ A B"

    def test_power(self):
        assert convert_to_prefix("A ^ B ^ C") == "^ A ^ B C"

    def test_precedence(self):
        assert convert_to_prefix("A + B * C") == "+ A * B C"

    def test_parentheses(self):
        assert convert_to_prefix("(A + B) * C") == "* + A B C"

    def test_complex_expression(self):
        expr = "A + B * (C ^ D - E) ^ (F + G * H) - I"
        expected = "- + A * B ^ - ^ C D E + F * G H I"
        assert convert_to_prefix(expr) == expected


class TestVariableExtraction:
    def test_extract_single_variable(self):
        assert extract_variables("A + 1") == ("A",)

    def test_extract_many_variables(self):
        assert extract_variables("(A + B) * C ^ D - E") == ("A", "B", "C", "D", "E")

    def test_extract_duplicates(self):
        """Las variables duplicadas deben aparecer una sola vez."""
        assert extract_variables("A + A * B") == ("A", "B")

    def test_extract_no_variables(self):
        """Expresiones con solo números no tienen variables."""
        assert extract_variables("1 + 2 * 3") == ()

    def test_alphabetical_order(self):
        """Las variables deben retornarse en orden alfabético."""
        assert extract_variables("Z + A + M") == ("A", "M", "Z")


class TestPostfixEvaluation:
    def test_basic_evaluation(self):
        assert evaluate_postfix("A B +", {"A": 1, "B": 2}) == 3.0

    def test_precedence_evaluation(self):
        assert evaluate_postfix("A B C * +", {"A": 1, "B": 2, "C": 3}) == 7.0

    def test_power_evaluation(self):
        assert evaluate_postfix("A B ^", {"A": 2, "B": 3}) == 8.0

    def test_division(self):
        assert evaluate_postfix("A B /", {"A": 10, "B": 2}) == 5.0

    def test_subtraction(self):
        assert evaluate_postfix("A B -", {"A": 10, "B": 3}) == 7.0

    def test_complex_evaluation(self):
        # (A + B) * C ^ D - E con A=1, B=2, C=2, D=3, E=5
        # Postfix: A B + C D ^ * E -
        # = (1 + 2) * (2 ^ 3) - 5 = 3 * 8 - 5 = 19
        postfix = "A B + C D ^ * E -"
        variables = {"A": 1, "B": 2, "C": 2, "D": 3, "E": 5}
        assert evaluate_postfix(postfix, variables) == 19.0

    def test_numbers_only(self):
        """Evaluar expresión con solo números (sin variables)."""
        assert evaluate_postfix("2 3 +", {}) == 5.0

    def test_mixed_numbers_and_variables(self):
        """Mezcla de números literales y variables."""
        assert evaluate_postfix("A 2 * 3 +", {"A": 5}) == 13.0

    def test_division_by_zero(self):
        with pytest.raises(ValueError, match="División por cero"):
            evaluate_postfix("A B /", {"A": 1, "B": 0})

    def test_missing_variable(self):
        with pytest.raises(KeyError):
            evaluate_postfix("A B +", {"A": 1})  # B no definido

    def test_insufficient_operands(self):
        with pytest.raises(ValueError, match="requiere al menos dos operandos"):
            evaluate_postfix("A +", {"A": 1})

    def test_malformed_expression(self):
        with pytest.raises(ValueError, match="malformada"):
            evaluate_postfix("A B", {"A": 1, "B": 2})  # Falta operador

    def test_invalid_token(self):
        with pytest.raises(ValueError, match="Token inválido"):
            evaluate_postfix("A B @", {"A": 1, "B": 2})


class TestExpressionEvaluation:
    def test_evaluate_simple(self):
        assert evaluate_expression("A + B", {"A": 1, "B": 2}) == 3.0

    def test_evaluate_with_precedence(self):
        # A + B * C con A=1, B=2, C=3 = 1 + 6 = 7
        assert evaluate_expression("A + B * C", {"A": 1, "B": 2, "C": 3}) == 7.0

    def test_evaluate_with_parentheses(self):
        # (A + B) * C con A=1, B=2, C=3 = 9
        assert evaluate_expression("(A + B) * C", {"A": 1, "B": 2, "C": 3}) == 9.0

    def test_evaluate_power(self):
        # A ^ B con A=2, B=3 = 8
        assert evaluate_expression("A ^ B", {"A": 2, "B": 3}) == 8.0

    def test_evaluate_complex(self):
        # (A + B) * C ^ D - E con A=1, B=2, C=2, D=3, E=5
        # = (1 + 2) * (2 ^ 3) - 5 = 3 * 8 - 5 = 19
        expr = "(A + B) * C ^ D - E"
        variables = {"A": 1, "B": 2, "C": 2, "D": 3, "E": 5}
        assert evaluate_expression(expr, variables) == 19.0

    def test_missing_variable_value(self):
        with pytest.raises(KeyError, match="Faltan valores"):
            evaluate_expression("A + B + C", {"A": 1, "B": 2})  # Falta C

    def test_evaluate_only_numbers(self):
        # Expresión sin variables
        assert evaluate_expression("2 + 3 * 4", {}) == 14.0

    def test_evaluate_with_division(self):
        assert evaluate_expression("A / B + C", {"A": 10, "B": 2, "C": 3}) == 8.0

    def test_all_variables_required(self):
        """Verificar que extract_variables encuentra todas las variables necesarias."""
        expr = "A + B + C + D"
        with pytest.raises(KeyError, match="Faltan valores.*C.*D"):
            evaluate_expression(expr, {"A": 1, "B": 2})  # Faltan C y D
