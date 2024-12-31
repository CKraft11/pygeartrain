from pygeartrain.compound_planetary import CompoundPlanetary, CompoundPlanetaryGeometry


def test_compound_planetary():
	print()
	# sun-driven
	kinematics = CompoundPlanetary('s1', 'r2', 'r1')
	print(kinematics)
	gear = CompoundPlanetaryGeometry.create(kinematics, (5, 2, 1), (4, 1, 2), 3, b1=0.25, b2=0.75)
	gear.animate()
	gear = CompoundPlanetaryGeometry.create(kinematics, (11, 2, 7), (8, 2, 4), 6, b1=0.6, b2=0.4)
	gear.animate()
	gear = CompoundPlanetaryGeometry.create(kinematics, (15, 5, 5), (14, 4, 6), 5, b1=0.4, b2=0.7)
	gear.animate()
	gear = CompoundPlanetaryGeometry.create(kinematics, (22, 7, 8), (21, 6, 9), 5, b1=0.4, b2=0.6)
	gear.animate()

	# carrier-driven
	kinematics = CompoundPlanetary('c', 'r2', 'r1')
	print(kinematics)
	gear = CompoundPlanetaryGeometry.create(kinematics, (15, 5, 5), (14, 4, 6), 5, b1=0.4, b2=0.7)
	print(gear)
	gear.animate()


def test_readme_animation():
	# sun-driven
	kinematics = CompoundPlanetary('s1', 'r2', 'r1')
	print(kinematics)
	gear = CompoundPlanetaryGeometry.create(kinematics, (5, 2, 1), (4, 1, 2), 3, b1=0.25, b2=0.75)
	gear.save_animation(frames=40, basename='compound')


def test_readme():
	kinematics = CompoundPlanetary('s1', 'r2', 'r1')
	gear = CompoundPlanetaryGeometry.create(kinematics, (22, 7, 8), (21, 6, 9), 5, b1=0.4, b2=0.6)
	gear.plot(show=False, filename='compound.png')
