import copy

def sat_clause(clause, v):
    if clause.intersection(v):
        return True
    return False

def sat_all(f, v):
    for clause in f:
        if len(clause) == 0 or not sat_clause(clause, v):
            return False
    return True

def unsat(f,v):
    neg_v = [-x for x in v]
    for clause in f:
        if unsat_clause(clause, neg_v):
            return True
    return False

def unsat_clause(clause, neg_v):
    return len(clause.intersection(neg_v)) == len(clause)

def unassigned_literals(clause, v):
    unit_lit = [l for l in clause if l not in v and -l not in v]
    return unit_lit

def get_unit_clause(f,v):
    for clause in f:
        unit_lit = unassigned_literals(clause, v)
        if len(unit_lit) == 1:
            n = remove_falses([clause for clause in f if unit_lit[0] not in clause], unit_lit[0])
            return unit_lit[0], n
    return None, None

def get_pure_literal(f):
    all_literals = set()
    for clause in f:
        all_literals.update(clause)

    for l in all_literals:
        if -l not in all_literals:
            return l
    return None

def get_symbols(f):
    return set([abs(l) for clause in f for l in clause])

def remove_falses(f, lit):
    for clause in f:
        if -lit in clause:
            clause.remove(-lit)
    return f

def remove_clauses(f, lit):
    return [clause for clause in f if lit not in clause]

@profile
def first_pass(old_f, v, lits, must_copy):
    new_f = []
    neg_v = [-x for x in v]
    neg_lits = [-l for l in lits]

    if len(lits.intersection(neg_lits)) > 0:
        return False, None

    unit_clauses = set()
    all_literals = set()
    to_delete = []

    for clause in old_f:
        if unsat_clause(clause, neg_v):
            return False, None

        cl = clause.difference(neg_lits)
        # remove symbols from clauses where they yield false

        if len(clause) == 1: # if clause is a unit clause, remove it and store assignment
            unit_clauses.update(cl)
            continue

        if len(cl.intersection(lits)) > 0:
        # if any of the variables in lits is true, clause is true, remove it
            continue

        all_literals.update(cl)
        new_f.append(cl)


    for l in all_literals:
        if -l not in unit_clauses and -l not in all_literals:
            unit_clauses.add(l)

    return new_f, unit_clauses

#@profile
def dfs(old_f, symbols, old_v, lits, must_copy):
    #print("lits {}".format(lits))
    if must_copy:
        v = old_v.copy()
        sym = symbols.copy()
    else:
        v = old_v
        sym = symbols

    v.update(lits)
    sym.difference_update([abs(lit) for lit in lits])

    if sat_all(old_f,v):
        return v

    if len(sym) == 0:
        return False

    f, unit_clauses = first_pass(old_f, v, lits, must_copy)
    if f == False:
        return False

    if len(unit_clauses) != 0:
        return dfs(f, sym, v, unit_clauses, False)


    l = max(sym)
    return dfs(f, sym, v, set([l]), True) or dfs(f, sym, v, set([-l]), False)


def solver_DPLL(f):
    symbols = get_symbols(f)
    lit = min(symbols)
    return dfs(f, symbols, set(), set([lit]), True) or dfs(f, symbols, set(), set([-lit]), False)
