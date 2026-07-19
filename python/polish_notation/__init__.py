from typing import cast

import questionary
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .core.convert import (
    Quadruples,
    Triples,
    ast_to_postfix_from_ast,
    ast_to_prefix,
    ast_to_quadruples,
    ast_to_triples,
    convert_to_postfix,
    evaluate_postfix,
    extract_variables,
)
from .core.models import Assignment
from .core.parser import parse_expression

type PostfixValues = dict[str, int | float]
console = Console()


def construct_table(title: str) -> Table:
    return Table(
        title=f"\n[bold cyan]{title}[/bold cyan]",
        show_header=True,
        show_lines=True,
        header_style="bold magenta",
    )


def _build_triples_table(t: Triples) -> Table:
    """Muestra una tabla con la representación de triplos."""
    table = construct_table("Triplos")
    table.add_column("Ref", style="yellow", justify="center")
    table.add_column("Operador", style="red", justify="center")
    table.add_column("Arg 1", style="green", justify="center")
    table.add_column("Arg 2", style="green", justify="center")

    for i, (op, arg1, arg2) in enumerate(t, start=1):
        table.add_row(str(f"({i})"), op, arg1, arg2)
    return table


def _build_quadruples_table(q: Quadruples) -> Table:
    """Muestra una tabla con la representación de cuádruplos."""
    table = construct_table("Cuádruplos")
    table.add_column("Operador", style="red", justify="center")
    table.add_column("Arg 1", style="green", justify="center")
    table.add_column("Arg 2", style="green", justify="center")
    table.add_column("Resultado", style="yellow", justify="center")

    for op, arg1, arg2, result in q:
        table.add_row(op, arg1, arg2, result)
    return table


def _eval(p: str, toeval: str, v: PostfixValues | None = None, target: str | None = None) -> None:
    if v is None:
        v = {}
    result = evaluate_postfix(toeval, v)
    # replace postfix values in the output without mutating the original string
    postfix = p if not target else toeval

    for var, val in v.items():
        postfix = postfix.replace(var, str(val))

    console.print(f"\n[bold yellow]Evaluando NPI:[/bold yellow] [bold white]{p}[/bold white]", justify="center")
    if target:
        console.print(f"[bold green]{target} = [{postfix}] = {result}[/bold green]\n", justify="center")
    else:
        console.print(f"[bold green][{postfix}] = {result}[/bold green]\n", justify="center")


def _help() -> None:
    console.print(
        """
[bold cyan]Comandos disponibles:[/bold cyan]
- Ingresa una expresión matemática en infija para convertirla y evaluarla.
- Usa [bold]/q[/bold] para salir.
- Usa [bold]/c[/bold] para limpiar la consola.
- Puedes usar variables (letras) en la expresión y se te pedirá su valor.
- Soporta operadores: [bold magenta]+, -, *, /, ^[/bold magenta] y paréntesis.
        """,
        justify="center",
    )


def _process_expression(expr: str, values: PostfixValues) -> None:
    """Procesa una expresión: convierte, genera triplos/cuádruplos y evalúa."""
    ast = parse_expression(expr)
    isAssignment = isinstance(ast, Assignment)

    prefix = ast_to_prefix(ast)
    # remove parentheses from expr to get infix, keeping single spaces between tokens
    infix = " ".join([c for c in expr.strip().replace("(", "").replace(")", "").replace(" ", "")])
    postfix = convert_to_postfix(expr)
    triples = ast_to_triples(parse_expression(expr))
    quadruples = ast_to_quadruples(parse_expression(expr))

    triples_table = _build_triples_table(triples)
    quadruples_table = _build_quadruples_table(quadruples)
    tables = Align.center(Columns([triples_table, quadruples_table]))
    console.print(
        Panel.fit(
            tables,
            title="Representaciones Intermedias",
            title_align="center",
        ),
        justify="center",
    )
    console.print(f"[bold cyan]Notación Prefija:[/bold cyan] [bold white]{prefix}[/bold white]", justify="center")
    console.print(f"[bold magenta]Notación Infija:[/bold magenta] [bold white]{infix}[/bold white]", justify="center")
    console.print(f"[bold cyan]Notación Postfija:[/bold cyan] [bold white]{postfix}[/bold white]", justify="center")
    _eval(
        postfix,
        ast_to_postfix_from_ast(ast.value) if isAssignment else postfix,
        values,
        None if not isAssignment else ast.target.name,
    )


def _display_variables(variables: tuple[str, ...]) -> None:
    """Muestra las variables encontradas en la expresión."""
    console.print(
        f"[bold yellow][+] Variables encontradas[/bold yellow]: [bold]{', '.join(variables)}[/bold]"
        if variables
        else "[bold yellow][!] No se encontraron variables.[/bold yellow]\n",
    )


def _collect_variable_values(variables: tuple[str, ...]) -> PostfixValues | None:
    """Solicita al usuario los valores de las variables. Retorna None si se cancela."""
    console.print("\n[bold cyan]Ingresa los valores para las variables:[/bold cyan]")
    values: PostfixValues = {}

    for var in list(variables):
        while True:
            val_str = cast(str | None, questionary.text(f"  - Valor para {var}:").ask())
            if val_str is None or val_str == "":
                return None
            try:
                values[var] = float(val_str) if "." in val_str else int(val_str)
                break
            except ValueError:
                console.print(f"[red]Valor inválido para {var}. Por favor, ingresa un número.[/red]")

    console.print()
    return values


def main() -> None:
    """Punto de entrada para la aplicación de notación polaca."""

    while True:
        expr = cast(
            str | None,
            questionary.text(
                "Ingresa una expresión infija ('/q' para salir):",
                placeholder="A + B * (C - D)",
                style=questionary.Style(
                    [("qmark", "fg:#89dceb bold"), ("answer", "fg:#cba6f7 bold")],
                ),
            ).ask(),
        )

        if expr is None or expr == "" or expr.strip().lower() == "/q":
            break
        elif expr.strip().lower() == "/c":
            console.clear()
            continue
        elif expr.strip().lower() == "/h":
            _help()
            continue

        expr = str(expr).strip()
        if not expr:
            console.print("[bold red]Por favor, ingresa una expresión válida.[/bold red]\n")
            continue

        try:
            variables = extract_variables(expr)
            _display_variables(variables)

            if variables:
                values = _collect_variable_values(variables)
                if values is None:
                    continue
                _process_expression(expr, values)
            else:
                _process_expression(expr, {})

        except Exception as e:
            console.print(f"[bold red]Error: {e}[/bold red]\n")
