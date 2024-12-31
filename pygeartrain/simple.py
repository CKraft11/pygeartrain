import numpy as np
from sympy.core.cache import cached_property

from pygeartrain.core.geometry import GearGeometry
from pygeartrain.core.kinematics import GearKinematics
from pygeartrain.core.profiles import epi_hypo_gear, rotation


class SimpleGear(GearKinematics):
	"""Simplest plain gear arrangement, for testing purposes"""
	equations = ['A * a + B * b']

def move(A, B):
	return (A%2==0) and (B%2==0)

class SimpleGeometry(GearGeometry):

	@cached_property
	def generate_profiles(self, b=0.6, N=100):
		A = self.geometry['A']
		B = self.geometry['B']

		a = epi_hypo_gear(A, A, b, N)
		b = epi_hypo_gear(B, B, 1-b, N)
		# return a, b.transform(rotation(2 * np.pi / B * (B%2) / 2))
		return a, b.transform(rotation(2 * np.pi / B * ((B+1)%2) / 2))

	def arrange(self, phase):
		a, b = self.generate_profiles
		A = self.geometry['A']
		B = self.geometry['B']
		a = a.transform(rotation(phase * self.ratios_f['a']))
		b = b.transform(rotation(phase * self.ratios_f['b']))
		return a.translate([-A, 0]), b.translate([B, 0])

	def _plot(self, phase, ax):
		a, b = self.arrange(phase)
		a.plot(ax=ax, plot_vertices=False, color='r')
		b.plot(ax=ax, plot_vertices=False, color='b')
