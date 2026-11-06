"""Session 10, the configurations s' that a Heisenberg chain connects to s in Eq. (10.4)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import style

s = [1, -1, -1, 1, 1, -1]
L = len(s)
fig, ax = plt.subplots(figsize=(8.0 * style.CM, 5.2 * style.CM))
ax.axis('off')


def row(y, conf, hl=None, color=style.ACCENT):
    for i, v in enumerate(conf):
        c = style.ACCENT if v > 0 else style.BROKEN
        ax.annotate('', xy=(i, y + 0.28 * v), xytext=(i, y - 0.28 * v),
                    arrowprops=dict(arrowstyle='-|>', color=c, lw=1.5, mutation_scale=8, shrinkA=0, shrinkB=0))
    if hl is not None:
        ax.add_patch(FancyBboxPatch((hl - 0.32, y - 0.42), 1.64, 0.84, boxstyle='round,pad=0,rounding_size=0.15',
                                    fc='none', ec=style.INK, lw=0.9, ls=(0, (3, 2))))


row(0, s)
style.label(ax, -1.3, 0, r'$s$', fontsize=10)
bonds = [i for i in range(L - 1) if s[i] != s[i + 1]]
y = -1.35
for i in bonds:
    t = list(s); t[i], t[i + 1] = t[i + 1], t[i]
    row(y, t, hl=i)
    style.label(ax, -1.3, y, r"$s'$", fontsize=10)
    y -= 1.0
ax.set_xlim(-1.9, L - 0.2); ax.set_ylim(y - 0.5, 0.8)
ax.set_aspect('equal')
style.save(fig, __file__)
