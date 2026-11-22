"""Shared code of the BdG band plots of Sections 5.8 and 5.9, the bands of a superconductor colored by their electron weight.

The data come from the downloadable scripts webnotes/scripts/session05/g2_*.py, which call pyqula. Each script returns, for
every Delta or every chemical potential, the four BdG energies at each step of a k-path, sorted, and the electron weight of each
state, which is its weight on the first two entries (c_up, c_dn) of the Nambu spinor (5.6), from 0 to 1. The four bands come in
two degenerate pairs, one from each of the two identical blocks (5.8), so only the bands 1 and 2 of the four are drawn, one
of each pair. The color goes from the red style.BROKEN of a hole (weight 0) to the dark blue style.ACCENT of an electron
(weight 1). A line is cut into pieces of the same color, with 24 levels of the weight, so that the SVG stays small.
This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable
import style

EH = LinearSegmentedColormap.from_list('electron_hole', [style.BROKEN, style.ACCENT])
LEVELS = 24


def check(energies, weights):
    """The checks of what every BdG plot shows: sorted energies, pairs +E and -E, the two degenerate pairs, weights in [0, 1],
    and the electron weight of +E and of -E adding up to one, as u^2 and v^2 do."""
    e, w = np.asarray(energies), np.asarray(weights)
    assert e.shape == w.shape and e.shape[1] == 4
    assert np.all(np.diff(e, axis=1) > -1e-9)                                   # sorted at each momentum
    assert np.allclose(e[:, 0], e[:, 1], atol=1e-7) and np.allclose(e[:, 2], e[:, 3], atol=1e-7)
    assert np.allclose(e[:, 0], -e[:, 3], atol=1e-9)                           # particle-hole pairs
    assert w.min() > -1e-9 and w.max() < 1 + 1e-9
    gapped = np.abs(e[:, 2]) > 1e-3                                             # away from a crossing of Delta=0
    assert np.allclose((w[:, 1] + w[:, 2])[gapped], 1, atol=1e-6)


def colored(ax, x, y, w, lw=1.9):
    """A curve y(x) whose color is the electron weight w, as pieces of constant color."""
    x, y, w = map(np.asarray, (x, y, w))
    lev = np.clip(np.round(w * (LEVELS - 1)), 0, LEVELS - 1).astype(int)
    cut = np.where(np.diff(lev) != 0)[0] + 1
    starts = np.r_[0, cut]
    ends = np.r_[cut, len(x) - 1]
    segs, cols = [], []
    for a, b in zip(starts, ends):
        segs.append(np.c_[x[a:b + 1], y[a:b + 1]])
        cols.append(EH(lev[a] / (LEVELS - 1)))
    ax.add_collection(LineCollection(segs, colors=cols, linewidths=lw, capstyle='round', joinstyle='round'))


def bands(ax, x, energies, weights, lw=1.9):
    """The bands 1 and 2 of the four BdG bands, one of each degenerate pair, colored by the electron weight."""
    for n in (1, 2):
        colored(ax, x, energies[:, n], weights[:, n], lw=lw)


def path_x(kpath, B):
    """The distance along a k-path given in units of the reciprocal vectors (rows of B), and the steps of its corners."""
    k = np.asarray(kpath, float)[:, :2] @ np.asarray(B, float)
    x = np.r_[0, np.cumsum(np.linalg.norm(np.diff(k, axis=0), axis=1))]
    return x


def colorbar(fig, ax, fontsize=10):
    """A colorbar of the electron weight, from 0 (hole) to 1 (electron), next to the axes ax."""
    sm = ScalarMappable(norm=Normalize(0, 1), cmap=EH)
    cb = fig.colorbar(sm, ax=ax, fraction=0.05, pad=0.04, aspect=14, ticks=[0, 0.5, 1])
    cb.ax.set_yticklabels(['0', '0.5', '1'], fontsize=fontsize)
    cb.set_label('electron weight', fontsize=fontsize, labelpad=2)
    cb.outline.set_linewidth(0.5)
    cb.ax.tick_params(length=2, width=0.5)
    return cb


def frame(ax, xticks, yticks, xlabel, ylabel, fontsize=11.5):
    """Left and bottom axes with ticks and names, no box on the top and the right."""
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_linewidth(0.6)
    ax.set_xticks([t for t, _ in xticks]); ax.set_xticklabels([l for _, l in xticks], fontsize=fontsize)
    ax.set_yticks([t for t, _ in yticks]); ax.set_yticklabels([l for _, l in yticks], fontsize=fontsize)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=fontsize + 0.5, labelpad=1)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=fontsize + 0.5, labelpad=1)


def square_option(script, i):
    """A picture option of the quiz of Section 5.8, the BdG bands of the square lattice for the Delta number i of the script
    webnotes/scripts/session05/g2_nambu_square.py (0, 0.2, 0.4, 0.8), with its axes and no other text. The energy window and the
    ticks at -0.8 and 0.8 are the same in the three pictures."""
    d = style.run_script('session05/g2_nambu_square.py')
    D, e, w = d['deltas'][i], d['energies'][i], d['weights'][i]
    check(e, w)
    kp = np.array(d['kpath'])
    k = 2 * np.pi * kp[:, :2]
    eps = 2 * (np.cos(k[:, 0]) + np.cos(k[:, 1])) + d['onsite']
    assert np.allclose(e[:, 2], np.sqrt(eps**2 + D**2), atol=1e-9)
    cross = np.where(np.diff(np.sign(eps)) != 0)[0]
    near = [np.min(e[c - 5:c + 6, 2]) for c in cross]
    assert len(cross) == 2 and np.allclose(near, D, atol=2e-3)              # the branches come closest at +-Delta, at both crossings
    apart = [np.min(e[c - 5:c + 6, 2] - e[c - 5:c + 6, 1]) for c in cross]   # the two drawn branches, bands 1 and 2
    assert np.allclose(apart, 2 * D, atol=4e-3)                             # 2|Delta| apart: 0.4, 0.8, 1.6 for Delta 0.2, 0.4, 0.8
    print('Delta', D, 'smallest |E| at the two crossings', np.round(near, 4), 'gap between the branches', np.round(apart, 4))
    x = path_x(kp, 2 * np.pi * np.eye(2))
    corners = [0, 150, 300, 450]
    plt.rcParams.update({'font.size': 11})
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    style.guide(ax, y=0, lw=0.7)
    bands(ax, x, e, w, lw=1.6)
    ax.set_xlim(0, x[-1]); ax.set_ylim(-1.9, 1.9)
    frame(ax, [(x[c], l) for c, l in zip(corners, (r'$\Gamma$', r'$X$', r'$M$', r'$\Gamma$'))],
          [(-0.8, '$-0.8$'), (0.8, '$0.8$')], r'$\mathbf{k}$', r'$E/|t|$', fontsize=11)
    ax.yaxis.labelpad = -1
    style.save(fig, script)
