import ply.yacc as yacc
import datetime
import logging
import os
import numbers
from lexico import tokens

variables = {}

log = logging.getLogger('syntax')
semanticLog = logging.getLogger('semantic')

def p_body(p):
    '''
    body : instruction SEMICOLON body
         | instruction SEMICOLON
         | noSemicolonStructure body
         | noSemicolonStructure
    '''

def p_noSemicolonStructure(p):
    '''
    noSemicolonStructure : controlStructure
                         | functionDeclaration
                         | classDeclaration
    '''

def p_controlStructure(p):
    '''
    controlStructure : if
                     | for
                     | while
                     | switch
    '''

def p_condition(p): 
    '''
    condition : IF LPAREN value RPAREN LBRACE body RBRACE
    '''

def p_if(p):
    '''
    if : condition ELSE if
       | condition ELSE LBRACE body RBRACE
       | condition
    '''

def p_for(p):
    '''
    for : FOR LPAREN variableDeclarationInitialized SEMICOLON value SEMICOLON variableMutation RPAREN LBRACE body RBRACE
        | FOR LPAREN variableMutation SEMICOLON value SEMICOLON variableMutation RPAREN LBRACE body RBRACE
        | FOR LPAREN VARIABLE SEMICOLON value SEMICOLON variableMutation RPAREN LBRACE body RBRACE
    '''

def p_while(p):
    '''
    while : WHILE LPAREN value RPAREN LBRACE body RBRACE
    '''

def p_switch(p):
    '''
    switch : SWITCH LPAREN value RPAREN LBRACE multipleCases RBRACE
    '''

def p_multipleCases(p):
    '''
    multipleCases : case multipleCases
                  | case DEFAULT COLON LBRACE body RBRACE
                  | case DEFAULT COLON instruction SEMICOLON
                  | case
    '''

def p_case(p):
    '''
    case : CASE value COLON LBRACE body RBRACE
         | CASE value COLON instruction SEMICOLON
    '''

def p_import(p):
    '''
    import : IMPORT string
    '''

def p_instruction(p):
    '''
    instruction : functionCall
                | variableDeclarationUninitialized
                | variableDeclarationInitialized
                | variableDeclarationAS
                | variableMutation
                | import
                | return
                | BREAK
    '''

def p_classDeclaration(p):
    '''
    classDeclaration : CLASS VARIABLE LBRACE classBody RBRACE
                     | ABSTRACT CLASS VARIABLE LBRACE classBody RBRACE
                     | CLASS VARIABLE EXTENDS VARIABLE LBRACE classBody RBRACE
    '''

def p_classBody(p):
    '''
    classBody : classMember classBody
              | classMember
    '''

def p_classMember(p):
    '''
    classMember : functionDeclaration
                | variableDeclarationUninitialized SEMICOLON
                | variableDeclarationInitialized SEMICOLON
                | variableDeclarationAS SEMICOLON
                | variableMutation SEMICOLON
                | constructorDeclaration
                | controlStructure
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
             | VARIABLE
    '''
    if p[1] == 'int':
        p[0] = int
    elif p[1] == 'double':
        p[0] = numbers.Number
    elif p[1] == 'bool':
        p[0] = bool
    elif p[1] == 'String':
        p[0] = str
    elif p[1] == 'List':
        p[0] = list
    elif p[1] == 'Map':
        p[0] = dict
    elif p[1] == 'Set':
        p[0] = set
    elif p[1] == 'Runes':
        pass # No hay análogo en Python
    elif p[1] == 'Symbol':
        pass # No hay análogo en Python
    elif p[1] == 'var':
        pass


def p_nullable_datatype(p):
    '''
    nullable_datatype : non_nullable_datatype ACCEPT_NULL
    '''
    p[0] = p[1] # todos los tipos de Python aceptan None, así que no se puede implementar un análogo directamente

def p_datatype(p):
    '''
    datatype : nullable_datatype
             | non_nullable_datatype
             | VOID
             | recordTypes
             | dataStructureTypes
    '''
    p[0] = p[1]

def p_variableDeclarationUninitialized(p):
    '''
    variableDeclarationUninitialized : datatype VARIABLE
    '''
    if not variables.get(p[2]): 
        variables[p[2]] = [p[1], None] # Vamos a guardar las variables como pares de tipo y valor
        p[0] = p[2]
    else:
        semanticLog.debug(f'Error semántico, la variable {p[1]} {p[2]} ya ha sido declarada.')

def p_variableInitialization(p):
    '''
    variableInitialization : ASSIGN value
    '''
    p[0] = p[2]

def p_variableDeclarationInitialized(p):
    '''
    variableDeclarationInitialized : variableDeclarationUninitialized variableInitialization
    '''
     # Regla por José Julio Suárez, verifica que el valor que inicializa a una variable sea del tipo declarado
    if  variables.get(p[1]):
        if (variables[p[1]][0] != None) and isinstance(p[2], variables[p[1]][0]):
            variables[p[1]] = [variables[p[1]][0], p[2]]
        else:
            semanticLog.debug(f'Error semántico, la variable {p[1]} esperaba un valor de tipo {variables[p[1]][0]} y recibió {type(p[2])}')
    else:
        semanticLog.debug(f'Error semántico, la variable {p[1]} no ha sido declarada')

def p_variableDeclarationAS(p):
    '''
    variableDeclarationAS : variableDeclarationInitialized AS datatype
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
    p[0] = p[1]

def p_immediateMutate(p):
    '''
    immediateMutate : PLUS PLUS
                    | MINUS MINUS
    '''
    if p[1] == '+':
        p[0] = '++'
    else:
        p[0] = '--'

def p_variableMutation(p):
    '''
    variableMutation : VARIABLE variableInitialization
                     | VARIABLE immediateAssign value
                     | VARIABLE immediateMutate
                     | THIS DOT VARIABLE variableInitialization
                     | THIS DOT VARIABLE immediateAssign value
                     | THIS DOT VARIABLE immediateMutate
    '''
    # Regla por José Julio Suárez, verifica que las variables reciban valores del mismo tipo que el declarado
    if variables.get(p[1]) and (variables[p[1]][0] != None):
        if p[2] == '++':
            if isinstance(variables[p[1]][1], numbers.Number):
                variables[p[1]] = [variables[p[1]][0], variables[p[1]][1] + 1]
            else:
                semanticLog.debug(f'Error semántico, el operador {p[2]} esperaba una variable de tipo {numbers.Number} y recibió {type(variables[p[1]][1])}')
        elif p[2] == '--'  and isinstance(variables[p[1]][1], numbers.Number):
            if isinstance(variables[p[1]][1], numbers.Number):
                variables[p[1]] = [variables[p[1]][0], variables[p[1]][1] - 1]
            else:
                semanticLog.debug(f'Error semántico, el operador {p[2]} esperaba una variable de tipo {numbers.Number} y recibió {type(variables[p[1]][1])}')
        elif p[2] == '+=':
            if (isinstance(p[3], numbers.Number) or isinstance(p[3], str)) and isinstance(p[3], variables[p[1]][0]):
                variables[p[1]] = [variables[p[1]][0], variables[p[1]][1] + p[3]]
            else:
                semanticLog.debug(f'Error semántico, la variable {p[1]} esperaba un valor de tipo {variables[p[1]][0]} y recibió {type(p[3])}')
        elif p[2] == '-=':
            if isinstance(p[3], numbers.Number) and issubclass(variables[p[1]][0], numbers.Number):
                variables[p[1]] = [variables[p[1]][0], variables[p[1]][1] - p[3]]
            else:
                semanticLog.debug(f'Error semántico, el operador -= solo maneja tipos numéricos')
        elif p[1] == 'this':
            # Manejo de variables de instancia
            pass
        else:
            if isinstance(p[2], variables[p[1]][0]):
                variables[p[1]] = [variables[p[1]][0], p[2]]
            else:
                semanticLog.debug(f'Error semántico, la variable {p[1]} esperaba un valor de tipo {variables[p[1]][0]} y recibió {type(p[2])}')
    else: 
        semanticLog.debug(f'Error semántico, la variable {p[1]} no ha sido declarada')

def p_functionCall(p): # engloba a print() y a stdin.readLineSync()
    '''
    functionCall : VARIABLE DOT consecutiveCalls  
                 | consecutiveCalls
    '''

def p_consecutiveCalls(p):
    '''
    consecutiveCalls : prototype DOT consecutiveCalls
                     | prototype
    '''

def p_functionDeclaration(p):
    '''
    functionDeclaration : datatype VARIABLE LPAREN parameters RPAREN LBRACE body RBRACE
                        | datatype VARIABLE LPAREN RPAREN LBRACE body RBRACE
    '''

def p_return(p):
    '''
    return : RETURN value
           | RETURN
    '''

def p_constructorDeclaration(p):
    '''
    constructorDeclaration : VARIABLE LPAREN RPAREN LBRACE body RBRACE
                           | VARIABLE LPAREN parameters RPAREN LBRACE body RBRACE
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
    p[0] = p[1]

def p_number(p):
    '''
    number : INTEGER
           | DOUBLE
    '''
    p[0] = p[1]
    
def p_string(p):
    '''
    string : STRING
    '''
    p[0] = p[1]

def p_arithmeticOperator(p):
    '''
    arithmeticOperator : PLUS
                       | MINUS
                       | TIMES
                       | DIVIDE
                       | MOD
    '''
    p[0] = p[1]

def p_logicOperator(p):
    '''
    logicOperator : LOGICAL_AND
                  | LOGICAL_OR
    '''
    p[0] = p[1]

def p_bitwiseOperator(p):
    '''
    bitwiseOperator : BITWISE_AND
                    | BITWISE_OR
                    | BITWISE_XOR
    '''
    p[0] = p[1]

def p_bitShiftOperator(p):
    '''
    bitShiftOperator : LESS_THAN LESS_THAN
                     | MORE_THAN MORE_THAN
                     | LESS_THAN LESS_THAN LESS_THAN
                     | MORE_THAN MORE_THAN MORE_THAN
    '''
    if len(p) == 3:
        if p[1] == '>':
            p[0] = '>>'
        elif p[1] == '<':
            p[0] = '<<'
    elif len(p) == 4:
        if p[1] == '>':
            p[0] = '>>>'
        elif p[1] == '<':
            p[0] = '<<<'


def p_comparator(p):
    '''
    comparator : EQUALS
               | LESS_THAN
               | MORE_THAN
               | LESS_EQUAL
               | MORE_EQUAL
    '''
    p[0] = p[1]

def p_staticValue(p):
    '''
    staticValue : number
                | MINUS number
                | object
                | arithmeticExpression
                | MINUS LPAREN arithmeticExpression RPAREN
                | bitwiseExpression
                | MINUS LPAREN bitwiseExpression RPAREN
                | logicExpression
                | NOT LPAREN logicExpression RPAREN
                | string
                | VARIABLE
                | NOT VARIABLE
                | boolean
                | NOT boolean
                | variableValuePair
                | tuple
                | list
                | comparison
                | NOT LPAREN comparison RPAREN
                | bitShift
                | NULL
    '''
    # Regla de José Julio Suárez. NO TOPAR SIN CUIDADO, un cambio aquí tumba todas las otras reglas semánticas
    if p[1] == 'true':
        p[0] = True
        return
    elif p[1] == 'false':
        p[0] = False
        return
    elif variables.get(p[1]):
        p[0] = variables[p[1]][1] # Si el símbolo es encontrado en la tabla de variables, es una variable!
        return
    elif isinstance(p[1], str) and not (p[1][0] == '"' or p[1][0] == '\''): # si no está en la tabla y no es un string, es una variable sin declarar
        semanticLog.debug(f'Error semántico, la variable {p[1]} no ha sido declarada')
        return 

    if p[1] == '-':
        if p[2] == '(':
            p[0] = -p[3]
        else:
            p[0] = -p[2]
    else:
        p[0] = p[1]
    

def p_value(p):
    '''
    value : staticValue
          | functionCall
          | attributeValue
    '''
    p[0] = p[1]

def p_attributeValue(p):
    '''
    attributeValue : VARIABLE DOT consecutiveAttributeCalls
                   | VARIABLE consecutiveElementCalls
    '''

def p_consecutiveAttributeCalls(p):
    '''
    consecutiveAttributeCalls : DOLLAR INTEGER DOT consecutiveAttributeCalls
                              | DOLLAR INTEGER
                              
    '''

def p_consecutiveElementCalls(p):
    '''
    consecutiveElementCalls : LBRACKET INTEGER RBRACKET consecutiveElementCalls
                            | LBRACKET INTEGER RBRACKET
    '''

def p_comparison(p):
    '''
    comparison : value comparator value
               | LPAREN value comparator value RPAREN
    '''
    if len(p) == 4:
        value1 = p[1]
        operator = p[2]
        value2 = p[3]
    elif len(p) == 6:
        value1 = p[2]
        operator = p[3]
        value2 = p[4]
    
    if type(value1) == type(value2):
        if operator == '==':
             p[0] = (value1 == value2)
        elif isinstance(value1, str) or (isinstance(value1, numbers.Number) and not isinstance(value1, bool)):
            if operator == '<':
                p[0] = value1 < value2
            if operator == '<=':
                p[0] = value1 <= value2
            if operator == '>':
                p[0] = value1 > value2
            if operator == '>=':
                p[0] = value1 >= value2
        else:
            semanticLog.debug(f'Error semántico: La operación intentada no es permitida entre tipos {type(value1)}')
    else:
        semanticLog.debug(f'Error semántico: no se puede comparar un tipo {type(value1)} con un tipo {type(value2)}')


def p_bitShift(p):
    '''
    bitShift : value bitShiftOperator value
             | LPAREN value bitShiftOperator value RPAREN
    '''
    # Regla de José Julio Suárez: verifica que las operaciones de bitShift solo se hagan entre números enteros
    if len(p) == 4:
        if isinstance(p[1], int) and isinstance(p[3], int):
            if p[2] == '<<' or p[2] == '<<<':
                p[0] = p[1] << p[3]
            elif p[2] == '>>' or p[2] == '>>>':
                p[0] = p[1] >> p[3]

        if isinstance(p[1], int):
            pass
        else:
            semanticLog.debug(f'Error semántico, {p[1]} no es de tipo int')

        if isinstance(p[3], int):
            pass
        else:
            semanticLog.debug(f'Error semántico, {p[3]} no es de tipo int')
    
    elif len(p) == 6:
        if isinstance(p[2], int) and isinstance(p[4], int):
            if p[3] == '>>' or p[3] == '>>>':
                p[0] = p[2] >> p[4]
            elif p[3] == '<<' or p[3] == '<<<':
                p[0] = p[2] << p[4]

        if isinstance(p[2], int):
            pass
        else:
            semanticLog.debug(f'Error semántico, {p[2]} no es de tipo int')

        if isinstance(p[4], int):
            pass
        else:
            semanticLog.debug(f'Error semántico, {p[4]} no es de tipo int')

def p_logicExpression(p):
    '''
    logicExpression : value logicOperator value
                    | LPAREN value logicOperator value RPAREN
    '''
    # Regla de Néstor Arias
    if len(p) == 4:
        value1 = p[1]
        op = p[2]
        value2 = p[3]
    else:
        value1 = p[2]
        op = p[3]
        value2 = p[4]

    if isinstance(value1, bool) and isinstance(value2, bool):
        if op == '&&':
            p[0] = value1 and value2
        elif op == '||':
            p[0] = value1 or value2
        else:
            semanticLog.debug(f'Error Semantico: operador {op} no es válido')
    else:
        semanticLog.debug(f'Error Semantico: Los valores ingresados no son los esperados ({value1}, {value2})')
    

def p_arithmeticExpression(p):
    '''
    arithmeticExpression : value arithmeticOperator value
                         | LPAREN value arithmeticOperator value RPAREN
    '''
    # Regla de José Julio Suárez, verifica las operaciones numéricas y la concatenación de Strings
    if len(p) == 4:
        if isinstance(p[1], (int, float, complex)) and isinstance(p[3], (int, float, complex)):
            if p[2] == '+':
                p[0] = p[1] + p[3]
            elif p[2] == '-':
                p[0] = p[1] - p[3]
            elif p[2] == '*':
                p[0] = p[1] * p[3]
            elif p[2] == '/':
                p[0] = p[1] / p[3]
        elif isinstance(p[1], str) and isinstance(p[3], str):
            if p[2] == '+':
                p[0] = p[1][:-1] + p[3][1:]
            else:
                semanticLog.debug(f'El operador {p[2]} no espera cadenas')
        else:
            semanticLog.debug(f'Error semántico, {p[1]} es de tipo {type(p[1])} mientras {p[3]} es de tipo {type(p[3])}')
    
    elif len(p) == 6:
        if isinstance(p[2], (int, float, complex)) and isinstance(p[4], (int, float, complex)):
            if p[3] == '+':
                p[0] = p[2] + p[4]
            elif p[3] == '-':
                p[0] = p[2] - p[4]
            elif p[3] == '*':
                p[0] = p[2] * p[4]
            elif p[3] == '/':
                p[0] = p[2] / p[4]
        elif isinstance(p[2], str) and isinstance(p[4], str):
            if p[3] == '+':
                p[0] = p[2][:-1] + p[4][1:]
            else:
                semanticLog.debug(f'Error semántico, el operador {p[3]} no espera cadenas')
        else:
            semanticLog.debug(f'Error semántico, {p[1]} es de tipo {type(p[1])} mientras {p[3]} es de tipo {type(p[3])}')

def p_bitwiseExpression(p):
    '''
    bitwiseExpression : value bitwiseOperator value
                      | LPAREN value bitwiseOperator value RPAREN
    '''
    # Regla de José Julio Suárez, verifica que las operaciones bitwise se lleven a cabo únicamente entre números enteros
    if len(p) == 4:
        if isinstance(p[1], int) and isinstance(p[3], int): 
            if p[2] == '&':
                p[0] = p[1] & p[3]
            elif p[2] == '|':
                p[0] = p[1] | p[3]
            elif p[2] == '^':
                p[0] = p[1] ^ p[3]

        if isinstance(p[1], int):
            pass
        else:
            semanticLog.debug(f'Error semántico, {p[1]} no es de tipo int')

        if isinstance(p[3], int):
            pass
        else:
            semanticLog.debug(f'Error semántico, {p[3]} no es de tipo int')
    
    elif len(p) == 6:
        if isinstance(p[2], int) and isinstance(p[4], int):
            if p[3] == '&':
                p[0] = p[2] & p[4]
            elif p[3] == '|':
                p[0] = p[2] | p[4]
            elif p[3] == '^':
                p[0] = p[2] ^ p[4]

        if isinstance(p[2], int):
            pass
        else:
            semanticLog.debug(f'Error semántico, {p[2]} no es de tipo int')

        if isinstance(p[4], int):
            pass
        else:
            semanticLog.debug(f'Error semántico, {p[4]} no es de tipo int')
    


def p_dataStructureTypes(p):
    '''
    dataStructureTypes : datatype LESS_THAN multipleDatatypes MORE_THAN
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

def p_list(p):
    '''
    list : LBRACKET values RBRACKET
         | LBRACKET RBRACKET
    '''

def p_tuple(p):
    '''
    tuple : LPAREN values RPAREN
    '''

# Error rule for syntax errors
def p_error(p):
    print(f'Error sintáctico!')

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

time = datetime.datetime.now()
date = str(time.year) + str(time.month) + str(time.day)

def validate_algorithm(algorithm, username):
    syntaxOK = semanticsOK = False

    #syntax log
    filename = 'logs/sintactico-' + username + '-' + date + '-' + time.strftime('%Hh%M') + '.txt'
    file_handler = logging.FileHandler(filename, 'w')
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    #semantic log
    layout = 'logs/semantico-' + username + '-' + date + '-' + time.strftime('%Hh%M') + '.txt'
    handler = logging.FileHandler(layout, 'w')
    handler.setLevel(logging.DEBUG)
    semanticLog.addHandler(handler)
    semanticLog.setLevel(logging.DEBUG)

    result = parser.parse(algorithm, debug=log)
    file = open(filename, 'a')
    if os.path.getsize(filename) == 0:
        file.write('No se detectaron errores sintácticos!')
        syntaxOK = True
    file.close()

    file2 = open(layout, 'a')
    if os.path.getsize(layout) == 0:
        file2.write('No se detectaron errores semánticos!')
        semanticsOK = True
    file2.close()
    
    return (syntaxOK, semanticsOK, filename, layout)



algorithmJJ = """
abstract class MyAbstractClass {
void nullTest;
MyAbstractClass() {
print('You just instanced a class!');
}
}
class MyClass extends MyAbstractClass {
(double, int, String) record = (0, 0, ' ');
MyClass(double d, int i, String s) {
this.nullTest = null;
this.record = (d, i, s);
}
double doStuff() {
int x = 0;
double y = 0;
for (int i = 0; i < 10; i++) {
y -= record.$1;
x += record.$2;
}
while (x > 0 || y <= 0) {
x--;
y++;
}
bool xAndYAreEqual = false;
switch (y) {
case 0:
{
if (x == 0) {
xAndYAreEqual = true;
}
break;
}
default:
break;
}
if (!xAndYAreEqual) {
print('Bad luck!');
} else {
print('Good luck!');
}
int magicNumber = (record.$2 << 2) * 3;
int mask = 633245;
magicNumber = magicNumber & mask;
magicNumber = magicNumber | record.$2;
double magicDouble = magicNumber * (magicNumber % 2) / 5;
return magicDouble;
}
}
void main() {
print('Test code by Jose Julio Suarez');
var _myObject001 = new MyClass(2.3, 73, 'xd');
print("Your soul number: " + _myObject001.doStuff());
}
"""

algortimoNA = """
void main() { 
int a = 10; 
double b = a; // Conversión implícita: int a double, permitido 
double c = 5.5; 
int d = c; // Error: Conversión implícita de double a int no permitida 
int e = c as int; // Error: Conversión explícita de double a int no válida en este contexto 
num f = c; // Correcto: double se puede asignar a num 
int g = f as int; // Error: Runtime error si f no es un int 
} 



int doSomething1(bool flag) { 
if (true && false) { 
return 1; 
} else { 
return 0; // Correcto: ambas ramas retornan un valor 
} 
} 

String doSomething2(int code) { 
switch (code) { 
case 1: 
return "One"; 
case 2: 
return "Two"; 
default: 
return "Unknown"; // Correcto: todas las rutas retornan un valor 
} 
} 

void doSomething3(int numero) { 
if (numero > 0) { 
print('Positive'); 
} else if (numero < 0) { 
print('Negative'); 
} else { 
print('Zero'); // Correcto, ahora el else está después de todos los else if
} 
}
"""

algorithmOL = """
class Persona{
Persona({
required this.id,
required this.nombre,
required this.estatura,
}) : assert(id>0),
assert(name.isnotEmpty),
assert(estatura > 0.0)

final int id;
final String nombre;
final float estatura;
}

var list = ['a', 'b', 'c'];
int a = 10;
int b= 5;
assert(a);
a += 5;
b -= 2;
printf(a);
printf(b);

float c = 15.00;
c /= 3;
print(c);
float d = 2;
d *= 4


"""
#interactiveTest()
#validate_algorithm(algorithmJJ, "jojusuar")
#validate_algorithm(algortimoNA, 'niarias')
#validate_algorithm(algorithmOL, 'OliLM')