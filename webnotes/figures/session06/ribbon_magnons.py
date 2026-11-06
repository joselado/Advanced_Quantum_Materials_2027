"""Session 6, the edge states of a magnon ribbon with the Dzyaloshinskii-Moriya term of one sign and of the opposite sign."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import style, _haldane as hd

W, t = 24, 1.0
kxs = np.linspace(-np.pi, np.pi, 241)

def bands(t2):
    E, side = [], []
    for kx in kxs:
        e, v = np.linalg.eigh(hd.ribbon(kx, W, t, t2))
        w = abs(v)**2
        lower = w[:2 * 5].sum(axis=0); upper = w[-2 * 5:].sum(axis=0)    # weight on the 5 first and the 5 last cells
        E.append(e); side.append(lower - upper)
    return np.array(E), np.array(side)

res = {s: bands(s * 0.1) for s in (+1, -1)}
# the edge branch in the gap, its velocity on each edge. For one sign the lower edge carries v>0, for the other v<0.
def edge_velocity(E, side, edge):
    vs = []
    for j in range(E.shape[1]):
        e = E[:, j]; sd = side[:, j]
        sel = (abs(e) < 0.35) & (edge * sd > 0.6)
        if sel.sum() > 20:
            idx = np.where(sel)[0]
            vs.append(np.polyfit(kxs[idx], e[idx], 1)[0])
    return np.mean(vs)
vp = [edge_velocity(*res[+1], edge=e) for e in (+1, -1)]
vm = [edge_velocity(*res[-1], edge=e) for e in (+1, -1)]
assert vp[0] * vp[1] < 0 and vm[0] * vm[1] < 0 and vp[0] * vm[0] < 0, (vp, vm)

fig, axs = plt.subplots(1, 2, figsize=(11.0 * style.CM, 5.2 * style.CM), sharey=True)
for ax, s, ttl in zip(axs, (+1, -1), (r'(a) $D>0$', r'(b) $D<0$')):
    E, side = res[s]
    for j in range(E.shape[1]):
        c = np.where(side[:, j] > 0.6, 1, np.where(side[:, j] < -0.6, -1, 0))
        ax.plot(kxs, E[:, j], color=style.GRID, lw=0.8, zorder=1)
        for val, col in ((1, style.ACCENT), (-1, style.BROKEN)):
            m = c == val
            ax.plot(kxs[m], E[m, j], '.', color=col, ms=1.8, zorder=3)
    style.arrows(ax, xlabel=r'$k_x$', ylabel=r'$E$' if s > 0 else '')
    style.label(ax, 0, 1.75, ttl, fontsize=8.5)
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-1.7, 1.7)
    ax.set_xticks([])
style.label(axs[0], -2.05, -1.45, 'lower edge', color=style.ACCENT, fontsize=8)
style.label(axs[0], 2.05, -1.45, 'upper edge', color=style.BROKEN, fontsize=8)
fig.subplots_adjust(wspace=0.12)
style.save(fig, __file__)
print(vp, vm)
