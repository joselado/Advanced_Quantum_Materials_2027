"""Session 8, quiz of 8.4, the 8 Ising configurations of an antiferromagnetic triangle with their energies."""
import os, sys, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
from matplotlib.patches import FancyArrowPatch, Circle

configs = list(itertools.product([1, -1], repeat=3))
bonds = [(0, 1), (1, 2), (2, 0)]
def energy(c):
    return sum(0.25 * c[i] * c[j] for i, j in bonds)             # H = sum S^z_i S^z_j with S^z = +-1/2
E = [energy(c) for c in configs]
assert sorted(E) == [-0.25] * 6 + [0.75] * 2                      # six ground states with one unsatisfied bond

fig, axs = style.plt.subplots(2, 4, figsize=(9.5 * style.CM, 5.6 * style.CM))
order = sorted(range(8), key=lambda i: (E[i], -configs[i][0], -configs[i][1], -configs[i][2]))
for ax, idx in zip(axs.flat, order):
    c = configs[idx]; e = E[idx]
    ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.45, 1.35); ax.set_aspect('equal'); ax.axis('off')
    P = [np.array([-0.8, -0.55]), np.array([0.8, -0.55]), np.array([0.0, 0.85])]
    for i, j in bonds:
        bad = c[i] == c[j]
        ax.plot([P[i][0], P[j][0]], [P[i][1], P[j][1]], color=style.BROKEN if bad else style.GRID, lw=2.0 if bad else 1.2, zorder=1)
    for p, s in zip(P, c):
        ax.add_patch(Circle(p, 0.2, facecolor='white', edgecolor='none', zorder=2))
        ax.add_patch(FancyArrowPatch((p[0], p[1] - s * 0.3), (p[0], p[1] + s * 0.3), arrowstyle='-|>', mutation_scale=10, color=style.ACCENT, lw=1.6, zorder=3, shrinkA=0, shrinkB=0))
    style.label(ax, 0, -1.2, r'$E=%s$' % (r'-\frac{1}{4}' if e < 0 else r'+\frac{3}{4}'), fontsize=8.0, color=style.INK)
style.save(fig, __file__)
