"""Session 3, section 3.6, the chiral modes of a quantum Hall ribbon with the chemical potential between the second
and the third Landau level.

The continuum ribbon of width W=12 l_B with hard walls. In the Landau gauge each k_y gives the oscillator
H = p^2/2 + (x - x0)^2/2 in units of hbar omega_c and l_B, with x0 = k_y l_B^2, on 0<x<W with zero at the walls. The levels are
found by finite differences on 1500 points. The flat levels are n+1/2, and each of the two walls bends the levels up.
The chemical potential mu=2 is between 3/2 and 5/2, and the circles are the crossings."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from scipy.linalg import eigh_tridiagonal
import style

W, Npts, mu, nlev = 12.0, 1500, 2.0, 5
x = np.linspace(0, W, Npts + 2)[1:-1]
h = x[1] - x[0]
ks = np.linspace(-3.5, W + 3.5, 500)
E = np.array([eigh_tridiagonal(1 / h ** 2 + 0.5 * (x - k) ** 2, -0.5 / h ** 2 * np.ones(Npts - 1),
                               select='i', select_range=(0, nlev - 1))[0] for k in ks])
print('bulk levels', E[250, :4])
assert np.allclose(E[250, :4], np.arange(4) + 0.5, atol=1e-3)

fig, ax = style.figure(width_cm=10.5, height_cm=5.2)
ax.set_xlim(ks[0], ks[-1]); ax.set_ylim(0, 4.2)
for n in range(nlev):
    left = ks < W / 2
    ax.plot(ks[left], E[left, n], color=style.ACCENT)
    ax.plot(ks[~left], E[~left, n], color=style.BROKEN)
ax.axhline(mu, color=style.INK, lw=0.8, ls=(0, (4, 2.5)), zorder=0)
n_cross = 0
for n in range(nlev):
    for side in (ks < W / 2, ks >= W / 2):
        k, e = ks[side], E[side, n]
        i = np.where(np.diff(np.sign(e - mu)) != 0)[0]
        for j in i:
            kc = k[j] + (mu - e[j]) / (e[j + 1] - e[j]) * (k[j + 1] - k[j])
            ax.plot([kc], [mu], 'o', ms=4.5, mfc='white', mec=style.INK, mew=0.9, zorder=5)
            n_cross += 1
print('crossings', n_cross)
assert n_cross == 4
style.arrows(ax, xlabel=r'$k_y\ell_B$', ylabel=r'$E/\hbar\omega_c$')
style.label(ax, W / 2, mu + 0.22, r'$\mu$', fontsize=9)
style.label(ax, -2.0, 0.6, 'left edge\n$v_y<0$', color=style.ACCENT, fontsize=8.5)
style.label(ax, W + 2.0, 0.6, 'right edge\n$v_y>0$', color=style.BROKEN, fontsize=8.5)
style.label(ax, W / 2, 0.2, 'bulk levels', color=style.MUTED, fontsize=8)
style.save(fig, __file__)
