"""Shared code of the picture options of the quiz of Section 5.3, the field lines around a sphere in a field along z.

The field code is copied from tc_meissner.py and generalized to a sphere that expels a part of the field. Outside a
sphere of radius a in a uniform field B0 along z, with the field B_in = (1 + 2 beta) B0 inside, the field is
B_r = B0 cos(th) (1 + 2 beta a^3/r^3) and B_th = -B0 sin(th) (1 - beta a^3/r^3), which is divergence free and has B_r
continuous at r = a. beta = 0 is no sample, the lines cross it, beta = -1/2 is a perfect diamagnet with B = 0 inside,
the Meissner state, and beta = -1/4 lets half of the field through. In the last picture the lines inside are drawn
in thin tubes, the vortices of a type-II superconductor at a moderate field, each tube with one line. The drawing is
the cut y = 0 of the sphere, where the field lies in the plane by symmetry, so the lines are true field lines. A
picture is a drawing of real space with no axes, so it is saved with sketch=True. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import style

A = 1.0                                                       # the radius of the sphere
BETA = {'cross': 0.0, 'around': -0.5, 'vortices': -0.25}
STARTS = np.linspace(-2.2, 2.2, 12)                           # the lines start at these x, far below the sphere
Z0 = -2.55


def field(x, z, beta):
    """(B_x, B_z) in units of B0 at the points (x, z) of the plane y = 0."""
    r = np.hypot(x, z)
    th = np.arctan2(np.abs(x), z)
    sgn = np.where(x >= 0, 1.0, -1.0)
    with np.errstate(divide='ignore', invalid='ignore'):
        Br = np.cos(th) * (1 + 2 * beta * A ** 3 / r ** 3)
        Bt = -np.sin(th) * (1 - beta * A ** 3 / r ** 3)
    Bx = (Br * np.sin(th) + Bt * np.cos(th)) * sgn
    Bz = Br * np.cos(th) - Bt * np.sin(th)
    inside = r < A
    return np.where(inside, 0.0, Bx), np.where(inside, 1 + 2 * beta, Bz)


def trace(x0, beta, step=0.004, zmax=2.55):
    """A field line from (x0, Z0), by Runge-Kutta steps along the unit field, up to z = zmax."""
    p = np.array([x0, Z0])
    pts = [p.copy()]
    for _ in range(4000):
        def u(q):
            b = np.array(field(np.array(q[0]), np.array(q[1]), beta), dtype=float)
            return b / max(np.linalg.norm(b), 1e-12)
        k1 = u(p); k2 = u(p + step / 2 * k1); k3 = u(p + step / 2 * k2); k4 = u(p + step * k3)
        p = p + step / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        pts.append(p.copy())
        if p[1] > zmax:
            break
    return np.array(pts)


def check():
    """The field is divergence free in three dimensions, B_r is continuous at the surface, the Meissner field is
    tangent to it, and four lines of the last picture pass through the sphere."""
    th = np.linspace(0.05, np.pi - 0.05, 50)
    for beta in BETA.values():
        Bx, Bz = field(A * 1.0001 * np.sin(th), A * 1.0001 * np.cos(th), beta)
        Br_out = Bx * np.sin(th) + Bz * np.cos(th)
        assert np.allclose(Br_out, (1 + 2 * beta) * np.cos(th), atol=1e-3)
        # div B = (1/r^2) d(r^2 B_r)/dr + (1/(r sin th)) d(sin th B_th)/dth vanishes outside, checked at r = 1.7
        r, h = 1.7, 1e-5
        Brf = lambda rr, tt: np.cos(tt) * (1 + 2 * beta * A ** 3 / rr ** 3)
        Btf = lambda rr, tt: -np.sin(tt) * (1 - beta * A ** 3 / rr ** 3)
        div = ((r + h) ** 2 * Brf(r + h, th) - (r - h) ** 2 * Brf(r - h, th)) / (2 * h * r ** 2) \
            + (np.sin(th + h) * Btf(r, th + h) - np.sin(th - h) * Btf(r, th - h)) / (2 * h * r * np.sin(th))
        assert np.abs(div).max() < 1e-6
    entering = [x0 for x0 in STARTS if np.any(np.hypot(*trace(x0, BETA['vortices']).T) < A)]
    assert len(entering) == 4, entering
    assert not any(np.any(np.hypot(*trace(x0, BETA['around']).T) < A * 0.999) for x0 in STARTS)


def option(script, name):
    """One picture option, the field lines of BETA[name], with the same sample and the same window for the three."""
    check()
    beta = BETA[name]
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    ax.add_patch(Circle((0, 0), A, fc='#e6edf4', ec='none', zorder=1))
    for x0 in STARTS:
        line = trace(x0, beta)
        ax.plot(line[:, 0], line[:, 1], color=style.ACCENT, lw=1.0, zorder=3)
        i = np.argmin(np.abs(line[:, 1] + 1.8))                       # one arrow head below the sphere
        ax.annotate('', xy=tuple(line[i + 12]), xytext=tuple(line[i]), zorder=3,
                    arrowprops=dict(arrowstyle='-|>', color=style.ACCENT, lw=0.8, mutation_scale=10, shrinkA=0, shrinkB=0))
        inside = np.hypot(line[:, 0], line[:, 1]) < A
        if name == 'vortices' and inside.any():
            x = line[inside, 0].mean()
            hz = np.sqrt(A ** 2 - x ** 2)
            tube = Rectangle((x - 0.09, -hz), 0.18, 2 * hz, fc=style.LIGHT, ec='none', alpha=0.8, zorder=2)
            ax.add_patch(tube)
            tube.set_clip_path(Circle((0, 0), A, transform=ax.transData))
    ax.add_patch(Circle((0, 0), A, fc='none', ec=style.INK, lw=0.8, zorder=4))
    ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.6, 2.6); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((-2.4, -2.6), 4.8, 5.2, fill=False, lw=0, ec='none'))   # the same window for the three
    style.save(fig, script, sketch=True)
