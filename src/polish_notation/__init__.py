from typing import Dict, Union

import questionary
from rich.console import Console
from rich.table import Table

from .core.convert import convert_to_postfix, convert_to_prefix, evaluate_postfix, extract_variables

type PostfixValues = Dict[str, Union[int, float]]
console = Console()


def _draw_table(expr: str, postfix: str, prefix: str) -> None:
    """Dibuja una tabla con las conversiones de notación."""

    # infix is the same without parentheses
    infix = expr.replace("(", "").replace(")", "")

    table = Table(
        title="\n[bold cyan]Conversión de Notación[/bold cyan]",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Infija", style="magenta", justify="center")
    table.add_column("Prefija (NP)", style="blue", justify="center")
    table.add_column("Postfija (NPI)", style="green", justify="center")
    table.add_row(infix, prefix, postfix)
    console.print(table, justify="center")


def _eval(p: str, v: PostfixValues = {}) -> None:
    result = evaluate_postfix(p, v)
    console.print(f"\n[bold green]Resultado: {result}[/bold green]\n", justify="center")


def main() -> None:
    """Punto de entrada para la aplicación de notación polaca."""

    while True:
        expr = questionary.text("Ingresa una expresión infija ('q' para salir):").ask()
        if expr is None or expr.lower() == "q":
            break

        # Normalize input
        expr = str(expr).strip().upper()
        if not expr:
            console.print("[bold red]Por favor, ingresa una expresión válida.[/bold red]\n")
            continue

        try:
            # Convert and evaluate
            prefix = convert_to_prefix(expr)
            postfix = convert_to_postfix(expr)

            # get variable values from the user
            variables = extract_variables(expr)
            console.print(
                f"[bold yellow][+] Variables encontradas[/bold yellow]: [bold]{', '.join(variables)}[/bold]"
                if variables
                else "[bold yellow][!] No se encontraron variables.[/bold yellow]",
            )
            if variables:
                console.print("\n[bold cyan]Ingresa los valores para las variables:[/bold cyan]")
                values: PostfixValues = {}
                cancelled = False

                for var in sorted(list(variables)):
                    while True:
                        val_str = questionary.text(f"  - Valor para {var}:").ask()
                        if val_str is None:
                            cancelled = True
                            break
                        try:
                            values[var] = float(val_str) if "." in val_str else int(val_str)
                            break
                        except ValueError:
                            console.print(f"[red]Valor inválido para {var}. Por favor, ingresa un número.[/red]")
                    if cancelled:
                        break

                if not cancelled:
                    _draw_table(expr, postfix, prefix)
                    _eval(postfix, values)
            else:
                _draw_table(expr, postfix, prefix)
                _eval(postfix)

        except Exception as e:
            console.print(f"[bold red]Error: {e}[/bold red]\n")
