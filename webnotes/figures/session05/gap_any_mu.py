"""Session 5, the minimum of the quasiparticle energy is |Delta| at the Fermi momentum, for any chemical potential."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

t, D = 1.0, 0.3
k = np.linspace(0, np.pi, 600)
fig, ax = style.figure(height_cm=5.6)
cols = [style.ACCENT, style.BROKEN, style.LIGHT]
for mu, col in zip((-1.2, 0.0, 1.2), cols):
    eps = -2 * t * np.cos(k) - mu
    E = np.sqrt(eps**2 + D**2)
    ax.plot(k, E, color=col)
    kF = np.arccos(-mu / (2 * t))
    i = np.argmin(E)
    assert abs(E[i] - D) < 1e-3 and abs(k[i] - kF) < 0.01
    ax.plot([kF], [D], 'o', color=col, ms=4)
    style.guide(ax, x=kF, color=col, lw=0.7, ls=(0, (3, 2)))
    ax.text(kF, -0.12, r'$k_F$', color=col, ha='center', va='top', fontsize=8.5)
style.guide(ax, y=D, color=style.MUTED, lw=0.8, ls=(0, (3, 2)))
style.label(ax, 3.0, D + 0.06, r'$|\Delta|$', fontsize=8.5, ha='left', va='bottom')
for yy, mu_s, col in ((1.62, '-1.2t', cols[0]), (1.4, '0', cols[1]), (1.18, '1.2t', cols[2])):
    style.label(ax, 0.08, yy, r'$\mu=%s$' % mu_s, color=col, fontsize=8.5, ha='left')
style.arrows(ax, xlabel=r'$k$', ylabel=r'$E(k)$')
ax.set_xlim(0, np.pi); ax.set_ylim(0, 1.75)
style.save(fig, __file__)
