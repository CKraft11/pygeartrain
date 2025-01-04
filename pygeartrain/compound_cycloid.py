"""This is different from the usual cycloidal gearbox
Rather than the typical setup, with pins interior to the disc,
it uses two cycloidal discs of identical design but different tooth count back to back,
which makes the design less cramped compared to radially nested cycloids,
sharing the same eccentricity

In terms of gearing, we can view this as a carrier-driven compound planetary;
just having a single planet, thats scaled up all over the sun gear
"""
from dataclasses import dataclass
from functools import cached_property
import numpy as np

from pygeartrain.core.kinematics import GearKinematics
from pygeartrain.core.geometry import GearGeometry
from pygeartrain import cycloid


class CompoundCycloid(GearKinematics):
    """Two cycloids, sharing a single disc
    Same as a compound planetary, just fusing disk instead pf planets
    """
    # sun is 1-1 with carrier, so it drops out of equations
    # R = P + 1, so R also drops out
    equations = [
        '(P1+1) * r1 - P1 * p - (1) * c',  # planet-ring contact 1
        '(P2+1) * r2 - P2 * p - (1) * c',  # planet-ring contact 2
    ]


@dataclass(repr=False)
class CompoundCycloidGeometry(GearGeometry):
    P1: int
    P2: int
    b: float = 1.0  # bearing size
    f: float = 0.5  # cycloid depth; 1=full cycloid, 0 is circle
    offset = True   # 180 wobbler offset
    cycloid: str ='epi'

    @classmethod
    def create(cls, kinematics, P1, P2, b=1, f=1, cycloid='epi'):
        geometry = {'P1': P1, 'P2': P2}
        return cls(
            kinematics=kinematics,
            geometry=geometry,
            P1=P1, P2=P2, b=b, f=f, cycloid=cycloid,

        )

    @cached_property
    def generate_profiles(self):
        s=0.5
        return (
            cycloid.generate_profiles(self.P1, self.f, self.b, self.cycloid, s=1.0),
            cycloid.generate_profiles(self.P2, self.f, self.b, self.cycloid),#, 'hypo', offset=0.5),
        )

    def arrange(self, phase):
        p1, p2 = self.generate_profiles
        r = self.phases(phase)
        o = np.pi * self.offset
        return (
            cycloid.arrange(p1, r['p'], r['r1'], r['c']),
            cycloid.arrange(p2, r['p']+o, r['r2']+o, r['c']+o),
        )

    def _plot(self, ax, phase):
        (r1, p1, s1, c1), (r2, p2, s2, c2) = self.arrange(phase)
        r1.plot(ax=ax, color='r')
        p1.plot(ax=ax, color='r')
        r2.plot(ax=ax, color='b')
        p2.plot(ax=ax, color='b')
        s1.plot(ax=ax, color='g')
        s2.plot(ax=ax, color='g')
