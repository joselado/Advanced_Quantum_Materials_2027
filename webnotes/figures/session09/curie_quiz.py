"""Session 9, quiz of Section 9.2, the inverse susceptibility with a line that reaches zero at T=-30 K.

Redrawn on 2026-11-22 with the axes of the rule of 2026-11-21: ticks at T = -30, 0 and 60 K and at 1/chi = 60 and 90,
the values that the quiz quotes. Both lines have the Curie constant C = 1 of 1/chi = (T - theta)/C, as a free spin in
the units of the steps fold of Section 9.2, so 1/chi is in kelvin. The measured line is solid from 40 K up, where we
measure, and dashed down to its intercept. The asserts compare it with the self-consistent mean field of
_g1_curie.loop for an antiferromagnet with z|J| = 30 K."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
import _g1_curie

THETA = -30.0
inv60 = _g1_curie.loop(60.0, THETA)
assert abs(inv60 - 90) < 1e-4 and abs(_g1_curie.loop(60.0, 0.0) - 60) < 1e-4 and abs(_g1_curie.loop(90.0, THETA) - 120) < 1e-4
print('1/chi at 60 K: measured line %.4f, paramagnet %.4f' % (inv60, _g1_curie.loop(60.0, 0.0)))

fig, ax = style.figure(height_cm=4.8, width_cm=8.5)
style.arrows(ax, xlabel=r'$T$ (K)', ylabel=r'$1/\chi$ (K)', ticks=True)
T = np.linspace(40, 120, 100)
ax.plot(T, T - THETA, color=style.ACCENT)
T = np.linspace(THETA, 40, 100)
ax.plot(T, T - THETA, color=style.ACCENT, ls=(0, (3, 2)), lw=1.2)
T = np.linspace(0, 120, 100)
ax.plot(T, T, color=style.MUTED, lw=1.0)
ax.plot([THETA], [0], 'o', color=style.ACCENT, ms=3.5, zorder=5)
style.guide(ax, x=0, y=0)
ax.set_xlim(-45, 125); ax.set_ylim(-20, 160)
ax.plot([60, 60], [60, 90], '-', color=style.BROKEN, lw=1.2)
ax.plot([60, 60], [60, 90], 'o', color=style.BROKEN, ms=3)
ax.plot([-45, 60], [90, 90], color=style.GRID, lw=0.8, zorder=0)
ax.plot([-45, 60], [60, 60], color=style.GRID, lw=0.8, zorder=0)
ax.set_xticks([-30, 0, 60]); ax.set_xticklabels([r'$-30$', r'$0$', r'$60$'], fontsize=8.5)
ax.set_yticks([0, 60, 90]); ax.set_yticklabels([r'$0$', r'$60$', r'$90$'], fontsize=8.5)
ax.tick_params(length=2.5, width=0.6, pad=2)
style.label(ax, 10, 125, r'measured line', color=style.ACCENT, fontsize=8, ha='left')
style.label(ax, 104, 78, r'paramagnet', color=style.MUTED, fontsize=8)
style.save(fig, __file__)
