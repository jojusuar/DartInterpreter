#Estudiante 1: Néstor Arias Velásquez
#Matricula 1: 202111159
#Estudiante 2: José Julio Suárez
#Matrícula 2: 202205324
#Estudiante 3: Olivier León Márquez
#Matrícula 3: 202002028


import ply.lex as lex
import datetime

# List of token names.   This is always required

tokens = ('INTEGER', #inicio contribuciones Néstor
        'DOT',
        'DOLLAR',
        'NOT',
        'COMMENT',
        'MULTILINE_COMMENT',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'LPAREN',
        'RPAREN',
        'MOD',
        'EQUALS',
        'NOT_EQUAL',
        'VARIABLE',
        'COMMA',  
        'COLON',
        'DOUBLE',
        'SEMICOLON', #Inicio contribuciones Oliver
        'LBRACE',
        'RBRACE',
        'LBRACKET',
        'RBRACKET',
        'STRING',
        'ASSIGN',
        'SUM_ASSIGN',
        'SUB_ASSIGN',
        'MUL_ASSIGN',
        'DIV_ASSIGN',
        'MOD_ASSIGN',
        'AND_ASSIGN',
        'OR_ASSIGN',
        'XOR_ASSIGN',
        'LSHIFT_ASSIGN', #Inicio contribuciones José Julio
        'RSHIFT_ASSIGN',
        'RUNSIGNED_SHIFT_ASSIGN',
        'LESS_THAN',
        'MORE_THAN',
        'LESS_EQUAL',
        'MORE_EQUAL',
        'BITWISE_AND',
        'BITWISE_OR',
        'BITWISE_XOR',
        'LOGICAL_AND',
        'LOGICAL_OR',
        'IF_NULL',
        'FUNC_START',
        'ACCEPT_NULL'
    )

reserved = {
    'abstract': 'ABSTRACT',
    'as': 'AS',
    'assert': 'ASSERT',
    'async': 'ASYNC',
    'await': 'AWAIT',
    'base': 'BASE',
    'break': 'BREAK',
    'case': 'CASE',
    'catch': 'CATCH',
    'class': 'CLASS',
    'const': 'CONST',
    'continue': 'CONTINUE',
    'covariant': 'COVARIANT',
    'default': 'DEFAULT',
    'deferred': 'DEFERRED',
    'do': 'DO',
    'dynamic': 'DYNAMIC',
    'else': 'ELSE',
    'enum': 'ENUM',
    'export': 'EXPORT',
    'extends': 'EXTENDS',
    'extension': 'EXTENSION',
    'external': 'EXTERNAL',
    'factory': 'FACTORY',
    'false': 'FALSE',
    'final': 'FINAL',
    'finally': 'FINALLY',
    'for': 'FOR',
    'Function': 'FUNCTION',
    'get': 'GET',
    'hide': 'HIDE',
    'if': 'IF',
    'implements': 'IMPLEMENTS',
    'import': 'IMPORT',
    'in': 'IN',
    'interface': 'INTERFACE',
    'is': 'IS',
    'late': 'LATE',
    'library': 'LIBRARY',
    'mixin': 'MIXIN',
    'new': 'NEW',
    'null': 'NULL',
    'of': 'OF',
    'on': 'ON',
    'operator': 'OPERATOR',
    'part': 'PART',
    'required': 'REQUIRED',
    'rethrow': 'RETHROW',
    'return': 'RETURN',
    'sealed': 'SEALED',
    'set': 'SET',
    'show': 'SHOW',
    'static': 'STATIC',
    'super': 'SUPER',
    'switch': 'SWITCH',
    'sync': 'SYNC',
    'this': 'THIS',
    'throw': 'THROW',
    'true': 'TRUE',
    'try': 'TRY',
    'type': 'TYPE',
    'typedef': 'TYPEDEF',
    'var': 'VAR',
    'void': 'VOID',
    'when': 'WHEN',
    'with': 'WITH',
    'while': 'WHILE',
    'yield': 'YIELD',
    'int': 'INT_TYPE',
    'double': 'DOUBLE_TYPE',
    'num': 'NUM_TYPE',
    'bool': 'BOOL_TYPE',
    'String': 'STRING_TYPE',
    'List': 'LIST_TYPE',
    'Map': 'MAP_TYPE',
    'Runes': 'RUNES_TYPE',
    'Set': 'SET_TYPE',
    'Symbol': 'SYMBOL_TYPE',
    'var': 'VAR_TYPE'
}

tokens = tokens + tuple(reserved.values())

# Regular expression rules for simple tokens
t_DOT = r'\.'
t_DOLLAR = r'\$'
t_NOT = r'!'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_MOD = r'%'
t_EQUALS = r'=='
t_NOT_EQUAL = r'!='
t_COMMA = r','
t_COLON = r':'
t_SEMICOLON = r';'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_ASSIGN = r'='
t_LESS_THAN = r'<'
t_MORE_THAN = r'>'
t_LESS_EQUAL = r'<='
t_MORE_EQUAL = r'>='
t_SUM_ASSIGN = r'\+='
t_SUB_ASSIGN = r'-='
t_MUL_ASSIGN = r'\*='
t_DIV_ASSIGN = r'\/='
t_MOD_ASSIGN = r'%='
t_AND_ASSIGN = r'&='
t_OR_ASSIGN= r'\|='
t_XOR_ASSIGN = r'\^='
t_LSHIFT_ASSIGN = r'<<='
t_RSHIFT_ASSIGN = r'>>='
t_RUNSIGNED_SHIFT_ASSIGN = r'>>>=' 
t_BITWISE_AND = r'\&'
t_BITWISE_OR = r'\|'
t_BITWISE_XOR = r'\^'
t_LOGICAL_AND = r'\&\&'
t_LOGICAL_OR = r'\|\|'
t_IF_NULL = r'\?\?'
t_ACCEPT_NULL = r'\?'

def t_FUNC_START(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*\('
    t.type = reserved.get(t.value, 'FUNC_START')
    return t

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VARIABLE')
    return t

def t_COMMENT(t):
    r'//.*'
    t.type = reserved.get(t.value, 'COMMENT')
    return t

def t_MULTILINE_COMMENT(t):
    r'\/\*(?:(?!\*\/)[\S\s])*\*\/'
    t.type = reserved.get(t.value, 'MULTILINE_COMMENT')
    return t


# A regular expression rule with some action code
def t_DOUBLE(t):
    r'-?(\d+\.\d*|\d*\.\d+)'
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'(\".*\")|(\'.*\')'
    t.value = str(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

#algoritmo José Julio Suárez
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


data = """
& && | || ^ == != < > <= >= + - * / % = == != < > <= >= + - * / % = ??
*= += -= *= /= %= &= |= ^= <<= >>= >>>= <<= >>= &= |= ^= <<= >>= >>>=
( ) { } [ ] , : ;
"""

time = datetime.datetime.now()
date = str(time.year) + str(time.month) + str(time.day)

def testTokens(algorithm, username):
    lexer.input(algorithm)
    log = open('logs/lexico-' + username + '-' + date + '-' + time.strftime('%Hh%M') + '.txt', 'w')
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        log.write(str(tok) + '\n')
    log.close()
    print('Log written!')

# testTokens(algorithmJJ, 'jojusuar')
# testTokens(algortimoNA, 'Niariasve')
# testTokens(algorithmOL, 'OliLM')