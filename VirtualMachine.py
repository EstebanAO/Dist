import sys
import pickle
import tokens
import limits
import SpecialFunctions

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
        self.params = {}
        self.jumps = []
        self.temp_return_value = ""
        self.temp_to_return_direction = []

    """ Retruns true if the direction provided is a pointer, false otherwise """
    def is_pointer(self, direction):
        return direction >= limits.P_CHAR and direction < limits.P_FLOAT + limits.MEMORY_RANGE

    """ Retruns the value of a pointer (it is a direction) """
    def get_pointer_value(self, direction):
        return self.local[-1][int(direction / limits.MEMORY_RANGE) - 4][direction % limits.MEMORY_RANGE]

    """ Retruns the value of a non pointer direction """
    def get_variable_value(self, direction):
        if self.is_pointer(direction):
            return self.get_variable_value(self.get_pointer_value(direction))
        if direction < limits.G_FLOAT + limits.MEMORY_RANGE:
            return self.global_var[int(direction / limits.MEMORY_RANGE)][direction % limits.MEMORY_RANGE]
        elif direction < limits.P_FLOAT + limits.MEMORY_RANGE:
            return self.local[-1][int(direction / limits.MEMORY_RANGE) - 4][direction % limits.MEMORY_RANGE]
        else:
            return self.constants[direction]

    """ Cast all the constants received from the compiler to their correct type """
    def cast_constants(self):
        for key, value in self.constants.items():
            self.constants[key] = self.cast_type(key, value)

    """ Casts a single value to the correct type according to the direction provided """
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

    """ retrun the type-token given a direction """
    def get_direction_type(self, direction):
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
        elif direction < limits.P_FLOAT + limits.MEMORY_RANGE:
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

    """ Retruns the default values of the four elemental types of Dist """
    def get_default_value(self, index_type):
        if index_type in [0, 4]:
            return 'a'
        elif index_type in [1, 5]:
            return int(0)
        elif index_type in [2, 6]:
            return 'false'
        elif index_type in [3, 7]:
            return 0.0
    
    """ Generates all the memory spaces of the global context until
        the index limit is reached """
    def generate_memory_global(self, index_type, index_limit):
        global_size = len(self.global_var[index_type])
        value = self.get_default_value(index_type)
        while ( global_size <= index_limit ):
            self.global_var[index_type].append(value)
            global_size += 1

    """ Generates all the memory spaces of the local context until
        the index limit is reached """
    def generate_memory_local(self, index_type, index_limit):
        local_size = len(self.local[-1][index_type])
        value = self.get_default_value(index_type)
        while ( local_size <= index_limit ):
            self.local[-1][index_type].append(value)
            local_size += 1

    """ Creates the space of an array in memory """
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

    """ Sets the value of a pointer """
    def set_initial_pointer_value(self, direction, value):
        index_type = int(direction / limits.MEMORY_RANGE) - 4
        index_limit = direction % limits.MEMORY_RANGE
        self.generate_memory_local(index_type, index_limit)
        self.local[-1][index_type][index_limit] = value

    """ Sets the value of a variable """
    def set_variable_value(self, direction, value):
        if self.is_pointer(direction):
            direction = self.get_pointer_value(direction)
        if direction < limits.L_CHAR:
            index_type = int(direction / limits.MEMORY_RANGE)
            index_limit = direction % limits.MEMORY_RANGE
            self.generate_memory_global(index_type, index_limit)
            if value != '@':
                self.global_var[index_type][index_limit] = self.cast_type(direction, value)
            else:
                self.global_var[index_type][index_limit] = '@'
        else:
            index_type = int(direction / limits.MEMORY_RANGE) - 4
            index_limit = direction % limits.MEMORY_RANGE
            self.generate_memory_local(index_type, index_limit)
            if value != '@':
                self.local[-1][index_type][index_limit] = self.cast_type(direction, value)
            else:
                self.local[-1][index_type][index_limit] = '@'

    """ This function prints relevant data to the developers of dist """
    def print_stuff(self):
        print('\n')
        print(self.global_var)
        print(self.local)
    
    """ Function to read from console and set the value to a given direction """
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

    """ Assign the value to sender direction to the temporal params dictionary """
    def assign_param(self, sender_direction, receiver_direction):
        value = self.get_variable_value(sender_direction)
        self.params[receiver_direction] = value

    """ Create new local context and asigns the params """
    def go_sub(self):
        self.local.append([[],[],[],[],[],[],[],[]])
        for key, value in self.params.items():
            self.set_variable_value(key, value)

    """ Copies the param array into the new local context  """
    def fill_params_array(self, start_dir, end_dir, new_start_dir):
        counter = 0
        for new_dir in range(start_dir, end_dir + 1):
            self.params[new_start_dir + counter] = self.get_variable_value(new_dir)
            counter += 1

    """ Create new variable space """
    def initialize_variable(self, direction):
        ini_value = self.get_default_value(int(direction/limits.MEMORY_RANGE))
        self.set_variable_value(direction, ini_value)
    
    """ The handler of the Virtual Machine, it runs every quadruple"""
    def run(self, file_name):
        self.get_quadruples(file_name)
        self.local.append([[],[],[],[],[],[],[],[]])
        self.actual_index = self.start_index
        while(self.actual_index < len(self.quadruples)):
            quad = self.quadruples[self.actual_index]
            if quad[1] != None and quad[0] != tokens.GO_SUB: 
                value_left = self.get_variable_value(quad[1]) # Get Pos 1 value
            if quad[2] != None and quad[0] != tokens.GO_SUB:
                value_right = self.get_variable_value(quad[2]) # Get pos 2 value
            if (quad[0] == tokens.PLUS):
                self.set_variable_value(quad[3], value_left + value_right)
            elif (quad[0] == tokens.MINUS):
                self.set_variable_value(quad[3], value_left - value_right)
            elif (quad[0] == tokens.MULT):
                self.set_variable_value(quad[3], value_left * value_right)
            elif (quad[0] == tokens.DIV):
                if (value_right == 0):
                    raise ZeroDivisionError('Division by cero is undefined')
                val = value_left / value_right
                if self.get_direction_type(quad[1]) == tokens.INT and self.get_direction_type(quad[2]) == tokens.INT:
                    val = int(value_left / value_right)
                self.set_variable_value(quad[3], val)
            elif (quad[0] == tokens.ASSIGN):
                if self.get_direction_type(quad[3]) == tokens.INT:
                    value_left = int(value_left)
                self.set_variable_value(quad[3], value_left)
            elif (quad[0] == tokens.EQU):
                self.set_variable_value(quad[3], value_left == value_right)
            elif (quad[0] == tokens.DIFF):
                self.set_variable_value(quad[3], value_left != value_right)
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
            elif (quad[0] == tokens.ERA):
                self.params = {}
            elif (quad[0] == tokens.ASSIGN_PARAM):
                self.assign_param(quad[1], quad[3])
            elif (quad[0] == tokens.GO_SUB):
                self.go_sub()
                if (quad[1] != None):
                    self.temp_to_return_direction.append(quad[1])
                self.jumps.append(self.actual_index)
                self.actual_index = quad[3]  - 1
            elif (quad[0] == tokens.END_PROC):
                self.local.pop()
                self.actual_index = self.jumps.pop()
            elif (quad[0] == tokens.RETURN):
                self.temp_return_value = self.get_variable_value(quad[3])
                self.local.pop()
                self.set_variable_value(self.temp_to_return_direction.pop(), self.temp_return_value)
                self.actual_index = self.jumps.pop()
            elif (quad[0] == tokens.ASSIGN_ARRAY_PARAM):
                self.fill_params_array(quad[1], quad[2], quad[3])
            elif (quad[0] == tokens.INI_VAR):
                self.initialize_variable(quad[3])
            elif (quad[0] == tokens.POW):
                pow = SpecialFunctions.pow(value_left, value_right)
                self.set_variable_value(quad[3], pow)
            elif (quad[0] == tokens.SQRT):
                sqrt = SpecialFunctions.sqrt(value_left, value_right)
                self.set_variable_value(quad[3], sqrt)
            elif (quad[0] == tokens.MODE):
                list = self.array_to_list(quad[1])
                mode = SpecialFunctions.mode(list)
                self.set_variable_value(quad[3], mode)
            elif (quad[0] == tokens.PROB):
                list = self.array_to_list(quad[1])
                value = self.get_variable_value(quad[2])
                prob = SpecialFunctions.prob(list, value)
                self.set_variable_value(quad[3], prob)
            elif (quad[0] == tokens.MOMENT):
                list = self.array_to_list(quad[1])
                num_moment = self.get_variable_value(quad[2])
                res_moment = SpecialFunctions.moment(list, num_moment)
                self.set_variable_value(quad[3], res_moment)
            elif (quad[0] == tokens.MEDIAN):
                list = self.array_to_list(quad[1])
                median = SpecialFunctions.median(list)
                self.set_variable_value(quad[3], median)
            elif (quad[0] == tokens.VAR):
                list = self.array_to_list(quad[1])
                var = SpecialFunctions.var(list)
                self.set_variable_value(quad[3], var)
            elif (quad[0] == tokens.EXP_BERNOULLI):
                exp_bernoulli = SpecialFunctions.exp_bernoulli(value_left)
                self.set_variable_value(quad[3], exp_bernoulli)
            elif (quad[0] == tokens.VAR_BERNOULLI):
                var_bernoulli = SpecialFunctions.var_bernoulli(value_left)
                self.set_variable_value(quad[3], var_bernoulli)
            elif quad[0] == tokens.PROB_BINOMIAL:
                return_dir = quad[3]
                self.actual_index += 1
                quad = self.quadruples[self.actual_index]
                prob = self.get_variable_value(quad[1])
                n = self.get_variable_value(quad[2])
                k = self.get_variable_value(quad[3])
                prob_binomial = SpecialFunctions.prob_binomial(prob, n, k)
                self.set_variable_value(return_dir, prob_binomial)
            elif quad[0] == tokens.EXP_BINOMIAL:
                return_dir = quad[3]
                p = self.get_variable_value(quad[2])
                n = self.get_variable_value(quad[1])
                exp_bin = SpecialFunctions.exp_binomial(p, n)
                self.set_variable_value(return_dir, exp_bin)
            elif quad[0] == tokens.VAR_BINOMIAL:
                return_dir = quad[3]
                p = self.get_variable_value(quad[2])
                n = self.get_variable_value(quad[1])
                var_bin = SpecialFunctions.var_binomial(p, n)
                self.set_variable_value(return_dir, var_bin)
            elif quad[0] == tokens.PROB_GEOMETRIC:
                return_dir = quad[3]
                p = self.get_variable_value(quad[2])
                k = self.get_variable_value(quad[1])
                prob_geometric = SpecialFunctions.prob_geometric(k, p)
                self.set_variable_value(return_dir, prob_geometric)
            elif (quad[0] == tokens.EXP_GEOMETRIC):
                exp_geometric = SpecialFunctions.exp_geometric(value_left)
                self.set_variable_value(quad[3], exp_geometric)
            elif (quad[0] == tokens.VAR_GEOMETRIC):
                var_geometric = SpecialFunctions.var_geometric(value_left)
                self.set_variable_value(quad[3], var_geometric)
            elif (quad[0] == tokens.PLOT_HISTOGRAM):
                list = self.array_to_list(quad[1])
                SpecialFunctions.plot_histogram(list)
                
            self.actual_index += 1
        self.print_stuff()

    """ This functions internally converts an array to a pyhton list """
    def array_to_list(self, direction):
        list = []
        while self.get_variable_value(direction) != '@':
            list.append(self.get_variable_value(direction))
            direction += 1
        return list

    """ Reads the quadruples from the .stv file that the compiler created """
    def get_quadruples(self, file_name):
        quad_file = open(file_name, 'rb')
        file_array = pickle.load(quad_file)
        self.quadruples = file_array[0]
        self.constants = file_array[1]
        self.start_index = 0
        self.cast_constants()
        quad_file.close()
