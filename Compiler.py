import ply.lex as lex
import ply.yacc as yacc
import sys

# Global error flag for when errors are encountered when parsing
g_error = 0

# ------- Here I write my lexing rules ---------

""" Hear we created a token list filled with tokens.
By creating this list, we are telling lex that these token are valid."""
tokens = [
    "NUM",
    "COMMA",
    "LEFT_BRACKET",  # [brackets]
    "RIGHT_BRACKET",
    "LEFT_BRACES",  # {braces}
    "RIGHT_BRACES",
    "COLON",
    "STRING",
    "TRUE",
    "FALSE",
    "NULL"

]

# -------- Next I write my specification of each token --------

"""We use regular expression to define each token."""
t_COMMA = r","
t_COLON = r":"
t_LEFT_BRACKET = r"\["
t_RIGHT_BRACKET = r"\]"
t_LEFT_BRACES = r"\{"
t_RIGHT_BRACES = r"\}"
t_TRUE = r"true"
t_FALSE = r"false"
t_NULL = r"null"

t_ignore = " \t\n"

""" Strings are made up of zero or more Any unicode character (except " or \), has a double quote (") 
    at the start and at the end. In string we can use backslash(\) which is also known as escape 
    character. So backslash with ", \, /, b, f, n, r, t or (u plus 4 hexadecimal digits)
    """


def t_STRING(t):
    r'\"([^\\"]|(\\(("|\\|\/|b|f|n|r|t)|u[0-9A-Fa-f]{4})))*"'
    return t


""" Number can be int, float or exponential """


def t_NUM(t):
    r"-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?"
    return t


""" If you get an error, it prints out the illegal character and skip a token """


def t_error(t):
    print("You have an error, Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)  # Skips one token onwards


# ----- End lexing rules ------
lexer = lex.lex()

# This commented out code was used to view the token that is created

# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)


# ------ Next I write my Parsing rules -------

"""JSON is built on two data structure, which are array and object"""


def p_json(p):
    """json : array
            | object"""


""" Array is wrapped in brackets. Inside an array there can be zero or more values (which I explain bellow)."""


def p_array(p):
    """array : LEFT_BRACKET valuelist RIGHT_BRACKET"""


def p_valuelist(p):
    '''valuelist : valuelist COMMA value
	             | value
	             | empty
	            '''


"""Object is wrapped in braces. Inside an object there can be zero or more pair of key and value (which I explain bellow) """


def p_object(p):
    """object : LEFT_BRACES middle_section RIGHT_BRACES"""


"""Middle section can be empty or have one pair or multiple pair seperated by a comma"""


def p_middle_section(p):
    """middle_section : middle_section COMMA pair
                      | pair
                      | empty"""


"""Key, value pair. A key has to always be a string and the value can be anythings from p_value (Which I stated below)"""


def p_pair(p):
    """pair : STRING COLON value"""


def p_value(p):
    """value : STRING
             | NUM
             | array
             | object
             | TRUE
             | FALSE
             | NULL
             """


"""Handle empty productions """


def p_empty(p):
    "empty :  "


# Error rule
def p_error(p):
    raise SyntaxError(p)


# --- End parsing rules ---


# Leave this here; this generates a parser from the above rules
parser = yacc.yacc()

# Main function:
in_text = ""
# If a filename has been specified, we parse it and report success/failure
if len(sys.argv) == 2:
    file = open(sys.argv[1]).read()
    in_text = file

# Otherwise, take input from the user
else:
    while 1:
        line = input("Input text: ")
        if line:
            line += "\n"
            in_text += line
        else:
            break

try:
    result = parser.parse(in_text)
except SyntaxError:
    print("Error: input is not properly formatted JSON")
    sys.exit(0)
print("Success: parsed input")
