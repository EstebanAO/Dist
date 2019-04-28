import sys
import pickle
import tokens
import limits
from collections import deque

class VirtualMachine:
    def __init__(self):
        # Compiler Data
        self.quadruples = []
        self.constants = {}
        self.start_index = 0
        self.actual_index = 0

        #Virtual Machine Data
        self.global_var = [[],[],[],[]]
        self.local = []

    def print_quad(self):
        print(self.constants)
        for idx, quad in enumerate(self.quadruples):
            print(str(idx) + " : " , quad)

    def is_pointer(self, direction):
        return direction >= limits.P_CHAR and direction < limits.P_FLOAT + limits.MEMORY_RANGE

    def get_pointer_value(self, direction):
    #    print("---- ", direction, " - ", self.local , " -----");
        return self.local[-1][int(direction / limits.MEMORY_RANGE) - 4][direction % limits.MEMORY_RANGE]

    def get_variable_value(self, direction):
    #     print(" ... ", direction)
        if self.is_pointer(direction):
            return self.get_variable_value(self.get_pointer_value(direction))
        if direction < limits.G_FLOAT + limits.MEMORY_RANGE:
            return self.global_var[int(direction / limits.MEMORY_RANGE)][direction % limits.MEMORY_RANGE]
        elif direction < limits.P_FLOAT + limits.MEMORY_RANGE:
        #    print("- ", direction, " ", self.local)
        #     print("sum: ", limits.P_FLOAT + limits.MEMORY_RANGE)
            return self.local[-1][int(direction / limits.MEMORY_RANGE) - 4][direction % limits.MEMORY_RANGE]
        else:
            return self.constants[direction]

    def cast_constants(self):
        for key, value in self.constants.items():
            self.constants[key] = self.cast_type(key, value)

    def cast_type(self, direction, value):
        if self.is_pointer(direction):
            return value
        if direction < limits.G_CHAR + limits.MEMORY_RANGE:
            if len(value) == 1:
                return value
            else:
                return value[1]
        elif direction < limits.G_INT + limits.MEMORY_RANGE:
            return int(value)
        elif direction < limits.G_BOOL + limits.MEMORY_RANGE:
            return value if type(value) == bool else value == 'true'
        elif direction < limits.G_FLOAT + limits.MEMORY_RANGE:
            return float(value)
        elif direction < limits.L_CHAR + limits.MEMORY_RANGE:
            if len(value) == 1:
                return value
            else:
                return value[1]
        elif direction < limits.L_INT + limits.MEMORY_RANGE:
            return int(value)
        elif direction < limits.L_BOOL + limits.MEMORY_RANGE:
            return value if type(value) == bool else value == 'true'
        elif direction < limits.L_FLOAT + limits.MEMORY_RANGE:
            return float(value)
        elif direction < limits.C_CHAR + limits.MEMORY_RANGE:
            if len(value) == 1:
                return value
            else:
                return value[1]
        elif direction < limits.C_INT + limits.MEMORY_RANGE:
            return int(value)
        elif direction < limits.C_BOOL + limits.MEMORY_RANGE:
            return value if type(value) == bool else value == 'true'
        elif direction < limits.C_FLOAT + limits.MEMORY_RANGE:
            return float(value)
        else:
            return value[1:-1]

    def get_direction_type(self, direction):
    #    if self.is_pointer(direction):
    #        return self.get_direction_type(self.get_variable_value(direction))
        # direction = int(direction)
        if direction < limits.G_CHAR + limits.MEMORY_RANGE:
            return tokens.CHAR
        elif direction < limits.G_INT + limits.MEMORY_RANGE:
            return tokens.INT
        elif direction < limits.G_BOOL + limits.MEMORY_RANGE:
            return tokens.BOOL
        elif direction < limits.G_FLOAT + limits.MEMORY_RANGE:
            return tokens.FLOAT
        elif direction < limits.L_CHAR + limits.MEMORY_RANGE:
            return tokens.CHAR
        elif direction < limits.L_INT + limits.MEMORY_RANGE:
            return tokens.INT
        elif direction < limits.L_BOOL + limits.MEMORY_RANGE:
            return tokens.BOOL
        elif direction < limits.L_FLOAT + limits.MEMORY_RANGE:
            return tokens.FLOAT
        elif direction < limits.P_CHAR + limits.MEMORY_RANGE:
            return tokens.CHAR
        elif direction < limits.P_INT + limits.MEMORY_RANGE:
            return tokens.INT
        elif direction < limits.P_BOOL + limits.MEMORY_RANGE:
            return tokens.BOOL
        elif direction < limits.L_FLOAT + limits.MEMORY_RANGE:
            return tokens.FLOAT
        elif direction < limits.C_CHAR + limits.MEMORY_RANGE:
            return tokens.CHAR
        elif direction < limits.C_INT + limits.MEMORY_RANGE:
            return tokens.INT
        elif direction < limits.C_BOOL + limits.MEMORY_RANGE:
            return tokens.BOOL
        elif direction < limits.C_FLOAT + limits.MEMORY_RANGE:
            return tokens.FLOAT
        else:
            return tokens.STRING

    def get_default_value(self, index_type):
        if index_type in [0, 4]:
            return 'a'
        elif index_type in [1, 5]:
            return int(0)
        elif index_type in [2, 6]:
            return 'false'
        elif index_type in [3, 7]:
            return 0.0

    def generate_memory_global(self, index_type, index_limit):
        global_size = len(self.global_var[index_type])
        value = self.get_default_value(index_type)
        while ( global_size <= index_limit ):
            self.global_var[index_type].append(value)
            global_size += 1

    def generate_memory_local(self, index_type, index_limit):
        local_size = len(self.local[-1][index_type])
        value = self.get_default_value(index_type)
        while ( local_size <= index_limit ):
            self.local[-1][index_type].append(value)
            local_size += 1

    def fill_array(self, direction):
        if direction < limits.L_CHAR:
            index_type = int(direction / limits.MEMORY_RANGE)
            index_limit = direction % limits.MEMORY_RANGE
            self.generate_memory_global(index_type, index_limit)
            self.global_var[index_type][index_limit] = '@'
        else:
            index_type = int(direction / limits.MEMORY_RANGE) - 4
            index_limit = direction % limits.MEMORY_RANGE
            self.generate_memory_local(index_type, index_limit)

            self.local[-1][index_type][index_limit] = '@'

    def set_initial_pointer_value(self, direction, value):
        index_type = int(direction / limits.MEMORY_RANGE) - 4
        index_limit = direction % limits.MEMORY_RANGE
        self.generate_memory_local(index_type, index_limit)
        self.local[-1][index_type][index_limit] = value

    def set_variable_value(self, direction, value):
    #    print(" * ", direction, " ", value, self.local)

        if self.is_pointer(direction):
            direction = self.get_pointer_value(direction)

        if direction < limits.L_CHAR:
            index_type = int(direction / limits.MEMORY_RANGE)
            index_limit = direction % limits.MEMORY_RANGE
            self.generate_memory_global(index_type, index_limit)
            self.global_var[index_type][index_limit] = self.cast_type(direction, value)
        else:
            index_type = int(direction / limits.MEMORY_RANGE) - 4
            index_limit = direction % limits.MEMORY_RANGE
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
        self.local.append([[],[],[],[],[],[],[],[]])
        self.actual_index = self.start_index
        while(self.actual_index < len(self.quadruples)):
            quad = self.quadruples[self.actual_index]
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
            elif (quad[0] == tokens.PLUS_POINTER):
                self.set_initial_pointer_value(quad[3], value_left + value_right)
            elif (quad[0] == tokens.GO_TO_F):
                if not self.get_variable_value(quad[1]):
                    self.actual_index = quad[3] - 1
            elif (quad[0] == tokens.GO_TO):
                self.actual_index = quad[3] - 1

            self.actual_index += 1
        self.print_stuff()

    def get_quadruples(self, file_name):
        quad_file = open(file_name, 'rb')
        file_array = pickle.load(quad_file)
        self.quadruples = file_array[0]
        self.constants = file_array[1]
        self.start_index = file_array[2]
        self.cast_constants()
        quad_file.close()
    #    self.print_quad()
