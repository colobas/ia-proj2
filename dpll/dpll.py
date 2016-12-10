def sat_clause(clause, v):
    if set(clause).intersection(v):
        return True
    return False

def sat_all(f, v):
    for clause in f:
        if clause == [] or not sat_clause(clause, v):
            return False
    return True

def unsat(f,v):
    for clause in f:
        if unsat_clause(clause, v):
            return True
    return False

def unsat_clause(clause, v):
    neg_v = [-x for x in v]

    if len(set(clause).intersection(neg_v)) == len(clause):
        return True

    return False

def get_unit_clause(f,v):
    def unassigned_literals(clause):
        unit_lit = [l for l in clause if l not in v and -l not in v]
        return unit_lit

    for clause in f:
        unit_lit = unassigned_literals(clause)
        if len(unit_lit) == 1:
            f = remove_falses([clause for clause in f if unit_lit[0] not in clause], unit_lit[0])
            return unit_lit[0], f
    return None, None

def get_pure_literal(f):
    all_literals = [l for clause in f for l in clause]
    for l in all_literals:
        if -l not in all_literals:
            return l, [clause for clause in f if l not in clause]

    return None, None

def get_symbols(f):
    symbols = list(set([abs(l) for clause in f for l in clause]))

    return symbols

def remove_falses(f, lit):
    x = f.copy()

    for i in range(0, len(x)):
        if -lit in x[i]:
            ind = x[i].index(-lit)
            x[i] = x[i][0:ind] + x[i][ind + 1:]
    return x

def remove_clauses(f, lit):
    return [clause for clause in f if lit not in clause]

def solver_DPLL(f):
    def remove(sym, l):
        x = sym.index(l)
        return sym[0:x] + sym[x+1:]

    def dfs(f, symbols, v):
        if sat_all(f,v):
            return v
        elif unsat(f,v):
            return False
        else:
            lit, h = get_unit_clause(f,v)
            if lit:
                #print("Found unit clause", lit)
                return dfs(h, remove(symbols, abs(lit)), v+[lit])

            lit, h = get_pure_literal(f)
            if lit:
                #print("Found pure literal", lit)
                return dfs(h, remove(symbols, abs(lit)), v+[lit])

            lit, sym = symbols[0], symbols[1:]

            print("Doing branching with", lit)
            f1 = remove_falses(f, lit)
            f1 = remove_clauses(f1, lit)

            f2 = remove_falses(f, -lit)
            f2 = remove_clauses(f2, -lit)

            return dfs(f1,sym, v+[lit]) or dfs(f2, sym, v+[-lit])

    return dfs(f, get_symbols(f), [])
