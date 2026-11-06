"""Session 7, quiz of 7.9, an MPO acting on an MPS, drawn as a tensor diagram, with the bond dimensions that multiply."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch

fig, ax = style.plt.subplots(figsize=(style.WIDTH_CM * 0.78 * style.CM, 5.6 * style.CM))
ax.set_xlim(-0.8, 12.4); ax.set_ylim(-1.7, 3.7); ax.set_aspect('equal'); ax.axis('off')
xs = [0.6, 2.4, 4.2]
# left: the MPO (squares, bond D) on top of the MPS (circles, bond M), joined by the physical legs
for x in xs:
    ax.plot([x, x], [2.1, 2.9], color=style.INK, lw=1.0)              # outgoing physical leg of the MPO
    ax.plot([x, x], [0.3, 1.5], color=style.INK, lw=1.0)              # physical leg shared, summed over
    ax.add_patch(Rectangle((x - 0.32, 1.5), 0.64, 0.64, facecolor='white', edgecolor=style.BROKEN, lw=1.4, zorder=3))
    ax.add_patch(Circle((x, 0.0), 0.32, facecolor='white', edgecolor=style.ACCENT, lw=1.4, zorder=3))
for a, b in zip(xs[:-1], xs[1:]):
    ax.plot([a + 0.32, b - 0.32], [1.82, 1.82], color=style.BROKEN, lw=1.4)
    ax.plot([a + 0.32, b - 0.32], [0.0, 0.0], color=style.ACCENT, lw=1.4)
style.label(ax, 1.5, 1.82 + 0.45, r'$D$', color=style.BROKEN, fontsize=9)
style.label(ax, 1.5, -0.42, r'$M$', color=style.ACCENT, fontsize=9)
style.label(ax, 2.4, -1.25, r'MPO on MPS', fontsize=8.5, color=style.MUTED)
ax.add_patch(FancyArrowPatch((5.2, 1.0), (6.7, 1.0), arrowstyle='-|>', mutation_scale=11, color=style.INK, lw=1.2))
style.label(ax, 5.95, 1.5, 'contract', fontsize=8, color=style.MUTED)
# right: the result, one tensor per site with the two bonds fused
xr = [8.0, 9.8, 11.6]
for x in xr:
    ax.plot([x, x], [1.0 + 0.3, 2.2], color=style.INK, lw=1.0)
    ax.add_patch(Circle((x, 1.0), 0.32, facecolor='white', edgecolor=style.INK, lw=1.4, zorder=3))
for a, b in zip(xr[:-1], xr[1:]):
    ax.plot([a + 0.32, b - 0.32], [1.0, 1.0], color=style.INK, lw=2.8)
    style.label(ax, (a + b) / 2, 1.5, r'$M\cdot D$', color=style.INK, fontsize=9)
style.label(ax, 9.8, -1.25, r'result, no truncation', fontsize=8.5, color=style.MUTED)
style.save(fig, __file__)
