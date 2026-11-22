"""Session 7, section 7.9, the shared code of the three diagrams of the quiz on which network is a number.

Each diagram is a chain of four sites in the notation of the page: a circle is a tensor of the MPS, a square a tensor of
the MPO, a line between two tensors a summed index and a line that ends in the void a free index. In 'ket' and 'norm'
the MPS is on top with its physical legs pointing down. In 'hpsi' the MPO is on top of the MPS, as in Figure 7.4 and in
mpo_on_mps.svg, so its free legs point up. The three have no text, since they are the options of a quiz. build() draws
a diagram and writes nothing, so that webnotes/checks/session07/g4_09_tensor_diagrams.py can count the free legs of
what is drawn. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import style

XS = [0.0, 1.0, 2.0, 3.0]
R = 0.2


def _row_circles(ax, y, color, fill='white'):
    for a, b in zip(XS[:-1], XS[1:]):
        ax.plot([a + R, b - R], [y, y], color=color, lw=1.4, zorder=2)
    for x in XS:
        ax.add_patch(Circle((x, y), R, facecolor=fill, edgecolor=color, lw=1.4, zorder=3))


def _row_squares(ax, y, color):
    for a, b in zip(XS[:-1], XS[1:]):
        ax.plot([a + R, b - R], [y, y], color=color, lw=1.4, zorder=2)
    for x in XS:
        ax.add_patch(Rectangle((x - R, y - R), 2 * R, 2 * R, facecolor='white', edgecolor=color, lw=1.4, zorder=3))


def build(kind):
    """kind is 'ket' (open legs), 'norm' (MPS on its conjugate, closed) or 'hpsi' (MPO on top of the MPS, open legs).
    Returns the figure, its axes and the number of free legs counted while drawing."""
    plt.rcParams.update({'savefig.dpi': 220})
    fig, ax = plt.subplots(figsize=(3.6 * style.CM, 3.0 * style.CM))
    ax.set_xlim(-0.45, 3.45); ax.set_aspect('equal'); ax.axis('off')
    nfree = 0
    if kind == 'ket':
        ax.set_ylim(-0.95, 1.35)
        _row_circles(ax, 1.0, style.ACCENT)
        for x in XS:
            ax.plot([x, x], [1.0 - R, 0.35], color=style.INK, lw=1.1, zorder=1)
            nfree += 1
    elif kind == 'norm':
        ax.set_ylim(-0.95, 1.35)
        _row_circles(ax, 1.0, style.ACCENT)
        _row_circles(ax, 0.0, style.LIGHT)
        for x in XS:
            ax.plot([x, x], [1.0 - R, R], color=style.INK, lw=1.1, zorder=1)
    elif kind == 'hpsi':
        ax.set_ylim(-0.6, 1.9)
        _row_squares(ax, 1.0, style.BROKEN)
        _row_circles(ax, 0.0, style.ACCENT)
        for x in XS:
            ax.plot([x, x], [R, 1.0 - R], color=style.INK, lw=1.1, zorder=1)
            ax.plot([x, x], [1.0 + R, 1.65], color=style.INK, lw=1.1, zorder=1)
            nfree += 1
    else:
        raise ValueError(kind)
    return fig, ax, nfree


def draw(script, kind):
    """Draws the diagram and writes it as the SVG of the script. Returns the number of free legs."""
    fig, ax, nfree = build(kind)
    style.save(fig, script, sketch=True)
    return nfree
