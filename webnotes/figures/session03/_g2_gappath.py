"""Shared code of the picture options of the quiz of Section 3.7, the bulk gap along a deformation.

The data come from the pyqula script webnotes/scripts/session03/g2_gap_paths.py. The model is the honeycomb lattice with
the Haldane coupling add_haldane(0.1) of pyqula, which alone opens the gap 0.90 (pyqula normalizes the coupling so that
the gap is 9 times its argument, and not 6 sqrt(3) times), and a staggered potential M that changes linearly with the
parameter lambda of the deformation. The gap is 2|M - 0.45|, so it closes at M = 0.45, half of the gap of the Haldane
coupling, and the size of the Chern number is 1 for M<0.45 and 0 for M>0.45. The three paths go from 0 to 0.36, from 0 to
0.90 and from 0.54 to 0.90. Only the size of the Chern number is used. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

# for each path: the gap at the start, the smallest gap, the gap at the end, |C| at the start and at the end
EXPECT = [(0.90, 0.18, 0.18, 1, 1), (0.90, 0.0, 0.90, 1, 0), (0.18, 0.18, 0.90, 0, 0)]
MRANGE = [(0.0, 0.36), (0.0, 0.90), (0.54, 0.90)]


def option(script, i):
    """One picture option, the gap along the path number i, with its axes and no other text."""
    d = style.run_script('session03/g2_gap_paths.py')
    lam, mc = d['lambdas'], d['m_closing']
    assert abs(d['gap_haldane'] - 0.90) < 1e-3 and abs(mc - 0.45) < 1e-3
    for j, (g, c, ex) in enumerate(zip(d['gaps'], d['cherns'], EXPECT)):
        M = d['m_start'][j] + lam * (d['m_end'][j] - d['m_start'][j])
        assert np.allclose(g, 2 * np.abs(M - mc), atol=2e-3), np.abs(g - 2 * np.abs(M - mc)).max()
        assert np.allclose((M[0], M[-1]), MRANGE[j], atol=1e-3)
        got = (g[0], g.min(), g[-1], abs(c[0]), abs(c[1]))
        print('path', j, 'gap start, min, end', np.round(got[:3], 3), 'C start, end', np.round(c, 4),
              'M from', round(M[0], 3), 'to', round(M[-1], 3), 'closes at lambda', lam[np.argmin(g)])
        assert np.allclose(got, ex, atol=2e-3), (got, ex)
    assert lam[np.argmin(d['gaps'][1])] == 0.5
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    ax.plot(lam, d['gaps'][i], color=style.ACCENT, lw=1.8, clip_on=False)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.05)
    ax.set_xticks([0, 0.5, 1]); ax.set_xticklabels(['0', '0.5', '1'], fontsize=11)
    ax.set_yticks([0, 0.5, 1]); ax.set_yticklabels(['0', '', '1'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$\lambda$', fontsize=12, labelpad=0); ax.set_ylabel(r'gap$/t$', fontsize=12, labelpad=-4)
    style.save(fig, script)
