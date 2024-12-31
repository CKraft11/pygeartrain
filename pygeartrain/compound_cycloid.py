"""This is different from the usual cycloidal gearbox
Rather than the typical setup, with pins interior to the disc,
it uses two cycloidal discs of identical design but different tooth count back to back,
which makes the design less cramped compared to radially nested cycloids,
sharing the same eccentricity

In terms of gearing, we can view this as a carrier-driven compound planetary;
just having a single planet, thats scaled up all over the sun gear
"""
from cmath import phase
from dataclasses import dataclass
from functools import cached_property
from typing import Tuple

from examples.modelling.gear import hypo_gear

from pygeartrain.core.kinematics import GearKinematics
from pygeartrain.core.geometry import GearGeometry
from pygeartrain.core.profiles import *


def concat(geo):
    es = [a.topology.elements[-1] for a in geo]
    offsets = np.cumsum([0] + [len(e) for e in es])
    return type(geo[0])(
        vertices=np.concatenate([a.vertices for a in geo], axis=0),
        cubes=np.concatenate([e + o for e, o in zip(es, offsets)], axis=0)
    )


def make_pins(N, R, r):
    pin = ring(sinusoid(1, 0, 0, r, n_points=100))
    return concat([pin.translate([R, 0]).transform(rotation(i / N * 2 * np.pi)) for i in range(N)])



class CompoundCycloid(GearKinematics):
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
    f: float = 0.8  # cycloid depth; 1=full cycloid, 0 is circle

    @classmethod
    def create(cls, kinematics, P1, P2):
        geometry = {'P1': P1, 'P2': P2}
        return cls(
            kinematics=kinematics,
            geometry=geometry,
            P1=P1, P2=P2
        )


    @cached_property
    def generate_profiles(self, res=500):
        P1, P2 = self.P1, self.P2
        R1 = P1+1
        R2 = P2+1

        def eccentricity(l):
            p = l + 1
            return l / p
        # scale factor to be applied, so that both cycloids have the same shared eccentricity
        # FIXME: allow variable f and radius per side?
        #  also, why not two independent discs? can also have independent eccentricity
        s = eccentricity(P1) / eccentricity(P2)
        e = 1 * self.f
        p1 = hypo_gear(P1, P1, b=-self.b, f=self.f)
        p2 = hypo_gear(P2*s, P2, b=-self.b, f=self.f)

        r1 = make_pins(R1, R1, self.b)
        r2 = make_pins(R2, R2*s, self.b)

        s = concat([make_pins(1, e, self.b+e), make_pins(1, 0, self.b)])

        return p1, p2, r1, r2, s, e

    def arrange(self, phase):
        p1, p2, r1, r2, s, e = self.generate_profiles

        p1 = p1.transform(rotation(phase * self.ratios_f['p']))
        p2 = p2.transform(rotation(phase * self.ratios_f['p']))
        r1 = r1.transform(rotation(phase * self.ratios_f['r1']))
        r2 = r2.transform(rotation(phase * self.ratios_f['r2']))
        s = s.transform(rotation(phase * self.ratios_f['c']))
        # carrier transform
        ca = phase * self.ratios_f['c']
        p1 = p1.transform(rotation(-ca)).translate([e, 0]).transform(rotation(ca))
        p2 = p2.transform(rotation(-ca)).translate([e, 0]).transform(rotation(ca))

        return p1, p2, r1, r2, s

    def _plot(self, ax, phase):
        p1, p2, r1, r2, s = self.arrange(phase)
        p1.plot(ax=ax, plot_vertices=False, color='r')
        p2.plot(ax=ax, plot_vertices=False, color='b')
        r1.plot(ax=ax, plot_vertices=False, color='r')
        r2.plot(ax=ax, plot_vertices=False, color='b')
        s.plot(ax=ax, plot_vertices=False, color='g')
