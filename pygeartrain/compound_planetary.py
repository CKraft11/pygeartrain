"""The compound planetary is defined as two stacked planetaries,
which are joined via their planets/carrier

It is known by various names; aso the Wolfram topology
"""
from dataclasses import dataclass
from functools import cached_property
from typing import Tuple

from pygeartrain.core.kinematics import GearKinematics
from pygeartrain.core.geometry import GearGeometry, flatten
from pygeartrain.planetary import generate_profiles, arrange


class CompoundPlanetary(GearKinematics):
    equations = [
        'S1 * s1 + P1 * p - (S1 + P1) * c',  # planet-sun contact 1
        'R1 * r1 - P1 * p - (R1 - P1) * c',  # planet-ring contact 1
        'S2 * s2 + P2 * p - (S2 + P2) * c',  # planet-sun contact 2
        'R2 * r2 - P2 * p - (R2 - P2) * c',  # planet-ring contact 2
    ]

    #     # primary config; drive s relative to r, and rings as mechanical outputs
    #     [r1, s1, r2],
    #     [r1, s2, r2],
    #     [r2, s1, r1],
    #     [r2, s2, r1],
    #
    #     # [s, r, s]
    #     # use both suns as mechanical connections
    #     # these seem like viable configs;
    #     # generally lower ratio than primary ones; 3-20x lower, but certainly nontrivial ones available
    #     # however, mechanically less favorable; another seal to deal with?
    #     # or just add housing attached to fixed shaft, with single seal on other shaft?
    #     # nice from sealing complexity pov, but now housing is additional component.
    #     [s1, r1, s2],
    #     [s2, r1, s1],
    #     [s1, r2, s2],
    #     [s2, r2, s1],
    #
    #     # [r, s, s]
    #     # using sun as output shaft; getting ratios rather close to one
    #     [r1, s1, s2],
    #     [r1, s2, s1],
    #     [r2, s1, s2],
    #     [r2, s2, s1],
    #     # [s, r, r]
    #     # similar story
    #     [s1, r2, r1],
    #     [s1, r1, r2],
    #     [s2, r2, r1],
    #     [s2, r1, r2],
    #     #
    #     # # [s, s, r]
    #     # # these configs perform upgearing; similar to r-r-s config; r backdriving of the primary
    #     # [s1, s2, r1],
    #     # [s1, s2, r2],
    #     # [s2, s1, r1],
    #     # [s2, s1, r2],
    #     # # [r, r, s]
    #     # # backdriving of the primary config; upgearing like above
    #     # [r1, r2, s1],
    #     # [r1, r2, s2],
    #     # [r2, r1, s1],
    #     # [r2, r1, s2],
    #
    #     # carrier-driven planetary options
    #     # these tend to be a few times lower in ratio than the r-s-r config
    #     [r1, c, r2],
    #     # these tend to be lower still, but still potentially useful
    #     [s1, c, s2],
    #     # r-c-s configs tend to have ratios < 1; not of real world interest
    #     # [r1, c, s1],
    #     # [r1, c, s2],
    #
    # ]

@dataclass(repr=False)
class CompoundPlanetaryGeometry(GearGeometry):
    """Compound planetary with cycloidal tooth profile"""

    G1: Tuple[int, int, int]
    G2: Tuple[int, int, int]
    N: int
    b1: float
    b2: float
    show_carrier: bool

    @classmethod
    def create(cls, kinematics, G1, G2, N, b1=0.5, b2=0.5, show_carrier=False):
        geometry = {**dict(zip(['R1','P1','S1'], G1)), **dict(zip(['R2', 'P2', 'S2'], G2))}

        return cls(
            kinematics=kinematics,
            geometry=geometry,
            G1=G1, G2=G2, N=N, b1=b1, b2=b2,
            show_carrier=show_carrier
        )

    @cached_property
    def generate_profiles(self, res=500):
        return (
            generate_profiles(self.G1, self.N, self.b1, res=res),
            generate_profiles(self.G2, self.N, self.b2, res=res, offset=0.5*self.G2[1])  # offset by half a planet tooth; works out nicer in P2=1 case
        )

    def arrange(self, phase):
        r = self.phases(phase)
        p1, p2 = self.generate_profiles
        return arrange(
            p1, self.G1, self.N,
            r['r1'], r['p'], r['s1'], r['c'],
        ), arrange(
            p2, self.G2, self.N,
            r['r2'], r['p'], r['s2'], r['c'],
        )

    def _plot(self, ax, phase):
        p1, p2 = self.arrange(phase)
        for p in flatten(p1 if self.show_carrier else p2[:-1]):
            p.plot(ax=ax, plot_vertices=False, color='r')
        for p in flatten(p2 if self.show_carrier else p2[:-1]):
            p.plot(ax=ax, plot_vertices=False, color='b')
