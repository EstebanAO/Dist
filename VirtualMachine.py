import sys
import pickle
import tokens
from collections import deque

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
MEMORY_RANGE = 40000

class VirtualMachine:
    def __init__(self):
        # Compiler Data
        self.quadruples = []
        self.constants = {}
        self.start_direction = 0

        #Virtual Machine Data
        self.global_var = [[],[],[],[]]
        self.local = []

    def print_quad(self):
        print(self.constants)
        for idx, quad in enumerate(self.quadruples):
            print(str(idx) + " : " , quad)

    def get_variable_value(self, direction):
    #    print(direction)
        if type(direction) == str:
            direction = self.get_variable_value(int(direction))
        if direction < LIMIT_L_CHAR:
            return self.global_var[int(direction / MEMORY_RANGE)][direction % MEMORY_RANGE]
        elif direction < LIMIT_C_CHAR:
            return self.local[-1][int(direction / MEMORY_RANGE) - 4][direction % MEMORY_RANGE]
        else:
            return self.constants[direction]

    def cast_constants(self):
        for key, value in self.constants.items():
            self.constants[key] = self.cast_type(key, value)


    def cast_type(self, direction, value):
        if direction < LIMIT_G_INT:
            if len(value) == 1:
                return value
            else:
                return value[1]
        elif direction < LIMIT_G_BOOL:
            return int(value)
        elif direction < LIMIT_G_FLOAT:
            return value if type(value) == bool else value == 'true'
        elif direction < LIMIT_L_CHAR:
            return float(value)
        elif direction < LIMIT_L_INT:
            if len(value) == 1:
                return value
            else:
                return value[1]
        elif direction < LIMIT_L_BOOL:
            return int(value)
        elif direction < LIMIT_L_FLOAT:
            return value if type(value) == bool else value == 'true'
        elif direction < LIMIT_C_CHAR:
            return float(value)
        elif direction < LIMIT_C_INT:
            if len(value) == 1:
                return value
            else:
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
        if type(direction) == str:
            return self.get_direction_type(self.get_variable_value(int(direction)))
        direction = int(direction)
        if direction < LIMIT_G_INT:
            return tokens.CHAR
        elif direction < LIMIT_G_BOOL:
            return tokens.INT
        elif direction < LIMIT_G_FLOAT:
            return tokens.BOOL
        elif direction < LIMIT_L_CHAR:
            return tokens.FLOAT
        elif direction < LIMIT_L_INT:
            return tokens.CHAR
        elif direction < LIMIT_L_BOOL:
            return tokens.INT
        elif direction < LIMIT_L_FLOAT:
            return tokens.BOOL
        elif direction < LIMIT_C_CHAR:
            return tokens.FLOAT
        elif direction < LIMIT_C_INT:
            return tokens.CHAR
        elif direction < LIMIT_C_BOOL:
            return tokens.INT
        elif direction < LIMIT_C_FLOAT:
            return tokens.BOOL
        elif direction < LIMIT_C_STRING:
            return tokens.FLOAT
        else:
            return tokens.STRING

    def generate_memory_global(self, index_type, index_limit):
        global_size = len(self.global_var[index_type])
        while ( global_size <= index_limit ):
            self.global_var[index_type].append(None)
            global_size += 1

    def generate_memory_local(self, index_type, index_limit):
        local_size = len(self.local[-1][index_type])
        if index_type == 0:
            value = 'a'
        elif index_type == 1:
            value = int(0)
        elif index_type == 2:
            value = 'false'
        elif index_type == 3:
            value = 0.0
        while ( local_size <= index_limit ):
            self.local[-1][index_type].append(value)
            local_size += 1

    def fill_array(self, direction):
        if direction < LIMIT_L_CHAR:
            index_type = int(direction / MEMORY_RANGE)
            index_limit = direction % MEMORY_RANGE
            self.generate_memory_global(index_type, index_limit)
            self.global_var[index_type][index_limit] = '@'
        else:
            index_type = int(direction / MEMORY_RANGE) - 4
            index_limit = direction % MEMORY_RANGE
            self.generate_memory_local(index_type, index_limit)

            self.local[-1][index_type][index_limit] = '@'

    def set_variable_value(self, direction, value):
        if type(direction) == str:
            direction = self.get_variable_value(int(direction))

        if direction < LIMIT_L_CHAR:
            index_type = int(direction / MEMORY_RANGE)
            index_limit = direction % MEMORY_RANGE
            self.generate_memory_global(index_type, index_limit)
            self.global_var[index_type][index_limit] = self.cast_type(direction, value)
        else:
            index_type = int(direction / MEMORY_RANGE) - 4
            index_limit = direction % MEMORY_RANGE
            self.generate_memory_local(index_type, index_limit)
            self.local[-1][index_type][index_limit] = self.cast_type(direction, value)

    def print_stuff(self):
        print('\n')
        print(self.global_var)
        print(self.local)

    def read_function(self, direction):
        type = self.get_direction_type(direction)
        try:
            val = input()
            if type == tokens.INT:
                self.set_variable_value(direction, int(val))
            elif type == tokens.FLOAT:
                self.set_variable_value(direction, float(val))
            elif type == tokens.CHAR:
                self.set_variable_value(direction, '\'' + str(val)[0] + '\'')
            elif type == tokens.BOOL:
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
        self.local.append([[],[],[],[]])
        index = 0
        while(index < len(self.quadruples)):
            quad = self.quadruples[index]
            if quad[1] != None:
                value_left = self.get_variable_value(quad[1])
            if quad[2] != None:
                value_right = self.get_variable_value(quad[2])
            if (quad[0] == tokens.PLUS):
                self.set_variable_value(quad[3], value_left + value_right)
            elif (quad[0] == tokens.MINUS):
                self.set_variable_value(quad[3], value_left - value_right)
            elif (quad[0] == tokens.MULT):
                self.set_variable_value(quad[3], value_left * value_right)
            elif (quad[0] == tokens.DIV):
                val = value_left / value_right
                if self.get_direction_type(quad[1]) == tokens.INT and self.get_direction_type(quad[2]) == tokens.INT:
                    val = int(value_left / value_right)
                self.set_variable_value(quad[3], val)
            elif (quad[0] == tokens.ASSIGN):
                if self.get_direction_type(quad[3]) == tokens.INT:
                    value_left = int(value_left)
                self.set_variable_value(quad[3], value_left)
            elif (quad[0] == tokens.EQU):
            #    print(value_left == value_right)
                self.set_variable_value(quad[3], value_left == value_right)
            elif (quad[0] == tokens.GREATER):
                self.set_variable_value(quad[3], value_left > value_right)
            elif (quad[0] == tokens.GREATER_EQ):
                self.set_variable_value(quad[3], value_left >= value_right)
            elif (quad[0] == tokens.LESS):
                self.set_variable_value(quad[3], value_left < value_right)
            elif (quad[0] == tokens.LESS_EQ):
                self.set_variable_value(quad[3], value_left <= value_right)
            elif (quad[0] == tokens.AND):
                self.set_variable_value(quad[3], value_left and value_right)
            elif (quad[0] == tokens.OR):
                self.set_variable_value(quad[3], value_left or value_right)
            elif (quad[0] == tokens.PRINT):
                print_value = self.get_variable_value(quad[3])
                if type(print_value) == bool:
                    sys.stdout.write('true' if print_value else 'false')
                else:
                    sys.stdout.write(str(print_value))
            elif (quad[0] == tokens.PRINT_NEW_LINE):
                print_value = ''
                print(print_value)
            elif (quad[0] == tokens.READ):
                self.read_function(quad[3])
            elif (quad[0] == tokens.FILL_ARRAY):
                self.fill_array(quad[3])
            elif (quad[0] == tokens.VER):
                if value_left > quad[3] - 1:
                    raise IndexError('Index error ', value_left, ' ', quad[3] - 1)
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
    #    self.print_quad()
