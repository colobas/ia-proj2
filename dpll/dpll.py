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

#@profile
def first_pass(old_f, v, lits, sym):
    f = old_f
    while True:
        new_f = []
        neg_v = [-x for x in v]
        neg_lits = [-l for l in lits]

        if len(lits.intersection(neg_lits)) > 0:
            return False, None, None

        unit_clauses = set()
        all_literals = set()

        for clause in f:
            if unsat_clause(clause, neg_v):
                return False, None, None

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

        if len(unit_clauses) == 0:
            return new_f, v, sym

        lits = unit_clauses.difference(lits)
        f = new_f.copy()
        v.update(unit_clauses)
        sym.difference_update(set([abs(x) for x in unit_clauses]))

#@profile
def dfs(old_f, sym, v, lit):
    if lit != 0:
        #print("branch with {}".format(lit))
        v.add(lit)
        #sym.remove(abs(lit))

    if len(sym) == 0:
        return False

    if lit != 0:
        f, v, sym = first_pass(old_f, v, {lit}, sym)
    else:
        f, v, sym = first_pass(old_f, v, set(), sym)

    if f == False:
        return False

    if sat_all(old_f,v):
        return v

    #l = max(sym, key = lambda x: sum([1 for clause in f if x in clause or -x in clause]))
    l = sym.pop()
    return dfs(f, sym.copy(), v.copy(), l) or dfs(f, sym, v, -l)


def solver_DPLL(f):
    no_dups = set()
    for clause in f:
        no_dups.add(frozenset(clause))

    new_f = [set(cl) for cl in no_dups]
    print("removed {} duplicates".format(len(f)-len(no_dups)))

    symbols = get_symbols(new_f)
    return dfs(new_f, symbols, set(), 0)
