"""Shared code of the band pictures of Section 4.20, the honeycomb lattice at zero field with a dispersive or a flat lower band.

The data come from the downloadable script webnotes/scripts/session04/g5_haldane_t3_bands.py, which calls pyqula for three models
of the honeycomb lattice with the first-neighbor hopping t=1 of pyqula, a second-neighbor hopping t2 exp(i phi), a third-neighbor
hopping t3 and a staggered potential M:
  0, the Haldane model of Section 3.10b, t2=0.1, phi=pi/2, which is h.add_haldane(0.1155), lower band of width 2.48 and gap 1.04,
  1, a flat Chern band, t2=0.3, phi=0.4 pi, t3=-0.2, which is tij=[1, 0.0927, -0.2] and h.add_haldane(0.3295), width 0.212 and
     gap 2.965, the ratio 14.0,
  2, a flat trivial band, a real t2=0.2 and M=1.5, width 0.200 and gap 3.000, with C=0 since every hopping is real.
The widths and gaps are those of the script, on a 48 x 48 mesh that holds K and K'. The Chern number is h.get_chern(), which counts
the states below zero energy, so load() checks that zero energy is in the gap of every model. The energies along the path are
shifted so that the middle of the lower band is at zero. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style, physcheck

GAP = '#ececec'                                    # the strip of the gap
NAMES = [r'$\Gamma$', r'$K$', r'$M$', r'$\Gamma$']
WINDOW = (-1.6, 7.0)                               # the energy window of the three quiz pictures, shared


def load(d):
    """The variables of the script, checked: the path, the three Chern numbers, the widths and the gaps that the page quotes."""
    models, bands = d['models'], [np.asarray(b, float) for b in d['bands']]
    W, D, C = np.array(d['width']), np.array(d['gap']), np.array(d['chern'], float)
    assert len(models) == 3 and all(b.shape == (301, 2) for b in bands)
    # the path is Gamma, K, M, Gamma: K is a corner of the zone and M the middle of the edge next to it
    B = physcheck.reciprocal([np.asarray(d['g'].a1, float)[:2], np.asarray(d['g'].a2, float)[:2]])
    Gm, K, M = [np.asarray(d['nodes'][i], float)[:2] @ B for i in range(3)]
    assert abs(np.linalg.norm(M) - np.sqrt(3) / 2 * np.linalg.norm(K)) < 1e-9 and abs((K - M) @ M) < 1e-9
    assert abs(np.linalg.norm(K) - 4 * np.pi / (3 * np.sqrt(3))) < 1e-9          # 4 pi / 3a with the lattice constant a = sqrt(3)
    assert np.allclose(bands[0][100], [-0.3 * np.sqrt(3), 0.3 * np.sqrt(3)])     # at K the Haldane mass 3 sqrt(3) t2 of t2 = 0.1
    # the Chern numbers of the lower bands, and zero energy in the gap, so that get_chern counts the lower band only
    assert np.allclose(C, [1, 1, 0], atol=1e-6), C
    for b in bands:
        assert b[:, 0].max() < 0 < b[:, 1].min()
    # the gap along the path is the gap of the mesh, so the drawn bands show the gap that the caption quotes
    for b, gap in zip(bands, D):
        assert abs(b[:, 1].min() - b[:, 0].max() - gap) < 1e-6
    # the numbers of the caption and of the quiz
    assert abs(W[0] - 2.48) < 0.005 and abs(D[0] - 1.04) < 0.005 and W[0] > 2 * D[0]       # 2.5 t, more than twice the gap
    assert abs(W[1] - 0.212) < 0.0005 and abs(D[1] - 2.965) < 0.0005 and abs(D[1] / W[1] - 14.0) < 0.05
    assert abs(W[2] - 0.200) < 0.0005 and abs(D[2] - 3.000) < 0.0005
    print('widths', np.round(W, 4), 'gaps', np.round(D, 4), 'gap/width', np.round(D / W, 2), 'C', np.round(C, 6))
    shifted = []
    for b in bands:
        mid = 0.5 * (b[:, 0].max() + b[:, 0].min())            # the middle of the lower band along the path goes to zero
        shifted.append(b - mid)
    # the width along the path is the width of the mesh, to 2 percent, so the drawn band shows the width that is quoted
    for s, w in zip(shifted, W):
        assert abs(np.ptp(s[:, 0]) - w) < 0.02 * w, (np.ptp(s[:, 0]), w)
    return dict(bands=shifted, width=W, gap=D, chern=C)


def draw(ax, b, color, fontsize=11):
    """The two bands of one model along the path, the lower one in color, the gap as a grey strip."""
    x = np.arange(len(b))
    ax.axhspan(b[:, 0].max(), b[:, 1].min(), color=GAP, lw=0, zorder=0)
    for tk in (100, 200):
        style.guide(ax, x=tk)
    ax.plot(x, b[:, 1], color=style.MUTED, lw=1.4, zorder=2)
    ax.plot(x, b[:, 0], color=color, lw=1.6, zorder=3)
    ax.set_xlim(0, len(b) - 1)
    ax.set_xticks([0, 100, 200, 300]); ax.set_xticklabels(NAMES, fontsize=fontsize)


def option(script, d, i):
    """One picture of the quiz: the model i, the lower band blue for C=1 and red for C=0, with its axes and no other text."""
    plt.rcParams.update({'savefig.dpi': 220})
    for b in d['bands']:
        assert WINDOW[0] < b.min() and b.max() < WINDOW[1]
    fig, ax = plt.subplots(figsize=(3.4 * style.CM, 3.8 * style.CM))
    color = style.ACCENT if round(d['chern'][i]) == 1 else style.BROKEN
    draw(ax, d['bands'][i], color)
    ax.set_ylim(*WINDOW)
    style.arrows(ax, ticks=True)
    ax.set_yticks([0, 2, 4, 6]); ax.set_yticklabels(['0', '2', '4', '6'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_ylabel(r'$E/t$', fontsize=12, labelpad=1)
    style.save(fig, script)
