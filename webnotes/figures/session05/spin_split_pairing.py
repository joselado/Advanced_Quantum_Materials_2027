"""Session 5, an exchange field splits the two spin bands, so only a pair of equal spins sits on one Fermi surface.

Redrawn on 2026-11-21 from the downloadable pyqula script g3_exchange_chain_bands.py, the chain with t=1, mu=0 and the
exchange field -h(n_up - n_dn) with h=0.6, with ticks at the Fermi momenta and at 2h on the energy axis, which the old
figure did not have. The checks are in _g3_spinbands.py, which the picture options of the quiz also use."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g3_spinbands as sb
from _g3_spinbands import style, plt

d = style.run_script('session05/g3_exchange_chain_bands.py')
k = sb.check(d)
mu, field = sb.CASES[0]
e, sz = d['energies'][0], d['spins'][0]
ku, kd = sb.kf(mu, field, 1), sb.kf(mu, field, -1)

FS = 11
fig, ax = plt.subplots(figsize=(12.0 * style.CM, 6.2 * style.CM))
style.guide(ax, y=0)
sb.bands(ax, k, e, sz, lw=1.9)
for kk, c in [(ku, style.ACCENT), (-ku, style.ACCENT), (kd, style.BROKEN), (-kd, style.BROKEN)]:
    ax.plot([kk], [0], 'o', color=c, ms=4.5, zorder=5)
style.label(ax, np.pi + 0.12, -2 * np.cos(np.pi) - mu - field, r'$\uparrow$', color=style.ACCENT, fontsize=FS + 3, ha='left', clip_on=False)
style.label(ax, np.pi + 0.12, -2 * np.cos(np.pi) - mu + field, r'$\downarrow$', color=style.BROKEN, fontsize=FS + 3, ha='left', clip_on=False)
# the pair of two up electrons sits on one Fermi surface, at -k_F up and k_F up
ax.annotate('', xy=(ku, 0.3), xytext=(-ku, 0.3), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.9, shrinkA=0, shrinkB=0))
style.label(ax, 0, 0.62, r'$\uparrow\uparrow$ pair', fontsize=FS - 1)
# the singlet partner of the up electron at k_F up is the down electron at -k_F up, 2h above E=0
ax.plot([-ku], [2 * field], 'o', mfc='white', mec=style.BROKEN, mew=1.3, ms=5, zorder=6)
ax.annotate('', xy=(-ku, 2 * field - 0.07), xytext=(-ku, 0.07), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.9, shrinkA=0, shrinkB=0))
style.label(ax, -ku + 0.22, 0.8, r'$2h$', ha='left', fontsize=FS)
ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-2.8, 2.8)
sb.frame(ax, [(-np.pi, r'$-\pi$'), (-ku, r'$-k_{F\uparrow}$'), (0, '0'), (kd, r'$k_{F\downarrow}$'), (ku, r'$k_{F\uparrow}$'),
              (np.pi, r'$\pi$')],
         [(-2, '$-2$'), (0, '0'), (2 * field, '1.2'), (2, '2')], r'$k$', r'$E/t$', FS)
style.save(fig, __file__)
