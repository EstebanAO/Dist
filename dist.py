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

def main(argv):
    input = FileStream(argv[1])
    lexer = distLexer(input)
    stream = CommonTokenStream(lexer)
    parser = distParser(stream)
    parser._listeners = [ MyErrorListener() ]
    tree = parser.dist()
    printer = distListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

if __name__ == '__main__':
    main(sys.argv)
