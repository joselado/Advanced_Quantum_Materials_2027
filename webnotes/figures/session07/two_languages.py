"""Session 7, the single-site dictionary between a fermion and a spin-1/2, and the sign that differs."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
from matplotlib.patches import Circle, FancyArrowPatch

fig, ax = style.plt.subplots(figsize=(style.WIDTH_CM * style.CM, 5.6 * style.CM))
ax.set_xlim(-0.9, 10.3); ax.set_ylim(-2.0, 3.3); ax.set_aspect('equal'); ax.axis('off')
occ = [1, 0, 1]
xs = [1.0, 3.0, 5.0]
for x, n in zip(xs, occ):
    ax.add_patch(Circle((x, 2.2), 0.45, facecolor=style.ACCENT if n else 'white', edgecolor=style.ACCENT, lw=1.4))
    ax.plot([x, x], [1.7, 0.95], color=style.GRID, lw=1.0, ls=(0, (2, 2)))
    ax.add_patch(FancyArrowPatch((x, 0.1 if n else 0.9), (x, 0.9 if n else 0.1), arrowstyle='-|>', mutation_scale=11,
                                 color=style.BROKEN if n else style.MUTED, lw=1.6))
    ax.plot([x - 0.35, x + 0.35], [0.5, 0.5], color=style.GRID, lw=0.8, zorder=0)
style.label(ax, -0.1, 2.2, 'fermion', ha='right', color=style.INK)
style.label(ax, -0.1, 0.5, 'spin-1/2', ha='right', color=style.INK)
for x, n in zip(xs, occ):
    style.label(ax, x, 2.95, r'$n=%d$' % n, fontsize=8.5)
    style.label(ax, x, -0.3, r'$S^z=%s$' % (r'+\frac{1}{2}' if n else r'-\frac{1}{2}'), fontsize=8.5)
style.label(ax, -0.9, -1.0, r'on one site, $S^z_i=n_i-\frac{1}{2}$ is exact', fontsize=8.5, ha='left')
style.label(ax, 8.0, 2.2, r'$c_i c_j=-c_j c_i$', color=style.ACCENT)
style.label(ax, 8.0, 1.65, 'anticommute', fontsize=8.5, color=style.ACCENT)
style.label(ax, 8.0, 0.8, r'$S^+_i S^+_j=S^+_j S^+_i$', color=style.BROKEN)
style.label(ax, 8.0, 0.25, 'commute', fontsize=8.5, color=style.BROKEN)
style.label(ax, -0.9, -1.6, 'between sites the sign differs, and the string $K_i$ carries it', fontsize=8.5, ha='left')
style.save(fig, __file__)
