from dataclasses import dataclass
from functools import cached_property
from typing import Tuple

from pygeartrain.core.geometry import GearGeometry, flatten
from pygeartrain.core.kinematics import GearKinematics
from pygeartrain.core.profiles import *
from pygeartrain.core.pga import rotor, translator


class Planetary(GearKinematics):
    """
    Classic single stage planetary
    https://en.wikipedia.org/wiki/Epicyclic_gearing
    """
    equations = [
        'S * s + P * p - (S + P) * c',  # planet-sun contact
        'R * r - P * p - (R - P) * c',  # planet-ring contact
    ]


@dataclass(repr=False)
class PlanetaryGeometry(GearGeometry):
    G: Tuple[int, int, int]
    N: int      # number of planets
    b: float    # ratio of epi/hypo cycloid in the tooth profile

    @classmethod
    def create(cls, kinematics, G, N, b=0.5):
        geometry = dict(zip('RPS', G))
        return cls(
            kinematics=kinematics,
            geometry=geometry,
            G=G, N=N, b=b
        )

    @cached_property
    def generate_profiles(self, res=500):
        return generate_profiles(self.G, self.N, self.b, res=res, show_carrier=True)

    def arrange(self, phase):
        r = self.phases(phase)
        return arrange(
            self.generate_profiles, self.G, self.N,
            r['r'], r['p'], r['s'], r['c'],
        )

    def _plot(self, ax, phase, col='b'):
        for profile in flatten(self.arrange(phase)):
            profile.plot(ax=ax, color=col)


# broken out as free functions for reusability in compound planetary
def generate_profiles(G, N, b, res=500, offset=0, scale=1, show_carrier=False):
    R,P,S = G
    # scale planetaries to unit circle
    f = (S + P) / scale

    r = epi_hypo_gear(R/f, R, b, res) >> rotor(offset / R * np.pi)
    p = epi_hypo_gear(P/f, P, b, res) >> rotor(offset / P * np.pi)
    s = epi_hypo_gear(S/f, S, 1 - b, res) >> rotor(-offset / S * np.pi)
    # optional carrier visualization
    if show_carrier:
        c = hypo_gear(N, N, f=0.5).scale(1/N)
    else:
        c = Profile.empty()
    # rotate sun gear in even toothed planet case for correct meshing
    s = s >> rotor(np.pi / S * (((P+1) % 2)))
    return r, p, s, c


def arrange(profiles, G, N, rr, rp, rs, rc):
    """Take generated profiles and arrange them into a planetary with the proper phase rotations"""
    rg, pg, sg, cg = profiles
    R, P, S = G
    rg = rg >> rotor(rr)
    pg = pg >> rotor(rp)
    sg = sg >> rotor(rs)
    cg = cg >> rotor(rc)

    # expand single planet into full ring of N
    def motor(i):
        a = 2 * np.pi * i / N   # rotation needed for placement along carrier
        w = (1-R/P) * a         # rotation needed to maintain meshing along carrier
        return (rotor(rc+a) >> translator(1, 0)) * rotor(w)
    pgs = [pg >> motor(i) for i in range(N)]

    return rg, pgs, sg, cg
