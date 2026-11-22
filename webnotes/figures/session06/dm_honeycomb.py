"""Session 6, the honeycomb lattice with the phases of the Dzyaloshinskii-Moriya term, and the magnon bands with a gap.

Panel (a) is a drawing of the second-neighbor hops, counterclockwise on A with the phase +pi/2 and clockwise on B with -pi/2,
which is D > 0 in the convention of the conventions sheet of Session 6. Panel (b) was redrawn on 2026-11-22 from the pyqula
script webnotes/scripts/session06/g5_magnon_honeycomb.py, which the student downloads: the magnon bands of the honeycomb
ferromagnet with |J|S = 1, the onsite energy 3|J|S and DS = 0.1, which is h.add_haldane(-0.1155), and the bands with DS = 0 in
grey. The numpy model of _haldane.py, 3|J|S + _haldane.hk(k, t=|J|S, t2=-DS), is the second route for the same bands."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import style, _haldane as hd

res = style.run_script('session06/g5_magnon_honeycomb.py')
DS = res['DS']
E, E0 = np.asarray(res['bands'], float), np.asarray(res['bands_plain'], float)
assert DS == 0.1 and E.shape == (301, 2) and E0.shape == (301, 2)
# the path is Gamma, K, M, Gamma with 100 steps per segment: K is a corner of the zone and M the middle of the edge next to it
g = res['g']
A = np.array([np.asarray(g.a1, float)[:2], np.asarray(g.a2, float)[:2]])
B = 2 * np.pi * np.linalg.inv(A).T
G_, K_, M_ = [np.asarray(res['nodes'][i], float)[:2] @ B for i in range(3)]
assert abs(np.linalg.norm(K_) - 4 * np.pi / (3 * np.sqrt(3))) < 1e-9 and abs(np.linalg.norm(M_) - np.sqrt(3) / 2 * np.linalg.norm(K_)) < 1e-9
assert abs((K_ - M_) @ M_) < 1e-9 and abs(np.linalg.norm(g.r[0] - g.r[1]) - 1) < 1e-12        # bond length 1
ticks = [0, 100, 200, 300]
# the numbers of the caption: zero at Gamma, the gap at K from 2.48 to 3.52, its width 6 sqrt(3) DS = 1.04, the top 6, DS = 0 touches
assert np.allclose(E[0], [0.0, 6.0], atol=1e-9) and abs(E.min()) < 1e-9 and abs(E.max() - 6.0) < 1e-9
assert np.allclose(E[100], [3 - 3 * np.sqrt(3) * DS, 3 + 3 * np.sqrt(3) * DS], atol=1e-9)
assert abs(E[100, 0] - 2.48) < 5e-3 and abs(E[100, 1] - 3.52) < 5e-3 and abs((E[100, 1] - E[100, 0]) - 1.04) < 5e-3
assert abs((E[:, 1] - E[:, 0]).min() - 6 * np.sqrt(3) * DS) < 1e-9                       # the smallest gap of the path is at K
assert abs(E0[100, 1] - E0[100, 0]) < 1e-9 and np.allclose(E0[0], [0.0, 6.0], atol=1e-9)
# the Chern number of the lower band from the script, -1 for this sign of DS, and the upper band has the opposite
assert abs(res['chern'] + 1) < 1e-6, res['chern']
# the second route, the numpy magnon matrix of the conventions sheet on the same path of its own lattice
Gh, Kh, Mh = np.zeros(2), np.array([4 * np.pi / 3, 0.0]), np.array([np.pi, np.pi / np.sqrt(3)])
nod = [Gh, Kh, Mh, Gh]
pts = [nod[i] + (nod[i + 1] - nod[i]) * j / 100 for i in range(3) for j in range(100)] + [Gh]
Eh = np.array([np.linalg.eigvalsh(3 * np.eye(2) + hd.hk(k, 1.0, -DS)) for k in pts])
assert np.abs(Eh - E).max() < 1e-9, np.abs(Eh - E).max()
print('gap at K', E[100, 1] - E[100, 0], 'bands at K', E[100], 'chern of the lower band', res['chern'])

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
    return vs                                       # the corners in the order of the arrows
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
drawnA = arrows_triangle(cornersA, style.ACCENT, True)
drawnB = arrows_triangle(cornersB, style.BROKEN, False)
# the arrows go counterclockwise on A and clockwise on B: the signed area of the corners in the order of the arrows. With the phase
# +pi/2 along the arrows, a counterclockwise hop has +pi/2 on both sublattices, which is D > 0 in the fold of Section 6.16
area = lambda v: 0.5 * sum(v[i][0] * v[(i + 1) % 3][1] - v[(i + 1) % 3][0] * v[i][1] for i in range(3))
assert area(drawnA) > 0 and area(drawnB) < 0, (area(drawnA), area(drawnB))
style.label(ax, 0.0, -1.35, r'phase $+\pi/2$ on $A$, $-\pi/2$ on $B$', fontsize=8, color=style.INK)
style.label(ax, 0.0, 2.35, r'(a) second-neighbor hopping, $t_2=DS$', fontsize=8.5)
ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.6, 2.6)

ax = axs[1]
x = np.arange(len(E))
ax.plot(x, E0[:, 0], color=style.MUTED, lw=0.9, ls=(0, (3, 2))); ax.plot(x, E0[:, 1], color=style.MUTED, lw=0.9, ls=(0, (3, 2)))
ax.plot(x, E[:, 0], color=style.ACCENT); ax.plot(x, E[:, 1], color=style.ACCENT)
for tk in ticks[1:3]:
    style.guide(ax, x=tk, color=style.GRID)
style.arrows(ax, xlabel='', ylabel=r'$E/|J|S$', ticks=True)
ax.set_xticks(ticks); ax.set_xticklabels([r'$\Gamma$', r'$K$', r'$M$', r'$\Gamma$'], fontsize=8.5)
ax.set_yticks([0, 2.48, 3.52, 6]); ax.set_yticklabels(['0', '2.48', '3.52', '6'], fontsize=8)
ax.tick_params(length=2.5, width=0.6, pad=2)
ax.annotate('', xy=(ticks[1] + 6, E[100, 1]), xytext=(ticks[1] + 6, E[100, 0]),
            arrowprops=dict(arrowstyle='<->', color=style.BROKEN, lw=0.9, shrinkA=0, shrinkB=0))
style.label(ax, ticks[1] + 14, 3.0, r'gap', color=style.BROKEN, fontsize=8.5, ha='left')
style.label(ax, 185, 7.0, '(b) bands, grey $DS=0$', fontsize=8.5)
ax.set_xlim(0, len(E) - 1); ax.set_ylim(-0.15, 6.5)
style.save(fig, __file__)
