"""Session 5, four Majoranas make two fermion modes and a fourfold degenerate level, two states of each parity."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import style

# the checks of what the figure says, on the four-dimensional Fock space of two modes
I2, Z, X = np.eye(2), np.diag([1.0, -1.0]), np.array([[0, 1.0], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
g = [np.kron(X, I2), np.kron(Y, I2), np.kron(Z, X), np.kron(Z, Y)]         # four Majorana operators
for i in range(4):
    for j in range(4):
        assert np.allclose(g[i] @ g[j] + g[j] @ g[i], 2 * np.eye(4) * (i == j))
c1, c2 = 0.5 * (g[0] + 1j * g[1]), 0.5 * (g[2] + 1j * g[3])
n1, n2 = c1.conj().T @ c1, c2.conj().T @ c2
U12 = np.eye(4) * np.cos(np.pi / 4) + g[0] @ g[1] * np.sin(np.pi / 4)      # exp(pi/4 g1 g2), as in (5.23)
P = (np.eye(4) - 2 * n1) @ (np.eye(4) - 2 * n2)                            # total fermion parity
assert np.allclose(U12 @ P, P @ U12)                                       # a braid keeps the parity
assert sorted(np.round(np.diag(P).real)) == [-1, -1, 1, 1]            # two even and two odd states

fig, ax = plt.subplots(figsize=(style.WIDTH_CM * style.CM, 5.2 * style.CM))
ax.axis('off'); ax.set_aspect('equal')
# left, four Majoranas and the two modes they form
xs = [0.0, 1.2, 2.8, 4.0]
for k, x in enumerate(xs):
    ax.add_patch(Circle((x, 0), 0.22, fc=style.ACCENT if k % 2 == 0 else style.BROKEN, ec=style.INK, lw=0.7, zorder=3))
    style.label(ax, x, -0.6, rf'$\gamma_{k+1}$', fontsize=8.5)
for (a, b), name in [((0, 1), r'$c_1$'), ((2, 3), r'$c_2$')]:
    r = 0.4
    ax.add_patch(FancyBboxPatch((xs[a] - r, -r), xs[b] - xs[a] + 2 * r, 2 * r, boxstyle=f'round,pad=0,rounding_size={r}',
                                fc='none', ec=style.MUTED, lw=1.0, ls=(0, (4, 2))))
    style.label(ax, 0.5 * (xs[a] + xs[b]), 0.95, name, fontsize=9)
style.label(ax, 2.0, 1.75, 'four Majoranas, two modes', fontsize=8.5)
# right, the four states at one energy
ax.annotate('', xy=(5.5, 1.5), xytext=(5.5, -0.2), arrowprops=dict(arrowstyle='-|>', color=style.INK, lw=0.7, mutation_scale=7))
style.label(ax, 5.5, 1.75, r'$E$', fontsize=9)
y0 = 0.0
states = [('00', style.ACCENT), ('11', style.ACCENT), ('01', style.BROKEN), ('10', style.BROKEN)]
for j, (s, col) in enumerate(states):
    x = 6.6 + 0.85 * j
    ax.plot([x - 0.35, x + 0.35], [y0, y0], color=col, lw=2.2, solid_capstyle='round')
    style.label(ax, x, y0 - 0.45, rf'$|{s}\rangle$', fontsize=8.5)
style.label(ax, 7.45, 0.55, r'$E=0$, four states', fontsize=8.5)
style.label(ax, 6.6 + 0.425, -1.2, 'even parity', color=style.ACCENT, fontsize=8.5)
style.label(ax, 6.6 + 0.85 * 2.5, -1.2, 'odd parity', color=style.BROKEN, fontsize=8.5)
ax.set_xlim(-0.8, 10.2); ax.set_ylim(-1.6, 2.1)
style.save(fig, __file__)
