from collections import deque
	
TYPE = "tipo"
VARS = "vars"
	
class Compiler:
	def __init__(self):
		self.pending_ids = []
		self.current_function = "global"
		self.functions = {
			"global": {
				TYPE: "void", 
				VARS: {}
			}
		}
	def push_id(self, id):
		self.pending_ids.append(id)
		
	def add_variables(self, type):
		while (len(self.pending_ids) > 0):
			name = self.pending_ids.pop()
			self.functions[self.current_function][VARS][name] = (type, 1, 0, False)
			
	def switch_context(self, function_name):
		self.current_function = function_name
		if function_name in self.functions:
			raise NameError('Function ', function_name, ' already exists')	
		self.functions[function_name] = {TYPE: "", VARS: {}}
		
	
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