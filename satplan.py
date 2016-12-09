from encoder.linencoder import encode,decode
from encoder.Domain import Domain
from dpll.solver import solver

import sys


def step_t(domain, t):
    sent = encode(domain, t)
    with open("res.txt", "w") as f:
        print("p cnf {} {}".format(sent.var_cnt-1, len(sent.sentence)), file=f)
        for line in sent.sentence:
            print(line, file=f)

    return sent


domain = Domain(sys.argv[1])
t = 0
while True:
    t += 1
    sentence = step_t(domain, t)
    sol = solver("res.txt")
    if not sol:
        continue

    decode(domain, sentence, sol, t)
    break
