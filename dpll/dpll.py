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
    pures = set()
    for clause in f:
        all_literals.update(clause)

    for l in all_literals:
        if -l not in all_literals:
            pures.add(l)

    return pures


def get_symbols(f):
    return set([abs(l) for clause in f for l in clause])

def remove_falses(f, lit):
    for clause in f:
        if -lit in clause:
            clause.remove(-lit)
    return f

def remove_clauses(f, lit):
    return [clause for clause in f if lit not in clause]

def first_pass(old_f, v, lit):
    new_f = []
    neg_v = [-x for x in v]
    for clause in old_f:
        if unsat_clause(clause, neg_v):
            return False
        if -lit in clause:
            # remove symbol from clauses where it yields false
            cl = clause.copy()
            cl.remove(-lit)
            new_f.append(cl)
            continue
        if lit not in clause:
            # only save clauses not made true by this assignment
            new_f.append(clause.copy())
    return new_f



def solver_DPLL(f):
    def dfs(old_f, symbols, old_v, lit):
        v = old_v.copy()
        v.add(lit)
        sym = symbols.copy()
        sym.remove(abs(lit))


        f = first_pass(old_f, v, lit)
        if not f:
            return False

        unit_lit = set()

        if sat_all(f,v):
            return v

        for clause in f[:]:
            if len(clause) == 1:
                unit_lit.add(clause.pop())
                f.remove(clause)

        for l in unit_lit:
            if -l in unit_lit:
                return False
            for clause in f[:]:
                if -l in clause:
                    clause.remove(-l)
                if l in clause:
                    f.remove(clause)
            sym.remove(abs(l))
            v.add(l)

        pures = get_pure_literal(f)
        if len(pures) > 0:
            for l in pures:
                for clause in f[:]:
                    if l in clause:
                        f.remove(clause)
                sym.remove(abs(l))
                v.add(l)

        if len(sym) == 0:
            if sat_all(f,v):
                return v
            return False

        lit = max(sym)
        return dfs(f, sym, v, lit) or dfs(f, sym, v, -lit)

    symbols = get_symbols(f)
    lit = max(symbols)
    return dfs(f, symbols, set(), lit) or dfs(f, symbols, set(), -lit)
