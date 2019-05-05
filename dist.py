import sys
import ntpath
import tokens
from antlr4 import *
from distLexer import distLexer
from distListener import distListener
from distParser import distParser
from VirtualMachine import VirtualMachine
from antlr4.error.ErrorListener import ErrorListener

class MyErrorListener( ErrorListener ):
    def __init__(self):
        super(MyErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if offendingSymbol.text in tokens.SPECIAL_TOKENS:
            print(offendingSymbol.text, ' is a reserved token in line ', line, ' col ', column)
        else:
            print(msg, " in line ", line, " column ", column)
        sys.exit()

class distPrintListener(distListener):
    def exitVars_arreglo(self, ctx):
        print("")

def main(argv):
    print("\n- - - - - - - - compilación - - - - - - - -\n\n")
    input = FileStream(argv[1])
    lexer = distLexer(input)
    stream = CommonTokenStream(lexer)
    parser = distParser(stream)
    parser._listeners = [ MyErrorListener() ]
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
