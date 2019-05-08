# Omar Iván Flores Quijada
# Esteban Arocha Ortuño
# Enero - Mayo 2019
# ITESM

import sys
from VirtualMachine import VirtualMachine
def main(argv):
    a = VirtualMachine()
    a.run(argv[1])

if __name__ == '__main__':
    main(sys.argv)
