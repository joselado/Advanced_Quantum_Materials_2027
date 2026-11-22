"""Session 5, one step of the pairing loop for U>0 flips the sign of the guess, so the iteration goes to zero.

Redrawn on 2026-11-21 under the same name, with the axes named through style.arrows and ticks at the values of the
caption, the first guess Delta_0 = 1 and the next ones -0.5 and 0.25, with both axes in units of Delta_0."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

Ug = 0.5                      # U g, the product of the interaction and the pair susceptibility, for U > 0
f = lambda d: -Ug * d         # Delta_new = -U g Delta, from (5.3) in the linear regime
d0 = 1.0
fig, ax = style.plt.subplots(figsize=(8.0 * style.CM, 6.0 * style.CM))
x = np.linspace(-0.75, 1.15, 10)
style.guide(ax, x=0, color=style.GRID, lw=0.8)
style.guide(ax, y=0, color=style.GRID, lw=0.8)
ax.plot(x, f(x), color=style.ACCENT)
ax.plot(x, x, color=style.MUTED, lw=1.0, ls=(0, (3, 2)))
d = d0; pts = [(d, 0.0)]
for _ in range(5):
    nd = f(d)
    pts += [(d, nd), (nd, nd)]
    d = nd
px, py = zip(*pts)
ax.plot(px, py, color=style.BROKEN, lw=1.0)
ax.plot([d0], [0], 'o', color=style.BROKEN, ms=3.5)
# the caption: each step flips the sign and halves the guess, 1, -0.5, 0.25, ..., so the iteration goes to zero
assert f(d0) == -0.5 and f(f(d0)) == 0.25 and abs(d) < 0.04
style.arrows(ax, xlabel=r'$\Delta$', ylabel=r'$\Delta_\mathrm{new}$', ticks=True)
ax.set_xticks([-0.5, 0, 0.5, 1]); ax.set_xticklabels([r'$-0.5$', '0', '0.5', '1'])
ax.set_yticks([-0.5, 0, 0.5, 1]); ax.set_yticklabels([r'$-0.5$', '0', '0.5', '1'])
ax.tick_params(length=2.5, width=0.6)
style.label(ax, -0.7, 0.6, r'$\Delta_\mathrm{new}=-0.5\,\Delta$', fontsize=8.5, color=style.ACCENT, ha='left')
style.label(ax, 0.7, 0.95, r'$\Delta_\mathrm{new}=\Delta$', fontsize=8.5, color=style.MUTED, ha='right')
style.label(ax, 1.0, 0.1, r'$\Delta_0$', fontsize=8.5, color=style.BROKEN)
ax.set_xlim(-0.75, 1.15); ax.set_ylim(-0.75, 1.15)
style.save(fig, __file__)
