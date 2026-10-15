"""Figure s07f01, fig:s07:jwstring: the Jordan-Wigner string, spin equals fermion times string.

Two chains of eight sites, one behind the other, with a fermion ball on every occupied site and the
spin of each site beside it (up for occupied, down for empty, S^z = n - 1/2). The string K_6 is a
translucent ribbon over sites 1 to 5, to the left of the marked site 6. Behind, three fermions to
the left of site 6; in front, two. The site i = 6 is marked by a ring.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
from mathutils import Vector                                              # noqa: E402

NAME = 's07f01_jwstring'
L, STEP = 8, 1.3
X0 = -(L - 1) * STEP / 2
OCC = {'back': [1, 0, 1, 1, 0, 0, 1, 0], 'front': [1, 0, 0, 1, 0, 0, 1, 1]}
MARK = 6                               # site i = 6, counted from 1


def chain(y, occ, tag):
    for i in range(L):
        x = X0 + i * STEP
        F.site(f'{tag}_s{i}', (x, y, 0), r=0.28)
        if i < L - 1:
            F.bond(f'{tag}_b{i}', (x + 0.28, y, 0.05), (x + STEP - 0.28, y, 0.05))
        if occ[i]:
            F.ball(f'{tag}_e{i}', (x - 0.18, y, 0.3), 0.18)
        F.arrow(f'{tag}_a{i}', (x + 0.22, y, 0.5), (0, 0, 1 if occ[i] else -1), length=0.7)
        F.anchor(f'n{i + 1}', (x, y - 0.45, 0))
    xa, xb = X0 - 0.45, X0 + (MARK - 2) * STEP + 0.45
    F.slab(f'{tag}_string', ((xa + xb) / 2, y, 0.02), (xb - xa, 0.95, 0.02), rgb=F.BROKEN, alpha=0.14)
    ring = F.mat('mark_ring', F.ACCENT_AQM, rough=0.4)
    xm = X0 + (MARK - 1) * STEP
    F.obj(f'{tag}_mark', F.mesh_of(f'{tag}_mark', [ring], lambda bm: F.bm_sweep(
        bm, [(0.42 * math.cos(2 * math.pi * k / 48), 0.42 * math.sin(2 * math.pi * k / 48), 0)
             for k in range(49)], 0.025, end_caps=False)), loc=(xm, y, 0.04))
    F.anchor('string', ((xa + xb) / 2, y + 0.5, 0.02))
    F.anchor('count', (X0 - 0.5, y, 0.02))


def build():
    F.studio()
    F.PREFIX[0] = 'b'
    chain(2.6, OCC['back'], 'back')
    F.PREFIX[0] = 'f'
    chain(0.0, OCC['front'], 'front')
    F.PREFIX[0] = ''
    F.camera((0.0, 1.3, 0.5), elev=28.0, ortho=12.6, aspect=2.8)


F.main(build, NAME)
