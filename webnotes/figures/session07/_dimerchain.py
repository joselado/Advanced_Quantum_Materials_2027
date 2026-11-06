"""Helper of the schematics of the dimer quizzes of session 7, a chain of 8 sites with the singlets of (7.8) and one block."""
import numpy as np
import style
from matplotlib.patches import Circle, FancyBboxPatch, Arc

def draw(script, block=None, width_cm=9.5):
    """block = (first, last) sites, inclusive, or None. A singlet is cut when only one of its two sites is in the block."""
    fig, ax = style.plt.subplots(figsize=(width_cm * style.CM, 3.5 * style.CM))
    ax.set_xlim(-0.7, 7.7); ax.set_ylim(-1.45, 1.0); ax.set_aspect('equal'); ax.axis('off')
    ncut = 0
    if block is not None:
        lo, hi = block
        ax.add_patch(FancyBboxPatch((lo - 0.38, -0.38), hi - lo + 0.76, 0.76, boxstyle='round,pad=0,rounding_size=0.3',
                                    facecolor='#e6eef6', edgecolor=style.LIGHT, lw=1.0, zorder=0))
    for a in range(0, 8, 2):
        cut = block is not None and ((block[0] <= a <= block[1]) != (block[0] <= a + 1 <= block[1]))
        ncut += cut
        col = style.BROKEN if cut else style.ACCENT
        ax.add_patch(Arc((a + 0.5, -0.38), 1.0, 0.9, theta1=180, theta2=360, color=col, lw=1.7 if cut else 1.4, zorder=1))
    for i in range(8):
        inside = block is not None and block[0] <= i <= block[1]
        ax.add_patch(Circle((i, 0), 0.26, facecolor=style.ACCENT if inside else 'white', edgecolor=style.ACCENT, lw=1.2, zorder=3))
        style.label(ax, i, 0.62, str(i), fontsize=8.5, color=style.INK)
    if block is not None:
        style.label(ax, 3.5, -1.28, '%s cut singlet%s, $S=%s$' % ({0: 'no', 1: 'one', 2: 'two'}[ncut], '' if ncut == 1 else 's', (r'\log 2' if ncut == 1 else r'%d\log 2' % ncut) if ncut else '0'),
                    fontsize=8.5, color=style.BROKEN if ncut else style.ACCENT)
    style.save(fig, script)
    return ncut
