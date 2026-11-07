"""Session 4, section 4.4, the Landau levels of a square lattice are flat bands with Chern number one.

The square lattice with hopping t=1 and the flux phi=1/20 of a flux quantum per plaquette, with the Peierls phases (4.4) in the
Landau gauge, so the magnetic unit cell has q=20 sites along x. Panel (a) is the lowest bands against k_y at k_x=0, with the dashed
lines at the continuum Landau levels -4t + hbar omega_c (n + 1/2), hbar omega_c = 4 pi phi t, as in the widget of Section 4.11.
The Chern number of each band is computed from the link variables on a 12 x 60 grid of the magnetic Brillouin zone and is printed.
Panel (b) is the Hall conductivity of (4.2), the sum of the Chern numbers of the bands below E_F, drawn for E_F in the gaps."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

q = 20; phi = 1 / q; nb = 4
wc = 4 * np.pi * phi


def H(kx, ky):
    h = np.zeros((q, q), complex)
    for j in range(q):
        h[j, j] = -2 * np.cos(ky + 2 * np.pi * phi * j)
        amp = np.exp(1j * kx * q) if j == q - 1 else 1.0
        h[(j + 1) % q, j] += -amp; h[j, (j + 1) % q] += -np.conj(amp)
    return h


def chern(n, N1=12, N2=60):
    kxs = np.arange(N1) / N1 * 2 * np.pi / q; kys = np.arange(N2) / N2 * 2 * np.pi
    V = np.array([[np.linalg.eigh(H(a, b))[1][:, n] for b in kys] for a in kxs])
    def link(a, b):
        z = np.sum(a.conj() * b, -1)
        return z / np.abs(z)
    U1 = link(V, np.roll(V, -1, 0)); U2 = link(V, np.roll(V, -1, 1))
    return np.angle(U1 * np.roll(U2, -1, 0) / np.roll(U1, -1, 1) / U2).sum() / (2 * np.pi)


C = [chern(n) for n in range(nb)]
print('Chern numbers of the lowest bands', np.round(C, 6))
assert np.allclose(C, 1, atol=1e-6)
kys = np.linspace(-np.pi, np.pi, 121)
E = np.array([np.linalg.eigvalsh(H(0.0, k))[:nb + 1] for k in kys])
Eall = np.array([[np.linalg.eigvalsh(H(a, b))[:nb + 1] for b in np.linspace(0, 2 * np.pi, 41)] for a in np.linspace(0, 2 * np.pi / q, 5)])
lo, hi = Eall.min((0, 1)), Eall.max((0, 1))
print('band edges', np.round(lo, 3), np.round(hi, 3), 'continuum', np.round(-4 + wc * (np.arange(nb) + 0.5), 3))

fig, axs = plt.subplots(1, 2, figsize=(12 * style.CM, 5.6 * style.CM), gridspec_kw=dict(wspace=0.25, width_ratios=[1.3, 1]))
ax = axs[0]
ylo, yhi = -4.05, -1.55
for n in range(nb):
    style.guide(ax, y=-4 + wc * (n + 0.5), ls='--', color=style.MUTED, lw=0.8)
    ax.plot(kys, E[:, n], color=style.ACCENT)
    style.label(ax, 2.2, E[:, n].mean() - 0.19, r'$C=%d$' % round(C[n]), fontsize=11, color=style.ACCENT)
ax.set_xlim(-np.pi, np.pi); ax.set_ylim(ylo, yhi)
style.arrows(ax, xlabel=r'$k_y$', ylabel=r'$E/t$')
ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=11)
ax.set_yticks([-4, -3, -2]); ax.set_yticklabels(['$-4$', '$-3$', '$-2$'], fontsize=11); ax.tick_params(length=2.5, width=0.6)
ax.text(0.5, -0.17, '(a)', transform=ax.transAxes, ha='center', va='top', fontsize=11)
ax = axs[1]
# the Hall conductivity, N(E_F) = number of bands entirely below E_F, drawn in the gaps only
gaps = [(ylo, lo[0])] + [(hi[n], lo[n + 1]) for n in range(nb)]
for n, (a, b) in enumerate(gaps):
    sig = sum(round(c) for c in C[:n])
    ax.plot([sig, sig], [a, min(b, yhi)], color=style.BROKEN, lw=2.2)
    if n < nb:
        ax.axhspan(lo[n], hi[n] + 0.01, color=style.GRID, lw=0)
for n in range(nb):
    ax.plot([n, n + 1], [lo[n], lo[n]], color=style.BROKEN, lw=0.6, ls=':')
ax.set_xlim(-0.3, 4.6); ax.set_ylim(ylo, yhi)
style.arrows(ax, xlabel=r'$\sigma_{xy}$', ylabel=r'$E_F/t$')
ax.set_xticks([0, 1, 2, 3, 4]); ax.set_xticklabels(['0', '1', '2', '3', '4'], fontsize=11)
ax.set_yticks([-4, -3, -2]); ax.set_yticklabels(['$-4$', '$-3$', '$-2$'], fontsize=11); ax.tick_params(length=2.5, width=0.6)
ax.text(0.5, -0.17, '(b)', transform=ax.transAxes, ha='center', va='top', fontsize=11)
style.save(fig, __file__)
