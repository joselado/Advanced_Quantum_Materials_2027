"""Session 3, section 3.6, the Hall conductivity of equally spaced Landau levels against the chemical potential, for
three temperatures.

The levels are at n + 1/2 in units of hbar omega_c, and each of them has the Chern number 1. In a clean system the Hall
conductivity is e^2/h times the sum of the occupations of the levels, which are Fermi functions of the chemical
potential mu. The plateau is quantified by the part of the first gap, 1/2 < mu < 3/2, where the value is within one
percent of e^2/h. This is a formula and not a diagonalization, so it has no pyqula script."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from scipy.special import expit
import style

levels = np.arange(60) + 0.5


def sigma(mu, kT):
    return expit((np.atleast_1d(mu)[:, None] - levels[None]) / kT).sum(1)


Ts = (0.02, 0.1, 0.3)
flat = {}
for kT in Ts:
    m = np.linspace(0.5, 1.5, 200001)
    flat[kT] = np.mean(np.abs(sigma(m, kT) - 1) < 0.01)
print('part of the first gap within one percent of e^2/h', flat)
assert abs(flat[0.02] - 0.82) < 0.005 and abs(flat[0.1] - 0.14) < 0.005 and abs(flat[0.3] - 0.02) < 0.005

mu = np.linspace(0, 3.6, 900)
fig, ax = style.figure(height_cm=6.0, width_cm=9.6)
ax.set_xlim(0, 3.6); ax.set_ylim(0, 3.75)
for n in range(4):
    style.guide(ax, x=n + 0.5, ls=':')
for c in (1, 2, 3):
    style.guide(ax, y=c, ls=':')
for kT, col, lw in zip(Ts, (style.ACCENT, style.LIGHT, style.BROKEN), (1.9, 1.7, 1.7)):
    ax.plot(mu, sigma(mu, kT), color=col, lw=lw)
style.plt.rcParams.update({'font.size': 11})
style.arrows(ax, xlabel=r'$\mu/\hbar\omega_c$', ylabel=r'$\sigma_{xy}$ in units of $e^2/h$', ticks=True)
ax.set_xticks([0.5, 1.5, 2.5, 3.5]); ax.set_xticklabels([r'$\frac{1}{2}$', r'$\frac{3}{2}$', r'$\frac{5}{2}$', r'$\frac{7}{2}$'], fontsize=13)
ax.set_yticks([0, 1, 2, 3]); ax.set_yticklabels(['0', '1', '2', '3'], fontsize=11)
ax.tick_params(length=2.5, width=0.6)
style.label(ax, 2.58, 1.78, r'$k_BT=0.02\,\hbar\omega_c$', color=style.ACCENT, fontsize=10, ha='left')
style.label(ax, 2.58, 1.47, r'$k_BT=0.1\,\hbar\omega_c$', color=style.LIGHT, fontsize=10, ha='left')
style.label(ax, 2.58, 1.16, r'$k_BT=0.3\,\hbar\omega_c$', color=style.BROKEN, fontsize=10, ha='left')
style.save(fig, __file__)
