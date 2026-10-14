"""Figure s01f05, fig:s01:mfloop: the mean-field self-consistency loop, one pass of it computed.

Four stations in a row, each a periodic chain of four sites at half filling with V = 3t, as in
the charge density wave of (1.6). 1, the guessed charges <n_i> = 0.6, 0.4, 0.6, 0.4 as columns.
2, the mean-field Hamiltonian, whose onsite energies V(n_{i-1} + n_{i+1}) = 2.4t, 3.6t raise and
lower the sites. 3, its four levels, the lowest two filled. 4, the new charges 0.82, 0.18, which
are not the guess, so the loop goes round again. The arrows of the loop are set in the overlay.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's01f05_selfconsistency'
XS = (-6.0, -2.55, 0.9, 4.35)          # the four stations
STEP, N, V = 0.55, 4, 3.0
HC = 1.1                               # height of a column of charge 1


def hamiltonian(n):
    h = np.zeros((N, N))
    for i in range(N):
        h[i, (i + 1) % N] = h[(i + 1) % N, i] = -1.0
        h[i, i] = V * (n[i - 1] + n[(i + 1) % N])
    return h


def sites(x0, tag, z=None):
    xs = [x0 + (i - 1.5) * STEP for i in range(N)]
    for i, x in enumerate(xs):
        F.site(f'{tag}_s{i}', (x, 0, 0 if z is None else z[i]), r=0.19, h=0.05)
        if z is None and i < N - 1:
            F.bond(f'{tag}_b{i}', (x + 0.19, 0, 0.03), (xs[i + 1] - 0.19, 0, 0.03), r=0.025)
    return xs


def build():
    F.studio()
    guess = np.array([0.6, 0.4, 0.6, 0.4])
    h = hamiltonian(guess)
    e, v = np.linalg.eigh(h)
    new = (v[:, :N // 2] ** 2).sum(1)
    print('onsite', np.diag(h), 'levels', np.round(e, 3), 'new', np.round(new, 3))
    # 1, the guess
    xs = sites(XS[0], 's1')
    for i, x in enumerate(xs):
        F.column(f's1_c{i}', (x, 0, 0.05), HC * guess[i], r=0.15)
    # 2, the mean-field Hamiltonian as sites raised by their onsite energy
    eps = np.diag(h)
    z = [0.35 + 0.5 * (eps[i] - eps.min()) for i in range(N)]
    xs = sites(XS[1], 's2', z=z)
    for i, x in enumerate(xs):
        F.rod(f's2_post{i}', (x, 0, 0), (x, 0, z[i]), r=0.02)
    # 3, its levels, the lowest two filled
    F.axis('s3_axis', (XS[2] - 0.75, 0, 0.02), (XS[2] - 0.75, 0, 1.75), r=0.02, head=0.15)
    F.ladder('s3', XS[2], 0, 0.15, e, 0.28, length=0.9, r=0.03, filled=N // 2)
    # 4, the new charges
    xs = sites(XS[3], 's4')
    for i, x in enumerate(xs):
        F.column(f's4_c{i}', (x, 0, 0.05), HC * new[i], r=0.15)
    for k, x in enumerate(XS):
        F.anchor(f'st{k + 1}', (x, 0, 1.95))
        F.anchor(f'in{k + 1}', (x - 1.3, 0, 0.6))
        F.anchor(f'out{k + 1}', (x + 1.3, 0, 0.6))
        F.anchor(f'low{k + 1}', (x, -0.5, 0))
    F.camera((-0.2, 0.0, 1.0), elev=18.0, ortho=15.6, aspect=3.0)


F.main(build, NAME)
