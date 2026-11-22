"""Session 8, Section 8.9, the three classes of spinon bands of (8.15) for one spin species, redrawn with pyqula.

The calculation is the pyqula script webnotes/scripts/session08/g3_spinon_band_classes.py, which the student downloads
under the figure. It takes the hopping chi = +1 of pyqula, so the uniform chain has the band +2 cos k, the chain of two
sites per cell has the hoppings 0.6 inside the cell and 1 between the cells, and the pi-flux square lattice is
square_lattice().get_supercell([1, 2]) with add_orbital_magnetic_field(0.5), cut along k_y = pi/2 of its cell of two
sites along y, where the two Dirac points of this gauge lie, as webnotes/conventions/session08.md says. The momentum is
the phase per cell, from -pi to pi, which is in units of the inverse distance between sites for the uniform chain and
for k_x of the pi-flux lattice, and per cell of two sites for the dimerized chain. The helper _g3_bands.py checks the
numbers of the caption and of the quiz and holds the drawing of one panel."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g3_bands
from _g3_bands import style

d = style.run_script('session08/g3_spinon_band_classes.py')
_g3_bands.check(d)

fig, axs = style.plt.subplots(1, 3, figsize=(style.WIDTH_CM * style.CM, 5.4 * style.CM), sharey=True)
panels = [('uniform', 'gapless', 'uniform chain', r'$k$'), ('dimerized', 'gapped', 'dimerized chain', r'$k$'),
          ('piflux', 'Dirac', r'$\pi$-flux lattice, $k_y=\pi/2$', r'$k_x$')]
for ax, (name, cls, sub, xl) in zip(axs, panels):
    k, E = _g3_bands.panel(ax, d, name, xlabel=xl, fontsize=10.5, ylabel=r'$E/\chi$' if name == 'uniform' else None)
    ax.set_title(cls, fontsize=10.5, pad=15)
    ax.text(0.5, 1.035, sub, transform=ax.transAxes, ha='center', va='bottom', fontsize=9.5, color=style.MUTED)
# the gap of the dimerized chain at the zone edge, and the Dirac points of the pi-flux lattice
ax = axs[1]
ax.annotate('', xy=(np.pi - 0.2, 0.4), xytext=(np.pi - 0.2, -0.4),
            arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.7, mutation_scale=6, shrinkA=0, shrinkB=0))
style.label(ax, np.pi - 0.38, 0.0, r'$0.8$', fontsize=10, ha='right')
ax = axs[2]
for x in (-np.pi, 0.0, np.pi):
    ax.plot([x], [0], 'o', ms=3.2, color=style.INK, zorder=4, clip_on=False)
ax.annotate('Dirac point', xy=(0, 0.12), xytext=(0, 2.25), ha='center', va='bottom', fontsize=9.5, color=style.INK,
            arrowprops=dict(arrowstyle='-|>', color=style.INK, lw=0.6, mutation_scale=6, shrinkA=1, shrinkB=1))
axs[0].tick_params(axis='y', length=2.5, pad=2)
fig.subplots_adjust(wspace=0.3)
style.save(fig, __file__)
