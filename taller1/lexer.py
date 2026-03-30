import sys

# ─── Palabras reservadas (fuente: es.js.org/sintaxis/palabras-reservadas) ──────
RESERVED_WORDS = {
    # Control keywords
    'capturar', 'caso', 'con', 'continuar', 'crear', 'desde', 'elegir',
    'esperar', 'exportar', 'hacer', 'importar', 'mientras', 'para',
    'retornar', 'sino', 'si', 'constructor', 'eliminar', 'extiende',
    'finalmente', 'instanciaDe', 'intentar', 'lanzar', 'longitud',
    'romper', 'simbolo', 'subcad', 'tipoDe', 'vacio', 'producir',
    'ambiente', 'super', 'de', 'en',
    # Storage types
    'asincrono', 'clase', 'const', 'var', 'mut', 'porDefecto', 'funcion',
    # Language constants
    'falso', 'nulo', 'verdadero', 'indefinido', 'Infinito', 'NuN',
    'ambienteGlobal',
    # Support functions (built-in objects)
    'consola', 'depurador', 'establecerTemporizador', 'establecerIntervalo',
    'Fecha', 'Numero', 'Mate', 'Matriz', 'Arreglo', 'Booleano', 'Cadena',
    'Funcion', 'Promesa',
    # Console methods
    'afirmar', 'limpiar', 'contar', 'reiniciarContador', 'depurar',
    'listar', 'listarXml', 'error', 'agrupar', 'agruparColapsado',
    'finalizarAgrupacion', 'info', 'escribir', 'perfil', 'finalizarPerfil',
    'tabla', 'tiempo', 'finalizarTiempo', 'registrarTiempo', 'marcaDeTiempo',
    'rastrear', 'advertencia',
    # String methods
    'enPosicion', 'caracterEn', 'codigoDeCaracterEn', 'puntoDeCodigoEn',
    'concatenar', 'terminaCon', 'desdeCodigoDeCaracter', 'desdePuntoDeCodigo',
    'incluye', 'indiceDe', 'ultimoIndiceDe', 'compararLocalizada',
    'coincidir', 'coincidirTodo', 'normalizar', 'rellenarAlFinal',
    'rellenarAlComienzo', 'crudo', 'repetir', 'reemplazar', 'reemplazarTodo',
    'buscarRegex', 'recortar', 'dividir', 'comienzaCon', 'subcadena',
    'aMinusculasLocalizada', 'aMayusculasLocalizada', 'aMinusculas',
    'aMayusculas', 'aCadena', 'recortarEspacios', 'recortarEspaciosAlFinal',
    'recortarEspaciosAlComienzo', 'valorDe',
    # Number methods
    'esNuN', 'esFinito', 'esEntero', 'esEnteroSeguro', 'interpretarDecimal',
    'interpretarEntero', 'aExponencial', 'fijarDecimales', 'aCadenaLocalizada',
    'aPrecision',
    # Math methods
    'absoluto', 'arcocoseno', 'arcocosenoHiperbolico', 'arcoseno',
    'arcosenoHiperbolico', 'arcotangente', 'arcotangente2',
    'arcotangenteHiperbolica', 'raizCubica', 'redondearHaciaArriba',
    'cerosALaIzquierdaEn32Bits', 'coseno', 'cosenoHiperbolico', 'exponencial',
    'exponencialMenos1', 'redondearHaciaAbajo', 'redondearAComaFlotante',
    'hipotenusa', 'multiplicacionEntera', 'logaritmo', 'logaritmoBase10',
    'logaritmoDe1Mas', 'logaritmoBase2', 'maximo', 'minimo', 'potencia',
    'aleatorio', 'redondear', 'signo', 'seno', 'senoHiperbolico',
    'raizCuadrada', 'tangente', 'tangenteHiperbolica', 'truncar',
    # Date methods
    'obtenerDia', 'obtenerDiaSemana', 'obtenerAnio', 'obtenerAño',
    'obtenerHoras', 'obtenerMilisegundos', 'obtenerMinutos', 'obtenerMes',
    'obtenerSegundos', 'obtenerTiempo', 'obtenerDesfaseDeZonaHoraria',
    'obtenerDiaUTC', 'obtenerDiaSemanaUTC', 'obtenerAnioUTC', 'obtenerAñoUTC',
    'obtenerHorasUTC', 'obtenerMilisegundosUTC', 'obtenerMinutosUTC',
    'obtenerMesUTC', 'obtenerSegundosUTC', 'ahora', 'analizar',
    'establecerFecha', 'establecerAnio', 'establecerAño', 'establecerHoras',
    'establecerMilisegundos', 'establecerMinutos', 'establecerMes',
    'establecerSegundos', 'establecerTiempo', 'establecerFechaUTC',
    'establecerAnioUTC', 'establecerAñoUTC', 'establecerHorasUTC',
    'establecerMilisegundosUTC', 'establecerMinutosUTC', 'establecerMesUTC',
    'establecerSegundosUTC', 'aCadenaFecha', 'aCadenaISO', 'aJSON',
    'aCadenaFechaLocale', 'aCadenaLocale', 'aCadenaTiempoLocale',
    'aCadenaTiempo', 'aCadenaUTC', 'UTC',
    # Array methods
    'posicion', 'copiarDentro', 'entradas', 'cada', 'llenar', 'filtrar',
    'buscar', 'buscarIndice', 'buscarUltimo', 'buscarUltimoIndice',
    'plano', 'planoMapear', 'paraCada', 'grupo', 'grupoAMapear',
    'juntar', 'claves', 'mapear', 'sacar', 'agregar', 'reducir', 'reducirDerecha',
    'reverso', 'sacarPrimero', 'rodaja', 'algun', 'ordenar', 'empalmar',
    'agregarInicio', 'valores',
    # Promise methods
    'todos', 'todosTerminados', 'cualquiera', 'carrera', 'rechaza',
    'resuelve', 'luego',
}

# Palabras reservadas que actúan como valores (para la heurística de regex vs división)
VALUE_RESERVED = {
    'verdadero', 'falso', 'nulo', 'indefinido', 'Infinito', 'NuN', 'ambiente',
}

# ─── Operadores y símbolos (orden: más largo primero para maximal munch) ────────
OPERATORS = [
    # 3 caracteres
    ('**=', 'power_assign'),
    ('===', 'strict_equal'),
    ('!==', 'strict_neq'),
    ('...', 'spread'),
    # 2 caracteres
    ('**', 'power'),
    ('==', 'equal'),
    ('!=', 'neq'),
    ('<=', 'leq'),
    ('>=', 'geq'),
    ('=>', 'arrow'),
    ('&&', 'and'),
    ('||', 'or'),
    ('??', 'nulish'),
    ('++', 'increment'),
    ('--', 'decrement'),
    ('%=', 'mod_assign'),
    ('*=', 'times_assign'),
    ('-=', 'minus_assign'),
    ('+=', 'plus_assign'),
    # 1 carácter  (nota: '/' y '/=' se manejan por separado)
    ('+', 'plus'),
    ('-', 'minus'),
    ('*', 'times'),
    ('%', 'mod'),
    ('<', 'less'),
    ('>', 'greater'),
    ('=', 'assign'),
    ('!', 'not'),
    ('?', 'ternary'),
    ('.', 'period'),
    (',', 'comma'),
    (';', 'semicolon'),
    (':', 'colon'),
    ('{', 'opening_key'),
    ('}', 'closing_key'),
    ('[', 'opening_bra'),
    (']', 'closing_bra'),
    ('(', 'opening_par'),
    (')', 'closing_par'),
]

# Nombres de operadores que producen un valor (para la heurística de regex)
VALUE_OPERATORS = {'closing_par', 'closing_bra', 'increment', 'decrement'}


def is_id_start(c: str) -> bool:
    """Un identificador puede comenzar con letra, '_' o '$'."""
    return c.isalpha() or c == '_' or c == '$'


def is_id_part(c: str) -> bool:
    """Continuación de identificador: letra, dígito, '_' o '$'."""
    return c.isalpha() or c.isdigit() or c == '_' or c == '$'


def tokenize(source: str) -> None:
    pos = 0
    line = 1
    col = 1
    n = len(source)

    # Heurística: ¿el token anterior fue un "valor"?
    # True  → '/' se interpreta como división
    # False → '/' se intenta como regex primero
    last_was_value = False

    while pos < n:
        c = source[pos]

        # ── Salto de línea ────────────────────────────────────────────────
        if c == '\n':
            line += 1
            col = 1
            pos += 1
            continue

        # ── Espacio en blanco ─────────────────────────────────────────────
        if c in ' \t\r':
            col += 1
            pos += 1
            continue

        tok_line = line
        tok_col = col

        # ── Barra: comentario, /=, regex o división ───────────────────────
        if c == '/':
            # Comentario de línea //
            if pos + 1 < n and source[pos + 1] == '/':
                while pos < n and source[pos] != '\n':
                    pos += 1
                    col += 1
                continue

            # Comentario de bloque /* ... */
            if pos + 1 < n and source[pos + 1] == '*':
                comment_line = tok_line
                comment_col = tok_col
                pos += 2
                col += 2
                closed_comment = False
                while pos < n:
                    if source[pos] == '\n':
                        line += 1
                        col = 1
                        pos += 1
                    elif source[pos:pos + 2] == '*/':
                        pos += 2
                        col += 2
                        closed_comment = True
                        break
                    else:
                        col += 1
                        pos += 1
                if not closed_comment:
                    print(f'>>> Error lexico (linea: {comment_line}, posicion: {comment_col})')
                    return
                continue

            # Expresión regular /pattern/ (solo si el token anterior no fue valor)
            if not last_was_value:
                save_pos, save_col = pos, col
                pos += 1
                col += 1
                regex_chars = []
                found_close = False
                while pos < n and source[pos] != '\n':
                    ch = source[pos]
                    if ch == '\\':
                        regex_chars.append(ch)
                        pos += 1
                        col += 1
                        if pos < n:
                            regex_chars.append(source[pos])
                            pos += 1
                            col += 1
                    elif ch == '/':
                        pos += 1
                        col += 1
                        found_close = True
                        break
                    else:
                        regex_chars.append(ch)
                        pos += 1
                        col += 1
                if found_close:
                    print(f'<tkn_reg,{"".join(regex_chars)},{tok_line},{tok_col}>')
                    last_was_value = True
                    continue
                # No se encontró cierre: revertir y tratar como división
                pos, col = save_pos, save_col

            # Operador /=
            if pos + 1 < n and source[pos + 1] == '=':
                print(f'<tkn_div_assign,{tok_line},{tok_col}>')
                pos += 2
                col += 2
                last_was_value = False
                continue

            # Operador de división
            print(f'<tkn_div,{tok_line},{tok_col}>')
            pos += 1
            col += 1
            last_was_value = False
            continue

        # ── Cadena de caracteres ──────────────────────────────────────────
        if c in ('"', "'"):
            quote = c
            pos += 1
            col += 1
            chars = []
            closed = False
            while pos < n:
                ch = source[pos]
                if ch == '\\':
                    chars.append(ch)
                    pos += 1
                    col += 1
                    if pos < n:
                        chars.append(source[pos])
                        pos += 1
                        col += 1
                elif ch == quote:
                    pos += 1
                    col += 1
                    closed = True
                    break
                elif ch == '\n':
                    print(f'>>> Error lexico (linea: {tok_line}, posicion: {tok_col})')
                    return
                else:
                    chars.append(ch)
                    pos += 1
                    col += 1
            if not closed:
                print(f'>>> Error lexico (linea: {tok_line}, posicion: {tok_col})')
                return
            print(f'<tkn_str,{"".join(chars)},{tok_line},{tok_col}>')
            last_was_value = True
            continue

        # ── Número ────────────────────────────────────────────────────────
        if c.isdigit():
            num = []
            while pos < n and source[pos].isdigit():
                num.append(source[pos])
                pos += 1
                col += 1
            # Parte decimal opcional (solo un punto)
            if (pos < n and source[pos] == '.'
                    and pos + 1 < n and source[pos + 1].isdigit()):
                num.append('.')
                pos += 1
                col += 1
                while pos < n and source[pos].isdigit():
                    num.append(source[pos])
                    pos += 1
                    col += 1
            print(f'<tkn_num,{"".join(num)},{tok_line},{tok_col}>')
            last_was_value = True
            continue

        # ── Identificador o palabra reservada ────────────────────────────
        if is_id_start(c):
            word = []
            while pos < n and is_id_part(source[pos]):
                word.append(source[pos])
                pos += 1
                col += 1
            w = ''.join(word)
            if w in RESERVED_WORDS:
                print(f'<{w},{tok_line},{tok_col}>')
                last_was_value = w in VALUE_RESERVED
            else:
                print(f'<id,{w},{tok_line},{tok_col}>')
                last_was_value = True
            continue

        # ── Operadores y símbolos ─────────────────────────────────────────
        matched = False
        for sym, name in OPERATORS:
            if source[pos:pos + len(sym)] == sym:
                print(f'<tkn_{name},{tok_line},{tok_col}>')
                pos += len(sym)
                col += len(sym)
                last_was_value = name in VALUE_OPERATORS
                matched = True
                break
        if matched:
            continue

        # ── Error léxico ──────────────────────────────────────────────────
        print(f'>>> Error lexico (linea: {tok_line}, posicion: {tok_col})')
        return


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    source = sys.stdin.buffer.read().decode('utf-8')
    tokenize(source)
