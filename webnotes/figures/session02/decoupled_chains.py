"""Session 2, a square lattice with the hopping along y switched off, and its band."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

t = 1.0
eps = lambda kx, ky: -2 * t * np.cos(kx)                         # no hopping along y
fig = plt.figure(figsize=(9.6 * style.CM, 4.0 * style.CM))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1], wspace=0.3)
axL = fig.add_subplot(gs[0]); axR = fig.add_subplot(gs[1])
axL.axis('off'); axL.set_aspect('equal')
for j in range(4):
    axL.plot([0, 4], [j, j], color=style.INK, lw=1.8, zorder=2)
    axL.scatter(np.arange(5), [j] * 5, s=30, color=style.ACCENT, zorder=3)
    for i in range(5):
        if j < 3: axL.plot([i, i], [j, j + 1], color=style.GRID, lw=1.0, ls=(0, (3, 3)), zorder=1)
style.label(axL, 2.0, -0.55, r'$t$ along $x$, $0$ along $y$', fontsize=8.5)
axL.set_xlim(-0.4, 4.4); axL.set_ylim(-0.9, 3.4)
g = np.linspace(-np.pi, np.pi, 24)
KX, KY = np.meshgrid(g, g)
Z = eps(KX, KY)
assert np.allclose(Z, Z[0:1, :])                                  # the same for every ky
axR.imshow(Z[::-1], extent=(-np.pi, np.pi, -np.pi, np.pi), cmap='Blues_r', alpha=0.85, vmin=-2, vmax=2.5, interpolation='nearest')
axR.plot([-np.pi, np.pi, np.pi, -np.pi, -np.pi], [-np.pi, -np.pi, np.pi, np.pi, -np.pi], color=style.MUTED, lw=0.9, ls=(0, (4, 3)))
style.arrows(axR, xlabel=r'$\varphi_x$', ylabel=r'$\varphi_y$')
axR.set_aspect('equal'); axR.set_xlim(-np.pi - 0.1, np.pi + 0.1); axR.set_ylim(-np.pi - 0.1, np.pi + 0.1)
axR.set_title('colors give the energy', fontsize=8, pad=18)
style.save(fig, __file__)
