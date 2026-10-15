"""Figure s04f04, fig:s04:ladders: the Landau fans, linear against square root.

Seen from the front, a little from the side so that the cut reads as a plane. (a) Schroedinger
electrons, E_n = (n + 1/2) hbar omega_c = (n + 1/2) B in units hbar e / m = 1, n = 0..5, straight lines
through the origin. (b) Dirac electrons, E_n = sgn(n) sqrt(2 |n| B) in units v_F = hbar = e = 1,
n = 0, +-1, +-2, +-3, square-root curves, with the flat n = 0 line in the accent color. In both, a
translucent plane at B0 = 0.75 cuts the fan, and the short rods where it cuts are the ladder of
levels at that field. The two vertical scales are independent.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's04f04_ladders'
XA, XB = -3.9, 3.0                     # left ends of the two B axes
WB = 4.0                               # length of the B axis in the scene
B0 = 0.75
FAN = (0.42, 0.43, 0.48)


def fan(x0, z0, sz, curves, tag, zc, hz):
    bs = [j / 100 for j in range(101)]
    for n, f, rgb in curves:
        F.tube(f'{tag}_n{n}', [(x0 + WB * b, 0, z0 + sz * f(b)) for b in bs], 0.028, rgb)
        F.level(f'{tag}_rung{n}', x0 + WB * B0, 0, z0 + sz * f(B0), length=0.5, r=0.035, rgb=F.BROKEN if (n == 0 and tag == 'b') else F.SITE)
    F.slab(f'{tag}_cut', (x0 + WB * B0, 0, zc), (0.02, 0.9, hz), rgb=F.ACCENT_AQM, alpha=0.15).visible_shadow = False
    F.anchor(f'{tag}B0', (x0 + WB * B0, 0, zc - hz / 2))


def build():
    F.studio()
    # (a) Schroedinger: straight lines through the origin
    za, sza = 0.35, 0.68
    curves = [(n, (lambda b, n=n: (n + 0.5) * b), FAN) for n in range(6)]
    fan(XA, za, sza, curves, 'a', za + 2.0, 4.0)
    F.axis('a_B', (XA, 0, za), (XA + WB + 0.4, 0, za), r=0.018, head=0.14)
    F.axis('a_E', (XA, 0, za), (XA, 0, za + 4.2), r=0.018, head=0.14)
    F.anchor('aB', (XA + WB + 0.4, 0, za))
    F.anchor('aE', (XA, 0, za + 4.2))
    F.anchor('apanel', (XA - 0.3, 0, za + 4.45))
    F.anchor('an5', (XA + WB, 0, za + sza * 5.5))
    F.anchor('an0', (XA + WB, 0, za + sza * 0.5))
    # (b) Dirac: square roots, with the n = 0 line flat at zero
    zb, szb = 2.35, 0.85
    curves = [(n, (lambda b, n=n: math.copysign(math.sqrt(2 * abs(n) * b), n) if n else 0.0),
               F.ACCENT_AQM if n == 0 else FAN) for n in range(-3, 4)]
    fan(XB, zb, szb, curves, 'b', zb, 4.4)
    F.axis('b_B', (XB, 0, zb), (XB + WB + 0.4, 0, zb), r=0.018, head=0.14)
    F.axis('b_E', (XB, 0, zb - 2.2), (XB, 0, zb + 2.2), r=0.018, head=0.14)
    F.anchor('bB', (XB + WB + 0.4, 0, zb))
    F.anchor('bE', (XB, 0, zb + 2.2))
    F.anchor('bpanel', (XB - 0.3, 0, za + 4.45))
    F.anchor('bn0', (XB + WB, 0, zb))
    F.anchor('bn3', (XB + WB, 0, zb + szb * math.sqrt(6)))
    F.camera((0.0, 0.0, 2.45), elev=10.0, azim=-18.0, ortho=15.4, aspect=2.9)


F.main(build, NAME)
