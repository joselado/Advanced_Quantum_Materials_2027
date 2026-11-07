"""Session 3, section 3.7, the bulk-boundary correspondence computed on a cylinder of the Haldane model.

The honeycomb lattice with first-neighbor hopping t=1 and the Haldane hopping t2=0.1 with the phase -pi/2, which gives C=1 at M=0.
The staggered potential M changes along the cylinder, M(y) = M0 [tanh((m-m1)/w) - tanh((m-m2)/w)]/2 with M0=1, w=2, m1=20 and
m2=60, on W=80 cells along a2 that close into a cylinder, so there is no edge with the vacuum. Where M=0 the bulk has C=1, and where
M=1 it has C=0. Panel (a) is M(y) and the local gap, the bulk gap of the Haldane model with the local value of M, which is
2|M - m_H| with m_H = 3 sqrt(3) t2 near the transition. It closes where M = m_H. Panel (b) is the spectrum of the cylinder against the
momentum k along the interfaces. The states inside the gap are colored by the interface where they sit, blue for the one at m1 and red for the one at m2,
which are the colors of the two crosses of (a)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import style, _honeycomb as hc
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

t2, phi = 0.1, -np.pi / 2
mH = 3 * np.sqrt(3) * t2
W, M0, w, m1, m2 = 80, 1.0, 2.0, 20, 60
m = np.arange(W)
Mprof = M0 * 0.5 * (np.tanh((m - m1) / w) - np.tanh((m - m2) / w))
C0, C1 = hc.chern(N=36, t2=t2, phi=phi), hc.chern(N=36, t2=t2, phi=phi, M=M0)
print('C at M=0', round(C0, 6), 'C at M=M0', round(C1, 6))
assert abs(C0 - 1) < 1e-6 and abs(C1) < 1e-6

K = np.array([4 * np.pi / 3, 0.0])
Bv = 2 * np.pi * np.linalg.inv(np.array([hc.a1, hc.a2])).T
grid = [i / 40 * Bv[0] + j / 40 * Bv[1] for i in range(40) for j in range(40)] + [K, -K]
def local_gap(M):
    return min(np.diff(np.linalg.eigvalsh(hc.bloch(k, t2=t2, phi=phi, M=M)))[0] for k in grid)
ys = np.linspace(0, W - 1, 321)
Mys = M0 * 0.5 * (np.tanh((ys - m1) / w) - np.tanh((ys - m2) / w))
gaps = np.array([local_gap(M) for M in Mys])
print('local gap in the C=1 region', local_gap(0.0), 'in the C=0 region', local_gap(M0), 'min', gaps.min())

ks = np.linspace(0, 2 * np.pi, 241)
E, side = [], []
for k in ks:
    e, v = np.linalg.eigh(hc.ribbon(k, W, t2=t2, phi=phi, M=Mprof, periodic=True))
    wt = (np.abs(v) ** 2).reshape(W, 2, -1).sum(1)
    near1 = wt[m1 - 8:m1 + 9].sum(0); near2 = wt[m2 - 8:m2 + 9].sum(0)
    E.append(e); side.append(near1 - near2)
E, side = np.array(E), np.array(side)
ingap = np.abs(E) < 0.45
print('in-gap states with weight > 0.9 on one interface', (ingap & (np.abs(side) > 0.9)).sum(), 'of', ingap.sum())

fig, axs = plt.subplots(1, 2, figsize=(12 * style.CM, 5.6 * style.CM), gridspec_kw=dict(wspace=0.38, width_ratios=[1.15, 1]))
ax = axs[0]
ax.axvspan(0, 79, color='white')
y_hit = [ys[i] for i in range(1, len(ys)) if (Mys[i - 1] - mH) * (Mys[i] - mH) < 0]
ax.plot(ys, Mys, color=style.MUTED, lw=1.3, ls='--')
ax.plot(ys, gaps, color=style.ACCENT)
for yh, col in zip(y_hit, (style.ACCENT, style.BROKEN)):          # the colors of the two interfaces in (b)
    ax.plot(yh, 0, 'x', color=col, ms=6, mew=1.6, clip_on=False, zorder=5)
ax.set_xlim(0, W - 1); ax.set_ylim(0, 1.35)
style.arrows(ax, xlabel=r'$y$')
style.label(ax, 13, 1.2, r'$C=1$', fontsize=11)
style.label(ax, 40, 1.2, r'$C=0$', fontsize=11)
style.label(ax, 67, 1.2, r'$C=1$', fontsize=11)
style.label(ax, 7, 0.1, r'$M$', color=style.MUTED, fontsize=11)
style.label(ax, 40, 0.55, 'local gap', color=style.ACCENT, fontsize=11)
ax.text(0.5, -0.17, '(a)', transform=ax.transAxes, ha='center', va='top', fontsize=11)
ax = axs[1]
keep = [j for j in range(E.shape[1]) if np.abs(E[:, j]).min() < 1.3]
Ek = np.vstack([E[::2, keep], np.full((1, len(keep)), np.nan)])        # all the bands as one path, every second k
Ek[np.abs(Ek) > 1.3] = np.nan                                           # nothing outside the window is drawn
ax.plot(np.tile(np.append(ks[::2], np.nan), len(keep)), Ek.T.ravel(), color=style.GRID, lw=0.6, zorder=0)
for sgn, col in ((1, style.ACCENT), (-1, style.BROKEN)):
    sel = ingap & (sgn * side > 0.5)
    ax.plot(np.broadcast_to(ks[:, None], E.shape)[sel], E[sel], 'o', ms=1.5, color=col, mec='none')
ax.set_xlim(0, 2 * np.pi); ax.set_ylim(-1.2, 1.2)
style.arrows(ax, xlabel=r'$k$', ylabel=r'$E/t$')
ax.set_xticks([0, np.pi, 2 * np.pi]); ax.set_xticklabels(['0', r'$\pi$', r'$2\pi$'], fontsize=11)
ax.set_yticks([-1, 0, 1]); ax.set_yticklabels(['$-1$', '0', '$1$'], fontsize=11); ax.tick_params(length=2.5, width=0.6)
ax.text(0.5, -0.17, '(b)', transform=ax.transAxes, ha='center', va='top', fontsize=11)
style.save(fig, __file__)
