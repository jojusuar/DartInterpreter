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
                        | datatype VARIABLE LPAREN RPAREN LBRACE body RBRACE
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
          | list
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

#interactiveTest()

def validate_algorithm(algorithm):
    # Resetea el estado de error antes de parsear
    try:
        result = parser.parse(algorithm, tracking=True)       
    except Exception as e:
        print(f"Error: {e}")


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

validate_algorithm(algortimoNA)