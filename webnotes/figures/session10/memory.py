"""Session 10, the memory of the table of 2^L complex coefficients of Eq. (10.2) against an MPS with D=10.

Decimal units, 1 GB = 1e9 bytes and 1 TB = 1e12 bytes, 16 bytes for a complex number in double precision. The marks
are the largest L that 16 GB and 1 TB hold, and the value of the MPS at L=300 of the caption is computed here and
not drawn, since the plot ends at L=60. The numbers are asserted again in checks/session10/g2_03_*.py."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
from matplotlib.ticker import FixedLocator, LogLocator, NullFormatter
import style

L = np.arange(2, 61)
table = 2.0 ** L * 16                     # bytes, complex double
D, d = 10, 2
mps = L * d * D ** 2 * 16.0


def largest(limit):
    return int(L[table <= limit].max())


L16, L1T = largest(16e9), largest(1e12)
assert (L16, L1T) == (29, 35), (L16, L1T)
assert 300 * d * D ** 2 * 16 == 960000 < 1e6, 'the MPS at L=300 of the caption'
assert 312 * d * D ** 2 * 16 < 1e6 < 313 * d * D ** 2 * 16
assert round(2.0 ** 40 * 16 / 1e13, 1) == 1.8

fig, ax = style.figure(height_cm=6.0, width_cm=10.5)
style.arrows(ax, xlabel=r'$L$', ylabel='memory in bytes', ticks=True)
ax.semilogy(L, table, color=style.BROKEN)
ax.semilogy(L, mps, color=style.ACCENT)
ax.set_xlim(0, 62); ax.set_ylim(1e2, 1e19)
ax.set_xticks([0, 10, 20, 30, 40, 50, 60])
ax.yaxis.set_major_locator(FixedLocator([1e3, 1e6, 1e9, 1e12, 1e15, 1e18]))
ax.yaxis.set_minor_locator(LogLocator(base=10, subs=(1.0,), numticks=30))
ax.yaxis.set_minor_formatter(NullFormatter())
ax.tick_params(which='both', direction='out', length=3, width=0.6)
ax.tick_params(which='minor', length=1.8)
for y, s in ((16e9, '16 GB, a laptop'), (1e12, '1 TB, a large node')):
    style.guide(ax, y=y, ls=(0, (4, 3)))
    style.label(ax, 1, y * 3.0, s, color=style.MUTED, fontsize=7.5, ha='left')
for Lm, dx, dy in ((L16, -1.2, 6.0), (L1T, -1.2, 6.0)):
    ax.plot([Lm], [2.0 ** Lm * 16], 'o', mfc='white', mec=style.BROKEN, mew=1.2, ms=4.5, zorder=4)
    style.label(ax, Lm + dx, 2.0 ** Lm * 16 * dy, r'$L=%d$' % Lm, color=style.BROKEN, fontsize=8, ha='right')
ax.plot([40], [2.0 ** 40 * 16], 'o', color=style.BROKEN, ms=4, zorder=4)
style.label(ax, 42, 2.0 ** 40 * 16 / 60, r'$L=40$, $1.8\times10^{13}$ bytes', color=style.BROKEN, fontsize=8,
            ha='left')
style.label(ax, 50, 1.2e7, r'MPS, $D=10$', color=style.ACCENT, fontsize=8)
style.label(ax, 40, 3e16, r'table, $2^L$ numbers', color=style.BROKEN, fontsize=8, ha='right')
print('largest L in 16 GB and 1 TB:', L16, L1T, ' MPS at L=300:', 300 * d * D ** 2 * 16, 'bytes')
style.save(fig, __file__)
