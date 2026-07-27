# Polish Notation Converter (Infix -> Prefix/Postfix)

A CLI tool that parses infix expressions, converts them to postfix (Reverse
Polish Notation) and prefix (Polish Notation), and evaluates postfix expressions
with optional variable substitution.

## :construction: Project Status

This repository started as a college assignment (Python-only) and is currently
undergoing a Rust FFI migration (maturin + PyO3) and some parts are still in
progress.

----------

## Features

- Expression parsing with support for `+`, `-`, `*`, `/`, `^`, assignment and
  parentheses
- Basic syntax validation (balanced parentheses, valid tokens)
- Evaluation from postfix notation with variable substitution

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Installation

```bash
git clone git@github.com:AleHanndro/polish-notation.git
cd polish-notation
uv sync
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

## Example

Input:

```text
(A + B) * C ^ D - E
```

Output:

- Postfix: A B + C D ^ * E -
- Prefix: - * + A B ^ C D E
