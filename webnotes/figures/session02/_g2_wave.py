"""Shared code of the picture options of the quiz of Section 2.6, which wave is the same state as cos(0.5 x) on the
sites x = n of a chain with a = 1.

numpy, since the pictures sample cosines and have no Hamiltonian. Each picture shows the dots cos(0.5 n) on the sites
n = 0 to 6 and one wave, with the same axes and no other text. The feedback quotes cos(2) = -0.42 against cos(1) = 0.54
for the wave cos(1.0 x), and -0.88 against 0.88 at x = 1 for the wave cos[(0.5 + pi) x], asserted here. This file
writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

K0 = 0.5
WAVES = {'2pi': K0 + 2 * np.pi, 'pi': K0 + np.pi, 'one': 1.0}


def option(script, name):
    """One picture option, the dots of cos(0.5 n) and the wave cos(k x) with k = WAVES[name]."""
    n = np.arange(7)
    dots = np.cos(K0 * n)
    assert np.allclose(np.cos(WAVES['2pi'] * n), dots)                              # the same on every site
    assert np.allclose(np.cos(WAVES['pi'] * n), (-1) ** n * dots)                   # the sign flips on odd sites
    assert np.isclose(np.cos(WAVES['pi'] * 1), -0.88, atol=0.005) and np.isclose(dots[1], 0.88, atol=0.005)
    assert np.isclose(np.cos(WAVES['one'] * 2), -0.42, atol=0.005) and np.isclose(dots[2], 0.54, atol=0.005)
    for k in (WAVES['one'], -WAVES['one']):                                         # 1.0 -+ 0.5 is no multiple of 2 pi
        assert min(abs((k - K0) / (2 * np.pi) - np.round((k - K0) / (2 * np.pi))), 0.5) > 0.05
    x = np.linspace(-0.1, 6.3, 2000)
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.6 * style.CM))
    ax.plot(x, np.cos(WAVES[name] * x), color=style.BROKEN, lw=1.1, zorder=2)
    ax.scatter(n, dots, s=22, color=style.INK, zorder=5, clip_on=False)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.axhline(0, color=style.GRID, lw=0.8, zorder=0)
    ax.set_xlim(-0.3, 6.4); ax.set_ylim(-1.15, 1.15)
    ax.set_xticks([0, 2, 4, 6]); ax.set_xticklabels(['0', '2', '4', '6'], fontsize=11)
    ax.set_yticks([-1, 0, 1]); ax.set_yticklabels(['$-1$', '$0$', '$1$'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$x/a$', fontsize=12, labelpad=0); ax.set_ylabel(r'$\psi$', fontsize=12, labelpad=0)
    style.save(fig, script)
