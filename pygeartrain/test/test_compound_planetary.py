from pygeartrain.compound_planetary import CompoundPlanetary, CompoundPlanetaryGeometry


def test_compound_planetary():
	print()
	# sun-driven
	kinematics = CompoundPlanetary('s1', 'r2', 'r1')
	print(kinematics)
	gear = CompoundPlanetaryGeometry.create(kinematics, (5, 2, 1), (4, 1, 2), 3, b1=0.25, b2=0.75)
	gear.animate()
	gear = CompoundPlanetaryGeometry.create(kinematics, (11, 2, 7), (8, 2, 4), 6, b1=0.7, b2=0.4)
	gear.animate()
	gear = CompoundPlanetaryGeometry.create(kinematics, (15, 5, 5), (14, 4, 6), 5, b1=0.4, b2=0.7)
	gear.animate()
	gear = CompoundPlanetaryGeometry.create(kinematics, (22, 7, 8), (21, 6, 9), 5, b1=0.4, b2=0.6)
	gear.animate()
	gear = CompoundPlanetaryGeometry.create(kinematics, (27, 6, 15), (28, 7, 14), 7, b1=0.6, b2=0.4)
	gear.animate()
	gear = CompoundPlanetaryGeometry.create(kinematics, (32, 8, 16), (26, 6, 14), 8, b1=0.4, b2=0.5)
	gear.animate()


def test_compound_planetary_carrier():
	# carrier-driven
	kinematics = CompoundPlanetary('c', 'r2', 'r1')
	print(kinematics)
	gear = CompoundPlanetaryGeometry.create(kinematics, (15, 5, 5), (14, 4, 6), 5, b1=0.4, b2=0.7)
	print(gear)
	gear.animate()


def test_compound_planetary_high():
	"""very high ratio with limited number of teeth"""
	print()
	# sun-driven
	kinematics = CompoundPlanetary('s1', 'r2', 'r1')
	print(kinematics)
	gear = CompoundPlanetaryGeometry.create(kinematics, (55, 21, 13), (42, 16, 10), 4, b1=0.55, b2=0.45)
	print(gear.ratios_f['s1'] / sum(gear.G1+gear.G2))	# this 14 is really extreme; usually its close to 1.
	gear.animate()
	# gear.plot(show=False, filename='2307.png')
	# also pretty good ratio-per-teeth, with lower absolutes. also super close in absolute tooth count
	gear = CompoundPlanetaryGeometry.create(kinematics, (37, 13, 11), (34, 12, 10), 4)
	print(gear.ratios_f['s1'] / sum(gear.G1+gear.G2))
	gear.animate()


def test_readme_animation():
	"""Using this example because it has a managable periodicity"""
	kinematics = CompoundPlanetary('s1', 'r2', 'r1')
	print(kinematics)
	gear = CompoundPlanetaryGeometry.create(kinematics, (5, 2, 1), (4, 1, 2), 3, b1=0.25, b2=0.75)
	gear.save_animation(frames=40, basename='compound')


def test_readme():
	kinematics = CompoundPlanetary('s1', 'r2', 'r1')
	gear = CompoundPlanetaryGeometry.create(kinematics, (22, 7, 8), (21, 6, 9), 5, b1=0.4, b2=0.6)
	gear.plot(show=False, filename='compound.png')


def test_gdfw():
	kinematics = CompoundPlanetary('s1', 'r2', 'r1')
	# geardownforwhat cf record holder; looking rather good now that upping the tooth count
	gear = CompoundPlanetaryGeometry.create(kinematics, (56, 11, 34), (50, 10, 30), 10, 0.4, 0.4)
	gear.animate()
	# this one seems strictly superior; same proprtions and gear ratio, but more printable and harder to skip teeth
	gear = CompoundPlanetaryGeometry.create(kinematics, (43, 8, 27), (37, 7, 23), 10, 0.4, 0.4)
	gear.animate()
