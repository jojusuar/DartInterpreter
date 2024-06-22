import ply.yacc as yacc
from lexico import tokens

def p_body(p):
    '''
    body : instruction SEMICOLON body
         | instruction SEMICOLON
         | noSemicolonStructure body
         | noSemicolonStructure
    '''

def p_noSemicolonStructure(p):
    '''
    noSemicolonStructure : dataStructure
                         | functionDeclaration
    '''

def p_dataStructure(p):
    '''
    dataStructure : if
    '''

def p_if(p): # se irán agregando las demás
    '''
    if : IF LPAREN value RPAREN LBRACE body RBRACE
    '''

def p_import(p):
    '''
    import : IMPORT STRING
    '''

def p_instruction(p):
    '''
    instruction : functionCall
                | variableDeclarationUninitialized
                | variableDeclarationInitialized
                | variableMutation
                | import
    '''

def p_non_nullable_datatype(p):
    '''
    non_nullable_datatype : INT_TYPE
             | DOUBLE_TYPE
             | NUM_TYPE
             | BOOL_TYPE
             | STRING_TYPE
             | LIST_TYPE
             | MAP_TYPE
             | SET_TYPE
             | RUNES_TYPE
             | SYMBOL_TYPE
             | VAR_TYPE
    '''

def p_nullable_datatype(p):
    '''
    nullable_datatype : non_nullable_datatype ACCEPT_NULL
    '''

def p_datatype(p):
    '''
    datatype : nullable_datatype
             | non_nullable_datatype
             | recordTypes
    '''

def p_variableDeclarationUninitialized(p):
    '''
    variableDeclarationUninitialized : datatype VARIABLE
    '''

def p_variableInitialization(p):
    '''
    variableInitialization : ASSIGN value
                           | ASSIGN functionCall
    '''

def p_variableDeclarationInitialized(p):
    '''
    variableDeclarationInitialized : variableDeclarationUninitialized variableInitialization
    '''

def p_immediateAssign(p):
    '''
    immediateAssign : SUM_ASSIGN
                    | SUB_ASSIGN
                    | MUL_ASSIGN
                    | DIV_ASSIGN
                    | MOD_ASSIGN
                    | AND_ASSIGN
                    | OR_ASSIGN
                    | XOR_ASSIGN
                    | LSHIFT_ASSIGN
                    | RSHIFT_ASSIGN
                    | RUNSIGNED_SHIFT_ASSIGN
    '''

def p_variableMutation(p):
    '''
    variableMutation : VARIABLE variableInitialization
                     | VARIABLE immediateAssign value
    '''

def p_functionCall(p): # engloba a print() y a stdin.readLineSync()
    '''
    functionCall : prototype    
                 | VARIABLE DOT prototype
    '''

def p_functionDeclaration(p):
    '''
    functionDeclaration : datatype VARIABLE LPAREN parameters RPAREN LBRACE body RBRACE
    '''

def p_parameters(p):
    '''
    parameters : datatype VARIABLE COMMA parameters
               | datatype VARIABLE
    '''

def p_values(p):
    '''
    values : value COMMA values
           | value
    '''

def p_prototype(p):
    '''
    prototype : VARIABLE LPAREN values RPAREN
              | VARIABLE LPAREN RPAREN
    '''

def p_object(p):
    '''
    object : NEW prototype
    '''

def p_boolean(p):
    '''
    boolean : TRUE
            | FALSE
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
                       | MOD
    '''

def p_logicOperator(p):
    '''
    logicOperator : LOGICAL_AND
                  | LOGICAL_OR
    '''

def p_bitwiseOperator(p):
    '''
    bitwiseOperator : BITWISE_AND
                    | BITWISE_OR
                    | BITWISE_XOR
    '''

def p_comparator(p):
    '''
    comparator : EQUALS
               | LESS_THAN
               | MORE_THAN
               | LESS_EQUAL
               | MORE_EQUAL
    '''

def p_value(p):
    '''
    value : number
          | MINUS number
          | object
          | arithmeticExpression
          | MINUS LPAREN arithmeticExpression RPAREN
          | bitwiseExpression
          | MINUS LPAREN bitwiseExpression RPAREN
          | logicExpression
          | NOT LPAREN logicExpression RPAREN
          | STRING
          | VARIABLE
          | NOT VARIABLE
          | boolean
          | NOT boolean
          | variableValuePair
          | tuple
          | comparison
          | NOT LPAREN comparison RPAREN
    '''

def p_comparison(p):
    '''
    comparison : value comparator value
               | LPAREN value comparator value RPAREN
    '''

def p_logicExpression(p):
    '''
    logicExpression : value logicOperator value
                    | LPAREN value logicOperator value RPAREN
    '''

def p_arithmeticExpression(p):
    '''
    arithmeticExpression : value arithmeticOperator value
                         | LPAREN value arithmeticOperator value RPAREN
    '''

def p_bitwiseExpression(p):
    '''
    bitwiseExpression : value bitwiseOperator value
                      | LPAREN value bitwiseOperator value RPAREN
    '''

def p_recordTypes(p): # estructura de datos de Jose Julio Suarez
    '''
    recordTypes : LPAREN multipleDatatypes RPAREN
                | LPAREN parameters RPAREN
                | LPAREN LBRACE recordTypeAnnotation RBRACE RPAREN
    '''

def p_recordTypeAnnotation(p):
    '''
    recordTypeAnnotation : datatype VARIABLE COMMA recordTypeAnnotation
                         | datatype VARIABLE
    '''

def p_multipleDatatypes(p):
    '''
    multipleDatatypes : datatype COMMA multipleDatatypes
                      | datatype
    '''

def p_variableValuePair(p):
    '''
    variableValuePair : VARIABLE COLON value
    '''

def p_tuple(p):
    '''
    tuple : LPAREN values RPAREN
    '''

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

def interactiveTest(): 
    while True:
        try:
            s = input('lp > ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print(result)

interactiveTest()