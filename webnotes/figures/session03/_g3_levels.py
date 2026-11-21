"""Shared code of the picture options of the quiz of Section 3.9b, the levels of three open chains of 16 sites.

The data come from the downloadable script webnotes/scripts/session03/g3_ssh_chains.py, which calls pyqula. Two chains
have the alternating hoppings 1 and t=1/2, one of them ends with a weak bond at both ends and the other with a strong
bond, and the third chain has all the hoppings equal to 1. A picture is the level E_n against its number n, with its
axes and no other text, and all the levels have the same color, so that the answer is read from the gap alone.
This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style


def check(d):
    """The numbers that the feedback of the quiz quotes, checked on the data of the pyqula script."""
    t, N = d['t'], d['N']
    weak, strong, uni = (np.sort(np.abs(d[k])) for k in ('levels_weak_ends', 'levels_strong_ends', 'levels_uniform'))
    assert len(weak) == len(strong) == len(uni) == 2 * N == 16
    # the two end states, at t^N (1 - t^2), which the feedback rounds to 0.003, and the first level of the band at 0.59
    assert abs(weak[0] - t ** N * (1 - t ** 2)) < 1e-5 and abs(weak[1] - weak[0]) < 1e-9 and abs(weak[0] - 0.003) < 5e-4
    assert abs(weak[2] - 0.59) < 0.005
    # the chain with the strong bonds at the ends has an empty gap, its first levels are at 0.55
    assert abs(strong[0] - 0.55) < 0.005 and abs(strong[1] - strong[0]) < 1e-9
    # the uniform chain, 2 cos(pi n / 17), from 0.18 to 1.97
    assert np.allclose(uni, np.sort(np.abs(2 * np.cos(np.pi * np.arange(1, 17) / 17))))
    assert abs(uni[0] - 0.18) < 0.005 and abs(uni[-1] - 1.97) < 0.005
    print('weak ends', np.round(weak[:3], 4), 'strong ends', np.round(strong[:2], 4), 'uniform', np.round(uni[[0, -1]], 4))


def option(script, d, name):
    """One picture option, the levels of the chain d[name]."""
    check(d)
    E = np.sort(d[name])
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    ax.axhline(0, color=style.GRID, lw=0.8, zorder=0)
    ax.plot(np.arange(1, len(E) + 1), E, 'o', color=style.ACCENT, ms=3.4, mew=0)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(0, 17); ax.set_ylim(-2.2, 2.2)
    ax.set_xticks([1, 8, 16]); ax.set_xticklabels(['1', '8', '16'], fontsize=11)
    ax.set_yticks([-2, -1, 0, 1, 2]); ax.set_yticklabels(['$-2$', '$-1$', '0', '1', '2'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'level $n$', fontsize=12, labelpad=0); ax.set_ylabel(r'$E_n$', fontsize=12, labelpad=-6)
    style.save(fig, script)
