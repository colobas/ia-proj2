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
def first_pass(old_f, v, lit):
    new_f = []
    neg_v = [-x for x in v]
    unit_clause = None
    pure = None
    all_literals = set()

    for clause in old_f:
        if unsat_clause(clause, neg_v):
            return False, None, None
        if -lit in clause:
            # remove symbol from clauses where it yields false
            cl = clause.copy()
            cl.remove(-lit)
            new_f.append(cl)
            all_literals.update(cl)
        elif lit not in clause:
            # only save clauses not made true by this assignment
            new_f.append(clause.copy())
            all_literals.update(clause)

        if len(clause) == 1:
            aux = max(clause)
            if aux != lit:
                unit_clause = aux

    for l in all_literals:
        if -l not in all_literals:
            if l != unit_clause and l != lit:
                pure = l
                break

    return new_f, unit_clause, pure


def solver_DPLL(f):
    @profile
    def dfs(old_f, symbols, old_v, lit):
        v = old_v.copy()
        v.add(lit)
        sym = symbols.copy()
        sym.remove(abs(lit))

        if sat_all(old_f,v):
            return v

        f, l, pure = first_pass(old_f, v, lit)
        if not f:
            return False

        if l != None:
            #print("unit clause {}".format(l))
            return dfs(f, sym, v, l)

        if pure != None:
            #print("pure symbol {}".format(pure))
            #print("found in {}".format(f))
            return dfs(f, sym, v, pure)

        l = max(sym)
        #print("branch {}".format(l))
        return dfs(f, sym, v, l) or dfs(f, sym, v, -l)

    symbols = get_symbols(f)
    lit = max(symbols)
    #print("root {}".format(lit))
    return dfs(f, symbols, set(), lit) or dfs(f, symbols, set(), -lit)
