"""Session 5, the lowest levels of an open Kitaev chain as a function of the chemical potential."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

def bdg(N, t, mu, D):
    """BdG matrix of (5.19) on an open chain, in the basis (c_1..c_N, c_1^dag..c_N^dag)."""
    h = -mu * np.eye(N) - t * (np.eye(N, k=1) + np.eye(N, k=-1))
    d = D * (np.eye(N, k=-1) - np.eye(N, k=1))       # antisymmetric pairing matrix of D(c_n c_{n+1} + h.c.)
    return np.block([[h, d], [d.conj().T, -h.T]])

N, t, D = 60, 1.0, 0.7
mus = np.linspace(-3.4, 3.4, 341)
low = []
for mu in mus:
    ev = np.linalg.eigvalsh(bdg(N, t, mu, D))
    low.append(np.sort(np.abs(ev))[::2][:3])      # the levels come in pairs +E, -E
low = np.array(low)

# checks against the text, the zero modes of the sweet spot and the criterion (5.22)
ev0 = np.linalg.eigvalsh(bdg(N, t, 0.0, t))
assert np.sum(abs(ev0) < 1e-9) == 2
inside = low[abs(mus) < 1.8, 0]
outside = low[abs(mus) > 2.3, 0]
assert inside.max() < 1e-3 and outside.min() > 0.05, (inside.max(), outside.min())

fig, ax = style.figure(height_cm=5.8)
for j, a in enumerate((1.0, 0.55, 0.55)):
    ax.plot(mus, low[:, j], color=style.ACCENT, alpha=a, lw=1.8 if j == 0 else 1.2)
ax.axvspan(-2, 2, color=style.GRID, alpha=0.45, lw=0, zorder=0)
for x in (-2, 2):
    style.guide(ax, x=x, color=style.MUTED, lw=0.8, ls=(0, (3, 2)))
style.arrows(ax, xlabel=r'$\mu$', ylabel=r'$E$')
style.label(ax, 0, 0.55, r'topological, $|\mu|<2t$', fontsize=8.5)
style.label(ax, 0, 0.35, r'two states pinned at $E=0$', fontsize=8.5, color=style.ACCENT)
for s in (-1, 1):
    style.label(ax, s * 2.85, 0.3, 'trivial', fontsize=8.5)
    style.label(ax, s * 2.0, -0.12, r'$%s2t$' % ('-' if s < 0 else ''), fontsize=8.5)
ax.set_xlim(-3.4, 3.4); ax.set_ylim(0, 1.7)
style.save(fig, __file__)
