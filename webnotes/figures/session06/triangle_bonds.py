"""Session 6, classical spins on one triangle, with a ferromagnetic and with an antiferromagnetic coupling."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow
import style

S = 1.0
def energy(J, angles):
    v = [S * np.array([np.cos(a), np.sin(a)]) for a in angles]
    return [J * v[i] @ v[j] for i, j in ((0, 1), (1, 2), (2, 0))]

cases = [(-1.0, [np.pi / 2] * 3, r'(a) $J<0$, all parallel'),
         (+1.0, [np.pi / 2, np.pi / 2 + 2 * np.pi / 3, np.pi / 2 + 4 * np.pi / 3], r'(b) $J>0$, $120^\circ$')]
fig, axs = plt.subplots(1, 2, figsize=(10.5 * style.CM, 5.0 * style.CM))
P = np.array([[0.0, 0.0], [2.0, 0.0], [1.0, 1.732]])
for ax, (J, ang, ttl) in zip(axs, cases):
    ax.axis('off'); ax.set_aspect('equal')
    e = energy(J, ang)
    for (i, j), eb in zip(((0, 1), (1, 2), (2, 0)), e):
        ax.plot(*zip(P[i], P[j]), color=style.GRID, lw=2.2, zorder=1)
        mid = (P[i] + P[j]) / 2 + 0.0
        out = (mid - P.mean(axis=0)); out /= np.hypot(*out)
        style.label(ax, *(mid + 0.55 * out), r'$%+.1f\,|J|S^2$' % eb if abs(eb) != 0.5 else r'$%+.1f\,|J|S^2$' % eb, fontsize=7.5, color=style.BROKEN if eb > -0.99 else style.INK)
    for p, a in zip(P, ang):
        ax.add_patch(FancyArrow(p[0] - 0.45 * np.cos(a), p[1] - 0.45 * np.sin(a), 0.9 * np.cos(a), 0.9 * np.sin(a), width=0.07, head_width=0.3, head_length=0.26,
                                length_includes_head=True, fc=style.ACCENT, ec='none', zorder=3))
        ax.plot(*p, 'o', color=style.INK, ms=3, zorder=4)
    style.label(ax, 1.0, 3.0, ttl, fontsize=8.5)
    style.label(ax, 1.0, -1.15, r'total $%+.1f\,|J|S^2$' % sum(e), fontsize=8.5)
    ax.set_xlim(-1.3, 3.3); ax.set_ylim(-1.5, 3.3)
assert abs(sum(energy(-1.0, cases[0][1])) + 3) < 1e-12 and abs(sum(energy(1.0, cases[1][1])) + 1.5) < 1e-12
style.save(fig, __file__)
