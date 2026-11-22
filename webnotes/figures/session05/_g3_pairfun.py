"""Shared code of the stem plots of the pair amplitude of a chain, Section 5.11, for pair_function and the three
picture options of its quiz.

The real-space amplitude Delta(r), with r the distance between the two paired electrons in units of the lattice
constant, is the Fourier transform Delta(r) = (1/N) sum_k Delta(k) e^{ikr}, computed with an FFT on a ring of N=64
sites, for Delta(k) = Delta0 (onsite s-wave), 2 Delta0 cos k (extended s-wave) and 2i Delta0 sin k (p-wave, the form
printed in (5.20)). The values are in units of Delta0. An even Delta(k) gives an even Delta(r), an odd one gives an odd
Delta(r) that vanishes at r=0. Which of the two stems of the p-wave case is positive depends on the sign of the Fourier
transform and of (5.20), which is open, so no caption and no feedback says it. This is numpy, since a Fourier
transform of a given function is no calculation for pyqula. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

N = 64
K = 2 * np.pi * np.fft.fftfreq(N)
R = np.arange(-3, 4)
CASES = {'onsite': (np.ones(N, complex), r'$\Delta_0$', r'onsite $s$', 'even'),
         'extended': (2 * np.cos(K) + 0j, r'$2\Delta_0\cos k$', r'extended $s$', 'even'),
         'pwave': (2j * np.sin(K), r'$2i\Delta_0\sin k$', r'$p$-wave', 'odd')}


def amplitude(name):
    """Delta(r)/Delta0 at r = -3..3 for one of the three cases, with the checks of what the figures and the quiz say."""
    dk, _, _, par = CASES[name]
    dr = np.fft.ifft(dk)                                         # (1/N) sum_k Delta(k) e^{ikr}
    vals = np.array([dr[r % N] for r in R])
    assert np.allclose(vals.imag, 0, atol=1e-12)
    vals = vals.real
    sgn = 1 if par == 'even' else -1
    assert np.allclose(vals, sgn * vals[::-1], atol=1e-12)        # Delta(-r) = +-Delta(r), as Delta(-k) = +-Delta(k)
    # the shapes that the caption and the alt texts describe
    nonzero = [int(r) for r, v in zip(R, vals) if abs(v) > 1e-9]
    if name == 'onsite':
        assert nonzero == [0] and abs(vals[3] - 1) < 1e-12                       # one stem of height Delta0 at r=0
    elif name == 'extended':
        assert nonzero == [-1, 1] and np.allclose(vals[[2, 4]], 1, atol=1e-12)    # two equal stems at r=-1 and 1
    else:
        assert nonzero == [-1, 1] and abs(vals[3]) < 1e-12                       # nothing at r=0
        assert abs(abs(vals[2]) - 1) < 1e-12 and abs(vals[2] + vals[4]) < 1e-12   # two stems of opposite sign
    # the Fourier transform back gives the Delta(k) of the case, so the stems are the whole pairing
    back = sum(v * np.exp(-1j * K * r) for r, v in zip(R, vals))
    assert np.allclose(back, dk, atol=1e-12)
    return vals


def stems(ax, vals, fs, ms=5.5, lw=2.2):
    """The stems of Delta(r), blue above zero and red below, and an open dot where Delta(r)=0."""
    style.guide(ax, y=0)
    for r, val in zip(R, vals):
        if abs(val) > 1e-9:
            c = style.ACCENT if val > 0 else style.BROKEN
            ax.plot([r, r], [0, val], color=c, lw=lw, solid_capstyle='butt')
            ax.plot(r, val, 'o', color=c, ms=ms, clip_on=False, zorder=5)
        else:
            ax.plot(r, 0, 'o', color=style.MUTED, ms=ms * 0.55, mfc='white', mew=0.9, zorder=5)


def frame(ax, fs, yname=True):
    """Axes r and Delta(r)/Delta0 with ticks, the left and bottom spines only."""
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_linewidth(0.6)
    ax.spines['bottom'].set_position(('data', -1.35))
    ax.set_xlim(-3.5, 3.5); ax.set_ylim(-1.35, 1.35)
    ax.set_xticks([-2, -1, 0, 1, 2]); ax.set_xticklabels(['$-2$', '$-1$', '0', '1', '2'], fontsize=fs - 1)
    ax.set_yticks([-1, 0, 1]); ax.set_yticklabels(['$-1$', '0', '1'], fontsize=fs - 1)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$r$', fontsize=fs, labelpad=1)
    if yname:
        ax.set_ylabel(r'$\Delta(r)/\Delta_0$', fontsize=fs, labelpad=1)


def option(script, name):
    """One picture option of the quiz, the stems of one case with their axes and no other text."""
    vals = amplitude(name)
    fs = 12
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.7 * style.CM))
    stems(ax, vals, fs, ms=5, lw=2.0)
    frame(ax, fs)
    ax.set_xticks([-2, 0, 2]); ax.set_xticklabels(['$-2$', '0', '2'], fontsize=fs - 1)
    style.save(fig, script)
