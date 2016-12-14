"""SATPLAN implementation, using the linear encoder and the dpll modules"""

import sys
from encoder.linencoder import encode, decode
from encoder.Domain import Domain
from dpll.solver import solver


DOMAIN = Domain(sys.argv[1]) # parse input file and build corresponding domain
T = 0
while True:
    T += 1
    FORMULA = encode(DOMAIN, T) # encode domain for horizon T
    SOL = solver(FORMULA.sentence) # apply dpll in the obtained encoding
    if not SOL: # if FORMULA is unsatisfiable, increase time horizon
        continue

    # if FORMULA is satisfiable decode and print solution
    decode(DOMAIN, FORMULA, SOL, T)
    break
