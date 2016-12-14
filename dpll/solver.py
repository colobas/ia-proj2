""" module to wrap dpll call"""

import sys
from dpll.dpll import dpll

def read_dimacs(lines):
    """ reads list of strings with DIMACS input, output a list of clauses """
    formula = list()

    for line in lines:
        if line[-1] != '0':
            print('Line not ending in 0')
            sys.exit(-1)
        line = line[:-2]
        clause = set([int(aux) for aux in line.split(' ')])
        formula.append(clause)

    return formula


def solver(lines):
    """ read DIMACS input from lines, and output dpll solution """
    formula = read_dimacs(lines)
    solution = dpll(formula)
    return solution
