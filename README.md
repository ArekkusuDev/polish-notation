# Generador de Notación Prefija y Postfija (a partir de Expresiones Infijas)

Simple CLI construida con [questionary](https://github.com/tmbo/questionary) para:
- Ingresar una expresión en notación infija.
- Ver su conversión a notación postfija (Notación Polaca Inversa) y prefija (Notación Polaca).
- Evaluar la expresión postfija con o sin valores para variables.

## Objetivo
Servir como herramienta educativa para cursos de Lenguajes y Autómatas, mostrando el uso de pilas en el proceso de conversión de expresiones.

## Características
- Parser básico con soporte de: + - * / ^ y paréntesis.
- Manejo de espacios opcionales.
- Validación sintáctica mínima (paréntesis balanceados, tokens válidos).
- Conversión:
  - Infix -> Postfix (Shunting Yard)
  - Infix -> Prefix (inversión + árbol de expresión)
- Evaluación de expresiones postfijas con sustitución de variables.
- CLI interactiva con:
  - Entrada de expresión
  - Resultados claros

## Requisitos
- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Instalación
Con uv:
```bash
git clone git@github.com:ArekkusuDev/polish-notation.git
cd polish-notation
uv sync
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

En la CLI
- Escribe: (A + B) * C ^ D - E
- Resultado Postfijo: A B + C D ^ * E -
- Resultado Prefijo: - * + A B ^ C D E

## Estructura Propuesta
```
app/
  __init__.py      # Punto de entrada
  core/
    lexer.py       # Tokenización
    parser.py      # Validación / árbol
    convert.py     # Funciones infix->postfix / infix->prefix
    models.py      # Clases de nodo (AST)
tests/
  test_convert.py
  test_lexer.py
```

## Roadmap
- [x] Configurar entorno
- [x] Implementar lexer básico
- [x] Implementar verificación de paréntesis
- [x] Implementar conversión a postfija (Shunting Yard)
- [x] Implementar conversión a prefija (AST o método invertido)
- [x] Añadir manejo de errores con mensajes claros
- [x] Implementar evaluación de expresiones postfijas con sustitución de variables
- [x] Implementar CLI interactiva con questionary
- [ ] Añadir modo "paso a paso" (cola de operadores / pila)
- [x] Pruebas unitarias de casos simples
- [x] Soporte de números multi-dígito
