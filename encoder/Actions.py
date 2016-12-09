from encoder.Atoms import Atom

cases = [
    "({})",
    "({},",
    ",{})",
    ",{},"
]

class Action:
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

class BaseAction:
    def __init__(self, string):
        aux1 = string.split(":")
        self.name = aux1[0].strip()
        aux2 = aux1[1].split("->")
        self.preconds = aux2[0].strip()
        self.effects = aux2[1].strip()
        self.n_args = len(self.name.split(","))

    def ground(self, arg_tup):
        args = self.name.split("(")[1].split(")")[0].split(",")
        name = self.name
        preconds = self.preconds
        effects = self.effects
        for i,arg in enumerate(args):
            name = name.replace(arg, arg_tup[i])
            preconds = preconds.replace(arg, arg_tup[i])
            effects = effects.replace(arg, arg_tup[i])

        return Action(name, preconds, effects)
