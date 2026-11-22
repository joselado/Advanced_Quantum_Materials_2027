"""Session 10, the order parameter m of Eq. (10.9) for the 2D Ising model, from the exact result of Onsager.

|m| = (1 - sinh^-4(2J/k_BT))^(1/8) below T_c = 2J/ln(1+sqrt 2) and zero above, with k_B = 1 and the temperature in
units of J. A formula and not a pyqula calculation, so numpy and no button. The numbers of the caption are asserted."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style
style.plt.rcParams.update({'font.size': 11, 'axes.labelsize': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5})

Tc = 2 / np.log(1 + np.sqrt(2))                      # in units of J, with k_B = 1
assert abs(np.sinh(2 / Tc) - 1) < 1e-12 and round(Tc, 2) == 2.27
# a grid that gets dense at T_c, where |m| goes to zero as (T_c - T)^(1/8)
T = np.concatenate([np.linspace(0.05, Tc - 1e-3, 1500), Tc - np.geomspace(1e-3, 1e-14, 300)])
m = (1 - np.sinh(2 / T) ** -4) ** (1 / 8)
assert m.max() > 0.9999 and m[T < 1.5].min() > 0.98                 # close to one well below T_c
assert round(np.interp(1.5, T, m), 2) == 0.99 and np.interp(2.2, T, m) < 0.8   # 0.99 at 1.5, 0.78 at 2.2
T = np.concatenate([T, [Tc, 3.6]])
m = np.concatenate([m, [0, 0]])

fig, ax = style.figure(height_cm=5.2, width_cm=10.5)
ax.plot(T, m, color=style.ACCENT)
style.guide(ax, x=Tc, color=style.BROKEN, lw=1.0, ls=(0, (4, 2.5)))
style.arrows(ax, xlabel=r'$k_BT/J$', ylabel=r'$|m|$', ticks=True)
ax.set_xlim(0, 3.7); ax.set_ylim(0, 1.12)
ax.set_xticks([0, 1, Tc, 3]); ax.set_xticklabels(['0', '1', '2.27', '3'])
ax.set_yticks([0, 0.5, 1]); ax.set_yticklabels(['0', '0.5', '1'])
ax.tick_params(length=2.5, pad=2)
style.label(ax, Tc + 0.05, 1.03, r'$T_c$', color=style.BROKEN, fontsize=11.5, ha='left')
style.label(ax, 0.9, 0.82, 'ordered', color=style.ACCENT, fontsize=11)
style.label(ax, 3.0, 0.14, 'disordered', color=style.ACCENT, fontsize=11)
style.save(fig, __file__)
