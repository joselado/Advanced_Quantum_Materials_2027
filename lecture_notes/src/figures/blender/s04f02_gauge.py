"""Figure s04f02, fig:s04:gauge: the Peierls phases of one field in two gauges, seen from above.

Two square patches of three by three plaquettes, with the phase of every bond as a dial, a needle
at the angle of the phase (pointing along +x for zero), for the bond traversed along +x or +y, with
phi = B a^2 = pi/4 per plaquette. (a) Landau gauge A = (0, Bx): horizontal bonds 0, the vertical
bond in column x has x phi. (b) Symmetric gauge A = (B/2)(-y, x): vertical x phi/2, horizontal in row
y has -y phi/2, with x and y measured from the center of the patch so that the pattern is
symmetric about it. The middle plaquette is highlighted in both, and its counterclockwise sum is phi
in both.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's04f02_gauge'
PHI = math.pi / 4
A0, S = 1.25, 1.25                     # bond length in the scene
XA, XB = -3.1, 3.1                     # centers of the two patches


def dial(name, loc, phase):
    disc = F.mat('dial', (0.74, 0.76, 0.80), rough=0.6, spec=0.2)
    F.obj(name, F.mesh_of(name, [disc], lambda bm: F.bm_cylinder(bm, (0, 0, 0), (0, 0, 0.03), 0.27, seg=40)), loc=loc)
    rim = F.mat('dial_rim', (0.30, 0.31, 0.35), rough=0.5)
    F.obj(name + '_rim', F.mesh_of(name + '_rim', [rim], lambda bm: F.bm_cylinder(
        bm, (0, 0, 0), (0, 0, 0.034), 0.275, seg=40, caps=False)), loc=loc)
    x, y, z = loc
    F.vector_arrow(name + '_needle', (x, y, z + 0.05), (x + 0.24 * math.cos(phase), y + 0.24 * math.sin(phase), z + 0.05),
                   r=0.022, head=0.09)


def patch(x0, gauge, tag):
    n = 4                                               # sites per side
    c = (n - 1) / 2
    pos = lambda i, j: (x0 + S * (i - c), S * (j - c))
    for i in range(n):
        for j in range(n):
            F.site(f'{tag}_s{i}{j}', (*pos(i, j), 0), r=0.12, h=0.04)
    for i in range(n):
        for j in range(n):
            xx, yy = i - c, j - c                       # coordinates measured from the center
            if i < n - 1:                               # horizontal bond (i, j) -> (i + 1, j)
                ph = 0.0 if gauge == 'landau' else -yy * PHI / 2
                (x1, y1), (x2, y2) = pos(i, j), pos(i + 1, j)
                F.bond(f'{tag}_h{i}{j}', (x1 + 0.12, y1, 0.03), (x2 - 0.12, y2, 0.03), r=0.02)
                dial(f'{tag}_dh{i}{j}', ((x1 + x2) / 2, y1, 0.04), ph)
            if j < n - 1:                               # vertical bond (i, j) -> (i, j + 1)
                ph = (i * PHI) if gauge == 'landau' else xx * PHI / 2
                (x1, y1), (x2, y2) = pos(i, j), pos(i, j + 1)
                F.bond(f'{tag}_v{i}{j}', (x1, y1 + 0.12, 0.03), (x2, y2 - 0.12, 0.03), r=0.02)
                dial(f'{tag}_dv{i}{j}', (x1, (y1 + y2) / 2, 0.04), ph)
    F.slab(f'{tag}_plaq', (x0, 0, 0.005), (S - 0.2, S - 0.2, 0.01), rgb=F.ACCENT_AQM, alpha=0.22)
    F.anchor('panel', (x0 - S * c - 0.35, S * c + 0.45, 0))
    F.anchor('plaq', (x0, 0, 0.02))
    F.axes_anchors('r', (x0 + S * c + 0.45, -S * c, 0.0), {'x': (x0 + S * c + 1.1, -S * c, 0.0), 'y': (x0 + S * c + 0.45, -S * c + 0.65, 0.0)})


def build():
    F.studio(shadows=False)
    F.PREFIX[0] = 'a'
    patch(XA, 'landau', 'a')
    F.PREFIX[0] = 'b'
    patch(XB, 'symmetric', 'b')
    F.PREFIX[0] = ''
    F.camera((0.0, 0.25, 0.0), elev=89.9, ortho=12.8, aspect=12.5 / 5.6)


F.main(build, NAME)
