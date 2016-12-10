class SATsentence:
    def __init__(self):
        self.sentence = []
        self.dimacs = dict()
        self.var_cnt = 1 #holds the dimacs value for the next variable


    def get_dimacs_var(self, var, t):
        negated = hasattr(var, "negated") and var.negated
        key = (var.name, t)

        if not key in self.dimacs:
            self.dimacs[key] = self.var_cnt
            self.var_cnt += 1

        if negated:
            return -self.dimacs[key]
        else:
            return self.dimacs[key]


    def add_unit_clause(self, atom, time):
        dimacs = self.get_dimacs_var(atom,time)
        self.sentence.append("{} 0".format(dimacs))

    def add_implication(self, implicates, t, implicated, t1):
        dimacs1 = self.get_dimacs_var(implicates,t)
        dimacs2 = self.get_dimacs_var(implicated,t1)
        self.sentence.append("-{} {} 0".format(dimacs1, dimacs2))

    def add_action_effects_and_preconds(self, action, t):
        # A => (B & C & D) is equivalent to (~A | B) & (~A | C) & (~A | D)
        for effect in action.effects:
            self.add_implication(action, t, effect, t+1)

        for precond in action.preconds:
            self.add_implication(action, t, precond, t)

    def add_frame_axioms(self, atom, action, t):
        # (A & B) => C is equivalent to !A | !B | C

        atom_t_dimacs = self.get_dimacs_var(atom,t)
        atom_t1_dimacs = self.get_dimacs_var(atom, t+1)
        action_dimacs = self.get_dimacs_var(action,t)
        self.sentence.append("-{} -{} {} 0".format(
            atom_t_dimacs, action_dimacs, atom_t1_dimacs))
        self.sentence.append("{} -{} -{} 0".format(
            atom_t_dimacs, action_dimacs, atom_t1_dimacs))

    def list_to_disjunction(self, actions, t):
        disj = ""
        for action in actions:
            disj += str(self.get_dimacs_var(action,t)) + " "

        disj += "0"
        self.sentence.append(disj)

    def add_action_mutex(self, pair, t):
        # !(A & B) is equivalent to
        dimacs1 = self.get_dimacs_var(pair[0],t)
        dimacs2 = self.get_dimacs_var(pair[1],t)

        self.sentence.append("-{} -{} 0".format(dimacs1, dimacs2))

