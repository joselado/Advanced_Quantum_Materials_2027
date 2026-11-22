"""Shared code of the figures of the self-consistent pairing of the attractive chain, Section 5.5.

The data come from the downloadable script webnotes/scripts/session05/g1_meanfield_swave_chain.py, which runs the
mean-field loop of pyqula for the chain (5.2) with t=1 (tij=[-1.]), 0.2 electrons per site (filling=0.1), nk=100 and
mix=0.5, the settings of the notebook cell "Dependence on the strength of the attractive interaction". The checks below
compare it with a second route, the BCS gap equation 1 = -U (1/N) sum_k 1/(2 E_k) solved with numpy at the same density,
and they hold the numbers that the caption of g1_gap_against_u and the feedback of the picture quiz quote. The picture
options draw the BdG bands of one chain each, with their axes and no other text. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style


def bcs(U, n=0.2, N=40000):
    """|Delta| and mu of the BCS gap equation of the chain -2 cos k at the density n per site, on N momenta. The
    density is (1/N) sum_k (1 - xi_k/E_k), with the two spins, and the gap equation 1 = -U (1/N) sum_k 1/(2 E_k)."""
    from scipy.optimize import brentq
    k = 2 * np.pi * (np.arange(N) + 0.5) / N
    eps = -2 * np.cos(k)

    def mu_of(D):
        return brentq(lambda mu: np.mean(1 - (eps - mu) / np.sqrt((eps - mu) ** 2 + D ** 2)) - n, -30, 30, xtol=1e-13)

    def gap_eq(D):
        xi = eps - mu_of(D)
        return 1 + U * np.mean(1 / (2 * np.sqrt(xi ** 2 + D ** 2)))

    D = brentq(gap_eq, 1e-6, 2.0, xtol=1e-12)
    return D, mu_of(D)


def check(d):
    """The numbers of the caption and of the quiz, on the data of the pyqula script and with the gap equation."""
    Us, deltas, smallest = np.array(d['Us']), d['deltas'], d['smallest']
    assert list(Us) == [-0.75, -1.0, -1.25, -1.5, -1.75, -2.0]
    # the smallest quasiparticle energy is |Delta| at every point, so the Fermi level is inside the band
    assert np.allclose(smallest, deltas, atol=2e-4), (smallest, deltas)
    # the second route, the BCS gap equation at the same density, agrees to 1e-3 at every point
    ref = np.array([bcs(U)[0] for U in Us])
    assert np.allclose(deltas, ref, atol=1e-3), (deltas, ref)
    # the values of the caption and of the quiz, 0.10, 0.22 and 0.36, and the conventions sheet, 0.1031, 0.2226, 0.3606
    D = dict(zip(Us, deltas))
    for U, v, two in ((-1.0, 0.1031, 0.10), (-1.5, 0.2226, 0.22), (-2.0, 0.3606, 0.36)):
        assert abs(D[U] - v) < 5e-4 and round(D[U], 2) == two, (U, D[U])
    # the two branches are 2|Delta| apart, as the feedback of the quiz says, here 0.21, 0.45 and 0.72
    for U, sep in ((-1.0, 0.21), (-1.5, 0.45), (-2.0, 0.72)):
        e = d['bands'][list(Us).index(U)]
        gap = e[:, 2].min() - e[:, 1].max()
        assert abs(gap - 2 * D[U]) < 5e-4 and round(gap, 2) == sep, (U, gap)
    # twice the attraction gives a pairing 3.5 times larger, and |Delta| grows with |U|
    assert round(D[-2.0] / D[-1.0], 1) == 3.5 and np.all(np.diff(deltas) > 0)
    # the curve bends up, its slope grows, and |Delta|/|U| grows, so |Delta| grows faster than |U|
    assert np.all(np.diff(np.diff(deltas)) > 0) and np.all(np.diff(deltas / -Us) > 0)
    # a mesh of 100 momenta is converged at U=-0.75 and not at U=-0.5, the reason why the plot starts at 0.75
    assert abs(bcs(-0.75, N=100)[0] - bcs(-0.75)[0]) < 1e-3
    assert abs(bcs(-0.5, N=100)[0] - bcs(-0.5)[0]) > 0.1 * bcs(-0.5)[0]
    print('|Delta|', np.round(deltas, 4), 'gap equation', np.round(ref, 4), 'ratio', round(D[-2.0] / D[-1.0], 3))


def option(script, d, U):
    """One picture option, the BdG bands of the chain with the interaction U, with the same axes for the three."""
    check(d)
    e = d['bands'][list(d['Us']).index(U)]
    k = 2 * np.pi * np.array(d['ks'])
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    ax.axhline(0, color=style.GRID, lw=0.8, zorder=0)
    for n in range(e.shape[1]):
        ax.plot(k, e[:, n], color=style.ACCENT, lw=1.6)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-0.6, 0.6)
    ax.set_xticks([-1, 0, 1]); ax.set_xticklabels(['$-1$', '0', '1'], fontsize=11)
    ax.set_yticks([-0.5, 0, 0.5]); ax.set_yticklabels(['$-0.5$', '0', '0.5'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$k$', fontsize=12, labelpad=0); ax.set_ylabel(r'$E$', fontsize=12, labelpad=-4)
    style.save(fig, script)
