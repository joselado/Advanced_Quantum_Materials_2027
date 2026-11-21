"""Session 2, Section 2.9, the density of states (2.16) of the square lattice, per site and for one spin.

The calculation is the pyqula script webnotes/scripts/session02/g3_square_dos.py, which the student downloads under the
figure: h.get_dos of the square lattice with the hopping -1, the sign of (2.14), t = 1, with each state a Lorentzian of
half width 0.05 on a mesh of 300 by 300 momenta. The grey line is the density of states with no broadening,
K(1 - w^2/16)/(2 pi^2) with K the complete elliptic integral, as in webnotes/conventions/session02.md. The checks
below compare the curve of pyqula with this formula broadened by the same Lorentzian, and assert the numbers of the
caption on the curve that is drawn."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from scipy.special import ellipk
import style

d = style.run_script('session02/g3_square_dos.py')
e, g = np.asarray(d['e'], float), np.asarray(d['dos'], float)
assert np.allclose(e, np.linspace(-5, 5, 501))
assert d['delta'] == 0.05 and d['nk'] == 300                        # the caption: 0.05 t and 300 by 300
inside = np.abs(e) < 4
exact = np.zeros_like(e)
exact[inside] = ellipk(np.clip(1 - e[inside] ** 2 / 16, 0, 1 - 1e-15)) / (2 * np.pi ** 2)
# the same formula broadened by the Lorentzian of half width 0.05, on a fine energy grid
dw = 8 / 160000
w = -4 + (np.arange(160000) + 0.5) * dw                               # midpoints, so that no point sits on the log at 0
gw = ellipk(1 - w ** 2 / 16) / (2 * np.pi ** 2)
broad = np.array([np.sum(0.05 / np.pi / ((x - w) ** 2 + 0.05 ** 2) * gw) * dw for x in e])
sel = (np.abs(e) > 0.3) & (np.abs(e) < 3.7)
print('largest difference to the broadened formula away from 0 and the edges', np.abs(g - broad)[sel].max())
assert np.abs(g - broad)[sel].max() < 2e-3
# one state per site, less the Lorentzian tails outside the window
area = np.trapezoid(g, e)
assert 0.98 < area < 1.0, area
# the peak is at zero energy, 0.29 with this broadening, while the formula diverges there
i0 = np.argmin(np.abs(e))
assert e[np.argmax(g)] == e[i0] == 0.0 and abs(g[i0] - 0.29) < 0.005, g[i0]
assert np.isclose(g[i0], broad[i0], atol=5e-3)
# the band edges: the formula gives 1/(4 pi) = 0.080 at +-4, the m*/2 pi hbar^2 of a parabolic band with m* = 1/2
assert np.isclose(ellipk(0.0) / (2 * np.pi ** 2), 1 / (4 * np.pi)) and abs(1 / (4 * np.pi) - 0.080) < 5e-4
assert np.allclose(g, g[::-1], atol=1e-10)                           # symmetric, eps(k + Q) = -eps(k)

fig, ax = style.figure(height_cm=5.2, width_cm=11.0)
ax.plot(e[inside], exact[inside], color=style.MUTED, lw=0.9, zorder=2)
ax.plot([-4, -4], [0, exact[inside][0]], color=style.MUTED, lw=0.9, zorder=2)
ax.plot([4, 4], [0, exact[inside][-1]], color=style.MUTED, lw=0.9, zorder=2)
ax.plot(e, g, color=style.ACCENT, zorder=3)
style.guide(ax, x=0)
style.arrows(ax, xlabel=r'$\omega/t$', ylabel=r'$g\,t$')
ax.set_xlim(-5, 5.2); ax.set_ylim(0, 0.42)
ax.set_xticks([-4, -2, 0, 2, 4]); ax.set_xticklabels([r'$-4$', r'$-2$', r'$0$', r'$2$', r'$4$'])
ax.set_yticks([0, 0.08, 0.29]); ax.set_yticklabels([r'$0$', r'$0.08$', r'$0.29$'])
ax.tick_params(length=2.5, width=0.6, labelsize=8, pad=1.5)
style.save(fig, __file__)
