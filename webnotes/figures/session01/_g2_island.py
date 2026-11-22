"""Shared code of the figures of Section 1.10 on the hexagonal honeycomb island, the figure island_states and the three
picture options of the quiz on the lowest level (g2_quiz_island_lowest, g2_quiz_island_second, g2_quiz_island_sixth).

The data come from the downloadable script webnotes/scripts/session01/g2_honeycomb_island.py, which calls pyqula with
the hopping -t of the caption, t = 1. Each figure script runs it with style.run_script and passes its variables here. The island is the union of the hexagons at most three steps from the central one,
96 sites with zigzag edges, and the positions are in units of the bond length a. A disc has an area proportional to the
density of the level on that site, averaged over the degenerate states of the level, with the same scale in every panel
and in every picture. The numbers that the caption and the feedback of the quiz quote are asserted in check(). This
file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import style

SHOW = (0, 1, 5)                                    # the lowest, the second and the sixth level, a degenerate level once
NAMES = {0: 'lowest level', 1: 'second level', 5: 'sixth level'}
S_LOWEST = 44.0                                     # area in pt^2 of the disc of the largest density of the lowest level
KEY = 0.03                                          # density of the disc of the key
LIM = 6.9                                           # half width of a panel, in units of a
TICKS = [-5, 0, 5]


def old_island(nr=4):
    """The numpy construction of the old figure: the hexagons whose centers are at most nr-1 steps from the origin."""
    b1, b2 = np.sqrt(3) * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)]), np.sqrt(3) * np.array([0.0, 1.0])
    pts = []
    for i in range(-nr, nr + 1):
        for j in range(-nr, nr + 1):
            if max(abs(i), abs(j), abs(i + j)) <= nr - 1:
                c = i * b1 + j * b2
                pts += [c + np.array([np.cos(th), np.sin(th)]) for th in np.arange(6) * np.pi / 3]
    return np.unique(np.round(np.array(pts), 6), axis=0)


def check(d):
    """The island, its levels and the densities, against the caption and the feedback of the quiz."""
    x, y, H = np.asarray(d['x']), np.asarray(d['y']), np.asarray(d['h'].intra)
    r = np.hypot(x, y)
    dist = np.hypot(x[:, None] - x[None], y[:, None] - y[None])
    A = np.isclose(dist, 1.0).astype(float)
    coord = A.sum(1)
    assert len(x) == 96 == 6 * 4 ** 2
    assert np.isclose(dist[dist > 1e-6].min(), 1.0) and coord.min() == 2 and coord.max() == 3
    assert np.allclose(H, -A) and abs(x.mean()) < 1e-9 and abs(y.mean()) < 1e-9     # hopping -t, centered island
    # zigzag edges, 24 sites with two neighbors, and only the six corners join two of them
    two = coord == 2
    assert two.sum() == 24 and A[np.ix_(two, two)].sum() // 2 == 6
    # the same island and the same levels as the numpy construction of the old figure
    old = old_island()
    key = lambda p: np.array(sorted(map(tuple, np.round(p, 5))))
    assert np.abs(key(np.array([x, y]).T) - key(old)).max() < 1e-4
    dold = np.linalg.norm(old[:, None] - old[None], axis=-1)
    assert np.allclose(np.linalg.eigvalsh(-np.isclose(dold, 1.0).astype(float)), d['energies'], atol=1e-10)
    # the levels: the lowest and the sixth are single, the second is a pair
    E, lev, dens = d['energies'], d['levels'], d['density']
    deg = [int(np.sum(np.abs(E - lev[n]) < 1e-6)) for n in range(6)]
    assert deg == [1, 2, 2, 1, 1, 1], deg
    assert [round(float(lev[n]), 2) for n in SHOW] == [-2.91, -2.76, -2.34]
    assert lev[0] > -3.0                                                             # above the bottom -3t of the band
    # real eigenvectors, so that the signs can be read
    ev, V = np.linalg.eigh(H.real)
    assert np.allclose(H.imag, 0) and np.allclose(ev, E)
    v0 = V[:, 0] * np.sign(V[0, 0])
    assert np.all(v0 > 1e-6)                                    # one sign on every site, Perron-Frobenius, no node
    for k in range(1, 6):                                       # every higher state changes sign, so it has a node
        assert (V[:, k] > 1e-6).any() and (V[:, k] < -1e-6).any()
    P = np.array([[1.0 if np.hypot(x[i] + x[j], y[i] + y[j]) < 1e-6 else 0.0 for j in range(96)] for i in range(96)])
    for k in (1, 2):                                            # the two states of the second level are odd under r -> -r
        assert np.isclose(V[:, k] @ P @ V[:, k], -1.0)
    center = r < 1.01                                           # the six sites of the central hexagon
    assert center.sum() == 6
    for n in SHOW:
        assert np.isclose(dens[n].sum(), 1.0)
    # the lowest level is largest on the central hexagon and falls toward the edge
    assert np.argmax(dens[0]) in np.where(center)[0] and np.isclose(dens[0][center].min(), dens[0].max())
    assert dens[0][center].mean() > 10 * dens[0][r > 4.5].mean()
    assert dens[1][center].mean() < dens[1].max() / 3                       # 0.0042 against 0.018
    assert dens[5][center].mean() < 0.01 * dens[5].max()                    # 0.00015 against 0.037
    # the mean distance of the density from the center, 2.87, 3.74 and 4.43 bond lengths, as on the conventions sheet
    mean_r = [float((dens[n] * r).sum()) for n in SHOW]
    assert np.allclose(mean_r, [2.87, 3.74, 4.43], atol=0.005), mean_r
    assert 0.025 < KEY < max(dens[n].max() for n in SHOW)                    # the key is inside the drawn range
    return mean_r




def panel(ax, d, n, fontsize=10):
    """The island with the density of level n as discs, with its axes x/a and y/a."""
    x, y = np.asarray(d['x']), np.asarray(d['y'])
    dist = np.hypot(x[:, None] - x[None], y[:, None] - y[None])
    segs = [[(x[p], y[p]), (x[q], y[q])] for p in range(len(x)) for q in range(p + 1, len(x)) if np.isclose(dist[p, q], 1)]
    ax.add_collection(LineCollection(segs, colors=style.GRID, linewidths=0.6, zorder=1))
    # area proportional to the density, one scale for all, with the diameter rounded to 0.1 pt so that the SVG reuses
    # one marker per size
    ms = np.round(np.sqrt(S_LOWEST * d['density'][n] / d['density'][0].max()), 1)
    for m in np.unique(ms[ms > 0]):
        ax.plot(x[ms == m], y[ms == m], 'o', ms=m, color=style.ACCENT, mew=0, zorder=3)
    ax.set_aspect('equal')
    ax.set_xlim(-LIM, LIM); ax.set_ylim(-LIM, LIM)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    ax.set_xticks(TICKS); ax.set_yticks(TICKS)
    ax.set_xticklabels(['$-5$', '$0$', '$5$'], fontsize=fontsize)
    ax.set_yticklabels(['$-5$', '$0$', '$5$'], fontsize=fontsize)
    ax.tick_params(length=2.5, width=0.6, pad=2)


def main(script, d):
    """The figure island_states, the three levels side by side with their energies and the key of the disc area. The
    dictionary d holds the variables of the pyqula script, which the figure script runs itself."""
    check(d)
    fig, axs = plt.subplots(1, 3, figsize=(12.5 * style.CM, 5.6 * style.CM), sharey=True)
    fig.subplots_adjust(wspace=0.12)
    for ax, n in zip(axs, SHOW):
        panel(ax, d, n)
        ax.set_title('%s\n$E=%.2f\\,t$' % (NAMES[n], d['levels'][n]), fontsize=10.5, pad=4, linespacing=1.4)
        ax.set_xlabel(r'$x/a$', fontsize=11, labelpad=1)
    axs[0].set_ylabel(r'$y/a$', fontsize=11, labelpad=0)
    # the key, a disc of the density KEY in the empty corner of the last panel
    ax = axs[2]
    ax.plot([4.6], [6.0], 'o', ms=np.sqrt(S_LOWEST * KEY / d['density'][0].max()), color=style.ACCENT, mew=0,
            zorder=3, clip_on=False)
    style.label(ax, 5.3, 6.0, r'$0.03$', ha='left', fontsize=9.5)
    style.save(fig, script)


def option(script, d, n):
    """One picture option of the quiz, the density of level n with its axes and no other text."""
    check(d)
    fig, ax = plt.subplots(figsize=(4.3 * style.CM, 4.3 * style.CM))
    panel(ax, d, n, fontsize=10.5)
    ax.set_xlabel(r'$x/a$', fontsize=12, labelpad=0); ax.set_ylabel(r'$y/a$', fontsize=12, labelpad=-1)
    style.save(fig, script)
