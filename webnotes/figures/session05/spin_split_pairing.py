"""Session 5, an exchange field splits the two spin bands, so only a pair of equal spins sits on one Fermi surface."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

t, mu, h = 1.0, 0.0, 0.6
k = np.linspace(-np.pi, 4.9, 700)
e0 = -2 * t * np.cos(k) - mu
eu, ed = e0 - h, e0 + h                 # the exchange field of the model, -h(n_up - n_down)
kFu = np.arccos(-(mu + h) / (2 * t))    # eps_up(kFu)=0
kFd = np.arccos(-(mu - h) / (2 * t))    # eps_down(kFd)=0
# the checks of what the figure says: the two Fermi momenta differ, and the singlet pair (k up, -k down) costs 2h
assert kFu > kFd
assert abs((-2 * t * np.cos(kFu) - mu + h) - 2 * h) < 1e-9

fig, ax = style.figure(height_cm=6.0)
ax.plot(k, eu, color=style.ACCENT)
ax.plot(k, ed, color=style.BROKEN)
style.guide(ax, y=0)
for kk, c in [(kFu, style.ACCENT), (-kFu, style.ACCENT), (kFd, style.BROKEN), (-kFd, style.BROKEN)]:
    ax.plot([kk], [0], 'o', color=c, ms=4.5, zorder=5)
style.arrows(ax, xlabel=r'$k$', ylabel=r'$E$')
style.label(ax, -2.6, -2.45, r'$\uparrow$, $\varepsilon-h$', color=style.ACCENT, fontsize=8.5)
style.label(ax, -2.6, 3.0, r'$\downarrow$, $\varepsilon+h$', color=style.BROKEN, fontsize=8.5)
# the pair of equal spins sits on one Fermi surface, the singlet pair does not
ax.annotate('', xy=(kFu, 0.42), xytext=(-kFu, 0.42), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.9, shrinkA=0, shrinkB=0))
style.label(ax, 0, 0.85, r'$\uparrow\uparrow$ pair, both at $E=0$', fontsize=8)
# the singlet partner of the up electron at kFu is the down electron at -kFu, which sits 2h above E=0
ax.plot([kFu], [2 * h], 'o', mfc='white', mec=style.BROKEN, ms=4.5, zorder=5)
ax.annotate('', xy=(kFu, 2 * h - 0.06), xytext=(kFu, 0.06), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.9, shrinkA=0, shrinkB=0))
style.label(ax, kFu + 0.2, h, r'$2h$', ha='left', fontsize=8.5, bbox=dict(fc='white', ec='none', pad=0.6), zorder=6)
style.label(ax, 3.4, -2.3, r'open circle, the $\downarrow$ partner of the' + '\n' + r'$\uparrow$ electron, is $2h$ above $E=0$', fontsize=8)
ax.set_xlim(-np.pi, 4.9); ax.set_ylim(-3.3, 3.6)
style.save(fig, __file__)
