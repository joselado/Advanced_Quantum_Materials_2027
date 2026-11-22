"""Session 5, an effective interaction mediated by a boson, here a phonon, and its sign as a function of frequency.

Redrawn on 2026-11-21 under the same name, with the axes of panel (b) in units and with ticks: V_eff in units of
2 g^2 / omega_0 with the ticks -0.5, 0 and V_c = 0.5, and omega in units of omega_0 with the tick 1. Panel (a) is a
drawing and stays a drawing."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

plt.rcParams.update({'font.size': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5})   # readable at 390 px
fig, axs = plt.subplots(1, 2, figsize=(12.5 * style.CM, 6.0 * style.CM),
                        gridspec_kw=dict(width_ratios=[1, 1.45]))
# (a) two electrons that exchange a phonon
ax = axs[0]
ax.axis('off')
for x in (0.0, 2.0):
    ax.annotate('', xy=(x, 3.0), xytext=(x, -0.2), arrowprops=dict(arrowstyle='-|>', color=style.ACCENT, lw=1.4, mutation_scale=10))
    style.label(ax, x, -0.7, r'$e^-$', fontsize=11)
y = np.linspace(0, 1, 200)
ax.plot(0.0 + 2.0 * y, 1.5 + 0.12 * np.sin(2 * np.pi * 7 * y), color=style.BROKEN, lw=1.4)
style.label(ax, 1.0, 2.1, 'phonon', color=style.BROKEN, fontsize=10.5)
style.label(ax, 1.0, 0.95, r'$g,\ \omega_0$', color=style.BROKEN, fontsize=10.5)
style.label(ax, 1.0, 3.6, '(a) the interaction passes\nthrough the lattice', fontsize=10)
ax.set_xlim(-0.8, 2.8); ax.set_ylim(-1.0, 4.0)

# (b) V_eff(w) = V_c + V_ph(w), with V_ph = -(2 g^2 / w0) / (1 - (w/w0)^2), in units of 2 g^2 / w0 and with V_c = 0.5
ax = axs[1]
Vc = 0.5
x = np.linspace(0, 2.6, 2000)
V = Vc - 1.0 / (1 - x**2)
V = np.where(abs(x - 1) < 0.02, np.nan, V)
# the numbers of the caption: V_eff(0) = V_c - 1 = -0.5, negative for every omega < omega_0, positive above omega_0
below, above = x < 0.98, x > 1.02
assert abs(V[0] + 0.5) < 1e-12 and np.all(V[below] <= -0.5 + 1e-12) and np.all(V[above] > Vc)
# above omega_0 it goes down towards V_c at high frequency
w = np.linspace(1.05, 200, 4000)
assert np.all(np.diff(Vc - 1.0 / (1 - w**2)) < 0) and abs(Vc - 1.0 / (1 - 200.0**2) - Vc) < 1e-4
ax.plot(x[x < 1], V[x < 1], color=style.ACCENT)
ax.plot(x[x > 1], V[x > 1], color=style.ACCENT)
style.guide(ax, y=0, color=style.MUTED, lw=0.8)
style.guide(ax, y=Vc, color=style.BROKEN, lw=0.9, ls=(0, (3, 2)))
style.guide(ax, x=1, color=style.MUTED, lw=0.8, ls=(0, (3, 2)))
ax.axvspan(0, 1, color=style.GRID, alpha=0.45, lw=0, zorder=0)
ax.set_xlim(0, 2.6); ax.set_ylim(-2.5, 2.1)
style.arrows(ax, xlabel=r'$\omega/\omega_0$', ylabel=r'$V_\mathrm{eff}$ in units of $2g^2/\omega_0$', ticks=True)
ax.set_xticks([0, 1, 2]); ax.set_xticklabels(['0', '1', '2'])
ax.set_yticks([-0.5, 0, 0.5]); ax.set_yticklabels([r'$-0.5$', '0', '0.5'])
ax.tick_params(length=2.5, width=0.6)
style.label(ax, 0.33, -2.0, 'attractive', color=style.ACCENT, fontsize=10)
style.label(ax, 2.0, 1.3, 'repulsive', color=style.ACCENT, fontsize=10)
style.label(ax, 2.45, Vc - 0.3, r'$V_c$', color=style.BROKEN, fontsize=10.5)
style.label(ax, 2.6, 2.5, '(b) net sign', fontsize=10, ha='right')
style.save(fig, __file__)
