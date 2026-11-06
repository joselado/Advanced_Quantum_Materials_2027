"""Session 1, the local moment and the Mott gap of the antiferromagnetic mean-field solution of the Hubbard chain (1.7) at half filling."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
from scipy.optimize import brentq
import style

t = 1.0
kk = np.linspace(-np.pi / 2, np.pi / 2, 20001)           # reduced zone of the doubled cell
eps = lambda k: 2 * t * np.cos(k)
def gap_of_U(U):
    # staggered mean field Delta = U m / 2, self-consistency 1 = (U/2) <1/sqrt(Delta^2 + eps^2)>_k
    f = lambda D: (U / 2) * np.trapezoid(1 / np.sqrt(D ** 2 + eps(kk) ** 2), kk) / np.pi - 1
    return brentq(f, 1e-9, U)
# check against the real-space solution of a ring, self-consistent loop with N=120 sites at U=3
def ring(U, N=120, it=300):
    n = np.zeros(N); n[::2] = 0.9; n[1::2] = 0.1; ndn = 1 - n; nup = n.copy()
    T = np.zeros((N, N))
    for i in range(N):
        T[i, (i + 1) % N] = T[(i + 1) % N, i] = -t
    for _ in range(it):
        out = []
        for ns in (ndn, nup):                                   # up feels U n_down and down feels U n_up
            w, v = np.linalg.eigh(T + np.diag(U * ns))
            out.append((np.abs(v[:, : N // 2]) ** 2).sum(axis=1))
        new_up, new_dn = out
        nup, ndn = 0.5 * nup + 0.5 * new_up, 0.5 * ndn + 0.5 * new_dn
    return nup - ndn
U0 = 3.0
m_ring = np.abs(ring(U0)[0]); D0 = gap_of_U(U0)
assert abs(U0 * m_ring / 2 - D0) < 0.02, (U0 * m_ring / 2, D0)
fig, axs = style.figure(height_cm=5.0, ncols=2)
Us = np.linspace(0.4, 8, 60)
Ds = np.array([gap_of_U(u) for u in Us])
ms = 2 * Ds / Us                                   # Delta = U m / 2
# (a) the local moment m of (1.8) on a site
a = axs[0]
a.plot(Us, ms, color=style.ACCENT)
style.guide(a, y=1.0)
style.arrows(a, xlabel=r'$U/t$', ylabel=r'$m$')
a.set_xlim(0, 8.3); a.set_ylim(0, 1.15)
style.label(a, 0.5, 1.07, r'$1$', color=style.MUTED, fontsize=8.5)
a.set_title('local moment', fontsize=8.5, pad=10)
# (b) the gap 2 Delta = U m
b = axs[1]
b.plot(Us, 2 * Ds, color=style.ACCENT)
b.plot(Us, Us, color=style.GRID, lw=1.2, ls=(0, (4, 3)))
style.arrows(b, xlabel=r'$U/t$', ylabel=r'gap$/t$')
b.set_xlim(0, 8.3); b.set_ylim(0, 8.3)
style.label(b, 6.9, 7.9, r'$U$', color=style.MUTED, fontsize=8.5)
style.label(b, 5.2, 2.6, r'gap $=Um$', color=style.ACCENT, fontsize=9)
b.set_title('Mott gap', fontsize=8.5, pad=10)
fig.subplots_adjust(wspace=0.35)
print('gap at U=3t', 2 * D0, 'm at U=8', ms[-1], 'm at U=1', np.interp(1, Us, ms))
style.save(fig, __file__)
