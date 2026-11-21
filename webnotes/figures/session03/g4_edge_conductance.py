"""Session 3, section 3.11, the lab box: the conductance of a clean ribbon against the chemical potential.

The data come from the downloadable script webnotes/scripts/session03/g4_edge_conductance.py, which calls pyqula. The ribbon is
honeycomb_zigzag_ribbon(10) with t=1, once with the intrinsic spin-orbit coupling add_soc(0.1), which is the quantum spin Hall
insulator with the bulk gap 0.9 t, and once with the sublattice imbalance 0.45 t, an ordinary insulator with the same gap. The
conductance is the Landauer transmission between two leads made of the same ribbon, in units of e^2/h, so it counts the states that
move to the right at this energy. Inside the gap it is 2 for the quantum spin Hall insulator, one channel for each of the two
edges, and 0 for the ordinary insulator. There is no disorder, no contact resistance and no inelastic scattering."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

d = style.run_script('session03/g4_edge_conductance.py')
mu, G, G0, gap = d['energies'], d['conductance_qsh'], d['conductance_trivial'], d['gap']
ingap = np.abs(mu) < 0.4
print('gap', round(gap, 4), 'in the gap: quantum spin Hall', round(G[ingap].min(), 4), 'to', round(G[ingap].max(), 4),
      'ordinary insulator, largest', G0[ingap].max())
assert abs(gap - 0.9) < 1e-6
assert abs(gap / (6 * np.sqrt(3)) - 0.087) < 5e-4      # the second-neighbor hopping t2 with the same gap, as the caption says
assert np.all(np.abs(G[ingap] - 2) < 2e-3) and np.all(G0[ingap] < 1e-3)

fig, ax = plt.subplots(figsize=(9.6 * style.CM, 5.6 * style.CM))
ax.axvspan(-gap / 2, gap / 2, color='#ececec', lw=0, zorder=0)
ax.plot(mu, G0, color=style.BROKEN, lw=1.6, ls=(0, (4, 2)), zorder=2)
ax.plot(mu, G, color=style.ACCENT, lw=1.9, zorder=3)
ax.set_xlim(-0.8, 0.8); ax.set_ylim(-0.25, 7.2)
style.arrows(ax, xlabel=r'$\mu/t$', ylabel=r'$G\ (e^2/h)$')
ax.set_xticks([-0.45, 0, 0.45]); ax.set_xticklabels(['$-0.45$', '0', '$0.45$'], fontsize=11)
ax.set_yticks([0, 2, 4, 6]); ax.set_yticklabels(['0', '2', '4', '6'], fontsize=11); ax.tick_params(length=2.5, width=0.6)
ax.text(0, 2.45, 'quantum spin Hall', color=style.ACCENT, fontsize=11, ha='center', va='bottom')
ax.text(0, 0.42, 'ordinary insulator', color=style.BROKEN, fontsize=11, ha='center', va='bottom')
ax.text(0, 6.6, 'gap', color=style.MUTED, fontsize=11, ha='center', va='center')
style.save(fig, __file__)
