from collections import deque
from semantic_cube import get_semantic_cube

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

class Compiler:
    def __init__(self):
        # Functions and variables tables
        self.pending_ids = []
        self.current_function = GLOBAL
        self.current_variable = ''
        self.functions = {
            GLOBAL: {
                TYPE: VOID,
                VARS: {},
                PARAMS: []
            }
        }

        # Quadruple
        self.temporal = 0
        self.quadruples = []
        self.p_values = [] # Variables and constants
        self.p_operators = [] # Operators
        self.current_cte_type = ''
        self.p_temporal = []
        self.cont_dim_1 = 0
        self.cont_dim_2 = 0
        self.current_array = ''

    def push_id(self, id):
        self.pending_ids.append(id)

    def add_variables(self, type):
        while (len(self.pending_ids) > 0):
            name = self.pending_ids.pop()
            self.functions[self.current_function][VARS][name] = [type, 1, 0, False]

    def switch_context(self, function_name):
        self.current_function = function_name
        if function_name in self.functions:
            raise NameError('Function ', function_name, ' already exists')
        self.functions[function_name] = {TYPE: "", VARS: {}, PARAMS: []}

    def add_variable(self, name, is_param):
        self.current_variable = name
        self.functions[self.current_function][VARS][self.current_variable] = ['', 1, 0, False]
        if (is_param):
            self.functions[self.current_function][PARAMS].append(name)

    def add_dimension_one(self, size):
        self.cont_dim_1 = int(size)
        self.cont_dim_2 = 0
        self.functions[self.current_function][VARS][self.current_variable][1] = int(size)
        self.functions[self.current_function][VARS][self.current_variable][3] = True

    def add_dimension_two(self, size):
        self.cont_dim_2 = int(size)
        self.functions[self.current_function][VARS][self.current_variable][2] = int(size)

    def add_type(self, type):
        self.functions[self.current_function][VARS][self.current_variable][0] = type

    def add_function_type(self, function_type):
        self.functions[self.current_function][TYPE] = function_type

    def print_tables(self):
        for func, value in self.functions.items():
            print('Funcion: ', func, value[TYPE])
            for var, data in value[VARS].items():
                print("   ", var)
                print("      Tipo: ", data[0])
                if(data[3]):
                    print("      Dim 1: ", data[1])
                    print("      Dim 2: ", data[2])


    # Quadruples logic
    #  arrVar [valor, tipoValor, tipoEstructura, pos1, pos2 ]
    def push_variable_data(self, id):
        if id in self.functions[self.current_function][VARS]:
            type = self.functions[self.current_function][VARS][id][0]
            self.p_values.append([id, type, VAR, None, None])
        elif id in self.functions[GLOBAL][VARS]:
            type = self.functions[GLOBAL][VARS][id][0]
            self.p_values.append([id, type, VAR, None, None])
        else:
            raise NameError('Variable: ' + id + ' does not exist in context')

    def push_constant_data(self, value):
        self.quadruples.append([ASSIGN, [value, self.current_cte_type, CTE, None, None], None, '_' + str(self.temporal)])
        self.p_values.append(['_' + str(self.temporal), self.current_cte_type, CTE, None, None])
        self.temporal += 1

    def push_operator(self, operator):
        self.p_operators.append(operator)

    def pop_operator(self):
        self.p_operators.pop()

    def generate_operation_quadruple(self, hierarchy):
        if len(self.p_operators) == 0:
            return
        if hierarchy == '+':
            array_symbol = ['+', '-']
        elif hierarchy == '*':
            array_symbol = ['*', '/']
        elif hierarchy == '>':
            array_symbol = ['>', '>=', '<', '<=', '==', '!=']
        elif hierarchy == '&&':
            array_symbol = ['&&']
        elif hierarchy == '||':
            array_symbol = ['||']

        top = self.p_operators[len(self.p_operators) - 1]
        if top in array_symbol:
            right_operand = self.p_values.pop()
            left_operand = self.p_values.pop()
            operator = self.p_operators.pop()
            new_type = get_semantic_cube()[right_operand[1]][left_operand[1]][operator]
            if new_type == ERROR:
                raise NameError('Type Mismatch Error: ', right_operand[1] , ' does not match ' , left_operand[1])
            self.quadruples.append([operator, left_operand, right_operand, '_' + str(self.temporal)])
            self.p_values.append(['_' + str( self.temporal), new_type, VAR, None, None])
            self.temporal = self.temporal + 1

    def generate_arr_pos_quadruple(self, id, dimension):
        if id in self.functions[self.current_function][VARS]:
            type = self.functions[self.current_function][VARS][id][0]
        elif id in self.functions[GLOBAL][VARS]:
            type = self.functions[GLOBAL][VARS][id][0]
        else:
            raise NameError('Variable: ' + id + ' does not exist in context')

        if dimension == 1:
            arr_value = [id, type, ARR, self.quadruples[-1][3], None]
        else:
            first_dimension = self.p_temporal.pop()
            arr_value = [id, type, ARR, first_dimension, self.quadruples[-1][3]]
        self.quadruples.append([ASSIGN, arr_value, None, '_' + str(self.temporal)])
        arr_temp = ['_' + str( self.temporal), arr_value[1], arr_value[2], arr_value[3], arr_value[4]]
        self.p_values.append(arr_temp)
        self.temporal = self.temporal + 1

    def get_variable(self, id):
        if id in self.functions[self.current_function][VARS]:
            type = self.functions[self.current_function][VARS][id][0]
            # is_Array = self.functions[self.current_function][VARS][id][3]
            # if is_array:
            #     raise TypeError ('')
            return ["", [id, type, VAR, None, None], "", id]
        elif id in self.functions[GLOBAL][VARS]:
            type = self.functions[GLOBAL][VARS][id][0]
            return ["", [id, type, VAR, None, None], "", id]
        else:
            raise NameError('Variable: ' + id + ' does not exist in context')

    def generate_assign_quadruple(self, quad_temp):
        expresion_to_assign = self.p_values.pop()
        new_type = get_semantic_cube()[expresion_to_assign[1]][quad_temp[1][1]][ASSIGN]
        if new_type == ERROR:
            raise NameError('Type Mismatch Error: ', expresion_to_assign[1] , ' does not match ' , quad_temp[1][1])
        self.quadruples.append([ASSIGN, expresion_to_assign[0], None, quad_temp[3]])

    def assign_new_single_pos(self):
        if self.current_variable in self.functions[self.current_function][VARS]:
            dim1 = self.functions[self.current_function][VARS][self.current_variable][1]
            dim2 = self.functions[self.current_function][VARS][self.current_variable][2]
            type = self.functions[self.current_function][VARS][self.current_variable][0]
        elif self.current_variable in self.functions[GLOBAL][VARS]:
            dim1 = self.functions[self.current_function][GLOBAL][self.current_variable][1]
            dim2 = self.functions[self.current_function][GLOBAL][self.current_variable][2]
            type = self.functions[self.current_function][GLOBAL][self.current_variable][0]
        else:
            raise NameError('Variable: ' + self.current_variable + ' does not exist in context')

        pos1 = dim1 - self.cont_dim_1
        pos2 = dim2 - self.cont_dim_2
        if dim2 == 0:
            self.cont_dim_1 -= 1
        else:
            self.cont_dim_2 -= 1

        arr_val = [self.current_variable, type, ARR, pos1, pos2]
        if type != self.quadruples[-1][1][1]:
            raise NameError('Type Mismatch Error in: ', self.current_variable)
        self.quadruples.append([ASSIGN, self.quadruples[-1][3], None, arr_val])

    def update_array_pos(self):
        if self.current_variable in self.functions[self.current_function][VARS]:
            dim2 = self.functions[self.current_function][VARS][self.current_variable][2]
        elif self.current_variable in self.functions[GLOBAL][VARS]:
            dim2 = self.functions[self.current_function][GLOBAL][self.current_variable][2]
        else:
            raise NameError('Variable: ' + self.current_variable + ' does not exist in context')
        if self.cont_dim_2 != 0:
            raise IndexError('Index out of range in: ', self.current_variable)
        else:
            self.cont_dim_1 -= 1
        self.cont_dim_2 = dim2


    def push_temporal(self):
        self.p_temporal.append(self.quadruples[-1][3])

    def print_quad(self):
        for idx, quad in enumerate(self.quadruples):
            print(str(idx) + " : " , quad)

    def print_piles(self):
        print(self.p_values)
        print(self.p_operators)
        print(self.quadruples)
