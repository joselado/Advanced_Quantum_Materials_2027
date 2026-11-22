"""Shared code of the magnon ribbons of Section 6.16, the figure ribbon_magnons and the three pictures of the quiz.

The data come from the downloadable script webnotes/scripts/session06/g5_magnon_ribbon.py, which calls pyqula for a ribbon of
the honeycomb ferromagnet with zigzag edges, honeycomb_zigzag_ribbon(12), 48 sites across and periodic along x. The magnon hops
with -|J|S between first neighbors, with |J|S = 1, and every site has the onsite energy 3|J|S of the bulk. The four models are
(DS, M) = (0.1, 0), (-0.1, 0), (0, 0.52), (0, 0): the Dzyaloshinskii-Moriya hopping DS of both signs, an onsite energy 2M on one
sublattice and 0 on the other, which opens a gap of the same size 1.04 with C = 0, and the plain magnet with no gap. A state is
drawn in color when it sits at an edge, |<y>| > 0.6 of the half width, and its energy is in the gap of the bulk of its model,
blue at the lower edge and red at the upper edge, so the plain magnet, with no gap, has no state in color. All the bands are
drawn in grey below. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

LOWER, UPPER = style.ACCENT, style.BROKEN
STRIP = '#ececec'                     # the gap of the bulk
WINDOW = (1.5, 4.5)                   # the energy window of all the ribbon pictures, in units of |J|S
GAP = 6 * np.sqrt(3) * 0.1            # 1.0392, the gap at K for DS = 0.1, and 2M for M = 0.52 to 1 percent


def load(d):
    """The variables of the script, from style.run_script('session06/g5_magnon_ribbon.py'), checked, with for each model its
    gap window (lo, hi) and the masks of the two edges."""
    assert [tuple(m) for m in d['models']] == [(0.1, 0.0), (-0.1, 0.0), (0.0, 0.52), (0.0, 0.0)]
    assert d['g'].r.shape[0] == 48 and abs(d['width'] - 35.0) < 1e-9          # 48 sites across, edges at y = -17.5 and 17.5
    k = np.asarray(d['momentum'], float)
    assert len(k) == d['nk'] == 201 and abs(k[100] - np.pi) < 1e-12 and abs(k[-1] - 2 * np.pi) < 1e-12
    out = []
    for (DS, M), E, Y in zip(d['models'], d['energy'], d['position']):
        E, Y = np.asarray(E, float), np.asarray(Y, float)
        assert E.shape == (201, 48) and np.all(np.diff(E, axis=1) > -1e-9)
        mid = 3.0 + M                                     # the middle of the gap of the bulk
        half = 3 * np.sqrt(3) * abs(DS) + M               # half of the gap of the bulk at K
        edge = np.abs(Y) > 0.6 * d['width'] / 2
        inside = np.abs(E - mid) < half + 1e-6 if half > 0 else np.zeros(E.shape, bool)    # no gap, nothing in color
        out.append(dict(DS=DS, M=M, E=E, Y=Y, k=k, lo=mid - half, hi=mid + half,
                        lower=edge & inside & (Y < 0), upper=edge & inside & (Y > 0)))
    assert abs(2 * 0.52 - GAP) < 0.01 * GAP
    return out


def branch_slopes(m, which, level):
    """Where the colored branch of one edge crosses the energy level: a list of (momentum, slope)."""
    E, k, sel = m['E'], m['k'], m[which]
    out = []
    for j in range(E.shape[1]):
        s = sel[:, j]
        for i in np.where(s[:-1] & s[1:] & (np.sign(E[:-1, j] - level) != np.sign(E[1:, j] - level)))[0]:
            out.append((k[i], (E[i + 1, j] - E[i, j]) / (k[i + 1] - k[i])))
    return out


def draw(ax, m, ms=1.6):
    """The bands of one model in grey, the gap of the bulk as a strip, and the states of the two edges in color."""
    E, k = m['E'], m['k']
    if m['hi'] > m['lo']:
        ax.axhspan(m['lo'], m['hi'], color=STRIP, lw=0, zorder=0)
    ax.plot(k, E, color='#c4c4c4', lw=0.5, zorder=1, rasterized=True)
    K = np.repeat(k[:, None], E.shape[1], axis=1)
    for which, col in (('lower', LOWER), ('upper', UPPER)):
        sel = m[which]
        ax.plot(K[sel], E[sel], 'o', ms=ms, color=col, mec='none', zorder=3, rasterized=True)
    ax.set_xlim(0, 2 * np.pi); ax.set_ylim(*WINDOW)


def option(script, m):
    """One picture of the quiz, with its axes and no other text."""
    plt.rcParams.update({'savefig.dpi': 220})
    fig, ax = plt.subplots(figsize=(3.2 * style.CM, 3.6 * style.CM))
    draw(ax, m)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    ax.set_xticks([0, np.pi, 2 * np.pi]); ax.set_xticklabels(['0', r'$\pi$', r'$2\pi$'], fontsize=11)
    ax.set_yticks([2, 3, 4]); ax.set_yticklabels(['2', '3', '4'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$k$', fontsize=12, labelpad=0); ax.set_ylabel(r'$E/|J|S$', fontsize=12, labelpad=1)
    style.save(fig, script)
