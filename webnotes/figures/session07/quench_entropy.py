"""Session 7, the half-chain entropy after a quench of a transverse-field Ising chain of 12 sites, by exact time evolution."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla
import style

L = 12
sx = sp.csr_matrix([[0, 1], [1, 0]]); sz = sp.csr_matrix([[1, 0], [0, -1]])
def op(o, i):
    return sp.kron(sp.kron(sp.identity(2 ** i), o), sp.identity(2 ** (L - i - 1)), format='csr')
g = 1.0
H = -sum(op(sz, i) @ op(sz, i + 1) for i in range(L - 1)) - g * sum(op(sx, i) for i in range(L))
psi = np.zeros(2 ** L, dtype=complex); psi[0] = 1               # all spins up along z, the ground state of the chain at g=0
dt = 0.05
ts = np.arange(0, 5 + dt / 2, dt)
S = []
for t in ts:
    s = np.linalg.svd(psi.reshape(2 ** (L // 2), -1), compute_uv=False) ** 2
    s = s[s > 1e-14]
    S.append(-np.sum(s * np.log(s)))
    psi = sla.expm_multiply(-1j * dt * H, psi)
assert abs(np.linalg.norm(psi) - 1) < 1e-8
S = np.array(S) / np.log(2)
assert S[0] < 1e-12 and S.max() <= L / 2 + 1e-9
print('S(t) at', ts[[20, 40, 60, 80]], S[[20, 40, 60, 80]], 'max', S.max(), ts[S.argmax()])

fig, ax = style.figure(height_cm=5.4)
ax.plot(ts, S, color=style.ACCENT)
for M, col in ((2, style.MUTED), (4, style.BROKEN), (8, style.ACCENT)):
    ax.axhline(np.log2(M), color=col, lw=1.2, ls=(0, (3, 3)))
for M, col in ((2, style.MUTED), (4, style.BROKEN), (8, style.ACCENT)):
    style.label(ax, 5.2, np.log2(M) + 0.25, r'$M=%d$' % M, color=col, fontsize=8.5, ha='right')
ax.set_xlim(0, 5.3); ax.set_ylim(0, 4.0)
ax.set_xticks([0, 1, 2, 3, 4, 5]); ax.set_yticks([0, 1, 2, 3]); ax.tick_params(length=2.5, pad=2)
style.arrows(ax, xlabel=r'$t$', ylabel=r'$S/\log 2$', ticks=True)
style.save(fig, __file__)
