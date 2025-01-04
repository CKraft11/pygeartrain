from dataclasses import dataclass

from functools import cached_property

from pygeartrain.core.geometry import GearGeometry
from pygeartrain.core.kinematics import GearKinematics
from pygeartrain.core.profiles import *
from pygeartrain.core.pga import rotor, translator


class Cycloid(GearKinematics):
    """A cycloid can be viewed as a planetary with a single planet, grown to maximum size"""
    # sun is 1-1 with carrier, so it drops out of equations
    # R = P + 1, so R also drops out
    equations = [
        '(P+1) * r - P * p - (1) * c',  # planet-ring contact
    ]


@dataclass(repr=False)
class CycloidGeometry(GearGeometry):
    P: int          # number of lobes on the disc
    b: float = 1.0  # bearing size
    f: float = 0.8  # cycloid depth; 1=full cycloid, 0 is circle
    cycloid: str ='epi'
    O: int = 0      # output pins

    @classmethod
    def create(cls, kinematics, P, cycloid='epi', O=0):
        geometry = {'P': P}
        return cls(
            kinematics=kinematics,
            geometry=geometry,
            P=P, cycloid=cycloid,
            O=O,
        )

    @cached_property
    def generate_profiles(self):
        return generate_profiles(self.P, self.f, self.b, self.cycloid, O=self.O)

    def arrange(self, phase):
        r = self.phases(phase)
        return arrange(self.generate_profiles, r['p'], r['r'], r['c'])

    def _plot(self, ax, phase):
        r, p, s, o = self.arrange(phase)
        p.plot(ax=ax, color='r')
        r.plot(ax=ax, color='r')
        s.plot(ax=ax, color='g')
        o.plot(ax=ax, color='k')



def generate_profiles(P, f, b, cycloid, offset=0, s=1, scale=1, O=0):
    R = P + 1
    e = 1 * f * s

    if cycloid == 'epi':
        p = epi_gear_offset(P*s, P, b=-b, f=f*s)
        # carrier output pin holes
        p = Profile.concat([p, make_pins(O, R*s/2, b*s)])
        r = make_pins(R, R*s, b)
    elif cycloid == 'hypo':
        p = make_pins(P, (P+2)*s, b)
        r = hypo_gear_offset(R*s, R, b=b, f=f*s)

    if O:
        o = make_pins(O, R*s/2, (b+e)*s)  # carrier output pins
        o = Profile.concat([o, hypo_gear(R * s*0.6, O, 0.5)])
    else:
        o = Profile.empty()
    # wobbler / single-tooth hypocycloid
    s = Profile.concat([make_pins(1, e, b + e), make_pins(1, 0, b)])

    o = o.scale(scale) >> rotor(offset / P * np.pi)
    p = p.scale(scale) >> rotor(offset / P * np.pi)
    r = r.scale(scale) >> rotor(offset / R * np.pi)
    s = s.scale(scale) >> rotor(offset / 1 * np.pi)
    return r, p, s, o, e * scale


def arrange(profiles, rp, rr, rc):
    r, p, s, o, e = profiles

    o = o >> rotor(rp)
    r = r >> rotor(rr)
    s = s >> rotor(rc)
    # combined p and c transform
    m = (rotor(rc) >> translator(e, 0)) * rotor(rp)
    p = p >> m

    return r, p, s, o
