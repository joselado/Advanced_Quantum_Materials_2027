"""Session 2, Section 2.11a, the density of states of graphene, a new figure of the web notes.

The calculation is the pyqula script webnotes/scripts/session02/g4_graphene_dos.py, which the student downloads under
the figure. It is the call of the notebook cell "Density of states of the honeycomb lattice": the spinless honeycomb
lattice with the hopping +1, every level a Lorentzian of half width 0.04 on a mesh of 200 x 200 momenta. pyqula counts
per unit cell, summed over the two bands, and for one spin. The asserts check what the caption states: two states per
cell in the window less the tails, the value 0.04 at zero energy where the V of the cones is rounded, the peaks at +-t,
a density that grows in proportion to |E| close to zero, and no states beyond +-3t but the tails."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

d = style.run_script('session02/g4_graphene_dos.py')
e, dos = np.array(d['e']), np.array(d['dos'])
assert abs(d['states'] - 1.98) < 0.01                                   # two states per cell, less the tails
i0 = np.argmin(np.abs(e))
assert abs(e[i0]) < 1e-9 and abs(dos[i0] - 0.04) < 0.002 and dos[i0] == dos[np.abs(e) < 0.5].min()
ip, im = np.argmax(np.where(e > 0, dos, 0)), np.argmax(np.where(e < 0, dos, 0))
assert abs(e[ip] - 1) < 0.015 and abs(e[im] + 1) < 0.015                # the van Hove peaks at +-t
ratio = [dos[np.argmin(np.abs(e - E))] / E for E in (0.3, 0.4, 0.5)]
assert max(ratio) / min(ratio) < 1.03                                   # proportional to |E| between 0.3t and 0.5t
assert dos[np.abs(e) > 3.2].max() < 0.02                                # only the tails of the Lorentzians beyond 3t
assert np.allclose(dos, dos[::-1], atol=1e-6)                           # the same for E and -E

fig, ax = style.figure(height_cm=5.2, width_cm=11.0)
ax.fill_between(e, 0, dos, color=style.LIGHT, alpha=0.35, lw=0)
ax.plot(e, dos, color=style.ACCENT, lw=1.6)
for xv in (-1, 1):
    style.guide(ax, x=xv)
style.arrows(ax, xlabel=r'$E/t$', ylabel=r'$g(E)$, states per cell and per $t$', ticks=True)
ax.set_xlim(-3.5, 3.5); ax.set_ylim(0, 0.8)
ax.set_xticks([-3, -1, 0, 1, 3]); ax.set_xticklabels([r'$-3$', r'$-1$', '0', '1', '3'])
ax.set_yticks([0, 0.5]); ax.set_yticklabels(['0', '0.5'])
ax.tick_params(labelsize=9, length=2.5)
ax.spines['left'].set_visible(True); ax.spines['bottom'].set_visible(True)
style.save(fig, __file__)
