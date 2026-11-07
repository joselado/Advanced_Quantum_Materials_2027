"""Session 6, the one-magnon states of the ferromagnetic Heisenberg ring, exact against the bosonic tight-binding band.

The many-body Hamiltonian H = J sum_i S_i . S_{i+1} with J = -1 is built with sparse spin matrices on a ring of
N=10 spins 1/2 and of N=8 spins 1. It is applied to the N states with one unit of spin removed from saturation, the
subspace is checked to be closed under H, and the N x N block is diagonalized together with the translation, which
gives the momentum of each level. The dots are these exact energies above the polarized ground state, and the lines
are the linear spin-wave band E = |J| S z (1 - cos k) of (6.8) with z=2, which comes from the bosonic hopping S J of
Section 6.14.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import scipy.sparse as sp
import style

J = -1.0


def spin_ops(S):
    m = np.arange(S, -S - 1, -1)
    d = len(m)
    sz = np.diag(m)
    sp_ = np.zeros((d, d))
    for i in range(1, d):
        sp_[i - 1, i] = np.sqrt(S * (S + 1) - m[i] * (m[i] + 1))
    return sp.csr_matrix(sz), sp.csr_matrix(sp_)


def one_magnon(S, N):
    sz, spl = spin_ops(S)
    d = sz.shape[0]
    def site(op, i):
        return sp.kron(sp.kron(sp.identity(d**i), op), sp.identity(d**(N - i - 1)), format='csr')
    H = sp.csr_matrix((d**N, d**N))
    for i in range(N):
        j = (i + 1) % N
        H = H + J * (site(sz, i) @ site(sz, j) + 0.5 * (site(spl, i) @ site(spl.T, j) + site(spl.T, i) @ site(spl, j)))
    # the polarized state is index 0 (all m=S); one unit removed on site i
    full = np.zeros(d**N); full[0] = 1
    E0 = full @ (H @ full)
    states = []
    for i in range(N):
        v = site(spl.T, i) @ full
        states.append(v / np.linalg.norm(v))
    P = np.array(states)                                  # N x d^N
    HP = (H @ P.T)
    assert np.allclose(HP, P.T @ (P @ HP), atol=1e-12)    # the one-magnon subspace is closed under H
    h = P @ HP
    T = np.roll(np.eye(N), 1, axis=0)                     # translation by one site in this basis
    w, U = np.linalg.eigh(h)
    E = w - E0
    # the momentum from <T>, which is cos k also for the standing waves made of +k and -k
    k = np.array([np.arccos(np.clip(np.real(U[:, n] @ T @ U[:, n]), -1, 1)) for n in range(N)])
    return k, E


FS = 11.5
style.plt.rcParams['font.size'] = FS          # labels of the arrows too, for a phone
fig, ax = style.figure(height_cm=5.6, width_cm=11.0)
kk = np.linspace(0, np.pi, 200)
for S, N, col, mk in ((0.5, 10, style.ACCENT, 'o'), (1.0, 8, style.BROKEN, 's')):
    k, E = one_magnon(S, N)
    band = abs(J) * S * 2 * (1 - np.cos(k))
    assert np.allclose(E, band, atol=1e-9)              # linear spin-wave theory is exact for one magnon
    ax.plot(kk, abs(J) * S * 2 * (1 - np.cos(kk)), color=col, lw=1.6, zorder=1)
    ax.plot(k, E, mk, color=col, ms=5.5, mfc='white', mew=1.4, zorder=3)
style.arrows(ax, xlabel='$k$', ylabel=r'$E/|J|$')
style.label(ax, np.pi, -0.1, r'$\pi$', fontsize=FS, va='top')
style.label(ax, 0, -0.1, r'$0$', fontsize=FS, va='top')
for y, lab in ((2, '$2$'), (4, '$4$')):
    ax.text(-0.06, y, lab, ha='right', va='center', fontsize=FS - 0.5)
style.label(ax, 2.05, 3.55, '$S=1$, $N=8$', color=style.BROKEN, fontsize=FS, ha='right')
style.label(ax, 2.35, 1.0, r'$S=\frac{1}{2}$, $N=10$', color=style.ACCENT, fontsize=FS, ha='left')
ax.set_xlim(0, np.pi + 0.05); ax.set_ylim(0, 4.6)
style.save(fig, __file__)
