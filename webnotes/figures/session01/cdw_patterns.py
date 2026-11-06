"""Session 1, the two charge patterns of period two that a translation by one site exchanges."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

fig, ax = plt.subplots(figsize=(9.6 * style.CM, 3.0 * style.CM))
ax.axis('off'); ax.set_aspect('equal')
N = 6
pat = np.array([0.8, 0.2] * 3)
assert np.allclose(np.roll(pat, 1), 1 - pat) and np.isclose(pat.mean(), 0.5)   # a translation gives the other pattern
for y, p, name in ((1.0, pat, r'$(0.8,\,0.2,\,\dots)$'), (-0.3, np.roll(pat, 1), r'$(0.2,\,0.8,\,\dots)$')):
    ax.plot([0, N - 1], [y, y], color=style.GRID, lw=1.2, zorder=1)
    for i in range(N):
        ax.scatter([i], [y], s=330, color='white', edgecolor=style.MUTED, lw=0.8, zorder=2)
        ax.scatter([i], [y], s=330 * p[i], color=style.ACCENT, zorder=3)
    style.label(ax, N - 0.2, y, name, ha='left', fontsize=8)
ax.annotate('', xy=(-1.0, -0.15), xytext=(-1.0, 0.85), arrowprops=dict(arrowstyle='-|>', color=style.BROKEN, lw=1.1, shrinkA=0, shrinkB=0, mutation_scale=8))
style.label(ax, -1.3, 0.35, 'translation\nby one site', color=style.BROKEN, ha='right', fontsize=8)
ax.set_xlim(-3.6, N + 3.0); ax.set_ylim(-0.9, 1.6)
style.save(fig, __file__)
