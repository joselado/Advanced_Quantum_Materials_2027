"""Session 5, Section 5.5, the self-consistent pairing |Delta| of the attractive chain against the attraction |U|.

The calculation is the pyqula script webnotes/scripts/session05/g1_meanfield_swave_chain.py, which the student
downloads under the figure, with the settings of the notebook. The asserts are in _g1_gapbands.check, which also
solves the BCS gap equation at the same density with numpy as a second route."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g1_gapbands
from _g1_gapbands import style

d = style.run_script('session05/g1_meanfield_swave_chain.py')
_g1_gapbands.check(d)
U, D = -np.array(d['Us']), d['deltas']

style.plt.rcParams.update({'font.size': 10.5, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5})   # readable at 390 px
fig, ax = style.figure(height_cm=5.4, width_cm=9.5)
ax.set_xlim(0.5, 2.2); ax.set_ylim(0, 0.42)
for u, dd in zip(U, D):
    if u in (1.0, 1.5, 2.0):
        ax.plot([0.5, u], [dd, dd], color=style.GRID, lw=0.8, zorder=0)
        ax.plot([u, u], [0, dd], color=style.GRID, lw=0.8, zorder=0)
ax.plot(U, D, color=style.ACCENT, lw=1.2)
ax.plot(U, D, 'o', color=style.ACCENT, ms=4.5, mew=0)
style.arrows(ax, xlabel=r'$|U|$ in units of $t$', ylabel=r'$|\Delta|$ in units of $t$', ticks=True)
ax.set_xticks([1, 1.5, 2]); ax.set_xticklabels(['1', '1.5', '2'])
ax.set_yticks([0, 0.10, 0.22, 0.36]); ax.set_yticklabels(['0', '0.10', '0.22', '0.36'])
ax.tick_params(length=2.5, width=0.6)
style.save(fig, __file__)
