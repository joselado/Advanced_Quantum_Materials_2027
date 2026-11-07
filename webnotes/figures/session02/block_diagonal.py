"""Session 2, a Hamiltonian that commutes with a symmetry is block diagonal in the eigenbasis of the symmetry.

A ring of L = 4 cells with two orbitals per cell (an onsite splitting, an intracell hopping, and hoppings
to the next cell). The rotation R moves every cell to the next one, so [H, R] = 0. On the left, |H_ij| in the
basis of the sites. On the right, |H_ij| in the basis of the eigenstates of R, which are the Fourier modes
of the cells. Only 2x2 blocks with the same eigenvalue of R survive, one block for each phase 2 pi n / 4.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import style

FS = 10.5
L, n_orb = 4, 2
h0 = np.array([[0.6, 1.0], [1.0, -0.6]])                 # inside a cell
h1 = np.array([[-0.7, 0.4], [0.25, 0.5]])                # to the next cell
H = np.zeros((L * n_orb, L * n_orb))
for c in range(L):
    s = slice(n_orb * c, n_orb * (c + 1))
    s1 = slice(n_orb * ((c + 1) % L), n_orb * ((c + 1) % L + 1))
    H[s, s] += h0
    H[s, s1] += h1
    H[s1, s] += h1.T
R = np.kron(np.roll(np.eye(L), 1, axis=0), np.eye(n_orb))     # cell c -> c + 1
assert np.allclose(H @ R, R @ H)
# eigenbasis of R, Fourier modes of the cells, ordered by the phase 2 pi n / L
phases = 2 * np.pi * np.arange(L) / L
U = np.zeros((L * n_orb, L * n_orb), complex)
for n, ph in enumerate(phases):
    for a in range(n_orb):
        v = np.zeros(L * n_orb, complex)
        v[a::n_orb] = np.exp(-1j * ph * np.arange(L)) / np.sqrt(L)
        assert np.allclose(R @ v, np.exp(1j * ph) * v)
        U[:, n * n_orb + a] = v
assert np.allclose(U.conj().T @ U, np.eye(L * n_orb))
Hk = U.conj().T @ H @ U
mask = np.kron(np.eye(L), np.ones((n_orb, n_orb)))
assert np.allclose(Hk * (1 - mask), 0)                  # nothing outside the blocks
assert np.allclose(np.sort(np.linalg.eigvalsh(Hk)), np.sort(np.linalg.eigvalsh(H)))

fig, axs = plt.subplots(1, 2, figsize=(12.5 * style.CM, 7.0 * style.CM))
fig.subplots_adjust(wspace=0.18, left=0.02, right=0.98, top=0.86, bottom=0.08)
vmax = np.abs(H).max()
cmap = plt.get_cmap('Blues')
for ax, M, title in ((axs[0], H, 'site basis'), (axs[1], Hk, 'eigenbasis of $R$')):
    N = M.shape[0]
    for i in range(N):
        for j in range(N):
            v = abs(M[i, j]) / vmax
            if v > 1e-9:
                ax.add_patch(Rectangle((j, N - 1 - i), 1, 1, fc=style.ACCENT, alpha=0.25 + 0.75 * min(v, 1), lw=0))
    ax.add_patch(Rectangle((0, 0), N, N, fill=False, ec=style.INK, lw=0.8))
    for k in range(1, L):
        ax.plot([k * n_orb] * 2, [0, N], color=style.GRID, lw=0.6)
        ax.plot([0, N], [N - k * n_orb] * 2, color=style.GRID, lw=0.6)
    ax.set_xlim(-0.2, N + 0.2); ax.set_ylim(-1.6, N + 0.2)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(title, fontsize=FS)
for n, lab in enumerate([r'$1$', r'$i$', r'$-1$', r'$-i$']):
    axs[1].add_patch(Rectangle((n * n_orb, L * n_orb - (n + 1) * n_orb), n_orb, n_orb, fill=False,
                               ec=style.BROKEN, lw=1.4))
    style.label(axs[1], n * n_orb + 1, -0.75, lab, color=style.BROKEN, fontsize=FS)
style.label(axs[0], 4, -0.75, 'cells 1 to 4', fontsize=FS)
style.save(fig, __file__)
