"""Figure s09f03, fig:s09:ysr: Yu-Shiba-Rusinov states, seen from the front.

(a) The BCS density of states |E| / sqrt(E^2 - Delta^2), Delta = 1, cut at 3, as a slab, with a
ghost copy behind it for a non-magnetic impurity, which leaves it unchanged, and two narrow
Lorentzian peaks at +-E_b in the broken color for a magnetic impurity with alpha = 0.6, E_b from
(9.10). (b) E_b(alpha) = Delta (1 - alpha^2) / (1 + alpha^2) and -E_b, crossing zero at alpha = 1.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's09f03_ysr'
ALPHA = 0.6
EB = (1 - ALPHA ** 2) / (1 + ALPHA ** 2)


def build():
    F.studio()
    xa, sx, sz, z0 = -3.1, 0.92, 0.55, 0.35
    es = [-2.8 + 5.6 * j / 800 for j in range(801)]
    bcs = [min(3.0, abs(e) / math.sqrt(e * e - 1)) if abs(e) > 1.0005 else 0.0 for e in es]
    P = lambda e, g: (xa + sx * e, 0, z0 + sz * g)
    F.profile('a_bcs', [P(e, 0)[0] for e in es], [P(0, g)[2] for g in bcs], 0.12, F.ACCENT_AQM, y0=z0)
    F.profile('a_ghost', [P(e, 0)[0] for e in es], [P(0, g)[2] for g in bcs], 0.12, F.BOND, y0=z0, alpha=0.3).location = (0, 0.35, 0)
    for s in (1, -1):
        ys = [min(3.0, 0.03 / math.pi / ((e - s * EB) ** 2 + 0.03 ** 2) * 0.2) for e in es]
        F.profile(f'a_ysr{s}', [P(e, 0)[0] for e in es], [P(0, g)[2] for g in ys], 0.14, F.BROKEN, y0=z0).location = (0, -0.15, 0)
    F.axis('a_ax', P(-2.9, 0), P(3.1, 0), r=0.016, head=0.13)
    F.axis('a_ay', P(0, 0), P(0, 3.3), r=0.016, head=0.13)
    F.anchor('aE', P(3.1, 0))
    F.anchor('aN', P(0, 3.3))
    F.anchor('aD', P(1, -0.05))
    F.anchor('amD', P(-1, -0.05))
    F.anchor('aEb', P(EB, 1.6))
    F.anchor('apanel', P(-2.9, 3.4))
    xb, ax, ez = 1.6, 1.25, 0.8
    Q = lambda a, e: (xb + ax * a, 0, z0 + 0.9 + ez * e)
    alphas = [2.5 * j / 300 for j in range(301)]
    for s in (1, -1):
        F.tube(f'b_E{s}', [Q(a, s * (1 - a * a) / (1 + a * a)) for a in alphas], 0.035, F.BROKEN)
        F.tube(f'b_gap{s}', [Q(0, s), Q(2.5, s)], 0.008, F.BOND).visible_shadow = False
    F.tube('b_zero', [Q(0, 0), Q(2.5, 0)], 0.008, F.BOND).visible_shadow = False
    F.ball('b_cross', Q(1, 0), 0.07, rgb=F.SITE)
    F.axis('b_ax', Q(0, -1.15), Q(2.75, -1.15), r=0.016, head=0.13)
    F.axis('b_ay', Q(0, -1.15), Q(0, 1.3), r=0.016, head=0.13)
    F.anchor('balpha', Q(2.75, -1.15))
    F.anchor('bE', Q(0, 1.3))
    F.anchor('bone', Q(1, -1.2))
    F.anchor('bD', Q(2.5, 1))
    F.anchor('bmD', Q(2.5, -1))
    F.anchor('bS0', Q(0.22, 0.0))
    F.anchor('bS1', Q(1.62, 0.0))
    F.anchor('bpanel', Q(-0.2, 1.4))
    F.camera((-0.25, 0.0, 1.35), elev=3.0, ortho=11.4, aspect=2.8)


F.main(build, NAME)
