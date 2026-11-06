"""Session 8, the levels of the Ising dimer (8.1) and of the Heisenberg dimer (8.2), from the 4x4 matrices."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import style
import _dimerlevels as dl

assert dl.levels(dl.ISING) == [(-0.25, 2), (0.25, 2)]
assert dl.levels(dl.HEIS) == [(-0.75, 1), (0.25, 3)]
fig, ax = style.plt.subplots(figsize=(style.WIDTH_CM * 0.8 * style.CM, 5.6 * style.CM))
ax.axis('off'); ax.set_xlim(-0.9, 9.6); ax.set_ylim(-1.5, 1.4)
dl.column(ax, 1.0, dl.ISING, r'Ising dimer', [style.BROKEN, style.ACCENT], [r'$-\frac{1}{4}$, $|{\uparrow\downarrow}\rangle$, $|{\downarrow\uparrow}\rangle$', r'$+\frac{1}{4}$, $|{\uparrow\uparrow}\rangle$, $|{\downarrow\downarrow}\rangle$'])
dl.column(ax, 6.6, dl.HEIS, r'Heisenberg dimer', [style.BROKEN, style.ACCENT], [r'$-\frac{3}{4}$, singlet', r'$+\frac{1}{4}$, triplet'])
for x, t1, t2 in ((1.6, 'twofold ground level,', 'each state breaks time reversal'), (6.6, 'unique ground state,', 'time-reversal symmetric')):
    style.label(ax, x, -1.0, t1, fontsize=7.8, color=style.MUTED)
    style.label(ax, x, -1.28, t2, fontsize=7.8, color=style.MUTED)
ax.annotate('', xy=(-0.55, 1.0), xytext=(-0.55, -0.7), arrowprops=dict(arrowstyle='-|>', color=style.INK, lw=0.7, mutation_scale=7))
style.label(ax, -0.55, 1.22, r'$E$', fontsize=9)
style.save(fig, __file__)
