"""Shared code of the three picture options of the quiz on the flux of a plaquette in Section 8.10.

A picture is one square plaquette with the hopping chi_ij = +1 or -1 written on each link, the links with -1 in red.
The flux is the product of the four hoppings around the plaquette, and for real hoppings the direction of the loop does
not matter. draw() asserts the flux that the feedback of the quiz states, so a picture cannot disagree with it. It is a
drawing with no axes, saved with sketch=True. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
from matplotlib.patches import Circle

CORNERS = [(-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0)]       # sites 1, 2, 3, 4, counterclockwise


def draw(script, signs, flux):
    """signs are the hoppings of the links 12, 23, 34, 41, and flux is the product that the quiz states."""
    signs = np.array(signs, float)
    assert set(np.abs(signs)) == {1.0} and np.prod(signs) == flux
    assert np.prod(signs[::-1]) == flux                                   # the same flux for the other direction
    print(os.path.basename(script), 'links', signs.astype(int).tolist(), 'flux', int(np.prod(signs)))
    fig, ax = style.plt.subplots(figsize=(4.0 * style.CM, 4.0 * style.CM))
    ax.set_xlim(-1.75, 1.75); ax.set_ylim(-1.75, 1.75); ax.set_aspect('equal'); ax.axis('off')
    for i, s in enumerate(signs):
        a, b = np.array(CORNERS[i]), np.array(CORNERS[(i + 1) % 4])
        col = style.BROKEN if s < 0 else style.ACCENT
        ax.plot([a[0], b[0]], [a[1], b[1]], color=col, lw=3.2 if s < 0 else 1.8, solid_capstyle='butt', zorder=1)
        mid = (a + b) / 2
        out = mid / np.linalg.norm(mid)
        style.label(ax, *(mid + 0.42 * out), r'$+1$' if s > 0 else r'$-1$', fontsize=12, color=col)
    for p in CORNERS:
        ax.add_patch(Circle(p, 0.17, facecolor=style.INK, edgecolor='none', zorder=3))
    style.save(fig, script, sketch=True)
