"""Session 5, one step of the pairing loop for U>0 flips the sign of the guess, so the iteration goes to zero."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

Ug = 0.5                      # U g, the product of the interaction and the pair susceptibility, for U > 0
f = lambda d: -Ug * d         # Delta_new = -U g Delta, from (5.3) in the linear regime
d0 = 1.0
fig, ax = style.plt.subplots(figsize=(9.0 * style.CM, 5.0 * style.CM))
x = np.linspace(-1.15, 1.15, 10)
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
assert abs(f(f(d0)) - 0.25) < 1e-12 and abs(d) < 0.04
for sp in ax.spines.values():
    sp.set_visible(False)
ax.set_xticks([]); ax.set_yticks([])
kw = dict(arrowstyle='-|>', color=style.INK, lw=0.7, mutation_scale=7, shrinkA=0, shrinkB=0, clip_on=False)
ax.annotate('', xy=(1.2, 0), xytext=(-1.15, 0), arrowprops=kw, annotation_clip=False)
ax.annotate('', xy=(0, 1.2), xytext=(0, -1.15), arrowprops=kw, annotation_clip=False)
style.label(ax, 1.22, 0.0, r'$\Delta$', ha='left', va='center')
style.label(ax, 0.0, 1.24, r'$\Delta_\mathrm{new}$', ha='center', va='bottom')
style.label(ax, 1.0, -0.12, r'$\Delta_0$', fontsize=8.5, color=style.BROKEN)
style.label(ax, 0.95, 0.38, r'$\Delta_\mathrm{new}=-0.5\,\Delta$', fontsize=8.5, color=style.ACCENT, ha='right')
style.label(ax, -0.75, -0.95, r'$\Delta_\mathrm{new}=\Delta$', fontsize=8.5, color=style.MUTED)
ax.set_xlim(-1.15, 1.15); ax.set_ylim(-1.15, 1.15)
ax.set_aspect('auto')
style.save(fig, __file__)
