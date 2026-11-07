"""Session 1, the splitting of the two lowest states of an open Ising chain with a small transverse field.

H = -J sum_i sz_i sz_{i+1} - g sum_i sx_i. For g << J the two lowest states are the even and the odd
combination of all up and all down, and the transverse field lets the chain tunnel between them, so the
splitting Delta falls exponentially with the length L. Exact diagonalization, sparse, L = 2 to 14.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla
import matplotlib.pyplot as plt
import style

J = 1.0
FS = 10.5
sx = sp.csr_matrix([[0., 1.], [1., 0.]])
sz = sp.csr_matrix([[1., 0.], [0., -1.]])


def op(o, i, L):
    return sp.kron(sp.kron(sp.identity(2 ** i), o), sp.identity(2 ** (L - i - 1)), format='csr')


def lowest_two(L, g):
    H = sp.csr_matrix((2 ** L, 2 ** L))
    for i in range(L - 1):
        H = H - J * op(sz, i, L) @ op(sz, i + 1, L)
    for i in range(L):
        H = H - g * op(sx, i, L)
    if L <= 8:
        E, V = np.linalg.eigh(H.toarray())
    else:
        v0 = np.random.default_rng(7).random(2 ** L)               # fixed start vector, so that the SVG is reproducible
        E, V = sla.eigsh(H, k=2, which='SA', tol=1e-13, v0=v0)
        o = np.argsort(E); E, V = E[o], V[:, o]
    P = op(sx, 0, L)
    for i in range(1, L):
        P = P @ op(sx, i, L)                                   # the global spin flip
    parity = V[:, 0] @ (P @ V[:, 0])
    return E[1] - E[0], parity


Ls = np.arange(2, 15)
data = {}
for g in (0.3, 0.5):
    out = [lowest_two(L, g) for L in Ls]
    D = np.array([o[0] for o in out])
    assert all(abs(o[1] - 1) < 1e-8 for o in out)              # the ground state is even under the flip, so symmetric
    assert np.all(np.diff(np.log(D)) < 0)                      # the splitting falls with L
    slope = np.polyfit(Ls[-6:], np.log(D[-6:]), 1)[0]
    assert abs(slope - np.log(g / J)) < 0.15                   # roughly Delta ~ (g/J)^L
    data[g] = D

fig, ax = style.figure(height_cm=6.4, width_cm=12.5)
for g, col in ((0.3, style.ACCENT), (0.5, style.BROKEN)):
    ax.semilogy(Ls, data[g] / J, 'o-', color=col, ms=4.5, lw=1.6)
    style.label(ax, Ls[-1] + 0.3, data[g][-1] / J, r'$g=%.1f\,J$' % g, color=col, ha='left', fontsize=FS)
style.arrows(ax, xlabel=r'$L$', ylabel=r'$\Delta/J$', ticks=True)
ax.set_xticks([2, 6, 10, 14])
ax.set_yticks([1e-6, 1e-4, 1e-2, 1])
ax.tick_params(labelsize=FS, length=2.5)
ax.spines['bottom'].set_visible(True); ax.spines['left'].set_visible(True)
ax.set_xlim(1.5, 17.5)
ax.minorticks_off()
style.save(fig, __file__)
