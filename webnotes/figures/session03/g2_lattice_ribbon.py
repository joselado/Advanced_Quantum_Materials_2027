"""Session 3, section 3.6b, the ribbon of the square lattice without and with a magnetic field.

The data come from the pyqula script scripts/session03/g2_square_ribbon.py, which the student downloads. Panel (a) has no
field and panel (b) has the flux 0.02 per plaquette, in units of the flux quantum. The window is the bottom of the band.
The dashed lines of (b) are the continuum levels -4 + 4 pi B (n + 1/2) in units of t. The color is the position across
the ribbon, with the same scale in both panels."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import style, _g2_ribbon as rb
plt.rcParams.update({'font.size': 11, 'savefig.dpi': 300})     # labels a size up from style.py, readable on a phone

d = style.run_script('session03/g2_square_ribbon.py')
num = rb.check(d)
B = 0.02
i0, i1 = d['Bs'].index(0.0), d['Bs'].index(B)
# the numbers of the caption
assert abs(num[B]['hw'] - 0.25) < 0.002 and abs(num[B]['gaps'][0] - 0.24) < 0.005
assert abs(num[B]['levels'][0] + 3.88) < 0.005
assert d['W'] == 40

fig, axs = plt.subplots(1, 2, figsize=(13.2 * style.CM, 5.6 * style.CM), gridspec_kw=dict(wspace=0.42))
for ax, i, name, nlev in ((axs[0], i0, '(a) no field', 0), (axs[1], i1, '(b) flux 0.02', 4)):
    lc = rb.draw(ax, d, i, levels=nlev)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'])
    ax.set_yticks([-4, -3.5, -3]); ax.set_yticklabels(['$-4$', '$-3.5$', '$-3$'])
    ax.tick_params(length=2.5, width=0.6)
    ax.set_xlabel(r'$k$', labelpad=0); ax.set_ylabel(r'$E/t$', labelpad=2)
    ax.text(0.5, -0.27, name, transform=ax.transAxes, ha='center', va='top', fontsize=11)
cb = fig.colorbar(lc, ax=axs, fraction=0.035, pad=0.03, ticks=[-20, 0, 20])
cb.set_label(r'position $y/a$', fontsize=11); cb.ax.tick_params(length=2.5, width=0.6, labelsize=10)
cb.outline.set_linewidth(0.6)
style.save(fig, __file__)
