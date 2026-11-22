"""Shared code of the picture options of the quiz of Section 9.8 on a vacancy in three honeycomb insulators.

The data come from the downloadable script webnotes/scripts/session09/g5_vacancy_honeycomb.py, the same calculation as the
figure vacancy_dos: a pyqula torus of 18x18 cells with one site removed, the site with the onsite energy +M, and the LDOS
summed on its three neighbors with a broadening 0.03t. The three models are the Haldane model with t2 = 0.15t ("chern"), the
sublattice mass M = 0.78t ("trivial") and the Haldane model with t2 = 0.15t and M = 1.0t ("both"). Each picture has its axes,
the bulk gap shaded and no other text, and the three share the window and the ticks. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style


def option(script, name):
    """Draws the LDOS next to the vacancy of one model and returns the data of the script."""
    d = style.run_script('session09/g5_vacancy_honeycomb.py')
    E, ldos, gap = d['energies'], d['ldos'][name], d['gaps'][name]
    # the neighbors of the last model of the loop, t2 = 0.15 with M = 1.0, where the vacancy has the onsite energy 1.0 and
    # the test |H[v, j]| = 1 alone would also pick the vacancy itself: three sites at the distance 1, and not v
    nbr, v, r = d['nbr'], d['v'], d['g'].r
    assert len(nbr) == 3 and v not in nbr and np.allclose(np.linalg.norm(r[nbr] - r[v], axis=1), 1.0)
    assert ldos.max() < 5.4
    plt.rcParams.update({'font.size': 11})
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.9 * style.CM))
    ax.axvspan(-gap / 2, gap / 2, color=style.GRID, alpha=0.6, lw=0, zorder=0)
    ax.plot(E, ldos, color=style.ACCENT, lw=1.3)
    ax.set_xlim(E[0], E[-1]); ax.set_ylim(0, 5.4)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_linewidth(0.6)
    ax.set_xticks([-1, 0, 1]); ax.set_yticks([0, 2, 4])
    ax.tick_params(length=2.5, width=0.6, pad=2, labelsize=10.5)
    ax.set_xlabel(r'$E/t$', fontsize=11, labelpad=1)
    ax.set_ylabel(r'LDOS $(1/t)$', fontsize=11, labelpad=1)
    style.save(fig, script)
    return d
