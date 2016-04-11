# -----------------------------------------------------------------------------
# simpleGrammar.py
#
# A simple integer grammar -- all in one file.
# -----------------------------------------------------------------------------

# Tokens
tokens = (
    'NUM',
)

t_NUM    = r'[0-9]'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex   # ply.lex comes from the ply folder in the PLY download.
lexer = lex.lex()

# Parsing rules

def p_start(t):
    '''integer : digit
               | integer digit
    '''
    if len(t) == 3:
        print "Recognzed a", t[2], 'in second part of rule'
    else:
        print "Recognzed a", t[1], 'in first part of rule'

def p_digit(t):
    'digit : NUM'
    print "Saw a", t[1]
    t[0] = t[1]

def p_error(t):
    if t != None:
        print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc   # ply.yacc comes from the ply folder in the PLY download.
parser = yacc.yacc()

while True:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    parser.parse(s)