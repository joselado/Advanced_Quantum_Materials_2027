"""Figure s06f04, fig:s06:kitaev: the Kitaev interaction, frustration in the coupling.

A honeycomb patch, sublattices as dark and light discs, with the three bond directions in three rod
styles: x bonds thin and grey, y bonds medium and accent, z bonds thick and dark. On one highlighted
site, three ghost arrows along x, y and z in spin space, the three directions that its three bonds
ask for, which no single orientation can satisfy at once.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's06f04_kitaev'
B = 0.75                               # bond length
LIGHT = (0.62, 0.64, 0.70)
STYLE = {'z': (0.06, (0.20, 0.21, 0.25)), 'x': (0.025, F.BOND), 'y': (0.042, F.ACCENT_AQM)}


def bond_type(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    if abs(dx) < 1e-6:
        return 'z'
    return 'x' if dx * dy < 0 else 'y'


def build():
    F.studio()
    A, Bs, bonds = F.honeycomb(lambda x, y: x * x / 9.0 + (y - 0.3) ** 2 / 4.0 < 1.0, bond=B)
    for k, (a, b) in enumerate(bonds):
        r, rgb = STYLE[bond_type(a, b)]
        F.rod(f'b{k}', (a[0], a[1], 0.05), (b[0], b[1], 0.05), r=r, rgb=rgb)
    light = F.mat('site_light', LIGHT, rough=0.5, spec=0.3)
    for k, (x, y) in enumerate(A):
        F.site(f'A{k}', (x, y, 0), r=0.17, h=0.06)
    for k, (x, y) in enumerate(Bs):
        F.obj(f'B{k}', F.mesh_of(f'B{k}', [light], lambda bm: F.bm_cylinder(bm, (0, 0, 0), (0, 0, 0.06), 0.13, seg=40)),
              loc=(x, y, 0))
    c = min(A, key=lambda p: math.hypot(p[0], p[1] - 0.3))
    F.ball('focus', (c[0], c[1], 0.1), 0.2, rgb=F.BROKEN)
    for k, d in enumerate(((1, 0, 0), (0, 1, 0), (0, 0, 1))):
        F.ghost_arrow(f'g{k}', (c[0] + 0.35 * d[0], c[1] + 0.35 * d[1], 0.25 + 0.35 * d[2]), d, length=0.75, alpha=0.4)
        F.anchor('xyz'[k], (c[0] + 0.85 * d[0], c[1] + 0.85 * d[1], 0.25 + 0.85 * d[2]))
    for t, near in (('x', (-2.0, 1.2)), ('y', (-1.6, -0.9)), ('z', (2.3, -0.2))):
        a, b = min(((a, b) for a, b in bonds if bond_type(a, b) == t), key=lambda ab: math.dist(ab[0], near))
        F.anchor('bond' + t, ((a[0] + b[0]) / 2 + 0.12, (a[1] + b[1]) / 2, 0.08))
    F.camera((0.0, 0.3, 0.4), elev=40.0, azim=-35.0, ortho=6.6, aspect=1.8)


F.main(build, NAME)
