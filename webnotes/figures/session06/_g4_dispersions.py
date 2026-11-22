"""Shared code of the picture options of the quiz of Section 6.15 on the magnon of the antiferromagnetic chain near
k = 0. This file writes no figure.

The question gives the Heisenberg chain with J > 0 and S = 1/2. The three pictures are closed forms of linear
spin-wave theory, so numpy and no pyqula: the antiferromagnetic band (6.9) of the chain, E = 2JS|sin k| = |sin k|,
the ferromagnetic band (6.8) of the same chain with J = -1, E = 2|J|S (1 - cos k) = 1 - cos k, and the same parabola
lifted by a gap of 0.2, which linear spin-wave theory of a Heisenberg magnet does not give. The momentum k is in units of the inverse lattice constant and
the window is -1 < k < 1, around the zone center. A picture has the axes k and E/|J|, the ticks -1, 0, 1 on k and 0,
0.2, 1 on the energy, the same scale in the three, one color and no other text, so that the answer is read from the
shape near k = 0. The asserts check every number that the feedback quotes."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

GAP = 0.2
J, S = 1.0, 0.5
K = np.linspace(-1, 1, 401)
CURVES = {
    'afm': lambda k: J * S * 2 * np.sqrt(1 - np.cos(k) ** 2),          # (6.9), z = 2, gamma = cos k
    'fm': lambda k: abs(J) * S * 2 * (1 - np.cos(k)),                   # (6.8), z = 2, for J = -1
    'gapped': lambda k: abs(J) * S * 2 * (1 - np.cos(k)) + GAP,
}


def check():
    """The numbers of the feedback: the values at k = 0, the cone and the parabola at small k."""
    f = CURVES
    assert np.allclose(f['afm'](K), np.abs(np.sin(K))) and np.allclose(f['fm'](K), 1 - np.cos(K))
    assert f['afm'](0.0) == 0 and f['fm'](0.0) == 0 and np.isclose(f['gapped'](0.0), 0.2)
    assert np.all(f['gapped'](K) >= GAP - 1e-12) and np.all(f['afm'](K) >= 0) and np.all(f['fm'](K) >= 0)
    q = 1e-4                                                         # the cone has the slope 2JS = 1, the parabola none
    assert np.isclose(f['afm'](q) / q, 2 * J * S, rtol=1e-6) and np.isclose(f['fm'](q) / q ** 2, abs(J) * S, rtol=1e-6)
    assert np.isclose(round(f['fm'](0.1), 3), 0.005) and np.isclose(round(f['fm'](0.2), 3), 0.020)   # the parabola
    assert 3.9 < f['fm'](0.2) / f['fm'](0.1) < 4.0                                                    # four times more
    assert f['afm'](K).max() < 1 and f['gapped'](K).max() < 1                                         # inside the window


def option(script, name):
    """One picture option, the curve of name against k."""
    check()
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 4.2 * style.CM))
    for y in (GAP, 1.0):
        ax.axhline(y, color=style.GRID, lw=0.8, zorder=0)
    ax.plot(K, CURVES[name](K), color=style.ACCENT, lw=1.6)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(-1, 1); ax.set_ylim(0, 1.08)
    ax.set_xticks([-1, 0, 1]); ax.set_xticklabels([r'$-1$', '0', '1'], fontsize=11)
    ax.set_yticks([0, GAP, 1]); ax.set_yticklabels(['0', '0.2', '1'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$k$', fontsize=12, labelpad=0)
    ax.set_ylabel(r'$E/|J|$', fontsize=12, labelpad=2)
    style.save(fig, script)
