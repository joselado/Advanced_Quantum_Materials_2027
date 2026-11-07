"""Session 3, section 3.11, the two spin sectors of the quantum spin Hall insulator on a zigzag ribbon.

The Kane-Mele model is two copies of the Haldane model, with the second-neighbor hopping t2 exp(+i pi/2) for spin up and
t2 exp(-i pi/2) for spin down, t=1 and t2=0.1, so the two sectors have opposite Chern numbers. The ribbon has W=40 cells along a2
and is periodic along a1 with the momentum k. In each panel the states in the gap are colored by the edge where they sit, with the
weight on the 6 cells next to each edge. For spin up the branch of the lower edge has a positive velocity at E=0, for spin down a
negative one, so on one edge the two spins move in opposite directions."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import style, _honeycomb as hc
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

W, t2 = 40, 0.1
ks = np.linspace(0, 2 * np.pi, 241)
print('C up', round(hc.chern(N=30, t2=t2, phi=np.pi / 2), 6), 'C down', round(hc.chern(N=30, t2=t2, phi=-np.pi / 2), 6))


def bands(phi):
    E, side = [], []
    for k in ks:
        e, v = np.linalg.eigh(hc.ribbon(k, W, t2=t2, phi=phi))
        wt = (np.abs(v) ** 2).reshape(W, 2, -1).sum(1)
        E.append(e); side.append(wt[:6].sum(0) - wt[-6:].sum(0))
    return np.array(E), np.array(side)


fig, axs = plt.subplots(1, 2, figsize=(12 * style.CM, 5.4 * style.CM), gridspec_kw=dict(wspace=0.3))
for ax, phi, name in ((axs[0], np.pi / 2, '(a) spin up'), (axs[1], -np.pi / 2, '(b) spin down')):
    E, side = bands(phi)
    keep = [j for j in range(E.shape[1]) if np.abs(E[:, j]).min() < 1.3]
    Ek = np.vstack([E[::2, keep], np.full((1, len(keep)), np.nan)])
    Ek[np.abs(Ek) > 1.3] = np.nan
    ax.plot(np.tile(np.append(ks[::2], np.nan), len(keep)), Ek.T.ravel(), color=style.GRID, lw=0.6, zorder=0)
    ingap = np.abs(E) < 0.45
    for sgn, col in ((1, style.ACCENT), (-1, style.BROKEN)):
        sel = ingap & (sgn * side > 0.5)
        kk = np.broadcast_to(ks[:, None], E.shape)[sel]
        ax.plot(kk, E[sel], 'o', ms=1.5, color=col, mec='none')
        # the velocity at E=0 of the branch of this edge
        near = np.abs(E[sel]) < 0.2
        print(name, 'edge', 'lower' if sgn > 0 else 'upper', 'velocity', round(np.polyfit(kk[near], E[sel][near], 1)[0], 3))
    ax.set_xlim(0, 2 * np.pi); ax.set_ylim(-1.2, 1.2)
    style.arrows(ax, xlabel=r'$k$', ylabel=r'$E/t$')
    ax.set_xticks([0, np.pi, 2 * np.pi]); ax.set_xticklabels(['0', r'$\pi$', r'$2\pi$'], fontsize=11)
    ax.set_yticks([-1, 0, 1]); ax.set_yticklabels(['$-1$', '0', '$1$'], fontsize=11); ax.tick_params(length=2.5, width=0.6)
    ax.text(0.5, -0.17, name, transform=ax.transAxes, ha='center', va='top', fontsize=11)
axs[0].text(5.0, 0.2, 'lower\nedge', color=style.ACCENT, fontsize=11, ha='center', va='center')
axs[0].text(1.3, 0.2, 'upper\nedge', color=style.BROKEN, fontsize=11, ha='center', va='center')
style.save(fig, __file__)
