"""Figure s01f04, fig:s01:cdw: the charge density wave of the spinless chain (1.6).

Both rows are the Hartree mean-field solution of a periodic chain of eight sites at half filling,
computed below, with the cups filled to <n_i> and the spectrum next to each chain, the four
occupied levels carrying an electron and degenerate levels side by side.
In front, V = 0: every cup half full, unit cell a, and the Fermi level inside a degenerate pair
of levels at E = 0, so the spectrum is gapless.
Behind, V = 3t: <n_i> = 0.95, 0.05, ..., the unit cell is doubled, and a gap of 5.4t opens.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's01f04_cdw'
L, STEP = 8, 0.95
X0 = -6.3                              # x of the first site
XL = 3.6                               # x of the level ladders
Y_BACK = 5.4
Z0, ES = 1.1, 0.25                     # height of E = 0 and height per unit of t
H = 0.9                                # height of a full cup


def mean_field(V, iters=400):
    n = np.array([0.6, 0.4] * (L // 2))
    for _ in range(iters):
        h = np.zeros((L, L))
        for i in range(L):
            h[i, (i + 1) % L] = h[(i + 1) % L, i] = -1.0
            h[i, i] = V * (n[i - 1] + n[(i + 1) % L])
        e, v = np.linalg.eigh(h)
        ef = e[L // 2 - 1]                         # a degenerate level at the Fermi level is shared
        deg = np.abs(e - ef) < 1e-8
        occ = (e < ef - 1e-8) + deg * (L // 2 - np.sum(e < ef - 1e-8)) / deg.sum()
        n = 0.5 * n + 0.5 * (v ** 2 @ occ)
    return n, e - e.mean()


def row(y, tag, V, cell):
    n, e = mean_field(V)
    xs = [X0 + i * STEP for i in range(L)]
    for i, x in enumerate(xs):
        F.cup(f'{tag}_cup{i}', (x, y, 0.0), float(n[i]), r=0.3, h=H)
        if i < L - 1:
            F.bond(f'{tag}_b{i}', (x + 0.3, y, 0.03), (xs[i + 1] - 0.3, y, 0.03))
    xc = xs[-1] - (cell - 1) * STEP / 2          # the unit cell at the right end of the chain
    F.slab(f'{tag}_cell', (xc, y, 0.0), (cell * STEP - 0.1, 0.95, 0.02), rgb=F.ACCENT_AQM, alpha=0.18)
    F.anchor('cell', (xs[-1] + 0.45, y, 0.0))
    F.axis(f'{tag}_axis', (XL - 0.75, y, 0.02), (XL - 0.75, y, Z0 + 3.9 * ES), r=0.02, head=0.15)
    F.ladder(tag, XL, y, Z0, e, ES, length=0.8, r=0.026, filled=L // 2)
    F.anchor('E', (XL - 0.75, y, Z0 + 3.9 * ES + 0.05))
    F.anchor('spec', (XL + 0.5, y, Z0))
    F.anchor('panel', (X0 - 0.45, y, 1.35))
    print(tag, 'n =', np.round(n, 3), 'levels =', np.round(e, 3))


def build():
    F.studio()
    F.PREFIX[0] = 'a'
    row(0.0, 'a', 0.0, 1)
    F.PREFIX[0] = 'b'
    row(Y_BACK, 'b', 3.0, 2)
    F.PREFIX[0] = ''
    F.camera((-0.9, Y_BACK / 2, 1.0), elev=28.0, ortho=13.4, aspect=2.6)


F.main(build, NAME)
