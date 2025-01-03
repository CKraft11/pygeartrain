"""The Nabtesco is kinda like a compounded cycloid+planetary

It has a single cycloidal outer ring, but is driven by a sun gear
"""
from dataclasses import dataclass
from functools import cached_property

from sympy import Tuple

from pygeartrain.core.kinematics import GearKinematics
from pygeartrain.core.geometry import GearGeometry
from pygeartrain import cycloid
from pygeartrain import planetary
from pygeartrain.core.profiles import concat


class NabtescoKinematics(GearKinematics):
    """
    o:  output carrier
    w : wobbler
    s : input sun
    l : lobed wheel
    r : pin ring
    """
    equations = [
        '(L+1) * r - L * l - (1) * w',  # lobed-ring contact
        'S * s + W * w - (S+W) * o',	# connect sun with wobblers on output carrier; planetary gear equation
        'o - l',        # lobed wheel and output are matched
    ]


@dataclass(repr=False)
class NabtescoGeometry(GearGeometry):
    L: int
    S: int
    W: int
    G: Tuple
    b: float = 1.0  # bearing size
    f: float = 0.5  # cycloid depth; 1=full cycloid, 0 is circle
    N: int = 3 		# number of wobblers

    @classmethod
    def create(cls, kinematics, L, S, W, b=1, f=1):
        geometry = {'L': L, 'S': S, 'W': W}
        return cls(
            kinematics=kinematics,
            geometry=geometry,
            b=b, f=f, **geometry,
            G = (S+W*2, W, S)

        )

    @cached_property
    def generate_profiles(self):
        # we reuse planetary and cycloid functionality; just with small flourishes to the profiles
        scale=1.8
        C = cycloid.generate_profiles(self.L, self.f, self.b, cycloid='epi', scale=scale / self.L)
        r, p, s, e = C
        p = concat([p, cycloid.make_pins(3, 1, self.b / self.L * scale)])
        C = r, p, s, e

        P = planetary.generate_profiles(self.G, 0.5)
        r, p, s = P
        p = concat([p, cycloid.circle(self.b / self.L + e*2)])
        P = r, p, s

        return C, P

    def arrange(self, phase):
        C, P = self.generate_profiles
        r = {k:v * phase for k,v in self.ratios_f.items()}
        return (
            cycloid.arrange(C, r['l'], r['r'], r['w']),
            planetary.arrange(P, self.G, self.N, 0, r['w'], r['s'], r['o']),
        )

    def _plot(self, ax, phase):
        C, P = self.arrange(phase)
        for c in C[:-1]:
            c.plot(ax=ax, plot_vertices=False, color='r')
        for p in P[1:]:
            p.plot(ax=ax, plot_vertices=False, color='b')
