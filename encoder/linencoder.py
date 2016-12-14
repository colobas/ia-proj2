""" module to implement the linear encoder """

from itertools import permutations
from encoder.SAT import SATsentence

def encode(domain, h):
    """ encode problem domain with time horizon h """
    sentence = SATsentence()
    action_perms = list(permutations(domain.actions, r=2))

    for atom in domain.hebrand:
        if atom in domain.initial_state: # initial state axioms
            sentence.add_unit_clause(atom, 0)
        else:
            sentence.add_unit_clause(atom.negate(), 0)

        if atom in domain.goal_state: # goal state axioms
            sentence.add_unit_clause(atom, h)

    for tim in range(h):
        for action in domain.actions:
            # each action implies its effects and preconditions
            sentence.add_action_eff_prec(action, tim)

            for atom in domain.hebrand:
                if atom not in action.effects:
                    if atom.negate() not in action.effects:
                        # atoms not in this action's effects aren't affected by it
                        sentence.add_frame_axioms(atom, action, tim)

        # at least one action is performed at time t
        sentence.list_to_disjunction(domain.actions, tim)
        for pair in action_perms:
            sentence.add_action_mutex(pair, tim)
    return sentence

def decode(domain, sentence, sol, horiz):
    """ decode solution and print resulting plan """
    to_rem = []
    for var in sol:
        if var < 0:
            to_rem.append(var)

    for var in to_rem:
        sol.remove(var)

    for tim in range(horiz):
        for action in domain.actions:
            action_dimacs_var = sentence.get_dimacs_var(action, tim)
            if action_dimacs_var in sol:
                aux = action.name.split("(")
                print(aux[0] + " " + aux[1].replace(",", " ").strip(")"))
                break
