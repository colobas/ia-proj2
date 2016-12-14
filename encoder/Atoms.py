""" module to implement the Atom class"""

class Atom:
    """ class to represent an Atom """
    def __init__(self, string):
        """ parse string to build Atom """
        self.name = string.replace("-", "").replace("\n", "")
        self.negated = "-" in string

    def __repr__(self):
        if self.negated:
            return "-"+self.name
        else:
            return self.name

    def negate(self):
        """ retrieve the negation of this Atom """
        if self.negated:
            return Atom(self.name)
        else:
            return Atom("-"+self.name)

    def __eq__(self, other):
        if self.negated != other.negated:
            return False
        if self.name != other.name:
            return False
        return True

    def __hash__(self):
        return hash(self.name)
