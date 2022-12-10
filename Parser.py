'''
RECURSIVE DECENT ALGORITHM ( RDA )
Used to code out top down parsers, and LL Grammars which have two restrictions:
- Must be pairwise disjoint
- No left hand recursion

<stmt> --> <if_stmt> | <while_stmt> | <as_s> | <block>
<block> --> `{` { <stmt>`;` } `}`
<if_stmt> -->  `ifin` `(`<bool_expr>`)` `{` <stmt> `}` [ `orelse` `{` <stmt> `}`]
<while_loop> -->  `loop``(`<bool_expr>`)` `{` <stmt> `}`
<as_s>  --> `id` `=` <expr>
<expr> --> <term> { (`+`|`-`) <term> }
<term> --> <factor> { (`*`|`\`|`%`) <factor> }
<factor> --> `id` | `int_lit` | `float_lit` | `(` <expr> `)`
<var> -->  [_a-zA-Z]{6,8}
<datatype> --> (XS|S|L|XL)

<bool_expr> --> <band> { `OR` <band> }
<band> --> <beq> { `AND` <beq> }
<beq> --> <brel> { (`!=`|`==`) <brel> }
<brel> --> <expr> { (`<=`|`>=` | `<` | `>`) <expr> }
<expr> --> <term> { (`+`|`-`) <term> }
<term> --> <not> { (`*`|`/`|`%`) <bnot> }
<bnot> -> [!]<factor>
<factor> --> `id` | `int_lit` | `float_lit` | `bool_lit` | `(` <expr> `)`
'''

import re


class RDA:

    def __init__(self, tokens: list()):
        self.current = 0
        self.currentToken = tokens[self.current]

    def getNextToken(self):
        if self.current < len(self.tokens):
            self.current += 1

        self.currentToken = self.tokens[self.current]

    def variableCheck(self):
        # Variable should be between 6-8 characters
        variableName = re.findall("(_a-zA-Z){6,8}")

        if not variableName:
            raise Exception("Invalid Syntax")

    def stmt(self):
        # <stmt> --> <if_stmt> | <while_stmt> | <as_s> | <block>
        match self.currentToken:
            case 'ifin':
                self.if_stmt()
            case 'loop':
                self.while_stmt()
            case 'id':
                self.as_s()
            case '{':
                self.block()
            case _:
                self.error()

    def block(self):
        # <block> --> `{` { <stmt>`;` } `}`

        if self.currentToken == '{':
            self.getNextToken()
            while self.currentToken == 'ifin' or self.currentToken == 'while' or self.currentToken == 'id' or self.currentToken == '{':
                self.stmt()
                if self.currentToken == ';':
                    self.getNextToken()
                else:
                    self.error()

            if self.currentToken == '}':
                self.getNextToken()
            else:
                self.error()
        else:
            self.error()

    def if_stmt(self):
        # <if_stmt> -->  `if``(`<bool_expr>`)` <stmt> [ `else` <stmt> ]
        if self.currentToken == 'ifin':
            self.getNextToken()
            if self.currentToken == '(':
                self.getNextToken()
                self.expr()
                if self.currentToken == ")":
                    self.getNextToken()
                    if self.currentToken == "{":
                        self.getNextToken()
                        self.stmt()
                        if self.getNextToken() == "}":
                            self.getNextToken()
                        else:
                            self.error()
                    else:
                        self.error()
                    if self.currentToken == 'orelse':
                        self.getNextToken()
                        if self.getNextToken() == "{":
                            self.getNextToken()
                            self.stmt()
                        if self.getNextToken() == "}":
                            self.getNextToken()
                        else:
                            self.error()
                    else:
                        self.error()

                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()

    def while_stmt(self):
        # <while_loop> -->  `while``(`<bool_expr>`)` `{` <stmt> `}`
        if self.currentToken == 'loop':
            self.getNextToken()
            if self.currentToken == '(':
                self.getNextToken()
                self.expr()
                if self.currentToken == ')':
                    self.getNextToken()
                    if self.getNextToken() == '{':
                        self.getNextToken()
                        self.stmt()
                        if self.currentToken == '}':
                            self.getNextToken()
                        else:
                            self.error()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()

    def as_s(self):
        # <as_s>  --> `id` `=` <expr>
        if self.currentToken == 'id':
            self.getNextToken()
            if self.currentToken == '=':
                self.getNextToken()
                self.expr()
            else:
                self.error()
        else:
            self.error()

    def expr(self):
        # <expr> --> <term> { (`+`|`-`) <term> }
        self.term()
        while self.currentToken == '+' or self.currentToken == '-':
            self.getNextToken()
            self.term()

    def term(self):
        # <term> --> <not> { (`*`|`/`|`%`) <not> }
        self.bnot()
        while self.currentToken == '*' or self.currentToken == '/' or self.currentToken == '%':
            self.getNextToken()
            self.bnot()

    def factor(self):
        # <factor> --> `id` | `int_lit` | `float_lit` | `(` <expr> `)`
        # FIRST(<factor>) -> {id}{int_lit}{float_lit}{'('}

        if self.currentToken == 'id' or self.currentToken == 'int_lit' or self.currentToken == 'float_lit':
            self.getNextToken()
        elif self.currentToken == '(':
            self.getNextToken()
            self.expr()
            if self.currentToken == ')':
                self.getNextToken()
            else:
                self.error()
        else:
            self.error()

    def error(self):
        print ("This is a syntax error")

    # Boolean part

    def bool_expr(self):

        # < bool_expr > --> < band > {`OR` < band >}
        self.band()
        while self.currentToken == 'OR':
            self.getNextToken()
            self.band()

    def band(self):

        # <band> --> <beq> { `AND` <beq> }

        self.beq()
        while self.currentToken == 'AND':
            self.getNextToken()
            self.beq()

    def beq(self):

        # <beq> --> <brel> { (`!=`|`==`) <brel> }
        self.brel()
        while self.currentToken == '!' | self.currentToken == '==':
            self.getNextToken()
            self.brel()

    def brel(self):

        # <brel> --> <expr> { (`<=`|`>=` | `<` | `>`) <expr> }
        self.expr()
        while self.currentToken == '<=' or self.currentToken == '>=' or self.currentToken == '<' or self.currentToken == '>':
            self.getNextToken()
            self.expr()

    def bnot(self):

        # <bnot> -> [!]<factor>
        if self.currentToken == '!':
            self.getNextToken()
            self.factor()

        self.factor()

    def error(self):
        print("There is an error!")
