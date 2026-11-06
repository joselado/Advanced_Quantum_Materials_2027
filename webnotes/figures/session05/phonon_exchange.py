"""Session 5, an effective interaction mediated by a boson, here a phonon, and its sign as a function of frequency."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

fig, axs = plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.4 * style.CM),
                        gridspec_kw=dict(width_ratios=[1, 1.25]))
# (a) two electrons that exchange a phonon
ax = axs[0]
ax.axis('off')
for x in (0.0, 2.0):
    ax.annotate('', xy=(x, 3.0), xytext=(x, -0.2), arrowprops=dict(arrowstyle='-|>', color=style.ACCENT, lw=1.4, mutation_scale=10))
    style.label(ax, x, -0.7, r'$e^-$', fontsize=9)
y = np.linspace(0, 1, 200)
ax.plot(0.0 + 2.0 * y, 1.5 + 0.12 * np.sin(2 * np.pi * 7 * y), color=style.BROKEN, lw=1.4)
style.label(ax, 1.0, 2.05, 'phonon', color=style.BROKEN, fontsize=8.5)
style.label(ax, 1.0, 1.0, r'$g,\ \omega_0$', color=style.BROKEN, fontsize=8.5)
style.label(ax, 1.0, 3.5, '(a) the interaction passes\nthrough the lattice', fontsize=8.5)
ax.set_xlim(-0.8, 2.8); ax.set_ylim(-1.0, 4.0)

# (b) V_eff(w) = V_c + V_ph(w), with V_ph = -(2 g^2 / w0) / (1 - (w/w0)^2), in units of 2 g^2 / w0 and with V_c = 0.5
ax = axs[1]
Vc = 0.5
x = np.linspace(0, 2.6, 2000)
V = Vc - 1.0 / (1 - x**2)
V = np.where(abs(x - 1) < 0.02, np.nan, V)
ax.plot(x[x < 1], V[x < 1], color=style.ACCENT)
ax.plot(x[x > 1], V[x > 1], color=style.ACCENT)
style.guide(ax, y=0, color=style.MUTED)
style.guide(ax, y=Vc, color=style.BROKEN, lw=0.9, ls=(0, (3, 2)))
style.guide(ax, x=1, color=style.MUTED, lw=0.8, ls=(0, (3, 2)))
ax.axvspan(0, 1, color=style.GRID, alpha=0.45, lw=0, zorder=0)
style.arrows(ax, xlabel=r'$\omega$', ylabel=r'$V_\mathrm{eff}$')
style.label(ax, 1.0, -2.75, r'$\omega_0$', fontsize=8.5)
style.label(ax, 0.42, -0.3, 'attractive', color=style.ACCENT, fontsize=8.5)
style.label(ax, 2.0, 1.25, 'repulsive', color=style.ACCENT, fontsize=8.5)
style.label(ax, 2.35, Vc - 0.2, r'$V_c$', color=style.BROKEN, fontsize=8.5)
ax.set_xlim(0, 2.6); ax.set_ylim(-2.5, 2.1)
ax.set_yticks([]); 
style.label(ax, 1.3, 2.35, '(b) net sign of the channel', fontsize=8.5)
assert V[0] < 0 and V[-1] > 0
style.save(fig, __file__)
