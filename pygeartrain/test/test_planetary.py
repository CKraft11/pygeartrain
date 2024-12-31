from pygeartrain.planetary import *


def test_ratio():
	print()
	# kinematics = Planetary('s', 'c', 'r')
	# kinematics = Planetary('s', 'r', 'c')
	kinematics = Planetary('c', 'r', 's')
	print(kinematics)

	gear = PlanetaryGeometry.create(kinematics, (14,4,6), 5, b=0.8)
	print(gear)
	gear.animate()
	gear = PlanetaryGeometry.create(kinematics, (11, 2, 7), 6, b=0.6)
	print(gear)
	gear.animate()
