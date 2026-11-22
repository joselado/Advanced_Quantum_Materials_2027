"""Shared code of the ribbon figures of Section 5.14, the BdG spectrum of a ribbon of the triangular lattice with s-wave,
chiral p-wave and nodal f-wave pairing, colored by the position of each state across the ribbon.

The data come from the downloadable script webnotes/scripts/session05/g4_pwave_ribbon.py, which calls pyqula. It is the
model of the notebook cells "Trivial and topological superconducting order parameters", the triangular lattice with the
hopping +1 of pyqula, add_onsite(-3.0), which is mu = 3 and leaves a pocket of empty states around Gamma (the band is 6 at
Gamma), and add_pairing(mode=..., delta=0.4) for the three modes. The ribbon is ribbon.bulk2ribbon(g, n=20), 20 sites
across and periodic along x with the period 1, so the momentum k = 2 pi ks is in units of the inverse lattice constant.

check() asserts on these data what the caption and the quiz feedback state. The numbers of the bulk, the smallest energy
1.34 of the chiral p-wave and the nodes of the f-wave, are asserted in webnotes/checks/session05/g4_14_chiral_topology.py.
The color is blue at the edge y < 0, grey in the middle and red at the edge y > 0, as in the ribbon figures of Session 3.
This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import style

CMAP = LinearSegmentedColormap.from_list('edge', [style.ACCENT, '#b9b9b9', style.BROKEN])
YMAX = 8.2            # the edges of the ribbon are at y = -8.23 and 8.23, in units of the lattice constant
ELIM = 3.0            # the energy window of the pictures, in units of the hopping


def load(d):
    """The variables of the pyqula script, from style.run_script('session05/g4_pwave_ribbon.py') in the figure script,
    with the momentum k in units of the inverse lattice constant added."""
    d['k'] = 2 * np.pi * np.asarray(d['ks'])
    return d


def crossings(k, E, Y, level):
    """(momentum, sign of the slope, position) of every band that crosses the energy level between two momenta."""
    out = []
    for n in range(E.shape[1]):
        e = E[:, n]
        for j in np.where(np.diff(np.sign(e - level)) != 0)[0]:
            out.append((k[j], np.sign(e[j + 1] - e[j]), 0.5 * (Y[j, n] + Y[j + 1, n])))
    return out


def check(d):
    """The statements of the caption and of the quiz, on the data of the pyqula script."""
    assert d['modes'] == ['swave', 'chiral_pwave', 'nodal_fwave']
    k, nk = d['k'], d['nk']
    assert nk % 2 == 0 and abs(k[nk // 2]) < 1e-12 and abs(d['width'] / 2 - 8.227) < 1e-3   # k = 0 is on the mesh
    assert all(E.shape == (nk, 4 * 20) for E in d['energies'])                  # 20 sites, four BdG states each
    Es, Ys = d['energies'], d['positions']
    for E in Es:                                    # each state comes with its partner at -E
        assert np.allclose(np.sort(E, axis=1), -np.sort(E, axis=1)[:, ::-1], atol=1e-9)
    # the Chern numbers of the bulk that the caption quotes, from h.get_chern()
    C = np.array(d['cherns'], float)
    assert abs(C[0]) < 1e-6 and abs(C[1] + 2) < 1e-6, C
    # (a) s-wave: the gap of the ribbon is empty, and its smallest energy is 0.40, the Delta of the bulk
    lows = Es[0]
    assert abs(np.abs(lows).min() - 0.40) < 1e-3, np.abs(lows).min()
    # (b) chiral p-wave: the states inside the bulk gap sit at the two edges, away from k = 0 where the edges mix
    E, Y = Es[1], Ys[1]
    inside = (np.abs(E) < 1.0) & (np.abs(k)[:, None] > 0.15)
    assert inside.sum() > 0 and np.all(np.abs(Y[inside]) > 0.6 * YMAX), np.abs(Y[inside]).min()
    # at energies inside the gap, two branches at the edge y > 0 go down with k and two at the edge y < 0 go up
    for level in (0.1, 0.3, 0.5, 0.8, -0.5):
        c = crossings(k, E, Y, level)
        top = [x for x in c if x[2] > 0]; bottom = [x for x in c if x[2] < 0]
        assert len(c) == 4 and len(top) == 2 and len(bottom) == 2, (level, c)
        assert all(x[1] < 0 for x in top) and all(x[1] > 0 for x in bottom), (level, c)
    # the branches of the two edges meet at k = 0, where the states mix the two edges, at +-0.0012 for this width
    assert abs(np.abs(E[nk // 2]).min() - 0.0012) < 1e-4, np.abs(E[nk // 2]).min()
    # nodal f-wave: no state sits at an edge, and the bulk states come close to zero at k = 0 and k = +-1.32
    E, Y = Es[2], Ys[2]
    assert np.abs(Y).max() < 0.5 * YMAX, np.abs(Y).max()
    low = np.abs(E).min(axis=1)
    for k0 in (-1.318, 0.0, 1.318):
        near = np.abs(k - k0) < 0.1
        assert low[near].min() < 0.12, (k0, low[near].min())
    assert low.min() < 0.1 and np.abs(Es[0]).min() > 3.5 * low.min()
    print('Chern', np.round(C, 6), 'smallest |E|: s-wave', round(np.abs(lows).min(), 4), 'chiral at k=0',
          round(np.abs(Es[1][nk // 2]).min(), 5), 'f-wave', round(low.min(), 4))


def draw(ax, d, i, lw=1.6):
    """The bands of the pairing number i, colored by the position across the ribbon."""
    k, E, Y = d['k'], d['energies'][i], d['positions'][i]
    segs, cols = [], []
    for n in range(E.shape[1]):
        if np.abs(E[:, n]).min() > ELIM + 0.1:
            continue
        p = np.column_stack([k, E[:, n]])
        segs.append(np.stack([p[:-1], p[1:]], axis=1))
        cols.append(0.5 * (Y[:-1, n] + Y[1:, n]))
    segs, cols = np.concatenate(segs), np.concatenate(cols)
    order = np.argsort(np.abs(cols))                 # the edge states are drawn last, on top of the bulk
    lc = LineCollection(segs[order], array=cols[order], cmap=CMAP, lw=lw, capstyle='round', rasterized=True)
    lc.set_clim(-YMAX, YMAX)
    ax.add_collection(lc)
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-ELIM, ELIM)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'])
    ax.tick_params(length=2.5, width=0.6, pad=2)
    return lc


def option(script, d, i):
    """One picture option of the quiz, the ribbon with the pairing number i of the data d of load, with its axes and no
    other text."""
    plt.rcParams.update({'savefig.dpi': 200})
    check(d)
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    draw(ax, d, i, lw=1.2)
    ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=11)
    ax.set_yticks([-2, 0, 2]); ax.set_yticklabels(['$-2$', '0', '2'], fontsize=11)
    ax.set_xlabel(r'$k$', fontsize=12, labelpad=1); ax.set_ylabel(r'$E/t$', fontsize=12, labelpad=-4)
    style.save(fig, script)
