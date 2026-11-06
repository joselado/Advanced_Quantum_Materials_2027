"""Session 5, the splitting of the two end modes of a finite Kitaev chain as a function of its length."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

def bdg(N, t, mu, D):
    h = -mu * np.eye(N) - t * (np.eye(N, k=1) + np.eye(N, k=-1))
    d = D * (np.eye(N, k=-1) - np.eye(N, k=1))
    return np.block([[h, d], [d.conj().T, -h.T]])

t, mu, D = 1.0, 1.0, 0.5
Ns = np.arange(4, 31, 2)
E0 = np.array([np.sort(abs(np.linalg.eigvalsh(bdg(N, t, mu, D))))[0] for N in Ns])
E1 = np.array([np.sort(abs(np.linalg.eigvalsh(bdg(N, t, mu, D))))[2] for N in Ns])   # first bulk level
assert abs(E0[Ns == 8][0] - 0.011) < 0.0005 and abs(E0[Ns == 20][0] - 2e-5) < 5e-6

fig, ax = style.figure(height_cm=5.0, width_cm=10.5)
ax.semilogy(Ns, E0, 'o-', color=style.ACCENT, ms=3.2, lw=1.4)
ax.semilogy(Ns, E1, 's-', color=style.MUTED, ms=2.6, lw=1.0)
style.arrows(ax, xlabel=r'$N$', ylabel=r'$E$')
ax.set_xticks([8, 20]); ax.set_xticklabels(['8', '20'])
ax.tick_params(axis='x', length=2)
ax.set_xlim(2, 31); ax.set_ylim(1e-8, 3)
ax.set_yticks([1e-6, 1e-3, 1]); ax.set_yticklabels([r'$10^{-6}$', r'$10^{-3}$', r'$1$'])
ax.tick_params(axis='y', length=2)
ax.minorticks_off()
style.label(ax, 22, 0.25, 'first bulk level', color=style.MUTED, fontsize=8.5)
style.label(ax, 11.5, 2e-7, 'end modes', color=style.ACCENT, fontsize=8.5)
ax.annotate(r'$0.011t$', xy=(8, E0[Ns == 8][0]), xytext=(9.6, 0.05), fontsize=8.5, color=style.ACCENT, arrowprops=dict(arrowstyle='-', color=style.ACCENT, lw=0.7))
ax.annotate(r'$2\times10^{-5}t$', xy=(20, E0[Ns == 20][0]), xytext=(22.5, 6e-5), fontsize=8.5, color=style.ACCENT, arrowprops=dict(arrowstyle='-', color=style.ACCENT, lw=0.7))
style.save(fig, __file__)
