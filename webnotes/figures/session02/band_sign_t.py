"""Session 2, section 2.5, the chain band for t=+1 and t=-1, in the feedback of a quiz.

The two bands come from the pyqula script webnotes/scripts/session02/g2_chain_second_neighbor.py, the band of eta=0
with tij=[-1.], which is t=+1 in the sign of (2.5), and the band with tij=[1.], which is t=-1. The energy is in units
of |t|, since t changes sign between the two curves."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

d = style.run_script('session02/g2_chain_second_neighbor.py')
p, up, down = d['phi'], d['bands'][0.0], d['band_negative_t']
assert np.allclose(up, -2 * np.cos(p)) and np.allclose(down, 2 * np.cos(p))   # -2t cos(phi) for t=+1 and t=-1
i0 = np.argmin(np.abs(p))
assert np.isclose(up[i0], -2) and np.isclose(down[i0], 2)                     # the caption: -2 and +2 at phi=0
assert np.isclose(down[0], -2) and np.isclose(down[-1], -2)                   # for t=-1 the bottom is at phi=pi

fig, ax = style.figure(height_cm=4.2, width_cm=9.6)
ax.plot(p, up, color=style.ACCENT)
ax.plot(p, down, color=style.BROKEN)
style.guide(ax, y=0)
style.arrows(ax, xlabel=r'$\varphi$', ylabel=r'$\epsilon/|t|$')
ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-2.8, 2.8)
ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', r'$0$', r'$\pi$'])
ax.set_yticks([-2, 0, 2]); ax.set_yticklabels(['$-2$', '$0$', '$2$'])
ax.tick_params(length=2.5, labelsize=9)
ax.spines['bottom'].set_visible(True); ax.spines['left'].set_visible(True)
ax.scatter([0, 0], [-2, 2], s=16, color=style.INK, zorder=5)
style.label(ax, -2.4, 2.45, r'$t=+1$', color=style.ACCENT, fontsize=9)
style.label(ax, -2.4, -2.45, r'$t=-1$', color=style.BROKEN, fontsize=9)
style.save(fig, __file__)
