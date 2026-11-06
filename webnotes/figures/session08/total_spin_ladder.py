"""Session 8, quiz of 8.2, the total spins allowed for N spin-1/2 sites, with their multiplicities, checked against S^2 for N <= 7."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from math import comb
import style

def multiplicity(N, S2):
    """Number of times the total spin S = S2/2 occurs for N spin-1/2, from the binomial formula."""
    m = (N - S2) // 2
    return comb(N, m) - (comb(N, m - 1) if m >= 1 else 0)

sx = np.array([[0, 1], [1, 0]]) / 2; sy = np.array([[0, -1j], [1j, 0]]) / 2; sz = np.diag([.5, -.5])
def check(N):
    tot = [sum(np.kron(np.kron(np.eye(2 ** i), s), np.eye(2 ** (N - i - 1))) for i in range(N)) for s in (sx, sy, sz)]
    S2 = sum(t @ t for t in tot)
    ev = np.round(np.linalg.eigvalsh(S2), 8)
    for s2 in range(N % 2, N + 1, 2):
        S = s2 / 2
        assert (ev == round(S * (S + 1), 8)).sum() == (s2 + 1) * multiplicity(N, s2), (N, s2)
for N in range(1, 8):
    check(N)

fig, ax = style.plt.subplots(figsize=(9.5 * style.CM, 5.4 * style.CM))
Ns = range(2, 8)
for N in Ns:
    for s2 in range(N % 2, N + 1, 2):
        col = style.ACCENT if N % 2 == 0 else style.BROKEN
        ax.plot([s2 / 2], [N], 'o', ms=8.5, color=col)
        style.label(ax, s2 / 2, N + 0.0, r'%d' % multiplicity(N, s2), fontsize=6.8, color='white')
ax.set_xlim(-0.5, 3.9); ax.set_ylim(1.4, 7.6)
ax.set_xticks([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]); ax.set_xticklabels([r'$0$', r'$\frac{1}{2}$', r'$1$', r'$\frac{3}{2}$', r'$2$', r'$\frac{5}{2}$', r'$3$', r'$\frac{7}{2}$'])
ax.set_yticks(list(Ns))
ax.tick_params(length=2.5, pad=2)
ax.set_xlabel('total spin $S$', fontsize=8.8); ax.set_ylabel('number of sites $N$', fontsize=8.8)
for sp in ('top', 'right'):
    ax.spines[sp].set_visible(False)
style.save(fig, __file__)
