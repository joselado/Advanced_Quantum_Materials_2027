"""Session 4, section 4.9, the Landau levels of the square lattice against the flux per plaquette, computed with pyqula.

The data come from the downloadable script scripts/session04/g3_landau_fan_square.py: the bulk magnetic cell of q sites
along y with one flux quantum, so the flux per plaquette is phi = 1/q for q = 10 to 60, with the hopping -1 and the band
bottom at -4. The dots are those of the six lowest levels at k = 0 that lie below -2.5, so one at the flux 0.1 and six
from q = 42 on, and the dashed lines are the continuum levels
-4 + 4 pi phi (n + 1/2) of (4.6), with hbar omega_c = 4 pi phi t. The numbers of the caption are asserted below."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, readable on a phone

d = style.run_script('session04/g3_landau_fan_square.py')
phi, lev, cont, qs = d['fluxes'], d['levels'], d['continuum'], d['qs']
assert qs[0] == 10 and qs[-1] == 60 and lev.shape == (51, 6)
assert np.all(lev <= cont + 1e-9)                                   # every lattice level sits below its line
# the caption: at phi = 1/20 the two lowest levels are -3.70 and -3.12, the lines -3.69 and -3.06
i20 = list(qs).index(20)
print('phi = 1/20:', np.round(lev[i20, :2], 3), 'lines', np.round(cont[i20, :2], 3))
assert np.allclose(np.round(lev[i20, :2], 2), [-3.70, -3.12]) and np.allclose(np.round(cont[i20, :2], 2), [-3.69, -3.06])
# the caption: the dots fall below the lines more when n grows and when the flux grows, the lattice correction
dev = cont - lev
print('deviation at phi = 0.1', np.round(dev[0], 3), 'at phi = 1/60', np.round(dev[-1], 4))
assert np.all(np.diff(dev, axis=1) > 0)                             # larger for a higher level, at every flux
assert np.all(np.diff(dev, axis=0) < 0)                             # larger for a stronger flux, phi decreases with q
# and the second order of the conventions sheet, -(pi phi)^2 t (2n^2+2n+1)/2, holds to 2e-3 for phi <= 1/40 and n <= 3
n = np.arange(4)
second = -4 + 4 * np.pi * np.outer(phi, n + 0.5) - np.outer((np.pi * phi) ** 2, 2 * n ** 2 + 2 * n + 1) / 2
assert np.abs(second - lev[:, :4])[qs >= 40].max() < 2e-3

EMIN, ETOP, EMAX = -4.05, -2.5, -2.3                    # the data stop at ETOP, the indices sit above it
# the caption: the dots are the levels below -2.5 t, up to six, and at phi = 0.1 only one is left
drawn = (lev < ETOP).sum(axis=1)
print('dots drawn per column, q = 10 to 60:', drawn)
assert ETOP == -2.5 and drawn[0] == 1 and qs[0] == 10 and drawn.max() == 6 and np.all(np.diff(drawn) >= 0)
assert np.all(drawn[qs >= 42] == 6) and np.all(drawn[qs < 42] < 6)

fig, ax = plt.subplots(figsize=(9.5 * style.CM, 6.6 * style.CM))
for n in range(6):
    fend = min(0.105, (ETOP + 4) / (4 * np.pi * (n + 0.5)))
    f = np.linspace(0, fend, 100)
    ax.plot(f, -4 + 4 * np.pi * f * (n + 0.5), ls='--', color=style.MUTED, lw=0.8, zorder=1)
    keep = lev[:, n] < ETOP
    ax.plot(phi[keep], lev[keep, n], 'o', ms=2.6, color=style.ACCENT, zorder=2)
    if n == 0:
        style.label(ax, fend + 0.002, -4 + 4 * np.pi * fend * 0.5, r'$n=0$', fontsize=9.5, color=style.MUTED, ha='left')
    else:
        style.label(ax, fend, ETOP + 0.03, r'$%d$' % n, fontsize=9.5, color=style.MUTED, va='bottom')
style.guide(ax, x=0.05, ls=':', color=style.MUTED, lw=0.8)
ax.set_xlim(0, 0.118); ax.set_ylim(EMIN, EMAX)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
ax.set_xticks([0, 0.05, 0.1]); ax.set_xticklabels(['0', '0.05', '0.1'])
ax.set_yticks([-4, -3.5, -3, -2.5]); ax.set_yticklabels(['$-4$', '$-3.5$', '$-3$', '$-2.5$'])
ax.tick_params(length=2.5, width=0.6, labelsize=10)
ax.set_xlabel(r'flux per plaquette $\phi$, in units of $h/e$', fontsize=10.5, labelpad=2)
ax.set_ylabel(r'$E/t$', labelpad=2)
style.save(fig, __file__)
