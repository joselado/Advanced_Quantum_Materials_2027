"""Session 2, the chain with a second-neighbor hopping eta, and the band of (2.9) for three values of eta."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import style

t = 1.0
eps = lambda p, eta: -2 * t * np.cos(p) - 2 * eta * np.cos(2 * p)
# extra extrema appear for eta > t/4: d eps/d phi = 2 t sin(phi) + 4 eta sin(2 phi) = 2 sin(phi) (t + 4 eta cos(phi))
p = np.linspace(-np.pi, np.pi, 2001)
n_ext = lambda eta: np.sum(np.diff(np.sign(np.diff(eps(p, eta)))) != 0)
assert n_ext(0.2) == 1 and n_ext(0.5) == 3            # interior extrema, the zone edge is the third one at eta=0.5 and not counted
fig = plt.figure(figsize=(style.WIDTH_CM * style.CM, 5.0 * style.CM))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.15], wspace=0.3)
axL = fig.add_subplot(gs[0]); axR = fig.add_subplot(gs[1])
axL.axis('off'); axL.set_aspect('equal')
N = 7
x = np.arange(N)
axL.plot([x[0] - 0.6, x[-1] + 0.6], [0, 0], color=style.GRID, lw=1.2, zorder=1)
axL.scatter(x, np.zeros(N), s=40, color=style.ACCENT, zorder=3)
for i in range(N - 1):                                             # nearest neighbor t, straight bond
    axL.plot([x[i], x[i + 1]], [0, 0], color=style.INK, lw=1.8, zorder=2)
style.label(axL, 1.5, -0.35, r'$t$', fontsize=9)
for i in range(N - 2):                                             # second neighbor eta, arc above
    c = style.BROKEN if i in (1,) else style.LIGHT
    th = np.linspace(0, np.pi, 40)
    axL.plot(x[i] + 1 + np.cos(th), 0.12 + 0.75 * np.sin(th), color=c, lw=1.2 if i != 1 else 1.8, zorder=2)
style.label(axL, 3.0, 1.15, r'$\eta$', color=style.BROKEN, fontsize=9)
axL.set_xlim(-0.8, N - 0.2); axL.set_ylim(-0.9, 1.5)
# bands
for eta, col, lw in ((0.0, style.GRID, 1.4), (0.2, style.LIGHT, 1.8), (0.5, style.ACCENT, 1.8)):
    axR.plot(p, eps(p, eta), color=col, lw=lw)
style.guide(axR, y=0)
style.arrows(axR, xlabel=r'$\varphi$', ylabel=r'$\epsilon/t$')
axR.set_xlim(-np.pi, np.pi); axR.set_ylim(-3.2, 2.4)
axR.set_xticks([-np.pi, 0, np.pi]); axR.set_xticklabels([r'$-\pi$', r'$0$', r'$\pi$'])
axR.tick_params(axis='x', length=2.5); axR.spines['bottom'].set_visible(True)
for y0, col, txt in ((-1.55, style.MUTED, r'$\eta=0$'), (-2.05, style.LIGHT, r'$\eta=0.2$'), (-2.55, style.ACCENT, r'$\eta=0.5$')):
    axR.plot([-2.95, -2.45], [y0, y0], color=col, lw=1.8)
    style.label(axR, -2.35, y0, txt, color=col, fontsize=8, ha='left')
axR.scatter([np.pi], [eps(np.pi, 0.5)], s=18, color=style.ACCENT, zorder=5)
axR.annotate('new minimum', xy=(np.pi, eps(np.pi, 0.5)), xytext=(0.9, -1.65), fontsize=8, color=style.INK, arrowprops=dict(arrowstyle='-', color=style.MUTED, lw=0.7))
style.save(fig, __file__)
