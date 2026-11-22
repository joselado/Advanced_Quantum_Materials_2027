"""Shared code of the picture options of the first quiz of Section 7.6, which block of the product of singlets (7.8)
has zero entanglement entropy.

Each picture is the chain of 8 sites with the singlets on (0,1), (2,3), (4,5), (6,7) drawn as arcs of one color, and
one block of sites shaded. Unlike the old helper _dimerchain.py, nothing is red and there is no label under the chain,
so the picture does not give the answer, and the site numbers stay. The check counts the singlets that the block cuts,
a singlet being cut when only one of its two sites is in the block, and asserts 2, 0 and 2 for the blocks 1 to 4, 2 to 5
and 3 to 6. A picture is a drawing with no axes, so it is saved with sketch=True. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Arc
import style

EXPECTED = {(1, 4): 2, (2, 5): 0, (3, 6): 2}


def ncut(block):
    lo, hi = block
    return sum((lo <= a <= hi) != (lo <= a + 1 <= hi) for a in range(0, 8, 2))


def option(script, block):
    for b, n in EXPECTED.items():
        assert ncut(b) == n, (b, ncut(b))
    lo, hi = block
    fig, ax = plt.subplots(figsize=(4.6 * style.CM, 1.9 * style.CM))
    ax.set_xlim(-0.6, 7.6); ax.set_ylim(-1.0, 0.95); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(FancyBboxPatch((lo - 0.42, -0.42), hi - lo + 0.84, 0.84, boxstyle='round,pad=0,rounding_size=0.3',
                                facecolor='#e6eef6', edgecolor=style.LIGHT, lw=1.0, zorder=0))
    for a in range(0, 8, 2):
        ax.add_patch(Arc((a + 0.5, -0.32), 1.0, 1.1, theta1=180, theta2=360, color=style.ACCENT, lw=1.6, zorder=1))
    for i in range(8):
        inside = lo <= i <= hi
        ax.add_patch(Circle((i, 0), 0.28, facecolor=style.ACCENT if inside else 'white', edgecolor=style.ACCENT,
                            lw=1.2, zorder=3))
        style.label(ax, i, 0.66, str(i), fontsize=9, color=style.INK)
    style.save(fig, script, sketch=True)
