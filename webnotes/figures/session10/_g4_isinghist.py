"""Histograms of |m| for single snapshots of the Ising model (10.9) on 16 x 16 sites, the picture options of a quiz of
Section 10.6a, at k_BT = 1.5 J, 2.27 J and 3.5 J.

The snapshots come from the pyqula script scripts/session10/g4_ising_snapshots.py, which style.run_script runs, so that
the pictures are that calculation. A picture of a quiz has no button. On 256 spins |m| takes the values k/128, so a
bin holds three of these values and its edges sit between them, which avoids a comb. The three pictures share the bins,
the axes and the scale, and nothing else is written on them. check() asserts the numbers of the feedback for the seed
of the script, and checks/session10/g4_06_phase_classification.py asserts them again for other seeds. This file writes
no figure, the scripts g4_quiz_ising_hist_*.py call draw."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

TEMPS = (1.5, 2.27, 3.5)
BINS = (3 * np.arange(44) - 0.5) / 128      # 43 bins of width 3/128, from -0.5/128 to 128.5/128
TC = 2 / np.log(1 + np.sqrt(2))


def exact_m(T):
    """|m| of the infinite lattice, from the exact solution, below T_c."""
    return (1 - np.sinh(2 / T) ** -4) ** 0.125


def check(absm):
    """The statements of the feedback, for one set of snapshots: a dictionary from the temperature to |m|."""
    assert round(TC, 2) == 2.27 and abs(TC - 2.27) < 2e-3          # 2.27 J is T_c to 0.001 J
    lo, tc, hi = (np.asarray(absm[T]) for T in TEMPS)
    assert len(lo) == len(tc) == len(hi) == 1000
    for a in (lo, tc, hi):                                           # the values k/128 of 256 spins
        assert np.allclose(a * 128, np.round(a * 128))
    assert round(lo.mean(), 2) == 0.99 == round(exact_m(1.5), 2)     # the mean 0.99, as the exact 0.9865
    assert lo.min() > 0.85                                           # every snapshot close to one
    assert tc.min() < 0.5 and tc.max() > 0.9                          # wide, from below 0.5 to above 0.9
    assert np.percentile(tc, 5) < 0.6 and np.percentile(tc, 95) > 0.9
    assert 0.115 <= hi.mean() < 0.135                                 # the mean 0.12 to 0.13
    assert hi.max() < lo.min()                                        # the two ends do not overlap
    return lo.mean(), tc.min(), tc.max(), hi.mean()


def check_pictures(absm):
    """What the alt texts say of the drawn histograms, for the seed of the script."""
    dens = densities(absm)
    mid = (BINS[:-1] + BINS[1:]) / 2
    assert np.percentile(absm[1.5], 5) > 0.95                         # one narrow peak next to one
    assert 0.8 < mid[dens[2.27].argmax()] < 0.9                       # wide, with its maximum near 0.85
    assert mid[dens[3.5].argmax()] < 0.1 and np.percentile(absm[3.5], 95) < 0.4   # highest near zero, off toward 0.4


def densities(absm):
    return {T: np.histogram(absm[T], bins=BINS, density=True)[0] for T in TEMPS}


def draw(script, T):
    """Writes the picture of the snapshots at the temperature T, one of TEMPS."""
    d = style.run_script('session10/g4_ising_snapshots.py')     # the literal name, which the build reads as a dependency
    check(d['absm'])
    check_pictures(d['absm'])
    dens = densities(d['absm'])
    top = max(c.max() for c in dens.values())
    fig, ax = style.plt.subplots(figsize=(4.4 * style.CM, 4.4 * style.CM))
    style.arrows(ax, xlabel=r'$|m|$', ylabel=r'$p(|m|)$', ticks=True)
    ax.stairs(dens[T], BINS, color=style.ACCENT, lw=0, fill=True, alpha=0.35)
    ax.stairs(dens[T], BINS, color=style.ACCENT, lw=1.4)
    ax.set_xlim(0, 1.06); ax.set_ylim(0, 1.08 * top)
    ax.set_xticks([0, 0.5, 1]); ax.set_xticklabels(['0', '0.5', '1'])
    ax.set_yticks([0, 15, 30] if top > 30 else [0, 10, 20])
    ax.tick_params(direction='out', length=3, width=0.6, labelsize=12)      # large, so that it reads at 390 px
    for t in ax.texts:
        t.set_fontsize(12.5)
    style.save(fig, script)
