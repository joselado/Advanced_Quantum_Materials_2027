"""Shared code of the picture options of the quiz of Section 6.14 on the one-magnon band of a ferromagnetic ring. This
file writes no figure.

The question gives the bosonic tight-binding Hamiltonian of a ring, the hopping -|J|S and the onsite energy 2|J|S,
with S = 1 and |J| = 1, so the band is E = 2|J|S (1 - cos k), with the largest value 4|J|S = 4 at k = pi. The three
pictures are this closed form for the spin S = 1/2, 1 and 2, which reach 2, 4 and 8, so numpy and no pyqula: the
band is the one that the problem of the page derives, and pyqula has no spin operators. A picture has the axes k and
E/|J|, the ticks -pi, 0, pi on k and 0, 2, 4, 8 on the energy, the same scale in the three, one color and no other
text, so that the answer is read from the height of the band alone. The asserts check every number of the feedback."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

K = np.linspace(-np.pi, np.pi, 401)
SPIN = {'w2': 0.5, 'w4': 1.0, 'w8': 2.0}


def band(S, k, J=1.0):
    """The one-magnon band of a ferromagnetic ring, E = 2|J|S (1 - cos k)."""
    return 2 * abs(J) * S * (1 - np.cos(k))


def check():
    """The numbers of the question and of the feedback."""
    S, J = 1.0, 1.0
    onsite, hop = 2 * abs(J) * S, -abs(J) * S                     # the bosonic Hamiltonian of the question
    tb = onsite + hop * 2 * np.cos(K)                                # onsite plus a hop to the two neighbors
    assert np.allclose(tb, band(S, K)) and np.isclose(tb.max(), 4) and np.isclose(tb[np.argmax(tb)], 4)
    assert np.isclose(abs(K[np.argmax(tb)]), np.pi) and np.isclose(tb.min(), 0) and np.isclose(K[np.argmin(tb)], 0, atol=1e-9)
    tops = {name: band(S_, np.pi) for name, S_ in SPIN.items()}
    assert np.allclose([tops['w2'], tops['w4'], tops['w8']], [2, 4, 8])   # the three maxima, 4|J|S for S = 1/2, 1, 2
    assert all(np.isclose(band(S_, 0.0), 0) for S_ in SPIN.values())     # every band starts at zero, the Goldstone mode


def option(script, name):
    """One picture option, the band of the spin SPIN[name] against k."""
    check()
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 4.2 * style.CM))
    for y in (2, 4, 8):
        ax.axhline(y, color=style.GRID, lw=0.8, zorder=0)
    ax.plot(K, band(SPIN[name], K), color=style.ACCENT, lw=1.6)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(0, 8.8)
    ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=11)
    ax.set_yticks([0, 2, 4, 8]); ax.set_yticklabels(['0', '2', '4', '8'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$k$', fontsize=12, labelpad=0)
    ax.set_ylabel(r'$E/|J|$', fontsize=12, labelpad=2)
    style.save(fig, script)
