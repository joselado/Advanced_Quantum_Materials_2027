"""Session 4, section 4.6, the Hall resistance of a two-dimensional electron gas at fixed density as the field grows.

N_eff is the number of Landau levels below the chemical potential, with each level filled in a window of width w
in the filling factor nu around its center, where nu = n h / (e B) is the number of filled levels at the field B.
The Hall resistance is R_xy = h / (N_eff e^2), and the classical Hall resistance is R_xy = B / (n e) = (h/e^2) / nu.
The model is in _g2_hall.py, which also checks the numbers of the caption. Redrawn on 2026-11-21 with the field in
units of B_1, the field where nu = 1, and with the ticks at 1/4, 1/3, 1/2 and 1 on both axes, where the classical
line crosses the plateaus."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
import _g2_hall as hall

flat, widths = hall.check()
print('flat part of the plateaus N = 1 to 4, in B/B_1:', {N: tuple(round(float(v), 3) for v in flat[N]) for N in flat})

x = np.linspace(0.1, hall.XMAX, 3000)
R = hall.quantum(x)

fig, ax = style.figure(width_cm=10.5, height_cm=6.4)
ax.set_xlim(0, 1.6)
ax.set_ylim(0, 1.45)
ax.plot(x, hall.classical(x), color=style.GRID, lw=1.4, ls=(0, (4, 2.5)), zorder=1)
ax.plot(x, R, color=style.ACCENT)
for N in (1, 2, 3, 4):
    style.guide(ax, y=1 / N, ls=':')
    ax.plot([1 / N], [1 / N], 'o', ms=3.2, color=style.INK, zorder=4)
for N, xl in ((1, 1.25), (2, 0.53), (3, 0.31)):
    style.label(ax, xl, 1 / N + 0.08, r'$N=%d$' % N, fontsize=8.5, color=style.ACCENT)
style.arrows(ax, xlabel=r'$B/B_1$', ylabel=r'$R_{xy}$ in units of $h/e^2$', ticks=True)
fr = [r'$\frac{1}{4}$', r'$\frac{1}{3}$', r'$\frac{1}{2}$', '1']
ax.set_xticks([0, 1 / 4, 1 / 3, 1 / 2, 1]); ax.set_xticklabels(['0'] + fr)
ax.set_yticks([1 / 4, 1 / 3, 1 / 2, 1]); ax.set_yticklabels(['$1/4$', '$1/3$', '$1/2$', '1'])
ax.tick_params(length=2.5, width=0.6)
style.label(ax, 1.38, 1.27, 'classical,\n$R_{xy}\\propto B$', fontsize=8.5, color=style.MUTED)
style.save(fig, __file__)
