"""Session 4, section 4.10, the Landau levels of the honeycomb lattice against the flux, computed with pyqula.

The data come from the downloadable script scripts/session04/g3_landau_fan_honeycomb.py: the magnetic supercell of 4n sites
of honeycomb_lattice_square_cell().rotate(90), with one flux quantum through the cell of area 3 sqrt(3) n, for n = 10 to
60. The argument of add_orbital_magnetic_field is the flux per unit area in units of h/e, with the bond length 1, so a
hexagon holds 3 sqrt(3)/2 = 2.60 times it. The dots are the 14 states closest to zero energy at k = 0, two per level, which
at the strongest fluxes are one point of a band and not a flat level (the widths are asserted in g3_10), and
the curves are 0 and +-sqrt(|n|) E_1 of (4.7), with E_1 = 3 sqrt(pi phi) t for hbar v = 3t/2. The unit of the field is
checked below by E_1: with the flux per unit area the lattice is within one percent of (4.7) at weak flux, while the flux
per hexagon would put it 61 percent off. The numbers of the caption are asserted below."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, readable on a phone

d = style.run_script('session04/g3_landau_fan_honeycomb.py')
phi, lev, E1, ns = d['fluxes'], d['levels'], d['E1'], d['ns']
assert ns[0] == 10 and ns[-1] == 60 and lev.shape == (51, 14)
# the zero level: two states at zero energy for every flux, one per valley
assert np.all(np.abs(lev[:, 6:8]) < 1e-3)
# the first level against E_1 = 3 sqrt(pi phi): the unit of the field of pyqula on the honeycomb lattice
first = lev[:, 8]
ratio = first / E1
print('E_1 of the lattice over (4.7):', np.round(ratio[[0, 10, -1]], 4), 'at phi', np.round(phi[[0, 10, -1]], 4))
assert abs(ratio[-1] - 1) < 0.01 and round(phi[-1], 4) == 0.0032       # phi = 0.0032, the weakest flux
assert abs(first[-1] / (3 * np.sqrt(np.pi * phi[-1] / (3 * np.sqrt(3) / 2))) - 1) > 0.5   # the flux per hexagon fails
assert np.all(ratio < 1) and np.all(np.diff(ratio) > 0)            # below (4.7), and closer at weaker flux
# the caption: at phi = 0.0096, the cell of 80 sites, the first level is 0.51 against 0.52 of (4.7)
i20 = list(ns).index(20)
print('phi', round(phi[i20], 4), 'first level', round(first[i20], 4), 'E_1', round(E1[i20], 4))
assert round(phi[i20], 4) == 0.0096 and round(first[i20], 2) == 0.51 and round(E1[i20], 2) == 0.52
# particle-hole symmetry, and every level a little below its curve, more for a higher level, the lattice correction
low = []
for m, j in ((1, 8), (2, 10), (3, 12)):
    assert np.allclose(lev[:, j], -lev[:, 13 - j], atol=1e-6)
    assert np.allclose(lev[ns >= 20, j], lev[ns >= 20, j + 1], atol=0.01)   # two states per level at weak flux
    low.append(1 - lev[:, j] / (np.sqrt(m) * E1))
low = np.array(low)
print('relative shift below (4.7) at the weakest and the strongest flux', np.round(low[:, -1], 3), np.round(low[:, 0], 3))
assert np.all(low > 0) and np.all(np.diff(low, axis=0) > 0)
# the caption: below the curves more for a stronger flux, for every dot, and at phi = 0.0192, the strongest flux, the
# two dots of n = 3 are 13 and 18 percent below. The widths of the bands there are asserted on a k-mesh in g3_10.
for m, j in ((1, 8), (2, 10), (3, 12)):
    for jj in (j, j + 1):
        assert np.all(np.diff(1 - lev[:, jj] / (np.sqrt(m) * E1)) < 0)   # phi decreases along the columns
three = 1 - lev[0, 12:14] / (np.sqrt(3) * E1[0])
print('phi', round(phi[0], 4), 'the dots of n = 3 below their curve by', np.round(three, 4))
assert round(phi[0], 4) == 0.0192 and [round(100 * s) for s in sorted(three)] == [13, 18]
# the caption: the cell has 4N sites, here the last one of the script, N = 60
assert len(d['g'].r) == 4 * ns[-1] == 240

fig, ax = plt.subplots(figsize=(9.5 * style.CM, 6.6 * style.CM))
f = np.linspace(0, 0.0205, 300)
for m in range(-3, 4):
    ax.plot(f, np.sign(m) * np.sqrt(abs(m)) * 3 * np.sqrt(np.pi * f), ls='--', color=style.MUTED, lw=0.8, zorder=1)
    if m > 0:
        style.label(ax, 0.0207, np.sqrt(m) * 3 * np.sqrt(np.pi * 0.0205), r'$%d$' % m, fontsize=9.5, color=style.MUTED,
                    ha='left')
style.label(ax, 0.0207, 0.0, r'$n=0$', fontsize=9.5, color=style.MUTED, ha='left')
for j in range(14):
    ax.plot(phi, lev[:, j], 'o', ms=2.6, color=style.ACCENT, zorder=2)
style.guide(ax, x=phi[i20], ls=':', color=style.MUTED, lw=0.8)
ax.set_xlim(0, 0.0235); ax.set_ylim(-1.3, 1.3)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
ax.set_xticks([0, 0.01, 0.02]); ax.set_xticklabels(['0', '0.01', '0.02'])
ax.set_yticks([-1, 0, 0.51, 1]); ax.set_yticklabels(['$-1$', '0', '$0.51$', '1'])
ax.tick_params(length=2.5, width=0.6, labelsize=10)
ax.set_xlabel(r'flux per unit area $\phi$, in units of $h/e$', fontsize=10.5, labelpad=2)
ax.set_ylabel(r'$E/t$', labelpad=2)
style.save(fig, __file__)
