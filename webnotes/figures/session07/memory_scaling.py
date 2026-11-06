"""Session 7, the number of coefficients of the exact state (7.4) and of a matrix product state (7.5)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

L = np.arange(1, 51)
fig, ax = style.figure(height_cm=5.6)
ax.plot(L, np.log10(2.0 ** L), color=style.ACCENT)
for M, col in ((16, style.BROKEN), (64, style.LIGHT)):
    ax.plot(L, np.log10(L * M ** 2.0), color=col)
ax.set_xlim(0, 52); ax.set_ylim(0, 16.5)
# 16 bytes per complex number, so 1 GB is 6.25e7 coefficients
gb = np.log10(1e9 / 16)
style.guide(ax, y=gb, linestyle=(0, (3, 3)))
style.label(ax, 3, gb + 0.6, '1 GB', ha='left', fontsize=8.5, color=style.MUTED)
style.arrows(ax, xlabel=r'$L$', ylabel=r'$\log_{10}$ of the number of coefficients')
style.label(ax, 39, 13.2, r'exact state, $2^L$', color=style.ACCENT, ha='right', fontsize=8.5)
style.label(ax, 51, 6.3, r'MPS, $LM^2$ with $M=64$', color=style.LIGHT, ha='right', fontsize=8.5)
style.label(ax, 51, 2.8, r'MPS, $LM^2$ with $M=16$', color=style.BROKEN, ha='right', fontsize=8.5)
ax.plot([30], [np.log10(2.0 ** 30)], 'o', color=style.ACCENT, ms=4)
style.label(ax, 29, 10.6, r'$L=30$', ha='right', fontsize=8.5)
style.save(fig, __file__)
