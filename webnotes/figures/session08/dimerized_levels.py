"""Session 8, the lowest levels of the open four-site chain J(S0.S1 + S2.S3) + J' S1.S2 against J', by exact diagonalization."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

sx = np.array([[0, 1], [1, 0]]) / 2; sy = np.array([[0, -1j], [1j, 0]]) / 2; sz = np.diag([.5, -.5])
N = 4
def op(o, i):
    m = np.eye(1)
    for j in range(N):
        m = np.kron(m, o if j == i else np.eye(2))
    return m
def SS(i, j):
    return sum(op(s, i) @ op(s, j) for s in (sx, sy, sz)).real
def spectrum(Jp):
    return np.linalg.eigvalsh(SS(0, 1) + SS(2, 3) + Jp * SS(1, 2))

e = spectrum(0.1)
assert abs(e[0] + 1.50096) < 1e-5 and abs(e[1] + 0.52749) < 1e-5 and e[0] < e[1] - 0.9       # the numbers of the quiz of the page
Jp = np.linspace(0, 1.0, 101)
E = np.array([spectrum(j) for j in Jp])

fig, ax = style.figure(height_cm=5.6, width_cm=11.0)
# the singlet ground state, the triplet above it, and the second singlet, each drawn once
ax.plot(Jp, E[:, 0], color=style.BROKEN)
ax.plot(Jp, E[:, 1], color=style.ACCENT)
ax.plot(Jp, E[:, 4], color=style.MUTED, lw=1.4)
ax.axvline(0.1, color=style.GRID, lw=1.0, zorder=0)
ax.set_xlim(0, 1.0); ax.set_ylim(-2.0, 0.55)
style.label(ax, 0.30, -1.8, r'ground state, a nondegenerate singlet', color=style.BROKEN, fontsize=8.3, ha='left')
style.label(ax, 0.30, -1.02, r'lowest triplet, threefold', color=style.ACCENT, fontsize=8.3, ha='left')
style.label(ax, 0.55, -0.10, r'other triplet', color=style.MUTED, fontsize=8.3, ha='left')
style.label(ax, 0.105, 0.42, r"$J'=0.1$", color=style.MUTED, fontsize=8.3, ha='left')
ax.set_xticks([0, 0.5, 1.0]); ax.set_xticklabels([r'$0$', r'$0.5$', r'$1$']); ax.set_yticks([-1.5, -1, -0.5, 0]); ax.tick_params(length=2.5, pad=2)
style.arrows(ax, xlabel=r"$J'/J$", ylabel=r'$E/J$', ticks=True)
style.save(fig, __file__)
