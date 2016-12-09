from Actions import BaseAction
from Atoms import Atom
from itertools import product

class Domain:
    def __init__(self, filepath):
        self.hebrand = set()
        self.initial_state = set()
        self.goal_state = set()
        self.actions = set()
        self.variables = set()
        base_actions = set()

        with open(filepath, "r") as f:
            lines = f.readlines()

        for line in lines:
            if line[0] == "I":
               atoms = line.split(" ")[1:]
               for atom in atoms:
                   args = atom.split("(")[1].split(")")[0].split(",")
                   for arg in args:
                       self.variables.add(arg)

                   a = Atom(atom)
                   self.initial_state.add(a)
                   if a.negated:
                       self.hebrand.add(a.negate())
                   else:
                       self.hebrand.add(a)

            elif line[0] == "G":
               atoms = line.split(" ")[1:]
               for atom in atoms:
                   args = atom.split("(")[1].split(")")[0].split(",")
                   for arg in args:
                       self.variables.add(arg)

                   a = Atom(atom)
                   self.goal_state.add(a)
                   if a.negated:
                       self.hebrand.add(a.negate())
                   else:
                       self.hebrand.add(a)

            elif line[0] == "A":
                base_actions.add(BaseAction(line[2:]))

        for atom in self.initial_state.union(self.goal_state):
            vars = atom.base.split("(")[1].split(")")[0].split(",")
            for var in vars:
                self.variables.add(var)

        for base_action in base_actions:
            for comb in product(self.variables, repeat=base_action.n_args):
                self.actions.add(base_action.ground(comb))

        for action in self.actions:
            for a in action.preconds.union(action.effects):
                if a.negated:
                    self.hebrand.add(a.negate())
                else:
                    self.hebrand.add(a)


