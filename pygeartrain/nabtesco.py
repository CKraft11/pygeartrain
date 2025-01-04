"""The Nabtesco is kinda like a compounded cycloid+planetary

It has a single cycloidal outer ring, but is driven by a sun gear
"""
from dataclasses import dataclass
from functools import cached_property

from typing import Tuple

from pygeartrain.core.kinematics import GearKinematics
from pygeartrain.core.geometry import GearGeometry, flatten
from pygeartrain import cycloid
from pygeartrain import planetary
from pygeartrain.core.profiles import Profile


class NabtescoKinematics(GearKinematics):
    """
    o:  output carrier
    w : wobbler
    s : input sun
    l : lobed wheel
    r : pin ring
    """
    equations = [
        '(L+1) * r - L * l - (1) * w',  # lobed-ring contact; cycloid equation
        'S * s + W * w - (S+W) * o',	# connect sun with wobblers on output carrier; planetary gear equation
        'o - l',        # lobed wheel and output carrier are matched
    ]


@dataclass(repr=False)
class NabtescoGeometry(GearGeometry):
    L: int
    S: int
    W: int
    G: Tuple[int, int, int]
    b: float = 1.0  # pin size
    f: float = 0.5  # cycloid depth; 1=full cycloid, 0 is circle
    N: int = 3 		# number of wobblers

    @classmethod
    def create(cls, kinematics, L, S, W, b=1, f=1, N=3):
        geometry = {'L': L, 'S': S, 'W': W}
        return cls(
            kinematics=kinematics,
            geometry=geometry,
            b=b, f=f, **geometry,
            G=(S+W*2, W, S),
            N=N,
        )

    @cached_property
    def generate_profiles(self):
        # we reuse planetary and cycloid functionality; just with small flourishes to the profiles
        scale=1.9
        b2 = 2.0
        C = cycloid.generate_profiles(self.L, self.f, self.b, cycloid='epi', scale=scale / self.L)
        r, p, s, o, e = C
        p = Profile.concat([p, cycloid.make_pins(self.N, 1, b2*(self.b / self.L + 0*e) * scale)])   # add bearing holes into disc
        C = r, p, s, o, e

        P = planetary.generate_profiles((1,)+self.G[1:], self.N, 0.5)
        r, p, s, c = P
        p = Profile.concat([p, planetary.circle((self.b / self.L + e*0)*b2)]) # add wobbler bearing onto planets
        P = r, p, s, c

        return C, P

    def arrange(self, phase):
        C, P = self.generate_profiles
        r = self.phases(phase)
        return (
            cycloid.arrange(C, r['l'], r['r'], r['w']),
            planetary.arrange(P, self.G, self.N, 0, r['w'], r['s'], r['o']),
        )

    def _plot(self, ax, phase):
        C, P = self.arrange(phase)
        for c in C[:-2]:    # skip default cycloid wobbler and carrier
            c.plot(ax=ax, color='r')
        for p in flatten(P[1:]):    # skip default planet ring gear
            p.plot(ax=ax, color='b')
