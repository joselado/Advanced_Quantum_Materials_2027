"""Helper of the picture quiz of 7.2b, a chain of the sites 1 to 6 with fermions on some of the sites 1 to 5.

Site 6 is empty and marked by a ring, as in Figure 7.1, and the shaded strip is the string K_6 over the sites j < 6.
The number of fermions in the strip fixes K_6 = (-1)^(N_left), which the check script of the page asserts."""
import style
from matplotlib.patches import Circle, FancyBboxPatch


def draw(script, occupied, width_cm=6.0):
    """occupied lists the sites, from 1 to 5, that hold a fermion."""
    assert all(1 <= i <= 5 for i in occupied)
    fig, ax = style.plt.subplots(figsize=(width_cm * style.CM, 2.1 * style.CM))
    ax.set_xlim(0.45, 6.55); ax.set_ylim(-0.95, 0.55); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(FancyBboxPatch((0.55, -0.42), 4.9, 0.84, boxstyle='round,pad=0,rounding_size=0.2',
                                facecolor='#f3dcd8', edgecolor='none', zorder=0))
    ax.plot([1, 6], [0, 0], color=style.GRID, lw=1.6, zorder=1)
    for i in range(1, 7):
        full = i in occupied
        ax.add_patch(Circle((i, 0), 0.3, facecolor=style.ACCENT if full else 'white', edgecolor=style.ACCENT,
                            lw=1.2, zorder=3))
        style.label(ax, i, -0.72, str(i), fontsize=9, color=style.INK)
    ax.add_patch(Circle((6, 0), 0.43, facecolor='none', edgecolor=style.BROKEN, lw=1.4, zorder=4))
    style.save(fig, script, sketch=True)
    return len(occupied)
