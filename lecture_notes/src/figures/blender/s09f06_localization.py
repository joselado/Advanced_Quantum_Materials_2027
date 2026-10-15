"""Figure s09f06, fig:s09:localization: three regimes, three eigenstates, and the IPR.

Two renders. Left: three chains of N = 89 sites at three depths with |psi_i|^2 as columns, each
row scaled to its own maximum (three different vertical scales): (a) behind, a Bloch state of the
periodic ring, |psi_i|^2 = 1/N (the cos^2 standing wave of a degenerate pair is replaced by the
running wave); (b) the eigenstate nearest the band center of the Aubry-Andre-Harper chain at its
self-dual point, V_0 = 2t, q = (sqrt5 - 1)/2; (c) in front, the eigenstate nearest the band center
of a chain with uniform random onsite energies in [-2t, 2t], W = 4t, fixed seed. Right, seen from
the front: (d) log10 IPR against log10 N for N = 34 ... 610, averaged over the six states nearest the
band center (and eight disorder realizations for the random chain).
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's09f06_localization'
NS = (34, 55, 89, 144, 233, 377, 610)
Q = (math.sqrt(5) - 1) / 2


def chain(n, kind, seed=0):
    h = np.diag(-np.ones(n - 1), 1)
    h = h + h.T
    if kind == 'aah':
        h += np.diag(2.0 * np.cos(2 * np.pi * Q * np.arange(n)))
    if kind == 'rand':
        h += np.diag(np.random.default_rng(seed).uniform(-2, 2, n))
    if kind == 'bloch':
        h[0, -1] = h[-1, 0] = -1
    return h


def center_states(n, kind, seed=0, k=1):
    e, v = np.linalg.eigh(chain(n, kind, seed))
    return [v[:, i] for i in np.argsort(np.abs(e))[:k]]


def ipr(n, kind):
    vals = []
    for r in range(8 if kind == 'rand' else 1):
        vals += [np.sum(np.abs(s) ** 4) for s in center_states(n, kind, seed=100 + r, k=6)]
    return float(np.mean(vals))


def build_states():
    F.studio()
    n, sp = 89, 0.105
    rows = (('bloch', 4.0), ('aah', 2.0), ('rand', 0.0))
    for kind, y in rows:
        if kind == 'bloch':
            w = np.full(n, 1.0 / n)
        else:
            w = np.abs(center_states(n, kind, seed=100)[0]) ** 2
        w = w / w.max()
        rgb = {'bloch': F.ACCENT_AQM, 'aah': F.SURFACE, 'rand': F.BROKEN}[kind]
        F.slab(f'{kind}_base', (0, y, 0.01), (n * sp + 0.2, 0.3, 0.02), rgb=(0.86, 0.87, 0.90))
        for i in range(n):
            h = 0.85 * w[i]
            if h > 0.004:
                F.column(f'{kind}_c{i}', (-(n - 1) * sp / 2 + i * sp, y, 0.02), h, r=0.04, rgb=rgb)
        F.anchor(kind, (-(n - 1) * sp / 2 - 0.25, y, 0.3))
        print(kind, 'IPR of the drawn state', round(float(np.sum((w / w.sum()) ** 2)), 4))
    F.camera((0.0, 2.0, 0.6), elev=30.0, ortho=10.4, aspect=10.0 / 4.6)


def build_ipr():
    F.studio()
    sx, sz = 2.6, 1.55
    P = lambda ln, li: (sx * (ln - 1.5) - 1.6, 0, 4.65 + sz * li)   # the log N axis just above the floor
    for kind, rgb in (('bloch', F.ACCENT_AQM), ('aah', F.SURFACE), ('rand', F.BROKEN)):
        pts = [P(math.log10(n), math.log10(ipr(n, kind))) for n in NS]
        F.tube(f'{kind}_line', pts, 0.03, rgb)
        for k, p in enumerate(pts):
            F.ball(f'{kind}_p{k}', p, 0.07, rgb=rgb)
        F.anchor(kind, pts[-1])
        print(kind, [round(ipr(n, kind), 4) for n in NS])
    F.axis('ax', P(1.45, -2.9), P(2.9, -2.9), r=0.016, head=0.13)
    F.axis('ay', P(1.45, -2.9), P(1.45, -0.4), r=0.016, head=0.13)
    F.anchor('lN', P(2.9, -2.9))
    F.anchor('lI', P(1.45, -0.4))
    F.anchor('panel', P(1.3, -0.25))
    F.camera((sx * (2.17 - 1.5) - 1.6, 0, 4.65 + sz * -1.6), elev=3.0, ortho=5.2, aspect=5.4 / 4.6)


F.main_panels(NAME, [('states', build_states), ('ipr', build_ipr)])
