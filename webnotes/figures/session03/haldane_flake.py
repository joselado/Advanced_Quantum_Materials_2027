"""Session 3, section 3.1, a gapped bulk with states at the boundary, computed on a finite flake of the honeycomb lattice.

A disk of radius 11 of the honeycomb lattice with first-neighbor hopping t=1, about 860 sites. The topological flake has the
Haldane hopping t2=0.1 of Section 3.10b, with the bulk gap 6 sqrt(3) t2 = 1.04. The trivial flake has instead the staggered
potential M=0.52, which gives the same bulk gap 2M with Chern number zero. Panel (a) is the sorted spectrum of the two flakes,
the 91 states around the middle, with the grey band for the bulk gap. Panel (b) is the weight of the states of the topological flake with |E| < 0.3, the
local density of states inside the gap, drawn as a dot on every site in four sizes of growing weight."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import style, _honeycomb as hc
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

R, t2, M = 11.0, 0.1, 0.52
gap = 3 * np.sqrt(3) * t2
pts, sub, Ht = hc.flake(R, t2=t2)
_, _, Hs = hc.flake(R, M=M)
et, vt = np.linalg.eigh(Ht)
es = np.linalg.eigvalsh(Hs)
ing = np.abs(et) < 0.3
w = (np.abs(vt[:, ing]) ** 2).sum(1)
rr = np.hypot(*pts.T)
print('sites', len(pts), 'in-gap states topological', ing.sum(), 'trivial', (np.abs(es) < 0.3).sum())
print('weight in the outer ring r > R-2', w[rr > R - 2].sum() / w.sum(), 'fraction of sites there', (rr > R - 2).mean())

fig = plt.figure(figsize=(12 * style.CM, 5.6 * style.CM))
ax = fig.add_axes([0.08, 0.14, 0.4, 0.78]); style.arrows(ax)
n0 = len(et) // 2
x = np.arange(len(et)) - n0
win = np.abs(x) <= 45                        # the 90 states around the middle of the spectrum
ax.axhspan(-gap, gap, color=style.GRID, alpha=0.6, lw=0, zorder=0)
ax.plot(x[win], es[win], 'o', ms=2.6, color=style.MUTED, mec='none')
ax.plot(x[win], et[win], 'o', ms=2.6, color=style.ACCENT, mec='none')
ax.set_xlim(-47, 47); ax.set_ylim(-1.25, 1.25)
style.arrows(ax, xlabel='state', ylabel=r'$E/t$')
ax.set_yticks([-1, -0.5, 0, 0.5, 1]); ax.set_yticklabels(['$-1$', '', '0', '', '$1$'], fontsize=11)
ax.tick_params(length=2.5, width=0.6)
style.label(ax, -18, 0.22, 'Haldane', color=style.ACCENT, fontsize=11)
style.label(ax, 22, -0.25, 'trivial', color=style.MUTED, fontsize=11)
style.label(ax, -30, 0.78, 'bulk gap', color=style.INK, fontsize=11)
ax.annotate('', xy=(-30, gap), xytext=(-30, 0.68), arrowprops=dict(arrowstyle='-|>', lw=0.6, color=style.INK, mutation_scale=7))
ax.text(0.5, -0.19, '(a)', transform=ax.transAxes, ha='center', va='top', fontsize=11)
ax = fig.add_axes([0.56, 0.1, 0.42, 0.86])
ax.set_aspect('equal'); ax.axis('off')
D = np.linalg.norm(pts[:, None] - pts[None], axis=-1)
I, J = np.where(np.triu(np.abs(D - 1 / np.sqrt(3)) < 1e-6))
seg = np.full((len(I), 3, 2), np.nan); seg[:, 0] = pts[I]; seg[:, 1] = pts[J]
ax.plot(*seg.reshape(-1, 2).T, color=style.GRID, lw=0.5)   # all the bonds as one path
# four marker sizes, so that the SVG reuses one marker per size and stays small
lev = np.digitize(w / w.max(), [0.03, 0.15, 0.4, 0.7])
for L, ms in ((1, 1.6), (2, 2.8), (3, 4.0), (4, 5.0)):
    ax.plot(*pts[lev == L].T, 'o', ms=ms, color=style.ACCENT, mec='none')
ax.set_xlim(-R, R); ax.set_ylim(-R, R)
ax.text(0.5, -0.06, '(b)', transform=ax.transAxes, ha='center', va='top', fontsize=11)
style.save(fig, __file__)
