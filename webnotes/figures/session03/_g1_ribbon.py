"""Shared code of the figures of the quiz of Section 3.6 on the reversal of the magnetic field.

The data come from the downloadable script webnotes/scripts/session03/g1_qh_ribbon.py, which calls pyqula. It is the
ribbon of the triangular lattice of the notebook cell "From electrons in a ribbon to the quantum Hall state", 20 cells
wide, with the fields 0.04, -0.04 and 0 of add_orbital_magnetic_field. The color of a state is its position y across
the ribbon, blue at the edge y<0, grey in the middle and red at the edge y>0. Only relative statements are checked
and drawn: the two edges have opposite slopes, and the reversal of the field exchanges them. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import style

CMAP = LinearSegmentedColormap.from_list('edge', [style.ACCENT, '#b9b9b9', style.BROKEN])
EMIN, EMAX = -2.1, 0.75
YMAX = 9.0


def crossings(E, Y, ks, mu):
    """(momentum, sign of the slope, position) of every band that crosses the energy mu."""
    out = []
    for n in range(E.shape[1]):
        e = E[:, n]
        for j in np.where(np.diff(np.sign(e - mu)) != 0)[0]:
            out.append((ks[j], np.sign(e[j + 1] - e[j]), Y[j, n]))
    return out


def check(d):
    """The statements of the quiz, checked on the data of the pyqula script."""
    Bs, ks, E, Y = d['Bs'], d['ks'], d['energies'], d['positions']
    assert Bs[0] == -Bs[1] and Bs[0] != 0 and Bs[2] == 0
    mid = len(ks) // 2
    lev = E[0][mid, :4]
    print('flat levels at k=0', np.round(lev, 3), 'the same for the opposite field', np.round(E[1][mid, :4], 3))
    for n in range(3):                                   # the lowest levels are flat in the middle of the zone
        assert np.ptp(E[0][mid - 30:mid + 31, n]) < 0.01
    assert np.allclose(E[0], E[1], atol=1e-6)            # the energies do not change with the sign of the field
    for g in range(3):                                   # the gap above the level g has g+1 modes at each edge
        mu = 0.5 * (lev[g] + lev[g + 1])
        cp, cm = crossings(E[0], Y[0], ks, mu), crossings(E[1], Y[1], ks, mu)
        top = [c for c in cp if c[2] > 5]; bot = [c for c in cp if c[2] < -5]
        assert len(cp) == 2 * (g + 1) and len(top) == g + 1 and len(bot) == g + 1, (g, cp)
        assert len(set(c[1] for c in top)) == 1 and len(set(c[1] for c in bot)) == 1      # one direction at each edge
        assert top[0][1] == -bot[0][1]                                                   # opposite on the two edges
        topm = [c for c in cm if c[2] > 5]
        assert len(topm) == g + 1 and topm[0][1] == -top[0][1]                           # reversed by the field
        print('gap', g + 1, 'modes at each edge', len(top), 'slope at the edge y>0:', top[0][1], 'for B and',
              topm[0][1], 'for -B')
    # without the field no band is flat and no state sits at an edge
    assert np.abs(Y[2]).max() < 1 and np.ptp(E[2][mid - 30:mid + 31, 0]) > 0.02
    return lev


def draw(ax, d, i, lw=1.6):
    """The bands of the field number i, colored by the position across the ribbon."""
    ks = 2 * np.pi * d['ks']
    E, Y = d['energies'][i], d['positions'][i]
    segs, cols = [], []
    for n in range(E.shape[1]):
        if E[:, n].min() > EMAX + 0.05:
            continue
        p = np.column_stack([ks, E[:, n]])
        segs.append(np.stack([p[:-1], p[1:]], axis=1))
        cols.append(0.5 * (Y[:-1, n] + Y[1:, n]))
    lc = LineCollection(np.concatenate(segs), array=np.concatenate(cols), cmap=CMAP, lw=lw, capstyle='round',
                        rasterized=True)
    lc.set_clim(-YMAX, YMAX)
    ax.add_collection(lc)
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(EMIN, EMAX)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    return lc


def option(script, i):
    """One picture option, the ribbon with the field number i, with its axes and no other text."""
    plt.rcParams.update({'savefig.dpi': 300})
    d = style.run_script('session03/g1_qh_ribbon.py')
    check(d)
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    draw(ax, d, i, lw=1.3)
    ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=11)
    ax.set_yticks([-2, -1, 0]); ax.set_yticklabels(['$-2$', '', '$0$'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$k$', fontsize=12, labelpad=1); ax.set_ylabel(r'$E/t$', fontsize=12, labelpad=-7)
    style.save(fig, script)
