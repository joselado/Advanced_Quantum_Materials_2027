"""Session 9, the two spin patterns that the static response of the square lattice can favor."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import matplotlib.pyplot as plt
import style

fig, axs = plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 4.4 * style.CM), gridspec_kw=dict(wspace=0.1))
n = 4
for ax, stag, title in zip(axs, (False, True), (r'$q=0$, ferromagnet', r'$Q=(\pi,\pi)$, antiferromagnet')):
    ax.set_aspect('equal'); ax.axis('off')
    for i in range(n):
        for j in range(n):
            s = (-1) ** (i + j) if stag else 1
            ax.plot([i, i + 1], [j, j], color=style.GRID, lw=0.8, zorder=0) if i < n - 1 else None
            if j < n - 1:
                ax.plot([i, i], [j, j + 1], color=style.GRID, lw=0.8, zorder=0)
            col = style.ACCENT if s > 0 else style.BROKEN
            ax.annotate('', xy=(i, j + 0.32 * s), xytext=(i, j - 0.32 * s),
                        arrowprops=dict(arrowstyle='-|>', color=col, lw=1.6, mutation_scale=9, shrinkA=0, shrinkB=0))
    ax.set_xlim(-0.6, n - 0.4); ax.set_ylim(-0.6, n - 0.4)
    ax.set_title(title, fontsize=9, color=style.INK, pad=2)
style.save(fig, __file__)
