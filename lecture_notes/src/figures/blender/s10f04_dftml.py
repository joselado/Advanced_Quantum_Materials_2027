"""Figure s10f04, fig:s10:dft: where machine learning enters density functional theory.

Seen from the front. The Kohn-Sham loop as four stations on a ring: the density n(r) (a profile),
the effective potential v_eff = v_ext + v_H + v_xc (a curve), the diagonalization (a level ladder)
and the new density; the loop arrows are drawn in the overlay. Route 1: a small network placed on
the v_xc part of the potential station, inside the loop. Route 2: a network outside the loop that
goes straight from the input v_ext (left) to the output n (right), bypassing it.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s10 as N                                                    # noqa: E402

NAME = 's10f04_dftml'


def density(tag, x0, z0, w=1.0, h=0.5):
    xs = [x0 - w / 2 + w * j / 60 for j in range(61)]
    ys = [z0 + h * (math.exp(-((x - x0 + 0.2) / 0.18) ** 2) + 0.7 * math.exp(-((x - x0 - 0.22) / 0.16) ** 2)) for x in xs]
    F.profile(tag, xs, ys, 0.08, F.ACCENT_AQM, y0=z0)


def potential(tag, x0, z0, w=1.0, h=0.5):
    F.tube(tag, [(x0 - w / 2 + w * j / 60, 0, z0 + h * (1 - 0.8 * math.exp(-((j / 60 - 0.3) / 0.12) ** 2)
                                                         - 0.6 * math.exp(-((j / 60 - 0.72) / 0.1) ** 2))) for j in range(61)],
           0.025, F.ACCENT_AQM)


def build():
    F.studio()
    cx, cz, R = 0.0, 2.45, 1.55
    st = {'n': (cx - R, cz), 'v': (cx, cz + R * 0.75), 'diag': (cx + R, cz), 'new': (cx, cz - R * 0.75)}
    density('n_prof', *st['n'])
    potential('v_curve', st['v'][0], st['v'][1] - 0.2)
    for k, e in enumerate((-0.25, -0.1, 0.05, 0.25, 0.42)):
        F.level(f'lad{k}', st['diag'][0], 0, st['diag'][1] + e, length=0.6, r=0.02, rgb=F.SITE if k < 3 else F.BOND)
    density('new_prof', st['new'][0], st['new'][1] - 0.25)
    for k, (x, z) in st.items():
        F.anchor(k, (x, 0, z))
    N.net('r1', st['v'][0] + 0.85, st['v'][1] + 0.05, [3, 3, 1], w=0.5, h=0.4, r=0.045)
    F.anchor('r1', (st['v'][0] + 0.85, 0, st['v'][1] + 0.35))
    # route 2, outside the loop
    potential('vext', -5.2, 2.3)
    density('nout', 5.2, 2.3)
    N.net('r2', 0.0, 0.45, [4, 4, 4, 2], w=1.6, h=0.55, r=0.05)
    F.anchor('vext', (-5.2, 0, 2.0))
    F.anchor('nout', (5.2, 0, 2.0))
    F.anchor('r2', (0.0, 0, 0.05))
    F.anchor('r2in', (-4.6, 0, 1.95))
    F.anchor('r2a', (-0.95, 0, 0.45))
    F.anchor('r2b', (0.95, 0, 0.45))
    F.anchor('r2out', (4.6, 0, 1.95))
    F.anchor('l_in', (-4.5, 0, 2.45))
    F.anchor('l_out', (4.5, 0, 2.45))
    F.camera((0.0, 0.0, 2.05), elev=6.0, ortho=14.4, aspect=2.8)


F.main(build, NAME)
