"""Session 4, section 4.11, why a Landau level bends up near a wall.

The oscillator H = p^2/2 + (x - x0)^2/2 of one k_y, in units of hbar omega_c and l_B, on x>0 with a hard wall at x=0, and
the lowest level found by finite differences on 3000 points. For x0 = 3 the wall does not touch the state and E = 1/2.
For x0 = 1 the state is pushed against the wall and E = 0.734. For x0 = 0 the wall cuts the well in two and the lowest
state is the odd one, E = 3/2. The curve is |psi|^2 drawn on its level. Redrawn on 2026-11-21 under the same name, with
the axes x/l_B and E/hbar omega_c and their ticks. The second route to the three energies, the zero of the parabolic
cylinder function, is on the conventions sheet of the session."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from scipy.linalg import eigh_tridiagonal
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # the figure sits in a quiz, at most 360 px wide

L, N = 9.0, 3000
x = np.linspace(0, L, N + 2)[1:-1]
h = x[1] - x[0]


def ground(x0):
    w, v = eigh_tridiagonal(1 / h ** 2 + 0.5 * (x - x0) ** 2, -0.5 / h ** 2 * np.ones(N - 1), select='i', select_range=(0, 0))
    psi = v[:, 0] / np.sqrt(h)
    return w[0], psi


cases = [(3.0, r'$x_0=3\,\ell_B$'), (1.0, r'$x_0=\ell_B$'), (0.0, r'$x_0=0$')]
E = [ground(x0)[0] for x0, _ in cases]
print('E', E)
assert abs(E[0] - 0.5) < 1e-3 and abs(E[1] - 0.734) < 1e-3 and abs(E[2] - 1.5) < 1e-3
assert [round(e, 2) for e in E] == [0.5, 0.73, 1.5]            # the 0.50, 0.73 and 1.50 of the caption

fig, axs = plt.subplots(1, 3, figsize=(10.5 * style.CM, 4.6 * style.CM), sharey=True, gridspec_kw=dict(wspace=0.15))
for ax, (x0, title), e in zip(axs, cases, E):
    xx = np.linspace(-1.2, 6.2, 400)
    ax.set_xlim(-1.2, 6.2); ax.set_ylim(0, 3.1)
    ax.plot(xx, 0.5 * (xx - x0) ** 2, color=style.GRID, lw=1.2)
    xs = np.linspace(0, 6.2, 400)
    _, psi = ground(x0)
    p = np.interp(xs, x, psi ** 2)
    ax.axhline(e, color=style.MUTED, lw=0.6, ls=':', zorder=0)
    ax.fill_between(xs, e, e + 0.85 * p, color=style.ACCENT, alpha=0.25, lw=0)
    ax.plot(xs, e + 0.85 * p, color=style.ACCENT, lw=1.4)
    ax.axvspan(-1.2, 0, color='#d0d0d0', lw=0)
    ax.axvline(0, color=style.INK, lw=1.2)
    ax.text(0.55, 1.0, title, transform=ax.transAxes, ha='center', va='bottom', fontsize=10, color=style.INK)
    ax.text(6.1, e + 0.35 + (0.35 if x0 == 3.0 else 0), r'$%.2f$' % e, fontsize=10, ha='right', va='bottom',
            color=style.ACCENT)
    ax.plot([x0], [0], 'v', color=style.BROKEN, ms=5, clip_on=False, zorder=5)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xticks([0, 2, 4]); ax.set_xticklabels(['0', '2', '4'])
    ax.tick_params(length=2.5, width=0.6, labelsize=10, pad=2)
    ax.set_xlabel(r'$x/\ell_B$', fontsize=11, labelpad=1)
axs[0].set_yticks([0.5, 1.5]); axs[0].set_yticklabels(['0.5', '1.5'])
axs[0].set_ylabel(r'$E/\hbar\omega_c$', fontsize=11, labelpad=2)
for ax in axs[1:]:
    ax.tick_params(axis='y', length=0)
style.save(fig, __file__)
