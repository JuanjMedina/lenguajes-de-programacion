# Progreso del curso — Lenguajes de Programación 2026-1

## Taller 1 — Analizador Léxico ✓ COMPLETO

**Archivo:** `taller1/lexer.py`
**Estado:** Pasa 100% de los tests en UNCode.

### Uso
```bash
py taller1/lexer.py < archivo.esjs
```

### Tokens que produce
| Tipo | Formato |
|---|---|
| Palabra reservada | `<palabra,fila,col>` |
| Identificador | `<id,lexema,fila,col>` |
| Número | `<tkn_num,lexema,fila,col>` |
| Cadena | `<tkn_str,lexema,fila,col>` |
| Regex | `<tkn_reg,lexema,fila,col>` |
| Operador | `<tkn_nombre,fila,col>` |
| Error | `>>> Error lexico (linea: X, posicion: Y)` |

### Decisiones clave
- `/` ambiguo: si el token anterior fue un "valor" → división; sino → intenta regex (fallback a `tkn_div` si no cierra).
- Lexema de strings no incluye comillas; escapes preservados as-is.
- Maximal munch: operadores 3-char > 2-char > 1-char.
- `??` y `...` sí se lexifican (como `tkn_nulish` y `tkn_spread`).

---

## Taller 2 — Analizador Sintáctico ✓ IMPLEMENTADO

**Archivo:** `taller2/parser.py`
**Deadline entrega:** 29 abril 2026 a las 23:59 (UNCode)
**Deadline gramática PDF:** 30 abril 2026 a las 23:59 → enviar a rtoledol@unal.edu.co con asunto `[LP] - Gramatica Parser EsJS`

### Uso
```bash
py taller2/parser.py < archivo.esjs
```

### Salidas
```
El analisis sintactico ha finalizado exitosamente.
```
```
<linea:col> Error sintactico: se encontro: "lexema"; se esperaba: "a" "b" "c".
```

### Gramática implementada (LL(1) recursivo descendente)
| Construcción | Estado |
|---|---|
| `var`, `mut`, `const` | ✓ |
| `funcion` (declaración y expresión) | ✓ |
| Arrow functions `=>` | ✓ |
| `si` / `sino` | ✓ |
| `elegir` / `caso` / `porDefecto` | ✓ |
| `para` (C-style y for-in con `en`) | ✓ |
| `mientras` | ✓ |
| `hacer … mientras` | ✓ |
| `intentar` / `capturar` / `finalmente` | ✓ |
| `retornar`, `romper`, `continuar` | ✓ |
| `crear` (new) | ✓ |
| Literales: array `[]`, objeto `{}` | ✓ |
| Operadores (torre de precedencia completa) | ✓ |
| Semicolons opcionales | ✓ |
| **Excluidos:** `??`, `...`, regex | ✓ |

### Decisiones de diseño importantes
- `consola` en primario **requiere** `.` inmediatamente: `consola escribir(i)` → `se esperaba: "."`.
- Tras `parse_expr()` en arg-list se valida que el siguiente token sea operador binario o `,`/`)`, produciendo el conjunto completo de esperados (ej. `"&&" ")" "," ...`).
- El tokenizer está embebido en `parser.py` (copia modificada de `taller1/lexer.py` que retorna `list[Token]` en vez de imprimir).
- Tokens `??` y `...` se omiten silenciosamente en el tokenizer del parser.

### Ejemplos verificados
| Entrada | Salida esperada | Estado |
|---|---|---|
| `funcion iniciar() { const fecha = crear Fecha() consola.escribir(fecha) } iniciar()` | éxito | ✓ |
| `var 1;` | `<1:5> ... se esperaba: "id".` | ✓ |
| `consola.escribir(45"this")` | `<1:20> ... se esperaba: "!=" "!==" "%" ...` | ✓ |
| `mut entrada; si (entrada === indefinido) { ... }` | éxito | ✓ |
| `consola escribir(i)` | `<4:13> ... se esperaba: "."` | ✓ |
