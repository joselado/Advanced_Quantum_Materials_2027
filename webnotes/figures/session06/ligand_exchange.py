"""Session 6, the virtual process with two holes on the ligand that can make the exchange between two ions ferromagnetic."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import style

fig, ax = plt.subplots(figsize=(style.WIDTH_CM * style.CM, 4.4 * style.CM))
ax.axis('off'); ax.set_aspect('equal')

def metal(x, y, label):
    ax.add_patch(Circle((x, y), 0.85, fc=style.LIGHT, ec=style.ACCENT, lw=1.2, alpha=0.55))
    style.label(ax, x, y + 1.15, label, fontsize=8.5)

def ligand(x, y, holes):
    ax.add_patch(Circle((x, y), 0.6, fc='white', ec=style.INK, lw=1.2))
    for dx in (-0.2, 0.2):
        if holes:
            ax.add_patch(Circle((x + dx, y), 0.1, fc='white', ec=style.BROKEN, lw=1.0, zorder=4))
        else:
            ax.add_patch(Circle((x + dx, y), 0.1, fc=style.INK, ec=style.INK, lw=0.5, zorder=4))

def spin(x, y, up):
    ax.annotate('', xy=(x, y + (0.45 if up else -0.45)), xytext=(x, y - (0.45 if up else -0.45)),
                arrowprops=dict(arrowstyle='-|>', color=style.INK, lw=1.4, mutation_scale=9))

for row, x0, holes in [(0, 0.0, False), (1, 11.0, True)]:
    y = 0.0
    metal(x0, y, 'ion 1'); metal(x0 + 6.0, y, 'ion 2'); ligand(x0 + 3.0, y, holes)
    style.label(ax, x0 + 3.0, y + 1.0, 'ligand p shell', fontsize=8)
    style.label(ax, x0, y, r'$\mathbf{S}_1$', fontsize=9); style.label(ax, x0 + 6.0, y, r'$\mathbf{S}_2$', fontsize=9)
    if row:
        ax.add_patch(Circle((x0 + 0.5, y - 0.5), 0.1, fc=style.INK, ec='none'))
        ax.add_patch(Circle((x0 + 5.5, y - 0.5), 0.1, fc=style.INK, ec='none'))
for xa, xb in [(2.3, 0.9), (3.7, 5.1)]:
    ax.add_patch(FancyArrowPatch((xa, 0.0), (xb, 0.0), connectionstyle='arc3,rad=-0.35', arrowstyle='-|>', mutation_scale=9, color=style.BROKEN, lw=1.2))
ax.annotate('', xy=(10.0, 0.0), xytext=(7.6, 0.0), arrowprops=dict(arrowstyle='-|>', color=style.INK, lw=0.9, mutation_scale=9))
style.label(ax, 8.8, 0.45, 'two hops', color=style.BROKEN, fontsize=8.5)
style.label(ax, 3.0, -1.6, 'initial state, ligand p shell full', fontsize=8.5)
style.label(ax, 14.0, -1.6, 'virtual state, two holes on the ligand', color=style.BROKEN, fontsize=8.5)
ax.set_xlim(-1.3, 18.3); ax.set_ylim(-2.0, 2.3)
style.save(fig, __file__)
