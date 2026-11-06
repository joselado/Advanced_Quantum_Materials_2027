"""Session 4, section 4.7, the phases of the four bonds of one plaquette in the two gauges, in units of the flux phi of the plaquette.

For the plaquette with the lower left corner at (x, y) = (2, 1), the phases of (4.4) along the bonds taken counterclockwise are
Landau gauge A = B(0, x): 0, (x+1) phi, 0, -x phi. Symmetric gauge A = (B/2)(-y, x): -y phi/2, (x+1) phi/2, (y+1) phi/2, -x phi/2.
The sums are checked below, and both are phi."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import style

x, y = 2, 1
landau = [0.0, (x + 1), 0.0, -x]                         # bottom, right, top, left, in units of phi
sym = [-y / 2, (x + 1) / 2, (y + 1) / 2, -x / 2]
assert abs(sum(landau) - 1) < 1e-12 and abs(sum(sym) - 1) < 1e-12


def fmt(v):
    if v == 0:
        return '0'
    sign = '-' if v < 0 else ''
    a = abs(v)
    if a == 1:
        return sign + r'\varphi'
    if a % 1:
        return sign + r'\frac{%d}{2}\varphi' % round(2 * a)
    return sign + '%d\\,\\varphi' % a


fig, axs = plt.subplots(1, 2, figsize=(10.5 * style.CM, 3.9 * style.CM), gridspec_kw=dict(wspace=0.15))
for ax, ph, title in ((axs[0], landau, '(a) Landau gauge'), (axs[1], sym, '(b) symmetric gauge')):
    ax.set_xlim(-1.0, 2.0); ax.set_ylim(-0.75, 1.55); ax.set_aspect('equal'); ax.axis('off')
    corners = [(0, 0), (1, 0), (1, 1), (0, 1)]
    for i in range(4):
        p, q = corners[i], corners[(i + 1) % 4]
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle='-|>', mutation_scale=9, color=style.ACCENT, lw=1.6, shrinkA=2, shrinkB=2))
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        off = [(0, -0.17), (0.1, 0), (0, 0.17), (-0.1, 0)][i]
        ha = ['center', 'left', 'center', 'right'][i]
        ax.text(mx + off[0], my + off[1], '$' + fmt(ph[i]) + '$', ha=ha, va='center', fontsize=8.5, color=style.INK)
    for c in corners:
        ax.plot(*c, 'o', color=style.INK, ms=3)
    ax.text(0.5, 0.5, r'$\sum=\varphi$', ha='center', va='center', fontsize=9, color=style.BROKEN)
    ax.text(0.5, -0.62, title, ha='center', va='top', fontsize=8.5)
style.save(fig, __file__)
