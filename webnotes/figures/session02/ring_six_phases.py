"""Session 2, the allowed phases of a ring of six sites and the phases that are not allowed."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

L = 6
allowed = 2 * np.pi * np.arange(L) / L
cand = 2 * np.pi * np.arange(2 * L) / (2 * L)                  # the phases of a ring with twice the sites, spacing pi/6
isok = np.array([np.isclose(np.exp(1j * c * L), 1) for c in cand])
assert isok.sum() == 6 and np.allclose(np.exp(1j * np.pi / 6 * L), -1)
fig, ax = plt.subplots(figsize=(style.WIDTH_CM * style.CM * 0.55, 4.6 * style.CM))
ax.set_aspect('equal'); ax.axis('off')
th = np.linspace(0, 2 * np.pi, 200)
ax.plot(np.cos(th), np.sin(th), color=style.GRID, lw=1.2)
for c, ok in zip(cand, isok):
    if ok:
        ax.scatter([np.cos(c)], [np.sin(c)], s=34, color=style.ACCENT, zorder=3)
    else:
        ax.scatter([np.cos(c)], [np.sin(c)], s=26, marker='x', color=style.BROKEN, zorder=3, lw=1.1)
style.label(ax, 0, 0.14, r'dots, $\lambda^6=1$', fontsize=7.5, color=style.ACCENT)
style.label(ax, 0, -0.14, r'crosses, $\lambda^6=-1$', fontsize=7.5, color=style.BROKEN)
style.label(ax, 1.37, 0.0, r'$0$', fontsize=8.5, ha='left'); style.label(ax, 1.07, 0.52, r'$\pi/6$', fontsize=8, ha='left', color=style.BROKEN)
ax.set_xlim(-1.3, 1.9); ax.set_ylim(-1.3, 1.3)
style.save(fig, __file__)
