"""Session 9, quiz of Section 9.6a, the density cos(2 k_F x) on the sites of a chain with k_F = pi/4.

Redrawn on 2026-11-22 with numbers on the axes, x at 0, 4, 8, 12 and the values -1, 0, 1, by the rules of
2026-11-21. The asserts are the pattern 1, 0, -1, 0 that the feedback quotes and its period of 4 sites."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

kF = np.pi / 4
x = np.arange(0, 13)
y = np.cos(2 * kF * x)
assert np.allclose(y[:4], [1, 0, -1, 0]) and np.allclose(y[4:], y[:-4])     # the pattern repeats after 4 sites
assert not np.allclose(y[2:], y[:-2])                                        # and not after 2
xx = np.linspace(0, 12, 400)
fig, ax = style.figure(height_cm=4.4, width_cm=8.5)
ax.plot(xx, np.cos(2 * kF * xx), color=style.GRID, lw=1.2)
ax.vlines(x, 0, y, color=style.ACCENT, lw=1.6)
ax.plot(x, y, 'o', color=style.ACCENT, ms=3.5)
ax.set_ylim(-1.5, 1.5); ax.set_xlim(-0.4, 12.8)
style.arrows(ax, xlabel=r'$x$', ylabel=r'$\cos(2k_Fx)$', ticks=True)
ax.set_xticks([0, 4, 8, 12]); ax.set_yticks([-1, 0, 1])
ax.tick_params(length=2.5, width=0.6, labelsize=8)
style.guide(ax, y=0)
for x0, x1 in ((1, 5), (5, 9)):
    ax.annotate('', xy=(x1, 1.28), xytext=(x0, 1.28), arrowprops=dict(arrowstyle='<|-|>', color=style.BROKEN, lw=1,
                                                                        mutation_scale=7, shrinkA=0, shrinkB=0))
    style.label(ax, (x0 + x1) / 2, 1.5, r'4 sites', color=style.BROKEN, fontsize=7.5)
style.save(fig, __file__)
