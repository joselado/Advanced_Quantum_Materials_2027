"""Session 9, quiz of Section 9.6, the density cos(2 k_F x) on the sites of a chain with k_F = pi/4."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

kF = np.pi / 4
x = np.arange(0, 13)
xx = np.linspace(0, 12, 400)
fig, ax = style.figure(height_cm=4.2, width_cm=8.5)
ax.plot(xx, np.cos(2 * kF * xx), color=style.GRID, lw=1.2)
ax.vlines(x, 0, np.cos(2 * kF * x), color=style.ACCENT, lw=1.6)
ax.plot(x, np.cos(2 * kF * x), 'o', color=style.ACCENT, ms=3.5)
ax.set_ylim(-1.5, 1.5); ax.set_xlim(-0.4, 12.8)
style.arrows(ax, xlabel=r'$x$', ylabel=r'$\cos(2k_Fx)$')
style.guide(ax, y=0)
for x0, x1 in ((1, 5), (5, 9)):
    ax.annotate('', xy=(x1, 1.28), xytext=(x0, 1.28), arrowprops=dict(arrowstyle='<|-|>', color=style.BROKEN, lw=1, mutation_scale=7, shrinkA=0, shrinkB=0))
    style.label(ax, (x0 + x1) / 2, 1.5, r'4 sites', color=style.BROKEN, fontsize=7.5)
style.save(fig, __file__)
