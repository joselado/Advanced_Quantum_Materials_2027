"""Session 3, section 3.5, the sum of the Berry curvature on a coarse k-mesh.

The two-band model d = (sin kx, sin ky, m + cos kx + cos ky) with m=-1.9, so that the mass at Gamma is 0.1. The curvature of
the lower band is Omega = (1/2) d.(d_kx d x d_ky d)/|d|^3, up to a sign, and the sum is (1/2 pi) sum_k Omega dk^2 on a mesh of
nk x nk points that includes Gamma. Panel (a) is Omega on the line ky=0 with the points of the mesh nk=8. Panel (b) is the sum against nk."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

m = -1.9


def omega(kx, ky):
    d = np.array([np.sin(kx), np.sin(ky), m + np.cos(kx) + np.cos(ky)])
    dx = np.array([np.cos(kx), 0 * kx, -np.sin(kx)])
    dy = np.array([0 * kx, np.cos(ky), -np.sin(ky)])
    return 0.5 * (d * np.cross(dx, dy, axis=0)).sum(0) / np.sqrt((d ** 2).sum(0)) ** 3


def csum(nk):
    k = 2 * np.pi * np.arange(nk) / nk
    KX, KY = np.meshgrid(k, k, indexing='ij')
    return omega(KX, KY).sum() * (2 * np.pi / nk) ** 2 / (2 * np.pi)


print('sums', {nk: round(csum(nk), 2) for nk in (8, 12, 100)})
assert abs(csum(8) - 5.39) < 0.01 and abs(csum(12) - 2.74) < 0.01 and abs(csum(200) - 1) < 1e-3

fig, axs = style.figure(ncols=2, width_cm=10.5, height_cm=4.8, gridspec_kw=dict(wspace=0.5))
ax = axs[0]
kx = np.linspace(-np.pi, np.pi, 2000)
ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-3, 58)
ax.plot(kx, omega(kx, 0 * kx), color=style.ACCENT)
kp = 2 * np.pi * np.arange(-4, 4) / 8
ax.vlines(kp, 0, omega(kp, 0 * kp), color=style.BROKEN, lw=1.0)
ax.plot(kp, omega(kp, 0 * kp), 'o', color=style.BROKEN, ms=3.2)
style.arrows(ax, xlabel=r'$k_x$', ylabel=r'$\Omega$ at $k_y=0$')
ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$']); ax.tick_params(length=2.5, width=0.6)
style.label(ax, 1.55, 33, 'mesh\n$8\\times8$', color=style.BROKEN, fontsize=8.5, ha='left')
ax.text(0.5, -0.2, '(a)', transform=ax.transAxes, ha='center', va='top', fontsize=8.5)
ax = axs[1]
nks = np.array([8, 10, 12, 16, 20, 30, 50, 100])
vals = np.array([csum(n) for n in nks])
ax.set_xscale('log'); ax.set_xlim(6, 130); ax.set_ylim(0, 6.5)
style.guide(ax, y=1, ls=':', color=style.MUTED)
ax.plot(nks, vals, 'o-', color=style.ACCENT, ms=3.2, lw=1.4)
style.arrows(ax, xlabel=r'$n_k$', ylabel=r'$\sum\Omega\,\Delta k^2/2\pi$')
ax.minorticks_off(); ax.set_xticks([10, 100]); ax.set_xticklabels(['10', '100'])
ax.set_yticks([1, 5]); ax.set_yticklabels(['1', '5']); ax.tick_params(length=2.5, width=0.6)
ax.text(0.5, -0.2, '(b)', transform=ax.transAxes, ha='center', va='top', fontsize=8.5)
style.save(fig, __file__)
