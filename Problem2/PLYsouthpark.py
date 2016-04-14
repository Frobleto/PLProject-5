tokens = ('HEADER','WORD','QUOTE','COMMA','INTEGER')
literals = ['"']

# Tokens
t_HEADER = r'^Season,Episode,Character,Line$'
t_WORD   = r'\b[a-zA-Z0-9]+\b'
t_QUOTE  = r'\".*$'
t_COMMA  = r','

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
    '''start : HEADER
             | speaker
             | episode
             | quote
             | empty
    '''
    print 'Saw: ' + str(t[1])

def p_episode(t):
    'episode : INTEGER COMMA INTEGER'
    print 'Season: ' + str(t[1]) + ' Episode: ' + str(t[3])

def p_speaker(t):
    'speaker : COMMA WORD COMMA'
    print "WORKS"
    print str(t[1]) + ': '

def p_quote(t):
    'quote : QUOTE'
    print str(t[1]) + '"'

def p_empty(t):
    'empty : '
    pass

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

# To run the parser, enter the following in a terminal window:
#    cat SouthParkS13E01.out | python PLYsouthpark.py
