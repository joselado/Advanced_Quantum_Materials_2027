"""Session 1, the lowest levels of a hexagonal honeycomb island, H = -t sum c_i^+ c_j over first neighbors.

Each panel is the density of one level, summed over its degenerate states, which is what a scanning tunneling
microscope maps at that energy. The disc area on a site is proportional to the density there.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import style

t = 1.0
FS = 10.5
NR = 4                                      # hexagons along each edge of the island
# the island is the union of the hexagons whose centres are at most NR-1 hexagon steps from the origin,
# the hexagons have side 1 and their centres form a triangular lattice of spacing sqrt(3)
b1, b2 = np.sqrt(3) * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)]), np.sqrt(3) * np.array([0.0, 1.0])
pts = []
for i in range(-NR, NR + 1):
    for j in range(-NR, NR + 1):
        if max(abs(i), abs(j), abs(i + j)) <= NR - 1:            # hexagonal distance on the triangular lattice
            c = i * b1 + j * b2
            for th in np.arange(6) * np.pi / 3:
                pts.append(c + np.array([np.cos(th), np.sin(th)]))
pts = np.unique(np.round(np.array(pts), 6), axis=0)
d = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=-1)
A = np.isclose(d, 1.0).astype(float)
H = -t * A
E, V = np.linalg.eigh(H)
R = np.linalg.norm(pts, axis=1).max()
assert len(pts) == 6 * NR ** 2 and A.sum(1).min() == 2 and A.sum(1).max() == 3
# group the degenerate levels, lowest first
levels, i = [], 0
while i < len(E):
    j = i
    while j + 1 < len(E) and abs(E[j + 1] - E[i]) < 1e-6:
        j += 1
    levels.append((E[i], list(range(i, j + 1))))
    i = j + 1
show = [0, 1, 5]
dens = [np.sum(np.abs(V[:, levels[n][1]]) ** 2, axis=1) / len(levels[n][1]) for n in show]
# the lowest level has its maximum close to the centre and no node, the higher ones have more structure
r = np.linalg.norm(pts, axis=1)
assert np.all(V[:, 0] * np.sign(V[0, 0]) > 0)                  # nodeless, by Perron-Frobenius
assert dens[0][r < 1.5].mean() > 3 * dens[0][r > R - 1.2].mean()
assert dens[1][r < 1.0].mean() < dens[1].max() / 3              # the second level has a node at the centre

segs = [pts[[p, q]] for p in range(len(pts)) for q in range(p + 1, len(pts)) if A[p, q]]
fig, axs = plt.subplots(1, 3, figsize=(12.5 * style.CM, 5.4 * style.CM))
fig.subplots_adjust(wspace=0.04, left=0.0, right=1.0)
names = ['lowest level', 'second level', 'sixth level']
for ax, n, rho, nm in zip(axs, show, dens, names):
    ax.axis('off'); ax.set_aspect('equal')
    ax.add_collection(LineCollection(segs, colors=style.GRID, linewidths=0.6, zorder=1))
    # disc area proportional to the density, in 20 bins, so that each bin is one marker that the SVG reuses
    ms = np.round(20 * np.sqrt(rho / dens[0].max())) / 20 * 6.6
    for m in np.unique(ms[ms > 0]):
        sel = ms == m
        ax.plot(pts[sel, 0], pts[sel, 1], 'o', ms=m, color=style.ACCENT, mew=0, zorder=3)
    ax.text(0, R + 0.9, nm, ha='center', va='bottom', fontsize=FS)
    ax.text(0, -R - 1.0, r'$E=%.2f\,t$' % levels[n][0], ha='center', va='top', fontsize=FS)
    ax.set_xlim(-R - 0.6, R + 0.6); ax.set_ylim(-R - 2.6, R + 2.4)
style.save(fig, __file__)
