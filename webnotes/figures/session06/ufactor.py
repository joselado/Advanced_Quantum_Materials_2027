"""Session 6, the product of U and the energy that the antiferromagnet gains per cell of two sites, at large U."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import style, _mf

def gain_per_site(U):
    """E_FM - E_AFM per site, as in mf_chain.py, with the saturated ferromagnet at zero energy for U > 4t."""
    D = _mf.gap_parameter(U); m = 2 * D / U
    kin = -_mf.avg(lambda e, D: e * e / np.sqrt(e * e + D * D), D)
    e_afm = kin + U * (1 - m * m) / 4
    return 0.0 - e_afm

Us = np.geomspace(6, 60, 30)
dE = np.array([2 * gain_per_site(U) for U in Us])       # per cell of two sites
d20, d40 = 2 * gain_per_site(20.0), 2 * gain_per_site(40.0)
assert abs(d20 - 0.1995) < 5e-4 and abs(d40 - 0.0999) < 5e-4, (d20, d40)
fig, ax = style.figure(height_cm=5.0, width_cm=9.5)
ax.loglog(Us, dE, color=style.ACCENT)
ax.loglog(Us, 4 / Us, color=style.BROKEN, lw=1.0, ls=(0, (3, 2)))
for U, d in ((20, d20), (40, d40)):
    ax.plot([U], [d], 'o', color=style.INK, ms=3.5, zorder=5)
    ax.annotate(r'$U=%dt$, $%.4f\,t$' % (U, d), xy=(U, d), xytext=(U * 1.12, d * 1.35), fontsize=8, color=style.INK)
style.arrows(ax, xlabel=r'$U/t$', ylabel=r'$E_\mathrm{FM}-E_\mathrm{AFM}$')
ax.set_xticks([]); ax.set_yticks([]); ax.minorticks_off()
ax.set_xlim(5, 80); ax.set_ylim(0.04, 0.9)
style.label(ax, 9.5, 0.2, r'slope $-1$, $4t^2/U$', color=style.BROKEN, fontsize=8.5, rotation=0)
style.save(fig, __file__)
