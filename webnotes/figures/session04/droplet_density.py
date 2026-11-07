"""Session 4, sections 4.15 and 4.16, the density of two states of N=20 electrons in the lowest Landau level.

In units of l_B, |psi_m|^2 = r^(2m) exp(-r^2/2) / (2 pi 2^m m!) is the normalized density of the orbital (4.10). The filled level
occupies m = 0, ..., N-1, and the density times 2 pi l_B^2 is the local filling factor, 1 inside the droplet. The second state is
the Laughlin state (4.12) with m=3, with the filling 1/3 inside the droplet of radius sqrt(6N). Its density is sampled with the Metropolis method on
|Psi|^2 = prod |z_i - z_j|^6 exp(-sum |z_i|^2 / 2), with 400 walkers, 3000 sweeps after 600 of equilibration, and a fixed seed.
The script also prints, without drawing it, the density of the Slater determinant of every third orbital, m = 0, 3, ..., 3(N-1).
Away from r < 2 l_B it is 1/3 within a few percent, so the rings of the single orbitals overlap and a regular pattern of empty
orbitals does not give lumps in the density."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from math import lgamma
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

N = 20
r = np.linspace(0, 12.5, 501)


def orbital(m, r):
    return np.exp(2 * m * np.log(np.maximum(r, 1e-300)) - r ** 2 / 2 - m * np.log(2) - lgamma(m + 1)) / (2 * np.pi)


nu_full = 2 * np.pi * sum(orbital(m, r) for m in range(N))
nu_third = 2 * np.pi * sum(orbital(3 * m, r) for m in range(N))

# the Laughlin state, Metropolis with single-electron moves, all walkers at once
rng = np.random.default_rng(7)
mexp, nw, nsweep, neq, step = 3, 400, 3000, 600, 0.9
R0 = np.sqrt(2 * mexp * N)
z = R0 * np.sqrt(rng.random((nw, N))) * np.exp(2j * np.pi * rng.random((nw, N)))
edges = np.linspace(0, 12.5, 76)
hist = np.zeros(len(edges) - 1); nsamp = 0; acc = 0
for sweep in range(neq + nsweep):
    for i in range(N):
        zn = z[:, i] + step * (rng.normal(size=nw) + 1j * rng.normal(size=nw)) / np.sqrt(2)
        others = np.delete(z, i, axis=1)
        dlog = 2 * mexp * (np.log(np.abs(zn[:, None] - others)).sum(1) - np.log(np.abs(z[:, i][:, None] - others)).sum(1)) \
            - (np.abs(zn) ** 2 - np.abs(z[:, i]) ** 2) / 2
        ok = np.log(rng.random(nw)) < dlog
        z[ok, i] = zn[ok]; acc += ok.sum()
    if sweep >= neq and sweep % 2 == 0:
        hist += np.histogram(np.abs(z).ravel(), edges)[0]; nsamp += nw
shell = np.pi * (edges[1:] ** 2 - edges[:-1] ** 2)
nu_laughlin = 2 * np.pi * hist / nsamp / shell
rc = 0.5 * (edges[1:] + edges[:-1])
print('acceptance', round(acc / ((neq + nsweep) * N * nw), 2))
print('electrons counted', round((hist / nsamp).sum(), 3), 'largest filling at the edge', round(nu_laughlin.max(), 3))
inner = rc < 5
print('Laughlin filling for r<5', round(nu_laughlin[inner].mean(), 3), '+-', round(nu_laughlin[inner].std(), 3))
sel = (r > 2) & (r < np.sqrt(6 * N) - 2)
print('every third orbital, filling for 2 < r < sqrt(6N)-2, min and max', round(nu_third[sel].min(), 3), round(nu_third[sel].max(), 3))

fig, ax = style.figure(height_cm=5.4, width_cm=12)
ax.plot(r, nu_full, color=style.MUTED, lw=1.4)
ax.plot(rc, nu_laughlin, color=style.ACCENT)
style.guide(ax, y=1 / 3, ls=':')
ax.set_xlim(0, 12.5); ax.set_ylim(0, 1.15)
style.arrows(ax, xlabel=r'$r/\ell_B$', ylabel=r'$2\pi\ell_B^2\,\rho(r)$')
ax.set_xticks([0, np.sqrt(2 * N), np.sqrt(6 * N)]); ax.set_xticklabels(['0', r'$\sqrt{2N}$', r'$\sqrt{6N}$'], fontsize=11)
ax.set_yticks([0, 1 / 3, 1]); ax.set_yticklabels(['0', r'$1/3$', '1'], fontsize=11); ax.tick_params(length=2.5, width=0.6)
style.label(ax, 3.2, 1.07, r'filled level, $\nu=1$', color=style.MUTED, fontsize=11)
style.label(ax, 9.6, 0.66, r'Laughlin, $m=3$', color=style.ACCENT, fontsize=11)
style.save(fig, __file__)
