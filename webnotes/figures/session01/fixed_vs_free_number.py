"""Session 1, a dot with two levels, the states with a fixed number of electrons and a superposition that mixes them."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch
import style

fig, ax = plt.subplots(figsize=(style.WIDTH_CM * style.CM, 6.2 * style.CM))
ax.axis('off')


def state(x, occ, y=0.0):
    """A dot with a lower and an upper level, a disc on each occupied one."""
    for j, o in enumerate(occ):
        yy = y + 0.55 * j
        ax.plot([x - 0.45, x + 0.45], [yy, yy], color=style.MUTED, lw=1.2)
        if o:
            ax.scatter([x], [yy + 0.16], s=45, color=style.ACCENT, zorder=3)


# the four Fock states of two levels, sorted by the number of electrons
xs = {'0': 0.0, '1a': 2.6, '1b': 4.0, '2': 6.6}
state(xs['0'], [0, 0]); state(xs['1a'], [1, 0]); state(xs['1b'], [0, 1]); state(xs['2'], [1, 1])
for x, s in [(0.0, '0'), (3.3, '1'), (6.6, '2')]:
    style.label(ax, x, -0.4, r'$N=%s$' % s, fontsize=9.5)
# first quantization lives in the column N = 1
ax.add_patch(FancyBboxPatch((1.9, -0.7), 2.8, 2.05, boxstyle='round,pad=0.05,rounding_size=0.15',
                            facecolor='none', edgecolor=style.LIGHT, lw=1.2, zorder=1))
style.label(ax, 3.3, -1.15, 'first quantization, always one electron', color=style.ACCENT, fontsize=8.5)
# a superposition of N = 0 and N = 2
ax.add_patch(FancyArrowPatch((0.0, 1.1), (6.6, 1.1), connectionstyle='arc3,rad=-0.28', arrowstyle='<|-|>',
                             mutation_scale=8, color=style.BROKEN, lw=1.2, zorder=2))
style.label(ax, 3.3, 3.05, r'$\frac{1}{\sqrt{2}}\left(|0\rangle+|2\rangle\right)$', color=style.BROKEN, fontsize=9.5)
style.label(ax, 3.3, 3.7, 'second quantization, a fluctuating number', color=style.BROKEN, fontsize=8.5)
ax.set_xlim(-1.0, 7.6)
ax.set_ylim(-1.5, 4.0)
style.save(fig, __file__)
