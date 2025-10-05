# Generador de Notación Prefija y Postfija (a partir de Expresiones Infijas)

Pequeña aplicación TUI construida con [Textual](https://github.com/Textualize/textual) para:
- Ingresar una expresión en notación infija.
- Ver su conversión a notación postfija (Notación Polaca Inversa) y prefija (Notación Polaca).
- Visualizar pasos intermedios.

## Objetivo
Servir como herramienta educativa para cursos de Lenguajes y Autómatas, mostrando el uso de pilas en el proceso de conversión de expresiones.

## Características
- Parser básico con soporte de: + - * / ^ y paréntesis.
- Manejo de espacios opcionales.
- Validación sintáctica mínima (paréntesis balanceados, tokens válidos).
- Conversión:
  - Infix -> Postfix (Shunting Yard)
  - Infix -> Prefix (inversión + árbol de expresión)
- Interfaz TUI con:
  - Campo de entrada
  - Panel de resultados
  - Registro de errores

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

Dentro de la TUI:
- Escribe: (A + B) * C ^ D - E
- Resultado Postfijo: A B + C D ^ * E -
- Resultado Prefijo: - * + A B ^ C D E

## Estructura Propuesta
```
app/
  __init__.py
  main.py          # Punto de entrada
  ui/              # Vistas / widgets
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
- [ ] Diseñar TUI mínima (entrada + salida)
- [ ] Añadir modo "paso a paso" (cola de operadores / pila)
- [x] Pruebas unitarias de casos simples
- [x] Soporte de números multi-dígito
- [ ] Soporte de funciones (sin, log, etc.) (futuro)
- [ ] Documentar ejemplos avanzados
