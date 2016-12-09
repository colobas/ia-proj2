import sys

def read_Dimacs(filename):
    file = open(filename, 'r')

    N_variables = -1
    N_clauses = -1
    formula = []

    for line in file:
        if line.startswith('c'):
            continue
        if line.startswith('p'):
            aux = line.split(' ')

            if aux[1] != 'cnf':
                print("Not a CNF problem")
                sys.exit(-1)

            N_variables = int(aux[2])
            N_clauses = int(aux[3])
        else:
            clause = [int(aux) for aux in line.split(' ')]
            if clause[-1] != 0:
                print('Line not ending in 0')
                sys.exit(-1)
            formula.append(clause[:-1])
    if N_clauses != len(formula):
        print('Number of clauses dont match')
        sys.exit(-1)
    if N_variables != len(set( abs(aux) for clause in formula for aux in clause)):
        print('Number of variables dont match')
        sys.exit(-1)
    print(formula)
    return formula