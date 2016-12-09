class Atom:
    def __init__(self, string):
        self.base = string.replace("-","")
        self.negated = "-" in string

    def negate(self):
        if self.negated:
            return Atom(self.base)
        else:
            return Atom("-"+self.base)

    def __eq__(self, other):
        if self.negated != other.negated:
            return False
        if self.base != self.other:
            return False
        return True

    def __hash__(self):
        return hash(self.base)