"""Session 3, section 3.11b, the helical edge of the Kane-Mele ribbon with a term that keeps time reversal and with one that breaks it.

The Kane-Mele zigzag ribbon of W=40 cells, t=1 and intrinsic spin-orbit coupling t2=0.1 (the Haldane hopping with the phase +pi/2 for
spin up and -pi/2 for spin down). Panel (a) adds the Rashba coupling lr=0.15, which mixes the spins and keeps time reversal. Panel (b)
adds to it the in-plane exchange field bx=0.1, which breaks time reversal. Only the states on the lower edge are drawn in color, those
with more than half of their weight on the 6 cells next to it, and the color is the sign of <s_z>. The crossing is at k=pi, which is a
time-reversal invariant momentum. The script prints the smallest |E| at k=pi in both cases."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import style, _honeycomb as hc
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

W, t2, lr, bx = 40, 0.1, 0.15, 0.1
ks = np.linspace(np.pi - 1.4, np.pi + 1.4, 281)
SZ = np.tile([1.0, -1.0], 2 * W)


def bands(b):
    E, low, sz = [], [], []
    for k in ks:
        e, v = np.linalg.eigh(hc.ribbon_spinful(k, W, lso=t2, lr=lr, bx=b))
        p = np.abs(v) ** 2
        E.append(e); low.append(p[:4 * 6].sum(0)); sz.append(SZ @ p)
    return np.array(E), np.array(low), np.array(sz)


for b in (0.0, bx):
    e = np.linalg.eigvalsh(hc.ribbon_spinful(np.pi, W, lso=t2, lr=lr, bx=b))
    print('bx', b, 'smallest |E| at k=pi', np.sort(np.abs(e))[:2])

fig, axs = plt.subplots(1, 2, figsize=(12 * style.CM, 5.4 * style.CM), gridspec_kw=dict(wspace=0.3))
for ax, b, name in ((axs[0], 0.0, '(a) Rashba, keeps time reversal'), (axs[1], bx, '(b) exchange, breaks it')):
    E, low, sz = bands(b)
    keep = [j for j in range(E.shape[1]) if np.abs(E[:, j]).min() < 1.0]
    Ek = np.vstack([E[::2, keep], np.full((1, len(keep)), np.nan)])
    Ek[np.abs(Ek) > 0.75] = np.nan
    ax.plot(np.tile(np.append(ks[::2], np.nan), len(keep)), Ek.T.ravel(), color=style.GRID, lw=0.6, zorder=0)
    kk = np.broadcast_to(ks[:, None], E.shape)
    for sgn, col in ((1, style.BROKEN), (-1, style.ACCENT)):
        sel = (np.abs(E) < 0.42) & (low > 0.5) & (sgn * sz > 0)
        ax.plot(kk[sel], E[sel], 'o', ms=1.5, color=col, mec='none')
    ax.set_xlim(ks[0], ks[-1]); ax.set_ylim(-0.7, 0.7)
    style.arrows(ax, xlabel=r'$k$', ylabel=r'$E/t$')
    ax.set_xticks([np.pi]); ax.set_xticklabels([r'$\pi$'], fontsize=11)
    ax.set_yticks([-0.5, 0, 0.5]); ax.set_yticklabels(['$-0.5$', '0', '$0.5$'], fontsize=11); ax.tick_params(length=2.5, width=0.6)
    ax.text(0.5, -0.17, name, transform=ax.transAxes, ha='center', va='top', fontsize=11)
axs[0].text(np.pi + 0.95, 0.12, 'up', color=style.BROKEN, fontsize=11, ha='center')
axs[0].text(np.pi - 0.95, 0.12, 'down', color=style.ACCENT, fontsize=11, ha='center')
style.save(fig, __file__)
