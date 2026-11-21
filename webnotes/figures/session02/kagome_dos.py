"""Session 2, Section 2.11b, the bands and the density of states of the kagome lattice, H = -t sum over first neighbors.

The calculation is the pyqula script webnotes/scripts/session02/g4_kagome_bands.py, which the student downloads under
the figure: the kagome lattice with tij=[-1.], the sign of (2.5), with the bond length 1 and the lattice constant 2.
The bands are on Gamma-K-M-Gamma with K = (2/3, 1/3) and M = (1/2, 0) in reduced momenta, which are the corner
(2 pi/3, 0) and the point (pi/2, -pi/2 sqrt3) of the zone. The density of states is h.get_dos with Lorentzians of half
width 0.04 on a mesh of 200 x 200 momenta, per unit cell, summed over the three bands and for one spin. The asserts
check the numbers of the caption: the flat band at 2t, the range -4t to 2t of the other two bands, the peaks at -2t
and 0 from M, the V at -t from the crossing at K, and about three states per cell in the window."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style
import _g4_bands

d = style.run_script('session02/g4_kagome_bands.py')
bands, steps = d['bands_kagome'], d['steps']
iK, iM = steps[0], steps[0] + steps[1]
assert np.allclose(bands[:, 2], 2)                                               # the flat band at +2t
assert np.isclose(bands[:, :2].min(), -4) and np.isclose(bands[:, 1].max(), 2)   # the two others from -4t to 2t
assert np.allclose(bands[iK], [-1, -1, 2]) and np.allclose(bands[iM], [-2, 0, 2])
e, dos = np.array(d['energies']), np.array(d['dos'])
de = e[1] - e[0]
assert abs(dos.sum() * de - 3) < 0.05                                            # three states per cell, less the tails
assert abs(e[np.argmax(dos)] - 2) < 1e-9 and dos.max() > 7                       # the flat band, a narrow high peak
for E0 in (-2.0, 0.0):                                                           # the peaks from the saddle points at M
    w = np.abs(e - E0) < 0.4
    assert abs(e[w][np.argmax(dos[w])] - E0) < 0.02
w = np.abs(e + 1) < 0.4
assert abs(e[w][np.argmin(dos[w])] + 1) < 0.02 and dos[w].min() < 0.05            # the V at -t, from the crossing at K
x, kc = _g4_bands.distance(d['g'], d['kpath'])
assert np.allclose(kc[iK], [2 * np.pi / 3, 0]) and np.allclose(kc[iM], [np.pi / 2, -np.pi / (2 * np.sqrt(3))])
xt = [x[0], x[iK], x[iM], x[-1]]

fig = plt.figure(figsize=(12.5 * style.CM, 6.6 * style.CM))
gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1.0], wspace=0.12)
axb, axd = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
for j in range(3):
    axb.plot(x, bands[:, j], color=style.BROKEN if j == 2 else style.ACCENT, lw=2.2 if j == 2 else 1.8)
for xv in xt:
    style.guide(axb, x=xv)
style.arrows(axb, ylabel=r'$\epsilon$ in units of $t$', ticks=True)
axb.set_xticks(xt); axb.set_xticklabels([r'$\Gamma$', r'$K$', r'$M$', r'$\Gamma$'])
axb.set_yticks([-4, -2, -1, 0, 2]); axb.set_yticklabels([r'$-4$', r'$-2$', r'$-1$', '0', '2'])
axb.tick_params(labelsize=10, length=2.5)
axb.spines['left'].set_visible(True)
axb.set_xlim(0, xt[-1]); axb.set_ylim(-4.6, 2.9)
cut = 1.0
shown = np.minimum(dos, cut)
axd.fill_betweenx(e, 0, shown, color=style.LIGHT, alpha=0.35, lw=0)
axd.plot(shown, e, color=style.ACCENT, lw=1.2)
flat = dos > cut
axd.plot(shown[flat], e[flat], color=style.BROKEN, lw=2.2)
for yv in (-4, -2, -1, 0, 2):
    style.guide(axd, y=yv)
style.arrows(axd, ticks=True)
axd.set_xlabel(r'$g(\epsilon)$, states per cell and per $t$', fontsize=9.5, labelpad=2)
axd.set_ylim(axb.get_ylim()); axd.set_xlim(0, cut * 1.05)
axd.set_yticks([]); axd.set_xticks([0, 0.5]); axd.set_xticklabels(['0', '0.5'])
axd.tick_params(labelsize=10, length=2.5)
axd.spines['bottom'].set_visible(True)
axd.annotate('flat band,\none third\nof the states', xy=(cut * 0.97, 1.95), xytext=(cut * 0.80, 1.0),
             fontsize=9.5, color=style.BROKEN, ha='center', va='center', linespacing=1.15,
             arrowprops=dict(arrowstyle='-', color=style.BROKEN, lw=0.8))
style.save(fig, __file__)
