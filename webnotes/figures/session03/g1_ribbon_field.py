"""Session 3, section 3.6, the bands of a ribbon in a magnetic field, the reference plot of the quiz on the reversal
of the field. The data come from webnotes/scripts/session03/g1_qh_ribbon.py, the first field of its list."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style, _g1_ribbon

plt.rcParams.update({'savefig.dpi': 300})
d = style.run_script('session03/g1_qh_ribbon.py')
_g1_ribbon.check(d)
fig, ax = plt.subplots(figsize=(8.6 * style.CM, 6.0 * style.CM))
lc = _g1_ribbon.draw(ax, d, 0, lw=1.8)
ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=11)
ax.set_yticks([-2, -1, 0]); ax.set_yticklabels(['$-2$', '$-1$', '$0$'], fontsize=11)
ax.tick_params(length=2.5, width=0.6)
ax.set_xlabel(r'momentum $k$', fontsize=11, labelpad=1); ax.set_ylabel(r'energy $E/t$', fontsize=11, labelpad=2)
cb = fig.colorbar(lc, ax=ax, pad=0.03, fraction=0.05, ticks=[-8, 0, 8])
cb.set_label(r'position $y$ across the ribbon', fontsize=10, labelpad=2)
cb.ax.tick_params(length=2, width=0.6, labelsize=10)
cb.outline.set_linewidth(0.5)
style.save(fig, __file__)
