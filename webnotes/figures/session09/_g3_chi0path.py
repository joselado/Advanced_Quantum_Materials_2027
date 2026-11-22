"""Session 9, Section 9.5b, the static Lindhard function (9.4) of the square lattice along Gamma-X-M-Gamma.

Shared by the figure stoner.py, the three picture options g3_quiz_chi0_*.py of the quiz on (9.8), and the check
script webnotes/checks/session09/g3_05b_stoner_instability.py, so that the figures and the asserts use the same
arrays. The band is eps(k) = -2t(cos kx + cos ky) - mu with t = 1, spinless, so chi_0 is per spin and per site and
positive, as on the sheet webnotes/conventions/session09.md. A pair with equal energies gives -n_F', its limit.
The second route for the half-filled lattice is the elliptic density of states, as in the check of the sheet.
Nothing here writes a file when it is imported; option() draws one picture and saves it next to its script."""
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from scipy.integrate import quad
from scipy.special import ellipk

T_FIG, NK_FIG = 0.1, 240            # the temperature and the k-mesh of the figure stoner and of the quiz pictures
MU_QUIZ = {'half': 0.0, 'incomm': -1.0, 'low': -3.0}     # the three fillings of the picture quiz


def fermi(e, T):
    return 0.5 * (1 - np.tanh(np.asarray(e) / (2 * T)))


def path(mu, T=T_FIG, nk=NK_FIG, step=8):
    """chi_0(q,0) of (9.4) on the q of the mesh along Gamma-X-M-Gamma, with q = 2 pi (ix, iy)/nk.

    Returns the points (ix, iy), the values and the positions of Gamma, X, M and Gamma in the list."""
    k = 2 * np.pi * np.arange(nk) / nk
    KX, KY = np.meshgrid(k, k, indexing='ij')
    e1 = -2 * (np.cos(KX) + np.cos(KY)) - mu
    f1 = fermi(e1, T)

    def chi0(ix, iy):
        e2 = np.roll(np.roll(e1, -ix, 0), -iy, 1)
        f2 = np.roll(np.roll(f1, -ix, 0), -iy, 1)
        d = e2 - e1
        small = np.abs(d) < 1e-9
        return float(np.mean(np.where(small, f1 * (1 - f1) / T, (f1 - f2) / np.where(small, 1.0, d))))

    h = nk // 2
    pts = [(i, 0) for i in range(0, h + 1, step)] + [(h, i) for i in range(step, h + 1, step)] \
        + [(h - i, h - i) for i in range(step, h + 1, step)]
    nseg = len(range(0, h + 1, step))
    ticks = [0, nseg - 1, 2 * (nseg - 1), 3 * (nseg - 1)]
    return pts, np.array([chi0(*p) for p in pts]), ticks


def elliptic(T):
    """chi_0 at q=0 and at (pi,pi) of the half-filled lattice from the density of states per spin, a second route."""
    dos = lambda E: ellipk(1 - E ** 2 / 16) / (2 * np.pi ** 2)
    g = 2 * quad(lambda E: dos(E) / (4 * T * np.cosh(E / (2 * T)) ** 2), 0, 4, points=[T, 10 * T], limit=400)[0]
    m = 2 * quad(lambda E: dos(E) * np.tanh(E / (2 * T)) / (2 * E), 0, 4, points=[T, 10 * T], limit=400)[0]
    return g, m


def option(script, which):
    """One picture option of the quiz, the same axes and the same scale for the three."""
    import matplotlib.pyplot as plt
    import style
    pts, y, xt = path(MU_QUIZ[which], step=4)
    x = np.arange(len(y))
    assert y.max() < 0.75 and y.min() > 0
    fig, ax = plt.subplots(figsize=(4.2 * style.CM, 3.9 * style.CM))
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for xx in xt[1:3]:
        ax.axvline(xx, color=style.GRID, lw=0.7, zorder=0)
    ax.plot(x, y, color=style.ACCENT, lw=1.6)
    ax.set_xlim(0, x[-1]); ax.set_ylim(0, 0.75)
    ax.set_xticks(xt); ax.set_xticklabels([r'$\Gamma$', r'$X$', r'$M$', r'$\Gamma$'], fontsize=11)
    ax.set_yticks([0, 0.3, 0.6]); ax.set_yticklabels(['0', '0.3', '0.6'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$q$', fontsize=12, labelpad=0)
    ax.set_ylabel(r'$\chi_0$', fontsize=12, labelpad=1)
    style.save(fig, script)
