"""Session 8, the three classes of spinon bands of (8.15), from Bloch Hamiltonians with chi=1 diagonalized on a k grid."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

chi = 1.0
nk = 401
k = np.linspace(-np.pi, np.pi, nk)

# (a) uniform chain, H = -chi sum f^dag_i f_{i+1} + h.c., one site per cell
Ea = (-2 * chi * np.cos(k))[:, None]

# (b) dimerized chain, chi1 = 1 and chi2 = 0.6 alternating, two sites per cell: h(k) = chi1 + chi2 exp(-ik)
chi1, chi2 = 1.0, 0.6
Eb = np.array([np.linalg.eigvalsh(-np.array([[0, chi1 + chi2 * np.exp(-1j * q)], [chi1 + chi2 * np.exp(1j * q), 0]])) for q in k])

# (c) pi-flux square lattice: hopping -chi along x, and -chi (-1)^x along y, two sites along x per cell, cut at ky = pi/2
ky = np.pi / 2
def Hpi(kx):
    return np.array([[-2 * chi * np.cos(ky), -chi * (1 + np.exp(-2j * kx))], [-chi * (1 + np.exp(2j * kx)), 2 * chi * np.cos(ky)]])
kx = np.linspace(0, np.pi, nk)
Ec = np.array([np.linalg.eigvalsh(Hpi(q)) for q in kx])
assert np.allclose(np.abs(Ec), 2 * chi * np.sqrt(np.cos(kx) ** 2 + np.cos(ky) ** 2)[:, None])    # the analytic result
assert abs(Eb[:, 1].min() - Eb[:, 0].max()) < 2 * (chi1 - chi2) + 1e-9 and Eb[:, 1].min() > 0.39   # gap 2(chi1-chi2) = 0.8
print('gap b', Eb[:, 1].min() - Eb[:, 0].max(), 'Dirac c', abs(Ec).min())

fig, axs = style.plt.subplots(1, 3, figsize=(style.WIDTH_CM * style.CM, 4.9 * style.CM), sharey=True)
panels = [(k, Ea, 'gapless', 'uniform chain', style.ACCENT), (k, Eb, 'gapped', 'dimerized chain', style.BROKEN),
          (kx, Ec, 'Dirac', r'$\pi$-flux square lattice, $k_y=\pi/2$', style.ACCENT)]
for ax, (x, E, cls, sub, col) in zip(axs, panels):
    style.arrows(ax, xlabel=r'$k$')
    ax.axhline(0, color=style.GRID, lw=1.0, zorder=0)
    for b in range(E.shape[1]):
        ax.plot(x, E[:, b], color=col)
    ax.set_xlim(x[0], x[-1]); ax.set_ylim(-2.7, 2.7)
    style.label(ax, (x[0] + x[-1]) / 2, 3.35, cls, fontsize=9)
    style.label(ax, (x[0] + x[-1]) / 2, -3.15, sub, fontsize=8.0, color=style.MUTED)
axs[0].set_ylabel(r'$E/\chi$', fontsize=9)
axs[0].set_yticks([-2, 0, 2]); axs[0].tick_params(axis='y', length=2.5, pad=2)
axs[1].tick_params(axis='y', left=False); axs[2].tick_params(axis='y', left=False)
style.label(axs[0], 0, 0.45, r'$E_F=0$', fontsize=7.5, color=style.MUTED)
style.save(fig, __file__)
