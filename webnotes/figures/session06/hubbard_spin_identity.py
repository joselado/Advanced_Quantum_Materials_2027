"""Session 6, the Hubbard term of one site written with the local spin, U n_up n_down = U n/2 - (2U/3) S^2.

The two modes of one site are built as Jordan-Wigner matrices, the identity is checked as an operator identity,
and its two terms are drawn on the four states of the site. The term U n/2 (grey) counts electrons, the term
-(2U/3) S^2 (blue) is nonzero only on a singly occupied site, where S^2 = 3/4, and their sum (red dots) is the
Hubbard energy, which is U only on the doubly occupied site.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

Z, a, I2 = np.diag([1., -1.]), np.array([[0., 1.], [0., 0.]]), np.eye(2)
cu, cd = np.kron(a, I2), np.kron(Z, a)
nu, nd = cu.T @ cu, cd.T @ cd
n = nu + nd
Sx = 0.5 * (cu.T @ cd + cd.T @ cu)
Sy = 0.5 * (-1j * cu.T @ cd + 1j * cd.T @ cu)
Sz = 0.5 * (nu - nd)
S2 = (Sx @ Sx + Sy @ Sy + Sz @ Sz).real
assert np.allclose(nu @ nd, n / 2 - (2 / 3) * S2)          # the identity, in units of U
assert np.allclose(S2, 0.75 * (n - 2 * nu @ nd))           # only a singly occupied site has a spin

# the four basis states of the two modes (up, down), occupation 0 or 1, in the order empty, up, down, both
occ = {(0, 0): 'empty', (1, 0): r'$\uparrow$', (0, 1): r'$\downarrow$', (1, 1): r'$\uparrow\downarrow$'}
idx = lambda o: 2 * o[0] + o[1]                             # index in the kron basis, 1 = occupied, since a = |0><1|
states = [(0, 0), (1, 0), (0, 1), (1, 1)]
tn = [n[idx(o), idx(o)] / 2 for o in states]
ts = [-(2 / 3) * S2[idx(o), idx(o)] for o in states]
hub = [(nu @ nd)[idx(o), idx(o)] for o in states]
assert np.allclose(tn, [0, 0.5, 0.5, 1]) and np.allclose(ts, [0, -0.5, -0.5, 0]) and np.allclose(hub, [0, 0, 0, 1])

FS = 11.5
style.plt.rcParams['font.size'] = FS          # labels of the arrows too, for a phone
fig, ax = plt.subplots(figsize=(11.0 * style.CM, 5.6 * style.CM))
x = np.arange(4)
wb = 0.3
ax.bar(x - wb / 2, tn, width=wb, color=style.GRID, edgecolor=style.MUTED, lw=0.8)
ax.bar(x + wb / 2, ts, width=wb, color=style.LIGHT, edgecolor=style.ACCENT, lw=0.8)
ax.plot(x, hub, 'o', color=style.BROKEN, ms=7, zorder=5)
ax.axhline(0, color=style.INK, lw=0.7)
ax.axis('off')
ax.annotate('', xy=(-0.6, 1.45), xytext=(-0.6, -0.65), arrowprops=dict(arrowstyle='-|>', color=style.INK, lw=0.7,
            mutation_scale=7, shrinkA=0, shrinkB=0))
style.label(ax, -0.6, 1.5, r'energy$/U$', fontsize=FS, va='bottom')
for xi, o in zip(x, states):
    style.label(ax, xi, -0.83, occ[o], fontsize=FS + 1 if o != (0, 0) else FS)
for y, lab in ((1, '$1$'), (0.5, r'$\frac{1}{2}$'), (-0.5, r'$-\frac{1}{2}$')):
    ax.text(-0.62, y, lab, ha='right', va='center', fontsize=FS - 0.5)
    style.guide(ax, y=y)
style.label(ax, 1.38, 1.13, r'$U n/2$', color=style.MUTED, fontsize=FS, ha='right')
style.label(ax, 1.72, 1.13, r'$-\frac{2U}{3}\mathbf{S}^2$', color=style.ACCENT, fontsize=FS, ha='left')
style.label(ax, 3.0, 1.32, r'$U n_\uparrow n_\downarrow$', color=style.BROKEN, fontsize=FS)
ax.set_xlim(-0.6, 3.6); ax.set_ylim(-1.0, 1.6)
style.save(fig, __file__)
