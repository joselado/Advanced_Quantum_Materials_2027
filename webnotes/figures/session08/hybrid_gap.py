"""Session 8, quiz of 8.13, the two bands of (8.21) per spin for gamma = 0.5 and gamma = 1, with the direct gap at the crossing."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

t = 1.0
k = np.linspace(-np.pi, np.pi, 401)
eps = -2 * t * np.cos(k)
def bands(g):
    H = np.array([[[e, -g], [-g, 0.0]] for e in eps])
    return np.linalg.eigvalsh(H)
res = {}
for g in (0.5, 1.0):
    E = bands(g)
    gap = (E[:, 1] - E[:, 0]).min()
    res[g] = gap
    assert abs(gap - 2 * g) < 1e-3, (g, gap)                          # direct gap at eps_k = 0 is 2 gamma
assert abs(res[1.0] / res[0.5] - 2) < 1e-2

fig, axs = style.plt.subplots(1, 2, figsize=(9.5 * style.CM, 4.9 * style.CM), sharey=True)
for ax, g, col in zip(axs, (0.5, 1.0), (style.ACCENT, style.BROKEN)):
    style.arrows(ax, xlabel=r'$k$')
    E = bands(g)
    ax.axhline(0, color=style.GRID, lw=1.0, zorder=0)
    for b in range(2):
        ax.plot(k, E[:, b], color=col)
    i = np.argmin(np.abs(k + np.pi / 2))
    ax.annotate('', xy=(k[i], E[i, 1]), xytext=(k[i], E[i, 0]), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.9, shrinkA=0, shrinkB=0))
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-3.0, 3.0)
    style.label(ax, 0, 3.6, r'$\gamma_K=%g$, direct gap $%g$' % (g, 2 * g), fontsize=8.5)
axs[0].set_yticks([-2, 0, 2]); axs[0].tick_params(axis='y', length=2.5, pad=2); axs[0].set_ylabel(r'$E/t$', fontsize=9)
axs[1].tick_params(axis='y', left=False)
style.save(fig, __file__)
