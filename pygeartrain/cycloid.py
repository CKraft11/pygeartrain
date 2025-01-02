from dataclasses import dataclass

from sympy.core.cache import cached_property

from pygeartrain.core.geometry import GearGeometry
from pygeartrain.core.kinematics import GearKinematics
from pygeartrain.core.profiles import *
from pygeartrain.planetary import arrange


class Cycloid(GearKinematics):
    """A cycloid can be viewed as a planetary with a single planet, grown to maximum size"""
    # sun is 1-1 with carrier, so it drops out of equations
    # R = P + 1, so R also drops out
    equations = [
        '(P+1) * r - P * p - (1) * c',  # planet-ring contact
    ]


@dataclass(repr=False)
class CycloidGeometry(GearGeometry):
    P: int
    b: float = 1.0  # bearing size
    f: float = 0.8  # cycloid depth; 1=full cycloid, 0 is circle
    cycloid: str ='epi'

    @classmethod
    def create(cls, kinematics, P, cycloid='epi'):
        geometry = {'P': P}
        return cls(
            kinematics=kinematics,
            geometry=geometry,
            P=P, cycloid=cycloid,
        )

    @cached_property
    def generate_profiles(self):
        return generate_profiles(self.P, self.f, self.b, self.cycloid)

    def arrange(self, phase):
        r = {k:v * phase for k,v in self.ratios_f.items()}
        return arrange(self.generate_profiles, r['p'], r['r'], r['c'])

    def _plot(self, ax, phase):
        r, p, s = self.arrange(phase)
        p.plot(ax=ax, plot_vertices=False, color='r')
        r.plot(ax=ax, plot_vertices=False, color='r')
        s.plot(ax=ax, plot_vertices=False, color='g')



def generate_profiles(P, f, b, cycloid):
    R = P + 1
    e = 1 * f

    if cycloid == 'epi':
        p = epi_gear_offset(P, P, b=-b, f=f)
        r = make_pins(R, R, b)
    elif cycloid == 'hypo':
        R = P+1
        p = make_pins(P, P+2, b)
        r = hypo_gear_offset(R, R, b=b, f=f)

    # wobbler / single-tooth hypocycloid
    s = concat([make_pins(1, e, b + e), make_pins(1, 0, b)])
    return r, p, s, e


def arrange(profiles, rp, rr, rc):
    r, p, s, e = profiles

    p = p.transform(rotation(rp))
    r = r.transform(rotation(rr))
    s = s.transform(rotation(rc))
    # carrier transform
    p = p.transform(rotation(-rc)).translate([e, 0]).transform(rotation(rc))

    return r, p, s
