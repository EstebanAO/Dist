import pickle
import tokens
import limits
from collections import deque
from semantic_cube import SEM_CUBE

class Compiler:
    def __init__(self):
        #Counters
        self.g_char = limits.G_CHAR - 1
        self.g_int = limits.G_INT - 1
        self.g_bool = limits.G_BOOL - 1
        self.g_float = limits.G_FLOAT - 1
        self.l_char = limits.L_CHAR - 1
        self.l_int = limits.L_INT - 1
        self.l_bool = limits.L_BOOL - 1
        self.l_float = limits.L_FLOAT - 1
        self.p_char = limits.P_CHAR - 1
        self.p_int = limits.P_INT - 1
        self.p_bool = limits.P_BOOL - 1
        self.p_float = limits.P_FLOAT - 1
        self.c_char = limits.C_CHAR - 1
        self.c_int = limits.C_INT - 1
        self.c_bool = limits.C_BOOL - 1
        self.c_float = limits.C_FLOAT - 1
        self.c_string = limits.C_STRING - 1

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

    def get_pointer_direction(self, type):
        if type == tokens.INT:
            self.p_int += 1
            return self.p_int
        elif type == tokens.CHAR:
            self.p_char += 1
            return self.p_char
        elif type == tokens.BOOL:
            self.p_bool += 1
            return self.p_bool
        elif type == tokens.FLOAT:
            self.p_float += 1
            return self.p_float

    def add_variables(self, type):
        while (len(self.pending_ids) > 0):
            name = self.pending_ids.pop()
            self.functions[self.current_function][tokens.VARS][name] = [type, self.get_variable_direction(type), None, None]

    def switch_context(self, function_name):
        self.l_char = limits.L_CHAR - 1
        self.l_int = limits.L_INT - 1
        self.l_bool = limits.L_BOOL - 1
        self.l_float = limits.L_FLOAT - 1
        self.p_char = limits.P_CHAR - 1
        self.p_int = limits.P_INT - 1
        self.p_bool = limits.P_BOOL - 1
        self.p_float = limits.P_FLOAT - 1
        self.current_function = function_name
        if function_name in self.functions:
            raise NameError('Function ', function_name, ' already exists')
        self.functions[function_name] = {tokens.TYPE: "", tokens.VARS: {}, tokens.PARAMS: [], tokens.START: len(self.quadruples)}

    def update_direction_counter(self, type, count):
        if type == tokens.CHAR:
            if self.current_function == tokens.GLOBAL:
                if self.g_char + count >= limits.G_INT:
                    raise MemoryError('Memory error')
                self.g_char += count
            else:
                if self.l_char + count >= limits.L_INT:
                    raise MemoryError('Memory error')
                self.l_char += count
        elif type == tokens.INT:
            if self.current_function == tokens.GLOBAL:
                if self.g_int + count >= limits.G_BOOL:
                    raise MemoryError('Memory error')
                self.g_int += count
            else:
                if self.l_int + count >= limits.L_BOOL:
                    raise MemoryError('Memory error')
                self.l_int += count
        elif type == tokens.BOOL:
            if self.current_function == tokens.GLOBAL:
                if self.g_bool + count >= limits.G_FLOAT:
                    raise MemoryError('Memory error')
                self.g_bool += count
            else:
                if self.l_bool + count >= limits.L_FLOAT:
                    raise MemoryError('Memory error')
                self.l_bool += count
        elif type == tokens.FLOAT:
            if self.current_function == tokens.GLOBAL:
                if self.g_float + count >= limits.L_CHAR:
                    raise MemoryError('Memory error')
                self.g_float += count
            else:
                if self.l_float + count >= limits.C_CHAR:
                    raise MemoryError('Memory error')
                self.l_float += count

    def add_array_one_dim(self, dim_one, type):
        name = self.pending_ids.pop()
        if dim_one < 1:
            raise IndexError('Array: ', name, ' size must be grater than zero')
        direction = self.get_variable_direction(type)
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
        self.functions[self.current_function][tokens.VARS][self.current_variable] = ['', None, None, None]
        self.functions[self.current_function][tokens.PARAMS].append(name)

    def print_tables(self):
        for func, value in self.functions.items():
            print('Funcion: ', func, value[tokens.TYPE])
            for var, data in value[tokens.VARS].items():
                print("data ", data)
                print("   ", var)
                print("      Tipo     : ", data[0])
                print("      Dirección: ", data[1])
                print("      Dim 1    : ", data[2])
                print("      Dim 2    : ", data[3])

    # Quadruples logic
    #  arrVar [valor, tipoValor, tipoEstructura, pos1, pos2 ]
    def push_variable_data(self, id):
        var_context = self.get_variable_context(id)
        if var_context == None:
            raise NameError('Variable: ', id, ' does not exist in context')
        variable = self.functions[var_context][tokens.VARS][id]
        self.p_values.append(variable[1])

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

    def generate_operation_quadruple(self, hierarchy):
        if len(self.p_operators) == 0:
            return
        if hierarchy == tokens.PLUS:
            array_symbol = [tokens.PLUS, tokens.MINUS]
        elif hierarchy == tokens.MULT:
            array_symbol = [tokens.MULT, tokens.DIV]
        elif hierarchy == tokens.GREATER:
            array_symbol = [tokens.GREATER, tokens.GREATER_EQ, tokens.LESS, tokens.LESS_EQ, tokens.EQU, tokens.DIFF]
        elif hierarchy == tokens.AND:
            array_symbol = [tokens.AND]
        elif hierarchy == tokens.OR:
            array_symbol = [tokens.OR]

        top = self.p_operators[-1]
        if top in array_symbol:
            right_operand = self.p_values.pop()
            left_operand = self.p_values.pop()
            operator = self.p_operators.pop()
            type_right_operand = self.get_direction_type(right_operand)
            type_left_operand = self.get_direction_type(left_operand)
            new_type = SEM_CUBE[type_right_operand][type_left_operand][operator]
            if new_type == tokens.ERROR:
                raise NameError('Type Mismatch Error: ', right_operand[1] , ' does not match ' , left_operand[1])
            new_direction = self.get_variable_direction(new_type)
            self.quadruples.append([operator, left_operand, right_operand, new_direction])
            self.p_values.append(new_direction)

    def get_variable(self, id):
        var_context = self.get_variable_context(id)
        if var_context == None:
            raise NameError('Variable: ', id, ' does not exist in context')
        variable = self.functions[var_context][tokens.VARS][id]
        return variable[1]

    def generate_assign_quadruple(self, to_assign_direction):
        assign_value_direction = self.p_values.pop()
        to_assign_type = self.get_direction_type(to_assign_direction)
        assign_value_type = self.get_direction_type(assign_value_direction)
        new_type = SEM_CUBE[to_assign_type][assign_value_type]
        if new_type == tokens.ERROR:
            raise NameError('Type Mismatch Error: ', to_assign_type , ' does not match ', assign_value_type)
        self.quadruples.append([tokens.ASSIGN, assign_value_direction, None, to_assign_direction])

    def add_new_line(self):
        self.quadruples.append([tokens.PRINT_NEW_LINE, None, None, None])

    def generate_print_quadruple(self):
        print("lo p hay", self.p_values)
        self.quadruples.append([tokens.PRINT, None, None, self.p_values.pop()])

    def generate_read_array_quadruple(self):
        self.quadruples.append([tokens.READ, None, None, self.p_values.pop()])

    def generate_read_quadruple(self, id):
        var_context = self.get_variable_context(id)
        if var_context == None:
            raise NameError('Variable: ', id, ' does not exist in context')
        direction = self.functions[var_context][tokens.VARS][id][1]
        self.quadruples.append([tokens.READ, None, None, direction])

    #Conditionals
    def generate_return_quadruple(self):
        direction = self.p_values[-1]
        self.quadruples.append([tokens.RETURN, None, None, direction])

    def generate_go_to_f(self):
        self.add_breadcrumb()
        condition = self.p_values.pop()
        if self.get_direction_type(condition) != tokens.BOOL:
            raise TypeError('If statements must evaluate boolean values')
        self.quadruples.append([tokens.GO_TO_F, condition, None, None])

    def complete_go_to_f(self):
        quad_index = self.p_jumps.pop()
        self.quadruples[quad_index][3] = len(self.quadruples)

    def generate_go_to_main(self):
        self.quadruples.append([tokens.GO_TO, None, None, None])
        self.p_jumps.append(len(self.quadruples))

    def complete_go_to_main(self):
        quad_index = self.p_jumps.pop()
        self.quadruples[quad_index-1][3] = len(self.quadruples)

    def generate_else_go_to(self):
        quad_index = self.p_jumps.pop()
        self.quadruples[quad_index][3] = len(self.quadruples) + 1
        self.add_breadcrumb()
        self.quadruples.append([tokens.GO_TO, None, None, None])

    def add_breadcrumb(self):
        self.p_jumps.append(len(self.quadruples))

    def end_of_while(self):
        quad_index = self.p_jumps.pop()
        self.quadruples[quad_index][3] = len(self.quadruples) + 1
        quad_index = self.p_jumps.pop()
        self.quadruples.append([tokens.GO_TO, None, None, quad_index])

    def assign_param_direction(self, function_call):
        var_name = self.functions[function_call][tokens.PARAMS][self.c_function_params]
        self.c_function_params += 1
        variable = self.functions[function_call][tokens.VARS][var_name]
        var_type = variable[0]
        var_direction = variable[1]
        argument = self.p_values.pop()
        argument_type = self.get_direction_type(argument)
        if (argument_type != var_type):
            raise TypeError('Argument type error')
        self.quadruples.append([tokens.ASSIGN_PARAM, argument, None, var_direction])

    def generate_era_quadruple(self):
        self.quadruples.append([tokens.ERA, None, None, None])

    def generate_go_sub_quadruple(self, name):
        start_direction = self.functions[name][tokens.START]
        direction_type = self.functions[name][tokens.TYPE]
        direction_temp = self.get_variable_direction(direction_type)
        self.p_values.append(direction_temp)
        self.quadruples.append([tokens.GO_SUB, direction_temp, None, start_direction])
        self.c_function_params = 0
        self.p_operators.pop()

    def add_fake_bottom(self):
        self.p_operators.append('(')

    # function that receives a variable id and returns its corresponding context
    def get_variable_context(self, var_id):
        if var_id in self.functions[self.current_function][tokens.VARS]:
            return self.current_function
        elif var_id in self.functions[tokens.GLOBAL][tokens.VARS]:
            return tokens.GLOBAL
        else:
            return None

    # function that raises an error when the variable is not a one dimension array
    def verify_one_dim_array(self, function_id, var_id):
        if self.functions[function_id][tokens.VARS][var_id][2] == None:
            raise TypeError('Variable: ', var_id, ' is not an array')
        if self.functions[function_id][tokens.VARS][var_id][3] != None:
            raise TypeError('Variable: ', var_id, ' is a two dimention array')

    # function that raises an error when the variable is not a two dimension array
    def verify_two_dim_array(self, function_id, var_id):
        if self.functions[function_id][tokens.VARS][var_id][2] == None:
            raise TypeError('Variable: ', var_id, ' is not an array')
        if self.functions[function_id][tokens.VARS][var_id][3] == None:
            raise TypeError('Variable: ', var_id, ' is not a two dimention array')

    def access_array_dim_one(self, id):
        array_context = self.get_variable_context(id)
        print(" > > > < < < ", array_context)
        if array_context == None:
            raise NameError('Variable: ', id, ' does not exist in context')
        self.verify_one_dim_array(array_context, id)

        dim_one = self.functions[array_context][tokens.VARS][id][2][0]
        direction = self.functions[array_context][tokens.VARS][id][1]
        type = self.functions[array_context][tokens.VARS][id][0]

        value = self.p_values.pop()
        temp_direction = self.get_pointer_direction(type)

        self.quadruples.append([tokens.VER, value, None, dim_one])
        self.current_cte_type = tokens.INT
        self.push_constant_data(direction)
        constant = self.p_values.pop()
        self.quadruples.append([tokens.PLUS_POINTER, value, constant, temp_direction])
        self.p_values.append(temp_direction) # push pointer to array position
        self.p_operators.pop() # pop fake bottom

    def access_array_dim_two(self, id):
        array_context = self.get_variable_context(id)
        if array_context == None:
            raise NameError('Variable: ', id, ' does not exist in context')
        self.verify_two_dim_array(array_context, id)

        dim_one = self.functions[array_context][tokens.VARS][id][2][0]
        m = self.functions[array_context][tokens.VARS][id][2][1] ######
        dim_two = self.functions[array_context][tokens.VARS][id][3][0]
        base_direction = self.functions[array_context][tokens.VARS][id][1]
        type = self.functions[array_context][tokens.VARS][id][0]

        pos_2 = self.p_values.pop()
        pos_1 = self.p_values.pop()

        self.quadruples.append([tokens.VER, pos_1, None, dim_one])

        self.current_cte_type = tokens.INT
        self.push_constant_data(m)
        m_direction = self.p_values.pop()

        t_jump = self.get_variable_direction(tokens.INT)

        self.quadruples.append([tokens.MULT, pos_1, m_direction, t_jump])
#        self.p_values.append(t_jump)

        self.quadruples.append([tokens.VER, pos_2, None, dim_two])

        t_offset = self.get_variable_direction(tokens.INT)
        self.quadruples.append([tokens.PLUS, t_jump, pos_2, t_offset])

        self.current_cte_type = tokens.INT
        self.push_constant_data(base_direction)
        constant = self.p_values.pop()
        temp_direction = self.get_pointer_direction(type)

        self.quadruples.append([tokens.PLUS_POINTER, t_offset, constant, temp_direction])
        self.p_values.append(temp_direction) # push pointer to array position
        #self.p_operators.pop() # pop fake bottom
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
