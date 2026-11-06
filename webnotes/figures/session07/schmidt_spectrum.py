"""Session 7, the Schmidt weights at the central bond of the ground state of an open Heisenberg chain, by exact diagonalization."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla
import style

L = 16
sx = sp.csr_matrix([[0, 1], [1, 0]]) / 2; sy = sp.csr_matrix([[0, -1j], [1j, 0]]) / 2; sz = sp.csr_matrix([[.5, 0], [0, -.5]])
def op(o, i):
    return sp.kron(sp.kron(sp.identity(2 ** i), o), sp.identity(2 ** (L - i - 1)), format='csr')
ops = {i: (op(sx, i), op(sy, i), op(sz, i)) for i in range(L)}
def bond(i, j):
    return sum(ops[i][a] @ ops[j][a] for a in range(3))
def weights(Jodd):
    """Bonds (0,1), (2,3), ... have J=1 and the bonds (1,2), (3,4), ... have Jodd."""
    H = sum((1.0 if i % 2 == 0 else Jodd) * bond(i, i + 1) for i in range(L - 1))
    e, v = sla.eigsh(H, k=1, which='SA')
    psi = v[:, 0].reshape(2 ** (L // 2), 2 ** (L // 2))
    s = np.linalg.svd(psi, compute_uv=False) ** 2
    return e[0], s

E1, w1 = weights(1.0)
E2, w2 = weights(0.5)
for w in (w1, w2):
    assert abs(w.sum() - 1) < 1e-9
M = 16

fig, ax = style.figure(height_cm=5.6)
n = 34
a = np.arange(1, n + 1)
ax.semilogy(a, np.maximum(w1[:n], 1e-16), color=style.BROKEN, marker='o', ms=2.6, lw=1.2)
ax.semilogy(a, np.maximum(w2[:n], 1e-16), color=style.ACCENT, marker='o', ms=2.6, lw=1.2)
ax.axvline(M + 0.5, color=style.MUTED, lw=1.0, ls=(0, (3, 3)))
ax.set_xlim(0, n + 1); ax.set_ylim(1e-11, 3)
style.label(ax, M + 1.0, 3e-10, r'$M=16$', fontsize=8.5, ha='left', color=style.MUTED)
style.label(ax, 18.2, 0.3, 'uniform chain, $J_2=J_1$', color=style.BROKEN, fontsize=8.5, ha='left')
style.label(ax, 18.2, 0.02, 'dimerized chain, $J_2=0.5J_1$', color=style.ACCENT, fontsize=8.5, ha='left')
style.arrows(ax, xlabel=r'$\alpha$', ylabel=r'$\lambda_\alpha^2$')
ax.set_xticks([1, 8, 16, 24, 32]); ax.tick_params(axis='x', length=2.5, pad=2)
ax.set_yticks([1e-10, 1e-5, 1]); ax.tick_params(axis='y', length=2.5, pad=2); ax.minorticks_off()
style.arrows(ax, xlabel=r'$\alpha$', ylabel=r'$\lambda_\alpha^2$', ticks=True)
style.save(fig, __file__)
