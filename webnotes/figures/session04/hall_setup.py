"""Session 4, section 4.2, the geometry of the measurement of the Hall conductance.

A square two-dimensional electron gas with four contacts, B into the page, which for electrons gives edge channels that go around the sample counterclockwise. A voltage V_y is applied between the top and the
bottom contact, and the current I_x is read in the left contact. With the chemical potential in a gap with N
filled Landau levels, the current is carried by the N chiral edge channels of each edge, which go around the sample in one
sense. The channels that leave the top contact at the potential V_y end in the contact next to it, so
I_x = N (e^2/h) V_y, which is sigma_xy = N e^2/h. This is a drawing without computed data."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle
import style

fig, ax = plt.subplots(figsize=(style.WIDTH_CM * style.CM, 5.6 * style.CM))
ax.set_aspect('equal'); ax.axis('off')
S = 4.0
x0, y0 = 1.0, 0.6
ax.add_patch(Rectangle((x0, y0), S, S, fc='#e6eef6', ec=style.ACCENT, lw=1.4, zorder=1))
cw, ch = 1.5, 0.38
cont = {'top': (x0 + S / 2 - cw / 2, y0 + S - 0.0, cw, ch), 'bottom': (x0 + S / 2 - cw / 2, y0 - ch, cw, ch),
        'left': (x0 - ch, y0 + S / 2 - cw / 2, ch, cw), 'right': (x0 + S, y0 + S / 2 - cw / 2, ch, cw)}
for name, (a, b, w, h) in cont.items():
    ax.add_patch(Rectangle((a, b), w, h, fc=style.MUTED, ec=style.INK, lw=0.8, zorder=2))
# the edge channels, counterclockwise, slightly inside the border
d = 0.28
kw = dict(arrowstyle='-|>', mutation_scale=9, color=style.ACCENT, lw=1.6, zorder=3, shrinkA=0, shrinkB=0)
for (p, q) in (((x0 + d, y0 + d), (x0 + S - d, y0 + d)), ((x0 + S - d, y0 + d), (x0 + S - d, y0 + S - d)),
               ((x0 + S - d, y0 + S - d), (x0 + d, y0 + S - d)), ((x0 + d, y0 + S - d), (x0 + d, y0 + d))):
    pm = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    ax.add_patch(FancyArrowPatch(p, q, **kw))
# the field, into the page (a cross)
cx, cy = x0 + S / 2, y0 + S / 2
ax.add_patch(Circle((cx, cy), 0.28, fc='white', ec=style.INK, lw=1.0, zorder=4))
for sg in (1, -1):
    ax.plot([cx - 0.2, cx + 0.2][::sg], [cy - 0.2, cy + 0.2], color=style.INK, lw=1.2, zorder=5)
ax.text(cx + 0.45, cy - 0.05, r'$B$', fontsize=10, ha='left', va='center', zorder=5)
# the applied voltage and the measured current
ax.text(x0 + S / 2, y0 + S + ch + 0.12, r'$V_y$', color=style.BROKEN, fontsize=10, ha='center', va='bottom')
ax.text(x0 + S / 2, y0 - ch - 0.12, r'$0$', color=style.BROKEN, fontsize=10, ha='center', va='top')
ax.add_patch(FancyArrowPatch((x0 - ch - 0.02, y0 + S / 2), (x0 - ch - 1.5, y0 + S / 2), arrowstyle='-|>', mutation_scale=9,
                             color=style.BROKEN, lw=1.4, shrinkA=0, shrinkB=0, zorder=3))
ax.text(x0 - ch - 0.75, y0 + S / 2 + 0.2, r'$I_x$', color=style.BROKEN, fontsize=10, ha='center', va='bottom')
ax.text(cx, cy - 1.15, 'edge channels', color=style.ACCENT, fontsize=8.5, ha='center')
ax.set_xlim(-3.6, 9.4); ax.set_ylim(-0.35, 5.5)
for xe in (-3.6, 9.4):
    ax.add_patch(Rectangle((xe - 0.01, 0), 0.02, 0.02, fc='white', ec='none', zorder=0))
style.save(fig, __file__)
