"""Shared code of the picture options of two quizzes of Session 2 on band structures. This file writes no figure.

Section 2.11a asks which of three band structures is graphene with first-neighbor hopping only. The data come from the
downloadable script webnotes/scripts/session02/g4_graphene_bands.py: the honeycomb lattice with the hopping +1, the
same lattice with h.add_sublattice_imbalance(0.5), and the triangular lattice with tij=[-1.], all on Gamma-K-M-Gamma.

Section 2.11b asks which of three band structures is the kagome lattice with H = -t sum c^dagger c and t > 0. The data
come from webnotes/scripts/session02/g4_kagome_bands.py: the kagome lattice with tij=[-1.] and with tij=[1.] on
Gamma-K-M-Gamma, and the Lieb lattice with tij=[-1.] on Gamma-X-M-Gamma.

A picture is the bands against the distance along the path, with the energy axis in units of t, the names of the
points and no other text. The three pictures of a quiz share the energy axis, and all the bands have the same color,
so that the answer is read from the shape alone. The asserts check every number that the feedback quotes."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style


def distance(g, kpath):
    """The distance along a path of reduced momenta, in units of the inverse bond length, and the Cartesian momenta."""
    A = np.array([g.a1[:2], g.a2[:2]])
    B = 2 * np.pi * np.linalg.inv(A).T
    kc = np.array([np.asarray(k)[:2] @ B for k in kpath])
    return np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(kc, axis=0), axis=1))]), kc


def check_graphene(d):
    """The numbers of the feedback of the quiz of Section 2.11a."""
    s0, s1, s2 = d['steps']
    iK, iM = s0, s0 + s1
    b, bi, bt = d['bands'], d['bands_imbalance'], d['band_triangular']
    assert np.allclose(b[0], [-3, 3]) and np.abs(b[iK]).max() < 1e-9 and np.allclose(b[iM], [-1, 1])
    assert np.allclose(bi[iK], [-0.5, 0.5])                              # the gap 1.0 at K
    assert abs((bi[:, 1] - bi[:, 0]).min() - 1.0) < 1e-9                  # and nowhere smaller on the path
    assert np.allclose(bi[0], [-np.sqrt(9.25), np.sqrt(9.25)])
    assert bt.ndim == 1 and len(bt) == len(b)                             # one band
    assert np.isclose(bt[0], -6) and np.isclose(bt[iK], 3) and np.isclose(bt[iM], 2)
    assert np.isclose(bt.min(), -6) and np.isclose(bt.max(), 3)           # the band runs from -6t to 3t
    return iK, iM


def check_flat(d):
    """The numbers of the feedback of the quiz of Section 2.11b."""
    s0, s1, s2 = d['steps']
    iK, iM = s0, s0 + s1
    km, kp, li = d['bands_kagome'], d['bands_kagome_plus'], d['bands_lieb']
    l0, l1, l2 = d['steps_lieb']
    iX, iMl = l0, l0 + l1
    assert np.allclose(km[:, 2], 2) and np.allclose(kp[:, 0], -2) and np.allclose(li[:, 1], 0)     # the flat bands
    assert np.allclose(km[0], [-4, 2, 2]) and np.allclose(km[iK], [-1, -1, 2]) and np.allclose(km[iM], [-2, 0, 2])
    assert np.allclose(kp, -km[:, ::-1])                                  # the opposite sign turns the bands upside down
    assert np.allclose(li[0], [-2 * np.sqrt(2), 0, 2 * np.sqrt(2)]) and np.allclose(li[iX], [-2, 0, 2])
    assert np.allclose(li[iMl], [0, 0, 0], atol=1e-9)                     # the three Lieb bands meet at M
    assert np.isclose(km.min(), -4) and np.isclose(km.max(), 2)
    assert np.isclose(kp.min(), -2) and np.isclose(kp.max(), 4)           # the opposite sign, from -2t to 4t
    return iK, iM, iX, iMl


def picture(script, x, bands, marks, names, ylim, yticks, ylabel=r'$E/t$'):
    """One picture option, the bands against the distance x along the path."""
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 4.2 * style.CM))
    for xv in marks:
        ax.axvline(x[xv], color=style.GRID, lw=0.8, zorder=0)
    ax.axhline(0, color=style.GRID, lw=0.8, zorder=0)
    bands = np.atleast_2d(np.asarray(bands).T).T
    for j in range(bands.shape[1]):
        ax.plot(x, bands[:, j], color=style.ACCENT, lw=1.6)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(x[0], x[-1]); ax.set_ylim(*ylim)
    ax.set_xticks([x[i] for i in marks]); ax.set_xticklabels(names, fontsize=11)
    ax.set_yticks(yticks); ax.set_yticklabels([('$%d$' % v) if v < 0 else '%d' % v for v in yticks], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_ylabel(ylabel, fontsize=12, labelpad=-2)
    style.save(fig, script)


def option_graphene(script, name):
    """A picture of the quiz of Section 2.11a: name is bands, bands_imbalance or band_triangular."""
    d = style.run_script('session02/g4_graphene_bands.py')
    iK, iM = check_graphene(d)
    g = d['gt'] if name == 'band_triangular' else d['g']
    x, _ = distance(g, d['kpath_t'] if name == 'band_triangular' else d['kpath'])
    picture(script, x, d[name], [0, iK, iM, len(x) - 1], [r'$\Gamma$', r'$K$', r'$M$', r'$\Gamma$'],
            (-6.6, 3.8), [-6, -3, 0, 3])


def option_flat(script, name):
    """A picture of the quiz of Section 2.11b: name is bands_kagome, bands_kagome_plus or bands_lieb."""
    d = style.run_script('session02/g4_kagome_bands.py')
    iK, iM, iX, iMl = check_flat(d)
    lieb = name == 'bands_lieb'
    x, _ = distance(d['gl'] if lieb else d['g'], d['kpath_lieb'] if lieb else d['kpath'])
    names = [r'$\Gamma$', r'$X$' if lieb else r'$K$', r'$M$', r'$\Gamma$']
    marks = [0, iX, iMl, len(x) - 1] if lieb else [0, iK, iM, len(x) - 1]
    picture(script, x, d[name], marks, names, (-4.5, 4.5), [-4, -2, 0, 2, 4], ylabel=r'$\epsilon/t$')
