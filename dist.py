import sys
import ntpath
from antlr4 import *
from distLexer import distLexer
from distListener import distListener
from distParser import distParser
from VirtualMachine import VirtualMachine

class distPrintListener(distListener):
    def exitVars_arreglo(self, ctx):
        print("")

def main(argv):
	print("\n- - - - - - - - compilación - - - - - - - -\n\n")
	input = FileStream(argv[1])
	lexer = distLexer(input)
	stream = CommonTokenStream(lexer)
	parser = distParser(stream)
	tree = parser.dist()
	printer = distPrintListener()
	walker = ParseTreeWalker()
	walker.walk(printer, tree)
	print("\n- - - - - - - - ejecución - - - - - - - -\n\n")
	a = VirtualMachine()
	fname, fext = ntpath.splitext(ntpath.basename(argv[1]))
	a.run(fname + '.stv')

if __name__ == '__main__':
    main(sys.argv)
