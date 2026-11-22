"""Shared code of the three pictures of the quiz of Section 4.10 on the Landau ladder of graphene.

Three ladders at one field, as closed formulas, so numpy and no pyqula: the parabolic ladder (n + 1/2) hbar omega_c of
(4.6), in units of hbar omega_c, the Dirac ladder sgn(n) sqrt(|n|) E_1 of (4.7), and the same square-root ladder without
the level at zero energy, both in units of E_1. The three pictures have the same size and the same height of the energy
window, 4.6 units, and each one has its energy axis with ticks. check() asserts the numbers of the feedback. This file
writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style


def levels(kind):
    if kind == 'parabolic':
        return np.arange(4) + 0.5
    n = np.arange(-4, 5)
    e = np.sign(n) * np.sqrt(np.abs(n))
    return e if kind == 'dirac' else e[n != 0]


def check():
    """The numbers of the feedback: the parabolic ladder at 0.5 to 3.5 in equal steps of one, the Dirac ladder at 1, 1.41,
    1.73 and 2 times E_1, with steps 0.41 and 0.32 after the first, and no level at zero in the third ladder."""
    p, d, z = levels('parabolic'), levels('dirac'), levels('nozero')
    assert np.allclose(p, [0.5, 1.5, 2.5, 3.5]) and np.allclose(np.diff(p), 1)
    pos = d[d > 0]
    assert [round(x, 2) for x in pos] == [1.0, 1.41, 1.73, 2.0]
    assert round(pos[1] - pos[0], 2) == 0.41 and round(pos[2] - pos[1], 2) == 0.32
    assert np.sum(d == 0) == 1 and np.all(z != 0) and np.allclose(np.sort(z), np.sort(d[d != 0]))
    assert np.allclose(d, -d[::-1])                                # symmetric around zero energy


def option(script, kind):
    """One picture option, with its energy axis and no other text."""
    check()
    plt.rcParams.update({'font.size': 11})
    fig, ax = plt.subplots(figsize=(3.0 * style.CM, 4.4 * style.CM))
    for e in levels(kind):
        ax.hlines(e, 0.15, 0.85, color=style.ACCENT, lw=2.2)
    ax.set_xlim(0, 1)
    if kind == 'parabolic':
        ax.set_ylim(0, 4.6)
        ax.set_yticks([0.5, 1.5, 2.5, 3.5]); ax.set_yticklabels(['0.5', '1.5', '2.5', '3.5'])
        ax.set_ylabel(r'$E/\hbar\omega_c$', labelpad=1)
    else:
        ax.set_ylim(-2.3, 2.3)
        ax.set_yticks([-2, -1, 0, 1, 2]); ax.set_yticklabels(['$-2$', '$-1$', '0', '1', '2'])
        ax.set_ylabel(r'$E/E_1$', labelpad=1)
    ax.set_xticks([])
    for s in ('top', 'right', 'bottom'):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=2.5, width=0.6, labelsize=10, pad=2)
    style.save(fig, script)
