class Token:
    def __int__(self, code: int, lexeme: str):
        self.code = code
        self.lexeme = lexeme

tokenList = {
        'id',
        'iffy',
        'loop',
        '+',
        '-',
        '*',
        '/',
        '%',
        '>',
        '<',
        '>=',
        '<=',
        '=',
        '!=',
        '{',
        '}',
        'int_lit',
        'float_lit',
        '|',
        '&',
        'bool_lit'
        ','
}


class Compiler:
    def __init__(self):
        self.lexer = Lexer()

    def fileInput(self, input_file):
        with open(input_file, 'r') as f:
            input_str = f.read()
        tokens = self.lexer(input_str)


class Lexer:
    def __init__(self, string: object) -> object:
        self.string = string
        self.pos = 0
        self.current_char = self.string[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.string):
            self.current_char = None
        else:
            self.current_char = self.string[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # Real Literals
    def get_real_literal(self):
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return Token(result)

    # Natural Literals
    def get_natural_literal(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(result)

    # Boolean Literals
    def get_bool_literal(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        if result.lower() in ['true', 'false']:
            return Token(result)
        raise Exception('Invalid bool literal')

    # Character Literal
    def get_char_literal(self):
        if self.current_char is None or self.current_char != "'":
            raise Exception('Invalid char literal')
        self.advance()
        result = ''
        while self.current_char is not None and self.current_char != "'":
            result += self.current_char
            self.advance()
        if self.current_char is None:
            raise Exception('Unterminated char literal')
        self.advance()
        return Token(result)

    # String Literals
    def get_string_literal(self):
        if self.current_char is None or self.current_char != '"':
            raise Exception('Invalid string literal')
        self.advance()
        result = ''
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\\':
                self.advance()
                if self.current_char is None:
                    raise Exception('Unterminated string literal')
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 'r':
                    result += '\r'
                elif self.current_char == 't':
                    result += '\t'
                else:
                    result += self.current_char
            else:
                result += self.current_char
            self.advance()
        if self.current_char is None:
            raise Exception('Unterminated string literal')
        self.advance()
        return Token(result)

    # Special Symbol Declarations
    def get_special_symbol(self):
        if self.current_char is None:
            raise Exception('Invalid special symbol')
        if self.current_char == '+':
            self.advance()
            return Token('addition')
        elif self.current_char == '-':
            self.advance()
            return Token('subtraction')
        elif self.current_char == '*':
            self.advance()
            return Token('multiplication')
        elif self.current_char == '/':
            self.advance()
            return Token('division')
        elif self.current_char == '^':
            self.advance()
            return Token('exponentiation')
        elif self.current_char == '(':
            self.advance()
            return Token('break_order_of_operations')
        elif self.current_char == ')':
            self.advance()
            return Token('break_order_of_operations')
        elif self.current_char == '>':
            self.advance()
            if self.current_char == '=':
                self.advance()
                return Token('greater_than_or_equal_to')
            else:
                return Token('greater_than')

        elif self.current_char == '<':
            self.advance()
            if self.current_char == '=':
                self.advance()
                return Token('lesser_than_or_equal_to')
            else:
                return Token('lesser_than')

        elif self.current_char == '=':
            self.advance()
            if self.current_char == '!':
                self.advance()
                return Token('not_equal')
            else:
                return Token('equal_to')

        elif self.current_char == '&':
            self.advance()
            return Token('logical_NOT')

        elif self.current_char == '|':
            self.advance()
            return Token('logical_OR')

        elif self.current_char == ',':
            self.advance()
            return Token('parameter_seperator')