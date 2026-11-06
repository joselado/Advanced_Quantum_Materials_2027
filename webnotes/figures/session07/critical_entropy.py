"""Session 7, the entropy of a block of l sites of the infinite XX chain at half filling (free fermions), critical and dimerized."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

LMAX = 1000
def entropy_from_C(C):
    nu = np.linalg.eigvalsh(C)
    nu = nu[(nu > 1e-13) & (nu < 1 - 1e-13)]
    return -np.sum(nu * np.log(nu) + (1 - nu) * np.log(1 - nu))

# critical chain, hopping 1: C_ij = sin(pi (i-j)/2) / (pi (i-j)), C_ii = 1/2
d = np.arange(LMAX)[:, None] - np.arange(LMAX)[None, :]
with np.errstate(all='ignore'):
    C = np.where(d == 0, 0.5, np.sin(np.pi * d / 2) / (np.pi * d))

# dimerized chain, hoppings t1=1 inside the cell and t2=0.6 between cells, lower band full: C_ij = <c_i^dag c_j>
t1, t2 = 1.0, 0.6
nk = 4000
k = (np.arange(nk) + 0.5) / nk * 2 * np.pi - np.pi                # cell momentum, two sites per cell
h = t1 + t2 * np.exp(-1j * k)                                     # off-diagonal element of the Bloch Hamiltonian -[[0,h],[h*,0]]
phase = h / np.abs(h)
ncell = LMAX // 2
Cd = np.zeros((LMAX, LMAX))
for R in range(-ncell + 1, ncell):
    ph = np.exp(1j * k * R)
    # C is the projector on the filled band, summed over the cell momentum, and the check below fixes its phases
    caa = (0.5 * np.mean(ph)).real
    cab = (0.5 * np.mean(ph * phase)).real      # element between the first and the second site of a cell
    cba = (0.5 * np.mean(ph * np.conj(phase))).real
    for a in range(max(0, R), min(ncell, ncell + R)):
        b = a - R
        Cd[2 * a, 2 * b] = caa; Cd[2 * a + 1, 2 * b + 1] = caa
        Cd[2 * a, 2 * b + 1] = cab; Cd[2 * a + 1, 2 * b] = cba
assert np.allclose(Cd, Cd.T, atol=1e-9)
# check against the exact diagonalization of a ring of 600 sites, whose block of 40 sites must agree
Nr = 600
Hr = np.zeros((Nr, Nr))
for i in range(Nr):
    Hr[i, (i + 1) % Nr] = Hr[(i + 1) % Nr, i] = -(t1 if i % 2 == 0 else t2)
w, v = np.linalg.eigh(Hr)
Cr = v[:, :Nr // 2] @ v[:, :Nr // 2].T
assert np.allclose(Cr[100:140, 100:140], Cd[:40, :40], atol=1e-6)

ells = np.unique(np.round(np.logspace(np.log10(2), np.log10(LMAX), 26) / 2).astype(int) * 2)   # even blocks, cut between cells
Sc = np.array([entropy_from_C(C[:l, :l]) for l in ells])
Sg = np.array([entropy_from_C(Cd[:l, :l]) for l in ells])
fit = np.polyfit(np.log(ells[ells > 20]), Sc[ells > 20], 1)
print('slope', fit[0], 'const', fit[1], 'S(10),S(1000)', np.interp(10, ells, Sc), Sc[-1], 'gapped', Sg[-1])
assert abs(fit[0] - 1 / 3) < 0.01

fig, ax = style.figure(height_cm=5.6)
ax.semilogx(ells, Sc, color=style.ACCENT, marker='o', ms=2.8, lw=1.4)
ax.semilogx(ells, Sg, color=style.BROKEN, marker='o', ms=2.8, lw=1.4)
ax.semilogx(ells, fit[0] * np.log(ells) + fit[1], color=style.GRID, lw=1.3, ls=(0, (3, 3)), zorder=0)
ax.set_xlim(1.6, 1.4e3); ax.set_ylim(0, 3.3)
style.label(ax, 3.2, 2.1, r'critical chain, $S\simeq\frac{1}{3}\log\ell$', color=style.ACCENT, fontsize=8.5, ha='left')
style.label(ax, 15, 0.95, r'dimerized chain, $S$ saturates', color=style.BROKEN, fontsize=8.5, ha='left')
ax.set_xticks([10, 100, 1000]); ax.set_xticklabels([r'$10$', r'$10^2$', r'$10^3$']); ax.minorticks_off()
ax.set_yticks([0, 1, 2]); ax.tick_params(length=2.5, pad=2)
style.arrows(ax, xlabel=r'$\ell$', ylabel=r'$S$', ticks=True)
style.save(fig, __file__)
