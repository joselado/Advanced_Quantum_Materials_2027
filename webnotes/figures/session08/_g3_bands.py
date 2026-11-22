"""Shared code of the figure spinon_bands of Section 8.9 and of the three picture options of its quiz on Dirac spinons.

The data come from the downloadable script webnotes/scripts/session08/g3_spinon_band_classes.py, which calls pyqula with
the hopping chi = +1. check() asserts the numbers that the caption of the figure and the feedback of the quiz quote, and
panel() draws one band structure against the phase per cell, from -pi to pi,
with the Fermi level of half filling as a grey line at zero. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style


def momenta(d, name):
    """The momentum of each point of the path as the phase per cell, from -pi to pi. The cell is one site for the uniform
    chain and, along x, for the pi-flux lattice, so there it is the momentum in units of the inverse distance between
    sites, and it is two sites for the dimerized chain."""
    return 2 * np.pi * d['ks']


def check(d):
    """The numbers of the caption and of the quiz, checked on the data of the pyqula script."""
    ks = d['ks']
    assert len(ks) == 401 and abs(ks[0] + 0.5) < 1e-12 and abs(ks[-1] - 0.5) < 1e-12
    eu, ed, ep = d['e_uniform'], d['e_dimerized'], d['e_piflux']
    k = momenta(d, 'uniform')
    # the uniform chain, 2 chi cos k with chi = +1, crosses the Fermi level at k = +-pi/2
    assert eu.shape == (401, 1) and np.abs(eu[:, 0] - 2 * np.cos(k)).max() < 1e-12
    cross = k[np.abs(eu[:, 0]) < 1e-9]
    assert np.allclose(cross, [-np.pi / 2, np.pi / 2])
    # the dimerized chain, hoppings 0.6 and 1, two bands +-|0.6 + exp(i k)| with k the phase per cell of two sites,
    # the gap 2 (1 - 0.6) = 0.8 at the edge of its zone, k = +-pi, and the bands between -1.6 and 1.6
    assert ed.shape == (401, 2) and np.allclose(ed[:, 1], np.abs(0.6 + np.exp(1j * k))) and np.allclose(ed[:, 0], -ed[:, 1])
    gap = ed[:, 1].min() - ed[:, 0].max()
    assert abs(gap - 0.8) < 1e-12 and np.allclose(k[np.isclose(ed[:, 1], 0.4)], [-np.pi, np.pi])
    assert abs(ed.max() - 1.6) < 1e-12
    # the pi-flux lattice along k_y = pi/2, two bands +-2|sin k_x| that touch linearly at k_x = 0 and +-pi
    assert ep.shape == (401, 2) and np.abs(ep[:, 1] - 2 * np.abs(np.sin(k))).max() < 1e-12 and np.allclose(ep[:, 0], -ep[:, 1])
    touch = k[np.abs(ep[:, 1]) < 1e-9]
    assert np.allclose(touch, [-np.pi, 0, np.pi])
    slope = (ep[201, 1] - ep[200, 1]) / (k[201] - k[200])
    assert abs(slope - 2) < 1e-3                                         # linear, with the velocity 2 chi
    # the opposite sign of the hopping gives the same levels: -2 cos k is 2 cos k moved by pi, and the two bands of the
    # other two models are symmetric around zero
    assert np.allclose(np.sort(-2 * np.cos(k)), np.sort(2 * np.cos(k + np.pi)), atol=1e-12)
    print('uniform chain crosses zero at k/pi =', np.round(cross / np.pi, 3), ', dimerized gap %.3f at k/pi = +-1' % gap,
          ', pi-flux bands touch at kx/pi =', np.round(touch / np.pi, 3), 'with the slope %.4f' % slope)


def panel(ax, d, name, xlabel, fontsize, ylabel=None):
    """One band structure of the script, its axes with ticks at k = -pi, 0, pi and at E = -2, 0, 2."""
    k, E = momenta(d, name), d['e_' + name]
    style.arrows(ax, xlabel=xlabel, ylabel=ylabel)
    ax.axhline(0, color=style.GRID, lw=1.0, zorder=0)
    for b in range(E.shape[1]):
        ax.plot(k, E[:, b], color=style.ACCENT, lw=1.4)
    edge = k[-1]
    ax.set_xlim(-edge, edge); ax.set_ylim(-2.7, 2.7)
    assert abs(edge - np.pi) < 1e-12
    ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', r'$0$', r'$\pi$'])
    ax.set_yticks([-2, 0, 2]); ax.set_yticklabels([r'$-2$', r'$0$', r'$2$'])
    ax.tick_params(length=2.5, width=0.6, pad=2, labelsize=fontsize - 0.5)
    for t in ax.texts:
        t.set_fontsize(fontsize)
    return k, E


def option(script, name):
    """One picture option of the quiz, the band structure d[name], with its axes and no other text."""
    d = style.run_script('session08/g3_spinon_band_classes.py')
    check(d)
    fig, ax = style.plt.subplots(figsize=(4.0 * style.CM, 4.0 * style.CM))
    panel(ax, d, name, xlabel=r'$k$', ylabel=r'$E/\chi$', fontsize=12)
    style.save(fig, script)
