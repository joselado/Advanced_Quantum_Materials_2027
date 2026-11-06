"""Session 9, quiz of Section 9.2, the inverse susceptibility with a line that reaches zero at T=-30 K."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

T = np.linspace(-30, 120, 100)
fig, ax = style.figure(height_cm=4.6, width_cm=8.5)
ax.plot(T[T >= 0], (T + 30)[T >= 0], color=style.ACCENT)
ax.plot(T[T <= 0], (T + 30)[T <= 0], color=style.ACCENT, ls=(0, (3, 2)))
ax.plot(T, T, color=style.MUTED, lw=1.0)
ax.plot([-30], [0], 'o', color=style.ACCENT, ms=3.5)
style.guide(ax, x=0, y=0)
ax.set_xlim(-45, 125); ax.set_ylim(-20, 160)
style.arrows(ax, xlabel=r'$T$ (K)', ylabel=r'$1/\chi$')
ax.plot([60, 60], [60, 90], '-', color=style.BROKEN, lw=1.2)
ax.plot([60, 60], [60, 90], 'o', color=style.BROKEN, ms=3)
style.label(ax, 56, 56, r'$60$', color=style.BROKEN, fontsize=8, ha='right')
style.label(ax, 56, 90, r'$90$', color=style.BROKEN, fontsize=8, ha='right')
style.label(ax, -30, -11, r'$-30$', fontsize=8)
style.label(ax, 12, 112, r'measured line', color=style.ACCENT, fontsize=8, ha='left')
style.label(ax, 108, 80, r'paramagnet', color=style.MUTED, fontsize=8)
style.save(fig, __file__)
