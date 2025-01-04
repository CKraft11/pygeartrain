from pygeartrain.cycloid import Cycloid, CycloidGeometry


def test_cycloid_carrier():
	print()
	kinematics = Cycloid('c', 'p', 'r')
	print(kinematics)
	gear = CycloidGeometry.create(kinematics, 9, cycloid='epi', O=6)
	gear.animate()


def test_cycloid():
	print()
	kinematics = Cycloid('c', 'p', 'r')
	print(kinematics)
	gear = CycloidGeometry.create(kinematics, 4, cycloid='epi')
	gear.animate()

	gear = CycloidGeometry.create(kinematics, 4, cycloid='hypo')
	gear.animate()
