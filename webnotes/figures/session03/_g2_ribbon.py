"""Shared code of the figures of Section 3.6b, the ribbon of the square lattice in a magnetic field.

The data come from the downloadable script webnotes/scripts/session03/g2_square_ribbon.py, which calls pyqula. The
ribbon has W=40 sites across, the hopping -t with t=1, and the flux B per plaquette in units of the flux quantum, which
is the argument of add_orbital_magnetic_field (checked against the Harper chain -2 cos(k - 2 pi B y) on each site y).
The bottom of the band is at -4t with the mass hbar^2/2ta^2, so the cyclotron energy is 4 pi B t and the flat levels
are close to -4 + 4 pi B (n + 1/2). The color of a state is its position across the ribbon, blue at the edge y<0,
grey in the middle and red at the edge y>0. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import style

CMAP = LinearSegmentedColormap.from_list('edge', [style.ACCENT, '#b9b9b9', style.BROKEN])
EMIN, EMAX = -4.0, -3.0


def check(d):
    """The numbers that the captions and the feedback quote, checked on the data of the pyqula script."""
    W, Bs, ks = d['W'], d['Bs'], d['ks']
    mid = len(ks) // 2
    out = {}
    ratios = []
    for B, E, Y in zip(Bs, d['energies'], d['positions']):
        assert np.allclose(np.sort(E, axis=1), E), 'the bands are sorted at each momentum'
        if B == 0:
            n = np.arange(1, W + 1)
            assert np.allclose(E[mid], np.sort(-2 - 2 * np.cos(np.pi * n / (W + 1))), atol=1e-9)
            out[B] = dict(bottom=E[mid, 0], width=E[:, 0].max() - E[:, 0].min())
            continue
        hw = 4 * np.pi * B
        lev = E[mid, :4]
        gaps = np.diff(lev)
        ratios.append(gaps[0] / hw)
        # the guiding center of the lowest level is y0 = k / (2 pi B) in units of a, so k>0 sits at y>0
        j = mid + 10
        assert abs(Y[j, 0] - ks[j] / B) < 0.05, (Y[j, 0], ks[j] / B)
        out[B] = dict(levels=lev, gaps=gaps, hw=hw, lB=1 / np.sqrt(2 * np.pi * B))
        print('B', B, 'levels', np.round(lev, 3), 'gaps', np.round(gaps, 3), '4 pi B', round(hw, 3),
              'first gap over 4 pi B', round(gaps[0] / hw, 3), 'l_B', round(out[B]['lB'], 2))
        assert np.all(np.abs(lev - (-4 + hw * (np.arange(4) + 0.5))) < 0.06 * (np.arange(4) + 1))
    # the spacing approaches the continuum one when the field decreases
    assert all(a > b for a, b in zip(ratios, ratios[1:])) and 0.98 < ratios[0] < 1.0, ratios
    return out


def draw(ax, d, i, lw=1.6, levels=0):
    """The bands of the field number i in the window near the bottom of the band, colored by the position."""
    W, ks = d['W'], 2 * np.pi * d['ks']
    E, Y = d['energies'][i], d['positions'][i]
    segs, cols = [], []
    for n in range(W):
        if E[:, n].min() > EMAX + 0.05:
            continue
        p = np.column_stack([ks, E[:, n]])
        segs.append(np.stack([p[:-1], p[1:]], axis=1))
        cols.append(0.5 * (Y[:-1, n] + Y[1:, n]))
    lc = LineCollection(np.concatenate(segs), array=np.concatenate(cols), cmap=CMAP, lw=lw, capstyle='round',
                        rasterized=True)
    lc.set_clim(-W / 2, W / 2)
    ax.add_collection(lc)
    for n in range(levels):
        ax.axhline(-4 + 4 * np.pi * d['Bs'][i] * (n + 0.5), color=style.INK, lw=0.7, ls=(0, (4, 3)), zorder=0)
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(EMIN, EMAX)
    return lc


def option(script, i):
    """One picture option, the ribbon with the field number i, with its axes and no other text."""
    plt.rcParams.update({'savefig.dpi': 300})
    d = style.run_script('session03/g2_square_ribbon.py')
    num = check(d)
    # the numbers of the feedback of the quiz: the first spacing and 4 pi B for the three fields, four flat bands at 0.02
    assert [round(float(num[B]['gaps'][0]), 2) for B in (0.01, 0.015, 0.02)] == [0.12, 0.18, 0.24]
    assert [round(float(num[B]['hw']), 2) for B in (0.01, 0.015, 0.02)] == [0.13, 0.19, 0.25]
    mid = len(d['ks']) // 2
    assert (d['energies'][d['Bs'].index(0.02)][mid] < EMAX).sum() == 4
    assert (d['energies'][d['Bs'].index(0.015)][mid] < EMAX).sum() == 6          # the alt text of the option
    assert d['Bs'][i] in (0.01, 0.015, 0.02)
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    draw(ax, d, i, lw=1.3)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', '', r'$\pi$'], fontsize=11)
    ax.set_yticks([-4, -3.5, -3]); ax.set_yticklabels(['$-4$', '', '$-3$'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$k$', fontsize=12, labelpad=-9); ax.set_ylabel(r'$E/t$', fontsize=12, labelpad=-9)
    style.save(fig, script)
