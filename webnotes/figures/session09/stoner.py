"""Session 9, Eq. (9.8) on the half-filled square lattice, the static chi_0(q) along the path Gamma-X-M-Gamma.

Redrawn on 2026-11-22 with ticks at the two values that the caption quotes and the unit on the axis. It stays numpy, as
the plan of the session says, and the values are those of _g3_chi0path.py, the code that the picture quiz of Section
9.5b also uses. The asserts check the caption: chi_0 = 0.264/t at Gamma and 0.677/t at M at T=0.1t on the 240x240
mesh, the same from the elliptic density of states, the maximum at M, and the thresholds 1/chi_0 = 1.48t and 3.79t,
which the caption rounds to 1.5t and 3.8t. pyqula h.get_chi gives -0.6768 and -0.2636 at nk=120, the same numbers
with the sign of dn/dv, at about 5 s per q, so the path is not drawn from it."""
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import style
import _g3_chi0path as cp

pts, y, xt = cp.path(0.0, T=0.1, nk=240, step=8)
x = np.arange(len(y))
g0, gM = cp.elliptic(0.1)
assert abs(y[0] - 0.264) < 1e-3 and abs(y[xt[2]] - 0.677) < 1e-3, (y[0], y[xt[2]])
assert abs(y[0] - g0) < 1e-5 and abs(y[xt[2]] - gM) < 1e-5, (g0, gM)
assert int(np.argmax(y)) == xt[2] and pts[xt[2]] == (120, 120)          # the maximum is at M = (pi, pi)
assert round(y[xt[2]], 2) == 0.68 and round(y[0], 2) == 0.26
assert round(1 / y[xt[2]], 1) == 1.5 and round(1 / y[0], 1) == 3.8     # U of the two thresholds, 1.48 and 3.79
print('chi0 at Gamma, X, M =', y[0], y[xt[1]], y[xt[2]], ' thresholds', 1 / y[xt[2]], 1 / y[0])

FS = 10
fig, ax = plt.subplots(figsize=(12.0 * style.CM, 6.0 * style.CM))
style.arrows(ax, ticks=True)
ax.spines['bottom'].set_visible(True); ax.spines['left'].set_visible(True)
ax.annotate(r'$\chi_0(q,0)$ in units of $1/t$', xy=(0, 1.06), xycoords='axes fraction', ha='left', va='bottom',
            fontsize=FS)
ax.annotate(r'$q$', xy=(1.03, 0), xycoords='axes fraction', ha='left', va='center', fontsize=FS)
for xx in xt[1:3]:
    ax.axvline(xx, color=style.GRID, lw=0.7, zorder=0)
ax.plot(x, y, color=style.ACCENT)
style.guide(ax, y=y[0], color=style.LIGHT, ls=(0, (4, 3)), lw=1.0)
style.guide(ax, y=y[xt[2]], color=style.BROKEN, ls=(0, (4, 3)), lw=1.0)
ax.set_ylim(0, 0.85)
ax.set_xlim(0, x[-1])
ax.set_xticks(xt); ax.set_xticklabels([r'$\Gamma$', r'$X$', r'$M$', r'$\Gamma$'])
ax.set_yticks([0, y[0], y[xt[2]]]); ax.set_yticklabels(['0', '0.26', '0.68'])
ax.tick_params(labelsize=FS, length=2.5, width=0.6)
style.label(ax, 1.0, y[0] + 0.03, r'$1/U=\chi_0(0,0)$, ferromagnet', color=style.ACCENT, ha='left', va='bottom',
            fontsize=FS)
style.label(ax, xt[2] - 1.5, y[xt[2]] + 0.03, r'$1/U=\chi_0(Q,0)$, antiferromagnet', color=style.BROKEN, ha='right',
            va='bottom', fontsize=FS)
ax.plot([xt[2]], [y[xt[2]]], 'o', color=style.BROKEN, ms=4)
ax.plot([0], [y[0]], 'o', color=style.ACCENT, ms=4)
style.save(fig, __file__)
