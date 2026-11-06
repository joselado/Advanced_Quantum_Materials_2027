"""Session 9, the response experiment of Section 9.1, a perturbation at one place and a measurement at another."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

fig, ax = plt.subplots(figsize=(style.WIDTH_CM * style.CM, 4.4 * style.CM))
ax.set_xlim(0, 10); ax.set_ylim(0, 4.6)
ax.axis('off')
ax.add_patch(FancyBboxPatch((0.4, 0.6), 9.2, 2.6, boxstyle='round,pad=0.05,rounding_size=0.3',
                            fc='#f3f6fa', ec=style.LIGHT, lw=1.2))
style.label(ax, 5, 0.25, r'material in its ground state, described by $H_0$', color=style.MUTED, fontsize=8.5)
# lattice of sites
xs = np.linspace(0.9, 9.1, 12)
ax.plot(xs, 1.9 + 0 * xs, 'o', color=style.LIGHT, ms=5)
ax.plot(xs, 1.9 + 0 * xs, '-', color=style.GRID, lw=1, zorder=0)
x0, x1 = xs[2], xs[9]
ax.plot([x0], [1.9], 'o', color=style.BROKEN, ms=8)
ax.plot([x1], [1.9], 'o', color=style.ACCENT, ms=8)
ax.add_patch(FancyArrowPatch((x0, 3.9), (x0, 2.2), arrowstyle='-|>', mutation_scale=11, color=style.BROKEN, lw=1.6))
ax.add_patch(FancyArrowPatch((x1, 2.2), (x1, 3.9), arrowstyle='-|>', mutation_scale=11, color=style.ACCENT, lw=1.6))
style.label(ax, x0, 4.25, r'perturb at $(x,t)$', color=style.BROKEN)
style.label(ax, x1, 4.25, r'measure at $(x^\prime,t^\prime)$', color=style.ACCENT)
ax.annotate('', xy=(x1 - 0.3, 1.2), xytext=(x0 + 0.3, 1.2),
            arrowprops=dict(arrowstyle='-|>', color=style.INK, lw=1.0, mutation_scale=9))
style.label(ax, 0.5 * (x0 + x1), 0.85, r'$\chi(x^\prime-x,\,t^\prime-t)$, in $(q,\omega)$ space $\chi(q,\omega)$', fontsize=9)
style.save(fig, __file__)
