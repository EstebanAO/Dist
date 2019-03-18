import sys
from antlr4 import *
from distLexer import distLexer
from distListener import distListener
from distParser import distParser
	
class distPrintListener(distListener):
    def exitVars_arreglo(self, ctx):
        print("")
		
def main(argv):
	input = FileStream(argv[1])
	lexer = distLexer(input)
	stream = CommonTokenStream(lexer)
	parser = distParser(stream)
	tree = parser.dist()
	printer = distPrintListener()
	walker = ParseTreeWalker()
	walker.walk(printer, tree)
	
if __name__ == '__main__':
    main(sys.argv)