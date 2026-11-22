"""Shared code of the band plots of a chain with an exchange field, Section 5.12, for spin_split_pairing and the three
picture options of the quiz on which spins reach the Fermi level.

The data come from the downloadable script webnotes/scripts/session05/g3_exchange_chain_bands.py, which calls pyqula
for the chain with t=1 (tij=[-1.]), the chemical potential mu (add_onsite(-mu)) and the exchange field
-h(n_up - n_dn) of Section 5.12 (add_exchange([0,0,-h]), as webnotes/conventions/session05.md says). Its cases are
(mu, h) = (0, 0.6) for the figure of the page and (-1.5, 0.2), (-1.5, 1.2), (-1.5, -1.2) for the quiz. The checks
compare every band with eps(k) -+ h, eps(k) = -2t cos k - mu, and hold the numbers that the caption and the feedback
quote. The bands are colored by spin, style.ACCENT for up and style.BROKEN for down. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

CASES = [(0., 0.6), (-1.5, 0.2), (-1.5, 1.2), (-1.5, -1.2)]


def kf(mu, field, s):
    """The Fermi momentum of spin s (+1 up, -1 down) of the band -2 cos k - mu - s h, or None when it does not cross."""
    c = -(mu + s * field) / 2
    return np.arccos(c) if abs(c) < 1 else None


def check(d):
    """The bands of pyqula against eps -+ h, and the numbers of the caption and of the quiz."""
    assert [tuple(c) for c in d['cases']] == CASES
    k = 2 * np.pi * np.array(d['kpath'])[:, 0]
    for (mu, field), e, sz in zip(CASES, d['energies'], d['spins']):
        assert np.allclose(np.abs(sz), 1, atol=1e-9)                        # every state has s_z = +1 or -1
        for s in (1, -1):
            band = np.where(np.isclose(sz, s), e, np.nan)
            band = np.nanmax(band, axis=1)                                    # one state of spin s at each k
            assert np.allclose(band, -2 * np.cos(k) - mu - s * field, atol=1e-9), (mu, field, s)
    # the figure of the page, t=1, mu=0, h=0.6: the Fermi momenta and the singlet partner at 2h=1.2
    mu, field = CASES[0]
    ku, kd = kf(mu, field, 1), kf(mu, field, -1)
    assert round(ku, 3) == 1.875 and round(kd, 3) == 1.266 and ku > kd
    partner = -2 * np.cos(-ku) - mu + field                                  # the down electron at -k_F up
    assert abs(partner - 2 * field) < 1e-12 and abs(2 * field - 1.2) < 1e-12
    # the quiz, mu=-1.5: both spins cross for h=0.2, only up for h=1.2, only down for h=-1.2
    assert round(kf(-1.5, 0.2, 1), 3) == 0.863 and round(kf(-1.5, 0.2, -1), 3) == 0.555
    assert round(kf(-1.5, 1.2, 1), 3) == 1.420 and kf(-1.5, 1.2, -1) is None
    assert round(kf(-1.5, -1.2, -1), 3) == 1.420 and kf(-1.5, -1.2, 1) is None
    for (mu, field), e, sz in zip(CASES[1:], d['energies'][1:], d['spins'][1:]):
        crosses = {s: np.nanmin(np.where(np.isclose(sz, s), e, np.nan)) < 0 < np.nanmax(np.where(np.isclose(sz, s), e, np.nan))
                   for s in (1, -1)}
        assert crosses == {1: kf(mu, field, 1) is not None, -1: kf(mu, field, -1) is not None}
    # the band that does not cross has its bottom 0.7 above the Fermi level, -2 - mu + |h|
    assert abs((-2 + 1.5 + 1.2) - 0.7) < 1e-12
    return k


def bands(ax, k, e, sz, lw=1.8):
    """The two bands, each drawn in the color of its spin."""
    for s, c in ((1, style.ACCENT), (-1, style.BROKEN)):
        band = np.nanmax(np.where(np.isclose(sz, s), e, np.nan), axis=1)
        ax.plot(k, band, color=c, lw=lw)


def frame(ax, xticks, yticks, xlabel, ylabel, fs):
    """Left and bottom axes with ticks and names."""
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_linewidth(0.6)
    ax.set_xticks([t for t, _ in xticks]); ax.set_xticklabels([l for _, l in xticks], fontsize=fs - 1)
    ax.set_yticks([t for t, _ in yticks]); ax.set_yticklabels([l for _, l in yticks], fontsize=fs - 1)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(xlabel, fontsize=fs, labelpad=0); ax.set_ylabel(ylabel, fontsize=fs, labelpad=1)


def option(script, d, case):
    """One picture option of the quiz, the bands of one chain with their axes and no other text."""
    k = check(d)
    i = CASES.index(case)
    fs = 12
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.9 * style.CM))
    style.guide(ax, y=0)
    bands(ax, k, d['energies'][i], d['spins'][i])
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-2.2, 3.2)
    frame(ax, [(-np.pi, r'$-\pi$'), (0, '0'), (np.pi, r'$\pi$')], [(-2, '$-2$'), (0, '0'), (2, '2')],
          r'$k$', r'$E/t$', fs)
    style.save(fig, script)
