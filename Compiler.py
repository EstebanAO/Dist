from collections import deque

TYPE = "tipo"
VARS = "vars"
PARAMS = 'params'
class Compiler:
    def __init__(self):
        self.pending_ids = []
        self.current_function = "global"
        self.current_variable = ''
        self.functions = {
            "global": {
                TYPE: "void",
                VARS: {},
                PARAMS: []
            }
        }
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

"""
compiler = Compiler()
compiler.funciones["global"][VARS]["vargloba14"] = (CHAR, 1, 0, False)
print(compiler.funciones["global"][VARS]["vargloba14"][3])
"""

"""
					"varglobal1": (INT, 1, 0, False),
					"varglobal2": (FLOAT, 4, 1, True),
					"vargloba13": (INT, 5, 5, True),
					"""

"""
TYPE = "tipo"
VARS = "vars"
VOID = "void"
INT = "int"
FLOAT = "float"
CHAR = "char"
"""
