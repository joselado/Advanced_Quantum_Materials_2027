"""Shared code of the ribbon figures of Section 4.11: lattice_ribbons and the three pictures of its quiz.

The data come from the downloadable script webnotes/scripts/session04/g3_ribbons_in_field.py, which calls pyqula. pyqula
builds a ribbon periodic along x and finite along y, so its momentum k along the ribbon plays the role of the k_y of the
pages, and y is the position across it. The square ribbon is 40 sites wide with the hopping -1 and the flux 0.02 per
plaquette. The honeycomb ribbon is the armchair ribbon of width 30, 51 bond lengths across, with the flux 0.005 per unit
area, with and without the field. The color of a state is its mean position y divided by the position of the edge,
blue at the edge y<0, grey in the middle and red at the edge y>0. check() asserts every number that the caption of
lattice_ribbons and the feedback of the quiz quote. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import style

CMAP = LinearSegmentedColormap.from_list('edge', [style.ACCENT, '#b9b9b9', style.BROKEN])
SQUARE_WINDOW = (-4.0, -3.2)
HONEY_WINDOW = (-0.62, 0.62)
PHI_SQUARE, PHI_HONEY = 0.02, 0.005


def crossings(E, Y, ks, mu):
    """(momentum, sign of the slope, position) of every band that crosses the energy mu."""
    out = []
    for n in range(E.shape[1]):
        e = E[:, n]
        for j in np.where(np.diff(np.sign(e - mu)) != 0)[0]:
            out.append((ks[j], np.sign(e[j + 1] - e[j]), Y[j, n]))
    return out


def edge_modes(E, Y, ks, mu, edge):
    """The number of branches that cross mu within 30 percent of the width from each edge, and their slopes."""
    c = crossings(E, Y, ks, mu)
    top = [s for (k, s, y) in c if y > 0.4 * edge]
    bot = [s for (k, s, y) in c if y < -0.4 * edge]
    assert len(top) + len(bot) == len(c), ('a crossing in the bulk', mu, c)
    return top, bot


def check(d):
    """The numbers of the caption of lattice_ribbons and of the feedback of the quiz, on the data of the pyqula script."""
    ks = d['ks']
    mid = len(ks) // 2
    assert abs(ks[mid]) < 1e-12
    # (a) the square ribbon: flat levels near the band bottom, close to -4 + 4 pi phi (n + 1/2)
    Es, Ys = d['square_energies'], d['square_positions']
    assert abs(d['square_edge'] - 19.5) < 1e-9 and Es.shape[1] == 40
    lev = np.sort(Es[mid])[:4]
    wc = 4 * np.pi * PHI_SQUARE
    cont = -4 + wc * (np.arange(4) + 0.5)
    print('square: levels', np.round(lev, 3), 'continuum', np.round(cont, 3), 'hbar omega_c', round(wc, 4),
          'spacings', np.round(np.diff(lev), 3))
    assert np.allclose(np.round(lev[:3], 2), [-3.88, -3.63, -3.40])     # the caption and the feedback
    assert abs(round(wc, 2) - 0.25) < 1e-9 and np.all(np.abs(np.diff(lev[:3]) - 0.24) < 0.006)
    assert np.all(lev < cont + 1e-9)                                     # the lattice levels sit below the lines
    assert abs((lev[0] + 4) - 0.5 * (lev[1] - lev[0])) < 0.005          # the lowest is half a spacing above -4
    for n in range(3):                                                   # flat in the middle of the zone
        assert np.ptp(np.sort(Es[mid - 40:mid + 41], axis=1)[:, n]) < 1e-3
    for g in range(2):                                                   # the gap above level g: g+1 modes per edge
        top, bot = edge_modes(Es, Ys, ks, 0.5 * (lev[g] + lev[g + 1]), d['square_edge'])
        assert len(top) == g + 1 and len(bot) == g + 1 and len(set(top)) == 1 and len(set(bot)) == 1
        assert top[0] == -bot[0]
    # (b) the honeycomb ribbon: 0 and +-sqrt(|n|) E_1, with E_1 = 3 sqrt(pi phi)
    Eh, Yh = d['honeycomb_energies'], d['honeycomb_positions']
    assert abs(d['honeycomb_edge'] - 25.5) < 0.05 and Eh.shape[1] == 120
    e = np.sort(Eh[mid])
    pos = np.unique(np.round(e[e > -1e-6], 4))[:4]
    E1 = 3 * np.sqrt(np.pi * PHI_HONEY)
    print('honeycomb: levels', pos, 'continuum', np.round(E1 * np.sqrt(np.arange(4)), 4))
    assert abs(pos[0]) < 1e-4 and np.sum(np.abs(e) < 1e-4) == 2          # the zero level, two states, one per valley
    assert abs(round(pos[1], 2) - 0.37) < 1e-9 and abs(round(pos[2], 2) - 0.52) < 1e-9
    assert abs(round(E1, 2) - 0.38) < 1e-9 and abs(round(np.sqrt(2) * E1, 2) - 0.53) < 1e-9
    assert abs(round(pos[2] / pos[1], 2) - 1.40) < 1e-9                  # close to sqrt(2), not 2
    assert np.all(np.abs(e[(e > 0.1) & (e < 0.6)][::2] - e[(e > 0.1) & (e < 0.6)][1::2]) < 1e-3)
    for mu, nmodes in ((0.5 * pos[1], 1), (0.5 * (pos[1] + pos[2]), 3)):  # 1 mode per edge, then 3
        top, bot = edge_modes(Eh, Yh, ks, mu, d['honeycomb_edge'])
        assert len(top) == nmodes and len(bot) == nmodes and len(set(top)) == 1 and len(set(bot)) == 1, (mu, top, bot)
        assert top[0] == -bot[0]
    # the same direction in the two ribbons: the branch of positive slope sits at the edge y > 0 for the same field sign
    ts, _ = edge_modes(Es, Ys, ks, 0.5 * (lev[0] + lev[1]), d['square_edge'])
    th, _ = edge_modes(Eh, Yh, ks, 0.5 * pos[1], d['honeycomb_edge'])
    assert ts[0] == th[0] == 1
    # (c) the honeycomb ribbon with no field: no flat band near zero energy
    E0 = d['nofield_energies']
    lowest = np.min(np.where(E0 > 0, E0, np.inf), axis=1)                # the band just above zero energy, at each k
    one = np.argmin(np.abs(2 * np.pi * ks - 1.0))                         # the point k a = 1
    print('no field: lowest band above zero', round(lowest[mid], 3), 'at k=0 and', round(lowest[one], 3), 'at ka=1')
    assert round(lowest[mid], 2) == 0.03 and round(lowest[one], 2) == 0.48   # the feedback of the quiz
    assert abs(lowest[one] - 0.5) < 0.03                                 # the Dirac cone, hbar v k = (3/2)(ka/3)
    assert np.all(np.ptp(np.sort(E0[:, :], axis=1)[:, 58:62], axis=0) > 0.3)  # the bands near zero are not flat
    return dict(square=lev, honeycomb=pos, E1=E1)


def draw(ax, ks, E, Y, edge, window, lw=1.5):
    """The bands, each segment colored by the position of the state across the ribbon."""
    k = 2 * np.pi * ks
    segs, cols = [], []
    for n in range(E.shape[1]):
        if E[:, n].min() > window[1] + 0.05 or E[:, n].max() < window[0] - 0.05:
            continue
        p = np.column_stack([k, E[:, n]])
        segs.append(np.stack([p[:-1], p[1:]], axis=1))
        cols.append(0.5 * (Y[:-1, n] + Y[1:, n]) / edge)
    lc = LineCollection(np.concatenate(segs), array=np.concatenate(cols), cmap=CMAP, lw=lw, capstyle='round',
                        rasterized=True)
    lc.set_clim(-1, 1)
    ax.add_collection(lc)
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(*window)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'])
    ax.tick_params(length=2.5, width=0.6)
    return lc


def option(script, which):
    """One picture option of the quiz, with its axes and no other text."""
    plt.rcParams.update({'savefig.dpi': 300, 'font.size': 11})
    d = style.run_script('session04/g3_ribbons_in_field.py')
    check(d)
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    if which == 'square':
        draw(ax, d['ks'], d['square_energies'], d['square_positions'], d['square_edge'], SQUARE_WINDOW, lw=1.3)
        ax.set_yticks([-3.88, -3.4]); ax.set_yticklabels(['$-3.88$', '$-3.40$'])
    else:
        name = 'honeycomb' if which == 'honeycomb' else 'nofield'
        draw(ax, d['ks'], d[name + '_energies'], d[name + '_positions'], d['honeycomb_edge'], HONEY_WINDOW, lw=1.3)
        if which == 'honeycomb':
            ax.set_yticks([-0.37, 0, 0.37]); ax.set_yticklabels(['$-0.37$', '0', '$0.37$'])
        else:
            ax.set_yticks([-0.5, 0, 0.5]); ax.set_yticklabels(['$-0.5$', '0', '$0.5$'])
    ax.tick_params(labelsize=10, pad=2)
    ax.set_xlabel(r'$k\,a$', fontsize=11, labelpad=1); ax.set_ylabel(r'$E/t$', fontsize=11, labelpad=1)
    style.save(fig, script)
