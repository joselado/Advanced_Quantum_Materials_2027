"""Small plots of a memory in bytes against the number of spins L, the picture options of a quiz of Section 10.3a.

Three curves on the same logarithmic axis: the table of the 2^L complex coefficients of (10.2), 16 x 2^L bytes, which
is a straight line, a power 16 x L^4, which bends down, and the matrix product state with d=2 and D=10, 16 L d D^2
bytes, which is almost flat. Arithmetic and not a pyqula calculation, so numpy and no button. The axes and their
ticks are the same in the three pictures, and nothing else is written on them. The numbers of the feedback are
asserted here and in checks/session10/g2_03_*.py. This file writes no figure, the scripts g2_quiz_memory_*.py call
draw."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from matplotlib.ticker import FixedLocator, LogLocator, NullFormatter
import style

L = np.linspace(1, 40, 200)
CURVES = {
    'table': 16 * 2.0 ** L,
    'power': 16 * L ** 4,
    'mps': 16 * L * 2 * 10 ** 2,
}
assert 16 * 2.0 ** 29 < 16e9 < 16 * 2.0 ** 30 and 16 * 2.0 ** 35 < 1e12 < 16 * 2.0 ** 36   # passes at 30 and 36
assert round(16 * 40 ** 4 / 1e7, 1) == 4.1 and round(16 * 40 * 2 * 100 / 1e5, 1) == 1.3
assert round(16 * 2.0 ** 40 / 1e13, 1) == 1.8


def draw(script, kind):
    """Writes the picture of one curve, 'table', 'power' or 'mps'."""
    fig, ax = style.plt.subplots(figsize=(4.4 * style.CM, 4.4 * style.CM))
    style.arrows(ax, xlabel=r'$L$', ylabel='bytes', ticks=True)
    ax.semilogy(L, CURVES[kind], color=style.ACCENT, lw=2.0)
    ax.set_xlim(0, 42); ax.set_ylim(1e1, 1e15)
    ax.set_xticks([0, 20, 40])
    ax.yaxis.set_major_locator(FixedLocator([1e2, 1e8, 1e14]))
    ax.yaxis.set_minor_locator(LogLocator(base=10, subs=(1.0,), numticks=30))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(which='both', direction='out', length=3, width=0.6, labelsize=10)
    ax.tick_params(which='minor', length=1.6)
    for t in ax.texts:
        t.set_fontsize(10)
    style.save(fig, script)
