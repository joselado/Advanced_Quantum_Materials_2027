"""Session 10, Eq. (10.6) for one configuration s, one D x D matrix per site multiplied into a number."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import style

s = [1, -1, -1, 1, -1]
D = 3
fig, ax = plt.subplots(figsize=(style.WIDTH_CM * style.CM, 4.4 * style.CM))
ax.axis('off'); ax.set_aspect('equal')
gap = 1.0
for i, v in enumerate(s):
    x0 = i * (D + gap)
    col = style.ACCENT if v > 0 else style.BROKEN
    ax.annotate('', xy=(x0 + D / 2, 3.4 + 0.45 * v), xytext=(x0 + D / 2, 3.4 - 0.45 * v),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.6, mutation_scale=9, shrinkA=0, shrinkB=0))
    ax.add_patch(Rectangle((x0, 0), D, D, fc='none', ec=col, lw=1.6))
    for k in range(1, D):
        ax.plot([x0 + k, x0 + k], [0, D], color=style.GRID, lw=0.7)
        ax.plot([x0, x0 + D], [k, k], color=style.GRID, lw=0.7)
    style.label(ax, x0 + D / 2, -0.55, r'$A^{\uparrow}$' if v > 0 else r'$A^{\downarrow}$', color=col, fontsize=9)
    if i < len(s) - 1:
        style.label(ax, x0 + D + gap / 2, D / 2, r'$\times$', fontsize=10)
n = len(s) * (D + gap) - gap
style.label(ax, n + 1.0, D / 2, r'$\mathrm{Tr}\,\to\,C(s)$', fontsize=9, ha='left')
style.label(ax, -0.2, 3.4, r'$s$', fontsize=10, ha='right')
ax.set_xlim(-1.2, n + 5.5); ax.set_ylim(-1.1, 4.2)
style.save(fig, __file__)
