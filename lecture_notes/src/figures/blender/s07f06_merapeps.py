"""Figure s07f06, fig:s07:merapeps: MERA and PEPS.

Two renders. Left, seen from the front: the MERA over eight sites, two layers, each made of square
disentanglers (teal cubes) on neighboring pairs and triangular isometries (prisms) that join two
sites into one, and a cut (a translucent plane) that crosses one bond in every layer. Right, seen
from above at an angle: the PEPS, a 4 by 4 grid of tensors joined by four virtual bonds each, with
one physical leg down from every tensor.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s07 as G                                                    # noqa: E402

NAME = 's07f06_merapeps'


def build_mera():
    F.studio()
    xs = [-2.17 + 0.62 * i for i in range(8)]
    z0, zd, zi, zd2, zi2 = 0.3, 0.95, 1.75, 2.55, 3.35
    pairs1 = (1, 3, 5)                                   # disentanglers on (1,2), (3,4), (5,6)
    for i, x in enumerate(xs):                          # physical legs and the legs up to layer 1
        inside = i in (1, 2, 3, 4, 5, 6)
        G.leg(f'm_p{i}', (x, z0 - 0.25), (x, (zd - 0.19) if inside else (zi - 0.21)))
        if inside:
            G.leg(f'm_q{i}', (x, zd + 0.19), (x, zi - 0.21))
    for i in pairs1:
        d = G.T(f'm_d1_{i}', (xs[i] + xs[i + 1]) / 2, zd, s=0.38)
        d.scale = (2.4, 1.0, 1.0)
    top = []
    for i in (0, 2, 4, 6):
        xc = (xs[i] + xs[i + 1]) / 2
        G.prism(f'm_i1_{i}', xc, zi, w=0.86, h=0.42, d=0.38)
        top.append(xc)
    for k, x in enumerate(top):                         # layer 2: one disentangler on (1,2), two isometries
        inside = k in (1, 2)
        G.leg(f'm_r{k}', (x, zi + 0.21), (x, (zd2 - 0.19) if inside else (zi2 - 0.21)))
        if inside:
            G.leg(f'm_s{k}', (x, zd2 + 0.19), (x, zi2 - 0.21))
    d = G.T('m_d2', (top[1] + top[2]) / 2, zd2, s=0.38)
    d.scale = (3.6, 1.0, 1.0)
    for k, (a, b) in enumerate(((0, 1), (2, 3))):
        xc = (top[a] + top[b]) / 2
        G.prism(f'm_i2_{k}', xc, zi2, w=1.5, h=0.42, d=0.38)
        G.leg(f'm_top{k}', (xc, zi2 + 0.21), (xc, zi2 + 0.55))
    xcut = (xs[3] + xs[4]) / 2 + 0.07
    F.slab('m_cut', (xcut, 0, 1.95), (0.03, 0.9, 3.7), rgb=F.BROKEN, alpha=0.22).visible_shadow = False
    F.anchor('sites', ((xs[0] + xs[-1]) / 2, 0, 0.0))
    F.anchor('cut', (xcut, 0, 3.85))
    F.anchor('scale0', (xs[-1] + 0.45, 0, 0.5))
    F.anchor('scale1', (xs[-1] + 0.45, 0, 3.4))
    F.anchor('panel', (xs[0] - 0.35, 0, 4.1))
    F.camera((0.1, 0.0, 2.05), elev=6.0, ortho=5.6, aspect=6.4 / 4.6)


def build_peps():
    F.studio()
    n, sp = 4, 0.9
    ox, oy = -(n - 1) * sp / 2, -(n - 1) * sp / 2
    for i in range(n):
        for j in range(n):
            x, y, z = ox + i * sp, oy + j * sp, 0.9
            G.T(f'p_{i}{j}', x, z, s=0.34, y=y)
            G.leg(f'p_phys{i}{j}', (x, y, z - 0.17), (x, y, z - 0.6))
            if i < n - 1:
                G.leg(f'p_h{i}{j}', (x + 0.17, y, z), (x + sp - 0.17, y, z), r=0.035)
            if j < n - 1:
                G.leg(f'p_v{i}{j}', (x, y + 0.17, z), (x, y + sp - 0.17, z), r=0.035)
    F.anchor('panel', (ox - 0.5, oy + n * sp, 1.4))
    F.anchor('phys', (ox + (n - 1) * sp + 0.25, oy - 0.1, 0.3))
    F.camera((0.3, 0.1, 0.6), elev=38.0, azim=-20.0, ortho=6.6, aspect=8.9 / 4.6)


F.main_panels(NAME, [('mera', build_mera), ('peps', build_peps)])
