"""Session 8, quiz of 8.3, the levels of H = J S0.S1 for J=1 and J=-1, from the 4x4 matrix."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import style
import _dimerlevels as dl

assert dl.levels(dl.HEIS) == [(-0.75, 1), (0.25, 3)]
assert dl.levels(-dl.HEIS) == [(-0.25, 3), (0.75, 1)]
fig, ax = style.plt.subplots(figsize=(9.5 * style.CM, 5.2 * style.CM))
ax.axis('off'); ax.set_xlim(-0.9, 7.4); ax.set_ylim(-1.0, 1.5)
dl.column(ax, 1.0, dl.HEIS, r'$J=1$', [style.BROKEN, style.ACCENT], [r'$-\frac{3}{4}$, singlet', r'$+\frac{1}{4}$, triplet'])
dl.column(ax, 5.0, -dl.HEIS, r'$J=-1$', [style.BROKEN, style.ACCENT], [r'$-\frac{1}{4}$, triplet', r'$+\frac{3}{4}$, singlet'])
style.save(fig, __file__)
