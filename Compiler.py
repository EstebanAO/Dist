from collections import deque
from semantic_cube import get_semantic_cube

VAR = "var"
CTE = "cte"
FUN = "fun"
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
ASIGN = '='
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
        self.functions[self.current_function][VARS][self.current_variable][1] = int(size)
        self.functions[self.current_function][VARS][self.current_variable][3] = True

    def add_dimension_two(self, size):
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
    def push_variable_data(self, id):
        if id in self.functions[self.current_function][VARS]:
            type = self.functions[self.current_function][VARS][id][0]
            self.p_values.append([id, type, VAR])
        elif id in self.functions[GLOBAL][VARS]:
            type = self.functions[GLOBAL][VARS][id][0]
            self.p_values.append([id, type, VAR])
        else:
            raise NameError('Variable: ' + id + ' does not exist in context')

    def push_constant_data(self, value):
        self.p_values.append([value, self.current_cte_type, CTE])
        print(self.p_values)

    def push_operator(self, operator):
        self.p_operators.append(operator)
        print(self.p_operators)

    def pop_operator(self):
        self.p_operators.pop()

    def generate_quadruple(self, hierarchy):
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
            self.quadruples.append([operator, left_operand, right_operand, str(self.temporal)])
            # print([operator, left_operand, right_operand, str(self.temporal)])
            self.p_values.append([str(self.temporal), new_type, VAR])
            self.temporal = self.temporal + 1


    def print_quad(self):
        for idx, quad in enumerate(self.quadruples):
            print(str(idx) + " : " , quad)

    def print_piles(self):
        print(self.p_values)
        print(self.p_operators)
        print(self.quadruples)
