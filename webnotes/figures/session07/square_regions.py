"""Session 7, quiz of 7.7, a square region of side 2 and one of side 4 on a square lattice, with the cut bonds counted."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
from matplotlib.patches import Rectangle
from matplotlib.collections import LineCollection

def panel(ax, side, n=8, origin=0):
    inside = lambda x, y: origin <= x < origin + side and origin <= y < origin + side
    ax.add_patch(Rectangle((origin - 0.3, origin - 0.3), side - 1 + 0.6, side - 1 + 0.6, facecolor='#e6eef6', edgecolor=style.LIGHT, lw=1.0, zorder=0))
    grey, red = [], []
    for x in range(n):
        for y in range(n):
            for dx, dy in ((1, 0), (0, 1)):
                x2, y2 = x + dx, y + dy
                if x2 < n and y2 < n:
                    (red if inside(x, y) != inside(x2, y2) else grey).append([(x, y), (x2, y2)])
    ax.add_collection(LineCollection(grey, colors=style.GRID, linewidths=1.0, zorder=1))
    ax.add_collection(LineCollection(red, colors=style.BROKEN, linewidths=1.8, zorder=2))
    pts = [(x, y) for x in range(n) for y in range(n)]
    face = [style.ACCENT if inside(x, y) else 'white' for x, y in pts]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=18, c=face, edgecolors=style.ACCENT, linewidths=1.0, zorder=3)
    return len(red)

fig, axs = style.plt.subplots(1, 2, figsize=(9.5 * style.CM, 5.0 * style.CM))
n = 8
cuts = []
for ax, side, org in zip(axs, (2, 4), (3, 2)):
    ax.set_xlim(-0.6, n - 0.4); ax.set_ylim(-0.6, n - 0.4); ax.set_aspect('equal'); ax.axis('off')
    cuts.append(panel(ax, side, n, org))
assert cuts == [8, 16]                                          # 4 times the side
for ax, side, c in zip(axs, (2, 4), cuts):
    style.label(ax, 3.5, -1.2, r'side %d, %d bonds cut' % (side, c), fontsize=8.3, color=style.BROKEN)
style.save(fig, __file__)
