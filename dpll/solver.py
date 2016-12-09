from dpll.dimacs import *
from dpll.dpll import *
import sys


def solver(filename):
    tracing = True
    formula = read_Dimacs(filename)
    solution = solver_DPLL(formula)

    return solution
