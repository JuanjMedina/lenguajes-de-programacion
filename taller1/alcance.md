# Alcance del Lenguaje EsJS — Curso 2026-1

**Profesor:** Felipe Restrepo Calle (ferestrepoca@unal.edu.co)
**Monitor:** Reinaldo Toledo Leguizamón (rtoledol@unal.edu.co)

---

## Descripción

EsJS es un lenguaje Open Source basado en JavaScript con sintaxis completamente en español. Para este curso se evalúa un subconjunto específico del lenguaje.

---

## Sintaxis contemplada

| Característica         | Incluida |
|------------------------|----------|
| Palabras reservadas    | ✓        |
| Comentarios            | ✓        |
| Variables              | ✓        |
| Constantes             | ✓        |
| Operadores             | ✓        |
| Condición `si … no`    | ✓        |
| Declaración `elegir`   | ✓        |
| Bucle `para`           | ✓        |
| Bucle `mientras`       | ✓        |
| Bucle `hacer … mientras` | ✓      |
| Módulos                | ✗ (ignorar) |

> Solo se permite un archivo fuente. No se usan módulos ni importaciones.

---

## Palabras reservadas

Solo se usan las palabras reservadas **en español** definidas en el manual de referencia de EsJS. No se mezclan con palabras reservadas nativas de JavaScript.

---

## Tipos de datos

Se contempla la totalidad de tipos de datos descritos en el manual de referencia.

---

## Temas avanzados contemplados

- **Elevación (Hoisting):** incluida según la sección de temas avanzados del manual.

---

## Palabras reservadas excluidas

Las siguientes palabras no se usan en ninguna práctica del curso:

| EsJS                     | JavaScript equivalente |
|--------------------------|------------------------|
| `asincrono`              | `async`                |
| `producir`               | `yield`                |
| `exportar`               | `export`               |
| `importar`               | `import`               |
| `desde`                  | `from`                 |
| `ambienteGlobal`         | `globalThis`           |
| `depurador`              | `debugger`             |
| `establecerTemporizador` | `setTimeout`           |
| `establecerIntervalo`    | `setInterval`          |
| `Promesa`                | `Promise`              |
| `contar`                 | `console.count`        |
| `reiniciarContador`      | `countReset`           |
| `depurar`                | `console.debug`        |
| `listarXml`              | `console.dirxml`       |
| `agruparColapsado`       | `groupCollapsed`       |
| `finalizarAgrupacion`    | `groupEnd`             |
| `perfil`                 | `profile`              |
| `finalizarPerfil`        | `profileEnd`           |
| `tiempo`                 | `time`                 |
| `finalizarTiempo`        | `timeEnd`              |
| `registrarTiempo`        | `timeLog`              |
| `marcaDeTiempo`          | `timeStamp`            |
| `rastrear`               | `trace`                |
| `advertencia`            | `warn`                 |

También se excluyen todas las palabras del objeto `Fecha` y del objeto `Promesa`.

---

## Expresiones regulares

Solo se permite definirlas con el delimitador `/regex/` **sin banderas**.

---

## Entorno de trabajo

- Interacción únicamente por consola.
- Se recomienda el editor en línea de EsJS para evitar instalación local.

---

## Notas

- Este documento puede actualizarse durante el semestre; los cambios se comunican por Campuswire.
