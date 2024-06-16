#Estudiante 1: Néstor Arias Velásquez
#Matricula 1: 202111159
#Estudiante 2: José Julio Suárez
#Matrícula 2: 202205324

import ply.lex as lex
import datetime

# List of token names.   This is always required

tokens = ('INTEGER', #inicio contribuciones Néstor
        'DOT',
        'DOLLAR',
        'NOT',
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
        'FLOAT',
        'SEMICOLON', #Inicio contribuciones Oliver
        'LBRACE',
        'RBRACE',
        'LBRACKET',
        'RBRACKET',
        'STRING',
        'ASSING',
        'SUM_ASSING',
        'SUB_ASSING',
        'MUL_ASSING',
        'DIV_ASSING',
        'MOD_ASSING',
        'AND_ASSING',
        'OR_ASSING',
        'XOR_ASSING',
        'LSHIFT_ASSING', #Inicio contribuciones José Julio
        'RSHIFT_ASSING',
        'RUNSINGED_SHIFT_ASSING',
        'LESS_THAN',
        'MORE_THAN',
        'LESS_EQUAL',
        'MORE_EQUAL',
        'BITWISE_AND',
        'BITWISE_OR',
        'BITWISE_XOR',
        'LOGICAL_AND',
        'LOGICAL_OR',
        'IF_NULL'
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
    'yield': 'YIELD'
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
t_ASSING = r'='
t_LESS_THAN = r'<'
t_MORE_THAN = r'>'
t_LESS_EQUAL = r'<='
t_MORE_EQUAL = r'>='
t_SUM_ASSING = r'\+='
t_SUB_ASSING = r'-='
t_MUL_ASSING = r'\*='
t_DIV_ASSING = r'\/='
t_MOD_ASSING = r'%='
t_AND_ASSING = r'&='
t_OR_ASSING = r'\|='
t_XOR_ASSING = r'\^='
t_LSHIFT_ASSING = r'<<='
t_RSHIFT_ASSING = r'>>='
t_RUNSINGED_SHIFT_ASSING = r'>>>=' 
t_BITWISE_AND = r'\&'
t_BITWISE_OR = r'\|'
t_BITWISE_XOR = r'\^'
t_LOGICAL_AND = r'\&\&'
t_LOGICAL_OR = r'\|\|'
t_IF_NULL = r'\?\?'


def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VARIABLE')
    return t


# A regular expression rule with some action code
def t_FLOAT(t):
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

testTokens(algorithmJJ, 'jojusuar')