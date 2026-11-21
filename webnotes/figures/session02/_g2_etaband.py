"""Shared code of the picture options of the quiz of Section 2.5 on the band of (2.9) with t=1 and three values of eta.

The bands come from the pyqula script webnotes/scripts/session02/g2_chain_second_neighbor.py, with tij=[-1., -eta],
the sign of (2.5). The three pictures share the scale of both axes and have no other text. The feedback of the quiz
quotes the curvature at phi=pi, -2t+8 eta, which is -2, -0.4 and 2, and for eta=0.5 the dip of 0.5 below the two
maxima at cos(phi)=-1/2, all asserted here. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

CURVATURE = {0.0: -2.0, 0.2: -0.4, 0.5: 2.0}


def option(script, eta):
    """One picture option, the band for this eta, with its axes and no other text."""
    d = style.run_script('session02/g2_chain_second_neighbor.py')
    p, bands = d['phi'], d['bands']
    for x, e in bands.items():
        assert np.allclose(e, -2 * np.cos(p) - 2 * x * np.cos(2 * p), atol=1e-12)
        dp = p[1] - p[0]                                   # the curvature at phi=pi from the pyqula band
        curv = (e[-2] - 2 * e[-1] + (e[1] if np.isclose(e[0], e[-1]) else e[-1])) / dp ** 2
        assert abs(curv - CURVATURE[x]) < 1e-3, (x, curv)
        assert np.isclose(-2 + 8 * x, CURVATURE[x])
    e5 = bands[0.5]
    assert np.isclose(e5.max() - e5[-1], 0.5, atol=1e-4) and np.isclose(np.cos(p[np.argmax(e5)]), -0.5, atol=0.01)
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.9 * style.CM))
    ax.plot(p, bands[eta], color=style.ACCENT, lw=1.8, clip_on=False)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.axhline(0, color=style.GRID, lw=0.8, zorder=0)
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-3.2, 2.4)
    ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', r'$0$', r'$\pi$'], fontsize=11)
    ax.set_yticks([-2, 0, 2]); ax.set_yticklabels(['$-2$', '$0$', '$2$'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$\varphi$', fontsize=12, labelpad=0); ax.set_ylabel(r'$\epsilon/t$', fontsize=12, labelpad=-2)
    style.save(fig, script)
