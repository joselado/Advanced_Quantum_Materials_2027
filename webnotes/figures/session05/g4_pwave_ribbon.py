"""Session 5, section 5.14, the BdG spectrum of a ribbon of the triangular lattice with (a) s-wave and (b) chiral p-wave
pairing, colored by the position of each state across the ribbon. The data come from the downloadable script
webnotes/scripts/session05/g4_pwave_ribbon.py, the first two pairings of its list, and _g4_ribbon.check asserts what the
caption states: the gap of (a) is empty with the smallest energy 0.40, the bulk has C = 0 and -2, and in (b) two branches
at the edge y > 0 go down with k and two at the edge y < 0 go up."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import _g4_ribbon as r
style = r.style

plt.rcParams.update({'savefig.dpi': 200})
d = r.load(style.run_script('session05/g4_pwave_ribbon.py'))
r.check(d)
fig, axs = plt.subplots(1, 2, figsize=(13.4 * style.CM, 6.0 * style.CM), gridspec_kw=dict(wspace=0.32))
ticks = ([-2, -0.4, 0.4, 2], [-2, -1.34, 1.34, 2])
tags = ('(a) s-wave', '(b) chiral p-wave')
for ax, i, tk, tag in zip(axs, (0, 1), ticks, tags):
    lc = r.draw(ax, d, i, lw=1.5)
    ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=10.5)
    ax.set_yticks(tk); ax.set_yticklabels([('%g' % t).replace('-', '$-$') for t in tk], fontsize=10.5)
    ax.set_xlabel(r'momentum $k$', fontsize=10.5, labelpad=1)
    ax.set_ylabel(r'energy $E/t$', fontsize=10.5, labelpad=1)
    ax.text(0, 3.25, tag, ha='center', va='bottom', fontsize=10.5)
cb = fig.colorbar(lc, ax=list(axs), pad=0.03, fraction=0.04, ticks=[-8, 0, 8])
cb.set_label(r'position $y$ across the ribbon', fontsize=10, labelpad=2)
cb.ax.tick_params(length=2, width=0.6, labelsize=10)
cb.outline.set_linewidth(0.5)
style.save(fig, __file__)
