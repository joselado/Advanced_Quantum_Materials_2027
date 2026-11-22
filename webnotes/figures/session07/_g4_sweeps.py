"""Session 7, section 7.10, the shared code of the three pictures of the quiz on the energy of a DMRG sweep.

The sweep is the one of dmrg_sweeps.py for M = 4 and seed 1, repeated here since that script draws its own figure: an
open Heisenberg chain J sum S_i.S_{i+1} of 10 sites with J = 1, from a random MPS, three sweeps of 18 one-site updates,
each the exact minimum of the energy over one tensor. The assert below ties it to the M = 4 curve of dmrg_sweeps.py,
which ends 6.12e-3 above E0. Each picture is E/J against the update on a linear axis, with the same axes, the same ticks
and a dashed line at E0, and no other text, since the pictures are the options of a quiz. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

L = 10
sx = np.array([[0, 1], [1, 0]]) / 2; sy = np.array([[0, -1j], [1j, 0]]) / 2; sz = np.diag([.5, -.5])


def op(o, i):
    m = np.eye(1)
    for j in range(L):
        m = np.kron(m, o if j == i else np.eye(2))
    return m


H = sum(op(s, i) @ op(s, i + 1) for i in range(L - 1) for s in (sx, sy, sz)).real
E0 = np.linalg.eigvalsh(H)[0]


def sweep(M=4, nsweeps=3, seed=1):
    """The energy after every one-site update, the same steps as run() of dmrg_sweeps.py."""
    rng = np.random.default_rng(seed)
    D = [1] + [min(M, 2 ** min(k, L - k)) for k in range(1, L)] + [1]
    A = [rng.normal(size=(D[k], 2, D[k + 1])) for k in range(L)]

    def contract(lo, hi):
        T = np.eye(D[lo]).reshape(1, D[lo], D[lo])
        for k in range(lo, hi):
            T = np.einsum('pab,bsc->psac', T, A[k]).reshape(-1, D[lo], D[k + 1])
        return T
    energies = []
    for _ in range(nsweeps):
        for k in list(range(L)) + list(range(L - 2, 0, -1)):
            Lf = contract(0, k)[:, 0, :]
            Rt = contract(k + 1, L)[:, :, 0].reshape(-1, D[k + 1])
            N = np.einsum('ia,st,jb->isjatb', Lf, np.eye(2), Rt).reshape(2 ** L, -1)
            U, sv, Vt = np.linalg.svd(N, full_matrices=False)
            keep = sv > 1e-9 * sv[0]
            U, sv, Vt = U[:, keep], sv[keep], Vt[keep]
            w, u = np.linalg.eigh(U.T @ H @ U)
            psi = U @ u[:, 0]
            A[k] = ((Vt.T / sv) @ (U.T @ psi)).reshape(D[k], 2, D[k + 1])
            energies.append(psi @ H @ psi / (psi @ psi))
    return np.array(energies)


E = sweep()
assert len(E) == 54 and np.all(np.diff(E) < 1e-9) and abs(E[-1] - E0 - 6.118e-3) < 1e-5, (len(E), E[-1] - E0)
K_UP, UP = 24, 1.5          # the update where the wrong option goes up, and by how much, in units of J
SHIFT = 0.5                 # the wrong option shifted down by this, in units of J


def option(script, e):
    """One picture option, E/J against the update, with a dashed line at E0, its axes and no other text."""
    plt.rcParams.update({'savefig.dpi': 220})
    fig, ax = plt.subplots(figsize=(3.6 * style.CM, 3.2 * style.CM))
    n = np.arange(1, len(e) + 1)
    ax.axhline(E0, color=style.MUTED, lw=0.9, ls=(0, (3, 2)), zorder=1)
    ax.plot(n, e, color=style.ACCENT, lw=1.2, marker='o', ms=1.6, zorder=2)
    ax.set_xlim(0, 56); ax.set_ylim(-5.2, 0.4)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    ax.set_xticks([1, 18, 36, 54]); ax.set_xticklabels(['1', '18', '36', '54'], fontsize=10)
    ax.set_yticks([E0, -2, 0]); ax.set_yticklabels([r'$E_0$', r'$-2$', r'$0$'], fontsize=10)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel('update', fontsize=11, labelpad=0); ax.set_ylabel(r'$E/J$', fontsize=11, labelpad=1)
    style.save(fig, script)
