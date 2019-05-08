import sys
from VirtualMachine import VirtualMachine
def main(argv):
    a = VirtualMachine()
    a.run(argv[1])

if __name__ == '__main__':
    main(sys.argv)
