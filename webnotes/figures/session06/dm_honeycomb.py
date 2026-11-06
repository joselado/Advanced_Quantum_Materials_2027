"""Session 6, the honeycomb lattice with the phases of the Dzyaloshinskii-Moriya term, and the magnon bands with a gap."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import style, _haldane as hd

t, t2 = 1.0, 0.1
pts, ticks = hd.path()
E = np.array([np.linalg.eigvalsh(hd.hk(k, t, t2)) for k in pts])
# the gap at K is 2 * 3 sqrt(3) t2 for phi = pi/2, and it is zero without the term
gapK = np.linalg.eigvalsh(hd.hk(np.array([4 * np.pi / 3, 0.0]), t, t2))
assert abs((gapK[1] - gapK[0]) - 6 * np.sqrt(3) * t2) < 1e-9
assert np.min(E[:, 1] - E[:, 0]) > 1.0
E0 = np.array([np.linalg.eigvalsh(hd.hk(k, t, 0.0)) for k in pts])
assert np.min(E0[:, 1] - E0[:, 0]) < 0.05

fig, axs = plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.8 * style.CM), gridspec_kw=dict(width_ratios=[1.1, 1]))
ax = axs[0]
ax.axis('off'); ax.set_aspect('equal')
d = (hd.a1 + hd.a2) / 3
# a patch of the lattice, the sites A at lattice points, B displaced by d
Rs = [n * hd.a1 + m * hd.a2 for n in range(-2, 3) for m in range(-2, 3)]
def inside(p): return np.hypot(*(p - np.array([0.0, 0.6]))) < 1.6
for R in Rs:
    A = R; 
    for dn, dm in hd.NN:
        B = R + dn * hd.a1 + dm * hd.a2 + d
        if inside(A) and inside(B):
            ax.plot([A[0], B[0]], [A[1], B[1]], color=style.GRID, lw=1.6, zorder=1)
for R in Rs:
    for sub, p in ((0, R), (1, R + d)):
        if inside(p):
            ax.plot([p[0]], [p[1]], 'o', color=style.ACCENT if sub == 0 else style.BROKEN, ms=4.5, zorder=3)
# the second-neighbor arrows around one hexagon, counterclockwise on A and clockwise on B
c = hd.a1 * 0 + d * 0
# the hexagon with A at 0, B at d, ... choose the hexagon whose centre is at (a1+a2)*2/3 - a2... use the one that contains A=0, B=d, A=a1... find the centre
centre = hd.a2 - d
hexa = [centre + (1 / np.sqrt(3)) * np.array([np.cos(-np.pi / 2 + j * np.pi / 3), np.sin(-np.pi / 2 + j * np.pi / 3)]) for j in range(6)]
# the six corners alternate A and B, each triangle of one sublattice has three second-neighbor arrows
def arrows_triangle(vs, col, ccw):
    cx = np.mean(vs, axis=0)
    ang = [np.arctan2(v[1] - cx[1], v[0] - cx[0]) for v in vs]
    order = np.argsort(ang)
    vs = [vs[i] for i in order]
    if not ccw:
        vs = vs[::-1]
    for i in range(3):
        a, b = vs[i], vs[(i + 1) % 3]
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=7, color=col, lw=1.0, shrinkA=3, shrinkB=3, zorder=4))
cornersA = [hexa[j] for j in range(0, 6, 2)]
cornersB = [hexa[j] for j in range(1, 6, 2)]
# which corners are A and which are B follows from the lattice, check it
def is_site(p, sub):
    for R in Rs:
        if np.hypot(*(p - (R if sub == 0 else R + d))) < 1e-6:
            return True
    return False
if not (all(is_site(p, 0) for p in cornersA) and all(is_site(p, 1) for p in cornersB)):
    cornersA, cornersB = cornersB, cornersA
assert all(is_site(p, 0) for p in cornersA) and all(is_site(p, 1) for p in cornersB), (hexa)
arrows_triangle(cornersA, style.ACCENT, True)
arrows_triangle(cornersB, style.BROKEN, False)
style.label(ax, 0.0, -1.35, r'phase $+\pi/2$ on $A$, $-\pi/2$ on $B$', fontsize=8, color=style.INK)
style.label(ax, 0.0, 2.35, r'(a) second-neighbor hopping, $t_2=DS$', fontsize=8.5)
ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.6, 2.6)

ax = axs[1]
x = np.arange(len(pts))
ax.plot(x, E0[:, 0], color=style.MUTED, lw=0.9, ls=(0, (3, 2))); ax.plot(x, E0[:, 1], color=style.MUTED, lw=0.9, ls=(0, (3, 2)))
ax.plot(x, E[:, 0], color=style.ACCENT); ax.plot(x, E[:, 1], color=style.ACCENT)
for tk in ticks:
    style.guide(ax, x=tk, color=style.GRID)
style.arrows(ax, xlabel='', ylabel=r'$E$')
for tk, lab in zip(ticks, [r'$\Gamma$', r'$K$', r'$M$', r'$\Gamma$']):
    style.label(ax, tk, -3.75, lab, fontsize=8.5)
style.label(ax, ticks[1], -0.0, r'$2\,\cdot 3\sqrt{3}\,t_2$', fontsize=0.1, alpha=0)
ax.annotate('', xy=(ticks[1] + 5, gapK[1]), xytext=(ticks[1] + 5, gapK[0]), arrowprops=dict(arrowstyle='<->', color=style.BROKEN, lw=0.9, shrinkA=0, shrinkB=0))
style.label(ax, ticks[1] + 12, 0, r'gap', color=style.BROKEN, fontsize=8.5, ha='left')
style.label(ax, 0.5 * (ticks[0] + ticks[3]), 3.7, '(b) bands, grey $t_2=0$', fontsize=8.5)
ax.set_xlim(0, len(pts) - 1); ax.set_ylim(-3.4, 3.4)
style.save(fig, __file__)
print('gap at K', gapK[1] - gapK[0])
