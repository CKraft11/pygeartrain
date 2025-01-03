from dataclasses import dataclass
from typing import Dict

import numpy as np
from sympy.core.cache import cached_property

from pygeartrain.core.kinematics import GearKinematics


def flatten(l):
    out = []
    if isinstance(l, (list, tuple)):
        for item in l:
            out.extend(flatten(item))
    else:
        out.append(l)
    return out

def fig_to_array(fig):
    import matplotlib.pyplot as plt
    canvas = plt.gca().figure.canvas
    canvas.draw()
    data = np.frombuffer(canvas.tostring_rgb(), dtype=np.uint8)
    return data.reshape((int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2])) + (3,))

    # import io
    # with io.BytesIO() as io_buf:
    #     fig.savefig(io_buf, format='raw')
    #     image = np.frombuffer(io_buf.getvalue(), np.uint8).reshape(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1)
    # return image


@dataclass
class GearGeometry:
    kinematics: GearKinematics
    geometry: Dict[str, float]  # values to stick into kinematic equations

    @cached_property
    def ratio(self):
        return self.kinematics.ratio.subs(self.geometry)
    @cached_property
    def ratios(self):
        return {k: r.subs(self.geometry) for k, r in self.kinematics.solve.items()}
    @cached_property
    def ratios_f(self):
        return {k: float(r.evalf()) for k, r in self.ratios.items()}

    def __repr__(self):
        geo = str(self.geometry).replace("'", "").replace(" ", "")
        return f'{self.kinematics.input}/{self.kinematics.output}: {self.kinematics.ratio} = {self.ratio} \n {geo}'

    @cached_property
    def generate_profiles(self):
        """Generate all gear elements in a correctly meshing fashion"""
        raise NotImplementedError

    def arrange(self, phase=0):
        """Arrange profiles given phase advancement of whole geartrain"""
        raise NotImplementedError

    @cached_property
    def limit(self):
        """For fixing plot bounds"""
        profiles = flatten(self.arrange(0))
        return max(np.max(np.linalg.norm(p.vertices, axis=1)) for p in profiles)*1.05

    def _plot(self, phase, ax, **kwargs):
        """Plotting"""
        raise NotImplementedError

    def plot(self, phase=0, ax=None, show=True, filename=None, **kwargs):
        import matplotlib.pyplot as plt
        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = plt.gcf()

        self._plot(phase=phase, ax=ax, **kwargs)

        lim = self.limit
        plt.xlim(-lim, +lim)
        plt.ylim(-lim, +lim)
        plt.title(str(self))
        plt.axis('off')
        if filename:
            fig.savefig(filename)
        if show:
            plt.show()

    def animate(self, scale=None):
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation

        if scale is None:
            rs = [np.abs(1/r) for r in self.ratios_f.values() if r]
            scale = np.prod(rs) ** (1 / len(rs)) / 50
        counter = [0]
        def updatefig(*args):
            counter[0] += 1
            phase = counter[0] * scale
            ax = plt.gca()
            ax.cla()
            self.plot(phase=phase, ax=ax, show=False)

        self.plot(phase=0, show=False)
        ani = animation.FuncAnimation(plt.gcf(), updatefig, interval=10, blit=False)
        plt.show()

    def save_animation(self, frames, filename, total=np.pi/2):
        import matplotlib.pyplot as plt
        self.plot(show=False)
        fig = plt.gcf()
        ax = plt.gca()
        data = []
        for i in range(frames):
            ax.cla()
            phase = i/frames*total
            self.plot(ax=ax, phase=phase, show=False)
            data.append(fig_to_array(fig))
        data = np.array(data)
        import imageio.v3 as iio
        iio.imwrite(filename, data, loop=0, fps=30)
        plt.close(fig)
