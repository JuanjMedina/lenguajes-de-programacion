# Lenguajes de Programación — Guía para Claude

## Contexto del curso
- **Materia:** Lenguajes de Programación — Semestre 2026-1
- **Lenguaje objetivo:** EsJS (JavaScript con sintaxis en español)
- **Referencia oficial:** https://es.js.org

---

## Estructura del repositorio

```
lenguajes-de-programacion/
└── taller1/
    ├── alcance.md                  # Palabras reservadas y restricciones del curso
    ├── Analizador_lexico_taller.md # Enunciado completo de la práctica 1
    ├── lexer.py                    # Implementación del analizador léxico
    ├── gen_tests.py                # Script de pruebas de casos borde
    └── test_escape.esjs            # Archivo temporal de pruebas (ignorar)
```

---

## Práctica 1 — Analizador Léxico (lexer.py)

### Estado: COMPLETO ✓

**Lenguaje:** Python 3.9
**Rama:** `taller1`

### Cómo ejecutar

```bash
py lexer.py < archivo.esjs
# o por stdin:
echo 'consola.escribir("Hola")' | py lexer.py
```

### Qué implementa

| Componente | Estado |
|---|---|
| Palabras reservadas (~200) | ✓ Completo — fuente: es.js.org/sintaxis/palabras-reservadas |
| Identificadores (Unicode, `_`, `$`) | ✓ |
| Números enteros y decimales | ✓ |
| Strings con `"` y `'` | ✓ Lexema sin comillas, escapes preservados |
| Expresiones regulares `/pat/` | ✓ Sin banderas |
| Operadores y símbolos (39 tokens) | ✓ |
| Comentarios `//` y `/* */` | ✓ Ignorados |
| Maximal munch | ✓ `===` antes `==`, `**=` antes `**`, `...` antes `.` |
| Case sensitive | ✓ `ESCRIBIR`→id, `escribir`→reservada |
| Error léxico (aborta en el primero) | ✓ Formato `>>> Error lexico (linea: X, posicion: Y)` |
| Encoding UTF-8 (Unicode en strings/ids) | ✓ |

### Formatos de salida

```
<palabra_reservada,fila,columna>
<id,lexema,fila,columna>
<tkn_num,lexema,fila,columna>
<tkn_str,lexema,fila,columna>
<tkn_reg,lexema,fila,columna>
<tkn_nombre_operador,fila,columna>
>>> Error lexico (linea: X, posicion: Y)
```

### Decisiones de diseño importantes

- **`/` ambiguo:** Si el token anterior fue un "valor" (id, número, string, `)`, `]`, `++`, `--`) → división. De lo contrario → intenta regex. Si el regex no cierra antes de fin de línea → fallback a división.
- **Regex sin cerrar:** Fallback a `tkn_div` (no error léxico).
- **`\r`:** Se ignora (compatibilidad Windows `\r\n`).
- **Tabs:** Cuentan como 1 columna.
- **Columna de strings:** Apunta a la comilla de apertura.
- **Signo `+`/`-`:** Siempre token separado, nunca parte del número.

### Palabras reservadas excluidas del curso (pero sí reconocidas por el lexer)

`asincrono`, `producir`, `exportar`, `importar`, `desde`, `ambienteGlobal`,
`depurador`, `establecerTemporizador`, `establecerIntervalo`, `Promesa`,
y todos los métodos de `Fecha`. Ver `alcance.md` para la lista completa.

---

## Notas generales

- Solo se usa **un archivo fuente** (sin módulos).
- Interacción únicamente por **consola** (stdin/stdout).
- Cambios al alcance se anuncian por **Campuswire**.
