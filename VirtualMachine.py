import pickle
import sys

from collections import deque
VAR = "var"
CTE = "cte"
FUN = "fun"
ARR = "arr"
GLOBAL = "global"
TYPE = "tipo"
VARS = "vars"
PARAMS = 'params'
VOID = "void"
INT = 'int'
FLOAT = 'float'
CHAR = 'char'
BOOL = 'bool'
STRING = 'str'
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
PRINT = 'print'
PRINT_NEW_LINE = 'print_new_line'
READ = 'read'
RETURN = 'return'
GO_TO_F = 'go_to_f'
GO_TO = 'go_to'
START = 'start'
END_PROC = 'end_proc'
ERA = 'era'
GO_SUB = 'go_sub'

LIMIT_G_CHAR = 0
LIMIT_G_INT = 40000
LIMIT_G_BOOL = 80000
LIMIT_G_FLOAT = 120000
LIMIT_L_CHAR = 160000
LIMIT_L_INT = 200000
LIMIT_L_BOOL = 240000
LIMIT_L_FLOAT = 280000
LIMIT_C_CHAR = 320000
LIMIT_C_INT = 360000
LIMIT_C_BOOL = 400000
LIMIT_C_FLOAT = 440000
LIMIT_C_STRING = 480000

class VirtualMachine:
    def __init__(self):
        # Compiler Data
        self.quadruples = []
        self.constants = {}
        self.start_direction = 0

        #Virtual Machine Data
        self.global_var = {}
        self.local = []

    def print_quad(self):
        print(self.constants)
        for idx, quad in enumerate(self.quadruples):
            print(str(idx) + " : " , quad)

    def get_variable_value(self, direction):
        if direction < LIMIT_L_CHAR:
            return self.global_var[direction]
        elif direction < LIMIT_C_CHAR:
            return self.local[-1][direction]
        else:
            return self.constants[direction]

    def cast_constants(self):
        for key, value in self.constants.items():
            self.constants[key] = self.cast_type(key, value)


    def cast_type(self, direction, value):
        if direction < LIMIT_G_INT:
            return value[1]
        elif direction < LIMIT_G_BOOL:
            return int(value)
        elif direction < LIMIT_G_FLOAT:
            return value if type(value) == bool else value == 'true'
        elif direction < LIMIT_L_CHAR:
            return float(value)
        elif direction < LIMIT_L_INT:
            return value[1]
        elif direction < LIMIT_L_BOOL:
            return int(value)
        elif direction < LIMIT_L_FLOAT:
            return value if type(value) == bool else value == 'true'
        elif direction < LIMIT_C_CHAR:
            return float(value)
        elif direction < LIMIT_C_INT:
            return value[1]
        elif direction < LIMIT_C_BOOL:
            return int(value)
        elif direction < LIMIT_C_FLOAT:
            return value if type(value) == bool else value == 'true'
        elif direction < LIMIT_C_STRING:
            return float(value)
        else:
            return value[1:-1]

    def get_direction_type(self, direction):
        if direction < LIMIT_G_INT:
            return CHAR
        elif direction < LIMIT_G_BOOL:
            return INT
        elif direction < LIMIT_G_FLOAT:
            return BOOL
        elif direction < LIMIT_L_CHAR:
            return FLOAT
        elif direction < LIMIT_L_INT:
            return CHAR
        elif direction < LIMIT_L_BOOL:
            return INT
        elif direction < LIMIT_L_FLOAT:
            return BOOL
        elif direction < LIMIT_C_CHAR:
            return FLOAT
        elif direction < LIMIT_C_INT:
            return CHAR
        elif direction < LIMIT_C_BOOL:
            return INT
        elif direction < LIMIT_C_FLOAT:
            return BOOL
        elif direction < LIMIT_C_STRING:
            return FLOAT
        else:
            return STRING

    def set_variable_value(self, direction, value):
        if direction < LIMIT_L_CHAR:
            self.global_var[direction] = self.cast_type(direction, value)
        else:
            self.local[-1][direction] = self.cast_type(direction, value)

    def print_stuff(self):
        print(self.global_var)
        print(self.local)

    def read_function(self, direction):
        type = self.get_direction_type(direction)
        try:
            val = input()
            if type == INT:
                self.set_variable_value(direction, int(val))
            elif type == FLOAT:
                self.set_variable_value(direction, float(val))
            elif type == CHAR:
                self.set_variable_value(direction, '\'' + str(val)[0] + '\'')
            elif type == BOOL:
                if val == 'true':
                    val = True
                elif val == 'false':
                    val = False
                else:
                    raise TypeError('Read type error')
                self.set_variable_value(direction, val)
        except:
            raise TypeError('Read type error')


    def run(self, file_name):
        self.get_quadruples(file_name)
        self.local.append({})
        index = 0
        while(index < len(self.quadruples)):
            quad = self.quadruples[index]
            if quad[1] != None:
                value_left = self.get_variable_value(quad[1])
            if quad[2] != None:
                value_right = self.get_variable_value(quad[2])
            if (quad[0] == PLUS):
                self.set_variable_value(quad[3], value_left + value_right)
            elif (quad[0] == MINUS):
                self.set_variable_value(quad[3], value_left - value_right)
            elif (quad[0] == MULT):
                self.set_variable_value(quad[3], value_left * value_right)
            elif (quad[0] == DIV):
                val = value_left / value_right
                if self.get_direction_type(quad[1]) == INT and self.get_direction_type(quad[2]) == INT:
                    val = int(value_left / value_right)
                self.set_variable_value(quad[3], val)
            elif (quad[0] == ASSIGN):
                if self.get_direction_type(quad[3]) == INT:
                    value_left = int(value_left)
                self.set_variable_value(quad[3], value_left)
            elif (quad[0] == EQU):
                print(value_left == value_right)
                self.set_variable_value(quad[3], value_left == value_right)
            elif (quad[0] == GREATER):
                self.set_variable_value(quad[3], value_left > value_right)
            elif (quad[0] == GREATER_EQ):
                self.set_variable_value(quad[3], value_left >= value_right)
            elif (quad[0] == LESS):
                self.set_variable_value(quad[3], value_left < value_right)
            elif (quad[0] == LESS_EQ):
                self.set_variable_value(quad[3], value_left <= value_right)
            elif (quad[0] == AND):
                self.set_variable_value(quad[3], value_left and value_right)
            elif (quad[0] == OR):
                self.set_variable_value(quad[3], value_left or value_right)
            elif (quad[0] == PRINT):
                print_value = self.get_variable_value(quad[3])
                if type(print_value) == bool:
                    sys.stdout.write('true' if print_value else 'false')
                else:
                    sys.stdout.write(str(print_value))
            elif (quad[0] == PRINT_NEW_LINE):
                print_value = ''
                print(print_value)
            elif (quad[0] == READ):
                self.read_function(quad[3])


            index += 1

        self.print_stuff()

    def get_quadruples(self, file_name):
        quad_file = open(file_name, 'rb')
        file_array = pickle.load(quad_file)
        self.quadruples = file_array[0]
        self.constants = file_array[1]
        self.start_direction = file_array[2]
        self.cast_constants()
        quad_file.close()
        self.print_quad()
