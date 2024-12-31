from tkinter.messagebox import showerror

from pygeartrain.angular_contact import *



def test_ratio():
	print()
	# low ratio eviolo-style, static inner ring
	kinematics = AngularContact('rob','rot','rib','rib-rit')
	print(kinematics)
	gear = AngularContactGeometry.from_geometry(kinematics)
	print(gear)

	# high ratio, driven by the fused ring; wolfram topology
	kinematics = AngularContact('rib','rot','rob','rib-rit')
	print(kinematics)
	gear = AngularContactGeometry.from_geometry(kinematics, cone=5, tilt=0)
	print(gear)
	gear.plot()


def test_readme():
	print()
	# high ratio, driven by the fused ring; wolfram topology
	kinematics = AngularContact('rib','rot','rob','rib-rit')
	print(kinematics)
	gear = AngularContactGeometry.from_geometry(kinematics, cone=5, tilt=5)
	gear.plot(show=False, filename='../../angular_contact.png')