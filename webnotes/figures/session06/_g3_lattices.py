"""Shared code of the picture options of the quiz of Section 6.10 on which lattice is frustrated for J > 0.

Each picture is a small patch of a lattice, the square, the honeycomb or the triangular lattice, with its sites and its
first-neighbor bonds, all sites drawn alike so that the picture does not give the answer. The check tries to color the
sites of each patch with two colors so that every bond joins two colors, by a walk over the bonds. It succeeds on the
square and on the honeycomb patch, which are bipartite, and it fails on the triangular patch, where a triangle of three
mutual neighbors closes an odd loop. A picture is a drawing of real space with no axes, so it is saved with
sketch=True. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style


def patch(kind):
    """The sites of a patch, about 3 by 3 lattice constants, and its first-neighbor bonds."""
    if kind == 'square':
        P = [np.array([i, j], float) for i in range(4) for j in range(4)]
    elif kind == 'triangular':
        P = [np.array([i + 0.5 * j, np.sqrt(3) / 2 * j]) for j in range(4) for i in range(-(j // 2), 4 - (j // 2))]
    elif kind == 'honeycomb':
        b = 0.65                                                  # the bond length, so that the patch fills the picture
        a1, a2 = np.array([np.sqrt(3) * b, 0.]), np.array([np.sqrt(3) / 2 * b, 1.5 * b])
        P = [i * a1 + j * a2 + d for i in range(-6, 8) for j in range(0, 8) for d in (np.array([0, 0.]), np.array([0, b]))]
        P = [p for p in P if -0.05 < p[0] < 3.2 and -0.05 < p[1] < 3.3]
    P = np.array(P)
    bl = 0.65 if kind == 'honeycomb' else 1.0
    while True:                                                   # no site hangs on a single bond
        nb = [sum(abs(np.linalg.norm(P[i] - q) - bl) < 1e-6 for q in P) for i in range(len(P))]
        if min(nb) >= 2:
            break
        P = P[np.array(nb) >= 2]
    bonds = [(i, j) for i in range(len(P)) for j in range(i + 1, len(P)) if abs(np.linalg.norm(P[i] - P[j]) - bl) < 1e-6]
    return P, bonds


def two_colors(n, bonds):
    """A coloring with two colors where every bond joins two colors, or None when there is none."""
    adj = {i: [] for i in range(n)}
    for i, j in bonds:
        adj[i].append(j); adj[j].append(i)
    color = {}
    for start in range(n):
        if start in color:
            continue
        color[start], todo = 0, [start]
        while todo:
            i = todo.pop()
            for j in adj[i]:
                if j not in color:
                    color[j] = 1 - color[i]; todo.append(j)
                elif color[j] == color[i]:
                    return None
    return color


def check():
    for kind, bipartite in (('square', True), ('honeycomb', True), ('triangular', False)):
        P, bonds = patch(kind)
        assert len(P) >= 12 and len(bonds) >= 15, (kind, len(P), len(bonds))
        assert (two_colors(len(P), bonds) is not None) == bipartite, kind


def option(script, kind):
    """One picture, the patch of one lattice with its bonds and its sites."""
    check()
    P, bonds = patch(kind)
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.9 * style.CM))
    ax.axis('off'); ax.set_aspect('equal')
    for i, j in bonds:
        ax.plot(*zip(P[i], P[j]), color=style.ACCENT, lw=1.6, zorder=1)
    ax.plot(P[:, 0], P[:, 1], 'o', color=style.INK, ms=4.5, zorder=2)
    c = (P.max(axis=0) + P.min(axis=0)) / 2
    ax.set_xlim(c[0] - 1.9, c[0] + 1.9); ax.set_ylim(c[1] - 1.9, c[1] + 1.9)
    style.save(fig, script, sketch=True)
