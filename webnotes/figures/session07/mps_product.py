"""Session 7, one coefficient of the state as a product of matrices, one matrix per site chosen by the spin value."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
from matplotlib.patches import Rectangle, FancyArrowPatch

spins = [1, 0, 0, 1, 1]            # 1 = up, 0 = down, the configuration whose coefficient we read
L = len(spins)
fig, ax = style.plt.subplots(figsize=(style.WIDTH_CM * style.CM, 5.6 * style.CM))
ax.set_xlim(-1.5, L * 2.0 + 0.3); ax.set_ylim(-1.7, 3.9); ax.set_aspect('equal'); ax.axis('off')
yup, ydn = 2.0, 0.6
xs = [1.0 + 2.0 * i for i in range(L)]
for i, (x, s) in enumerate(zip(xs, spins)):
    for y, val in ((yup, 1), (ydn, 0)):
        wd, ht = 1.05, 0.9
        on = (val == s)
        ax.add_patch(Rectangle((x - wd / 2, y - ht / 2), wd, ht, facecolor=style.ACCENT if on else 'white',
                               edgecolor=style.ACCENT if on else style.GRID, lw=1.3))
        sym = r'\uparrow' if val else r'\downarrow'
        style.label(ax, x, y, r'$M^{%s}_{%d}$' % (sym, i + 1), fontsize=7.6, color='white' if on else style.MUTED)
    style.label(ax, x, 3.35, r'$s_{%d}=\,%s$' % (i + 1, r'\uparrow' if s else r'\downarrow'), fontsize=8.5)
    ysel = yup if s else ydn
    ax.plot([x, x], [3.05, ysel + 0.5], color=style.GRID, lw=0.9, ls=(0, (2, 2)), zorder=0)
for i in range(L - 1):
    y1 = yup if spins[i] else ydn
    y2 = yup if spins[i + 1] else ydn
    ax.plot([xs[i] + 0.45, xs[i + 1] - 0.45], [y1, y2], color=style.BROKEN, lw=1.5)
style.label(ax, 5.0, -0.5, r'$C(\uparrow,\downarrow,\downarrow,\uparrow,\uparrow)=M^{\uparrow}_1M^{\downarrow}_2M^{\downarrow}_3M^{\uparrow}_4M^{\uparrow}_5$', fontsize=9.5)
style.label(ax, 5.0, -1.3, 'the product of the chosen matrices is one number', fontsize=8.5, color=style.MUTED)
style.save(fig, __file__)
