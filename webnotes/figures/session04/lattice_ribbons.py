"""Session 4, section 4.11, the Landau levels and the edge states of two lattice ribbons in a field, computed with pyqula.

Redrawn on 2026-11-21 under the same name, with axes, from the downloadable script scripts/session04/g3_ribbons_in_field.py.
Panel (a) is the square ribbon of 40 sites with the hopping -1 and the flux 0.02 per plaquette, near the bottom of the band,
with the dashed lines -4 + 4 pi phi (n + 1/2) of (4.6). Panel (b) is the armchair ribbon of width 30 of the honeycomb
lattice, 51 bond lengths across, with the flux 0.005 per unit area, with the dashed lines 0 and +-sqrt(|n|) E_1 of (4.7),
E_1 = 3 sqrt(pi phi). pyqula builds the ribbons along x, so k is the momentum along the ribbon and y the position across
it, and the color is y over the position of the edge. The numbers of the caption are asserted in _g3_ribbons.check."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import style
import _g3_ribbons as rb
plt.rcParams.update({'font.size': 11, 'savefig.dpi': 300})     # labels a size up from style.py, readable on a phone

d = style.run_script('session04/g3_ribbons_in_field.py')
num = rb.check(d)
E1 = num['E1']

fig, axs = plt.subplots(1, 2, figsize=(13.2 * style.CM, 5.8 * style.CM), gridspec_kw=dict(wspace=0.45))
ax = axs[0]
for n in range(4):
    style.guide(ax, y=-4 + 4 * np.pi * rb.PHI_SQUARE * (n + 0.5), ls='--', color=style.MUTED, lw=0.7)
lc = rb.draw(ax, d['ks'], d['square_energies'], d['square_positions'], d['square_edge'], rb.SQUARE_WINDOW)
ax.set_yticks([-4, -3.88, -3.63, -3.4]); ax.set_yticklabels(['$-4$', '$-3.88$', '$-3.63$', '$-3.40$'])
ax = axs[1]
for n in range(-2, 3):
    style.guide(ax, y=np.sign(n) * np.sqrt(abs(n)) * E1, ls='--', color=style.MUTED, lw=0.7)
rb.draw(ax, d['ks'], d['honeycomb_energies'], d['honeycomb_positions'], d['honeycomb_edge'], rb.HONEY_WINDOW)
ax.set_yticks([-0.52, -0.37, 0, 0.37, 0.52]); ax.set_yticklabels(['', '$-0.37$', '0', '$0.37$', '$0.52$'])
for ax, name in ((axs[0], '(a) square lattice'), (axs[1], '(b) honeycomb lattice')):
    ax.set_xlabel(r'$k\,a$', labelpad=0); ax.set_ylabel(r'$E/t$', labelpad=2)
    ax.text(0.5, -0.25, name, transform=ax.transAxes, ha='center', va='top', fontsize=11)
cb = fig.colorbar(lc, ax=axs, fraction=0.035, pad=0.03, ticks=[-1, 0, 1])
cb.set_label(r'position $y/y_{\mathrm{edge}}$', fontsize=11); cb.ax.tick_params(length=2.5, width=0.6, labelsize=10)
cb.outline.set_linewidth(0.6)
style.save(fig, __file__)
