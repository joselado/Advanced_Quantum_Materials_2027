"""Session 9, the geometric series behind Eq. (9.6), drawn as bubbles joined by interaction lines."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import style

fig, ax = plt.subplots(figsize=(style.WIDTH_CM * style.CM, 3.0 * style.CM))
ax.set_aspect('equal'); ax.axis('off')
R = 0.32


def bubble(x, y=0.0, left=True, right=True):
    ax.add_patch(Circle((x, y), R, fill=False, ec=style.ACCENT, lw=1.6))
    if left: ax.plot([x - R - 0.2, x - R], [y, y], color=style.INK, lw=0.9)
    if right: ax.plot([x + R, x + R + 0.2], [y, y], color=style.INK, lw=0.9)


def chain(x0, n):
    """n bubbles joined by n-1 dashed interaction lines, the outer legs are the probe and the measurement."""
    x = x0
    for i in range(n):
        bubble(x, left=(i == 0), right=(i == n - 1))
        if i < n - 1:
            ax.plot([x + R, x + 2 * R + 0.55 - 0.0], [0, 0], color=style.BROKEN, lw=1.3, ls=(0, (3, 2)))
            x += 2 * R + 0.55 + R
    return x + R + 0.2


def sym(x, s):
    style.label(ax, x, 0, s, fontsize=11)


style.label(ax, 0.2, 0, r'$\chi\;=$', fontsize=10)
x = 1.0
x = chain(x + 0.3, 1) + 0.5; sym(x, r'$-$'); x += 0.5
x = chain(x + 0.3, 2) + 0.5; sym(x, r'$+$'); x += 0.5
x = chain(x + 0.3, 3) + 0.5; sym(x, r'$-\ \cdots$')
ax.set_xlim(-0.2, x + 0.6); ax.set_ylim(-0.7, 0.7)
style.label(ax, 0.4, -0.62, r'bubble $=\chi_0$, dashed line $=U$', color=style.MUTED, fontsize=9, ha='left')
style.save(fig, __file__)
