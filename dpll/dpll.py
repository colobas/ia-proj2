""" module to implement DPLL algorithm and relevant auxiliary functions """

from collections import Counter

SYM_COUNT = Counter()

def sat_clause(clause, model):
    """ check if clause is satisfied by the model """

    if clause.intersection(model):
        return True
    return False

def sat_all(formula, model):
    """ check if all clauses in formula are satisfied by the model """
    for clause in formula:
        if len(clause) == 0 or not sat_clause(clause, model):
            return False
    return True

def unsat_clause(clause, neg_v):
    """ check if clause is unsatisfied by the model.
    (neg_v is the 'symmetric model')"""
    return len(clause.intersection(neg_v)) == len(clause)

def get_symbols(formula):
    """ get all symbols in formula """
    return set([abs(lit) for clause in formula for lit in clause])

def units_and_pures(old_f, model, lits, sym):
    """ remove unit clauses and pure symbols from formula,
    updating the model accordingly. unsatisfiability is
    also checked here. """

    formula = old_f
    while True:
        # cycle until there are no unit clauses or pure symbols to extract.
        # in each cycle, 'lits' contains the unit clauses and pure symbols
        # found in the previous cycle. in the first cycle, 'lits' will only
        # contain one element, which is the one with which this function is
        # called and corresponds to the assignment made in the branch where
        # this function was called.

        new_f = []
        neg_v = [-x for x in model] # 'symmetric' to the model

        neg_lits = [-l for l in lits] # symmetric to the unit clauses and pure
#                                       found in the previous cycle

        if len(lits.intersection(neg_lits)) > 0:
            # return False if a contradiction is found
            return False, None, None

        unit_clauses = set() # contains values from unit clauses and pure symbols
        all_literals = set() # contains all literals contained in the clauses

        for clause in formula:
            if unsat_clause(clause, neg_v):
                # if any clause in is unsatisfied the model doesn't hold
                return False, None, None

            cla = clause.difference(neg_lits)
            # remove symbols from clauses where they yield false

            if len(clause) == 1:
                # if clause is a unit clause, remove it and store assignment
                unit_clauses.update(cla)
                continue

            if len(cla.intersection(lits)) > 0:
                # if any of the variables in 'lits' is true in this clause,
                # clause is true, remove it
                continue

            all_literals.update(cla)
            new_f.append(cla)


        for lit in all_literals:
            if -lit not in unit_clauses and -lit not in all_literals:
                unit_clauses.add(lit)

        if len(unit_clauses) == 0:
            # if there are no unit clauses or pure symbols left, return
            return new_f, model, sym


        # prepare variables for the next cycle
        lits = unit_clauses.difference(lits)
        formula = new_f.copy()
        model.update(unit_clauses)
        sym.difference_update(set([abs(x) for x in unit_clauses]))

def dfs(old_f, sym, v, lit):
    """ recursive dfs implementation, that traverses the 'decision tree' """

    if lit != 0: # test for first iteration
        v.add(lit)

    if len(sym) == 0:
        return False


    # remove unit clauses and pure symbols
    if lit != 0: # test for first iteration
        formula, model, sym = units_and_pures(old_f, v, {lit}, sym)
    else:
        formula, model, sym = units_and_pures(old_f, v, set(), sym)

    if formula is False:
        # if removing unit clauses and pure symbols made the formula
        # unsatisfiable, return False
        return False

    if sat_all(old_f, v):
        # if removing unit clauses and pure symbols made the formula
        # satisfiable, return solution model
        return model


    # retrieve next variable to assign, based on the number of clauses it
    # was involved with in the beginning of the problem
    decision = max(sym, key = lambda x: SYM_COUNT[abs(x)])
    sym.remove(decision)

    # spawn two branches
    return (dfs(formula, sym.copy(), model.copy(), decision)
            or dfs(formula, sym, model, -decision))


def dpll(formula):
    """ remove duplicate clauses from formula, count number of clauses
    each symbol is involved in, and spawn root node for the recursion tree """
    no_dups = set()
    for clause in formula:
        no_dups.add(frozenset(clause))

    new_f = []
    for cla in no_dups:
        new_f.append(set(cla))
        for sym in cla:
            SYM_COUNT[abs(sym)] += 1

    symbols = get_symbols(new_f)
    return dfs(new_f, symbols, set(), 0)
