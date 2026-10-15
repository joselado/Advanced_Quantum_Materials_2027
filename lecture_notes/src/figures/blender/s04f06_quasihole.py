"""Figure s04f06, fig:s04:quasihole: the Laughlin quasihole, its charge and its statistics.

(a) A droplet as a flat-top surface with a dimple at w, the missing charge e/m, drawn schematically.
(b) The same droplet with two dimples, one carried once around the other along a loop (the arrow);
the Berry phase of the loop is the Aharonov-Bohm part plus 2 pi / m. In front, the exchange phase as
a bar from 0 (bosons) to pi (fermions) with pi/m for m = 3 marked. Schematic.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's04f06_quasihole'
XA, XB = -3.9, 3.0
R, H = 2.5, 0.55
M = 3


def droplet(name, x0, holes):
    def f(x, y):
        r = math.hypot(x, y)
        z = H / (1 + math.exp((r - R) / 0.15))
        for hx, hy in holes:
            z *= 1 - 0.85 * math.exp(-((x - hx) ** 2 + (y - hy) ** 2) / 0.12)
        return z
    ob = F.disc_surface(name, f, R + 0.6, F.SURFACE)
    ob.location = (x0, 1.2, 0.02)
    return ob


def build():
    F.studio()
    w = (0.6, 0.3)
    droplet('a_drop', XA, [w])
    F.anchor('w', (XA + w[0], 1.2 + w[1], 0.02))
    F.anchor('apanel', (XA - R - 0.2, 1.2 + R, H + 0.2))
    h1, h2 = (-0.25, 0.0), (1.25, 0.0)
    droplet('b_drop', XB, [h1, h2])
    rr = math.dist(h1, h2)
    pts = [(XB + h1[0] + rr * math.cos(a), 1.2 + h1[1] + rr * math.sin(a), H + 0.08)
           for a in [0.25 + 2 * math.pi * 0.88 * k / 80 for k in range(81)]]
    F.flow('loop', pts, r=0.03, rgb=F.BROKEN)
    F.anchor('h1', (XB + h1[0], 1.2, 0.05))
    F.anchor('loop', (XB + h1[0], 1.2 + rr + 0.1, H + 0.1))
    F.anchor('bpanel', (XB - R - 0.2, 1.2 + R, H + 0.2))
    # the exchange phase, from bosons to fermions
    x0, x1 = -2.2, 2.2
    F.tube('bar', [(x0, -2.2, 0.05), (x1, -2.2, 0.05)], 0.03, F.BOND)
    for x, kind in ((x0, 'ball'), (x1, 'ball'), (x0 + (x1 - x0) / M, 'mark')):
        if kind == 'ball':
            F.ball(f'end{x:.1f}', (x, -2.2, 0.09), 0.08, rgb=F.SITE)
        else:
            F.ball('anyon', (x, -2.2, 0.1), 0.11, rgb=F.BROKEN)
    F.anchor('boson', (x0, -2.45, 0.0))
    F.anchor('fermion', (x1, -2.45, 0.0))
    F.anchor('anyon', (x0 + (x1 - x0) / M, -2.45, 0.0))
    F.anchor('barlab', (x0 - 0.25, -2.2, 0.05))
    F.camera((-0.35, 0.05, 0.3), elev=42.0, ortho=15.4, aspect=2.9)


F.main(build, NAME)
