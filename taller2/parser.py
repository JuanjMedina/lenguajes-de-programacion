import sys
from dataclasses import dataclass
from typing import List, Optional

# ─── Token ────────────────────────────────────────────────────────────────────

@dataclass
class Token:
    type: str    # reserved word / 'id' / 'tkn_num' / 'tkn_str' / 'tkn_X' / 'EOF'
    lexeme: str  # raw text for display
    line: int
    col: int

# ─── Display maps ─────────────────────────────────────────────────────────────

# Maps internal token type → human-readable string for "se esperaba" list
_EXPECTED_DISPLAY = {
    'id':  'id',
    'tkn_num': 'valor_numerico',
    'tkn_str': 'cadena_de_caracteres',
    'EOF': 'final de archivo',
    'tkn_plus':         '+',
    'tkn_minus':        '-',
    'tkn_times':        '*',
    'tkn_div':          '/',
    'tkn_mod':          '%',
    'tkn_power':        '**',
    'tkn_assign':       '=',
    'tkn_plus_assign':  '+=',
    'tkn_minus_assign': '-=',
    'tkn_times_assign': '*=',
    'tkn_div_assign':   '/=',
    'tkn_mod_assign':   '%=',
    'tkn_power_assign': '**=',
    'tkn_equal':        '==',
    'tkn_neq':          '!=',
    'tkn_strict_equal': '===',
    'tkn_strict_neq':   '!==',
    'tkn_less':         '<',
    'tkn_greater':      '>',
    'tkn_leq':          '<=',
    'tkn_geq':          '>=',
    'tkn_and':          '&&',
    'tkn_or':           '||',
    'tkn_not':          '!',
    'tkn_ternary':      '?',
    'tkn_increment':    '++',
    'tkn_decrement':    '--',
    'tkn_arrow':        '=>',
    'tkn_period':       '.',
    'tkn_comma':        ',',
    'tkn_semicolon':    ';',
    'tkn_colon':        ':',
    'tkn_opening_key':  '{',
    'tkn_closing_key':  '}',
    'tkn_opening_bra':  '[',
    'tkn_closing_bra':  ']',
    'tkn_opening_par':  '(',
    'tkn_closing_par':  ')',
}

def expected_display(tok_type: str) -> str:
    if tok_type in _EXPECTED_DISPLAY:
        return _EXPECTED_DISPLAY[tok_type]
    return tok_type  # reserved word: type == lexeme

def found_display(tok: Token) -> str:
    if tok.type == 'EOF':
        return 'final de archivo'
    return tok.lexeme  # always the raw lexeme

# ─── Tokenizer (adapted from taller1/lexer.py) ───────────────────────────────

RESERVED_WORDS = {
    'capturar', 'caso', 'con', 'continuar', 'crear', 'desde', 'elegir',
    'esperar', 'exportar', 'hacer', 'importar', 'mientras', 'para',
    'retornar', 'sino', 'si', 'constructor', 'eliminar', 'extiende',
    'finalmente', 'instanciaDe', 'intentar', 'lanzar', 'longitud',
    'romper', 'simbolo', 'subcad', 'tipoDe', 'vacio', 'producir',
    'ambiente', 'super', 'de', 'en',
    'asincrono', 'clase', 'const', 'var', 'mut', 'porDefecto', 'funcion',
    'falso', 'nulo', 'verdadero', 'indefinido', 'Infinito', 'NuN',
    'ambienteGlobal',
    'consola', 'depurador', 'establecerTemporizador', 'establecerIntervalo',
    'Fecha', 'Numero', 'Mate', 'Matriz', 'Arreglo', 'Booleano', 'Cadena',
    'Funcion', 'Promesa',
    'afirmar', 'limpiar', 'contar', 'reiniciarContador', 'depurar',
    'listar', 'listarXml', 'error', 'agrupar', 'agruparColapsado',
    'finalizarAgrupacion', 'info', 'escribir', 'perfil', 'finalizarPerfil',
    'tabla', 'tiempo', 'finalizarTiempo', 'registrarTiempo', 'marcaDeTiempo',
    'rastrear', 'advertencia',
    'enPosicion', 'caracterEn', 'codigoDeCaracterEn', 'puntoDeCodigoEn',
    'concatenar', 'terminaCon', 'desdeCodigoDeCaracter', 'desdePuntoDeCodigo',
    'incluye', 'indiceDe', 'ultimoIndiceDe', 'compararLocalizada',
    'coincidir', 'coincidirTodo', 'normalizar', 'rellenarAlFinal',
    'rellenarAlComienzo', 'crudo', 'repetir', 'reemplazar', 'reemplazarTodo',
    'buscarRegex', 'recortar', 'dividir', 'comienzaCon', 'subcadena',
    'aMinusculasLocalizada', 'aMayusculasLocalizada', 'aMinusculas',
    'aMayusculas', 'aCadena', 'recortarEspacios', 'recortarEspaciosAlFinal',
    'recortarEspaciosAlComienzo', 'valorDe',
    'esNuN', 'esFinito', 'esEntero', 'esEnteroSeguro', 'interpretarDecimal',
    'interpretarEntero', 'aExponencial', 'fijarDecimales', 'aCadenaLocalizada',
    'aPrecision',
    'absoluto', 'arcocoseno', 'arcocosenoHiperbolico', 'arcoseno',
    'arcosenoHiperbolico', 'arcotangente', 'arcotangente2',
    'arcotangenteHiperbolica', 'raizCubica', 'redondearHaciaArriba',
    'cerosALaIzquierdaEn32Bits', 'coseno', 'cosenoHiperbolico', 'exponencial',
    'exponencialMenos1', 'redondearHaciaAbajo', 'redondearAComaFlotante',
    'hipotenusa', 'multiplicacionEntera', 'logaritmo', 'logaritmoBase10',
    'logaritmoDe1Mas', 'logaritmoBase2', 'maximo', 'minimo', 'potencia',
    'aleatorio', 'redondear', 'signo', 'seno', 'senoHiperbolico',
    'raizCuadrada', 'tangente', 'tangenteHiperbolica', 'truncar',
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
    'posicion', 'copiarDentro', 'entradas', 'cada', 'llenar', 'filtrar',
    'buscar', 'buscarIndice', 'buscarUltimo', 'buscarUltimoIndice',
    'plano', 'planoMapear', 'paraCada', 'grupo', 'grupoAMapear',
    'juntar', 'claves', 'mapear', 'sacar', 'agregar', 'reducir', 'reducirDerecha',
    'reverso', 'sacarPrimero', 'rodaja', 'algun', 'ordenar', 'empalmar',
    'agregarInicio', 'valores',
    'todos', 'todosTerminados', 'cualquiera', 'carrera', 'rechaza',
    'resuelve', 'luego',
}

VALUE_RESERVED = {'verdadero', 'falso', 'nulo', 'indefinido', 'Infinito', 'NuN', 'ambiente'}

# (symbol, internal_name, lexeme_for_token)
OPERATORS = [
    ('**=', 'power_assign',   '**='),
    ('===', 'strict_equal',   '==='),
    ('!==', 'strict_neq',     '!=='),
    ('...', 'spread',         '...'),
    ('**',  'power',          '**'),
    ('==',  'equal',          '=='),
    ('!=',  'neq',            '!='),
    ('<=',  'leq',            '<='),
    ('>=',  'geq',            '>='),
    ('=>',  'arrow',          '=>'),
    ('&&',  'and',            '&&'),
    ('||',  'or',             '||'),
    ('??',  'nulish',         '??'),
    ('++',  'increment',      '++'),
    ('--',  'decrement',      '--'),
    ('%=',  'mod_assign',     '%='),
    ('*=',  'times_assign',   '*='),
    ('-=',  'minus_assign',   '-='),
    ('+=',  'plus_assign',    '+='),
    ('+',   'plus',           '+'),
    ('-',   'minus',          '-'),
    ('*',   'times',          '*'),
    ('%',   'mod',            '%'),
    ('<',   'less',           '<'),
    ('>',   'greater',        '>'),
    ('=',   'assign',         '='),
    ('!',   'not',            '!'),
    ('?',   'ternary',        '?'),
    ('.',   'period',         '.'),
    (',',   'comma',          ','),
    (';',   'semicolon',      ';'),
    (':',   'colon',          ':'),
    ('{',   'opening_key',    '{'),
    ('}',   'closing_key',    '}'),
    ('[',   'opening_bra',    '['),
    (']',   'closing_bra',    ']'),
    ('(',   'opening_par',    '('),
    (')',   'closing_par',    ')'),
]

VALUE_OPERATORS = {'closing_par', 'closing_bra', 'increment', 'decrement'}
SKIP_OPERATORS  = {'spread', 'nulish'}  # ?? and ... not used in parser grammar

def is_id_start(c: str) -> bool:
    return c.isalpha() or c == '_' or c == '$'

def is_id_part(c: str) -> bool:
    return c.isalpha() or c.isdigit() or c == '_' or c == '$'

def tokenize(source: str) -> List[Token]:
    tokens: List[Token] = []
    pos = 0
    line = 1
    col = 1
    n = len(source)
    last_was_value = False
    last_line = line
    last_col = col

    while pos < n:
        c = source[pos]

        if c == '\n':
            line += 1
            col = 1
            pos += 1
            continue

        if c in ' \t\r':
            col += 1
            pos += 1
            continue

        tok_line = line
        tok_col  = col
        last_line = line
        last_col  = col

        # ── Slash: comment, regex, /=, division ──────────────────────────
        if c == '/':
            if pos + 1 < n and source[pos + 1] == '/':
                while pos < n and source[pos] != '\n':
                    pos += 1
                    col += 1
                continue

            if pos + 1 < n and source[pos + 1] == '*':
                pos += 2; col += 2
                while pos < n:
                    if source[pos] == '\n':
                        line += 1; col = 1; pos += 1
                    elif source[pos:pos+2] == '*/':
                        pos += 2; col += 2; break
                    else:
                        col += 1; pos += 1
                continue

            if not last_was_value:
                save_pos, save_col = pos, col
                pos += 1; col += 1
                regex_chars = []
                found_close = False
                in_cc = False
                while pos < n and source[pos] != '\n':
                    ch = source[pos]
                    if ch == '\\':
                        regex_chars.append(ch); pos += 1; col += 1
                        if pos < n and source[pos] != '\n':
                            regex_chars.append(source[pos]); pos += 1; col += 1
                    elif ch == '[':
                        in_cc = True; regex_chars.append(ch); pos += 1; col += 1
                    elif ch == ']' and in_cc:
                        in_cc = False; regex_chars.append(ch); pos += 1; col += 1
                    elif ch == '/' and not in_cc:
                        pos += 1; col += 1; found_close = True; break
                    else:
                        regex_chars.append(ch); pos += 1; col += 1
                if found_close:
                    # tkn_reg → skip (not used in parser grammar)
                    last_was_value = False
                    continue
                pos, col = save_pos, save_col

            if pos + 1 < n and source[pos + 1] == '=':
                tokens.append(Token('tkn_div_assign', '/=', tok_line, tok_col))
                pos += 2; col += 2; last_was_value = False; continue

            tokens.append(Token('tkn_div', '/', tok_line, tok_col))
            pos += 1; col += 1; last_was_value = False; continue

        # ── String ───────────────────────────────────────────────────────
        if c in ('"', "'"):
            quote = c
            pos += 1; col += 1
            chars = []; closed = False
            while pos < n:
                ch = source[pos]
                if ch == '\\':
                    chars.append(ch); pos += 1; col += 1
                    if pos < n:
                        chars.append(source[pos]); pos += 1; col += 1
                elif ch == quote:
                    pos += 1; col += 1; closed = True; break
                elif ch == '\n':
                    break
                else:
                    chars.append(ch); pos += 1; col += 1
            tokens.append(Token('tkn_str', ''.join(chars), tok_line, tok_col))
            last_was_value = True; continue

        # ── Number ───────────────────────────────────────────────────────
        if c.isdigit():
            num = []
            while pos < n and source[pos].isdigit():
                num.append(source[pos]); pos += 1; col += 1
            if (pos < n and source[pos] == '.'
                    and pos + 1 < n and source[pos+1].isdigit()):
                num.append('.'); pos += 1; col += 1
                while pos < n and source[pos].isdigit():
                    num.append(source[pos]); pos += 1; col += 1
            tokens.append(Token('tkn_num', ''.join(num), tok_line, tok_col))
            last_was_value = True; continue

        # ── Identifier / reserved word ────────────────────────────────────
        if is_id_start(c):
            word = []
            while pos < n and is_id_part(source[pos]):
                word.append(source[pos]); pos += 1; col += 1
            w = ''.join(word)
            if w in RESERVED_WORDS:
                tokens.append(Token(w, w, tok_line, tok_col))
                last_was_value = w in VALUE_RESERVED
            else:
                tokens.append(Token('id', w, tok_line, tok_col))
                last_was_value = True
            continue

        # ── Operators & symbols ───────────────────────────────────────────
        matched = False
        for sym, name, lex in OPERATORS:
            if source[pos:pos+len(sym)] == sym:
                if name not in SKIP_OPERATORS:
                    tokens.append(Token(f'tkn_{name}', lex, tok_line, tok_col))
                last_was_value = name in VALUE_OPERATORS
                pos += len(sym); col += len(sym); matched = True; break
        if matched:
            continue

        # Unknown character — skip (lexer guarantees no errors)
        pos += 1; col += 1

    tokens.append(Token('EOF', 'final de archivo', last_line, last_col))
    return tokens

# ─── Parser ───────────────────────────────────────────────────────────────────

class ParseError(Exception):
    pass

# Token types that can start an expression (FIRST(expr))
EXPR_FIRST = {
    'id', 'tkn_num', 'tkn_str',
    'verdadero', 'falso', 'nulo', 'indefinido', 'Infinito', 'NuN',
    'tkn_opening_par', 'tkn_opening_bra', 'tkn_opening_key',
    'funcion', 'crear',
    'consola', 'Numero', 'Mate', 'Arreglo', 'Matriz', 'Cadena', 'Booleano',
    'Fecha',
    # console/object method names can appear as expr start in some edge cases
    'afirmar', 'limpiar', 'error', 'agrupar', 'info', 'escribir', 'tabla',
    'tkn_not', 'tkn_minus', 'tkn_plus', 'tkn_increment', 'tkn_decrement',
}

STMT_FIRST = EXPR_FIRST | {
    'var', 'mut', 'const',
    'si', 'elegir', 'para', 'mientras', 'hacer',
    'intentar', 'retornar', 'romper', 'continuar',
    'funcion', 'tkn_semicolon',
}

STMT_END = {'tkn_closing_key', 'EOF', 'caso', 'porDefecto'}

ASSIGN_OPS = {
    'tkn_assign', 'tkn_plus_assign', 'tkn_minus_assign',
    'tkn_times_assign', 'tkn_div_assign', 'tkn_mod_assign', 'tkn_power_assign',
}

# All binary/ternary operators that can extend an expression mid-way
BINARY_OPS_TYPES = {
    'tkn_times', 'tkn_div', 'tkn_mod', 'tkn_power',
    'tkn_plus', 'tkn_minus',
    'tkn_less', 'tkn_greater', 'tkn_leq', 'tkn_geq',
    'tkn_equal', 'tkn_neq', 'tkn_strict_equal', 'tkn_strict_neq',
    'tkn_and', 'tkn_or',
    'tkn_ternary',
}

# All reserved words that can appear as member names after '.'
# (basically any reserved word token the lexer emits)
MEMBER_NAME_TYPES = RESERVED_WORDS | {'id'}

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[0]

    def advance(self) -> Token:
        tok = self.current
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        self.current = self.tokens[self.pos]
        return tok

    def peek(self, offset: int = 1) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def check(self, *types) -> bool:
        return self.current.type in types

    def match(self, *types) -> Optional[Token]:
        if self.current.type in types:
            return self.advance()
        return None

    def expect(self, *types) -> Token:
        if self.current.type in types:
            return self.advance()
        self.error(list(types))

    def error(self, expected_types: list):
        tok = self.current
        found = found_display(tok)
        expected = sorted(set(expected_display(e) for e in expected_types))
        exp_str = ' '.join(f'"{e}"' for e in expected)
        raise ParseError(
            f'<{tok.line}:{tok.col}> Error sintactico: '
            f'se encontro: "{found}"; se esperaba: {exp_str}.'
        )

    def opt_semi(self):
        self.match('tkn_semicolon')

    # ── Top level ──────────────────────────────────────────────────────────

    def parse(self):
        self.parse_stmt_list()
        if not self.check('EOF'):
            self.error(['EOF'])

    def parse_stmt_list(self):
        while self.current.type not in STMT_END:
            if self.current.type not in STMT_FIRST:
                break
            self.parse_stmt()

    # ── Statements ────────────────────────────────────────────────────────

    def parse_stmt(self):
        t = self.current.type
        if t in ('var', 'mut', 'const'):
            self.parse_decl_stmt()
        elif t == 'funcion':
            self.parse_func_decl()
        elif t == 'si':
            self.parse_if_stmt()
        elif t == 'elegir':
            self.parse_switch_stmt()
        elif t == 'para':
            self.parse_for_stmt()
        elif t == 'mientras':
            self.parse_while_stmt()
        elif t == 'hacer':
            self.parse_do_while_stmt()
        elif t == 'intentar':
            self.parse_try_stmt()
        elif t == 'retornar':
            self.parse_return_stmt()
        elif t == 'romper':
            self.parse_break_stmt()
        elif t == 'continuar':
            self.parse_continue_stmt()
        elif t == 'tkn_opening_key':
            self.parse_block()
        elif t == 'tkn_semicolon':
            self.advance()
        else:
            self.parse_expr_stmt()

    def parse_decl_stmt(self):
        self.advance()  # consume var/mut/const
        self.expect('id')
        if self.match('tkn_assign'):
            self.parse_expr()
        self.opt_semi()

    def parse_func_decl(self):
        self.advance()  # funcion
        self.expect('id')
        self.expect('tkn_opening_par')
        self.parse_param_list()
        self.expect('tkn_closing_par')
        self.parse_block()

    def parse_param_list(self):
        if self.check('id'):
            self.advance()
            while self.match('tkn_comma'):
                self.expect('id')

    def parse_block(self):
        self.expect('tkn_opening_key')
        self.parse_stmt_list()
        self.expect('tkn_closing_key')

    def parse_if_stmt(self):
        self.advance()  # si
        self.expect('tkn_opening_par')
        self.parse_expr()
        self.expect('tkn_closing_par')
        self.parse_block_or_stmt()
        if self.match('sino'):
            if self.check('si'):
                self.parse_if_stmt()
            else:
                self.parse_block_or_stmt()

    def parse_block_or_stmt(self):
        if self.check('tkn_opening_key'):
            self.parse_block()
        else:
            self.parse_stmt()

    def parse_switch_stmt(self):
        self.advance()  # elegir
        self.expect('tkn_opening_par')
        self.parse_expr()
        self.expect('tkn_closing_par')
        self.expect('tkn_opening_key')
        while self.check('caso', 'porDefecto'):
            if self.match('caso'):
                self.parse_expr()
                self.expect('tkn_colon')
                self.parse_stmt_list()
            else:
                self.advance()  # porDefecto
                self.expect('tkn_colon')
                self.parse_stmt_list()
        self.expect('tkn_closing_key')

    def parse_while_stmt(self):
        self.advance()  # mientras
        self.expect('tkn_opening_par')
        self.parse_expr()
        self.expect('tkn_closing_par')
        self.parse_block_or_stmt()

    def parse_do_while_stmt(self):
        self.advance()  # hacer
        self.parse_block()
        self.expect('mientras')
        self.expect('tkn_opening_par')
        self.parse_expr()
        self.expect('tkn_closing_par')
        self.opt_semi()

    def parse_for_stmt(self):
        self.advance()  # para
        self.expect('tkn_opening_par')

        t = self.current.type
        if t in ('var', 'mut', 'const'):
            self.advance()  # consume decl keyword
            self.expect('id')
            if self.check('en'):
                # for-in with declaration
                self.advance()  # en
                self.parse_expr()
            else:
                # C-style for with declaration
                if self.match('tkn_assign'):
                    self.parse_expr()
                self.expect('tkn_semicolon')
                if self.current.type in EXPR_FIRST:
                    self.parse_expr()
                self.expect('tkn_semicolon')
                if self.current.type in EXPR_FIRST:
                    self.parse_expr()
        elif t in EXPR_FIRST:
            self.parse_expr()
            if self.check('en'):
                # for-in without declaration
                self.advance()  # en
                self.parse_expr()
            else:
                # C-style for with expr init
                self.expect('tkn_semicolon')
                if self.current.type in EXPR_FIRST:
                    self.parse_expr()
                self.expect('tkn_semicolon')
                if self.current.type in EXPR_FIRST:
                    self.parse_expr()
        else:
            # empty init
            self.expect('tkn_semicolon')
            if self.current.type in EXPR_FIRST:
                self.parse_expr()
            self.expect('tkn_semicolon')
            if self.current.type in EXPR_FIRST:
                self.parse_expr()

        self.expect('tkn_closing_par')
        self.parse_block_or_stmt()

    def parse_try_stmt(self):
        self.advance()  # intentar
        self.parse_block()
        if self.match('capturar'):
            self.expect('tkn_opening_par')
            self.expect('id')
            self.expect('tkn_closing_par')
            self.parse_block()
        if self.match('finalmente'):
            self.parse_block()

    def parse_return_stmt(self):
        self.advance()  # retornar
        if self.current.type in EXPR_FIRST:
            self.parse_expr()
        self.opt_semi()

    def parse_break_stmt(self):
        self.advance()  # romper
        self.opt_semi()

    def parse_continue_stmt(self):
        self.advance()  # continuar
        self.opt_semi()

    def parse_expr_stmt(self):
        self.parse_expr()
        self.opt_semi()

    # ── Expressions ──────────────────────────────────────────────────────

    def parse_expr(self):
        self.parse_assign_expr()

    def parse_assign_expr(self):
        self.parse_cond_expr()
        if self.current.type in ASSIGN_OPS:
            self.advance()
            self.parse_assign_expr()

    def parse_cond_expr(self):
        self.parse_or_expr()
        if self.match('tkn_ternary'):
            self.parse_expr()
            self.expect('tkn_colon')
            self.parse_cond_expr()

    def parse_or_expr(self):
        self.parse_and_expr()
        while self.match('tkn_or'):
            self.parse_and_expr()

    def parse_and_expr(self):
        self.parse_eq_expr()
        while self.match('tkn_and'):
            self.parse_eq_expr()

    def parse_eq_expr(self):
        self.parse_rel_expr()
        while self.check('tkn_equal', 'tkn_neq', 'tkn_strict_equal', 'tkn_strict_neq'):
            self.advance()
            self.parse_rel_expr()

    def parse_rel_expr(self):
        self.parse_add_expr()
        while self.check('tkn_less', 'tkn_greater', 'tkn_leq', 'tkn_geq'):
            self.advance()
            self.parse_add_expr()

    def parse_add_expr(self):
        self.parse_mul_expr()
        while self.check('tkn_plus', 'tkn_minus'):
            self.advance()
            self.parse_mul_expr()

    def parse_mul_expr(self):
        self.parse_unary_expr()
        while self.check('tkn_times', 'tkn_div', 'tkn_mod', 'tkn_power'):
            self.advance()
            self.parse_unary_expr()

    def parse_unary_expr(self):
        if self.check('tkn_not', 'tkn_minus', 'tkn_plus', 'tkn_increment', 'tkn_decrement'):
            self.advance()
            self.parse_unary_expr()
        else:
            self.parse_postfix_expr()

    def parse_postfix_expr(self):
        self.parse_call_expr()
        self.match('tkn_increment', 'tkn_decrement')

    def parse_call_expr(self):
        self.parse_primary()
        self.parse_suffix_list()

    def parse_suffix_list(self):
        while True:
            if self.check('tkn_period'):
                self.advance()
                # accept any token as member name (id or reserved word)
                if self.current.type == 'id' or self.current.type in RESERVED_WORDS:
                    self.advance()
                else:
                    self.error(['id'])
                # optional call after member access
                if self.check('tkn_opening_par'):
                    self.advance()
                    self.parse_arg_list()
                    self.expect('tkn_closing_par')
            elif self.check('tkn_opening_bra'):
                self.advance()
                self.parse_expr()
                self.expect('tkn_closing_bra')
            elif self.check('tkn_opening_par'):
                self.advance()
                self.parse_arg_list()
                self.expect('tkn_closing_par')
            else:
                break

    def _check_expr_end(self, follow_types):
        """After parse_expr returns, verify current token is valid.
        Reports all binary ops + follow_types as expected if not."""
        valid = BINARY_OPS_TYPES | set(follow_types)
        if self.current.type not in valid:
            self.error(list(valid))

    def parse_arg_list(self):
        if self.current.type in EXPR_FIRST:
            self.parse_expr()
            self._check_expr_end(['tkn_comma', 'tkn_closing_par'])
            while self.match('tkn_comma'):
                self.parse_expr()
                self._check_expr_end(['tkn_comma', 'tkn_closing_par'])

    def parse_primary(self):
        t = self.current.type

        # Literals and identifiers
        if t in ('id', 'tkn_num', 'tkn_str',
                 'verdadero', 'falso', 'nulo', 'indefinido', 'Infinito', 'NuN'):
            self.advance()
            return

        # consola MUST be followed by '.' (e.g. consola.escribir(...))
        if t == 'consola':
            self.advance()
            self.expect('tkn_period')
            # consume the method name (id or reserved word)
            if self.current.type == 'id' or self.current.type in RESERVED_WORDS:
                self.advance()
            else:
                self.error(['id'])
            return

        # Other built-in objects usable as expression values
        if t in ('Numero', 'Mate', 'Arreglo', 'Matriz', 'Cadena', 'Booleano', 'Fecha',
                 'afirmar', 'limpiar', 'error', 'agrupar', 'info', 'escribir', 'tabla'):
            self.advance()
            return

        # Grouped expression or arrow function: ( ... )
        if t == 'tkn_opening_par':
            self.advance()
            if not self.check('tkn_closing_par'):
                self.parse_expr()
            self.expect('tkn_closing_par')
            # Arrow function?
            if self.match('tkn_arrow'):
                if self.check('tkn_opening_key'):
                    self.parse_block()
                elif self.current.type in EXPR_FIRST:
                    self.parse_expr()
                else:
                    self.error(['tkn_opening_key'] + list(EXPR_FIRST))
            return

        # Array literal
        if t == 'tkn_opening_bra':
            self.advance()
            if self.current.type in EXPR_FIRST:
                self.parse_expr()
                while self.match('tkn_comma'):
                    if self.current.type in EXPR_FIRST:
                        self.parse_expr()
            self.expect('tkn_closing_bra')
            return

        # Object literal (only inside expressions, never at statement start)
        if t == 'tkn_opening_key':
            self.advance()
            self._parse_object_body()
            self.expect('tkn_closing_key')
            return

        # Function expression
        if t == 'funcion':
            self.advance()
            self.match('id')  # optional name
            self.expect('tkn_opening_par')
            self.parse_param_list()
            self.expect('tkn_closing_par')
            self.parse_block()
            return

        # crear (new)
        if t == 'crear':
            self.advance()
            # constructor name: id or certain class-like reserved words
            if self.current.type in ('id', 'Fecha', 'Arreglo', 'Matriz',
                                      'Numero', 'Cadena', 'Booleano', 'Funcion',
                                      'Promesa'):
                self.advance()
            else:
                self.error(['id'])
            # optional chained .ClassName for things like crear Foo.Bar(...)
            while self.check('tkn_period'):
                self.advance()
                if self.current.type == 'id' or self.current.type in RESERVED_WORDS:
                    self.advance()
                else:
                    self.error(['id'])
            self.expect('tkn_opening_par')
            self.parse_arg_list()
            self.expect('tkn_closing_par')
            return

        # Nothing matched
        expected = sorted(set(
            expected_display(e) for e in [
                'id', 'tkn_num', 'tkn_str',
                'verdadero', 'falso', 'nulo', 'indefinido', 'Infinito', 'NuN',
                'tkn_opening_par', 'tkn_opening_bra', 'tkn_opening_key',
                'funcion', 'crear',
            ]
        ))
        exp_str = ' '.join(f'"{e}"' for e in expected)
        raise ParseError(
            f'<{self.current.line}:{self.current.col}> Error sintactico: '
            f'se encontro: "{found_display(self.current)}"; se esperaba: {exp_str}.'
        )

    def _parse_object_body(self):
        # prop (',' prop)*
        if self._is_prop_key():
            self._parse_prop()
            while self.match('tkn_comma'):
                if self._is_prop_key():
                    self._parse_prop()
                else:
                    break

    def _is_prop_key(self) -> bool:
        t = self.current.type
        return t in ('id', 'tkn_str', 'tkn_num') or t in RESERVED_WORDS

    def _parse_prop(self):
        self.advance()  # key
        if self.match('tkn_colon'):
            self.parse_expr()
        # else shorthand property (just the identifier)

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    source = sys.stdin.buffer.read().decode('utf-8')
    if source.startswith('\ufeff'):
        source = source[1:]
    tokens = tokenize(source)
    parser = Parser(tokens)
    try:
        parser.parse()
        print('El analisis sintactico ha finalizado exitosamente.')
    except ParseError as e:
        print(str(e))

if __name__ == '__main__':
    main()
