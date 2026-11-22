"""Shared code of the figures of Section 9.2: the mean-field Ising magnet of the steps of the page, used by
curie_weiss.py and curie_quiz.py, and the picture options of the quiz that asks which sample orders as a ferromagnet,
g1_quiz_curie_*.py. This file writes no figure.

The model is the one of the steps fold of Section 9.2 and of webnotes/conventions/session09.md. Ising spins s = +-1
with E = -J sum_<ij> s_i s_j - h sum_i s_i, J > 0 for a ferromagnet, z neighbors, all on the other sublattice of a
bipartite lattice, k_B = 1, and the field and the temperature in the same unit, so that a free spin has chi = 1/T.
Mean field gives m_A = tanh((h_A + zJ m_B)/T) and m_B = tanh((h_B + zJ m_A)/T). The function loop solves these two
equations by iteration in a small field, which is the self-consistent route, and the asserts compare it with the
closed form 1/chi = T - zJ of the steps, which is the second route. This is numpy, since pyqula has a Monte Carlo of
the Ising model and no mean field of it."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style


def loop(T, zJ, staggered=False, h=1e-7, ite=3000):
    """The inverse susceptibility 1/chi of the two-sublattice mean field at the temperature T, uniform or staggered.
    Above the order the iteration contracts by |zJ|/T per step, so 3000 steps converge for T > 1.01 |zJ|."""
    hA, hB = h, (-h if staggered else h)
    mA = mB = 0.0
    for i in range(ite):
        mA, mB = math.tanh((hA + zJ * mB) / T), math.tanh((hB + zJ * mA) / T)
    m = (mA - mB) / 2 if staggered else (mA + mB) / 2
    return h / m


def check_fold():
    """The three lines of (9.1) and the staggered response of the steps, with zJ = T_c = 1 or -1."""
    for T in (1.25, 1.5, 2.0, 2.5, 3.0):
        para, ferro, anti = loop(T, 0.0), loop(T, 1.0), loop(T, -1.0)
        assert abs(para - T) < 1e-5 and abs(ferro - (T - 1)) < 1e-5 and abs(anti - (T + 1)) < 1e-5, T
        assert abs(loop(T, -1.0, staggered=True) - (T - 1)) < 1e-5, T      # the antiferromagnet orders at T_c
    # the numbers of the sheet and of the quiz with equations as options, at 1.5 T_c and 3 T_c
    assert [round(loop(1.5, s), 3) for s in (1.0, -1.0)] == [0.5, 2.5]
    assert [round(loop(3.0, s), 3) for s in (0.0, 1.0, -1.0)] == [3.0, 2.0, 4.0]


# the picture options of the quiz: three samples with the intercepts theta = +30, 0 and -30 K
TMEAS, TMAX = 50.0, 120.0


def option(script, theta):
    """One picture option, the measured line 1/chi = T - theta from TMEAS to TMAX and its extrapolation to zero."""
    check_fold()
    Ts = np.array([60.0, 90.0, TMAX])
    inv = np.array([loop(T, theta) for T in Ts])                    # the self-consistent loop with zJ = theta
    slope, icpt = np.polyfit(Ts, inv, 1)
    assert abs(slope - 1) < 1e-6 and abs(-icpt / slope - theta) < 1e-4, (slope, icpt)
    print(os.path.basename(script), 'intercept of the line %.4f K, 1/chi at 60, 90, 120 K' % (-icpt / slope),
          np.round(inv, 4))
    fig, ax = style.plt.subplots(figsize=(4.2 * style.CM, 3.8 * style.CM))
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    T = np.linspace(TMEAS, TMAX, 50)
    ax.plot(T, T - theta, color=style.ACCENT, lw=1.6)
    T = np.linspace(theta, TMEAS, 50)
    ax.plot(T, T - theta, color=style.ACCENT, lw=1.2, ls=(0, (3, 2)))
    ax.plot([theta], [0], 'o', color=style.ACCENT, ms=3.5, clip_on=False, zorder=5)
    ax.axvline(0, color=style.GRID, lw=0.8, zorder=0)
    ax.set_xlim(-45, 125); ax.set_ylim(0, 160)
    ax.set_xticks([-30, 0, 30]); ax.set_xticklabels([r'$-30$', r'$0$', r'$30$'], fontsize=10)
    ax.set_yticks([0, 100]); ax.set_yticklabels([r'$0$', r'$100$'], fontsize=10)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$T$ (K)', fontsize=11, labelpad=0); ax.set_ylabel(r'$1/\chi$ (K)', fontsize=11, labelpad=4)
    style.save(fig, script)
