"""Session 9, Eq. (9.6) in the charge and in the spin channel, the ratio chi/chi_0 as a function of U chi_0.

Redrawn on 2026-11-22 with ticks at the values that the caption quotes. The point U chi_0 = 0.68 is U=t on the
half-filled square lattice at T=0.1t, where chi_0(pi,pi) = 0.677/t. The asserts check the caption, the charge ratio
1/1.68 = 0.595, written 0.60, and the spin ratio 1/0.32 = 3.125, written 3.1."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

x0 = 0.68
charge, spin = 1 / (1 + x0), 1 / (1 - x0)
assert abs(1 + x0 - 1.68) < 1e-12 and abs(1 - x0 - 0.32) < 1e-12
assert round(charge, 2) == 0.60 and round(spin, 1) == 3.1 and abs(x0 / 1.68 - 0.405) < 1e-3

FS = 10
x = np.linspace(0, 0.97, 400)
fig, ax = plt.subplots(figsize=(9.5 * style.CM, 6.8 * style.CM))
style.arrows(ax, ticks=True)
ax.spines['bottom'].set_visible(True); ax.spines['left'].set_visible(True)
ax.annotate(r'$\chi/\chi_0$', xy=(0, 1.06), xycoords='axes fraction', ha='center', va='bottom', fontsize=FS)
ax.annotate(r'$U\chi_0$', xy=(1.03, 0), xycoords='axes fraction', ha='left', va='center', fontsize=FS)
ax.plot(x, 1 / (1 - x), color=style.ACCENT)
ax.plot(x, 1 / (1 + x), color=style.BROKEN)
style.guide(ax, y=1)
style.guide(ax, x=1, ls=(0, (4, 3)))
ax.plot([x0, x0], [0, spin], color=style.GRID, lw=0.8, zorder=0)
ax.set_ylim(0, 4.2); ax.set_xlim(0, 1.15)
ax.set_xticks([0, x0, 1]); ax.set_xticklabels(['0', '0.68', '1'])
ax.set_yticks([charge, 1, spin]); ax.set_yticklabels(['0.60', '1', '3.1'])
ax.tick_params(labelsize=FS, length=2.5, width=0.6)
for f, c in ((spin, style.ACCENT), (charge, style.BROKEN)):
    ax.plot([x0], [f], 'o', color=c, ms=4)
style.label(ax, 0.30, 2.1, r'spin, $1/(1-U\chi_0)$', color=style.ACCENT, fontsize=FS)
style.label(ax, 0.42, 0.42, r'charge, $1/(1+U\chi_0)$', color=style.BROKEN, fontsize=FS)
style.save(fig, __file__)
