"""Figure s03f04, fig:s03:winding: the winding of d(k) = t + exp(ik) for t = 0.5, 1, 1.5.

Seen from the front. For each t, the complex plane standing upright, the origin as a ball, and
d(k) as a ring of radius 1 centered at (t, 0) with an arrowhead in the direction of increasing k;
next to it the bands E = +-|d(k)| over k in [-pi, pi]. (a) t = 0.5 winds once around the
origin, (b) t = 1 passes through it and the gap closes at k = pi, (c) t = 1.5 does not wind.
"""
import cmath
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's03f04_winding'
TS = (0.5, 1.0, 1.5)
XS = (-5.4, -0.2, 5.0)                 # the three columns
RS = 0.62                              # drawn radius of the unit circle
SXB, Z0, SZ = 0.3, 1.2, 0.42           # the band plot: x per unit of k, height of E = 0, height per unit


def build():
    F.studio()
    for c, (t, x0) in enumerate(zip(TS, XS)):
        tag = 'abc'[c]
        F.PREFIX[0] = tag
        xr, zr = x0 - 1.55, 1.2                        # the complex plane, standing upright
        F.rod(f'{tag}_re', (xr - 0.85, 0, zr), (xr + 1.65, 0, zr), r=0.012)
        F.rod(f'{tag}_im', (xr, 0, zr - 0.95), (xr, 0, zr + 0.95), r=0.012)
        enclosed = t < 1
        F.ball(f'{tag}_origin', (xr, -0.05, zr), 0.08, rgb=F.BROKEN if enclosed else F.SITE)
        pts = [(xr + RS * (t + math.cos(a)), 0, zr + RS * math.sin(a))
               for a in [-math.pi + 0.15 + 2 * math.pi * 0.92 * k / 80 for k in range(81)]]
        F.flow(f'{tag}_ring', pts, r=0.025, rgb=F.ACCENT_AQM)
        F.anchor('zero', (xr - 0.05, 0, zr - 0.05))
        F.anchor('re', (xr + RS * (t + 0.7), 0, zr + RS * 0.75))
        F.anchor('t', (x0 - 0.6, 0, 2.8))
        # the bands
        xb = x0 + 1.15
        ks = [-math.pi + 2 * math.pi * k / 200 for k in range(201)]
        for sgn in (1, -1):
            F.tube(f'{tag}_E{sgn}', [(xb + SXB * k, 0, Z0 + sgn * SZ * abs(t + cmath.exp(1j * k))) for k in ks],
                   0.03, F.ACCENT_AQM)
        F.axis(f'{tag}_ay', (xb - SXB * math.pi, 0, Z0 - 2.6 * SZ), (xb - SXB * math.pi, 0, Z0 + 2.9 * SZ),
               r=0.016, head=0.12)
        F.rod(f'{tag}_ax', (xb - SXB * math.pi, 0, Z0 - 2.6 * SZ), (xb + SXB * math.pi, 0, Z0 - 2.6 * SZ), r=0.016)
        F.tube(f'{tag}_zl', [(xb - SXB * math.pi, 0, Z0), (xb + SXB * math.pi, 0, Z0)], 0.006, F.BOND)
        F.anchor('E', (xb - SXB * math.pi, 0, Z0 + 2.9 * SZ))
        F.anchor('kmin', (xb - SXB * math.pi, 0, Z0 - 2.65 * SZ))
        F.anchor('kmax', (xb + SXB * math.pi, 0, Z0 - 2.65 * SZ))
        F.anchor('gap', (xb + SXB * math.pi + 0.05, 0, Z0))
    F.PREFIX[0] = ''
    F.camera((-0.2, 0.0, 1.25), elev=4.0, ortho=15.6, aspect=3.4)


F.main(build, NAME)
