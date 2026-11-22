"""Shared code of the picture options of the quiz on the bands of the chain at U=4t, Section 6.4.

The three options are drawn from the downloadable pyqula script webnotes/scripts/session06/g2_chain_meanfield.py, the
ferromagnet at n=0.2 (filling=0.1), the antiferromagnet at half filling and the bands of U=0 of the cell of two sites,
which are those of the paramagnet. All three have the energy measured from the Fermi level, the same axes and no other
text. The asserts are in _g2_chain.check_meanfield. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g2_chain
from _g2_chain import style
plt = style.plt


def option(script, which):
    """One picture option, 'fm', 'afm' or 'pm', with the same axes for the three."""
    d = style.run_script('session06/g2_chain_meanfield.py')
    _g2_chain.check_meanfield(d)
    ks = d['ks']
    bands = {'fm': d['bands_fm'], 'afm': d['bands_afm'][:, [0, 3]], 'pm': d['bands_pm'][:, [0, 3]]}[which]
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    ax.axhline(0, color=style.MUTED, lw=0.8, ls=(0, (3, 2)), zorder=0)
    for n in range(bands.shape[1]):
        ax.plot(ks, bands[:, n], color=style.ACCENT, lw=1.6)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-2.9, 4.7)
    ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=11)
    ax.set_yticks([-2, 0, 2, 4]); ax.set_yticklabels([r'$-2$', '0', '2', '4'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$k$', fontsize=12, labelpad=0); ax.set_ylabel(r'$E/t$', fontsize=12, labelpad=-2)
    style.save(fig, script)
