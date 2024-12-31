import numpy as np
from sympy.core.cache import cached_property

from pygeartrain.core.geometry import GearGeometry
from pygeartrain.core.kinematics import GearKinematics
from pygeartrain.core.profiles import epi_hypo_gear, rotation


class SimpleGear(GearKinematics):
	"""Simplest plain gear arrangement, for testing purposes"""
	equations = ['A * a + B * b']


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



class NestedGear(GearKinematics):
	"""Nested cycloid gear arrangement, as in a progressive cavity pump"""
	equations = ['N * a - (N + 1) * b']


class NestedGeometry(GearGeometry):

	@cached_property
	def generate_profiles(self, b=0.6, res=100):
		N = self.geometry['N']

		a = epi_hypo_gear(N, N, b, res)
		b = epi_hypo_gear(N+1, N+1, b, res)
		return a, b

	def arrange(self, phase):
		a, b = self.generate_profiles
		a = a.transform(rotation(phase * self.ratios_f['a']))
		b = b.transform(rotation(phase * self.ratios_f['b']))
		return a.translate([1, 0]), b

	def _plot(self, phase, ax):
		a, b = self.arrange(phase)
		a.plot(ax=ax, plot_vertices=False, color='r')
		b.plot(ax=ax, plot_vertices=False, color='b')
