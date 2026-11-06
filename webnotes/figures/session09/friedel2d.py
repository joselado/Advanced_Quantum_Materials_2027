"""Session 9, the Friedel ripples of a single impurity in a square lattice, the LDOS change at fixed energy."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

L, t, v0, E, eta = 61, 1.0, 3.0, -3.4, 0.12
N = L * L
idx = lambda x, y: x * L + y
H = np.zeros((N, N))
for x in range(L):
    for y in range(L):
        if x + 1 < L: H[idx(x, y), idx(x + 1, y)] = H[idx(x + 1, y), idx(x, y)] = -t
        if y + 1 < L: H[idx(x, y), idx(x, y + 1)] = H[idx(x, y + 1), idx(x, y)] = -t
c = L // 2


def ldos(H):
    e, w = np.linalg.eigh(H)
    lor = (eta / np.pi) / ((E - e) ** 2 + eta ** 2)
    return ((w ** 2) @ lor).reshape(L, L)


H1 = H.copy(); H1[idx(c, c), idx(c, c)] = v0
d = ldos(H1) - ldos(H)
d[c, c] = 0
r = 16
win = d[c - r:c + r + 1, c - r:c + r + 1]
yy, xx = np.mgrid[-r:r+1, -r:r+1]
m = np.abs(win[(xx**2 + yy**2) > 9]).max() * 0.8
# Fermi contour cos kx + cos ky = -E/(2t)
kk = np.linspace(-np.pi, np.pi, 600)
KX, KY = np.meshgrid(kk, kk)
kFx = np.arccos(-E / (2 * t) - 1)          # kF along kx, where ky=0
print('kF along x =', kFx, ' pi/kF =', np.pi / kFx)

fig, axs = plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.6 * style.CM), gridspec_kw=dict(width_ratios=[1, 1.1], wspace=0.25))
a, b = axs
a.set_aspect('equal'); a.axis('off')
a.contour(KX, KY, -2 * t * (np.cos(KX) + np.cos(KY)), levels=[E], colors=[style.ACCENT], linewidths=1.8, linestyles='solid')
a.plot([-np.pi, np.pi, np.pi, -np.pi, -np.pi], [-np.pi, -np.pi, np.pi, np.pi, -np.pi], color=style.GRID, lw=1)
a.annotate('', xy=(kFx, 0), xytext=(-kFx, 0), arrowprops=dict(arrowstyle='<|-|>', color=style.BROKEN, lw=1.3, mutation_scale=8, shrinkA=0, shrinkB=0))
style.label(a, 0, 0.45, r'$2k_F$', color=style.BROKEN, fontsize=9)
style.label(a, 0, -np.pi - 0.55, r'Fermi contour, $k$-space', fontsize=8.5)
b.set_aspect('equal'); b.axis('off')
b.imshow(win.T, origin='lower', cmap='RdBu_r', vmin=-m, vmax=m, extent=(-r - .5, r + .5, -r - .5, r + .5))
b.plot([-r, -r + 8], [-r - 2.2, -r - 2.2], color=style.INK, lw=1.2, clip_on=False)
style.label(b, -r + 4, -r - 4, r'8 sites', fontsize=8)
style.label(b, 0, r + 2.4, r'$\delta\rho(\vec{r},E)$, real space', fontsize=8.5)
style.save(fig, __file__)
