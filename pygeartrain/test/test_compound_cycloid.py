from pygeartrain.compound_cycloid import *


def test_ratio():
	print()
	# carrier-driven
	# kinematics = CompoundCycloid('c', 'r1', 'r2')
	kinematics = CompoundCycloid('c', 'r2', 'r1')
	print(kinematics)
	# gear = CompoundCycloidGeometry(kinematics, {'P1': 3, 'P2': 4})
	gear = CompoundCycloidGeometry.create(kinematics, P1=3, P2=4)

	gear.animate()


def test_readme():
	print()
	# carrier-driven
	kinematics = CompoundCycloid('c', 'r2', 'r1')
	gear = CompoundCycloidGeometry.create(kinematics, P1=3, P2=4)
	gear.plot(show=False, filename='../../cycloid.png')
