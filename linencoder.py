from SAT import SATsentence

def encode(domain, h):
    sentence = SATsentence()
    action_perms = list(permutations(domain.actions, r=2))

    for atom in domain.hebrand:
        if atom in domain.initial_state: # initial state axiom
            sentence.add_unit_clause(atom, 0)
        else:
            sentence.add_unit_clause(atom.negate(), 0)

        if atom in domain.goal_state:
            sentence.add_unit_clause(atom, h)

    for t in range(h):
        for action in domain.actions:
            sentence.add_action_effects_and_preconds(action, t)

            for atom in domain.herbrand:
                if atom not in action.effects:
                    if atom.negate() not in action.effects:
                        sentence.add_frame_axioms(atom, action, t)

        sentence.list_to_disjunction(domain.actions, t)
        for pair in action_perms:
            sentence.add_action_mutex(pair)
    return sentence
