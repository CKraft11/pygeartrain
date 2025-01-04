from pygeartrain.nabtesco import *


def test_nabtesco():
	print()
	kinematics = NabtescoKinematics('s', 'o', 'r')
	print(kinematics.solve)
	# gear = NabtescoGeometry.create(kinematics, L=15, S=10, W=8)
	gear = NabtescoGeometry.create(kinematics, L=15, S=8, W=19, b=1.5, f=0.8)
	# gear = NabtescoGeometry.create(kinematics, L=15, S=10, W=16, b=1.5, f=0.9, N=4)# N=2)
	# gear = NabtescoGeometry.create(kinematics, L=10, S=1, W=20, b=1.5, f=0.9, N=2)

	print(gear.ratios)
	# gear.plot(123)
	# gear.save_animation(150, 'nabtesco.gif', 1.0)
	gear.animate()#(scale=0.001)
