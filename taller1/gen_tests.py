"""Genera y ejecuta casos de prueba borde para el lexer."""
import subprocess
import sys

def run(src: str, label: str) -> None:
    result = subprocess.run(
        [sys.executable, 'lexer.py'],
        input=src.encode('utf-8'),
        capture_output=True
    )
    out = result.stdout.decode('utf-8').strip()
    print(f'=== {label} ===')
    print(f'INPUT:  {repr(src)}')
    print(f'OUTPUT:\n{out}')
    print()

# ── Strings con escapes ────────────────────────────────────────────────────────
run('var s = "hola\\nmundo"',          'String con \\n literal')
run("var s = 'tab\\there'",            'String con \\t literal')
run('var s = "quote\\"end"',           'String con \\" literal')
run("var s = 'quote\\'end'",           "String con \\' literal")

# ── Números borde ──────────────────────────────────────────────────────────────
run('0',                                'Número cero')
run('0.0',                              'Número 0.0')
run('0.5',                              'Número 0.5')
run('999999',                           'Número grande')
run('.5',                               '. seguido de 5 (period + num)')
run('5.',                               'Número 5 seguido de punto')
run('1.2.3',                            'Doble punto: 1.2 + . + 3')

# ── Palabras reservadas que son prefijo de otras ───────────────────────────────
run('si sino sinoa',                    'si / sino / sinoa')
run('para paraCada',                    'para / paraCada')
run('hacer hacerAlgo',                  'hacer / hacerAlgo')
run('en entradas',                      'en / entradas')
run('de desde',                         'de / desde')

# ── Operadores ambiguos ────────────────────────────────────────────────────────
run('a===b',                            '=== sin espacios')
run('a!==b',                            '!== sin espacios')
run('a**=b',                            '**= sin espacios')
run('a...b',                            '... sin espacios')
run('a??b',                             '?? sin espacios')

# ── Error: solo abortamos en el primero ───────────────────────────────────────
run('a @ b # c',                        'Dos errores: solo reporta el primero (@)')

# ── Bloque vacío ──────────────────────────────────────────────────────────────
run('{}',                               'Bloque vacío {}')
run('[]',                               'Arreglo vacío []')
run('()',                               'Paréntesis vacíos ()')

# ── Regex vs división ─────────────────────────────────────────────────────────
run('a / b / c',                        'División dos veces')
run('x = /abc/',                        'Regex después de =')
run('si (/abc/) {}',                    'Regex dentro de si()')

# ── Identificadores Unicode ───────────────────────────────────────────────────
run('müVariable',                       'Identificador con ü')
run('$crédito',                         'Identificador con $')
