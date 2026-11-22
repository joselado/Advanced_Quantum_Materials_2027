"""Session 1, the two lowest states of a double well, with the splitting that a finite barrier gives.

H = -d^2/dx^2 + V0 (x^2 - 1)^2 with hbar^2/2m = 1 and V0 = 8, on a grid of 1200 points from -2.2 to 2.2, by finite
differences. The minima are at x = +-1 and the barrier at x = 0 is V0 high. The upper panel draws the two wave
functions against x, the lower one the potential with the two levels. A continuum problem on a grid, not a lattice
model of the course, so it stays in numpy and has no script to download. The asserts check the numbers of the
caption in the quiz of Section 1.11a: the minima at x = +-1 and the barrier 8 high, the even and the odd state,
2 Delta = 0.92, and a higher barrier that makes Delta smaller. Each level is drawn between its outer turning points,
where V = E, so that it ends on the walls of the potential.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style


def levels(V0, n=1200):
    """Grid, eigenvalues and eigenvectors of -d^2/dx^2 + V0 (x^2-1)^2."""
    x = np.linspace(-2.2, 2.2, n); dx = x[1] - x[0]
    H = np.diag(2 / dx ** 2 + V0 * (x ** 2 - 1) ** 2) - (np.eye(n, k=1) + np.eye(n, k=-1)) / dx ** 2
    w, v = np.linalg.eigh(H)
    return x, dx, w, v


V0 = 8.0


def pot(x):
    return V0 * (x ** 2 - 1) ** 2


assert pot(1.0) == 0 and pot(-1.0) == 0                          # the minima are at x = +-1, with V = 0
assert pot(0.0) == 8                                            # and the barrier between them is 8 high
xs = np.linspace(-3, 3, 6001)
assert np.all(pot(xs) >= 0) and np.isclose(pot(xs[np.abs(xs) < 1]).max(), 8)   # 8 is the top of the barrier
x, dx, w, v = levels(V0)
V = pot(x)
psi0, psi1 = v[:, 0] / np.sqrt(dx), v[:, 1] / np.sqrt(dx)
if psi0.sum() < 0: psi0 = -psi0
if psi1[x > 0].sum() < 0: psi1 = -psi1
assert np.allclose(psi0, psi0[::-1], atol=1e-3) and np.allclose(psi1, -psi1[::-1], atol=1e-3)   # even and odd
assert np.all(psi0 > -1e-9)                                     # the ground state has weight in both wells, no node
split = w[1] - w[0]
assert '%.2f' % split == '0.92' and abs(split - 0.925) < 1e-3   # 2 Delta = 0.92 of the caption
assert abs(levels(V0, 2400)[2][1] - levels(V0, 2400)[2][0] - split) < 1e-4   # converged on the grid
assert w[1] < V0 and w[2] > V0                                  # both levels are below the top of the barrier
w10 = levels(10.0)[2]
assert w10[1] - w10[0] < split                                  # a higher barrier makes Delta smaller
turn = [np.sqrt(1 + np.sqrt(e / V0)) for e in w[:2]]            # the outer turning points, where V = E
assert all(np.isclose(pot(xt), e) and np.isclose(pot(-xt), e) for xt, e in zip(turn, w[:2]))
assert all(1.3 < xt < 1.4 for xt in turn)                       # each level line ends on the walls of V

FS = 10
fig, axs = plt.subplots(2, 1, figsize=(9.0 * style.CM, 7.6 * style.CM),
                        gridspec_kw=dict(height_ratios=[1, 1.3], hspace=0.18), sharex=True)
for a in axs:
    for s in ('top', 'right'):
        a.spines[s].set_visible(False)
    a.spines['left'].set_color(style.INK); a.spines['bottom'].set_color(style.INK)
    a.tick_params(labelsize=FS, length=2.5, width=0.6, pad=2)
a = axs[0]
a.axhline(0, color=style.GRID, lw=0.8, zorder=0)
a.plot(x, psi0, color=style.ACCENT)
a.plot(x, psi1, color=style.BROKEN)
a.set_ylim(-0.95, 1.05); a.set_yticks([0])
a.set_ylabel(r'$\psi(x)$', fontsize=FS + 1, labelpad=2)
a.tick_params(bottom=False)
style.label(a, -2.15, 0.9, r'$\psi_+$, even', color=style.ACCENT, ha='left', fontsize=FS)
imin = np.argmin(psi1)
assert x[imin] < 0 and abs(x[imin] + 1) < 0.15                  # the negative lobe of psi_- is in the left well
style.label(a, -0.3, 0.8 * psi1[imin], r'$\psi_-$, odd', color=style.BROKEN, ha='left', fontsize=FS)
b = axs[1]
b.plot(x, V, color=style.MUTED, lw=1.4)
b.plot([-turn[0], turn[0]], [w[0]] * 2, color=style.ACCENT, lw=1.4)
b.plot([-turn[1], turn[1]], [w[1]] * 2, color=style.BROKEN, lw=1.4)
b.set_xlim(-2.2, 2.2); b.set_ylim(0, 10.5)
b.set_xticks([-2, -1, 0, 1, 2]); b.set_xticklabels(['$-2$', '$-1$', '0', '1', '2'])
b.set_yticks([0, 4, 8])
b.set_xlabel(r'$x$', fontsize=FS + 1, labelpad=1)
b.set_ylabel(r'$E$', fontsize=FS + 1, labelpad=6, rotation=0, va='center')
XB = 0.85                                                       # the splitting is marked inside the right well
assert np.sqrt(1 - np.sqrt(7.6 / V0)) < XB - 0.45 and XB + 0.45 < np.sqrt(1 + np.sqrt(6.4 / V0))   # label clear of V
b.annotate('', xy=(XB, w[1]), xytext=(XB, w[0]),
           arrowprops=dict(arrowstyle='|-|, widthA=0.2, widthB=0.2', color=style.INK, lw=0.8, shrinkA=0, shrinkB=0))
style.label(b, XB, w[1] + 1.4, r'$2\Delta=%.2f$' % split, fontsize=FS - 1)
style.label(b, 0, 9.3, r'$V(x)$', color=style.MUTED, fontsize=FS)
print('levels', w[:2], 'split', split)
style.save(fig, __file__)
