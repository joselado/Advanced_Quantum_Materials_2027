"""Session 7, the energy after every one-site update of a variational sweep on an open Heisenberg chain, computed with numpy.

Redrawn on 2026-11-22 with the error in units of J and ticks at the three values of the caption of Section 7.10, which
are asserted below. The calculation is the one of the first version, which webnotes/checks/session07/conventions.py
reads, and figures/session07/_g4_sweeps.py repeats it for the picture options of the quiz."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

L = 10
sx = np.array([[0, 1], [1, 0]]) / 2; sy = np.array([[0, -1j], [1j, 0]]) / 2; sz = np.diag([.5, -.5])
def op(o, i):
    m = np.eye(1)
    for j in range(L):
        m = np.kron(m, o if j == i else np.eye(2))
    return m
H = sum(op(s, i) @ op(s, i + 1) for i in range(L - 1) for s in (sx, sy, sz)).real   # the Heisenberg chain, real in this basis
E0 = np.linalg.eigvalsh(H)[0]

def run(M, nsweeps=3, seed=1):
    rng = np.random.default_rng(seed)
    D = [1] + [min(M, 2 ** min(k, L - k)) for k in range(1, L)] + [1]
    A = [rng.normal(size=(D[k], 2, D[k + 1])) for k in range(L)]
    def contract(lo, hi):             # product of the tensors lo..hi-1, shape (2^(hi-lo), D[lo], D[hi]) as (phys, left, right)
        T = np.eye(D[lo]).reshape(1, D[lo], D[lo])
        for k in range(lo, hi):
            T = np.einsum('pab,bsc->psac', T, A[k]).reshape(-1, D[lo], D[k + 1])
        return T
    energies = []
    order = list(range(L)) + list(range(L - 2, 0, -1))
    for sweep in range(nsweeps):
        for k in order:
            Lf = contract(0, k)[:, 0, :]                       # (2^k, D[k])
            Rt = contract(k + 1, L)[:, :, 0]                    # (2^(L-k-1), D[k+1]) with the layout (phys, right)
            Rt = Rt.reshape(-1, D[k + 1])
            # psi[i,s,j] = sum Lf[i,a] A[a,s,b] Rt[j,b]
            N = np.einsum('ia,st,jb->isjatb', Lf, np.eye(2), Rt).reshape(2 ** L, -1)
            U, sv, Vt = np.linalg.svd(N, full_matrices=False)
            keep = sv > 1e-9 * sv[0]                              # the tensor may not use all of its directions
            U, sv, Vt = U[:, keep], sv[keep], Vt[keep]
            w, u = np.linalg.eigh(U.T @ H @ U)                    # exact minimum of the energy over this tensor
            psi = U @ u[:, 0]
            A[k] = ((Vt.T / sv) @ (U.T @ psi)).reshape(D[k], 2, D[k + 1])
            energies.append(psi @ H @ psi / (psi @ psi))
    return np.array(energies)

curves = {M: run(M) for M in (2, 4, 8)}
for M, e in curves.items():
    assert np.all(np.diff(e) < 1e-9), (M, np.diff(e).max())      # never goes up
    assert np.all(e > E0 - 1e-9)                                  # variational bound
    print(M, e[-1] - E0)
end = {M: e[-1] - E0 for M, e in curves.items()}
assert all(len(e) == 3 * 18 for e in curves.values())                          # one sweep is 2L - 2 = 18 updates
assert abs(end[2] - 0.2) < 0.005 and abs(end[4] - 6e-3) < 3e-4 and abs(end[8] - 1.5e-5) < 1e-6, end   # the caption

fig, ax = style.figure(height_cm=5.6)
cols = {2: style.MUTED, 4: style.BROKEN, 8: style.ACCENT}
for M, e in curves.items():
    ax.semilogy(np.arange(1, len(e) + 1), e - E0 + 1e-9, color=cols[M], marker='o', ms=2.2, lw=1.3)
n = len(curves[2])
ax.set_xlim(0, n + 1)
style.label(ax, n - 9, 1.0, r'$\chi=2$', color=style.MUTED, fontsize=8.5, ha='left')
style.label(ax, n - 9, 3e-2, r'$\chi=4$', color=style.BROKEN, fontsize=8.5, ha='left')
style.label(ax, n - 9, 1.5e-4, r'$\chi=8$', color=style.ACCENT, fontsize=8.5, ha='left')
ax.set_ylim(6e-6, 10)
ax.set_yticks([1.5e-5, 6e-3, 0.2]); ax.set_yticklabels([r'$1.5\times10^{-5}$', r'$6\times10^{-3}$', r'$0.2$'])
ax.tick_params(axis='y', length=2.5, pad=2); ax.minorticks_off()
ax.set_xticks([1, 18, 36, 54]); ax.tick_params(axis='x', length=2.5, pad=2)
style.arrows(ax, xlabel='update', ylabel=r'$(E-E_0)/J$', ticks=True)
style.save(fig, __file__)
