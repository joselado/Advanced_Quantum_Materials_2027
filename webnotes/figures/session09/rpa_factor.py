"""Session 9, Eq. (9.6) in the charge and in the spin channel, the ratio chi/chi_0 as a function of U chi_0."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

x = np.linspace(0, 0.97, 400)
fig, ax = style.figure(height_cm=5.2, width_cm=9.5)
ax.plot(x, 1 / (1 - x), color=style.ACCENT)
ax.plot(x, 1 / (1 + x), color=style.BROKEN)
style.guide(ax, y=1)
style.guide(ax, x=1, ls=(0, (4, 3)))
ax.set_ylim(-1.2, 6); ax.set_xlim(0, 1.15)
style.arrows(ax, xlabel=r'$U\chi_0$', ylabel=r'$\chi/\chi_0$')
x0 = 0.68
for f, c in ((1 / (1 - x0), style.ACCENT), (1 / (1 + x0), style.BROKEN)):
    ax.plot([x0], [f], 'o', color=c, ms=4)
style.label(ax, 0.36, 3.6, r'spin, $1/(1-U\chi_0)$', color=style.ACCENT, fontsize=8)
style.label(ax, 0.55, -0.5, r'charge, $1/(1+U\chi_0)$', color=style.BROKEN, fontsize=8)
style.label(ax, 1.0, -1.7, r'$1$', fontsize=8.5)
style.label(ax, 0.68, -1.7, r'$0.68$', fontsize=8)
style.save(fig, __file__)
