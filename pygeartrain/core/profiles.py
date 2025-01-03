import numpy as np


def ring(c):
    """Encode periodic vertex list to closed cubical complex"""
    from pycomplex.complex.cubical import ComplexCubical1Euclidian2
    v = np.arange(len(c))
    cubes = np.array([np.roll(v, 1), v]).T
    return ComplexCubical1Euclidian2(vertices=c, cubes=cubes)


def rotation(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, s], [-s, c]])


def trochoid_part(R, r, s, res, endpoint=False):
    # r = R / N
    N = R / r
    a = np.linspace(0, 2*np.pi/N, int(r * res), endpoint=endpoint)
    b = (R+r*s) / r * a * s

    q = [[np.cos(a), np.cos(b)], [np.sin(a), np.sin(b)]]
    return np.dot([(R+r*s), -r*s], q).T


def epitrochoid(a: float, q: int, d: float, N=2000):
    b = a / q
    k = d / b
    t = np.linspace(0, np.pi*2, N)
    x = b * ((q + 1) * np.cos(t) - k * np.cos((q+1)*t))
    y = b * ((q + 1) * np.sin(t) - k * np.sin((q+1)*t))

    q = (a + b) / b
    x = (a + b) * np.cos(t) - d * np.cos(q*t)
    y = (a + b) * np.sin(t) - d * np.sin(q*t)
    return np.array([x, y]).T


def hypotrochoid(a: float, q: int, d: float):
    """
    where a is the radius of the base circle,
    b = a / q that of the rolling circle,
    and d = k b the distance between the point and the centre of the moving circle
    """
    # a = a - 0.6
    b = a / q
    k = d / b
    # k = 0.6
    t = np.linspace(0, np.pi*2, 500)
    # x = b * ((q - 1) * np.cos(t) + k * np.cos((q-1)*t))
    # y = b * ((q - 1) * np.sin(t) - k * np.sin((q-1)*t))

    q = (a - b) / b
    x = (a + b) * np.cos(t) + d * np.cos(q*t)
    y = (a + b) * np.sin(t) - d * np.sin(q*t)

    return np.array([x, y]).T


def sinusoid(n_teeth: int, slope=1/10, amplitude=None, pitch_radius: float=1.0, n_points=2000, fb=0):
    a = np.linspace(0, np.pi * 2, n_points)
    if amplitude is None:
        tooth_length = pitch_radius / n_teeth
        amplitude = tooth_length * slope
    # add tangential motion, to fiddle contact point, like trochoid?
    #  not sure its desirable; just gives moment arm to static friction components?
    # add flank bias; offset with q**2?
    #  needs to be flipped for interior gears

    q = np.sin(n_teeth * a)
    qs = q*q
    q2 = qs * np.sign(q)

    # positive values make it more sawtoothy; negative values more snub
    # more snub gives more clearance, and less urethane consumption
    # but a lowering effect on skipping torque
    fb2 = 0.25
    fb2 = 0.1

    x = (pitch_radius + amplitude * (q + fb * qs + fb2 * q2)) * np.cos(a)
    y = (pitch_radius + amplitude * (q + fb * qs + fb2 * q2)) * np.sin(a)
    return np.array([x, y]).T


def involute(n_teeth, pressure_angle, pitch_radius):
    """how to parametrize? offset relative to pitch circle?"""
    n_points = 10   # points per tooth
    a = np.linspace(0, np.pi * 2)
    s = np.sin(n_teeth * a)
    c = np.cos(n_teeth * a)

    base_radius = pitch_radius * np.cos(pressure_angle)

    # for i in range(0, involutePointCount):
    #     involuteIntersectionRadius = (baseCircleDia / 2.0) + ((involuteSize / (involutePointCount - 1)) * i)
    #     newPoint = involutePoint(baseCircleDia / 2.0, involuteIntersectionRadius)
    #     involutePoints.append(newPoint)

    x = c + s * a
    y = s - c * a

    return np.array([x, y]).T * base_radius


def epi_hypo_gear(R, N, f, res):
    """compound gear of alternating epi and hypo curves

    Parameters
    ----------
    R: float
        radius of fixed circle
    N: int
        number of teeth
    f: float
        fraction of epi-vs-hypo
    res: int
        number of vertices per curve-section
    """
    # return circle(R)
    r = R / N
    t = 2*np.pi/N
    p = trochoid_part(R, r * f, +1, res=res)
    n = trochoid_part(R, r * (1 - f), -1, res=res)
    p = np.dot(p, rotation(-t*f/2))
    n = np.dot(n, rotation(t*f/2))
    # n = np.dot(n, rotation(t*f))
    u = np.concatenate([p, n], axis=0)
    c = np.concatenate([np.dot(u, rotation(t*i)) for i in range(N)], axis=0)
    return ring(c)


def buffer(complex, r):
    from shapely.geometry import Polygon
    poly = Polygon(complex.vertices).buffer(r)
    coords = np.array(poly.exterior.coords)
    # print(len(coords))
    return ring(coords[::-1])


def hypo_gear(R, N, f=1):
    """
    References
    ----------
    https://www.researchgate.net/publication/303053954_Specific_Sliding_of_Trochoidal_Gearing_Profile_in_the_Gerotor_Pumps
    """
    return ring(hypotrochoid(R, N, f))

def hypo_gear_offset(R, N, b, f=1):
    return buffer(hypo_gear(R, N, f), b)

def epi_gear(R, N, f=1):
    """
    References
    ----------
    https://www.researchgate.net/publication/303053954_Specific_Sliding_of_Trochoidal_Gearing_Profile_in_the_Gerotor_Pumps
    """
    return ring(epitrochoid(R, N, f))

def epi_gear_offset(R, N, b, f=1):
    """
    References
    ----------
    https://www.researchgate.net/publication/303053954_Specific_Sliding_of_Trochoidal_Gearing_Profile_in_the_Gerotor_Pumps
    """
    return buffer(epi_gear(R, N, f), b)


def concat(geo):
    es = [a.topology.elements[-1] for a in geo]
    offsets = np.cumsum([0] + [len(e) for e in es])
    return type(geo[0])(
        vertices=np.concatenate([a.vertices for a in geo], axis=0),
        cubes=np.concatenate([e + o for e, o in zip(es, offsets)], axis=0)
    )


def make_pins(N, R, r):
    pin = circle(r)
    return concat([pin.translate([R, 0]).transform(rotation(i / N * 2 * np.pi)) for i in range(N)])


def circle(R, N=100):
    return ring(sinusoid(1, 0, 0, R, n_points=N))
