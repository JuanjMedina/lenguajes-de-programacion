# Práctica 1 — Analizador Léxico: Lenguaje EsJS

**Profesor:** Felipe Restrepo Calle (ferestrepoca@unal.edu.co)
**Monitor:** Reinaldo Toledo Leguizamón (rtoledol@unal.edu.co)

---

## Descripción

Dado el código fuente de un programa en EsJS, realizar el análisis léxico de acuerdo a las especificaciones descritas. Lenguajes permitidos para la implementación: **Python 3.9, C/C++ y Java**.

---

## Entrada

Código fuente de un programa EsJS recibido por **entrada estándar (consola)**. Puede ser léxicamente correcto o no.

---

## Salida

Lista de tokens por **salida estándar (consola)**, uno por línea.

### Formato general

```
<tipo_de_token,lexema,fila,columna>
```

### Palabras reservadas

El tipo de token y el lexema son iguales; formato reducido:

```
<palabra_reservada,fila,columna>
```

Ejemplo: `<caso,4,6>`

---

## Tipos de token

### Identificadores (`id`)

```
<id,lexema,fila,columna>
```

- Deben comenzar con letra, guión bajo (`_`) o signo dólar (`$`).
- Los siguientes caracteres pueden ser dígitos (`0-9`).
- Soporta letras `A-Z`, `a-z`, ISO 8859-1, Unicode (ej: `å`, `ü`) y secuencias de escape Unicode.
- El lenguaje es **case sensitive**: `ESCRIBIR` → `id`; `escribir` → palabra reservada.

Ejemplos válidos: `Numero_ventas`, `temporal99`, `$crédito`, `_nombre`

### Valores numéricos

```
<tkn_num,lexema,fila,columna>
```

El lexema es el número (entero o decimal).

### Cadenas de caracteres

```
<tkn_str,lexema,fila,columna>
```

- El lexema se imprime **sin las comillas** delimitadoras (dobles o simples).
- Se respetan mayúsculas, minúsculas, espacios y secuencias de escape del manual.
- Comillas simples dentro de cadena delimitada con dobles: se escriben directamente.
- Comillas dobles dentro de cadena delimitada con simples: se escriben directamente.
- Comillas del mismo tipo que el delimitador: usar secuencias de escape.

### Expresiones regulares

```
<tkn_reg,lexema,fila,columna>
```

El lexema se imprime **sin los delimitadores** `/`. Solo se contemplan sin banderas.

---

## Tabla de operadores y símbolos

| Símbolo u Operador | nombre_token   | Token impreso            |
|--------------------|----------------|--------------------------|
| `&&`               | `and`          | `<tkn_and,fila,col>`     |
| `\|\|`             | `or`           | `<tkn_or,fila,col>`      |
| `...`              | `spread`       | `<tkn_spread,fila,col>`  |
| `.`                | `period`       | `<tkn_period,fila,col>`  |
| `,`                | `comma`        | `<tkn_comma,fila,col>`   |
| `;`                | `semicolon`    | `<tkn_semicolon,fila,col>` |
| `:`                | `colon`        | `<tkn_colon,fila,col>`   |
| `{`                | `opening_key`  | `<tkn_opening_key,fila,col>` |
| `}`                | `closing_key`  | `<tkn_closing_key,fila,col>` |
| `[`                | `opening_bra`  | `<tkn_opening_bra,fila,col>` |
| `]`                | `closing_bra`  | `<tkn_closing_bra,fila,col>` |
| `(`                | `opening_par`  | `<tkn_opening_par,fila,col>` |
| `)`                | `closing_par`  | `<tkn_closing_par,fila,col>` |
| `++`               | `increment`    | `<tkn_increment,fila,col>` |
| `--`               | `decrement`    | `<tkn_decrement,fila,col>` |
| `%=`               | `mod_assign`   | `<tkn_mod_assign,fila,col>` |
| `/=`               | `div_assign`   | `<tkn_div_assign,fila,col>` |
| `*=`               | `times_assign` | `<tkn_times_assign,fila,col>` |
| `-=`               | `minus_assign` | `<tkn_minus_assign,fila,col>` |
| `+=`               | `plus_assign`  | `<tkn_plus_assign,fila,col>` |
| `**=`              | `power_assign` | `<tkn_power_assign,fila,col>` |
| `+`                | `plus`         | `<tkn_plus,fila,col>`    |
| `-`                | `minus`        | `<tkn_minus,fila,col>`   |
| `*`                | `times`        | `<tkn_times,fila,col>`   |
| `/`                | `div`          | `<tkn_div,fila,col>`     |
| `**`               | `power`        | `<tkn_power,fila,col>`   |
| `%`                | `mod`          | `<tkn_mod,fila,col>`     |
| `==`               | `equal`        | `<tkn_equal,fila,col>`   |
| `===`              | `strict_equal` | `<tkn_strict_equal,fila,col>` |
| `!=`               | `neq`          | `<tkn_neq,fila,col>`     |
| `!==`              | `strict_neq`   | `<tkn_strict_neq,fila,col>` |
| `<=`               | `leq`          | `<tkn_leq,fila,col>`     |
| `>=`               | `geq`          | `<tkn_geq,fila,col>`     |
| `>`                | `greater`      | `<tkn_greater,fila,col>` |
| `<`                | `less`         | `<tkn_less,fila,col>`    |
| `=`                | `assign`       | `<tkn_assign,fila,col>`  |
| `=>`               | `arrow`        | `<tkn_arrow,fila,col>`   |
| `!`                | `not`          | `<tkn_not,fila,col>`     |
| `?`                | `ternary`      | `<tkn_ternary,fila,col>` |
| `??`               | `nulish`       | `<tkn_nulish,fila,col>`  |

> Formato: `<tkn_nombre_token,fila,columna>` — sin lexema para operadores y símbolos.
> No se contemplan operadores de operaciones a nivel de bits ni otros no listados.

---

## Comentarios

Se **ignoran** completamente en la salida.

- Línea: `// comentario hasta fin de línea`
- Bloque: `/* comentario de una o varias líneas */`

Un comentario puede aparecer al final de una línea con tokens válidos; solo se ignora la parte del comentario.

---

## Principio de subcadena más larga (maximal munch)

Se aplica siempre, incluso ante errores léxicos.

**Ejemplo:** `120.075.389` → `<tkn_num,120.075,...>` + `<tkn_period,...>` + `<tkn_num,389,...>`

El signo (`+` / `-`) antes de un número se reporta como token adicional separado (`tkn_plus` / `tkn_minus`).

---

## Errores léxicos

Al detectar un error léxico se **aborta el análisis** y se reporta:

```
>>> Error lexico (linea: X, posicion: Y)
```

Donde `X` = fila y `Y` = columna del inicio del error. El resto de la entrada no se analiza.

---

## Ejemplos

### Ejemplo 1 — Palabras reservadas e identificadores

| Entrada | Salida |
|---------|--------|
| `escribir` | `<escribir,1,1>` |
| `    elegir` | `<elegir,3,5>` |
| `     caso mientras sino` | `<caso,4,6>` `<mientras,4,11>` `<sino,4,20>` |
| ` escribir absoluto` | `<escribir,6,2>` `<absoluto,6,11>` |
| `    consola` | `<consola,7,5>` |
| `retornar` | `<retornar,8,1>` |

### Ejemplo 2 — Case sensitivity

```
ESCRIBIR escribir
Escribir Mi_Variable
MI_VARIABLE
MI_Variable
mIENtras MIENTRAS mientras
```

```
<id,ESCRIBIR,1,1>
<escribir,1,10>
<id,Escribir,3,1>
<id,Mi_Variable,3,10>
<id,MI_VARIABLE,5,1>
<id,MI_Variable,7,1>
<id,mIENtras,9,1>
<id,MIENTRAS,9,10>
<mientras,9,19>
```

### Ejemplo 3 — Comentarios

```
consola
   repetir en falso o sino
   // this is for open source enjoyers
         en verdadero Nene // perfect
   /* I don´t have enough creativity
      to write comments
  */
   v
```

```
<consola,1,1>
<repetir,2,4>
<en,2,12>
<falso,2,15>
<id,o,2,21>
<sino,2,23>
<en,5,10>
<verdadero,5,13>
<id,Nene,5,23>
<id,v,10,4>
```

### Ejemplo 4 — Símbolos especiales

```
si (x) {
  // código
} sino {
   // código
}
```

```
<si,1,1>
<tkn_opening_par,1,4>
<id,x,1,5>
<tkn_closing_par,1,6>
<tkn_opening_key,1,8>
<tkn_closing_key,3,1>
<sino,3,3>
<tkn_opening_key,3,8>
<tkn_closing_key,5,1>
```

### Ejemplo 5 — Números, strings y signo

```
mut my_Var1 = +2
const my_Var2 = -3.145
var string = '"double" string'
var string2 = "'single' string"
// another single comment
```

```
<mut,1,1>
<id,my_Var1,1,5>
<tkn_assign,1,13>
<tkn_plus,1,15>
<tkn_num,2,1,16>
<const,2,1>
<id,my_Var2,2,7>
<tkn_assign,2,15>
<tkn_minus,2,17>
<tkn_num,3.145,2,18>
<var,3,1>
<id,string,3,5>
<tkn_assign,3,12>
<tkn_str,"double" string,3,14>
<var,4,1>
<id,string2,4,5>
<tkn_assign,4,13>
<tkn_str,'single' string,4,15>
```

### Ejemplo 6 — Error léxico

```
const getSubject = () => {
  consola.escribir("EsJs (◕‿◕)")
  como se retornaba? @__@
}
consola.escribir(getSubject())
```

```
<const,1,1>
<id,getSubject,1,7>
<tkn_assign,1,18>
<tkn_opening_par,1,20>
<tkn_closing_par,1,21>
<tkn_arrow,1,23>
<tkn_opening_key,1,26>
<consola,2,3>
<tkn_period,2,10>
<escribir,2,11>
<tkn_opening_par,2,19>
<tkn_str,EsJs (◕‿◕),2,20>
<tkn_closing_par,2,32>
<id,como,3,3>
<id,se,3,8>
<id,retornaba,3,11>
<tkn_ternary,3,20>
>>> Error lexico (linea: 3, posicion: 22)
```

### Ejemplo 7 — Caso extremo

```
_f 4.559<>6="1"|vari8
```

```
<id,_f,1,1>
<tkn_num,4.559,1,4>
<tkn_less,1,9>
<tkn_greater,1,10>
<tkn_num,6,1,11>
<tkn_assign,1,12>
<tkn_str,1,1,13>
>>> Error lexico (linea: 1, posicion: 16)
```

---

## Observaciones finales

- Los casos de prueba del documento pueden tener variaciones de formato; usar los de la plataforma de evaluación.
- Se recomienda validar con los ejemplos disponibles en la plataforma de evaluación.
