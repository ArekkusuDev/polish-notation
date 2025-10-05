# Lenguajes y Autómatas 2 (7A - 2025B) - Actividad 4

## Project Overview
Educational TUI application for converting infix mathematical expressions to postfix (Reverse Polish Notation) and prefix (Polish Notation). Built with Textual framework to demonstrate stack-based algorithms for Languages and Automata courses.

## Architecture
Follow the proposed structure from README.md:
```
src/polish_notation/
├── main.py              # Entry point
├── ui/                  # Textual widgets and views
└── core/                # Algorithm implementations
    ├── lexer.py         # Tokenization
    ├── parser.py        # Syntax validation and AST
    ├── convert.py       # Shunting Yard + prefix conversion
    └── models.py        # AST node classes
```

## Development Workflow
- **Environment**: `uv sync` to install dependencies, `source .venv/bin/activate` to activate
- **Code Quality**: Pre-commit hooks run `ruff --fix` and `ruff-format` automatically
- **Commits**: Use `cz commit` for conventional commit messages
- **Testing**: `pytest` (no tests implemented yet)
- **Linting**: `ruff check` and `ruff format` (120 char line length)

## Key Patterns
- **Spanish Naming**: Use Spanish for comments, docstrings, and educational content
- **Textual TUI**: Follow Textual patterns for reactive UI components
- **Educational Focus**: Include step-by-step algorithm visualization
- **Error Handling**: Clear error messages for invalid expressions

## Implementation Notes
- Support operators: `+ - * / ^` with parentheses
- Handle optional spaces in input
- Validate balanced parentheses and valid tokens
- Show intermediate steps (operator queue/stack states)
- Two conversion methods: Shunting Yard for postfix, AST inversion for prefix
- Parentheses are not included in postfix and prefix output as operator precedence is implicit
- **Evaluation**: Compute results using postfix expression (stack-based evaluation) with variable substitution

## Examples
```
Infix: (A + B) * C ^ D - E
Postfix: A B + C D ^ * E -
Prefix: - * + A B ^ C D E
```

## Dependencies
- Textual (for TUI) - not yet added to pyproject.toml
- Core logic should be framework-agnostic for testing
