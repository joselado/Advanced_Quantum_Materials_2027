"""Shared code of the picture options of the quiz on the Stoner criterion, Section 6.6.

Each option draws the model f(m) = tanh(s m) of the right-hand side of the self-consistency condition m = f(m), with
the slope s = U D(E_F) at m=0, against the dashed line y = m. The slopes are 0.5, 1 and 1.5. The model is the shape of
panel (a) of Figure 6.1, and it is not a calculation of pyqula, so the pictures are numpy. check() holds the numbers of
the feedback, the crossing m0 = 0.86 for s = 1.5 and the values f(0.5) = 0.24 and 0.46 for s = 0.5 and 1. This file
writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from scipy.optimize import brentq
import matplotlib.pyplot as plt
import style

SLOPES = {'low': 0.5, 'none': 1.0, 'high': 1.5}


def f(m, s):
    return np.tanh(s * m)


def check():
    """The numbers of the feedback of the three options."""
    m = np.linspace(1e-4, 1.3, 20000)
    for s in (0.5, 1.0):
        assert np.all(f(m, s) < m), s                       # no crossing for m > 0, only m = 0
    assert np.any(f(m, 1.5) > m) and np.any(f(m, 1.5) < m)     # the curve starts above y = m and comes back under it
    m0 = brentq(lambda x: f(x, 1.5) - x, 0.1, 1.2)
    assert round(m0, 2) == 0.86, m0
    assert round(f(0.5, 0.5), 2) == 0.24 and round(f(0.5, 1.0), 2) == 0.46, (f(0.5, 0.5), f(0.5, 1.0))
    for s in SLOPES.values():                                  # the slope at m = 0 is s
        assert abs((f(1e-6, s) - f(-1e-6, s)) / 2e-6 - s) < 1e-6
    return m0


def option(script, which):
    """One picture option, with the same axes for the three."""
    check()
    s = SLOPES[which]
    m = np.linspace(-1.2, 1.2, 400)
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    ax.axhline(0, color=style.GRID, lw=0.7, zorder=0)
    ax.axvline(0, color=style.GRID, lw=0.7, zorder=0)
    ax.plot(m, m, color=style.MUTED, lw=1.0, ls=(0, (3, 2)))
    ax.plot(m, f(m, s), color=style.ACCENT, lw=1.6)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
    ax.set_xticks([-1, 0, 1]); ax.set_xticklabels([r'$-1$', '0', '1'], fontsize=11)
    ax.set_yticks([-1, 0, 1]); ax.set_yticklabels([r'$-1$', '0', '1'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$m$', fontsize=12, labelpad=0); ax.set_ylabel(r'$f(m)$', fontsize=12, labelpad=-4)
    style.save(fig, script)
