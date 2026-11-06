"""Session 1, the four Fock states of the two-site problem, with the energies of H = t (c0^+ c1 + h.c.)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
from matplotlib.patches import Circle
import style

t = 1.0
# exact diagonalization in the Fock space with the fermionic signs, basis |n0 n1>
I2, Z, a = np.eye(2), np.diag([1., -1.]), np.array([[0., 1.], [0., 0.]])   # a destroys an electron
c0 = np.kron(a, I2)
c1 = np.kron(Z, a)
assert np.allclose(c0 @ c1 + c1 @ c0, 0)
assert np.allclose(c1 @ c1.T + c1.T @ c1, np.eye(4))
H = t * (c0.T @ c1 + c1.T @ c0)
N = c0.T @ c0 + c1.T @ c1
E, V = np.linalg.eigh(H)
levels = {}
for e, v in zip(E, V.T):
    levels.setdefault(int(round(v @ N @ v)), []).append(round(float(e), 6))
assert levels[0] == [0.0] and levels[1] == [-1.0, 1.0] and levels[2] == [0.0]

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(style.WIDTH_CM * style.CM, 5.8 * style.CM))
ax.axis('off')


def sites(x, y, kind, signs=None):
    """Two discs for the two sites. kind 0 empty, 1 shared by one electron, 2 both occupied."""
    for j in range(2):
        xc = x + (j - 0.5) * 0.45
        fc = {0: 'white', 1: style.LIGHT, 2: style.ACCENT}[kind]
        ax.scatter([xc], [y], s=110, facecolor=fc, edgecolor=style.ACCENT, linewidths=1.0, zorder=3)
        if signs:
            style.label(ax, xc, y - 0.01, signs[j], color='white', fontsize=8, zorder=4)


cols = {0: 0.0, 1: 3.4, 2: 6.8}
for n, x0 in cols.items():
    style.label(ax, x0, 2.75, 'N = %d' % n, fontsize=9.5)
    for e in levels[n]:
        ax.plot([x0 - 0.9, x0 + 0.9], [e, e], color=style.ACCENT, lw=1.8)
        style.label(ax, x0 + 1.05, e, {-1.0: r'$-t$', 0.0: r'$0$', 1.0: r'$+t$'}[e], ha='left', fontsize=9)
sites(0.0, 0.45, 0);              style.label(ax, 0.0, 0.85, r'$|0\rangle$', fontsize=8.5)
sites(3.4, 1.45, 1, ['+', '+']);  style.label(ax, 3.4, 1.85, r'$(c_0^\dagger+c_1^\dagger)|0\rangle$', fontsize=8)
sites(3.4, -0.55, 1, ['+', '$-$']); style.label(ax, 3.4, -0.15, r'$(c_0^\dagger-c_1^\dagger)|0\rangle$', fontsize=8)
sites(6.8, 0.45, 2);              style.label(ax, 6.8, 0.85, r'$c_0^\dagger c_1^\dagger|0\rangle$', fontsize=8.5)
style.label(ax, 6.8, -0.6, r'$E=(-t)+(+t)=0$', color=style.BROKEN, fontsize=8.5)
ax.set_xlim(-1.3, 8.3)
ax.set_ylim(-1.5, 3.1)
style.save(fig, __file__)
