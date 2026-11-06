"""Session 5, a d-wave gap has nodes on the zone diagonals, and only a Fermi pocket that reaches them has gapless points."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import style

# d-wave gap Delta_0 (cos kx - cos ky), pockets of radius 0.8 around Gamma and around X = (pi, 0)
r = 0.8
th = np.linspace(0, 2 * np.pi, 721)
def gap_min(cx, cy):
    kx, ky = cx + r * np.cos(th), cy + r * np.sin(th)
    return np.abs(np.cos(kx) - np.cos(ky))
assert gap_min(0, 0).min() < 0.01            # the pocket at Gamma touches the nodal lines
assert gap_min(np.pi, 0).min() > 1.0         # the pocket at X stays far from them, |Delta| > Delta_0

fig, ax = plt.subplots(figsize=(7.2 * style.CM, 6.2 * style.CM))
ax.set_aspect('equal'); ax.axis('off')
ax.add_patch(Rectangle((-np.pi, -np.pi), 2 * np.pi, 2 * np.pi, fc='none', ec=style.INK, lw=0.8))
for s in (1, -1):
    ax.plot([-np.pi, np.pi], [-s * np.pi, s * np.pi], color=style.BROKEN, lw=1.1)
ax.add_patch(Circle((0, 0), r, fc='none', ec=style.ACCENT, lw=1.6))
for cx in (np.pi, -np.pi):
    # the pocket around X is cut by the zone boundary, it is one pocket seen twice
    ax.add_patch(Circle((cx, 0), r, fc='none', ec=style.LIGHT, lw=1.6))
for s in (1, -1):
    for u in (1, -1):
        d = r / np.sqrt(2)
        ax.plot([s * d], [u * d], 'o', color=style.BROKEN, ms=4, zorder=5)
style.label(ax, 0, -1.95, r'$\Gamma$, four nodes', fontsize=8, color=style.ACCENT)
style.label(ax, np.pi - 0.45, -1.35, 'at $X$,\nno node', fontsize=7.5, color=style.LIGHT)
style.label(ax, 0, np.pi + 0.45, r'red lines, $k_x=\pm k_y$', fontsize=8.5, color=style.BROKEN)
ax.set_xlim(-np.pi - 0.35, np.pi + 0.35); ax.set_ylim(-np.pi - 0.2, np.pi + 0.8)
style.save(fig, __file__)
