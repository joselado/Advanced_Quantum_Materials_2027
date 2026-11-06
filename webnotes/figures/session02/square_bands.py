"""Session 2, the band of the square lattice of (2.14) along a path and over the Brillouin zone."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

t = 1.0
eps = lambda kx, ky: -2 * t * (np.cos(kx) + np.cos(ky))
assert np.isclose(eps(0, 0), -4 * t) and np.isclose(eps(np.pi, 0), 0) and np.isclose(eps(np.pi, np.pi), 4 * t)
fig, axs = style.figure(height_cm=5.6, ncols=2)
# (a) Gamma -> X -> M -> Gamma
ax = axs[0]
n = 120
s1 = np.linspace(0, np.pi, n); s2 = np.linspace(0, np.pi, n); s3 = np.linspace(np.pi, 0, n)
kp = np.r_[np.c_[s1, 0 * s1], np.c_[np.pi + 0 * s2, s2], np.c_[s3, s3]]
x = np.r_[s1, np.pi + s2, 2 * np.pi + (np.pi - s3) * np.sqrt(2)]
ax.plot(x, eps(kp[:, 0], kp[:, 1]), color=style.ACCENT)
for xx in (0, np.pi, 2 * np.pi, 2 * np.pi + np.pi * np.sqrt(2)):
    style.guide(ax, x=xx)
style.guide(ax, y=0)
style.arrows(ax, xlabel='', ylabel=r'$\epsilon/t$')
ax.set_xticks([0, np.pi, 2 * np.pi, 2 * np.pi + np.pi * np.sqrt(2)])
ax.set_xticklabels([r'$\Gamma$', r'$X$', r'$M$', r'$\Gamma$'])
ax.set_yticks([-4, 0, 4]); ax.set_yticklabels([r'$-4$', r'$0$', r'$4$'])
ax.set_ylim(-4.6, 4.6); ax.set_xlim(0, 2 * np.pi + np.pi * np.sqrt(2))
# (b) contour lines over the Brillouin zone
ax = axs[1]
g = np.linspace(-np.pi, np.pi, 300)
KX, KY = np.meshgrid(g, g)
Z = eps(KX, KY)
ax.contour(KX, KY, Z, levels=[-3, -2, -1, 1, 2, 3], colors=style.LIGHT, linewidths=1.0, linestyles='solid')
ax.contour(KX, KY, Z, levels=[0], colors=style.BROKEN, linewidths=1.8)
ax.plot([-np.pi, np.pi, np.pi, -np.pi, -np.pi], [-np.pi, -np.pi, np.pi, np.pi, -np.pi], color=style.MUTED, lw=0.9, ls=(0, (4, 3)))
ax.scatter([0], [0], s=14, color=style.INK, zorder=4); style.label(ax, 0.3, -0.4, r'$\Gamma$', fontsize=8.5)
ax.scatter([np.pi, np.pi], [np.pi, -np.pi], s=14, color=style.INK, zorder=4)
style.label(ax, 2.55, 2.8, r'$M$', fontsize=8.5)
style.arrows(ax, xlabel=r'$\varphi_x$', ylabel=r'$\varphi_y$')
ax.set_aspect('equal'); ax.set_xlim(-np.pi - 0.1, np.pi + 0.1); ax.set_ylim(-np.pi - 0.1, np.pi + 0.1)
fig.subplots_adjust(wspace=0.3)
style.save(fig, __file__)
