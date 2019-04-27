import pickle
import tokens
from collections import deque
from semantic_cube import get_semantic_cube

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

class Compiler:
    def __init__(self):
        #Counters
        self.g_char = LIMIT_G_CHAR - 1
        self.g_int = LIMIT_G_INT - 1
        self.g_bool = LIMIT_G_BOOL - 1
        self.g_float = LIMIT_G_FLOAT - 1
        self.l_char = LIMIT_L_CHAR - 1
        self.l_int = LIMIT_L_INT - 1
        self.l_bool = LIMIT_L_BOOL - 1
        self.l_float = LIMIT_L_FLOAT - 1
        self.c_char = LIMIT_C_CHAR - 1
        self.c_int = LIMIT_C_INT - 1
        self.c_bool = LIMIT_C_BOOL - 1
        self.c_float = LIMIT_C_FLOAT - 1
        self.c_string = LIMIT_C_STRING - 1

        # Functions and variables tables
        self.program_name = ''
        self.pending_ids = []
        self.current_function = tokens.GLOBAL
        self.current_variable = ''
        self.functions = {
            tokens.GLOBAL: {
                tokens.TYPE: tokens.VOID,
                tokens.VARS: {},
                tokens.PARAMS: [],
                tokens.START: -1
            }
        }

        # Quadruple
        self.cte_values = {}
        self.temporal = 0
        self.quadruples = []
        self.p_values = [] # Variables and constants
        self.p_operators = [] # Operators
        self.current_cte_type = ''
        self.p_temporal = []
        self.p_jumps = []
        self.c_function_params = 0

        #Assign array
        self.id_arr = ''

    def save_program_name(self, prog_name):
        self.program_name = prog_name

    def push_id(self, id):
        self.pending_ids.append(id)

    def get_variable_direction(self, type):
        if type == tokens.INT:
            if self.current_function == tokens.GLOBAL:
                self.g_int += 1
                return self.g_int
            else:
                self.l_int += 1
                return self.l_int
        elif type == tokens.CHAR:
            if self.current_function == tokens.GLOBAL:
                self.g_char += 1
                return self.g_char
            else:
                self.l_char += 1
                return self.l_char
        elif type == tokens.BOOL:
            if self.current_function == tokens.GLOBAL:
                self.g_bool += 1
                return self.g_bool
            else:
                self.l_bool += 1
                return self.l_bool
        elif type == tokens.FLOAT:
            if self.current_function == tokens.GLOBAL:
                self.g_float += 1
                return self.g_float
            else:
                self.l_float += 1
                return self.l_float

    def add_variables(self, type):
        while (len(self.pending_ids) > 0):
            name = self.pending_ids.pop()
            self.functions[self.current_function][tokens.VARS][name] = [type, self.get_variable_direction(type), None, None]

    def switch_context(self, function_name):
        self.l_char = LIMIT_L_CHAR - 1
        self.l_int = LIMIT_L_INT - 1
        self.l_bool = LIMIT_L_BOOL - 1
        self.l_float = LIMIT_L_FLOAT - 1
        self.current_function = function_name
        if function_name in self.functions:
            raise NameError('Function ', function_name, ' already exists')
        self.functions[function_name] = {tokens.TYPE: "", tokens.VARS: {}, tokens.PARAMS: [], tokens.START: len(self.quadruples)}

    def update_direction_counter(self, type, count):

        if type == tokens.CHAR:
            if self.current_function == tokens.GLOBAL:
                if self.g_char + count >= LIMIT_G_INT:
                    raise MemoryError('Memory error')
                self.g_char += count
            else:
                if self.l_char + count >= LIMIT_L_INT:
                    raise MemoryError('Memory error')
                self.l_char += count
        elif type == tokens.INT:
            if self.current_function == tokens.GLOBAL:
                if self.g_int + count >= LIMIT_G_BOOL:
                    raise MemoryError('Memory error')
                self.g_int += count
            else:
                if self.l_int + count >= LIMIT_L_BOOL:
                    raise MemoryError('Memory error')
                self.l_int += count
        elif type == tokens.BOOL:
            if self.current_function == tokens.GLOBAL:
                if self.g_bool + count >= LIMIT_G_FLOAT:
                    raise MemoryError('Memory error')
                self.g_bool += count
            else:
                if self.l_bool + count >= LIMIT_L_FLOAT:
                    raise MemoryError('Memory error')
                self.l_bool += count
        elif type == tokens.FLOAT:
            if self.current_function == tokens.GLOBAL:
                if self.g_float + count >= LIMIT_L_CHAR:
                    raise MemoryError('Memory error')
                self.g_float += count
            else:
                if self.l_float + count >= LIMIT_C_CHAR:
                    raise MemoryError('Memory error')
                self.l_float += count

    def add_array_one_dim(self, dim_one, type):
        name = self.pending_ids.pop()
        if dim_one < 1:
            raise IndexError('Array: ', name, ' size must be grater than zero')
        direction = self.get_variable_direction(type)
        print(" > DIM1: ", dim_one)
        self.functions[self.current_function][tokens.VARS][name] = [type, direction, [dim_one, 0], None]
        self.update_direction_counter(type, dim_one)
        self.quadruples.append([tokens.FILL_ARRAY, None, None, direction + dim_one])

    def add_array_two_dim(self, dim_one, dim_two, type):
        name = self.pending_ids.pop()
        if dim_one < 1 or dim_two < 1:
            raise IndexError('Array: ', name, ' size must be grater than zero')
        direction = self.get_variable_direction(type)
        self.functions[self.current_function][tokens.VARS][name] = [type, direction, [dim_one, dim_two], [dim_two, 0]]
        self.update_direction_counter(type, dim_one * dim_two)
        self.quadruples.append([tokens.FILL_ARRAY, None, None, direction + dim_one * dim_two])

    def add_type(self, type):
        self.functions[self.current_function][tokens.VARS][self.current_variable][0] = type
        self.functions[self.current_function][tokens.VARS][self.current_variable][1] = self.get_variable_direction(type)

    def add_function_type(self, function_type):
        self.functions[self.current_function][tokens.TYPE] = function_type

    def add_param(self, name):
        self.current_variable = name
        self.functions[self.current_function][tokens.VARS][self.current_variable] = ['', None]
        self.functions[self.current_function][tokens.PARAMS].append(name)

    def print_tables(self):
        for func, value in self.functions.items():
            print('Funcion: ', func, value[tokens.TYPE])
            for var, data in value[tokens.VARS].items():
                print("   ", var)
                print("      Tipo     : ", data[0])
                print("      Dirección: ", data[1])
                print("      Dim 1    : ", data[2])
                print("      Dim 2    : ", data[3])



    # Quadruples logic
    #  arrVar [valor, tipoValor, tipoEstructura, pos1, pos2 ]
    def push_variable_data(self, id):
        if id in self.functions[self.current_function][tokens.VARS]:
            variable = self.functions[self.current_function][tokens.VARS][id]
            self.p_values.append(variable[1])
        elif id in self.functions[tokens.GLOBAL][tokens.VARS]:
            variable = self.functions[tokens.GLOBAL][tokens.VARS][id]
            self.p_values.append(variable[1])
        else:
            raise NameError('Variable: ', id, ' does not exist in context')

    def push_constant_data(self, value):
        if self.current_cte_type == tokens.INT:
            self.c_int += 1
            self.p_values.append(self.c_int)
            self.cte_values[self.c_int] = value
        elif self.current_cte_type == tokens.CHAR:
            self.c_char += 1
            self.p_values.append(self.c_char)
            self.cte_values[self.c_char] = value
        elif self.current_cte_type == tokens.FLOAT:
            self.c_float += 1
            self.p_values.append(self.c_float)
            self.cte_values[self.c_float] = value
        elif self.current_cte_type == tokens.BOOL:
            self.c_bool += 1
            self.p_values.append(self.c_bool)
            self.cte_values[self.c_bool] = value
        elif self.current_cte_type == tokens.STRING:
            self.c_string += 1
            self.p_values.append(self.c_string)
            self.cte_values[self.c_string] = value

    def push_operator(self, operator):
        self.p_operators.append(operator)

    def pop_operator(self):
        self.p_operators.pop()

    def get_direction_type(self, direction):
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

    def generate_operation_quadruple(self, hierarchy):
        if len(self.p_operators) == 0:
            return
        if hierarchy == tokens.PLUS:
            array_symbol = ['+', '-']
        elif hierarchy == tokens.MULT:
            array_symbol = ['*', '/']
        elif hierarchy == tokens.GREATER:
            array_symbol = ['>', '>=', '<', '<=', '==', '!=']
        elif hierarchy == tokens.AND:
            array_symbol = ['&&']
        elif hierarchy == tokens.OR:
            array_symbol = ['||']

        top = self.p_operators[ -1 ]
        if top in array_symbol:
            right_operand = self.p_values.pop()
            left_operand = self.p_values.pop()
            operator = self.p_operators.pop()
            type_right_operand = self.get_direction_type(right_operand)
            type_left_operand = self.get_direction_type(left_operand)
            new_type = get_semantic_cube()[type_right_operand][type_left_operand][operator]
            if new_type == tokens.ERROR:
                raise NameError('Type Mismatch Error: ', right_operand[1] , ' does not match ' , left_operand[1])
            new_direction = self.get_variable_direction(new_type)
            self.quadruples.append([operator, left_operand, right_operand, new_direction])
            self.p_values.append(new_direction)

    def get_variable(self, id):
        if id in self.functions[self.current_function][tokens.VARS]:
            variable = self.functions[self.current_function][tokens.VARS][id]
            return variable[1]
        elif id in self.functions[tokens.GLOBAL][tokens.VARS]:
            variable = self.functions[tokens.GLOBAL][tokens.VARS][id]
            return variable[1]
        else:
            raise NameError('Variable: ', id, ' does not exist in context')

    def generate_assign_quadruple(self, to_assign_direction):
        assign_value_direction = self.p_values.pop()
        to_assign_type = self.get_direction_type(to_assign_direction)
        assign_value_type = self.get_direction_type(assign_value_direction)
        new_type = get_semantic_cube()[to_assign_type][assign_value_type]
        if new_type == tokens.ERROR:
            raise NameError('Type Mismatch Error: ', to_assign_type , ' does not match ', assign_value_type)
        self.quadruples.append([tokens.ASSIGN, assign_value_direction, None, to_assign_direction])

    def add_new_line(self):
        self.quadruples.append([tokens.PRINT_NEW_LINE, None, None, None])

    def generate_print_quadruple(self):
        self.quadruples.append([tokens.PRINT, None, None, self.p_values.pop()])

    def generate_read_quadruple(self, id):
        if id in self.functions[self.current_function][tokens.VARS]:
            direction = self.functions[self.current_function][tokens.VARS][id][1]
            self.quadruples.append([tokens.READ, None, None, direction])
        elif id in self.functions[tokens.GLOBAL][tokens.VARS]:
            direction = self.functions[tokens.GLOBAL][tokens.VARS][id][1]
            self.quadruples.append([tokens.READ, None, None, direction])
        else:
            raise NameError('Variable: ', id, ' does not exist in context')

    #Conditionals
    def generate_return_quadruple(self):
        direction = self.p_values[-1]
        self.quadruples.append([tokens.READ, None, None, direction])

    def generate_go_to_f(self):
        self.add_breadcrumb()
        condition = self.p_values.pop()
        if self.get_direction_type(condition) != tokens.BOOL:
            raise TypeError('If statements must evaluate boolean values')
        self.quadruples.append([tokens.READ, condition, None, None])

    def complete_go_to_f(self):
        quad_index = self.p_jumps.pop()
        self.quadruples[quad_index][3] = len(self.quadruples)

    def generate_else_go_to(self):
        quad_index = self.p_jumps.pop()
        self.quadruples[quad_index][3] = len(self.quadruples) + 1
        self.add_breadcrumb()
        self.quadruples.append([tokens.READ, None, None, None])

    def add_breadcrumb(self):
        self.p_jumps.append(len(self.quadruples))

    def end_of_while(self):
        quad_index = self.p_jumps.pop()
        self.quadruples[quad_index][3] = len(self.quadruples) + 1
        quad_index = self.p_jumps.pop()
        self.quadruples.append([tokens.READ, None, None, quad_index])

    def assign_param_direction(self, function_call):
        var_name = self.functions[function_call][tokens.PARAMS][self.c_function_params]
        self.c_function_params += 1
        variable = self.functions[function_call][tokens.VARS][var_name]
        var_type = variable[0]
        var_direction = variable[1]
        argument = self.p_values.pop()
        argument_type = self.get_direction_type(argument)
    #    print(argument_type, var_type)
        if (argument_type != var_type):
            raise TypeError('Argument type error')
        self.quadruples.append([tokens.ASSIGN, argument, None, var_direction])

    def generate_era_quadruple(self):
        self.quadruples.append([tokens.END_PROC, None, None, None])

    def generate_go_sub_quadruple(self, name):
        start_direction = self.functions[name][tokens.START]
        direction_type = self.functions[name][tokens.TYPE]
        direction_temp = self.get_variable_direction(direction_type)
        self.p_values.append(direction_temp)
        self.quadruples.append([tokens.GO_SUB, direction_temp, None, start_direction])
        self.c_function_params = 0

    def add_fake_bottom(self):
        self.p_operators.append('(')

    def access_array_dim_one(self, id):
        #id = self.id_assign
        print("Accessing array", id)
        if id in self.functions[self.current_function][tokens.VARS]:
            if self.functions[self.current_function][tokens.VARS][id][2] == None:
                raise TypeError('Variable: ', id, ' is not a one dimention array')
            if self.functions[self.current_function][tokens.VARS][id][3] != None:
                raise TypeError('Variable: ', id, ' is a two dimention array')
            dim_one = self.functions[self.current_function][tokens.VARS][id][2][0]
            direction = self.functions[self.current_function][tokens.VARS][id][1]
            type = self.functions[self.current_function][tokens.VARS][id][0]
        elif id in self.functions[tokens.GLOBAL][tokens.VARS]:
            if self.functions[tokens.GLOBAL][tokens.VARS][id][2] == None:
                raise TypeError('Variable: ', id, ' is not a one dimention array')
            if self.functions[tokens.GLOBAL][tokens.VARS][id][3] != None:
                raise TypeError('Variable: ', id, ' is a two dimention array')
            dim_one = self.functions[tokens.GLOBAL][tokens.VARS][id][2][0]
            direction = self.functions[tokens.GLOBAL][tokens.VARS][id][1]
            type = self.functions[tokens.GLOBAL][tokens.VARS][id][0]
        else:
            raise NameError('Variable: ', id, ' does not exist in context')
        #print(self.p_values)
        value = self.p_values.pop()
        temp_direction = self.get_variable_direction(tokens.INT)
        print(" >> DIM1: ", dim_one);
        self.quadruples.append([tokens.VER, value, None, dim_one])
        self.current_cte_type = tokens.INT
        self.push_constant_data(direction)
        constant = self.p_values.pop()
        self.quadruples.append([tokens.PLUS, value, constant, temp_direction])
        self.p_values.append(str(temp_direction))
        self.p_operators.pop()

    #Functions
    def generate_end_proc(self):
        self.quadruples.append([tokens.END_PROC, None, None, None])

    def print_quad(self):
        self.print_tables()
        print(self.cte_values)
        for idx, quad in enumerate(self.quadruples):
            print(str(idx) + " : " , quad)

    def write_quadruples(self):
        quadruples = [self.quadruples, self.cte_values, self.functions['main'][tokens.START]]
        file_name = self.program_name + '.stv'
        file = open(file_name, 'wb')
        pickle.dump(quadruples, file)
        file.close()

    def print_piles(self):
        print(self.p_values)
        print(self.p_operators)
        print(self.quadruples)
