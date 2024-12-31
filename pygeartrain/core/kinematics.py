from typing import List

from sympy import symbols, linsolve, parse_expr
from sympy.core.cache import cached_property


class GearKinematics:
    """A gearing mechanism is defined by its kinematic equations.
    Lower case identifiers are degrees of freedom, such as the angle a given gear is at
    (partial) Upper case variables denote geometric variables, such as gear radii
    """
    equations: List[str]

    def __init__(self, *config):
        self.input, self.output, *self.aux = config

    @classmethod
    def get_identifiers(cls):
        import re
        pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
        return set(a for e in cls.equations for a in re.findall(pattern, e))
    @classmethod
    def dofs(cls):
        return [i for i in cls.get_identifiers() if i.islower()]
    @classmethod
    def geometry(cls):
        return [i for i in cls.get_identifiers() if not i.islower()]

    @cached_property
    def solve(self):
        """Symbolic solve for all variables

        Returns
        dict[str, sympy equation]
            For each dof-key, an equation how this dof advances with one unit of output rotation,
            expressed in terms of all geometric variables
        """
        dofs = symbols(self.dofs())
        geometry = symbols(self.geometry())
        loc = {s.name: s for s in dofs + geometry}

        bcs = [f'{self.output} - 1'] + list(self.aux)    # unit step applied to output
        res = linsolve([parse_expr(e, local_dict=loc) for e in self.equations + bcs], dofs)
        assert len(res.args) == 1
        return dict(zip(self.dofs(), res.args[0]))

    @property
    def ratio(self):
        """Select input/output ratio equation"""
        return self.solve[self.input]

    def __repr__(self):
        return f'{self.input}/{self.output}: {self.ratio}'


