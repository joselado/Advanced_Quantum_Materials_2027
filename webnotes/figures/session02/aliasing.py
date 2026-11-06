"""Session 2, two waves with k and k + 2 pi / a that are the same vector on the sites of the chain."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

a = 1.0
k = 0.5
x = np.linspace(0, 9, 3000)
n = np.arange(0, 10)
w1 = lambda x: np.cos(k * x)
w2 = lambda x: np.cos((k + 2 * np.pi / a) * x)
assert np.allclose(w1(n * a), w2(n * a))
fig, ax = style.figure(height_cm=4.6)
ax.plot(x, w1(x), color=style.ACCENT)
ax.plot(x, w2(x), color=style.BROKEN, lw=0.9, alpha=0.85)
ax.scatter(n, w1(n), s=26, color=style.INK, zorder=5)
style.guide(ax, y=0)
style.arrows(ax, xlabel=r'$x/a$', ylabel='')
ax.set_xlim(-0.3, 9.4); ax.set_ylim(-1.35, 1.5)
ax.set_xticks(n); ax.set_xticklabels([str(i) for i in n]); ax.tick_params(axis='x', length=2.5, labelsize=8); ax.spines['bottom'].set_visible(True)
style.label(ax, 4.6, 1.36, r'$\cos(kx)$, $k=0.5/a$', color=style.ACCENT, fontsize=8.5, ha='right')
style.label(ax, 4.9, 1.36, r'$\cos[(k+2\pi/a)x]$', color=style.BROKEN, fontsize=8.5, ha='left')
style.save(fig, __file__)
