"""Shared code of the picture options of the quiz of Section 3.10b, the bands of three honeycomb ribbons with the same gap.

The data come from the downloadable script webnotes/scripts/session03/g3_haldane_ribbons.py, which calls pyqula. The
ribbons have armchair edges and are 20 cells wide. The first has the Haldane coupling 0.1 of pyqula, whose mass at the
Dirac points is m_H = 0.45 (the gap of the infinite lattice is 0.9, checked below, so this coupling is 4.5 times the
mass and not 3 sqrt(3) times). The second has only the sublattice imbalance M = 0.45, and the third has the Haldane
coupling 0.1 and M = 0.9, with the valley masses 1.35 and 0.45. All three have the bulk gap 0.9, and only the first
has a Chern number different from zero. The color of a state is its position across the ribbon, blue at one edge,
grey in the middle and red at the other edge. A picture has its axes and no other text. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import style

CMAP = LinearSegmentedColormap.from_list('edge', [style.ACCENT, '#b9b9b9', style.BROKEN])
MH = 0.45          # the mass of the Haldane coupling 0.1 of pyqula


def check(d):
    """The numbers that the feedback of the quiz quotes, checked on the data of the pyqula script."""
    assert d['haldane'] == [0.1, 0., 0.1] and d['imbalance'] == [0., 0.45, 0.9]
    # the same bulk gap 0.9 in the three lattices, which is 2 min |M + m_H|, |M - m_H| with m_H = 0.45
    for g, t2, M in zip(d['bulk_gap'], d['haldane'], d['imbalance']):
        mh = MH * t2 / 0.1
        assert abs(g - 0.9) < 1e-6 and abs(g - 2 * min(abs(M + mh), abs(M - mh))) < 1e-6, g
    C = np.array(d['chern'])
    assert abs(abs(C[0]) - 1) < 1e-6 and abs(C[1]) < 1e-6 and abs(C[2]) < 1e-6, C
    # the smallest |E| of each ribbon: the edge states cross zero in the first, the gap is empty in the other two
    low = [np.abs(E).min() for E in d['energies']]
    # (the k-mesh of the script has no point at k=0, where the two branches cross, so the first is small and not zero)
    assert low[0] < 0.02 and low[1] > 0.45 and low[2] > 0.45, low
    # in the first ribbon the states inside the gap sit at the two edges
    E, Y = d['energies'][0], d['positions'][0]
    ymax = np.abs(Y).max()
    assert np.all(np.abs(Y[np.abs(E) < 0.3]) > 0.9 * ymax)
    print('bulk gaps', np.round(d['bulk_gap'], 4), 'Chern', np.round(C, 3), 'smallest |E| of the ribbons', np.round(low, 4))


def option(script, d, i):
    """One picture option, the bands of the ribbon number i."""
    plt.rcParams.update({'savefig.dpi': 300})
    check(d)
    ks = 2 * np.pi * d['ks']
    E, Y = d['energies'][i], d['positions'][i]
    clim = np.abs(d['positions'][0]).max()
    sel = np.abs(E) < 1.6
    K = np.repeat(ks[:, None], E.shape[1], axis=1)
    order = np.argsort(np.abs(Y[sel]))                              # the edge states are drawn last, on top of the bulk
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    ax.scatter(K[sel][order], E[sel][order], c=Y[sel][order], cmap=CMAP, vmin=-clim, vmax=clim, s=1.6, lw=0,
               rasterized=True)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-1.5, 1.5)
    ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=11)
    ax.set_yticks([-1, 0, 1]); ax.set_yticklabels(['$-1$', '0', '1'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$k$', fontsize=12, labelpad=1); ax.set_ylabel(r'$E/t$', fontsize=12, labelpad=-4)
    style.save(fig, script)
