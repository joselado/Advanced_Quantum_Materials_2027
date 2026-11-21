"""Shared code of the picture options of the quiz of Section 2.2, the electric field on the mirror axis of a charge.

Each picture shows the same uniformly charged egg, which has one mirror axis, the axis as a dashed line, a point on
the axis above the egg, and one arrow at that point. The arrow is along the axis, across it, or tilted. The field of
the egg is computed here by a sum over a grid of charges inside the drawn shape, and the asserts check that at the
point on the axis it points along the axis and away from the egg, and that at a point away from the axis it is
tilted. A picture is a drawing with no axes, so it is saved with sketch=True. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import style

A, B, EPS = 1.25, 1.0, -0.25          # half height, half width, and the asymmetry between the top and the bottom
P = np.array([0.0, 2.0])               # the point on the axis
ARROWS = {'along': (0.0, 0.95), 'across': (0.95, 0.0), 'tilted': (0.67, 0.67)}


def half_width(y):
    """The half width of the egg at the height y. It is the same on the left and on the right, so x -> -x is a mirror,
    while the top and the bottom differ, so y -> -y is not."""
    return B * np.sqrt(np.clip(1 - (y / A) ** 2, 0, None)) * (1 + EPS * y / A)


def field(p, n=241):
    """The electric field at the point p of a uniform charge on the egg, in arbitrary units, from a grid that is
    symmetric under x -> -x."""
    xs = np.linspace(-B * 1.3, B * 1.3, n)
    ys = np.linspace(-A, A, n)
    X, Y = np.meshgrid(xs, ys)
    inside = np.abs(X) < half_width(Y)
    d = np.stack([p[0] - X[inside], p[1] - Y[inside]], axis=1)
    r = np.linalg.norm(d, axis=1)
    return (d / r[:, None] ** 3).sum(0)


def check():
    yy = np.linspace(-A, A, 101)
    assert not np.allclose(half_width(yy), half_width(-yy))                            # the top and bottom differ
    e = field(P)
    assert abs(e[0]) < 1e-9 * abs(e[1]) and e[1] > 0          # on the axis, along the axis and away from the egg
    q = field(np.array([1.6, 1.6]))
    assert abs(q[0]) > 0.3 * np.linalg.norm(q) and abs(q[1]) > 0.3 * np.linalg.norm(q)   # away from it, tilted
    for name, (dx, dy) in ARROWS.items():
        assert np.isclose(np.hypot(dx, dy), 0.95, atol=0.01)                            # the three arrows have one length
    dx, dy = ARROWS['tilted']
    assert np.isclose(np.degrees(np.arctan2(dx, dy)), 45.0)          # the alt text: tilted by 45 degrees from the axis
    assert np.isclose(np.degrees(np.arctan2(*ARROWS['across'])), 90.0) and ARROWS['along'][0] == 0.0
    print('field on the axis', np.round(e, 4), 'away from it', np.round(q, 4))


def option(script, name):
    """One picture option, with the arrow ARROWS[name] at the point on the axis."""
    check()
    fig, ax = plt.subplots(figsize=(3.6 * style.CM, 4.3 * style.CM))
    ax.set_aspect('equal'); ax.axis('off')
    y = np.linspace(-A, A, 200)
    w = half_width(y)
    ax.add_patch(Polygon(np.r_[np.c_[w, y], np.c_[-w[::-1], y[::-1]]], closed=True, facecolor=style.LIGHT, alpha=0.35,
                         edgecolor=style.ACCENT, lw=1.2))
    for x0, y0 in ((-0.5, -0.55), (0.5, -0.55), (-0.55, 0.12), (0.55, 0.12), (-0.3, 0.75), (0.3, 0.75)):
        style.label(ax, x0, y0, '+', fontsize=9, color=style.ACCENT)
    ax.plot([0, 0], [-A - 0.35, P[1] + 1.25], color=style.MUTED, lw=1.0, ls=(0, (4, 3)), zorder=1)
    ax.scatter(*P, s=22, color=style.INK, zorder=4)
    dx, dy = ARROWS[name]
    ax.annotate('', xy=(P[0] + dx, P[1] + dy), xytext=tuple(P), zorder=5,
                arrowprops=dict(arrowstyle='-|>', color=style.BROKEN, lw=1.8, mutation_scale=10, shrinkA=0, shrinkB=0))
    ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.7, 3.35)
    # an empty frame over the whole window, so that the three pictures are cut to the same size
    ax.add_patch(plt.Rectangle((-1.45, -1.7), 2.9, 5.05, fill=False, lw=0, ec='none'))
    style.save(fig, script, sketch=True)
