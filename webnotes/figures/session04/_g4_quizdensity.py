"""Session 4, section 4.17, the shared code of the three pictures of the quiz on the density with a quasihole.

Each picture is 2 pi l_B^2 times the density of N = 20 electrons in the lowest Landau level against r/l_B, with the same
axes and the same ticks and no other text, since the pictures are the options of a quiz. The filled level comes from the
orbitals (4.10). The Laughlin state with m = 3 and the same state with a quasihole at the origin are the mean of four
Metropolis runs of _g4_laughlin_mc.py each, with the seeds 1 to 4 and 51 to 54 of g4_quasihole_dimple.py, so that the two
pictures have the same noise and the noise of one run does not draw a dip at the origin. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import style
import _g4_laughlin_mc as mc

N = 20


def mean_density(holes, seeds):
    """The bin centers and the mean over the runs of 2 pi l_B^2 times the density, for the Laughlin state with m = 3."""
    runs = [mc.metropolis(N, 3, holes, s) for s in seeds]
    return runs[0][0], np.mean([u[1] for u in runs], 0)


def option(script, r, filling):
    """One picture option, 2 pi l_B^2 rho against r/l_B, with its axes and no other text."""
    plt.rcParams.update({'savefig.dpi': 220})
    fig, ax = plt.subplots(figsize=(3.4 * style.CM, 3.2 * style.CM))
    ax.plot(r, filling, color=style.ACCENT, lw=1.5)
    ax.axhline(1 / 3, color=style.GRID, lw=0.8, ls=':', zorder=0)
    ax.set_xlim(0, 12.5); ax.set_ylim(0, 1.15)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    ax.set_xticks([0, 5, 10]); ax.set_xticklabels(['0', '5', '10'], fontsize=11)
    ax.set_yticks([0, 1 / 3, 1]); ax.set_yticklabels(['0', r'$\frac{1}{3}$', '1'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$r/\ell_B$', fontsize=12, labelpad=0); ax.set_ylabel(r'$2\pi\ell_B^2\rho$', fontsize=12, labelpad=1)
    style.save(fig, script)
