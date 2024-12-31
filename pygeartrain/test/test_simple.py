from pygeartrain.simple import SimpleGear, SimpleGeometry


def test_simple():
	print()
	kinematics = SimpleGear('a', 'b')
	print(kinematics)
	gear = SimpleGeometry(kinematics, {'A': 4, 'B': 5})
	gear.animate()
