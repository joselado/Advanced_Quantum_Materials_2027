"""Shared code of the picture options of the quiz of Section 4.4 that asks which of three staircases of the Hall
conductivity belongs to the strongest field. This file writes no figure.

The data come from the downloadable script webnotes/scripts/session04/g1_landau_levels_square.py, the square lattice
with tij=[-1.] in the magnetic cell of q sites along y and h.add_orbital_magnetic_field(1/q), for q = 10, 20 and 40.
The Hall conductivity in units of e^2/h is the Chern number h.get_chern() of the filled bands with the Fermi energy in
each gap below E_F = -2t, and a picture draws it as the staircase of a clean system at zero temperature, against E_F
from -4t to -2t, with the steps at the energies of the bands. The three pictures share both axes. The asserts check
every number that the feedback of the quiz quotes."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

XLO, XHI, YTOP = -4.0, -2.0, 7.6


def check(d):
    """The numbers of the feedback, for the three fluxes."""
    lev = {q: np.asarray(d['levels'][q]) for q in (10, 20, 40)}
    sig = {q: np.asarray(d['sigma_xy'][q]) for q in (10, 20, 40)}
    bands = {q: np.asarray(d['bands'][q]) for q in (10, 20, 40)}
    step = {q: lev[q][1] - lev[q][0] for q in (10, 20, 40)}
    for q in (10, 20, 40):
        n = len(sig[q]) - 1
        # the levels below -2t, each with a jump of one, and the bands that are drawn are flat on the scale of a step
        assert np.allclose(sig[q], np.arange(n + 1), atol=1e-6) and np.all(lev[q][:n] < XHI) and lev[q][n] > XHI
        assert np.ptp(bands[q][:, :n], axis=0).max() < 0.01 * step[q]
    assert [len(sig[q]) - 1 for q in (10, 20, 40)] == [2, 4, 7]
    # the plateau at sigma_xy = e^2/h, between the first two jumps, is 1.07, 0.58 and 0.30 t wide, against 4 pi t / q
    # of the continuum, 1.26, 0.63 and 0.31 t. The alt texts count the jumps below -2t, 2, 4 and 7
    assert [round(step[q], 2) for q in (10, 20, 40)] == [1.07, 0.58, 0.30]
    assert [round(4 * np.pi / q, 2) for q in (10, 20, 40)] == [1.26, 0.63, 0.31]
    assert step[10] > step[20] > step[40] and all(step[q] < 4 * np.pi / q for q in (10, 20, 40))
    print('first steps', {q: round(step[q], 3) for q in (10, 20, 40)}, 'levels below -2t', {q: len(sig[q]) - 1 for q in (10, 20, 40)},
          'widest band drawn', max(np.ptp(bands[q][:, :len(sig[q]) - 1], axis=0).max() for q in (10, 20, 40)))


def option(script, q):
    """One picture option, the staircase of the flux 1/q."""
    d = style.run_script('session04/g1_landau_levels_square.py')
    check(d)
    lev, sig = np.asarray(d['levels'][q]), np.asarray(d['sigma_xy'][q])
    n = len(sig) - 1
    xs, ys = [XLO], [0.]
    for i in range(n):
        xs += [lev[i], lev[i]]; ys += [i, i + 1]
    xs.append(XHI); ys.append(n)
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.6 * style.CM))
    ax.plot(xs, ys, color=style.BROKEN, lw=1.5)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(XLO, XHI); ax.set_ylim(0, YTOP)
    ax.set_xticks([-4, -3, -2]); ax.set_xticklabels([r'$-4$', r'$-3$', r'$-2$'], fontsize=11)
    ax.set_yticks([0, 2, 4, 6]); ax.set_yticklabels(['0', '2', '4', '6'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$E_F/t$', fontsize=12, labelpad=0); ax.set_ylabel(r'$\sigma_{xy}\,h/e^2$', fontsize=12, labelpad=1)
    style.save(fig, script)
