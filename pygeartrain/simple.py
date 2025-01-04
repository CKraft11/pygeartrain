from sympy.core.cache import cached_property

from pygeartrain.core.geometry import GearGeometry
from pygeartrain.core.kinematics import GearKinematics
from pygeartrain.core.profiles import *
from pygeartrain.core.pga import rotor, translator


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
		return a, b >> rotor(2 * np.pi / B * ((B+1)%2) / 2)

	def arrange(self, phase):
		a, b = self.generate_profiles
		A = self.geometry['A']
		B = self.geometry['B']
		r = self.phases(phase)
		ma = translator(-A, 0) * rotor(r['a'])
		mb = translator(+B, 0) * rotor(r['b'])
		return a >> ma, b >> mb

	def _plot(self, phase, ax):
		a, b = self.arrange(phase)
		a.plot(ax=ax, color='r')
		b.plot(ax=ax, color='b')



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
		r = self.phases(phase)
		ma = translator(1, 0) * rotor(r['a'])
		mb = translator(0, 0) * rotor(r['b'])
		return a >> ma, b >> mb

	def _plot(self, phase, ax):
		a, b = self.arrange(phase)
		a.plot(ax=ax, color='r')
		b.plot(ax=ax, color='b')


