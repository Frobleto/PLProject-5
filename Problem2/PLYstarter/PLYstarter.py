""" This will parse the data from the unix command echo "Header1 is this~Header2 and that~~Data 1.0~Data 2.0" | tr "~" "\n"
which is:
Header1 is this
Header2 and that

Data 1.0
Data 2.0
"""

tokens = ('HEADER1', 'HEADER2', 'DATA', 'INTEGER')
literals = ['.',  ]

# Tokens
t_HEADER1  = r'^Header1[ -~]+$'
t_HEADER2  = r'^Header2.*$'
t_DATA     = r'Data'

def t_INTEGER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \r"

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

global time_step
time_step = 0

def p_start(t):
    '''start : HEADER1
             | HEADER2
             | DATA float
    '''
    if len(t) > 2: #This matches the third line in the parser rule, i.e., | DATA float
        print "Saw a ", t[0], ", ", t[1], ", ", t[2], "_~_"

def p_float(t):
    'float : INTEGER "." INTEGER'
    t[0] =  str(t[1]) + str(t[2]) + str(t[3])

def p_error(t):
    if t == None:
        print("Syntax error at '%s'" % t)
    else:
        print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc   # ply.yacc comes from the ply folder in the PLY download.
parser = yacc.yacc()

while True:
    try:
        s = raw_input('')
    except EOFError:
        break
    parser.parse(s)

# To run the parser do the following in a terminal window: echo "Header1 is this~Header2 and that~~Data 1.0~Data 2.0" | tr "~" "\n" | grep -v '^\s*$' | python PLYstarter.py | sed "s/_~_/ which is a float./"
