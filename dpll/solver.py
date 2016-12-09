from dimacs import *
from dpll import *
import sys


def solver(argv=sys.argv):
    tracing = True

    if len(argv) != 2:
        print("Wrong number of arguments")
        return -1

    try:
        filename = argv[1]
    except IOError:
        print("Could not open file")
        return -1

    formula = read_Dimacs(filename)
    solution = solver_DPLL(formula)

    return solution
