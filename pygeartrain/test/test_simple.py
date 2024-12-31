from pygeartrain.simple import SimpleGear, SimpleGeometry, NestedGear, NestedGeometry


def test_simple():
	print()
	kinematics = SimpleGear('a', 'b')
	print(kinematics)
	gear = SimpleGeometry(kinematics, {'A': 4, 'B': 5})
	gear.animate()


def test_nested():
	print()
	kinematics = NestedGear('a', 'b')
	print(kinematics)
	gear = NestedGeometry(kinematics, {'N': 4})
	gear.animate()
