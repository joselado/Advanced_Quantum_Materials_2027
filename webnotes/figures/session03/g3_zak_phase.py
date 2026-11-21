"""Session 3, section 3.9c, the Zak phase of the SSH chain and the end level of the open chain, against the hopping t.

The data come from the downloadable script webnotes/scripts/session03/g3_ssh_zak.py, which calls pyqula. The chain has
the intracell hopping t and the intercell hopping 1. Top, the gap of the infinite chain, 2|1-t|, and the level closest
to zero of an open chain of 20 cells, which is 40 sites. Bottom, the Zak phase (3.6) of the lower band in units of pi.
pyqula gives the phase between -pi and pi and the script keeps its size, since the phase is defined modulo 2 pi."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

d = style.run_script('session03/g3_ssh_zak.py')
ts, zak, gap, low = (np.array(d[k]) for k in ('ts', 'zak_phase', 'gap', 'end_level'))
N = d['N']
# the numbers of the caption: the phase is pi for t<1 and 0 for t>1, the gap is 2|1-t|, the chain has 40 sites
i1 = np.argmin(np.abs(ts - 1))
assert 2 * N == 40 and ts[i1] == 1 and gap[i1] < 1e-6 and np.isnan(zak[i1])          # the gap closes at t=1
assert np.allclose(zak[ts < 1], np.pi, atol=1e-6) and np.allclose(zak[ts > 1], 0, atol=1e-6)
assert np.allclose(gap, 2 * np.abs(1 - ts), atol=2e-3)
# the end level is t^N (1 - t^2) while the two end states do not overlap, and it is below 0.001 up to t = 0.7
sel = ts < 0.7
assert np.all(low[sel] < 1e-3) and np.allclose(low[sel], ts[sel] ** N * (1 - ts[sel] ** 2), atol=1e-5)
# at t = 0.9 the level has already left zero, 0.024, and for t>1 it follows the edge of the band
i9 = np.argmin(np.abs(ts - 0.9))
print('t', ts[i9], 'end level', round(low[i9], 4), ' end level at t=1.5:', round(low[np.argmin(np.abs(ts - 1.5))], 3))
assert abs(ts[i9] - 0.9) < 1e-9 and abs(low[i9] - 0.024) < 0.002
assert np.all(low[ts > 1.2] > np.abs(1 - ts[ts > 1.2]))

fig, axs = style.figure(nrows=2, height_cm=7.6, sharex=True, gridspec_kw=dict(hspace=0.22, height_ratios=[1.5, 1]))
ax = axs[0]
ax.axvspan(0, 1, color=style.GRID, alpha=0.35, lw=0)
ax.plot(ts, gap, color=style.ACCENT)
ax.plot(ts, low, color=style.BROKEN)
ax.set_xlim(0, 2); ax.set_ylim(0, 2.1)
style.arrows(ax, ticks=True)
ax.annotate('energy, in units of the intercell hopping', xy=(-0.02, 1.07), xycoords='axes fraction', ha='left', va='bottom')
ax.set_yticks([0, 1, 2])
style.label(ax, 0.30, 1.72, 'gap of the bulk', color=style.ACCENT, ha='left', fontsize=8.5)
style.label(ax, 1.97, 0.13, 'smallest $|E|$ of the open chain', color=style.BROKEN, ha='right', fontsize=8.5)
ax = axs[1]
ax.axvspan(0, 1, color=style.GRID, alpha=0.35, lw=0)
# the phase is constant on each side, so each line is drawn up to the transition at t=1
ax.plot(np.append(ts[ts < 1], 1), np.append(zak[ts < 1], zak[ts < 1][-1]) / np.pi, color=style.ACCENT)
ax.plot(np.append(1, ts[ts > 1]), np.append(zak[ts > 1][0], zak[ts > 1]) / np.pi, color=style.ACCENT)
ax.plot([1, 1], [0, 1], color=style.ACCENT, lw=1.0, ls=':')
ax.set_xlim(0, 2); ax.set_ylim(-0.15, 1.25)
style.arrows(ax, xlabel='$t$', ylabel=r'$\gamma/\pi$', ticks=True)
ax.set_xticks([0, 0.5, 1, 1.5, 2]); ax.set_xticklabels(['0', '0.5', '1', '1.5', '2'])
ax.set_yticks([0, 1])
for a in axs:
    a.tick_params(length=2.5, width=0.6)
style.label(ax, 0.5, 0.55, 'end states', color=style.MUTED, fontsize=8.5)
style.label(ax, 1.5, 0.55, 'no end states', color=style.MUTED, fontsize=8.5)
style.save(fig, __file__)
