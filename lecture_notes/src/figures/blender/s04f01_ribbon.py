"""Figure s04f01, fig:s04:ribbon: the quantum Hall ribbon, its spectrum and its edges.

Two renders. (a) The spectrum of a strip of width L = 12 l_B along x, infinite along y, from a
finite-difference diagonalization of H = p^2/2 + (x - k_y)^2/2 with hard walls at x = +-L/2, in units
of hbar omega_c and l_B, so the guiding center is x0 = k_y. The four lowest levels are flat in the
bulk and bend up at both walls; the chemical potential mu = 2.0 (a translucent plane) cuts N = 2
of them, and the crossings are balls, dark on the right edge (k_y > 0, v_y > 0) and light on the
left one. (b) The strip seen from above, with the edge modes as arrows, +y on the right edge and
-y on the left, and an impurity on the right edge that the mode goes around.
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's04f01_ribbon'
L, NX = 12.0, 300                      # strip width in l_B and finite-difference points
MU = 2.0
SX, SZ, Z0 = 0.42, 0.62, 0.35          # x per unit of k_y, height per hbar omega_c, height of E = 0


def spectrum(ks, nlev=4):
    xs = np.linspace(-L / 2, L / 2, NX + 2)[1:-1]
    h = xs[1] - xs[0]
    lap = (np.diag(np.full(NX, 2.0)) - np.diag(np.ones(NX - 1), 1) - np.diag(np.ones(NX - 1), -1)) / h ** 2
    return np.array([np.linalg.eigvalsh(0.5 * lap + np.diag(0.5 * (xs - k) ** 2))[:nlev] for k in ks])


def build_a():
    F.studio()
    ks = np.linspace(-L / 2 - 2.5, L / 2 + 2.5, 241)
    E = spectrum(ks)
    P = lambda k, e: (SX * k, 0, Z0 + SZ * e)
    emax = 4.6
    for n in range(4):
        pts = [P(k, e) for k, e in zip(ks, E[:, n]) if e < emax]
        F.tube(f'LL{n}', pts, 0.035, F.ACCENT_AQM)
        F.anchor(f'n{n}', P(0.0, E[len(ks) // 2, n] + 0.08))
    F.slab('mu', (0, 0.2, Z0 + SZ * MU), (2 * SX * (L / 2 + 2.6), 1.4, 0.015), rgb=F.BROKEN, alpha=0.18)
    for n in range(2):
        for side in (1, -1):
            e = E[:, n]
            idx = [i for i in range(len(ks) - 1) if (e[i] - MU) * (e[i + 1] - MU) < 0 and side * ks[i] > 0]
            i = idx[0]
            k = ks[i] + (ks[i + 1] - ks[i]) * (MU - e[i]) / (e[i + 1] - e[i])
            F.ball(f'cross{n}{side}', P(k, MU), 0.09, rgb=F.ACCENT_AQM if side > 0 else F.SURFACE)
    F.axis('ax_k', (-SX * (L / 2 + 2.7), 0, Z0 - 0.15), (SX * (L / 2 + 2.9), 0, Z0 - 0.15), r=0.018, head=0.14)
    F.axis('ax_E', (0, 0, Z0 - 0.15), (0, 0, Z0 + SZ * 4.9), r=0.018, head=0.14)
    for side in (1, -1):
        F.tube(f'wall{side}', [P(side * L / 2, -0.25), P(side * L / 2, 4.7)], 0.008, F.BOND).visible_shadow = False
        F.anchor('wallR' if side > 0 else 'wallL', P(side * L / 2, -0.3))
    F.anchor('k', (SX * (L / 2 + 2.9), 0, Z0 - 0.15))
    F.anchor('E', (0, 0, Z0 + SZ * 4.9))
    F.anchor('mu', P(L / 2 + 2.5, MU))
    F.anchor('panel', P(-L / 2 - 2.9, 4.75))
    print('bulk levels', np.round(E[len(ks) // 2], 4))
    F.camera((0.15, 0.0, Z0 + SZ * 2.3), elev=3.0, ortho=8.3, aspect=9.6 / 5.0)


def build_b():
    F.studio(shadows=False)
    w, h = 2.4, 4.4
    F.slab('strip', (0, 0, 0.02), (w, h, 0.04), rgb=(0.84, 0.86, 0.90), radius=0.03)
    x = w / 2 - 0.22
    pts = []
    for k in range(81):                        # the right edge, +y, going around the impurity at y = 0.4
        y = -h / 2 + 0.25 + (h - 0.5) * k / 80
        pts.append((x - 0.5 * math.exp(-((y - 0.4) / 0.38) ** 2), y, 0.08))
    F.flow('right', pts, r=0.035, rgb=F.ACCENT_AQM)
    F.flow('left', [(-x, h / 2 - 0.25, 0.08), (-x, -h / 2 + 0.25, 0.08)], r=0.035, rgb=F.SURFACE)
    bump = F.mat('impurity', (0.30, 0.31, 0.35), rough=0.5)
    F.obj('imp', F.mesh_of('imp', [bump], lambda bm: F.bm_sphere(bm, F.Vector((0, 0, 0)), 0.2)), loc=(w / 2 - 0.15, 0.4, 0.06))
    F.anchor('imp', (w / 2 + 0.05, 0.4, 0.06))
    F.anchor('right', (w / 2, -h / 2 + 0.6, 0))
    F.anchor('left', (-w / 2, -h / 2 + 0.6, 0))
    F.anchor('panel', (-w / 2 - 1.05, h / 2 + 0.05, 0))
    F.anchor('y', (0, h / 2, 0))
    F.axes_anchors('r', (w / 2 + 0.35, h / 2 - 0.85, 0.0), {'x': (w / 2 + 1.05, h / 2 - 0.85, 0.0), 'y': (w / 2 + 0.35, h / 2 - 0.15, 0.0)})
    F.camera((0.0, 0.0, 0.0), elev=89.9, ortho=5.0, aspect=5.8 / 5.0)


F.main_panels(NAME, [('a', build_a), ('b', build_b)])
