"""Session 5, where the lowest state of an open Kitaev chain sits, in the topological and in the trivial phase."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

def bdg(N, t, mu, D):
    """BdG matrix of (5.19) on an open chain, in the basis (c_1..c_N, c_1^dag..c_N^dag)."""
    h = -mu * np.eye(N) - t * (np.eye(N, k=1) + np.eye(N, k=-1))
    d = D * (np.eye(N, k=-1) - np.eye(N, k=1))
    return np.block([[h, d], [d.conj().T, -h.T]])

def lowest_weight(N, t, mu, D):
    """Weight |u_n|^2+|v_n|^2 on each site of the lowest state with E>0, and its energy."""
    e, v = np.linalg.eigh(bdg(N, t, mu, D))
    i = np.argmax(e > 0)
    i = np.where(e > 0)[0][np.argmin(e[e > 0])]
    psi = v[:, i]
    w = abs(psi[:N])**2 + abs(psi[N:])**2
    return w, e[i]

N, t, D = 40, 1.0, 0.5
w1, e1 = lowest_weight(N, t, 1.0, D)
w2, e2 = lowest_weight(N, t, 2.5, D)
assert abs(w1.sum() - 1) < 1e-9 and e1 < 1e-4 and e2 > 0.3
assert w1[:4].sum() + w1[-4:].sum() > 0.9 and w2[N // 2 - 8:N // 2 + 8].sum() > 0.5

fig, axs = plt.subplots(2, 1, figsize=(style.WIDTH_CM * style.CM, 6.6 * style.CM), sharex=True)
n = np.arange(1, N + 1)
for ax, w, col, ttl in ((axs[0], w1, style.ACCENT, r'(a) $\mu=t$, topological, $E\approx 0$'),
                        (axs[1], w2, style.BROKEN, r'(b) $\mu=2.5t$, trivial, $E=%.2ft$' % e2)):
    style.arrows(ax, xlabel=None, ylabel=None)
    ax.vlines(n, 0, w, color=col, lw=2.2)
    ax.set_ylim(0, 0.46); ax.set_xlim(0, N + 2)
    style.label(ax, N / 2 + 1, 0.40, ttl, fontsize=8.5)
style.label(axs[1], N + 3.5, 0.0, 'site', fontsize=8.5, ha='left')
fig.text(0.02, 0.5, 'weight of the lowest state', rotation=90, va='center', fontsize=8.5, color=style.INK)
fig.subplots_adjust(left=0.1, hspace=0.25)
style.save(fig, __file__)
