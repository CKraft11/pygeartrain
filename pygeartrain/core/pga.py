from numga.backend.numpy.context import NumpyContext
import numpy as np


pga = NumpyContext('w0x+y+')
x = pga.multivector.x
y = pga.multivector.y
w = pga.multivector.w
xy = pga.multivector.xy
wx = pga.multivector.wx
wy = pga.multivector.wy


def rotor(angle):
	return xy * np.sin(angle/-2) + np.cos(angle/-2)


def translator(tx, ty):
	return 1 + wx*tx/-2 + wy*ty/-2


# # god this is so janky... need to add custom subspace ordering to numga to get rid of these signs
signs = 1 - (np.arange(9).reshape(3,3)%2)*2
assert pga.subspace.antivector().named_str == 'wx,wy,xy'
def as_matrix(motor):
	return motor.sandwich(pga.subspace.antivector()).kernel
def transform(motor, p):
	"""Optimized sandwich implementation for point transformation, eliminating intermediaries"""
	m = (as_matrix(motor) *signs)[::-1,::-1]
	return p.dot(m[1:, 1:]) + m[0:1, 1:]


def test_pga():
	from pygeartrain.core.profiles import epi_hypo_gear
	from pygeartrain.core.profiles import Profile, circle

	gear = Profile.concat([epi_hypo_gear(3, 5, 0.5, 100), circle(0.1)])
	m = translator(1, 2) * rotor(0.1)
	(gear>> m).plot()
	import matplotlib.pyplot as plt
	plt.show()