"""Session 4, section 4.6, the Hall resistance of a two-dimensional electron gas at fixed density as the field grows.

N_eff is the number of Landau levels below the chemical potential, with each level filled in a window of width w
in the filling factor nu around its center, where nu = n h / (e B) is the number of filled levels at the field B.
The Hall resistance is R_xy = h / (N_eff e^2), and the classical Hall resistance is R_xy = B / (n e) = (h/e^2) / nu."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

x = np.linspace(0.1, 1.55, 3000)         # B in units of the field B1 at which nu = 1
nu = 1 / x
w = 0.05
Neff = sum(0.5 * (1 + np.tanh((nu - (n - 0.5)) / w)) for n in range(1, 40))
R = 1 / Neff

fig, ax = style.figure(height_cm=5.8)
ax.set_xlim(0, 1.6)
ax.set_ylim(0, 1.45)
ax.plot(x, x, color=style.GRID, lw=1.4, ls=(0, (4, 2.5)), zorder=1)
ax.plot(x, R, color=style.ACCENT)
for N in (1, 2, 3, 4):
    style.guide(ax, y=1 / N, ls=':')
for N in (1, 2, 3):
    style.label(ax, 1.0 / N + 0.1, 1 / N + 0.07, r'$N=%d$' % N, fontsize=8.5, color=style.ACCENT)
style.arrows(ax, xlabel=r'$B$', ylabel=r'$R_{xy}\,e^2/h$')
style.label(ax, 1.42, 1.2, 'classical,\n$R_{xy}\\propto B$', fontsize=8.5, color=style.MUTED)
ax.text(0.0, -0.07, '0', ha='center', va='top', fontsize=8.5)
style.save(fig, __file__)
