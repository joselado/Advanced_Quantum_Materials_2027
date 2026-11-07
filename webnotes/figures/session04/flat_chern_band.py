"""Session 4, section 4.20, a flat band with Chern number one at zero field, on the honeycomb lattice.

Both panels are the Haldane model of Section 3.10b, first-neighbor hopping t=1 and the second-neighbor hopping t2 exp(-i phi), along the
path Gamma, K, M, Gamma. Panel (a) is the case of Session 3, t2=0.1 and phi=pi/2. Panel (b) has t2=0.3, phi=0.4 pi and a third-neighbor
hopping t3=-0.2, found by a search on a grid of (t2, phi, t3) for the largest ratio of the gap to the width of the lower band.
The script prints the width W of the lower band, the gap Delta to the upper band, both on a 48 x 48 grid plus K, and the Chern number
of the lower band from the link variables. In (b) the ratio Delta/W is about 14, and the lower band has C=1 as in (a)."""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, '..'))
sys.path.insert(0, os.path.join(here, '..', 'session03'))
import numpy as np
import matplotlib.pyplot as plt
import style, _honeycomb as hc
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

cases = [dict(t2=0.1, phi=-np.pi / 2), dict(t2=0.3, phi=-0.4 * np.pi, t3=-0.2)]
Bv = 2 * np.pi * np.linalg.inv(np.array([hc.a1, hc.a2])).T
grid = [i / 48 * Bv[0] + j / 48 * Bv[1] for i in range(48) for j in range(48)] + [np.array([4 * np.pi / 3, 0.0])]
pts, ticks = hc.path(150)

fig, axs = plt.subplots(1, 2, figsize=(12 * style.CM, 5.6 * style.CM), gridspec_kw=dict(wspace=0.3))
for ax, kw, name in zip(axs, cases, ('(a) the model of Session 3', '(b) a flat Chern band')):
    Eg = np.array([np.linalg.eigvalsh(hc.bloch(k, **kw)) for k in grid])
    W = Eg[:, 0].max() - Eg[:, 0].min(); D = Eg[:, 1].min() - Eg[:, 0].max()
    C = hc.chern(N=40, **kw)
    print(name, 'W', round(W, 3), 'Delta', round(D, 3), 'Delta/W', round(D / W, 1), 'C', round(C, 6))
    assert abs(C - 1) < 1e-6
    E = np.array([np.linalg.eigvalsh(hc.bloch(k, **kw)) for k in pts])
    E = E - Eg[:, 0].mean()                           # the lower band is centred at zero in both panels
    ax.plot(np.arange(len(pts)), E[:, 1], color=style.MUTED, lw=1.4)
    ax.plot(np.arange(len(pts)), E[:, 0], color=style.ACCENT)
    for tk in ticks[1:-1]:
        style.guide(ax, x=tk)
    ax.set_xlim(0, len(pts) - 1); ax.set_ylim(-2.2, 6.2)
    style.arrows(ax, ylabel=r'$E/t$')
    ax.set_xticks(ticks); ax.set_xticklabels([r'$\Gamma$', r'$K$', r'$M$', r'$\Gamma$'], fontsize=11)
    ax.set_yticks([0, 2, 4, 6]); ax.set_yticklabels(['0', '2', '4', '6'], fontsize=11); ax.tick_params(length=2.5, width=0.6)
    i = int(0.58 * len(pts))                         # the label halfway between the two bands, between K and M
    style.label(ax, i, 0.5 * (E[i, 0] + E[i, 1]), r'$C=1$', color=style.ACCENT, fontsize=11)
    ax.text(0.5, -0.15, name, transform=ax.transAxes, ha='center', va='top', fontsize=11)
style.save(fig, __file__)
