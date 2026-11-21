"""Shared code of the ribbon pictures of Sections 3.11 and 3.11b, the edge states of a honeycomb ribbon colored by their spin.

The data come from the downloadable scripts webnotes/scripts/session03/g4_ribbon_*.py and g4_edge_*.py, which call pyqula. The
ribbon is honeycomb_zigzag_ribbon(10), 40 sites across, periodic along x, with the first-neighbor hopping t=1. In pyqula
add_soc(0.1) gives the bulk gap 0.9 t (the scripts use -0.1, so that spin up moves to the right on the lower edge, as in
spin_sectors.py and kramers_edge.py), add_haldane(0.1) gives the same gap, and add_sublattice_imbalance(m) gives the gap 2m.
Each script returns, for every state, its momentum times the lattice constant, its energy, <s_z> and its mean position <y> across
the ribbon, whose edges are at y = -width/2 and width/2. A small bias 0.002 y across the ribbon separates the states of the two
edges, which are degenerate without it, so that these two numbers are well defined. A state is drawn in color when it sits at the
lower edge, <y> < -0.36 width, red for <s_z> > 0 and blue for <s_z> < 0, and all the bands are drawn in grey below. The pictures have their axes and no other text,
since they are the options of a quiz. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

UP, DOWN = style.BROKEN, style.ACCENT


def load(d):
    """The variables of one script, from style.run_script, as arrays of the shape (momenta, bands). At each momentum the
    energies are sorted. 'lower' marks the states of the lower edge."""
    nk = d['nk']
    out = {key: np.asarray(d[key], float).reshape(nk, -1) for key in ('momentum', 'energy', 'spin', 'position')}
    out['lower'] = out['position'] < -0.36 * d['width']
    assert np.allclose(out['momentum'][:, 0], 2 * np.pi * d['ks']) and np.all(np.diff(out['energy'], axis=1) > -1e-9)
    assert nk % 2 == 1 and abs(out['momentum'][nk // 2, 0] - np.pi) < 1e-12        # k = pi is on the mesh
    return out


def edge(d, emax):
    """The states of the lower edge with |E| < emax: momentum, energy and <s_z>."""
    sel = d['lower'] & (np.abs(d['energy']) < emax)
    return d['momentum'][sel], d['energy'][sel], d['spin'][sel]


def crossings(k, e, s, level=0.0):
    """Where the branch of each spin of the lower edge crosses the energy level: (momentum, velocity) for up and for down."""
    out = []
    for sgn in (1, -1):
        m = sgn * s > 0.5
        kk, ee = k[m], e[m]
        o = np.argsort(kk); kk, ee = kk[o], ee[o]
        i = np.where(np.sign(ee[:-1] - level) != np.sign(ee[1:] - level))[0]
        i = i[np.diff(kk)[i] < 0.1]                 # neighbors on the mesh, so one branch and not a jump between two
        out.append([(kk[j] + (level - ee[j]) * (kk[j + 1] - kk[j]) / (ee[j + 1] - ee[j]),
                     (ee[j + 1] - ee[j]) / (kk[j + 1] - kk[j])) for j in i])
    return out


def option(script, d, klim, elim, kticks, eticks, emax):
    """One picture option with its axes and no other text."""
    plt.rcParams.update({'savefig.dpi': 220})
    fig, ax = plt.subplots(figsize=(3.2 * style.CM, 3.6 * style.CM))
    K, E = d['momentum'], d['energy']
    ax.plot(K, E, color='#c4c4c4', lw=0.5, zorder=0, rasterized=True)
    k, e, s = edge(d, emax)
    for sgn, col in ((1, UP), (-1, DOWN)):
        m = sgn * s > 0.05
        ax.plot(k[m], e[m], 'o', ms=1.7, color=col, mec='none', zorder=3 + sgn, rasterized=True)
    if kticks[0][0] > 0.1:                         # a zoom around k = pi, with a guide line at this momentum
        ax.axvline(np.pi, color=style.MUTED, lw=0.6, ls=(0, (4, 3)), zorder=1)
    ax.set_xlim(*klim); ax.set_ylim(*elim)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    ax.set_xticks([t for t, _ in kticks]); ax.set_xticklabels([l for _, l in kticks], fontsize=11)
    ax.set_yticks([t for t, _ in eticks]); ax.set_yticklabels([l for _, l in eticks], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$k$', fontsize=12, labelpad=0); ax.set_ylabel(r'$E/t$', fontsize=12, labelpad=-9)
    style.save(fig, script)


def ribbon_option(script, d):
    """A picture of Section 3.11, the whole zone."""
    option(script, d, (0, 2 * np.pi), (-1.25, 1.25), [(0, '0'), (np.pi, r'$\pi$'), (2 * np.pi, r'$2\pi$')],
           [(-1, '$-1$'), (0, ''), (1, '$1$')], emax=0.62)


def edge_option(script, d):
    """A picture of Section 3.11b, a zoom on the edge states around k = pi."""
    option(script, d, (np.pi - 1.1, np.pi + 1.1), (-0.62, 0.62), [(np.pi, r'$\pi$')],
           [(-0.5, '$-0.5$'), (0, ''), (0.5, '$0.5$')], emax=0.5)
