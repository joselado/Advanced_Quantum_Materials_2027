"""Shared code of the band plots of the Kondo lattice of Sections 8.12 and 8.13, by the group g4 of the web notes.

The data come from the downloadable pyqula scripts webnotes/scripts/session08/g4_*.py. In those scripts H2HFH of
pyqula puts one f site with its level at zero next to every conduction site and mixes the two by the hopping JK, which
is the hybridization gamma_K of (8.21) and not the Kondo coupling J_K of (8.17), as webnotes/conventions/session08.md
says. pyqula puts +JK between c and f where (8.21) has -gamma_K, so JK = -gamma_K, a gauge f -> -f that leaves the bands
the same; the check script of Section 8.13 asserts it. Every spin gives one copy of the two bands, so the four sorted bands come in two degenerate pairs, and the plots
draw one band of each pair. The chain uses tij=[-1.], so its conduction band is -2t cos k with t=1 and its minimum at
k=0, the sign of the pages.

check_chain() asserts what the captions and the quiz say about the chain, colored() draws a band whose color is its
weight on the conduction electrons, and option() draws one picture of the quiz of Section 8.13, with the filled states
dark, the empty states light and the half-filled f level of the metal in the middle tone HALF, the Fermi level placed
by the count of the particles. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable
import style

CF = LinearSegmentedColormap.from_list('f_to_c', [style.BROKEN, style.ACCENT])     # weight 0 is f, weight 1 is c
LEVELS = 24
EMPTY = style.LIGHT                                                                    # the empty states of the quiz
# a half-filled level of the quiz, the middle between the filled color style.ACCENT and the empty color EMPTY
HALF = '#%02x%02x%02x' % tuple((int(style.ACCENT[i:i + 2], 16) + int(EMPTY[i:i + 2], 16)) // 2 for i in (1, 3, 5))


def bands_formula(eps, gamma):
    """E_- and E_+ of the 2x2 matrix [[eps, -gamma], [-gamma, 0]], the box of Section 8.13."""
    r = np.sqrt(eps ** 2 + 4 * gamma ** 2)
    return (eps - r) / 2, (eps + r) / 2


def check_chain(d):
    """The numbers of the chain script g4_kondo_chain_bands.py that the pages quote."""
    k = 2 * np.pi * np.array(d['kpath'])[:, 0]
    assert len(k) == 201 and abs(k[0] + np.pi) < 1e-12 and abs(k[-1] - np.pi) < 1e-12
    assert np.isclose(k[50], -np.pi / 2) and np.isclose(k[150], np.pi / 2)          # the crossings are on the path
    eps = -2 * np.cos(k)
    for gamma, e, w in zip(d['gammas'], d['energies'], d['weights']):
        assert e.shape == (201, 4) and w.shape == (201, 4)
        assert np.allclose(e[:, 0], e[:, 1], atol=1e-9) and np.allclose(e[:, 2], e[:, 3], atol=1e-9)   # two spins
        lo, up = bands_formula(eps, gamma)
        assert np.allclose(e[:, 1], lo, atol=1e-9) and np.allclose(e[:, 2], up, atol=1e-9)
        assert w.min() > -1e-9 and w.max() < 1 + 1e-9
        if gamma > 0:
            assert np.all(e[:, 1] < 0) and np.all(e[:, 2] > 0)                         # E_- < 0 < E_+ at every k
            assert np.allclose(w[[50, 150], 1], 0.5, atol=1e-9)                       # half c and half f at the crossing
            # the f weight of the filled lower band, per spin, is one half: one f fermion per site with the two spins
            assert abs(np.mean(1 - w[:-1, 1]) - 0.5) < 1e-9
    g0 = d['gammas'].index(0.)
    e0 = d['energies'][g0]
    c0 = e0[:, 0] + e0[:, 3]                                     # with no mixing the bands are the c band and f at zero
    assert np.allclose(c0, eps, atol=1e-12) and np.argmin(c0) == 100 and abs(c0[100] + 2) < 1e-12   # minimum -2 at k=0
    assert np.allclose(np.sort(np.c_[c0, c0, 0 * c0, 0 * c0], axis=1), e0, atol=1e-12)
    for gamma, dg, ig in zip(d['gammas'], d['direct'], d['indirect']):
        assert abs(dg - 2 * gamma) < 1e-9                                               # direct gap 2 gamma_K
        assert abs(ig - 2 * (np.sqrt(1 + gamma ** 2) - 1)) < 1e-9                      # indirect gap of the chain
    return k


def colored(ax, x, y, w, lw=1.7, cmap=CF):
    """A curve y(x) whose color is the weight w on the conduction electrons, as pieces of constant color."""
    x, y, w = map(np.asarray, (x, y, w))
    lev = np.clip(np.round(w * (LEVELS - 1)), 0, LEVELS - 1).astype(int)
    cut = np.where(np.diff(lev) != 0)[0] + 1
    segs, cols = [], []
    for a, b in zip(np.r_[0, cut], np.r_[cut, len(x) - 1]):
        segs.append(np.c_[x[a:b + 1], y[a:b + 1]])
        cols.append(cmap(lev[a] / (LEVELS - 1)))
    ax.add_collection(LineCollection(segs, colors=cols, linewidths=lw, capstyle='round', joinstyle='round'))


def colorbar(fig, ax, fontsize=10):
    """A colorbar of the weight on the conduction electrons, from 0 (an f fermion) to 1 (a conduction electron)."""
    sm = ScalarMappable(norm=Normalize(0, 1), cmap=CF)
    cb = fig.colorbar(sm, ax=ax, fraction=0.05, pad=0.04, aspect=14, ticks=[0, 0.5, 1])
    cb.ax.set_yticklabels(['0', '0.5', '1'], fontsize=fontsize)
    cb.set_label(r'weight on $c$', fontsize=fontsize, labelpad=2)
    cb.outline.set_linewidth(0.5)
    cb.ax.tick_params(length=2, width=0.5)
    return cb


def ticks(ax, xticks, yticks, fontsize):
    """Ticks with numbers at the given places, on the axes drawn by style.arrows."""
    ax.set_xticks([t for t, _ in xticks]); ax.set_xticklabels([l for _, l in xticks])
    ax.set_yticks([t for t, _ in yticks]); ax.set_yticklabels([l for _, l in yticks])
    ax.tick_params(length=2.5, width=0.6, pad=2, labelsize=fontsize)


KTICKS = [(-np.pi, r'$-\pi$'), (0, r'$0$'), (np.pi, r'$\pi$')]
ETICKS = [(-2, r'$-2$'), (0, r'$0$'), (2, r'$2$')]


def fermi_level(e, gamma, count):
    """The Fermi level for count particles per momentum and spin. For one particle it is the middle between the sorted
    levels number n-1 and n of one spin, the bands 0 and 2 of the four, on the momenta of the path without the copy of
    k = -pi at k = pi. For fewer particles the lower band is filled where |k| < count pi, since E_- grows with -2t cos k,
    so the Fermi level is E_-(-2 cos(count pi)) of the infinite chain, and the count of the levels of the path below it
    is checked against count to one momentum of the path."""
    levels = np.sort(np.r_[e[:-1, 0], e[:-1, 2]])
    if count == 1:
        n = len(e) - 1
        return 0.5 * (levels[n - 1] + levels[n])
    ef = bands_formula(-2 * np.cos(count * np.pi), gamma)[0]
    assert abs(np.mean(levels < ef) * 2 - count) <= 1.0 / (len(e) - 1) + 1e-12
    return ef


def option(script, gamma, count):
    """One picture of the quiz of Section 8.13: the bands of the chain for the hybridization gamma, filled up to the Fermi
    level of count particles per momentum and spin, with the axes and no other text."""
    d = style.run_script('session08/g4_kondo_chain_bands.py')
    k = check_chain(d)
    e = d['energies'][d['gammas'].index(gamma)]
    ef = fermi_level(e, gamma, count)
    lo, up = e[:, 1], e[:, 2]
    if gamma == 0 and count == 1:                    # the metal: the c band crosses the f level at the Fermi level zero
        assert abs(ef) < 1e-12
        c0 = e[:, 0] + e[:, 3]
        assert np.sum(c0[:-1] < -1e-9) == 99 and np.sum(c0[:-1] > 1e-9) == 99     # filled and empty c states at E_F
        # the c band holds one half per k and spin, 99 of 200 momenta and the two at zero, so the flat f level at the
        # Fermi level holds the other half and is half filled, which the picture draws in the middle tone HALF
        zero = np.sum(np.abs(c0[:-1]) <= 1e-9)
        assert zero == 2 and abs((np.sum(c0[:-1] < -1e-9) + zero / 2) / (len(c0) - 1) - 0.5) < 1e-12
    elif count == 1:                                 # the insulator: the lower band is full and E_F is in the gap
        assert lo.max() < ef < up.min() and abs(ef) < 1e-12
    else:                                            # fewer particles: E_F cuts the lower band
        assert lo.min() < ef < lo.max() and ef < up.min()
        assert abs(np.mean(lo[:-1] < ef) - count) <= 1.0 / (len(e) - 1) + 1e-12
    print('gamma_K', gamma, 'particles per k and spin', count, 'Fermi level %.4f' % ef,
          'top of the lower band %.4f, bottom of the upper band %.4f' % (lo.max(), up.min()))
    fig, ax = plt.subplots(figsize=(4.0 * style.CM, 4.0 * style.CM))
    style.arrows(ax, xlabel=r'$k$', ylabel=r'$E/t$')
    if gamma == 0:
        curves = [e[:, 0] + e[:, 3], 0 * k]          # the c band and the f level, which sits at the Fermi level
    else:
        curves = [lo, up]
    for i, y in enumerate(curves):
        lw = 1.0 if (gamma == 0 and i == 1) else 1.6     # the f level of the metal is thinner, so the Fermi level shows
        if gamma == 0 and i == 1:                        # the half-filled f level of the metal, in the middle tone and
            ax.plot(k, y, color=HALF, lw=3.2, solid_capstyle='butt')     # wider than the Fermi level drawn on top
            continue
        filled = y <= ef + 1e-9
        empty = ~filled
        empty = empty | np.r_[empty[1:], False] | np.r_[False, empty[:-1]]     # one point more, so the line has no hole
        ax.plot(k, np.where(empty, y, np.nan), color=EMPTY, lw=lw, solid_capstyle='butt')
        ax.plot(k, np.where(filled, y, np.nan), color=style.ACCENT, lw=lw, solid_capstyle='butt')
    ax.axhline(ef, color=style.BROKEN, lw=1.5, ls=(0, (2.5, 1.5)), zorder=3)
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-2.7, 2.7)
    ticks(ax, KTICKS, ETICKS, fontsize=11.5)
    for t in ax.texts:
        t.set_fontsize(12)
    style.save(fig, script)
    return ef
