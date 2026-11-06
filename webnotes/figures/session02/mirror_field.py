"""Session 2, the mirror argument of the electric field, on the axis and away from it."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import style

fig, axs = plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.6 * style.CM))
arrow = lambda ax, p, d, **kw: ax.annotate('', xy=(p[0] + d[0], p[1] + d[1]), xytext=p,
                                           arrowprops=dict(dict(arrowstyle='-|>', lw=1.6, mutation_scale=9, shrinkA=0, shrinkB=0), **kw))
mirror = lambda ax, y0, y1: ax.plot([0, 0], [y0, y1], color=style.MUTED, lw=1.0, ls=(0, (4, 3)))
for ax in axs:
    ax.set_aspect('equal'); ax.axis('off')
# (a) a uniform plane, seen from the side
ax = axs[0]
ax.plot([-3, 3], [0, 0], color=style.INK, lw=2.2)
for x in np.linspace(-2.7, 2.7, 10):
    style.label(ax, x, -0.3, '+', fontsize=8)
mirror(ax, -0.7, 3.4)
style.label(ax, 0.0, 3.65, 'mirror', color=style.MUTED, fontsize=8.5)
P = (0.0, 1.5)
ax.scatter(*P, s=22, color=style.INK, zorder=4)
arrow(ax, P, (0.0, 1.3), color=style.ACCENT)
style.label(ax, 0.3, 2.95, r'$\mathbf{E}$', color=style.ACCENT, ha='left', fontsize=9.5)
arrow(ax, P, (1.1, 0.9), color=style.BROKEN)
arrow(ax, P, (-1.1, 0.9), color=style.BROKEN, ls=(0, (2, 2)), alpha=0.55)
style.label(ax, 1.25, 2.55, 'tilted', color=style.BROKEN, ha='left', fontsize=8.5)
style.label(ax, -1.25, 2.55, 'its mirror image', color=style.BROKEN, ha='right', fontsize=8.5, alpha=0.7)
ax.set_xlim(-3.3, 3.3); ax.set_ylim(-0.9, 4.0)
style.label(ax, -3.3, 3.9, '(a)', ha='left', fontsize=9)
# (b) an egg-shaped charge, a point on the mirror axis and a point away from it
ax = axs[1]
ax.add_patch(Ellipse((0, 0), 4.4, 2.4, facecolor=style.LIGHT, alpha=0.35, edgecolor=style.ACCENT, lw=1.2))
mirror(ax, -1.6, 3.4)
P1, P2 = (0.0, 1.9), (2.0, 1.9)
ax.scatter(*P1, s=22, color=style.INK, zorder=4)
arrow(ax, P1, (0.0, 1.2), color=style.ACCENT)
style.label(ax, 0.3, 3.5, r'$\mathbf{E}$', color=style.ACCENT, ha='left', fontsize=9.5)
ax.scatter(*P2, s=22, color=style.INK, zorder=4)
ax.scatter(-P2[0], P2[1], s=22, color=style.MUTED, zorder=4, alpha=0.6)
style.label(ax, P2[0] + 0.15, P2[1] + 0.55, r'$\mathbf{E}=\,?$', color=style.BROKEN, ha='left', fontsize=9.5)
style.label(ax, 0.0, 3.9, 'mirror', color=style.MUTED, fontsize=8.5)
ax.set_xlim(-3.3, 3.3); ax.set_ylim(-1.7, 4.2)
style.label(ax, -3.3, 4.1, '(b)', ha='left', fontsize=9)
style.save(fig, __file__)
