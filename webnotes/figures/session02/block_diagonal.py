"""Session 2, a Hamiltonian that commutes with a symmetry is block diagonal in the eigenbasis of the symmetry.

A ring of L = 4 cells with two orbitals per cell, with the onsite energies +0.6 and -0.6, the hopping 1 between the two
orbitals of a cell, and the hoppings h1 from the orbitals of a cell to those of the next cell. The rotation R moves the
amplitudes of every cell to the previous cell, the direction of Section 2.3 decided on 2026-11-22, so [H, R] = 0. On the left |H_ij| in the basis of the sites, on the right |H_ij| in the basis of
the eigenstates of R, which are the Fourier modes of the cells, on the same color scale. Only the 2x2 blocks with the
same eigenvalue of R survive, one block for each phase 2 pi n / 4. The numbers of the caption are asserted here.
pyqula has no change to the eigenbasis of a symmetry, so this is numpy and has no script to download.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import style

FS = 10.5
L, n_orb = 4, 2
h0 = np.array([[0.6, 1.0], [1.0, -0.6]])                 # inside a cell, the caption gives these numbers
h1 = np.array([[-0.7, 0.4], [0.25, 0.5]])                # h1[a, b] is the element of c^+_{c,a} c_{c+1,b}
# the numbers of the caption: onsite 0.6 and -0.6, the hopping 1 inside a cell, and -0.7, 0.4, 0.25, 0.5 to the next cell
assert np.allclose(np.diag(h0), [0.6, -0.6]) and h0[0, 1] == h0[1, 0] == 1.0
assert sorted(h1.ravel().tolist()) == [-0.7, 0.25, 0.4, 0.5]
H = np.zeros((L * n_orb, L * n_orb))
for c in range(L):
    s = slice(n_orb * c, n_orb * (c + 1))
    s1 = slice(n_orb * ((c + 1) % L), n_orb * ((c + 1) % L + 1))
    H[s, s] += h0
    H[s, s1] += h1
    H[s1, s] += h1.T
R = np.kron(np.roll(np.eye(L), -1, axis=0), np.eye(n_orb))    # (R v)_c = v_{c+1}, the amplitudes go to the previous cell
assert np.allclose(H @ R, R @ H) and np.allclose(H, H.T)
e2 = np.zeros(L * n_orb); e2[n_orb] = 1.0                       # one amplitude on the first orbital of the cell 2
assert np.allclose(R @ e2, np.eye(L * n_orb)[0])                # it moves to the cell 1, the previous cell
# every cell couples to its two neighbors in the site basis, the corner blocks are the bond from cell 4 to cell 1
for c in range(L):
    for c2 in range(L):
        blk = H[n_orb * c:n_orb * (c + 1), n_orb * c2:n_orb * (c2 + 1)]
        assert (np.abs(blk).max() > 0) == ((c - c2) % L in (0, 1, L - 1))
# eigenbasis of R, Fourier modes of the cells, ordered by the phase 2 pi n / L, so the eigenvalues 1, i, -1, -i
phases = 2 * np.pi * np.arange(L) / L
U = np.zeros((L * n_orb, L * n_orb), complex)
for n, ph in enumerate(phases):
    for a in range(n_orb):
        v = np.zeros(L * n_orb, complex)
        v[a::n_orb] = np.exp(1j * ph * np.arange(L)) / np.sqrt(L)
        assert np.allclose(R @ v, np.exp(1j * ph) * v)
        U[:, n * n_orb + a] = v
assert np.allclose(np.exp(1j * phases), [1, 1j, -1, -1j])
assert np.allclose(U.conj().T @ U, np.eye(L * n_orb))
Hk = U.conj().T @ H @ U
# the picture is |H_ij|, and it is the same for the rotation in the other sense, whose eigenbasis is U conjugated
assert np.allclose(np.abs(Hk), np.abs(U.T @ H @ U.conj()))
mask = np.kron(np.eye(L), np.ones((n_orb, n_orb)))
assert np.allclose(Hk * (1 - mask), 0)                  # nothing outside the four blocks of size 2 x 2
assert np.allclose(np.sort(np.linalg.eigvalsh(Hk)), np.sort(np.linalg.eigvalsh(H)))
vmax = max(np.abs(H).max(), np.abs(Hk).max())
assert np.isclose(np.abs(H).max(), 1.0) and np.isclose(vmax, 2.0)    # the largest element, in the block of -1
VMAX = 2.0                                               # one scale for the two panels, from 0 to 2

cmap = LinearSegmentedColormap.from_list('white_accent', ['#ffffff', style.LIGHT, style.ACCENT])
fig, axs = plt.subplots(1, 2, figsize=(13.0 * style.CM, 6.9 * style.CM))
fig.subplots_adjust(wspace=0.55, left=0.1, right=0.86, top=0.88, bottom=0.2)
N = L * n_orb
centers = np.arange(L) * n_orb + 0.5 * (n_orb - 1)
for ax, M, title, ticks, name in ((axs[0], H, 'site basis', ['1', '2', '3', '4'], 'cell'),
                                  (axs[1], Hk, r'eigenbasis of $R$', ['$1$', '$i$', '$-1$', '$-i$'], r'eigenvalue of $R$')):
    im = ax.pcolormesh(np.arange(N + 1) - 0.5, np.arange(N + 1) - 0.5, np.abs(M), cmap=cmap, vmin=0, vmax=VMAX,
                       edgecolors='face', linewidth=0, rasterized=True)
    for k in range(1, L):
        ax.axvline(k * n_orb - 0.5, color=style.GRID, lw=0.6)
        ax.axhline(k * n_orb - 0.5, color=style.GRID, lw=0.6)
    ax.set_xlim(-0.5, N - 0.5); ax.set_ylim(N - 0.5, -0.5)
    ax.set_aspect('equal')
    ax.set_xticks(centers); ax.set_xticklabels(ticks, fontsize=FS)
    ax.set_yticks(centers); ax.set_yticklabels(ticks, fontsize=FS)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.xaxis.set_ticks_position('top'); ax.xaxis.set_label_position('top')
    ax.set_xlabel(name, fontsize=FS + 0.5, labelpad=3); ax.set_ylabel(name, fontsize=FS + 0.5, labelpad=2)
    for s in ax.spines.values():
        s.set_linewidth(0.6); s.set_color(style.INK)
    ax.text(0.5, -0.1, title, transform=ax.transAxes, ha='center', va='top', fontsize=FS + 0.5)
for n in range(L):
    axs[1].add_patch(plt.Rectangle((n * n_orb - 0.5, n * n_orb - 0.5), n_orb, n_orb, fill=False, ec=style.BROKEN, lw=1.3))
cax = fig.add_axes([0.89, 0.2, 0.022, 0.68])
cb = fig.colorbar(im, cax=cax, ticks=[0, 0.5, 1, 1.5, 2])
cb.ax.tick_params(labelsize=FS, length=2.5, width=0.6)
cb.outline.set_linewidth(0.6)
cb.set_label(r'$|H_{ij}|$', fontsize=FS + 0.5, labelpad=4)
style.save(fig, __file__)
