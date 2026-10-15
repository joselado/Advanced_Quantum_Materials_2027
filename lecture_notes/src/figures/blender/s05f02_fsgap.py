"""Figure s05f02, fig:s05:fsgap: one Fermi surface and three outcomes.

Each column is the square Brillouin zone as a tile with a small Fermi pocket around Gamma, a ring
of radius k_F = 0.35 pi in units of 1/a, and on the ring a tube whose height is the minimum
quasiparticle energy min E = |Delta| there. (a) No pairing: the tube lies on the ring. (b) A constant
Delta0: lifted everywhere by the same amount. (c) d-wave, Delta0 (cos kx - cos ky), which on the
pocket is close to Delta0 (kF^2 / 2) |cos 2 phi|: the tube touches the ring at the four nodes,
where the pocket crosses the zone diagonals, drawn as grooves on the tile. The heights are scaled
so that (b) and the maximum of (c) are the same.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's05f02_fsgap'
XS = (-5.0, 0.0, 5.0)
ZS = 2.0                               # half side of a zone tile
KF = 0.35 * math.pi
H = 0.8                                # height of the full gap


def column(x0, kind, tag):
    F.slab(f'{tag}_bz', (x0, 0, 0.03), (2 * ZS, 2 * ZS, 0.06), rgb=(0.86, 0.87, 0.90))
    s = ZS / math.pi
    ring = [(x0 + s * KF * math.cos(2 * math.pi * j / 200), s * KF * math.sin(2 * math.pi * j / 200), 0.07) for j in range(201)]
    F.tube(f'{tag}_FS', ring, 0.02, F.SITE)
    if kind == 'd':
        for sgn in (1, -1):
            F.tube(f'{tag}_diag{sgn}', [(x0 - ZS, -sgn * ZS, 0.065), (x0 + ZS, sgn * ZS, 0.065)], 0.012, F.BROKEN)
    gaps = []
    for j in range(201):
        p = 2 * math.pi * j / 200
        kx, ky = KF * math.cos(p), KF * math.sin(p)
        d = {'metal': 0.0, 's': 1.0,
             'd': abs(math.cos(kx) - math.cos(ky))}[kind]       # normalized to its maximum below
        gaps.append(d)
    if kind == 'd':
        m = max(gaps)
        gaps = [g / m for g in gaps]
    pts = [(x0 + s * KF * math.cos(2 * math.pi * j / 200), s * KF * math.sin(2 * math.pi * j / 200), 0.09 + H * g)
           for j, g in enumerate(gaps)]
    F.tube(f'{tag}_gap', pts, 0.035, F.ACCENT_AQM)
    if kind != 'metal':
        for j in range(0, 200, 10):
            x, y, z = pts[j]
            if z > 0.12:
                F.rod(f'{tag}_post{j}', (x, y, 0.08), (x, y, z), r=0.008, rgb=F.BOND)
    F.anchor('Gamma', (x0, 0, 0.07))
    F.axes_anchors('k', (x0, 0, 0.07), {'x': (x0 + 0.8 * ZS, 0, 0.07), 'y': (x0, 0.8 * ZS, 0.07)})
    F.anchor('panel', (x0 - ZS, ZS + 0.2, 0.06))
    F.anchor('bz', (x0 + ZS, -ZS, 0.0))
    return gaps


def build():
    F.studio()
    for k, (x, kind) in enumerate(zip(XS, ('metal', 's', 'd'))):
        F.PREFIX[0] = 'abc'[k]
        g = column(x, kind, 'abc'[k])
        print(kind, 'min gap on the pocket', round(min(g), 4))
    F.PREFIX[0] = ''
    F.camera((0.0, 0.25, 0.4), elev=38.0, ortho=15.2, aspect=3.2)


F.main(build, NAME)
