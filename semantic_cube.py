INT = 'int'
FLOAT = 'float'
CHAR = 'char'
BOOL = 'bool'
PLUS = '+'
MINUS = '-'
MULT = '*'
DIV = '/'
EQU = '=='
GREATER = '>'
GREATER_EQ = '>='
LESS = '<'
LESS_EQ = '<='
DIFF = '!='
AND = '&&'
OR = '||'
ASSIGN = '='
ERROR = 'error'

def get_semantic_cube():
    sem_cube = {
        INT: {
            INT:{
                PLUS : INT,
                MINUS : INT,
                MULT : INT,
                DIV : INT,
                EQU : BOOL,
                GREATER : BOOL,
                GREATER_EQ : BOOL,
                LESS : BOOL,
                LESS_EQ : BOOL,
                DIFF : BOOL,
                AND : ERROR,
                OR : ERROR,
                ASSIGN : INT
            },
            FLOAT:{
                PLUS : FLOAT,
                MINUS : FLOAT,
                MULT : FLOAT,
                DIV : FLOAT,
                EQU : BOOL,
                GREATER : BOOL,
                GREATER_EQ : BOOL,
                LESS : BOOL,
                LESS_EQ : BOOL,
                DIFF : BOOL,
                AND : ERROR,
                OR : ERROR,
                ASSIGN : INT
            },
            CHAR:{
                PLUS : ERROR,
                MINUS : ERROR,
                MULT : ERROR,
                DIV : ERROR,
                EQU : ERROR,
                GREATER : ERROR,
                GREATER_EQ : ERROR,
                LESS : ERROR,
                LESS_EQ : ERROR,
                DIFF : ERROR,
                AND : ERROR,
                OR : ERROR,
                ASSIGN : ERROR
            },
            BOOL:{
                PLUS : ERROR,
                MINUS : ERROR,
                MULT : ERROR,
                DIV : ERROR,
                EQU : ERROR,
                GREATER : ERROR,
                GREATER_EQ : ERROR,
                LESS : ERROR,
                LESS_EQ : ERROR,
                DIFF : ERROR,
                AND : ERROR,
                OR : ERROR,
                ASSIGN : ERROR
            }
        },

        FLOAT: {
            FLOAT:{
                PLUS : FLOAT,
                MINUS : FLOAT,
                MULT : FLOAT,
                DIV : FLOAT,
                EQU : BOOL,
                GREATER : BOOL,
                GREATER_EQ : BOOL,
                LESS : BOOL,
                LESS_EQ : BOOL,
                DIFF : BOOL,
                AND : ERROR,
                OR : ERROR,
                ASSIGN : FLOAT
            },
            INT:{
                PLUS : FLOAT,
                MINUS : FLOAT,
                MULT : FLOAT,
                DIV : FLOAT,
                EQU : BOOL,
                GREATER : BOOL,
                GREATER_EQ : BOOL,
                LESS : BOOL,
                LESS_EQ : BOOL,
                DIFF : BOOL,
                AND : ERROR,
                OR : ERROR,
                ASSIGN : FLOAT
            },
            CHAR:{
                PLUS : ERROR,
                MINUS : ERROR,
                MULT : ERROR,
                DIV : ERROR,
                EQU : ERROR,
                GREATER : ERROR,
                GREATER_EQ : ERROR,
                LESS : ERROR,
                LESS_EQ : ERROR,
                DIFF : ERROR,
                AND : ERROR,
                OR : ERROR,
                ASSIGN : ERROR
            },
            BOOL:{
                PLUS : ERROR,
                MINUS : ERROR,
                MULT : ERROR,
                DIV : ERROR,
                EQU : ERROR,
                GREATER : ERROR,
                GREATER_EQ : ERROR,
                LESS : ERROR,
                LESS_EQ : ERROR,
                DIFF : ERROR,
                AND : ERROR,
                OR : ERROR,
                ASSIGN : ERROR
            }
        },
        CHAR: {
            CHAR:{
                PLUS : ERROR,
                MINUS : ERROR,
                MULT : ERROR,
                DIV : ERROR,
                EQU : BOOL,
                GREATER : ERROR,
                GREATER_EQ : ERROR,
                LESS : ERROR,
                LESS_EQ : ERROR,
                DIFF : BOOL,
                AND : ERROR,
                OR : ERROR,
                ASSIGN : CHAR
            },
            INT:{
                PLUS : ERROR,
                MINUS : ERROR,
                MULT : ERROR,
                DIV : ERROR,
                EQU : ERROR,
                GREATER : ERROR,
                GREATER_EQ : ERROR,
                LESS : ERROR,
                LESS_EQ : ERROR,
                DIFF : ERROR,
                AND : ERROR,
                OR : ERROR,
                ASSIGN : ERROR
            },
            FLOAT:{
                PLUS : ERROR,
                MINUS : ERROR,
                MULT : ERROR,
                DIV : ERROR,
                EQU : ERROR,
                GREATER : ERROR,
                GREATER_EQ : ERROR,
                LESS : ERROR,
                LESS_EQ : ERROR,
                DIFF : ERROR,
                AND : ERROR,
                OR : ERROR,
                ASSIGN : ERROR
            },
            BOOL:{
                PLUS : ERROR,
                MINUS : ERROR,
                MULT : ERROR,
                DIV : ERROR,
                EQU : ERROR,
                GREATER : ERROR,
                GREATER_EQ : ERROR,
                LESS : ERROR,
                LESS_EQ : ERROR,
                DIFF : ERROR,
                AND : ERROR,
                OR : ERROR,
                ASSIGN : ERROR
            }
        },
        BOOL: {
            BOOL:{
                PLUS : ERROR,
                MINUS : ERROR,
                MULT : ERROR,
                DIV : ERROR,
                EQU : BOOL,
                GREATER : ERROR,
                GREATER_EQ : ERROR,
                LESS : ERROR,
                LESS_EQ : ERROR,
                DIFF : BOOL,
                AND : BOOL,
                OR : BOOL,
                ASSIGN : BOOL
            },
            INT:{
                PLUS : ERROR,
                MINUS : ERROR,
                MULT : ERROR,
                DIV : ERROR,
                EQU : ERROR,
                GREATER : ERROR,
                GREATER_EQ : ERROR,
                LESS : ERROR,
                LESS_EQ : ERROR,
                DIFF : ERROR,
                AND : ERROR,
                OR : ERROR,
                ASSIGN : ERROR
            },
            FLOAT:{
                PLUS : ERROR,
                MINUS : ERROR,
                MULT : ERROR,
                DIV : ERROR,
                EQU : ERROR,
                GREATER : ERROR,
                GREATER_EQ : ERROR,
                LESS : ERROR,
                LESS_EQ : ERROR,
                DIFF : ERROR,
                AND : ERROR,
                OR : ERROR,
                ASSIGN : ERROR
            },
            CHAR:{
                PLUS : ERROR,
                MINUS : ERROR,
                MULT : ERROR,
                DIV : ERROR,
                EQU : ERROR,
                GREATER : ERROR,
                GREATER_EQ : ERROR,
                LESS : ERROR,
                LESS_EQ : ERROR,
                DIFF : ERROR,
                AND : ERROR,
                OR : ERROR,
                ASSIGN : ERROR
            }
        }
    }
    return sem_cube
