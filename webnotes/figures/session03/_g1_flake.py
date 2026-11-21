"""Shared code of the picture options of the quiz of Section 3.1, the local density of states of three flakes.

The data come from the downloadable script webnotes/scripts/session03/g1_flakes.py, which calls pyqula. The flake is a
hexagon of the honeycomb lattice with armchair edges and 834 sites, with the first-neighbor distance 1 and the hopping 1.
The three flakes have the Haldane coupling 0.1 of the notebook, a staggered potential 0.5, and no gap term with the
chemical potential moved by 0.6. The map is the local density of states at the chemical potential with a broadening
0.03, one dot per site, and the size and the color of a dot grow with it in five steps. The scale is the same in the
three maps, the largest value of the flake with the Haldane coupling, and the metal saturates. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

KEYS = ('ldos_haldane', 'ldos_staggered', 'ldos_metal')
ROWS = 3.0          # the boundary region, in units of the first-neighbor distance


def boundary_distance(x, y):
    """The distance of every site to the boundary of the hexagon, from its six flat sides."""
    r = np.array([x - x.mean(), y - y.mean()]).T
    best = None
    for th0 in np.linspace(0, np.pi / 3, 61):
        ns = np.array([[np.cos(th0 + j * np.pi / 3), np.sin(th0 + j * np.pi / 3)] for j in range(6)])
        hj = (r @ ns.T).max(0)
        if best is None or hj.sum() < best[0]:
            best = (hj.sum(), ns, hj)
    _, ns, hj = best
    return (hj[None] - r @ ns.T).min(1)


def check(d):
    """The numbers that the feedback of the quiz quotes, checked on the data of the pyqula script."""
    x, y = d['x'], d['y']
    edge = boundary_distance(x, y) < ROWS
    out = dict(sites=len(x), edge_sites=edge.mean(), gap_haldane=d['gap_haldane'], gap_staggered=d['gap_staggered'])
    for k in KEYS:
        out[k] = d[k][edge].sum() / d[k].sum()
    out['ratio_staggered'] = d['ldos_staggered'].max() / d['ldos_haldane'].max()
    out['bulk_ratio'] = np.median(d['ldos_haldane'][~edge]) / np.median(d['ldos_haldane'][edge])
    print({k: round(float(v), 3) for k, v in out.items()})
    assert out['sites'] == 834
    assert abs(out['gap_haldane'] - 0.9) < 0.01 and abs(out['gap_staggered'] - 1.0) < 0.01
    # add_haldane(0.1) of pyqula is a second-neighbor hopping 0.087, from the gap 6 sqrt(3) t2 of the Haldane model
    assert abs(out['gap_haldane'] / (6 * np.sqrt(3)) - 0.087) < 0.0005
    assert 0.33 < out['edge_sites'] < 0.36                      # 35 percent of the sites are in the boundary region
    assert 0.68 < out['ldos_haldane'] < 0.72                    # 70 percent of the weight is there
    assert 0.36 < out['ldos_metal'] < 0.38                      # 37 percent in the metal, close to the share of the sites
    assert out['ratio_staggered'] < 0.1                         # the trivial flake has less than a tenth of the weight
    out['tail'] = d['ldos_staggered'].sum() / d['ldos_haldane'].sum()
    assert 0.3 < out['tail'] < 0.4, out['tail']                # the tail of the bands alone is a third of the total weight
    return out


def draw(script, key):
    """One picture option, the map of one flake with its axes, in units of the first-neighbor distance a, and no other text."""
    plt.rcParams.update({'savefig.dpi': 220})        # the dots are one small image, so that the SVG stays light
    d = style.run_script('session03/g1_flakes.py')
    check(d)
    x, y = d['x'] - d['x'].mean(), d['y'] - d['y'].mean()
    vmax = d['ldos_haldane'].max()                       # the same scale in the three maps, the metal saturates
    w = np.clip(d[key] / vmax, 0, 1)
    fig, ax = plt.subplots(figsize=(4.4 * style.CM, 4.4 * style.CM))
    lev = np.digitize(w, [0.12, 0.3, 0.5, 0.75])        # five sizes and five colors
    cmap = plt.get_cmap('Blues')
    for L, ms, c in ((0, 1.3, 0.22), (1, 2.0, 0.45), (2, 2.7, 0.62), (3, 3.3, 0.8), (4, 3.9, 0.97)):
        ax.plot(x[lev == L], y[lev == L], 'o', ms=ms, color=cmap(c), mec='none', rasterized=True)
    R = 1.08 * max(np.abs(x).max(), np.abs(y).max())
    ax.set_xlim(-R, R); ax.set_ylim(-R, R); ax.set_aspect('equal')
    style.arrows(ax, ticks=True)
    ax.set_xticks([-10, 0, 10]); ax.set_yticks([-10, 0, 10])
    ax.set_xticklabels(['$-10$', '0', '10'], fontsize=10); ax.set_yticklabels(['$-10$', '0', '10'], fontsize=10)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$x/a$', fontsize=12, labelpad=1); ax.set_ylabel(r'$y/a$', fontsize=12, labelpad=0)
    style.save(fig, script)
