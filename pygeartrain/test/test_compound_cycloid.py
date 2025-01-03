from pygeartrain.compound_cycloid import *


def test_epi():
	print()
	# carrier-driven
	# kinematics = CompoundCycloid('c', 'r1', 'r2')
	kinematics = CompoundCycloid('c', 'r2', 'r1')
	print(kinematics)
	# gear = CompoundCycloidGeometry(kinematics, {'P1': 3, 'P2': 4})
	# gear = CompoundCycloidGeometry.create(kinematics, P1=8, P2=4, b=1.2, f=0.9, cycloid='epi')
	gear = CompoundCycloidGeometry.create(kinematics, P1=8, P2=7, b=1.2, f=0.5, cycloid='epi')
	gear.plot(123)
	gear.animate()


def test_hypo():
	print()
	kinematics = CompoundCycloid('c', 'r2', 'r1')
	print(kinematics)
	gear = CompoundCycloidGeometry.create(kinematics, P1=6, P2=7, b=3.7, f=0.7, cycloid='hypo')
	# gear.save_animation(100, 'hypo.gif', total=0.3)
	gear.animate()


def test_readme():
	print()
	# carrier-driven
	kinematics = CompoundCycloid('c', 'r2', 'r1')
	gear = CompoundCycloidGeometry.create(kinematics, P1=3, P2=4)
	gear.plot(show=False, filename='../../cycloid.png')
