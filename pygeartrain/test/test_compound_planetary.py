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
	gear = CompoundPlanetaryGeometry.create(kinematics, (15, 5, 5), (14, 4, 6), 5, b1=0.3, b2=0.7)
	gear.animate()
	gear = CompoundPlanetaryGeometry.create(kinematics, (22, 7, 8), (21, 6, 9), 5, b1=0.4, b2=0.6)
	gear.animate()
	gear = CompoundPlanetaryGeometry.create(kinematics, (27, 6, 15), (28, 7, 14), 7, b1=0.6, b2=0.4)
	gear.animate()
	gear = CompoundPlanetaryGeometry.create(kinematics, (32, 8, 16), (26, 6, 14), 8, b1=0.4, b2=0.5)
	gear.animate()


def test_50():
	kinematics = CompoundPlanetary('s1', 'r2', 'r1')
	gear = CompoundPlanetaryGeometry.create(kinematics, (13, 4, 5), (21, 6, 9), 6, b1=0.33, b2=0.66)
	gear.plot(filename='252_2.png')
	gear.animate(scale=0.0001)
	gear = CompoundPlanetaryGeometry.create(kinematics, (15, 3, 9), (19, 4, 11), 6, b1=0.6, b2=0.6)
	gear.animate()

	# compound((5, 4, 13), (9, 6, 21), 6, 0.66, 0.33)  # 50.400000000000006, 0.27433388230813804, 0.4)
	# compound((9, 3, 15), (11, 4, 19), 6, 0.4, 0.4)  # 50.66666666666667, 16.699111843077517, 0.4)


def test_compound_planetary_carrier():
	# carrier-driven
	kinematics = CompoundPlanetary('c', 'r2', 'r1')
	print(kinematics)
	gear = CompoundPlanetaryGeometry.create(kinematics, (15, 5, 5), (14, 4, 6), 5, b1=0.4, b2=0.7)
	print(gear)
	print(gear.ratios)
	gear.animate()


def test_low():
	print()
	# sun-driven
	kinematics = CompoundPlanetary('s1', 'r2', 'r1')
	print(kinematics)
	gear = CompoundPlanetaryGeometry.create(kinematics, (20, 4, 12), (16, 4, 8), 8, b1=0.7, b2=0.3)
	gear.plot(filename='32_3.png')
	gear.animate()
	gear = CompoundPlanetaryGeometry.create(kinematics, (28, 4, 20), (22, 4, 14), 12, b1=0.65, b2=0.35)
	gear.animate()
	gear = CompoundPlanetaryGeometry.create(kinematics, (30, 4, 22), (31, 5, 21), 13, b1=0.55, b2=0.3)
	gear.animate()
	gear = CompoundPlanetaryGeometry.create(kinematics, (42, 4, 34), (43, 5, 33), 19, b1=0.55, b2=0.3)
	gear.animate()

	# # nice ones in the 10 gear range. simpler gearboxes may exist in this range but not with such nice self bearing props
	# # 10 range should be quite easy to backdrive?
	# # compound((12, 4, 20), (8, 4, 16), 8)#10.666666666666666, 1.6991118430775174, 0.5)
	# # compound((20, 4, 28), (14, 4, 22), 12)#8.8, 4.548667764616276, 0.5)
	# # kinda cool; seems all planets are idential
	# compound((22, 4, 30), (21, 5, 31), 13, 0.3,
	# 		 0.6)  # 11.272727272727272, 11.681408993334628, 0.5) # noice; usually the primes dont do this well
	# # compound((34, 4, 42), (33, 5, 43), 19)#10.117647058823529, 19.38052083641213, 0.5)


def test_compound_planetary_high():
	"""very high ratio with limited number of teeth"""
	print()
	# sun-driven
	kinematics = CompoundPlanetary('s1', 'r2', 'r1')
	print(kinematics)
	gear = CompoundPlanetaryGeometry.create(kinematics, (55, 21, 13), (42, 16, 10), 4, b1=0.55, b2=0.45)
	print(gear.ratios_f['s1'] / sum(gear.G1+gear.G2))	# this 14 is really extreme; usually its close to 1.
	# gear.animate()
	# gear.plot(show=False, filename='2307.png')
	# also pretty good ratio-per-teeth, with lower absolutes. also super close in absolute tooth count
	gear = CompoundPlanetaryGeometry.create(kinematics, (37, 13, 11), (34, 12, 10), 4)
	print(gear.ratios_f['s1'] / sum(gear.G1+gear.G2))
	gear.save_animation(frames=40, total=.01, basename='compound')
	# print(gear.ratios_f['s1'])
	# gear.plot(show=False, filename='964.png')
	# gear.animate()


def test_compound_backdrive():
	"""https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8867893
	large planets seems to be the key to high efficiency
	"""
	print()
	# sun-driven
	kinematics = CompoundPlanetary('s1', 'r2', 'r1')
	print(kinematics)
	gear = CompoundPlanetaryGeometry.create(kinematics, (90, 39, 12), (81, 32, 17), 3, b1=0.5, b2=0.5)
	print(gear.ratios_f['s1'] / sum(gear.G1+gear.G2))	# this 14 is really extreme; usually its close to 1.
	gear.plot(123)

	gear = CompoundPlanetaryGeometry.create(kinematics, (43, 19, 5), (46, 19, 8), 3, b1=0.5, b2=0.5)
	print(gear.ratios_f['s1'] / sum(gear.G1+gear.G2))	# this 14 is really extreme; usually its close to 1.
	gear.plot(filename='736_5.png')
	gear.plot(123)
	# eval_compound_symbolic((5, 19, 43),
	# 					   (8, 19, 46))  # , 3)  # 147.20000000000002, 8.898223686155035, 0.1111111111111111)


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
