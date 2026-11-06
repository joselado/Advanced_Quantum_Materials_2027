"""Session 1, the filling of the bands in a metal, an insulator and a doped semiconductor."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

t, m = 1.0, 0.6
fig, axs = style.figure(height_cm=4.6, ncols=4)
k = np.linspace(-np.pi, np.pi, 500)
q = np.linspace(-np.pi / 2, np.pi / 2, 501)
metal = -2 * t * np.cos(k)
Ec = np.sqrt(m ** 2 + (2 * t * np.sin(q)) ** 2)           # chain with two different sites per cell, gap 2m
assert abs(Ec.min() - m) < 1e-6
titles = ['metal', 'insulator', 'n-doped', 'p-doped']
for a, ti in zip(axs, titles):
    a.set_title(ti, fontsize=8.5, pad=9)
    style.guide(a, y=0)
    a.set_ylim(-2.6, 2.6)
# (a) metal, half filled band, the states below E_F=0 are occupied
a = axs[0]
a.plot(k, metal, color=style.GRID, lw=1.2)
occ = np.abs(k) < np.pi / 2
a.plot(k[occ], metal[occ], color=style.ACCENT)
a.axhline(0, color=style.BROKEN, lw=0.9, ls=(0, (4, 3)))
a.set_xlim(-np.pi, np.pi)
style.arrows(a, xlabel=r'$k$', ylabel=r'$E$')
# (b) insulator, full valence band, empty conduction band
def two_bands(a, EF, mark):
    a.plot(q, Ec, color=style.ACCENT); a.plot(q, -Ec, color=style.ACCENT)
    a.axhline(EF, color=style.BROKEN, lw=0.9, ls=(0, (4, 3)))
    a.set_xlim(-np.pi / 2, np.pi / 2)
    style.arrows(a, xlabel=r'$k$', ylabel=r'$E$')
    if mark == 'n':
        sel = Ec < EF
        a.plot(q[sel], Ec[sel], color=style.BROKEN, lw=3.0, solid_capstyle='butt')
        for x in (-0.28, 0.28): a.scatter([x], [np.sqrt(m ** 2 + (2 * t * np.sin(x)) ** 2)], s=12, color=style.BROKEN, zorder=5)
    if mark == 'p':
        sel = -Ec > EF
        a.plot(np.where(~sel, q, np.nan), -Ec, color=style.ACCENT, lw=1.8)
        a.plot(q[sel], -Ec[sel], color=style.BROKEN, lw=3.0, solid_capstyle='butt')
two_bands(axs[1], 0.0, None)
two_bands(axs[2], m + 0.35, 'n')
two_bands(axs[3], -m - 0.35, 'p')
# the carriers: states of the conduction band below E_F, and empty states of the valence band above E_F
assert (Ec < m + 0.35).sum() > 0 and (-Ec > -m - 0.35).sum() > 0
axs[1].annotate('', xy=(1.25, m), xytext=(1.25, -m), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.8, shrinkA=0, shrinkB=0))
style.label(axs[1], 0.0, 0.3, 'gap', fontsize=8, color=style.INK)
style.label(axs[0], 2.2, 0.28, r'$E_F$', color=style.BROKEN, fontsize=8.5)
style.label(axs[2], -1.15, m + 0.55, r'$E_F$', color=style.BROKEN, fontsize=8.5)
style.label(axs[3], -1.2, -m - 0.05, r'$E_F$', color=style.BROKEN, fontsize=8.5)
fig.subplots_adjust(wspace=0.25)
style.save(fig, __file__)
