"""Shared code of the picture options of the quiz of Section 1.11b on the magnon with an easy-axis anisotropy. This
file writes no figure.

The three pictures are the closed forms of gapless_gapped.py, so numpy and no pyqula: the magnon of a ferromagnetic
chain, omega = 1 - cos k, the same with the gap 0.45 of an easy-axis anisotropy, omega = 1 - cos k + 0.45, and the
phonon of a chain of masses, omega = 2|sin(k/2)|. The momentum k is in units of the inverse lattice constant and omega
in the arbitrary units of gapless_gapped.svg. A picture has the axes k and omega, with the ticks 0, 0.45 and 2 on
omega, the same scale in the three, one color and no other text, so that the answer is read from the curve alone. The
asserts check every number that the feedback quotes: the value at k = 0, and the linear and the quadratic rise."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

GAP = 0.45
K = np.linspace(-np.pi, np.pi, 501)
CURVES = {
    'magnon': lambda k: 1 - np.cos(k),
    'magnon_gap': lambda k: 1 - np.cos(k) + GAP,
    'phonon': lambda k: 2 * np.abs(np.sin(k / 2)),
}


def check():
    """The numbers of the feedback: the values at k = 0 and at the zone edge, and the shape at small k."""
    f = CURVES
    assert f['magnon'](0.0) == 0 and np.isclose(f['magnon_gap'](0.0), 0.45) and f['phonon'](0.0) == 0
    assert np.isclose(f['magnon'](np.pi), 2) and np.isclose(f['magnon_gap'](np.pi), 2.45) and np.isclose(f['phonon'](np.pi), 2)
    q = 1e-3                                                        # small k: the phonon is linear, the magnon quadratic
    assert np.isclose(f['phonon'](q) / q, 1, atol=1e-6) and np.isclose(f['magnon'](q) / q ** 2, 0.5, atol=1e-6)
    assert np.isclose(f['magnon_gap'](q) - GAP, f['magnon'](q))      # the gap shifts the whole curve by 0.45
    assert np.all(f['magnon_gap'](K) >= GAP - 1e-12)                 # and it is the lowest value of the curve


def option(script, name):
    """One picture option, the curve of name against k."""
    check()
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 4.2 * style.CM))
    ax.axhline(0, color=style.GRID, lw=0.8, zorder=0)
    ax.plot(K, CURVES[name](K), color=style.ACCENT, lw=1.6)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-0.08, 2.6)
    ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=11)
    ax.set_yticks([0, GAP, 2]); ax.set_yticklabels(['0', '0.45', '2'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$k$', fontsize=12, labelpad=0)
    ax.set_ylabel(r'$\omega$', fontsize=12, labelpad=2, rotation=0, va='center')
    style.save(fig, script)
