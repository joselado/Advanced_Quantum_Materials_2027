"""Session 7, the entanglement entropy of the left block of a chain of 14 spins, for a random state of the full
Hilbert space and for the gapped ground state of a dimerized Heisenberg chain, computed with exact diagonalization."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spl
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

L = 14
J1, J2 = 1.0, 0.5           # strong bonds (0,1), (2,3), ... and weak bonds (1,2), (3,4), ...

def heisenberg(L, J):
    s = np.arange(2 ** L, dtype=np.int64)
    diag = np.zeros(2 ** L)
    rows, cols, vals = [], [], []
    for i, Jb in enumerate(J):
        a = (s >> i) & 1
        b = (s >> (i + 1)) & 1
        diag += Jb * np.where(a == b, 0.25, -0.25)
        flip = np.where(a != b)[0]
        rows.append(flip); cols.append(flip ^ (3 << i)); vals.append(np.full(len(flip), 0.5 * Jb))
    rows.append(s); cols.append(s); vals.append(diag)
    return sps.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(2 ** L, 2 ** L))

def entropy(psi, l):
    """S of the block made of the first l sites. Site i is bit i, so the first l sites are the fast index."""
    p = np.linalg.svd(psi.reshape(2 ** (L - l), 2 ** l), compute_uv=False) ** 2
    p = p[p > 1e-14]
    return -np.sum(p * np.log(p))

J = [J1 if i % 2 == 0 else J2 for i in range(L - 1)]
H = heisenberg(L, J)
e, v = spl.eigsh(H, k=1, which='SA', tol=1e-10, v0=np.ones(2 ** L))
gs = v[:, 0]
rng = np.random.default_rng(7)
rnd = rng.normal(size=2 ** L) + 1j * rng.normal(size=2 ** L)
rnd /= np.linalg.norm(rnd)

ls = np.arange(1, L)
S_gs = np.array([entropy(gs, l) for l in ls])
S_rnd = np.array([entropy(rnd, l) for l in ls])
S_max = np.minimum(ls, L - ls) * np.log(2)
assert np.all(S_rnd > S_max - 0.75)                      # a random state sits just below the maximum, a volume law
assert np.all(S_gs < 1.05 * np.log(2)) and S_gs[0] > 0.9 * np.log(2)   # a cut strong bond gives about log 2

fig, ax = style.figure(height_cm=6.4, width_cm=12.0)
ax.plot(ls, S_max / np.log(2), color=style.GRID, lw=1.2, ls=(0, (3, 3)), zorder=0)
ax.plot(ls, S_rnd / np.log(2), 'o-', ms=4, lw=1.4, color=style.BROKEN)
ax.plot(ls, S_gs / np.log(2), 'o-', ms=4, lw=1.4, color=style.ACCENT)
ax.set_xlim(0, L); ax.set_ylim(0, 8.0)
style.arrows(ax, xlabel=r'$|A|$', ylabel=r'$S_A/\log 2$')
ax.set_xticks([1, 7, 13]); ax.set_yticks([1, 7])
ax.tick_params(length=2.5, pad=2, labelsize=11)
style.label(ax, 7, 7.55, r'maximum, $\min(|A|,L-|A|)$', fontsize=11, color=style.MUTED)
style.label(ax, 9.9, 4.9, 'random state', ha='left', fontsize=11, color=style.BROKEN)
style.label(ax, 7, 1.75, 'gapped ground state', fontsize=11, color=style.ACCENT)
style.save(fig, __file__)
