"""Session 9, quiz of Section 9.3, two degenerate levels coupled by v."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import matplotlib.pyplot as plt
import style

fig, ax = plt.subplots(figsize=(8.0 * style.CM, 4.2 * style.CM))
ax.axis('off')
def level(x0, x1, y, c=style.INK, lw=2.0):
    ax.plot([x0, x1], [y, y], color=c, lw=lw, solid_capstyle='butt')
level(0.0, 0.9, 0.0); level(1.1, 2.0, 0.0)
style.label(ax, 0.45, -0.28, r'$|1\rangle$', fontsize=8.5); style.label(ax, 1.55, -0.28, r'$|2\rangle$', fontsize=8.5)
ax.annotate('', xy=(3.2, 0), xytext=(2.3, 0), arrowprops=dict(arrowstyle='-|>', color=style.MUTED, lw=1, mutation_scale=8))
style.label(ax, 2.75, 0.2, r'$v$', color=style.MUTED, fontsize=8.5)
level(3.7, 5.0, 0.8, style.ACCENT); level(3.7, 5.0, -0.8, style.BROKEN)
style.label(ax, 5.75, 0.8, r'$+v$', color=style.ACCENT, fontsize=8.5)
style.label(ax, 5.75, -0.8, r'$-v$', color=style.BROKEN, fontsize=8.5)
style.label(ax, 4.35, 1.2, r'$(|1\rangle+|2\rangle)/\sqrt{2}$', color=style.ACCENT, fontsize=7.5)
style.label(ax, 4.35, -1.2, r'$(|1\rangle-|2\rangle)/\sqrt{2}$', color=style.BROKEN, fontsize=7.5)
ax.set_xlim(-0.2, 6.4); ax.set_ylim(-1.5, 1.5)
style.save(fig, __file__)
