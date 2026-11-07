"""Session 9, Section 9.8, a vacancy in a Chern insulator and in a trivial insulator with the same gap.

The honeycomb lattice on a torus of 18x18 unit cells (648 sites, no edges), first-neighbor hopping t=1. The
Chern insulator is the Haldane model with t2=0.15 and phase pi/2 (gap 6 sqrt(3) t2 = 1.56 at K and K'), the
trivial insulator has t2=0 and a sublattice mass M=0.78 (gap 2M = 1.56). One A site is removed. We plot the
local density of states summed on the three neighbors of the vacancy, with a Lorentzian broadening 0.03,
next to the same sum in the clean torus. The bulk gap is shaded."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
style.plt.rcParams.update({'font.size': 11, 'axes.labelsize': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5,
                           'legend.fontsize': 10.5})     # larger than the default, so that the labels read on a phone

L = 18
t, t2 = 1.0, 0.15
M = 3 * np.sqrt(3) * t2                      # same gap as the Haldane model
ETA = 0.03


def idx(x, y, s):
    return 2 * ((x % L) * L + (y % L)) + s


def hamiltonian(t2, M):
    N = 2 * L * L
    H = np.zeros((N, N), dtype=complex)
    # first neighbors: B at (x,y) is joined to A at (x,y), (x+1,y), (x,y+1)
    for x in range(L):
        for y in range(L):
            b = idx(x, y, 1)
            for (dx, dy) in ((0, 0), (1, 0), (0, 1)):
                a = idx(x + dx, y + dy, 0)
                H[a, b] -= t; H[b, a] -= t
            H[idx(x, y, 0), idx(x, y, 0)] += M
            H[b, b] -= M
            # second neighbors, the three vectors of one orientation, with the Haldane phase +pi/2 for A and -pi/2 for B
            for (dx, dy) in ((1, 0), (-1, 1), (0, -1)):
                for s, sg in ((0, 1), (1, -1)):
                    i, j = idx(x, y, s), idx(x + dx, y + dy, s)
                    H[i, j] += t2 * np.exp(1j * sg * np.pi / 2)
                    H[j, i] += t2 * np.exp(-1j * sg * np.pi / 2)
    return H


def ldos(H, sites, E):
    e, v = np.linalg.eigh(H)
    w = (np.abs(v[sites, :]) ** 2).sum(axis=0)
    return (w[None, :] * ETA / np.pi / ((E[:, None] - e[None, :]) ** 2 + ETA ** 2)).sum(axis=1), e, w


E = np.linspace(-1.6, 1.6, 801)
vac = idx(L // 2, L // 2, 0)
nbr = [idx(L // 2, L // 2, 1), idx(L // 2 - 1, L // 2, 1), idx(L // 2, L // 2 - 1, 1)]
keep = [i for i in range(2 * L * L) if i != vac]
sel = [keep.index(i) for i in nbr]

fig, axs = style.plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.4 * style.CM), sharey=True,
                              gridspec_kw=dict(wspace=0.25))
for ax, (tt2, MM, title) in zip(axs, ((0.0, M, 'trivial insulator'), (t2, 0.0, 'Chern insulator'))):
    H = hamiltonian(tt2, MM)
    e0 = np.linalg.eigvalsh(H)
    gap = (e0[e0 > 0].min(), e0[e0 < 0].max())
    d0, _, _ = ldos(H, nbr, E)
    Hv = H[np.ix_(keep, keep)]
    d1, e1, w1 = ldos(Hv, sel, E)
    ingap = [(round(float(x), 3), round(float(y), 3)) for x, y in zip(e1, w1) if gap[1] + 0.02 < x < gap[0] - 0.02]
    print(title, 'gap edges %.3f %.3f' % (gap[1], gap[0]), 'in-gap levels (E, weight on the 3 neighbors):', ingap)
    ax.axvspan(gap[1], gap[0], color=style.GRID, alpha=0.6, lw=0, zorder=0)
    ax.plot(E, d0, color=style.MUTED, lw=1.0, label='clean')
    ax.plot(E, d1, color=style.BROKEN if tt2 else style.ACCENT, lw=1.5, label='with vacancy')
    style.arrows(ax, xlabel=r'$E/t$')
    ax.set_xlim(E[0], E[-1])
    ax.set_title(title, fontsize=11.5, pad=10)
    ax.set_xticks([-1, 0, 1]); ax.tick_params(axis='x', length=2.5, pad=2)
top = 1.08 * max(l.get_ydata().max() for a in axs for l in a.get_lines())
axs[0].set_ylim(0, top)
for ax in axs:
    style.label(ax, -0.42, top * 0.9, 'gap', color=style.MUTED, fontsize=11.5)
axs[0].annotate(r'LDOS', xy=(0, 1.06), xycoords='axes fraction', ha='center', va='bottom')
style.label(axs[0], 0.05, top * 0.45, 'no bound\nstate', color=style.ACCENT, fontsize=11.5)
style.label(axs[1], 0.1, top * 0.62, 'bound\nstate', color=style.BROKEN, fontsize=11.5, ha='left')
style.save(fig, __file__)
