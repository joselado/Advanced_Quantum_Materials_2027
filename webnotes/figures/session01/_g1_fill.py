"""Shared code of the band fillings of Section 1.2, the figure filling_bands and the three picture options of the
quiz "Which picture shows an n-doped semiconductor?". This file writes no figure.

The bands come from the downloadable script webnotes/scripts/session01/g1_chain_bands.py: the chain with one site per
cell and tij=[-1.], whose band is -2t cos k, and the chain with two sites per cell (geometry.bichain) with the same
hopping and add_sublattice_imbalance(0.6), whose bands are +-sqrt(m^2 + 4t^2 cos^2 k) with m = 0.6. The momentum k is
per site, from -pi to pi, so it covers two zones of the cell of two sites, whose edges k = +-pi/2 are drawn dashed.
The energies are in units of t. The Fermi levels are 0 for the metal and the insulator and +-(m + 0.35) = +-0.95 for
the doped chains, the values of the old script. check() asserts every number that the caption and the feedback quote."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

M = 0.6                       # the onsite energies +-m of the chain with two sites per cell
EF = {'metal': 0.0, 'insulator': 0.0, 'n': M + 0.35, 'p': -(M + 0.35)}


def data():
    return style.run_script('session01/g1_chain_bands.py')


def check(d=None):
    """The numbers of the caption of filling_bands and of the feedback of the picture quiz."""
    d = data() if d is None else d
    k, metal, bands = np.array(d['k']), np.array(d['metal']), np.array(d['bands'])
    E = np.sqrt(M ** 2 + 4 * np.cos(k) ** 2)
    assert np.allclose(metal, -2 * np.cos(k), atol=1e-12)                    # the metal is -2t cos k
    assert np.allclose(bands[:, 0], -E, atol=1e-12) and np.allclose(bands[:, 1], E, atol=1e-12)
    assert abs(d['gap'] - 2 * M) < 1e-12 and abs(d['gap'] - 1.2) < 1e-12      # the gap 2m = 1.2t
    edge = np.argmin(np.abs(np.abs(k) - np.pi / 2))
    assert abs(abs(k[edge]) - np.pi / 2) < 1e-12 and abs(bands[edge, 1] - 0.6) < 1e-12   # at k = +-pi/2
    assert abs(bands[:, 1].max() - 2.088) < 1e-3 and abs(np.sqrt(M ** 2 + 4) - 2.088) < 1e-3   # band top 2.09t
    assert abs(EF['n'] - 0.95) < 1e-12 and abs(EF['p'] + 0.95) < 1e-12
    # the metal at E_F = 0 has its states filled for |k| < pi/2, half of the band
    filled = np.abs(k) < np.pi / 2
    assert np.all(metal[filled] < 0) and np.all(metal[np.abs(k) > np.pi / 2] > 0)
    # E_F = 0.95t is above the bottom 0.6t of the conduction band and below its top, so a part of it is filled
    nfill = (bands[:, 1] < EF['n']).mean()
    assert 0.6 < EF['n'] < bands[:, 1].max() and 0.1 < nfill < 0.5
    # E_F = 0 lies inside the gap, between -0.6t and 0.6t, so the valence band is full and the conduction band empty
    assert bands[:, 0].max() < EF['insulator'] < bands[:, 1].min()
    print('filling: gap', round(float(d['gap']), 6), 'band top', round(float(bands[:, 1].max()), 4),
          'E_F of the doped chains', EF['n'], EF['p'], 'filled part of the conduction band at E_F = 0.95', round(nfill, 3))
    return d


def draw(ax, d, kind, carriers=True, lw=1.8, zone=True):
    """One filling on the axes ax. kind is 'metal', 'insulator', 'n' or 'p'. The filled states are blue and thick,
    the empty states grey, and with carriers=True the electrons of a conduction band and the holes of a valence band
    are red. The Fermi level is the red dashed line, and with zone=True the zone edges k = +-pi/2 of the chain with two
    sites per cell are dotted."""
    k, ef = np.array(d['k']), EF[kind]
    if kind == 'metal':
        bands = [np.array(d['metal'])]
    else:
        bands = [np.array(d['bands'])[:, 0], np.array(d['bands'])[:, 1]]
        for x in ((-np.pi / 2, np.pi / 2) if zone else ()):
            ax.axvline(x, color=style.MUTED, lw=0.7, ls=(0, (2, 2)), zorder=0)
    for j, e in enumerate(bands):
        full, empty = np.where(e <= ef, e, np.nan), np.where(e > ef, e, np.nan)
        ax.plot(k, empty, color=style.GRID, lw=lw * 0.8, zorder=1)
        hot = carriers and ((kind == 'n' and j == 1) or (kind == 'p' and j == 0))
        if hot and kind == 'n':
            ax.plot(k, full, color=style.BROKEN, lw=lw * 1.6, solid_capstyle='butt', zorder=3)
        elif hot and kind == 'p':
            ax.plot(k, full, color=style.ACCENT, lw=lw, zorder=2)
            ax.plot(k, empty, color=style.BROKEN, lw=lw * 1.6, solid_capstyle='butt', zorder=3)
        else:
            ax.plot(k, full, color=style.ACCENT, lw=lw, zorder=2)
    ax.axhline(ef, color=style.BROKEN, lw=0.9, ls=(0, (4, 3)), zorder=4)
    ax.set_xlim(-np.pi, np.pi)
    ax.set_ylim(-2.5, 2.5)


def option(script, kind):
    """One picture option, a filling with its axes and no other text."""
    d = check()
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.9 * style.CM))
    draw(ax, d, kind, carriers=False, lw=1.6, zone=False)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=11)
    ax.set_yticks([-2, -1, 0, 1, 2]); ax.set_yticklabels(['$-2$', '$-1$', '0', '1', '2'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$k$', fontsize=12, labelpad=0); ax.set_ylabel(r'$E/t$', fontsize=12, labelpad=-2)
    style.save(fig, script)
