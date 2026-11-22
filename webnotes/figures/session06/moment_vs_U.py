"""Session 6, Section 6.7, the moment of the half-filled chain against U, and the weight of double occupancy that is
left.

The data come from the downloadable pyqula script webnotes/scripts/session06/g2_chain_moment.py, the antiferromagnet of
the chain with two sites per cell on a mesh of 400 cells. The asserts are in _g2_chain.check_moment, which compares it
with the gap equation of _mf.py at every U and holds the numbers of the caption and of the quiz of Section 6.7. The
curve starts at U=t, since below it the mesh of 400 cells does not resolve the gap, which the check of the page shows."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g2_chain
from _g2_chain import style

d = style.run_script('session06/g2_chain_moment.py')
_g2_chain.check_moment(d)
Us, m, dbl = np.array(d['Us']), np.array(d['moment']), np.array(d['double'])
M = dict(zip(Us, m))

fig, ax = style.figure(height_cm=5.6)
ax.set_xlim(0, 24.5); ax.set_ylim(0, 1.12)
for U in (4.0, 16.0):
    ax.plot([0, U], [M[U], M[U]], color=style.GRID, lw=0.8, zorder=0)
    ax.plot([U, U], [0, M[U]], color=style.GRID, lw=0.8, zorder=0)
ax.plot(Us, m, color=style.ACCENT)
ax.plot(Us, dbl, color=style.BROKEN)
style.label(ax, 14.5, 0.86, r'$|m|$, the moment on a site', color=style.ACCENT, fontsize=8.5)
style.label(ax, 11.8, 0.22, r'$4\langle n_\uparrow n_\downarrow\rangle=1-m^2$', color=style.BROKEN, fontsize=8.5)
style.arrows(ax, xlabel=r'$U/t$', ylabel=r'$|m|$ and $1-m^2$', ticks=True)
ax.set_xticks([1, 4, 16]); ax.set_xticklabels(['1', '4', '16'])
ax.set_yticks([0, M[4.0], M[16.0]]); ax.set_yticklabels(['0', r'$%.2f$' % M[4.0], r'$%.2f$' % M[16.0]])
ax.tick_params(length=2.5, width=0.6)
style.save(fig, __file__)
