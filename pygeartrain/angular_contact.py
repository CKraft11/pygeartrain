from dataclasses import dataclass

from pygeartrain.core.kinematics import GearKinematics
from pygeartrain.core.geometry import GearGeometry
import numpy as np


class AngularContact(GearKinematics):
	"""4 point angular contact transmission
	Same as fixed-angle Eviolo in 'rob,rot,rib,rit' config

	"""
	# px and py lies on the planet/bearing rotation equator
	# 4 traction equations, for each corner contact; top/bottom, inner/outer
	# Dr is the diameter ratio of the ball ring divided by the ball diameter itself
	equations = [
		f'(Dr + P{io}{tb}x) * r{io}{tb} - Dr*c + P{io}{tb}x * px + P{io}{tb}y * py'
		for tb in 'tb' for io in 'io'
	]


@dataclass(repr=False)
class AngularContactGeometry(GearGeometry):
	points: np.ndarray
	angles: np.ndarray

	@classmethod
	def from_geometry(cls, kinematics, cone=5, squat=10, tilt=0, asym=0, Dr=3):
		a = cls.get_angles(cone=cone, squat=squat, tilt=tilt, asym=asym)
		P = cls.get_points(a)
		# translate contact points into input compatible with kinematics description
		geometry = {'Dr': Dr}
		for io, PP in zip('io', P):
			for bt, PPP in zip('bt', PP):
				for xy, PPPP in zip('xy', PPP):
					geometry['P'+io+bt+xy] = PPPP
		return cls(
			angles=a,
			points=P,
			kinematics=kinematics,
			geometry=geometry,
		)

	@classmethod
	def get_angles(cls, cone, squat, tilt, asym):
		"""

		Parameters
		----------
		cone: float, degrees
			conicity; major driver of ratios
		squat: float, degrees
			squat means flatness of contacts.
			flatter means more radial, less axial capacity.
			more squat, also means less contact point rotation
			low squat also lowers ratios
			more squat, also means lower axial preload requirements?
			high squat also eats into moment arm to transfer torque over the ball
		tilt: float, degrees
			tilt of contacts. does not seem hugely influential on net ratios
		asym: float, degrees
			assymmetry; diff in spacing between contat points, inner/outer

		Returns
		-------
		Point coordinates of contact points
		"""
		a = [
			[-135 - cone + tilt - squat + asym, +135 - cone + tilt + squat - asym],
			[-45 + cone + tilt + squat + asym, 45 + cone + tilt - squat - asym],
		]
		return np.array(a) / 180 * np.pi

	@classmethod
	def get_points(cls, angles):
		return np.dstack([np.cos(angles), np.sin(angles)])

	def plot(self, show=True, filename=None):
		import matplotlib.pyplot as plt
		fig, ax = plt.subplots()
		P = self.points
		a = (self.angles * 180 / np.pi).astype(int)
		ax.scatter([0], [0])
		ax.scatter(P[..., 0].flatten(), P[..., 1].flatten())
		axis = np.array([-self.ratios_f['py'], self.ratios_f['px']])
		axis = axis / np.linalg.norm(axis) * 1.1
		plt.plot(*(axis[:, None] * [-1, +1]))

		text = lambda t, p, a: plt.text(*p, t, horizontalalignment='center', verticalalignment='center', rotation=a)
		for i in range(2):
			for j in range(2):
				text(a[i][j], P[i, j] * 0.8, 0)

		# FIXME: this code assumes fused inner rings
		text('ground', P[1, 0] * 1.1, a[1, 0] - 90)
		text('output', P[1, 1] * 1.1, a[1, 1] - 90)
		text('input', P[0, :].mean(axis=0) * 1.2, a[0].mean(axis=0) + 90)

		a = np.linspace(0, 2 * np.pi, 200)
		xy = np.array([np.cos(a), np.sin(a)]).T
		# plot cup shapes
		delta = xy.reshape(-1, 1, 2) - P.reshape(1, 4, 2)
		dist = np.linalg.norm(delta, axis=2)
		mindist = np.min(dist, axis=1)
		curve_ratio = 0.5  # 0=unit circle, 1=flat
		r = mindist ** 2 * curve_ratio / 2 + 1
		ds = np.linalg.norm(P[:, 0] - P[:, 1], axis=1)
		r[np.logical_and(xy[:, 0] < 0, mindist > ds[0] / 1.9)] = np.nan
		r[np.logical_and(xy[:, 0] > 0, mindist > ds[1] / 2.1)] = np.nan
		# r[[0, 1, -1, -2]] = np.nan # split ring
		ax.plot(*(xy * r[:, None]).T)

		ax.plot(*xy.T)

		ax.axis('equal')
		plt.title(f'input/output =  {self.ratio:.2f}')
		plt.xlabel('inner <-> outer')
		plt.ylabel('bottom <-> top')
		# plt.axis('off')
		if filename:
			fig.savefig(filename)
		if show:
			plt.show()
