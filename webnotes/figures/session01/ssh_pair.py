"""Session 1, two chains with alternating hoppings 1 and 2 that have the same bulk bands and different edges."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

def levels(t1, t2, N=20):
    T = np.zeros((N, N))
    for i in range(N - 1):
        T[i, i + 1] = T[i + 1, i] = t1 if i % 2 == 0 else t2      # open chain, first bond is the intracell one
    w, v = np.linalg.eigh(T)
    return w, v
wA, vA = levels(1.0, 2.0)      # weak bond at the ends: end states
wB, vB = levels(2.0, 1.0)      # strong bond at the ends: no end states
inA = np.sum(np.abs(wA) < 0.1); inB = np.sum(np.abs(wB) < 0.1)
assert inA == 2 and inB == 0
# the same bulk: both have the bands |t1 - t2| < |E| < t1 + t2, i.e. a gap of 2 around zero
bulkA = np.sort(np.abs(wA))[2:]; bulkB = np.sort(np.abs(wB))
assert abs(bulkA.min() - 1) < 0.15 and abs(bulkB.min() - 1) < 0.15
fig = plt.figure(figsize=(9.6 * style.CM, 4.4 * style.CM))
gs = fig.add_gridspec(1, 2, width_ratios=[1.5, 1], wspace=0.4)
axL = fig.add_subplot(gs[0]); axR = fig.add_subplot(gs[1])
axL.axis('off'); axL.set_aspect('equal')
def chain(y, t1, t2, name, end):
    x = np.arange(6) * 1.0
    for i in range(5):
        tt = t1 if i % 2 == 0 else t2
        axL.plot([x[i], x[i + 1]], [y, y], color=style.INK, lw=0.8 + 1.1 * tt)
    axL.scatter(x, [y] * 6, s=30, color=style.ACCENT, zorder=3)
    for i in range(5):
        tt = t1 if i % 2 == 0 else t2
        style.label(axL, x[i] + 0.5, y + 0.5, rf'${tt:.0f}$', fontsize=8)
    style.label(axL, -0.9, y, name, ha='right', fontsize=8.5)
    if end:
        for xe in (x[0], x[-1]):
            axL.scatter([xe], [y], s=200, color=style.BROKEN, alpha=0.28, zorder=2)
chain(1.0, 1.0, 2.0, 'A', True)
chain(-0.4, 2.0, 1.0, 'B', False)
style.label(axL, 2.5, 2.1, 'end states', color=style.BROKEN, fontsize=8)
style.label(axL, 2.5, -1.4, 'no end states', color=style.MUTED, fontsize=8)
axL.set_xlim(-1.8, 6.4); axL.set_ylim(-1.7, 2.4)
# spectra of the open chains of 20 sites
axR.set_xlim(0, 2.3); axR.set_ylim(-3.4, 3.4)
for s in ('top', 'right', 'bottom'): axR.spines[s].set_visible(False)
axR.set_xticks([]); axR.set_yticks([-3, -1, 0, 1, 3])
for j, (w, off) in enumerate(((wA, 0.2), (wB, 1.4))):
    for e in w:
        c = style.BROKEN if (j == 0 and abs(e) < 0.1) else style.ACCENT
        axR.plot([off, off + 0.7], [e, e], color=c, lw=1.0 if c == style.ACCENT else 2.0)
style.label(axR, 0.55, -3.7, 'A', fontsize=9); style.label(axR, 1.75, -3.7, 'B', fontsize=9)
axR.set_ylabel(r'$E$', rotation=0, labelpad=8)
axR.axhspan(-1, 1, color=style.GRID, alpha=0.35, lw=0)
style.label(axR, 1.75, 0.0, 'gap', fontsize=8, color=style.INK)
style.save(fig, __file__)
