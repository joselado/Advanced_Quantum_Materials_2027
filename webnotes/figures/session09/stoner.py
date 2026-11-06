"""Session 9, Eq. (9.8) on the half-filled square lattice, the static chi_0(q) along the path Gamma-X-M-Gamma."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

t, mu, T, nk = 1.0, 0.0, 0.1, 240
kk = 2 * np.pi * np.arange(nk) / nk
KX, KY = np.meshgrid(kk, kk, indexing='ij')
nF = lambda e: 1 / (1 + np.exp(np.clip(e / T, -60, 60)))
eps = lambda kx, ky: -2 * t * (np.cos(kx) + np.cos(ky)) - mu


def chi0(ix, iy):
    """Static Lindhard function of Eq. (9.4) for q = 2 pi (ix, iy) / nk, on the same k-mesh."""
    q = 2 * np.pi / nk
    e1 = eps(KX, KY)
    e2 = eps(KX + ix * q, KY + iy * q)
    d = e2 - e1
    small = np.abs(d) < 1e-9
    dd = np.where(small, 1.0, d)
    val = np.where(small, nF(e1) * (1 - nF(e1)) / T, (nF(e1) - nF(e2)) / dd)   # -n_F' when d -> 0
    return val.mean()


h = nk // 2
path = [(i, 0) for i in range(0, h + 1, 8)] + [(h, i) for i in range(8, h + 1, 8)] + [(h - i, h - i) for i in range(8, h + 1, 8)]
x = np.arange(len(path))
y = np.array([chi0(*p) for p in path])
nseg = len(range(0, h + 1, 8))
xt = [0, nseg - 1, 2 * (nseg - 1), 3 * (nseg - 1)]
print('chi0 at Gamma, X, M =', y[0], y[xt[1]], y[xt[2]])

fig, ax = plt.subplots(figsize=(style.WIDTH_CM * style.CM, 5.6 * style.CM))
style.arrows(ax, ylabel=r'$\chi_0(q,0)$')
ax.plot(x, y, color=style.ACCENT)
style.guide(ax, y=y[0], color=style.LIGHT, ls=(0, (4, 3)), lw=1.0)
style.guide(ax, y=y[xt[2]], color=style.BROKEN, ls=(0, (4, 3)), lw=1.0)
ax.set_ylim(0, y.max() * 1.3)
ax.set_xlim(0, x[-1])
for xx, s in zip(xt, (r'$\Gamma$', r'$X$', r'$M=(\pi,\pi)$', r'$\Gamma$')):
    style.label(ax, xx, -0.06 * y.max(), s, fontsize=8.5)
style.label(ax, 1.5, y[0] + 0.03 * y.max(), r'$1/U=\chi_0(0,0)\approx D(E_F)$, ferromagnet', color=style.ACCENT, ha='left', va='bottom', fontsize=8.5)
style.label(ax, xt[2] - 3, y[xt[2]] + 0.03 * y.max(), r'$1/U=\chi_0(Q,0)$, antiferromagnet', color=style.BROKEN, ha='right', va='bottom', fontsize=8.5)
ax.plot([xt[2]], [y[xt[2]]], 'o', color=style.BROKEN, ms=4)
ax.plot([0], [y[0]], 'o', color=style.ACCENT, ms=4)
style.save(fig, __file__)
