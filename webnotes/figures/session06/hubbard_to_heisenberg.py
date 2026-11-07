"""Session 6, the low-energy spectrum of an open Hubbard chain of four sites at half filling, against the
Heisenberg chain (6.5) with J = 4t^2/U.

The Hubbard Hamiltonian (6.1) is built with Jordan-Wigner fermions on 8 modes and diagonalized exactly in the
sector with 4 electrons (70 states). The 16 lowest levels are the spin states of the four singly occupied sites.
Their excitation energies E_n - E_0, divided by J = 4t^2/U, are plotted against U/t and approach the excitation
energies of the Heisenberg chain, which are drawn as dashed lines. The next level is a charge excitation at about U.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from functools import reduce
import style

L = 4
M = 2 * L                                   # modes (i, up) = 2i, (i, down) = 2i+1
I2, Z = np.eye(2), np.diag([1., -1.])
a = np.array([[0., 1.], [0., 0.]])          # annihilates the occupied state of one mode


def c(m):                                   # Jordan-Wigner fermion on mode m
    return reduce(np.kron, [Z] * m + [a] + [I2] * (M - m - 1))


cs = [c(m) for m in range(M)]
n = [x.T @ x for x in cs]
Ntot = sum(n)
keep = np.where(abs(np.diag(Ntot) - L) < 1e-9)[0]     # half filling, 4 electrons
assert len(keep) == 70


def hubbard(U, t=1.0):
    H = np.zeros((2**M, 2**M))
    for i in range(L - 1):
        for s in (0, 1):
            h = cs[2 * i + s].T @ cs[2 * (i + 1) + s]
            H -= t * (h + h.T)
    for i in range(L):
        H += U * n[2 * i] @ n[2 * i + 1]
    return H[np.ix_(keep, keep)]


sx = np.array([[0, 1], [1, 0]]) / 2; sy = np.array([[0, -1j], [1j, 0]]) / 2; sz = np.diag([1, -1]) / 2
def site(op, i):
    return reduce(np.kron, [np.eye(2)] * i + [op] + [np.eye(2)] * (L - i - 1))
Hh = sum(site(s, i) @ site(s, i + 1) for i in range(L - 1) for s in (sx, sy, sz)).real   # J = 1
eh = np.linalg.eigvalsh(Hh)
heis = np.unique(np.round(eh - eh[0], 9))

Us = np.linspace(3, 30, 109)
lev = []
for U in Us:
    e = np.linalg.eigvalsh(hubbard(U))
    J = 4 / U
    lev.append((e[:16] - e[0]) / J)
    assert e[16] - e[0] > 0.6 * U                       # the 17th level is a charge excitation, of order U
lev = np.array(lev)
assert np.allclose(np.sort(lev[-1]), np.sort(eh - eh[0]), atol=0.08)   # at U=30t the two spectra agree

FS = 11.5
style.plt.rcParams['font.size'] = FS          # labels of the arrows too, for a phone
fig, ax = style.figure(height_cm=5.8, width_cm=11.5)
for y in heis:
    ax.axhline(y, color=style.BROKEN, lw=1.0, ls=(0, (4, 3)), zorder=1)
for j in range(16):
    ax.plot(Us, lev[:, j], color=style.ACCENT, lw=1.6, zorder=2)
style.arrows(ax, xlabel='$U/t$', ylabel=r'$(E_n-E_0)/J$')
for x in (3, 10, 20, 30):
    style.label(ax, x, -0.12, '$%d$' % x, fontsize=FS - 0.5, va='top')
for y in heis[1:]:
    ax.text(2.6, y, '$%.2f$' % y, ha='right', va='center', fontsize=FS - 1.5, color=style.BROKEN)
style.label(ax, 16.5, heis[-1] + 0.35, r'Heisenberg chain, $J=4t^2/U$', color=style.BROKEN, fontsize=FS)
ax.set_xlim(3, 30); ax.set_ylim(0, heis[-1] + 0.7)
style.save(fig, __file__)
