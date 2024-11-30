grammar CWeb;

// Lexer Rules
FUNC        : 'func';
RETURN      : 'return';
INT         : 'int';
BOOL        : 'bool';
IF          : 'if';
FOR         : 'for';
WHILE       : 'while';
TRUE        : 'true';
FALSE       : 'false';
LPAREN      : '(';
RPAREN      : ')';
LBRACE      : '{';
RBRACE      : '}';
SEMICOLON   : ';';
COMMA       : ',';
ASSIGN      : '=';
PLUS        : '+';
MINUS       : '-';
MULT        : '*';
DIV         : '/';
MOD         : '%';
EQ          : '==';
NEQ         : '!=';
LT          : '<';
GT          : '>';
LEQ         : '<=';
GEQ         : '>=';
AND         : '&&';
OR          : '||';
NOT         : '!';
COMMENT     : '/*' .*? '*/' -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
ID          : [a-zA-Z_][a-zA-Z0-9_]*;
NUM         : [0-9]+;
WS          : [ \t\r\n]+ -> skip;

// Parser Rules
program         : (function | statement)* EOF;
function        : FUNC ID LPAREN parameterList? RPAREN returnType LBRACE statement* RBRACE;
parameterList   : parameter (COMMA parameter)*;
parameter       : type ID;
returnType      : '->' type;
type            : INT | BOOL;

statement       : variableDeclaration
                | assignment
                | returnStatement
                | ifStatement
                | forLoop
                | whileLoop
                | expression SEMICOLON;

variableDeclaration
                : type ID (ASSIGN expression)? SEMICOLON;

assignment      : ID ASSIGN expression SEMICOLON;

returnStatement : RETURN expression SEMICOLON;

ifStatement     : IF LPAREN expression RPAREN LBRACE statement* RBRACE;

forLoop         : FOR LPAREN assignment expression SEMICOLON assignment RPAREN LBRACE statement* RBRACE;

whileLoop       : WHILE LPAREN expression RPAREN LBRACE statement* RBRACE;

expression      : term ((PLUS | MINUS) term)*;
term            : factor ((MULT | DIV | MOD) factor)*;
factor          : LPAREN expression RPAREN
                | NUM
                | ID
                | BOOL
                | NOT factor;
