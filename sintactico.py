import ply.yacc as yacc
from lexico import tokens

def p_body(p):
    '''
    body : instruction SEMICOLON body
         | instruction SEMICOLON
    '''

def p_instruction(p):
    '''
    instruction : functionCall
           | variableDeclaration
    '''

def p_datatype(p):
    '''
    datatype : INT_TYPE
             | DOUBLE_TYPE
             | NUM_TYPE
             | BOOL_TYPE
             | STRING_TYPE
             | LIST_TYPE
             | MAP_TYPE
             | SET_TYPE
             | RUNES_TYPE
             | SYMBOL_TYPE
    '''

def p_variableDeclaration(p):
    '''
    variableDeclaration : datatype VARIABLE ASSIGN value
                        | datatype VARIABLE ASSIGN functionCall
    '''

def p_functionCall(p):
    '''
    functionCall : prototype
                 | object DOT prototype
    '''

def p_values(p):
    '''
    values : value COMMA values
           | value
    '''

def p_prototype(p):
    '''
    prototype : FUNC_START values RPAREN
              | FUNC_START RPAREN
    '''

def p_object(p):
    '''
    object : NEW prototype
    '''


def p_number(p):
    '''
    number : INTEGER
           | DOUBLE
    '''

def p_arithmeticOperator(p):
    '''
    arithmeticOperator : PLUS
                       | MINUS
                       | TIMES
                       | DIVIDE
    '''

def p_value(p):
    '''
    value : number
          | object
          | arithmeticExpression
          | STRING
          | VARIABLE
          | BOOLEAN
    '''

def p_arithmeticExpression(p):
    '''
    arithmeticExpression : value arithmeticOperator value
                         | LPAREN value arithmeticOperator value RPAREN
    '''

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('lp > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)