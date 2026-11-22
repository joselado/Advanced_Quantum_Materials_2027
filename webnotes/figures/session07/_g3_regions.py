"""Shared code of the picture options of the first quiz of Section 7.7, which region of 16 sites of a square lattice has
the largest entropy under the area law S = alpha |dA|.

Each picture is the same patch of 18 by 6 sites of a square lattice, with the same spacing, so that the three regions
are drawn on the same scale. The region is shaded, its sites are filled, and the bonds between a site inside and a
site outside are red, the cut bonds that the student counts. The check counts them bond by bond and asserts 16, 20 and
34 for the square of 4 by 4, the rectangle of 2 by 8 and the line of 1 by 16, which is 2(a+b) for a region of a by b
sites that does not touch the edge of the patch. A picture is a drawing with no axes, so it is saved with sketch=True.
This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import LineCollection
import style

NX, NY = 18, 6
REGIONS = {'square': (7, 1, 4, 4), 'rect': (5, 2, 8, 2), 'line': (1, 2, 16, 1)}     # x0, y0, width, height in sites
EXPECTED = {'square': 16, 'rect': 20, 'line': 34}


def bonds(kind):
    x0, y0, w, h = REGIONS[kind]
    inside = lambda x, y: x0 <= x < x0 + w and y0 <= y < y0 + h
    grey, red = [], []
    for x in range(NX):
        for y in range(NY):
            for dx, dy in ((1, 0), (0, 1)):
                x2, y2 = x + dx, y + dy
                if x2 < NX and y2 < NY:
                    (red if inside(x, y) != inside(x2, y2) else grey).append([(x, y), (x2, y2)])
    return inside, grey, red


def check():
    for kind, n in EXPECTED.items():
        x0, y0, w, h = REGIONS[kind]
        assert w * h == 16, kind
        assert x0 >= 1 and y0 >= 1 and x0 + w <= NX - 1 and y0 + h <= NY - 1, kind     # away from the edge
        cut = len(bonds(kind)[2])
        assert cut == n == 2 * (w + h), (kind, cut)


def option(script, kind):
    check()
    inside, grey, red = bonds(kind)
    x0, y0, w, h = REGIONS[kind]
    fig, ax = plt.subplots(figsize=(4.8 * style.CM, 1.75 * style.CM))
    ax.set_xlim(-0.5, NX - 0.5); ax.set_ylim(-0.5, NY - 0.5); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((x0 - 0.4, y0 - 0.4), w - 1 + 0.8, h - 1 + 0.8, facecolor='#e6eef6', edgecolor=style.LIGHT,
                           lw=0.8, zorder=0))
    ax.add_collection(LineCollection(grey, colors=style.GRID, linewidths=0.7, zorder=1))
    ax.add_collection(LineCollection(red, colors=style.BROKEN, linewidths=1.5, zorder=2))
    pts = [(x, y) for x in range(NX) for y in range(NY)]
    face = [style.ACCENT if inside(x, y) else 'white' for x, y in pts]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=5, c=face, edgecolors=style.ACCENT, linewidths=0.6, zorder=3)
    style.save(fig, script, sketch=True)
