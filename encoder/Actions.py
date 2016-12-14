""" Define Actions and BaseActions classes"""

from encoder.Atoms import Atom

CASES = [
    "({})",
    "({},",
    ",{})",
    ",{},"
]

class Action:
    """ class to represent Actions (operations where the arguments are known)"""
    def __init__(self, name, preconds, effects):
        self.name = name
        self.preconds = set()
        self.effects = set()

        for precond in preconds.split():
            self.preconds.add(Atom(precond))
        for effect in effects.split():
            self.effects.add(Atom(effect))

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return self.name

class BaseAction:
    """ class to represent Action schemas"""
    def __init__(self, string):
        """ parses a line from the file corresponding to an action """
        aux1 = string.split(":")
        self.name = aux1[0].strip()
        aux2 = aux1[1].split("->")
        self.preconds = aux2[0].strip()
        self.effects = aux2[1].strip()
        self.n_args = len(self.name.split(","))

    def ground(self, arg_tup):
        """ applies the arguments in arg_tup to the schema, yielding an Action """
        args = self.name.split("(")[1].split(")")[0].split(",")
        name = self.name
        preconds = self.preconds
        effects = self.effects
        for i, arg in enumerate(args):
            for case in CASES:
                name = name.replace(case.format(arg), case.format(arg_tup[i]))
                preconds = preconds.replace(case.format(arg),
                                            case.format(arg_tup[i]))
                effects = effects.replace(case.format(arg),
                                          case.format(arg_tup[i]))

        return Action(name, preconds, effects)
