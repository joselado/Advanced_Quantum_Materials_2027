"""Shared code of the picture options of the closing quiz of Session 2, Section 2.13, which asks which of three
densities of states belongs to graphene. This file writes no figure.

The data come from the downloadable script webnotes/scripts/session02/g4_dos_three.py: the chain with tij=[-1.], the
honeycomb lattice with the hopping +1 and the kagome lattice with tij=[-1.], all spinless, with Lorentzians of half
width 0.04 on the same energies. pyqula counts per unit cell and sums over the bands. A picture is the density g(E)
against E in units of t, with its axes and no other text. The three pictures share both axes, and the high peak of
the kagome flat band is cut at the top. The asserts check every number that the feedback quotes."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style


def peak(e, d, E0, w=0.4):
    """The energy of the largest value of d within w of E0."""
    sel = np.abs(e - E0) < w
    return e[sel][np.argmax(d[sel])]


def check(d):
    e = np.array(d['e']); de = e[1] - e[0]
    c, hc, k = np.array(d['dos_chain']), np.array(d['dos_honeycomb']), np.array(d['dos_kagome'])
    i0 = np.argmin(np.abs(e))
    # the chain: 1/(pi sqrt(4t^2 - E^2)) per site, 1/(2 pi t) = 0.16/t at zero energy, peaks at the band edges +-2t
    assert abs(c[i0] - 1 / (2 * np.pi)) < 0.002 and abs(1 / (2 * np.pi) - 0.16) < 0.005
    assert abs(peak(e, c, -2.0) + 1.98) < 0.03 and abs(peak(e, c, 2.0) - 1.98) < 0.03
    assert abs(c.sum() * de - 1) < 0.02 and c[np.abs(e) < 1.5].min() > 0.15             # one state, no dip in the band
    # graphene: the V that touches zero energy, 0.04 from the broadening, peaks at +-t, ends at +-3t
    assert abs(hc[i0] - 0.04) < 0.002 and hc[np.abs(e) < 0.5].min() == hc[i0]
    assert abs(peak(e, hc, -1.0) + 1) < 0.015 and abs(peak(e, hc, 1.0) - 1) < 0.015
    assert hc[e < -3.3].max() < 0.02 and hc[e > 3.2].max() < 0.02
    # kagome: the flat band at 2t, a narrow peak far above the others, peaks at -2t and 0, a V at -t
    assert abs(e[np.argmax(k)] - 2) < 1e-9 and k.max() > 7
    assert abs(peak(e, k, -2.0) + 2) < 0.02 and abs(peak(e, k, 0.0)) < 0.02
    sel = np.abs(e + 1) < 0.4
    assert abs(e[sel][np.argmin(k[sel])] + 1) < 0.02
    assert k[e < -4.3].max() < 0.03
    print('chain at 0', round(c[i0], 4), 'graphene at 0', round(hc[i0], 4), 'kagome max', round(k.max(), 2))


def option(script, name):
    """One picture option, the density d[name] against the energy."""
    d = style.run_script('session02/g4_dos_three.py')
    check(d)
    e, g = np.array(d['e']), np.array(d[name])
    top = 0.9
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.6 * style.CM))
    ax.fill_between(e, 0, np.minimum(g, top), color=style.LIGHT, alpha=0.35, lw=0)
    ax.plot(e, np.minimum(g, top), color=style.ACCENT, lw=1.3)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(-4.5, 3.5); ax.set_ylim(0, top)
    ax.set_xticks([-4, -2, 0, 2]); ax.set_xticklabels([r'$-4$', r'$-2$', '0', '2'], fontsize=11)
    ax.set_yticks([0, 0.5]); ax.set_yticklabels(['0', '0.5'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$E/t$', fontsize=12, labelpad=0); ax.set_ylabel(r'$g(E)$', fontsize=12, labelpad=1)
    style.save(fig, script)
