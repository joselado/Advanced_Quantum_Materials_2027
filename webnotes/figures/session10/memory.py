"""Session 10, the memory of the table of 2^L complex coefficients of Eq. (10.2) against an MPS with D=10."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

L = np.arange(2, 61)
table = 2.0 ** L * 16                     # bytes, complex double
D, d = 10, 2
mps = L * d * D ** 2 * 16.0
fig, ax = style.figure(height_cm=5.6, width_cm=10.5)
ax.semilogy(L, table, color=style.BROKEN)
ax.semilogy(L, mps, color=style.ACCENT)
ax.set_xlim(0, 62); ax.set_ylim(1e2, 1e19)
style.arrows(ax, xlabel=r'$L$', ylabel='bytes')
for y, s in ((16e9, '16 GB, a laptop'), (1e12, '1 TB, a large node')):
    style.guide(ax, y=y, ls=(0, (4, 3)))
    style.label(ax, 61, y * 2.2, s, color=style.MUTED, fontsize=7.5, ha='right')
ax.plot([40], [2.0 ** 40 * 16], 'o', color=style.BROKEN, ms=4)
style.label(ax, 39.2, 2.0 ** 40 * 16 * 25, r'$L=40$, $1.8\times10^{13}$ bytes', color=style.BROKEN, fontsize=8, ha='right')
style.label(ax, 50, 1.2e7, r'MPS, $D=10$', color=style.ACCENT, fontsize=8)
style.label(ax, 21, 1e13, r'table, $2^L$ numbers', color=style.BROKEN, fontsize=8, ha='right')
for x in (10, 20, 30, 40, 50, 60):
    style.label(ax, x, 3.5e1, str(x), fontsize=7.5)
print('table L=30,36,40:', 2.0**30*16, 2.0**36*16, 2.0**40*16, ' mps L=100:', 100*2*100*16)
style.save(fig, __file__)
