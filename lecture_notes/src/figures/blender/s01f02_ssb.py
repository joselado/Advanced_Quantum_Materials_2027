"""Figure s01f02, fig:s01:ssb: a symmetric energy landscape with minima that are not symmetric.

E(m) = h (m^2 - 1)^2 drawn twice, for a small system with a low barrier h and for a large one
with a barrier four times higher, since the barrier grows with the size. The system sits at
+m0 (the ball) and the equivalent minimum at -m0 is the ghost ball.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's01f02_ssb'
XA, XB = -2.9, 2.9
SX, Z0, EMAX = 1.05, 0.35, 2.3        # x per unit of m, height of E = 0, top of the drawn curve
R = 0.17


def well(x0, h, tag):
    pts = []
    for k in range(241):
        m = -1.75 + 3.5 * k / 240
        e = h * (m * m - 1) ** 2
        if e <= EMAX:
            pts.append((x0 + SX * m, 0, Z0 + e))
    F.tube(f'{tag}_E', pts, 0.035, F.ACCENT_AQM)
    F.axis(f'{tag}_m', (x0 - 2.1, 0, 0.12), (x0 + 2.25, 0, 0.12), r=0.02, head=0.15)
    F.axis(f'{tag}_e', (x0 - 2.1, 0, 0.12), (x0 - 2.1, 0, EMAX + 0.55), r=0.02, head=0.15)
    F.ball(f'{tag}_ball', (x0 + SX, 0, Z0 + R), R)
    F.marker(f'{tag}_ghost', (x0 - SX, 0, Z0 + R), kind='ghost', r=R)
    F.anchor('m', (x0 + 2.25, 0, 0.12))
    F.anchor('E', (x0 - 2.1, 0, EMAX + 0.55))
    F.anchor('plus', (x0 + SX, 0, 0.1))
    F.anchor('minus', (x0 - SX, 0, 0.1))
    F.anchor('title', (x0 + 0.1, 0, EMAX + 0.45))


def build():
    F.studio()
    F.PREFIX[0] = 'a'
    well(XA, 0.45, 'a')
    F.PREFIX[0] = 'b'
    well(XB, 1.8, 'b')
    F.PREFIX[0] = ''
    F.camera((0.0, 0.0, 1.25), elev=12.0, ortho=12.4, aspect=2.0)


F.main(build, NAME)
