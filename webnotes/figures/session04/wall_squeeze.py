"""Session 4, section 4.11, why a Landau level bends up near a wall.

The oscillator H = p^2/2 + (x - x0)^2/2 of one k_y, in units of hbar omega_c and l_B, on x>0 with a hard wall at x=0, and
the lowest level found by finite differences on 3000 points. For x0 = 3 the wall does not touch the state and E = 1/2.
For x0 = 1 the state is pushed against the wall. For x0 = 0 the wall cuts the well in two and the lowest state is the
odd one, E = 3/2. The curve is |psi|^2 drawn on its level."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from scipy.linalg import eigh_tridiagonal
import style

L, N = 9.0, 3000
x = np.linspace(0, L, N + 2)[1:-1]
h = x[1] - x[0]


def ground(x0):
    w, v = eigh_tridiagonal(1 / h ** 2 + 0.5 * (x - x0) ** 2, -0.5 / h ** 2 * np.ones(N - 1), select='i', select_range=(0, 0))
    psi = v[:, 0] / np.sqrt(h)
    return w[0], psi


cases = [(3.0, 'far from the wall'), (1.0, 'close to the wall'), (0.0, 'at the wall')]
E = [ground(x0)[0] for x0, _ in cases]
print('E', E)
assert abs(E[0] - 0.5) < 1e-3 and abs(E[2] - 1.5) < 1e-3

fig, axs = style.figure(ncols=3, width_cm=11.5, height_cm=4.4, sharey=True, gridspec_kw=dict(wspace=0.12))
for ax, (x0, title), e in zip(axs, cases, E):
    xx = np.linspace(-1.2, 6.2, 400)
    ax.set_xlim(-1.2, 6.2); ax.set_ylim(0, 3.1)
    ax.plot(xx, 0.5 * (xx - x0) ** 2, color=style.GRID, lw=1.2)
    xs = np.linspace(0, 6.2, 400)
    _, psi = ground(x0)
    p = np.interp(xs, x, psi ** 2)
    ax.axhline(e, xmin=0.0, color=style.MUTED, lw=0.6, ls=':', zorder=0)
    ax.fill_between(xs, e, e + 0.85 * p / 1.0, color=style.ACCENT, alpha=0.25, lw=0)
    ax.plot(xs, e + 0.85 * p, color=style.ACCENT, lw=1.4)
    ax.axvspan(-1.2, 0, color='#d0d0d0', lw=0)
    ax.axvline(0, color=style.INK, lw=1.2)
    ax.text(0.5, -0.07, title, transform=ax.transAxes, ha='center', va='top', fontsize=8, color=style.INK)
    ax.text(6.1, e + 0.35 + (0.35 if x0 == 3.0 else 0), r'$E=%.2f$' % e, fontsize=8, ha='right', va='bottom', color=style.ACCENT)
    ax.plot([x0], [0], 'v', color=style.BROKEN, ms=4, clip_on=False)
for ax in axs:
    ax.set_xticks([]); ax.set_yticks([])
style.arrows(axs[0], ylabel=r'$E/\hbar\omega_c$')
for ax in axs[1:]:
    style.arrows(ax)
    ax.spines['left'].set_visible(False)
    ax.set_yticks([])
style.label(axs[1], 2.5, -0.9, r'$x$, the red triangle is the center $x_0$ of the well', fontsize=8)
style.save(fig, __file__)
