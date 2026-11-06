"""Session 9, a sketch of the mobility edges of the three-dimensional Anderson model, w_n uniform in [-W,W]."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

Wc = 8.25      # 16.5 t for a box of full width 16.5 t, i.e. w_n in [-W,W] with W = 8.25 t (numerical result, band center)
W = np.linspace(0, Wc, 200)
Ec = 6 * np.sqrt(1 - (W / Wc) ** 2)      # a guide for the eye, only the end point W_c is a computed number
Wl = np.linspace(0, 12, 200)
edge = 6 + Wl

fig, ax = style.figure(height_cm=6.0, width_cm=10.5)
ax.fill_between(W, -Ec, Ec, color=style.LIGHT, alpha=0.35, lw=0)
ax.fill_between(Wl, Ec.max() * 0 - edge, edge, color=style.WARM, alpha=0.18, lw=0, zorder=0)
ax.fill_between(W, -Ec, Ec, color=style.LIGHT, alpha=0.35, lw=0)
ax.plot(Wl, edge, color=style.MUTED, lw=1.0); ax.plot(Wl, -edge, color=style.MUTED, lw=1.0)
ax.plot(W, Ec, color=style.ACCENT); ax.plot(W, -Ec, color=style.ACCENT)
ax.set_xlim(0, 12.5); ax.set_ylim(-13, 13)
style.arrows(ax, xlabel=r'$W/t$', ylabel=r'$E/t$')
style.guide(ax, y=0)
style.label(ax, 2.6, 0, 'extended', color=style.ACCENT, fontsize=8.5)
style.label(ax, 7.0, 7.8, 'localized', color=style.BROKEN, fontsize=8.5)
style.label(ax, 4.0, 7.4, r'$E_c$', color=style.ACCENT, fontsize=8.5)
style.label(ax, 9.6, -1.8, r'$W_c\approx8t$', color=style.INK, fontsize=8.5)
ax.plot([Wc], [0], 'o', color=style.ACCENT, ms=4)
ax.plot([10.5], [0], 'o', color=style.BROKEN, ms=4)
style.label(ax, 11.3, 0.9, r'$E_F$', color=style.BROKEN, fontsize=8.5)
style.save(fig, __file__)
