"""Session 6, Section 6.5, the energy that the antiferromagnet of the half-filled chain gains over the saturated
ferromagnet, per cell of two sites, at large U, on logarithmic axes. It is the figure of the feedback of the quiz on the
1/U law.

The data come from the downloadable pyqula script webnotes/scripts/session06/g2_chain_energy_difference.py, whose
ferromagnet starts from the field of the saturated state, so that it does not stop at a moment of a few k-points. The
asserts are in _g2_chain.check_energy, which compares it with the gap equation of _mf.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g2_chain
from _g2_chain import style

d = style.run_script('session06/g2_chain_energy_difference.py')
_g2_chain.check_energy(d)
Us, dE = np.array(d['Us']), np.array(d['difference'])
D = dict(zip(Us, dE))

style.plt.rcParams.update({'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5})     # read at the 360 px of a quiz
fig, ax = style.figure(height_cm=5.6, width_cm=9.0)
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlim(5, 75); ax.set_ylim(0.05, 0.9)
Ut = np.geomspace(5.5, 70, 100)
ax.plot(Ut, 4 / Ut, color=style.BROKEN, lw=1.1, ls=(0, (3, 2)))
ax.plot(Us, dE, color=style.ACCENT, lw=1.3)
ax.plot(Us, dE, 'o', color=style.ACCENT, ms=3.5, mew=0)
for U in (20.0, 40.0):
    ax.plot([5, U], [D[U], D[U]], color=style.GRID, lw=0.8, zorder=0)
    ax.plot([U, U], [0.05, D[U]], color=style.GRID, lw=0.8, zorder=0)
    ax.plot([U], [D[U]], 'o', color=style.INK, ms=4.5, zorder=5)
style.label(ax, 7.2, 0.33, r'$4t^2/U$', color=style.BROKEN, fontsize=10.5)
style.arrows(ax, xlabel=r'$U/t$', ylabel=r'$(E_\mathrm{FM}-E_\mathrm{AFM})/t$', ticks=True)
ax.minorticks_off()
ax.set_xticks([10, 20, 40]); ax.set_xticklabels(['10', '20', '40'])
ax.set_yticks([D[40.0], D[20.0]]); ax.set_yticklabels([r'$%.4f$' % D[40.0], r'$%.4f$' % D[20.0]])
ax.tick_params(length=2.5, width=0.6)
style.save(fig, __file__)
