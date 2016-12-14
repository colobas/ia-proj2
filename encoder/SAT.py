""" module to implement SATsentence class"""

class SATsentence:
    """ class to represent a SAT formula, in DIMACS format """
    def __init__(self):
        self.sentence = [] #list of clauses
        self.dimacs = dict()
        self.var_cnt = 1 #holds the dimacs value for the next variable


    def get_dimacs_var(self, var, t):
        """ retrieve the DIMACS symbol corresponding to (var, t) """
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
        """ add unit clause from atom at given time step"""
        dimacs = self.get_dimacs_var(atom, time)
        self.sentence.append("{} 0".format(dimacs))

    def add_implication(self, implicates, tim, implicated, tim1):
        """ convert and add implication between variables, in DIMACS format """
        dimacs1 = self.get_dimacs_var(implicates, tim)
        dimacs2 = self.get_dimacs_var(implicated, tim1)
        self.sentence.append("-{} {} 0".format(dimacs1, dimacs2))

    def add_action_eff_prec(self, action, tim):
        """ convert and add action's effects and preconds, in DIMACS format """

        # A => (B & C & D) is equivalent to (~A | B) & (~A | C) & (~A | D)
        for effect in action.effects:
            self.add_implication(action, tim, effect, tim+1)

        for precond in action.preconds:
            self.add_implication(action, tim, precond, tim)

    def add_frame_axioms(self, atom, action, tim):
        """ convert and add frame axioms in DIMACS format """

        # (A & B) => C is equivalent to !A | !B | C

        atom_t_dimacs = self.get_dimacs_var(atom, tim)
        atom_t1_dimacs = self.get_dimacs_var(atom, tim+1)
        action_dimacs = self.get_dimacs_var(action, tim)
        self.sentence.append("-{} -{} {} 0".format(
            atom_t_dimacs, action_dimacs, atom_t1_dimacs))
        self.sentence.append("{} -{} -{} 0".format(
            atom_t_dimacs, action_dimacs, atom_t1_dimacs))

    def list_to_disjunction(self, actions, tim):
        """ convert list of actions to disjunction, i.e., one DIMACS line """

        disj = ""
        for action in actions:
            disj += str(self.get_dimacs_var(action, tim)) + " "

        disj += "0"
        self.sentence.append(disj)

    def add_action_mutex(self, pair, tim):
        """add mutual exclusion between actions in tuple 'pair', at given time """

        # !(A & B) is equivalent to
        dimacs1 = self.get_dimacs_var(pair[0], tim)
        dimacs2 = self.get_dimacs_var(pair[1], tim)

        self.sentence.append("-{} -{} 0".format(dimacs1, dimacs2))
