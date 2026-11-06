"""Session 8, a magnetic impurity screened by a conduction electron, and a lattice of impurities that share the electrons (schematic)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
from matplotlib.patches import Circle, FancyArrowPatch, Ellipse

rng = np.random.default_rng(5)
def arrow(ax, x, y, up, col, s, ms=13):
    ax.add_patch(FancyArrowPatch((x, y - up * s / 2), (x, y + up * s / 2), arrowstyle='-|>', mutation_scale=ms, color=col, lw=2.0, zorder=5))
def sea(ax, xs, ys, skip, jit=0.18):
    for x in xs:
        for y in ys:
            p = np.array([x, y]) + rng.uniform(-jit, jit, 2)
            if not skip(p):
                ax.add_patch(Circle(p, 0.07, facecolor=style.LIGHT, edgecolor='none', zorder=2))

fig, axs = style.plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.4 * style.CM), gridspec_kw=dict(width_ratios=[1, 1.3]))
ax = axs[0]; ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.4, 3.1); ax.set_aspect('equal'); ax.axis('off')
ax.add_patch(Ellipse((0.35, 0), 2.6, 2.0, facecolor='#f1dedb', edgecolor=style.BROKEN, lw=1.0, ls=(0, (3, 2)), zorder=0))
sea(ax, np.arange(-1.9, 2.0, 0.65), np.arange(-1.3, 1.5, 0.65), lambda p: np.hypot(*p) < 0.6 or np.hypot(p[0] - 0.95, p[1]) < 0.5)
arrow(ax, 0, 0, +1, style.BROKEN, 0.9)
ax.add_patch(Circle((0.95, 0.0), 0.28, facecolor='white', edgecolor=style.ACCENT, lw=1.4, zorder=4))
arrow(ax, 0.95, 0.0, -1, style.ACCENT, 0.45, ms=9)
ax.plot([0.3, 0.67], [0, 0], color=style.BROKEN, lw=1.6, zorder=3)
style.label(ax, 0.2, 2.8, 'one impurity', fontsize=8.8)
style.label(ax, 0.2, -1.85, 'impurity and electron', fontsize=8.0, color=style.BROKEN)
style.label(ax, 0.2, -2.3, 'form a singlet', fontsize=8.0, color=style.BROKEN)
ax = axs[1]; ax.set_xlim(-0.9, 3.9); ax.set_ylim(-2.4, 3.1); ax.set_aspect('equal'); ax.axis('off')
sites = [(x, y) for y in (0.0, 1.5) for x in (0.0, 1.5, 3.0)]
for s in sites:
    ax.add_patch(Circle(s, 0.95, facecolor='#f1dedb', edgecolor='none', alpha=0.55, zorder=0))
sea(ax, np.arange(-0.6, 3.7, 0.5), np.arange(-0.6, 2.1, 0.5), lambda p: min(np.hypot(*(p - np.array(s))) for s in sites) < 0.4)
for s in sites:
    arrow(ax, s[0], s[1], +1, style.BROKEN, 0.7)
style.label(ax, 1.5, 2.8, 'a lattice of impurities', fontsize=8.8)
style.label(ax, 1.5, -1.85, 'the clouds overlap, so the', fontsize=8.0, color=style.BROKEN)
style.label(ax, 1.5, -2.3, 'electrons are shared', fontsize=8.0, color=style.BROKEN)
style.save(fig, __file__)
