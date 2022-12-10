## Question 5: Denotational Semantics for selection statement
```commandline
M_if (iffy(<bool_expr>) <stmt>, s) -->
    if M_b (<bool_expr>, s) == error
        return error;
    if M_b (<bool_expr>, s)
        if M_stmt (<stmt>, s) == error
            return error;
        return M_stmt (<stmt>, s)

M_if (iffy(<bool_expr>) <stmt1> else <stmt2>, s) -->
    if M_b (<bool_expr>, s) == error
        return error;
    if M_b (<bool_expr>, s)
        if M_stmt (<stmt1>, s) == error
            return error;
        return M_stmt (<stmt2>, s)
    else
        if M_stmt (<stmt2>, s) == eror
            return error;
        return M_stmt (<stmt2>, s)
```

## Question 6: Denotational Semantics for loop statement
```commandline
M_while (loop(<bool_expr>) <stmt>, s) -->
    if M_b (<bool_expr>, s) == error
        return error;
    if M_b (<bool_expr>, s)
        if M_stmt (<stmt>, s) == error
            return error;
        return M_stmt (<stmt>, s)
```

## Question 7: Denotational Semantics for Expr statement
```commandline
M_expression (<term> { (+|-) <term>, s) -->
    if M_expr ((+ | -), s) == error
        return error;
    if M_expr((+| -), s)
        if M_term (<term>, s) == error
            return error;
        return (<term>, s)
```

## Question 8: Denotational Semantics for Expr statement with boolean solution
```commandline
M _booleanExpr (<band> { `OR` <band> }) -->
    if M_boolexpr (<band>, s) == error
        return error;
    if M_boolexpr (<band>, s)
        return M_boolexpr (<band>, s)
    elif M_boolexpr ('OR', s) == error
        return error;
    elif M_boolexpr ('OR', s)
        if M_boolexpr (<band>, s) == error
            return error
        return M_boolexpr (<band>, s)
    else
        return error
```

## Question 9: Attribute grammar for Assignment statements
```commandline
Assigment --> Identifier '=' Expression

Expression --> Expression '+' Expression
Expression --> Expressiom '*' Natural
Expression --> String
Expression --> Identifier
Expression --> Natural '%' Natural
Expression --> Natural '/' Natural
Expression --> Natural
Expression --> Real
Expression --> Bool
Expression --> Char

Natural --> [0-9]+
Real --> [0-9]+ '.' [0-9]+
Bool --> 'True' | 'False'
Char --> "'" [a-zA-Z0-9] "'"
String --> '"' [a-zA-Z0-9]* '"'
identifier --> [a-zA-Z]+
```

## Question 10: Examples for three syntactically valid assignment statements
    
    1. Syntactically valid, fails semantic rule: a = b + c / 0
    2. Syntactically valid, passes semantic rule: a = b + c / 2
    3. Syntactically valid, fails semantic rule: a = "hello" * -1

    1. This statement is true according to syntax but is dividing the expression with 0 which is failing the sematic rules.
    2. This statement is true according to syntax and is also valid semantically
    3. This statement is true according to syntax but you can only multiply a string with natural number. Therefore it is failing the semantic rules.

## Question 11: 

    Axiomatic Semantics (Weakest pre-conditions)
    (a) a = 2 * (b - 1) - 1 {a > 0}

            (2 * (b - 1) - 1 > 0)
        --> (2 * (b - 1) > 1)
        --> (b - 1 > 1 / 2)
        --> (b > 1 / 2 + 1)
        --> (b > 3 / 2)
        --> (b >= 2)       -----------------> weakest precondition for b

    (b) if (x < y)
        x = x + 1
        else
        x = 3 * x
        {x < 0}

            (x + 1 < 0) | (3 * x < 0)
        --> (x < -1) | (x < 0)
        --> From both of those above inequalisties weakest preconditon is
        --> (x < -1)       -----------------> weakest precondition for x

    (c) y = a * 2 * (b - 1) - 1
        if (x < y)
        x = y + 1
        else
        x = 3 * x
        {x < 0}
        
            3 * x < 0
        --> (x < 0)        -----------------> weakest precondition for x
            
            y + 1 < 0
        --> y < -1         -----------------> weakest precondition for y

            a * 2 * (b - 1) - 1 < -1
        --> a * 2 * (b - 1) < 0
        --> b - 1 < 0
        --> b < 1          -----------------> weakest precondition for b

            a * 2 * (b - 1) - 1 < -1
        --> a * 2 * (b - 1) < 0
        --> a < 0          -----------------> weakest precondition for a


    (d) a = 3 * (2 * b + a);
        b = 2 * a - 1
        {b > 5)

            b = 2 * a - 1
        --> 2 * a - 1 > 5
        --> 2 * a > 6
        --> a > 3          -----------------> weakest precondition for a

            a = 3 * (2 * b + a)
        --> a = 6 * b + 3 * a
        --> 2 * a = -6 * b
        --> a = -3 * b
        --> From above pre condition
        --> -3 * b > 3
        --> -b > 1
        --> b < -1         -----------------> weakest precondition for b