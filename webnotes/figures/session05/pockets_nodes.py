"""Session 5, section 5.10, a d-wave gap has nodes on the zone diagonals, and only a Fermi pocket that reaches them has gapless
points.

A map of Delta_d / Delta_0 = cos kx - cos ky of (5.13) over reciprocal space, in the extended zone with the first Brillouin zone
dashed, with two pockets of radius 0.5, one around Gamma and one around X = (pi, 0). The pocket at X sits on the edge of the zone,
so in the extended zone it shows at (pi, 0) and at (-pi, 0), which are the same point. The momenta are in units of the inverse
lattice constant. This draws a formula, so it is numpy and has no pyqula script."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import style

r = 0.5
th = np.linspace(0, 2 * np.pi, 3600, endpoint=False) + 1e-4     # no point of the grid on a diagonal


def gap_on(cx, cy):
    """|cos kx - cos ky| on the pocket of radius r around (cx, cy)."""
    kx, ky = cx + r * np.cos(th), cy + r * np.sin(th)
    return np.abs(np.cos(kx) - np.cos(ky))


gG, gX = gap_on(0, 0), gap_on(np.pi, 0)
zeros = th[1:][np.diff(np.sign(np.cos(r * np.cos(th)) - np.cos(r * np.sin(th)))) != 0]
assert gG.min() < 2e-3 and len(zeros) == 4                                     # the pocket at Gamma crosses the diagonals 4 times
assert np.allclose(np.sort(zeros), np.pi / 4 * np.array([1, 3, 5, 7]), atol=2e-3)
assert abs(gX.min() - 1.876) < 1e-3 and abs(gX.max() - 1.878) < 1e-3          # close to 2 and below it at X
assert gX.max() < 2 and round(gX.min(), 2) == round(gX.max(), 2) == 1.88       # the caption: 1.88, just below 2
print('pocket at Gamma: zeros at theta/pi', np.round(np.sort(zeros) / np.pi, 3), ' pocket at X: |Delta_d|/Delta_0 from',
      round(gX.min(), 4), 'to', round(gX.max(), 4))

N = 96
B = 2 * np.pi * np.eye(2)
u = np.arange(N) / N
values = np.cos(2 * np.pi * u)[:, None] - np.cos(2 * np.pi * u)[None, :]
fig, ax = plt.subplots(figsize=(7.4 * style.CM, 6.2 * style.CM))
half = 1.3 * np.pi
im = style.kmap(ax, B, values, half=half, cmap='RdBu_r', vmin=-2, vmax=2)
for c in ((0, 0), (np.pi, 0), (-np.pi, 0)):
    ax.add_patch(Circle(c, r, fc='none', ec=style.INK, lw=1.5, zorder=6))
d = r / np.sqrt(2)
for sx in (1, -1):
    for sy in (1, -1):
        ax.plot([sx * d], [sy * d], 'o', color=style.INK, ms=3.2, zorder=7)
ax.text(0.0, -r - 0.18, r'$\Gamma$', ha='center', va='top', fontsize=11, zorder=7)
ax.text(np.pi - r - 0.12, 0.0, r'$X$', ha='right', va='center', fontsize=11, zorder=7)
style.kaxes(ax, ticks=None, fontsize=11)
ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=10.5)
ax.set_yticks([-np.pi, 0, np.pi]); ax.set_yticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=10.5)
ax.tick_params(length=2.5, width=0.6, pad=2)
cb = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.04, aspect=14, ticks=[-2, 0, 2])
cb.ax.set_yticklabels(['$-2$', '0', '2'], fontsize=10.5)
cb.set_label(r'$\Delta_d/\Delta_0$', fontsize=11, labelpad=2)
cb.outline.set_linewidth(0.5); cb.ax.tick_params(length=2, width=0.5)
style.save(fig, __file__)
