"""Session 7, the number of coefficients of the exact state (7.4) and of a matrix product state (7.5).

Redrawn on 2026-11-22 under the same name, with a logarithmic axis that has its powers of ten and ticks at the
sizes L=26 and L=30 that the caption quotes. The curves are the same as before: 2^L for the exact state and L M^2,
without the factor d=2, for the MPS with M=16 and M=64. Since 2026-11-22, the pick of the lecturer, the labels write the
bond dimension as chi, and the variable M of the code stays."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

L = np.arange(1, 51)
exact = 2.0 ** L
mps = {M: L * M ** 2.0 for M in (16, 64)}
per_gb = 1e9 / 16                               # 16 bytes per complex number, so 1 GB (1e9 bytes) is 6.25e7 coefficients

# the caption: the exact state crosses the line of one gigabyte at L=26, the first size above it
assert 2.0 ** 25 < per_gb < 2.0 ** 26
assert int(L[np.argmax(exact > per_gb)]) == 26
# the caption says "about seventeen gigabytes" at L=30 since 2026-11-22, in place of the old "sixteen": 2^30 numbers of
# 16 bytes are sixteen in units of 2^30 bytes, but 17.2 in units of 1e9 bytes, the unit of the dashed line, and
# 1.72e10 bytes is the value of the first quiz of the page
bytes_per_number = 16                           # numpy complex128
assert np.dtype(np.complex128).itemsize == bytes_per_number
at30 = float(exact[L == 30][0]) * bytes_per_number      # the bytes of the drawn curve at its dot, L=30
assert at30 / 2 ** 30 == 16 and round(at30 / 1e9, 1) == 17.2 and abs(at30 / 1e10 - 1.72) < 0.005
# about seventeen gigabytes of the caption, by two routes: the bytes over 1e9, and the coefficients of the drawn curve over
# the coefficients of one gigabyte of the dashed line
assert round(at30 / 1e9) == 17 and round(float(exact[L == 30][0]) / per_gb) == 17
# the MPS curves stay far below the line over the whole range, which is the almost flat curve of the caption, and
# they would with the factor 2 of the two spin values too, which the caption says they leave out
assert max(mps[64]) < per_gb / 100 and 2 * max(mps[64]) < per_gb / 100

fig, ax = style.figure(height_cm=6.6, width_cm=12.0)
ax.set_yscale('log')
ax.plot(L, exact, color=style.ACCENT)
ax.plot(L, mps[16], color=style.BROKEN)
ax.plot(L, mps[64], color=style.LIGHT)
ax.set_xlim(0, 52); ax.set_ylim(1, 10 ** 16.5)
style.guide(ax, y=per_gb, linestyle=(0, (3, 3)))
style.label(ax, 1.5, per_gb * 4, '1 GB', ha='left', fontsize=11, color=style.MUTED)
ax.plot([30], [2.0 ** 30], 'o', color=style.ACCENT, ms=4)
style.label(ax, 17, 10 ** 13.6, r'exact state, $2^L$', color=style.ACCENT, ha='left', fontsize=11)
style.label(ax, 51, 10 ** 6.6, r'MPS, $L\chi^2$ with $\chi=64$', color=style.LIGHT, ha='right', fontsize=11)
style.label(ax, 51, 10 ** 2.1, r'MPS, $L\chi^2$ with $\chi=16$', color=style.BROKEN, ha='right', fontsize=11)
ax.set_xticks([10, 20, 26, 30, 40, 50])
ax.set_yticks([10.0 ** k for k in (0, 3, 6, 9, 12, 15)])
ax.set_yticklabels([r'$10^{%d}$' % k for k in (0, 3, 6, 9, 12, 15)])
ax.yaxis.set_minor_locator(plt.NullLocator())
ax.tick_params(axis='both', length=2.5, pad=2, labelsize=11)
style.arrows(ax, xlabel=r'$L$', ylabel=r'number of coefficients', ticks=True)
style.save(fig, __file__)
