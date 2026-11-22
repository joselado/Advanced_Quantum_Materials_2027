"""Session 6, Section 6.10, the moments of the mean-field ground state of the Hubbard model on the triangular lattice.

The data come from the downloadable script webnotes/scripts/session06/g3_triangular_meanfield.py, which solves the
half-filled triangular lattice at U = 10t on a cell of 3 x 3 sites with the random guess mf="XY" and maxite=4000, for
the four seeds 0 to 3, as the recipe "A noncollinear mean field on the triangular lattice" does, with nk=8 for the loop
and for get_vev. The moment of a site is read from its three components with get_vev, which is n_up - n_dn along each
axis and saturates at 1, and not with extract, which is the field with the opposite sign. The asserts hold the numbers
of the caption: 27 bonds, the angle between neighbors within 0.2 degrees of 120 degrees for every guess at the default
maxerror=1e-5 of the loop, the length 0.922 of every moment, no component along z, and the energy -3.8085 per cell of
nine sites for every guess. The check of the page asserts the caption's value below 0.001 degrees at maxerror=1e-8.
The picture is the guess of seed 0,
with the sites of the neighboring cells, and the arrows are colored by their direction, three directions at 120
degrees. The axes are x and y in units of the lattice constant a."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from matplotlib.patches import FancyArrow, Polygon
import style

d = style.run_script('session06/g3_triangular_meanfield.py')
g, pairs = d['g'], d['pairs']
assert len(pairs) == 27                                          # 9 sites with 6 neighbors each
for m, ang, e in zip(d['moments'], d['angles'], d['energies']):
    assert len(ang) == 27 and np.max(np.abs(ang - 120.)) < 0.2, np.max(np.abs(ang - 120.))
    size = np.linalg.norm(m, axis=1)
    assert np.all(np.round(size, 3) == 0.922), size
    assert np.max(np.abs(m[:, 2])) < 1e-6                       # the moments lie in the plane of the guess
    assert abs(e - (-3.8085)) < 1e-4, e
assert len(d['moments']) == 4

m = d['moments'][0]
phi = np.degrees(np.arctan2(m[:, 1], m[:, 0]))
cls = np.round(((phi - phi[0]) % 360) / 120.).astype(int) % 3   # three directions at 120 degrees
assert np.max(np.abs(((phi - phi[0] - 120. * cls) + 180.) % 360. - 180.)) < 1.   # the classes, not a caption number
assert sorted(np.bincount(cls)) == [3, 3, 3]                     # three sites of each direction in the cell
colors = [style.ACCENT, style.BROKEN, style.MUTED]

a1, a2 = np.array(g.a1)[:2], np.array(g.a2)[:2]
r0 = np.array(g.r)[:, :2]
XL, YL = 3.3, 2.3
sites = []                                                       # position and class of every site in the window
for n1 in range(-2, 3):
    for n2 in range(-2, 3):
        for i in range(9):
            p = r0[i] + n1 * a1 + n2 * a2
            if abs(p[0]) <= XL - 0.25 and abs(p[1]) <= YL - 0.2:
                sites.append((p, i))
P = np.array([p for p, _ in sites])

FS = 10.5
style.plt.rcParams['font.size'] = FS
fig, ax = style.figure(height_cm=6.6, width_cm=9.4)
style.arrows(ax, xlabel='$x/a$', ylabel='$y/a$', ticks=True)
for i in range(len(P)):                                          # the bonds of the lattice, light grey
    for j in range(i + 1, len(P)):
        if abs(np.linalg.norm(P[i] - P[j]) - 1.) < 1e-6:
            ax.plot(*zip(P[i], P[j]), color=style.GRID, lw=1.0, zorder=1)
e1, e2 = np.array([1., 0.]), np.array([-0.5, np.sqrt(3) / 2])   # the sites of the cell are i e1 + j e2, i, j = -1, 0, 1
cell = [1.5 * (s1 * e1 + s2 * e2) for s1, s2 in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
for i in range(9):                                               # check that the dashed cell holds the nine sites
    c = np.linalg.solve(np.array([e1, e2]).T, r0[i])
    assert np.allclose(c, np.round(c)) and np.all(np.abs(np.round(c)) <= 1)
ax.add_patch(Polygon(cell, closed=True, fill=False, ls=(0, (4, 3)), lw=1.0, ec=style.INK, zorder=2))
L = 0.62
for p, i in sites:
    u = m[i, :2] / np.linalg.norm(m[i, :2])
    ax.add_patch(FancyArrow(p[0] - 0.5 * L * u[0], p[1] - 0.5 * L * u[1], L * u[0], L * u[1], width=0.05,
                            head_width=0.2, head_length=0.17, length_includes_head=True, fc=colors[cls[i]], ec='none',
                            zorder=4))
    ax.plot(*p, 'o', color=style.INK, ms=2.2, zorder=5)
ax.set_aspect('equal')
ax.set_xlim(-XL, XL); ax.set_ylim(-YL, YL)
ax.set_xticks([-3, -2, -1, 0, 1, 2, 3]); ax.set_yticks([-2, -1, 0, 1, 2])
ax.tick_params(length=2.5, width=0.6, labelsize=FS - 1)
style.save(fig, __file__)
