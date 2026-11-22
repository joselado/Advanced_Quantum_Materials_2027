"""Session 1, the filling of the bands in a metal, an insulator and a doped semiconductor.

Redrawn on 2026-11-21 with its axes, from the downloadable pyqula script webnotes/scripts/session01/g1_chain_bands.py
through _g1_fill.py, which asserts the numbers of the caption. The momentum k is per site, from -pi to pi for every
panel, so the chain with two sites per cell is drawn over two of its zones, whose edges k = +-pi/2 are dashed. The
energies are in units of the hopping t, with m = 0.6t, and the Fermi levels are 0, 0, 0.95t and -0.95t."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style
import _g1_fill

d = _g1_fill.check(style.run_script('session01/g1_chain_bands.py'))
FS = 11
fig, axs = plt.subplots(2, 2, figsize=(11.0 * style.CM, 8.8 * style.CM))
panels = (('metal', 'metal'), ('insulator', 'insulator'), ('n', 'n-doped'), ('p', 'p-doped'))
for ax, (kind, title) in zip(axs.flat, panels):
    _g1_fill.draw(ax, d, kind)
    style.arrows(ax, xlabel=r'$k$', ylabel=r'$E/t$', ticks=True)
    ax.set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
    ax.set_xticklabels([r'$-\pi$', r'$-\frac{\pi}{2}$', '0', r'$\frac{\pi}{2}$', r'$\pi$'], fontsize=FS)
    ax.set_yticks([-2, -1, 0, 1, 2]); ax.set_yticklabels(['$-2$', '$-1$', '0', '1', '2'], fontsize=FS)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.spines['left'].set_visible(True); ax.spines['bottom'].set_visible(True)
    ax.set_title(title, fontsize=FS + 0.5, pad=12)
    ef = _g1_fill.EF[kind]
    style.label(ax, 2.7, ef + 0.5, r'$E_F$', color=style.BROKEN, fontsize=FS)
fig.subplots_adjust(wspace=0.5, hspace=0.75)
style.save(fig, __file__)
