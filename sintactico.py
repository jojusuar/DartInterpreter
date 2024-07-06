import ply.yacc as yacc
import datetime
import logging
import os
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
    import : IMPORT STRING
    '''

def p_instruction(p):
    '''
    instruction : functionCall
                | variableDeclarationUninitialized
                | variableDeclarationInitialized
                | variableMutation
                | import
                | return
                | BREAK
    '''

def p_classDeclaration(p):
    '''
    classDeclaration : CLASS VARIABLE LBRACE classBody RBRACE
    classDeclaration : ABSTRACT CLASS VARIABLE LBRACE classBody RBRACE
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
                | constructorDeclaration
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

def p_nullable_datatype(p):
    '''
    nullable_datatype : non_nullable_datatype ACCEPT_NULL
    '''

def p_datatype(p):
    '''
    datatype : nullable_datatype
             | non_nullable_datatype
             | VOID
             | recordTypes
             | dataStructureTypes
    '''

def p_variableDeclarationUninitialized(p):
    '''
    variableDeclarationUninitialized : datatype VARIABLE
    '''

def p_variableInitialization(p):
    '''
    variableInitialization : ASSIGN value
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
def p_immediateMutate(p):
    '''
    immediateMutate : PLUS PLUS
                    | MINUS MINUS
    '''
def p_variableMutation(p):
    '''
    variableMutation : VARIABLE variableInitialization
                     | VARIABLE immediateAssign value
                     | VARIABLE immediateMutate
                     | THIS DOT VARIABLE variableInitialization
                     | THIS DOT VARIABLE immediateAssign value
                     | THIS DOT VARIABLE immediateMutate
    '''


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

def p_bitShiftOperator(p):
    '''
    bitShift : LESS_THAN LESS_THAN
             | MORE_THAN MORE_THAN
    '''

def p_comparator(p):
    '''
    comparator : EQUALS
               | LESS_THAN
               | MORE_THAN
               | LESS_EQUAL
               | MORE_EQUAL
    '''

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
                | STRING
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

def p_value(p):
    '''
    value : staticValue
          | value immediateAssign value
          | functionCall
          | attributeValue
    '''

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

def p_bitShift(p):
    '''
    bitShift : value bitShift value
             | LPAREN value bitShift value RPAREN
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
    print(f'Syntax error in input! at token {p.value} (line {p.lineno})')

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
    log = logging.getLogger()
    filename = 'logs/sintactico-' + username + '-' + date + '-' + time.strftime('%Hh%M') + '.txt'
    file_handler = logging.FileHandler(filename, 'w')
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)
    result = parser.parse(algorithm, debug=log)
    file = open(filename, 'a')
    if os.path.getsize(filename) == 0:
        file.write('No se detectaron errores sintácticos!')
    file.close()



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
  if (flag) { 
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

void doSomething3(int num) { 
  if (num > 0) { 
    print('Positive'); 
  } else { (num < 0) { 
    print('Negative'); 
  } else if { 
    print('Zero'); //Incorrecto; no puede haber un else if despues de un else 
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
interactiveTest()
# validate_algorithm(algorithmJJ, "jojusuar")
#validate_algorithm(algortimoNA, 'niarias')