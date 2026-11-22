"""Session 4, Section 4.5, the continuum quantum Hall ribbon with hard walls, shared by ribbon_three.py and the picture
options g2_quiz_qhribbon_*.py of the quiz on the Hall conductance.

In the Landau gauge each k_y gives the oscillator H = p^2/2 + (x - x0)^2/2 + V(x), in units of hbar omega_c and of
l_B, with the guiding center x0 = k_y l_B^2, on 0 < x < W with the wavefunction zero at the two walls. So k_y l_B = 0
puts the guiding center on the left wall and k_y l_B = W on the right wall. The levels come from finite differences on
1500 points. Far from the walls they are the flat Landau levels n + 1/2, and each wall bends them up. The potential V is
zero for the figures, and the check script of the page uses a step of V for its problem. A branch at the right wall
rises with k_y, so it has v_y > 0, and a branch at the left wall has v_y < 0, as the labels of ribbon_three.py say.
This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from scipy.linalg import eigh_tridiagonal
import style

W = 12.0                                   # the width of the ribbon in units of l_B


def levels(ks, width=W, npts=1500, nlev=6, V=None):
    """The nlev lowest levels at each k_y l_B of ks, in units of hbar omega_c. V is a function of x or None."""
    x = np.linspace(0, width, npts + 2)[1:-1]
    h = x[1] - x[0]
    pot = np.zeros_like(x) if V is None else V(x)
    off = -0.5 / h ** 2 * np.ones(npts - 1)
    return np.array([eigh_tridiagonal(1 / h ** 2 + 0.5 * (x - k) ** 2 + pot, off, select='i',
                                      select_range=(0, nlev - 1))[0] for k in ks])


def crossings(ks, E, mu):
    """The momenta where a branch crosses the energy mu, as a list of (k, n), found by linear interpolation."""
    out = []
    for n in range(E.shape[1]):
        e = E[:, n]
        for j in np.where(np.diff(np.sign(e - mu)) != 0)[0]:
            out.append((ks[j] + (mu - e[j]) / (e[j + 1] - e[j]) * (ks[j + 1] - ks[j]), n))
    return out


def edge_counts(ks, E, mu, width=W):
    """The number of crossings at the left half and at the right half of the ribbon, which are the chiral modes of the
    left and of the right edge when mu is in a gap."""
    c = crossings(ks, E, mu)
    return sum(1 for k, n in c if k < width / 2), sum(1 for k, n in c if k >= width / 2)


def check_bulk(ks, E, nflat=4):
    """The levels at the middle of the ribbon are the Landau levels n + 1/2."""
    mid = np.argmin(np.abs(ks - W / 2))
    assert abs(ks[mid] - W / 2) < 0.05
    assert np.allclose(E[mid, :nflat], np.arange(nflat) + 0.5, atol=1e-3), E[mid, :nflat]
    # the branch at the right wall rises with k_y and the one at the left wall falls
    assert E[-1, 0] > E[mid, 0] + 1 and E[0, 0] > E[mid, 0] + 1
    right = ks > W - 1
    assert np.all(np.diff(E[right, 0]) > 0) and np.all(np.diff(E[ks < 1, 0]) < 0)
    return E[mid, :nflat]


def draw(ax, ks, E, mu, lw=1.8, circles=False):
    """The branches, blue on the left half and red on the right half, and the chemical potential as a dashed line."""
    left = ks < W / 2
    for n in range(E.shape[1]):
        ax.plot(ks[left], E[left, n], color=style.ACCENT, lw=lw)
        ax.plot(ks[~left], E[~left, n], color=style.BROKEN, lw=lw)
    ax.axhline(mu, color=style.INK, lw=0.8, ls=(0, (4, 2.5)), zorder=0)
    if circles:
        for k, n in crossings(ks, E, mu):
            ax.plot([k], [mu], 'o', ms=4.5, mfc='white', mec=style.INK, mew=0.9, zorder=5)


def option(script, mu, expect):
    """One picture option of the quiz, the ribbon with the chemical potential mu in units of hbar omega_c, with its axes
    and no other text. expect is the number of crossings at each edge, checked here."""
    ks = np.linspace(-3.0, W + 3.0, 400)
    E = levels(ks, nlev=5)
    check_bulk(ks, E)
    nl, nr = edge_counts(ks, E, mu)
    lev = E[np.argmin(np.abs(ks - W / 2))]
    filled = int(np.sum(lev < mu))
    print(os.path.basename(script), 'mu', mu, 'crossings left and right', nl, nr, 'filled levels', filled)
    assert nl == nr == filled == expect, (nl, nr, filled)
    fig, ax = style.plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    draw(ax, ks, E, mu, lw=1.4)
    ax.set_xlim(ks[0], ks[-1]); ax.set_ylim(0, 4.2)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xticks([0, W]); ax.set_xticklabels(['0', '12'], fontsize=11)
    ax.set_yticks([0.5, 1.5, 2.5, 3.5]); ax.set_yticklabels(['0.5', '', '2.5', ''], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$k_y\ell_B$', fontsize=12, labelpad=-2)
    ax.set_ylabel(r'$E/\hbar\omega_c$', fontsize=12, labelpad=0)
    style.save(fig, script)
