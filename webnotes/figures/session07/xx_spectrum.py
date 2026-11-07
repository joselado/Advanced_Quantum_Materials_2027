"""Session 7, the spectrum of an open XX chain of 6 spins computed twice, by exact diagonalization of the spins
and as sums of the single-particle levels of the free fermions that the Jordan-Wigner transformation (7.2) gives."""
import os, sys, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

L, J = 6, 1.0
sp = np.array([[0, 1], [0, 0.]])          # S^+ in the basis (up, down) = (n=1, n=0)
sm = sp.T
sz = np.diag([0.5, -0.5])
def site(op, i):
    out = np.eye(1)
    for j in range(L):
        out = np.kron(out, op if j == i else np.eye(2))
    return out
# H = J sum_i (S^x_i S^x_{i+1} + S^y_i S^y_{i+1}) = J/2 sum_i (S^+_i S^-_{i+1} + h.c.), open chain
H = sum(0.5 * J * (site(sp, i) @ site(sm, i + 1) + site(sm, i) @ site(sp, i + 1)) for i in range(L - 1))
Sz = sum(site(sz, i) for i in range(L))
szd = np.round(np.diag(Sz), 6)
assert np.allclose(H @ Sz, Sz @ H)
spin = {}
for m in np.unique(szd):
    idx = np.where(szd == m)[0]
    spin[int(round(m + L / 2))] = np.linalg.eigvalsh(H[np.ix_(idx, idx)])      # N = S^z_tot + L/2 fermions

# Jordan-Wigner: S^+_i S^-_{i+1} = c^dag_i c_{i+1}, a hopping J/2 on an open chain of L sites
eps = np.linalg.eigvalsh(0.5 * J * (np.eye(L, k=1) + np.eye(L, k=-1)))
ferm = {N: np.sort([eps[list(c)].sum() for c in itertools.combinations(range(L), N)]) for N in range(L + 1)}
for N in range(L + 1):
    assert np.allclose(spin[N], ferm[N], atol=1e-10), N

fig, ax = style.figure(height_cm=6.4, width_cm=12.0)
for N in range(L + 1):
    for e in spin[N]:
        ax.plot([N - 0.32, N + 0.32], [e, e], color=style.ACCENT, lw=1.3, zorder=2)
    ax.plot(np.full(len(ferm[N]), N), ferm[N], 'o', ms=3.4, color=style.BROKEN, zorder=3)
ax.set_xlim(-0.7, L + 0.7); ax.set_ylim(-2.0, 3.0)
ax.set_xticks(range(L + 1)); ax.tick_params(axis='x', length=2.5, pad=2, labelsize=11)
style.arrows(ax, xlabel=r'$N$', ylabel=r'$E/J$')
ax.set_xticks(range(L + 1))
ax.tick_params(axis='x', length=2.5, pad=2, labelsize=11)
ax.plot([0.35, 0.95], [2.75, 2.75], color=style.ACCENT, lw=1.3)
style.label(ax, 1.1, 2.75, 'spins, exact diagonalization', ha='left', fontsize=11, color=style.ACCENT)
ax.plot([0.65], [2.3], 'o', ms=3.4, color=style.BROKEN)
style.label(ax, 1.1, 2.3, 'free fermions, sums of levels', ha='left', fontsize=11, color=style.BROKEN)
style.save(fig, __file__)
