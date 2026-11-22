"""Session 7, the spectrum of an open XX chain of 6 spins computed twice, by exact diagonalization of the spins
and as sums of the single-particle levels of the free fermions that the Jordan-Wigner transformation (7.2) gives.

Redrawn on 2026-11-22 with numbers on the energy axis. The free fermions come from the pyqula script
g1_xx_chain_fermions.py, which the student downloads, and the spins stay in numpy, since pyqula has no solver for a
chain of interacting spins."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

d = style.run_script('session07/g1_xx_chain_fermions.py')
L, J = d['L'], d['J']
eps, ferm = d['eps'], d['levels']
assert L == 6 and J == 1.0
assert np.allclose(np.sort(eps), np.sort(J * np.cos(np.pi * np.arange(1, L + 1) / (L + 1))))   # J cos(pi k/7)
assert abs(d['ground'] + 1.7469796) < 1e-6                                                     # -1.7470 J

sp = np.array([[0, 1], [0, 0.]])          # S^+ in the basis (up, down) = (n=1, n=0)
sm = sp.T
sz = np.diag([0.5, -0.5])
ops = {}
for name, op in (('p', sp), ('m', sm), ('z', sz)):
    for i in range(L):
        out = np.eye(1)
        for j in range(L):
            out = np.kron(out, op if j == i else np.eye(2))
        ops[name, i] = out
# H = J sum_i (S^x_i S^x_{i+1} + S^y_i S^y_{i+1}) = J/2 sum_i (S^+_i S^-_{i+1} + h.c.), open chain
H = sum(0.5 * J * (ops['p', i] @ ops['m', i + 1] + ops['m', i] @ ops['p', i + 1]) for i in range(L - 1))
Sz = sum(ops['z', i] for i in range(L))
szd = np.round(np.diag(Sz), 6)
assert np.allclose(H @ Sz, Sz @ H)
spin = {}
for m in np.unique(szd):
    idx = np.where(szd == m)[0]
    spin[int(round(m + L / 2))] = np.linalg.eigvalsh(H[np.ix_(idx, idx)])      # N = S^z_tot + L/2 fermions
assert sum(len(v) for v in spin.values()) == 64
for N in range(L + 1):
    assert np.allclose(spin[N], ferm[N], atol=1e-10), N                          # the two languages, level by level
assert abs(min(spin[3]) - d['ground']) < 1e-10 and min(min(v) for v in spin.values()) == min(spin[3])
assert -1.8 < min(spin[3]) and max(spin[3]) < 1.8                                 # inside the ticks drawn below

fig, ax = style.figure(height_cm=6.4, width_cm=12.0)
for N in range(L + 1):
    for e in spin[N]:
        ax.plot([N - 0.32, N + 0.32], [e, e], color=style.ACCENT, lw=1.3, zorder=2)
    ax.plot(np.full(len(ferm[N]), N), ferm[N], 'o', ms=3.4, color=style.BROKEN, zorder=3)
style.guide(ax, y=0)
ax.set_xlim(-0.7, L + 0.7); ax.set_ylim(-2.0, 3.0)
style.arrows(ax, xlabel=r'$N$', ylabel=r'$E$ in units of $J$', ticks=True)
ax.set_xticks(range(L + 1))
ax.set_yticks([-1, 0, 1])
ax.tick_params(axis='both', length=2.5, pad=2, labelsize=11)
ax.plot([0.35, 0.95], [2.75, 2.75], color=style.ACCENT, lw=1.3)
style.label(ax, 1.1, 2.75, 'spins, exact diagonalization', ha='left', fontsize=11, color=style.ACCENT)
ax.plot([0.65], [2.3], 'o', ms=3.4, color=style.BROKEN)
style.label(ax, 1.1, 2.3, 'free fermions, sums of levels', ha='left', fontsize=11, color=style.BROKEN)
style.save(fig, __file__)
