"""Shared code of the picture options of the third quiz of Section 8.4, in which cluster of Ising spins with
antiferromagnetic bonds every bond can be satisfied.

Each picture is one cluster, the sites as circles and the bonds as lines, with no spin drawn, so that the picture does
not give the answer. The triangle has three sites and three bonds, the square plaquette four sites and four bonds, and
the tetrahedron four sites and all six pairs as bonds, drawn in perspective with the bond behind dashed. All three are
drawn in the same frame, so that the three SVGs have the same size.

The check enumerates the 2^N configurations of H = J sum_<ij> S^z_i S^z_j with S^z = +-1/2 and J = 1, and asserts the
numbers that the feedback of the quiz quotes. The lowest energy is -1/4 on the triangle, against -3/4 with every bond
satisfied, -1 on the square, where every bond is satisfied, and -1/2 on the tetrahedron, against -3/2. A picture is a
drawing with no axes, so it is saved with sketch=True. This file writes no figure."""
import os, sys, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import style

# the sites in the plane of the drawing and the bonds, with the bonds that are drawn dashed
CLUSTERS = {
    'triangle': ([(-0.85, -0.6), (0.85, -0.6), (0.0, 0.87)], [(0, 1), (1, 2), (2, 0)], []),
    'square': ([(-0.72, -0.72), (0.72, -0.72), (0.72, 0.72), (-0.72, 0.72)], [(0, 1), (1, 2), (2, 3), (3, 0)], []),
    'tetra': ([(-0.95, -0.55), (0.55, -0.85), (0.95, -0.12), (-0.05, 0.9)],
              [(0, 1), (1, 2), (0, 3), (1, 3), (2, 3), (0, 2)], [(0, 2)]),
}
# lowest energy, and the energy if every bond were satisfied, in units of J
EXPECTED = {'triangle': (-0.25, -0.75), 'square': (-1.0, -1.0), 'tetra': (-0.5, -1.5)}


def lowest(sites, bonds):
    return min(sum(c[i] * c[j] for i, j in bonds) for c in itertools.product((0.5, -0.5), repeat=len(sites)))


def option(script, name):
    for key, (sites, bonds, _) in CLUSTERS.items():
        e0 = lowest(sites, bonds)
        assert abs(e0 - EXPECTED[key][0]) < 1e-12 and abs(-0.25 * len(bonds) - EXPECTED[key][1]) < 1e-12, key
    sites, bonds, dashed = CLUSTERS[name]
    fig, ax = plt.subplots(figsize=(3.6 * style.CM, 3.4 * style.CM))
    ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.18, 1.18); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((-1.25, -1.18), 2.5, 2.36, facecolor='white', edgecolor='none', zorder=0))   # same frame
    for i, j in bonds:
        ls = (0, (2.5, 2.0)) if (i, j) in dashed else '-'
        ax.plot(*zip(sites[i], sites[j]), color=style.ACCENT, lw=1.8, ls=ls, zorder=1)
    for p in sites:
        ax.add_patch(Circle(p, 0.2, facecolor='white', edgecolor=style.ACCENT, lw=1.4, zorder=3))
    style.save(fig, script, sketch=True)
