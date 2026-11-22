"""Session 4, section 4.5, the chiral modes of a quantum Hall ribbon with the chemical potential between the third
and the fourth Landau level, in the feedback of the quiz on the number of modes.

The continuum ribbon of width W=12 l_B with hard walls of _g2_qhribbon.py. In the Landau gauge each k_y gives the
oscillator H = p^2/2 + (x - x0)^2/2 in units of hbar omega_c and l_B, with x0 = k_y l_B^2, on 0<x<W with zero at the
walls, so k_y l_B = 0 and 12 are the guiding centers on the two walls. The flat levels are n+1/2, and each of the two
walls bends the levels up. The chemical potential mu=3 is between 5/2 and 7/2, and the circles are the crossings,
three at each edge. Redrawn on 2026-11-21 with the ticks of the plot rules."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
import _g2_qhribbon as qh

W, mu = qh.W, 3.0
ks = np.linspace(-3.5, W + 3.5, 500)
E = qh.levels(ks, nlev=6)
bulk = qh.check_bulk(ks, E)
nl, nr = qh.edge_counts(ks, E, mu)
print('bulk levels', np.round(bulk, 4), 'crossings left and right', nl, nr)
assert nl == nr == 3

fig, ax = style.figure(width_cm=10.5, height_cm=5.6)
ax.set_xlim(ks[0], ks[-1]); ax.set_ylim(0, 4.8)
qh.draw(ax, ks, E, mu, circles=True)
style.arrows(ax, xlabel=r'$k_y\ell_B$', ylabel=r'$E/\hbar\omega_c$', ticks=True)
ax.set_xticks([0, W]); ax.set_xticklabels(['0', '12'])
ax.set_yticks([0.5, 1.5, 2.5, 3, 3.5]); ax.set_yticklabels(['0.5', '1.5', '2.5', r'$\mu=3$', '3.5'])
ax.tick_params(length=2.5, width=0.6)
style.label(ax, -2.0, 0.6, 'left edge\n$v_y<0$', color=style.ACCENT, fontsize=8.5)
style.label(ax, W + 2.0, 0.6, 'right edge\n$v_y>0$', color=style.BROKEN, fontsize=8.5)
style.label(ax, W / 2, 0.2, 'bulk levels', color=style.MUTED, fontsize=8)
style.save(fig, __file__)
