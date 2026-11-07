"""Shared drawing of the small concept maps of the index pages of Sessions 3 and 4.

A map has three tiers, what the session takes from before, what it builds, and where it comes back. Each box is a concept with
the section or session where it lives, and an arrow means that the concept at its tail is used to build the one at its head.
The coordinates are in cm on a canvas of the width of the figure. This file writes no figure."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import style

TIERS = {'before': (style.MUTED, '#f2f2f2'), 'now': (style.ACCENT, '#e6eef6'), 'later': (style.BROKEN, '#f7ebe9')}


def draw(boxes, arrows, headers, width=12.0, height=9.0, fontsize=11):
    """boxes: name -> (x, y, w, tier, text). arrows: (tail, head). headers: (y, text, tier)."""
    fig = plt.figure(figsize=(width * style.CM, height * style.CM))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, width); ax.set_ylim(0, height); ax.axis('off')
    H = {}
    for name, (x, y, w, tier, text) in boxes.items():
        edge, face = TIERS[tier]
        h = 0.48 * (text.count('\n') + 1) + 0.26
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle='round,pad=0,rounding_size=0.15',
                                    fc=face, ec=edge, lw=0.9, zorder=2))
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, color=style.INK, zorder=3, linespacing=1.15)
        H[name] = (x, y, w, h)
    for a, b in arrows:
        xa, ya, wa, ha = H[a]; xb, yb, wb, hb = H[b]
        if abs(ya - yb) < 1e-6:                      # same tier, from side to side
            s = 1 if xb > xa else -1
            p, q = (xa + s * wa / 2, ya), (xb - s * wb / 2, yb)
        else:                                       # from the bottom of the tail to the top of the head
            p, q = (xa + 0.25 * (xb - xa) / max(1, abs(xb - xa)) * min(abs(xb - xa), wa / 2), ya - ha / 2), (xb, yb + hb / 2)
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle='-|>', mutation_scale=8, lw=0.8, color=style.INK,
                                     shrinkA=1, shrinkB=1, zorder=1))
    for y, text, tier in headers:
        ax.text(0.08, y, text, ha='left', va='center', fontsize=fontsize, color=TIERS[tier][0], style='italic')
    return fig
