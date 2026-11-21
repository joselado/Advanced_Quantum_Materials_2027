"""Session 3, section 3.5, the Hall conductivity of the Haldane model against the chemical potential.

The calculation is the pyqula script webnotes/scripts/session03/hall_conductivity_haldane.py, which the student
downloads under the figure. The model is the honeycomb lattice with h.add_haldane(0.1), the one of panel (a) of
berry_haldane.py, with a gap of 0.9 around zero energy. pyqula computes the intrinsic part,
sigma_xy = (e^2/h) (1/2 pi) sum_n int f(e_n - mu) Omega_n d^2k, with f the Fermi function, so at low temperature and
mu in the gap it is the Chern number of the filled band, +1."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

d = style.run_script('session03/hall_conductivity_haldane.py')
mu, temps, sigma = np.array(d['mu']), d['temperatures'], np.array(d['sigma_xy'])
# the gap from a k-mesh that holds the Dirac points, with no file written (h.get_bands would write its output here)
hk = d['h'].get_hk_gen()
e = np.array([np.linalg.eigvalsh(hk(np.array([i / 60, j / 60, 0.]))) for i in range(60) for j in range(60)])
GAP = e[e > 0].min() - e[e < 0].max()
mid = sigma[:, np.argmin(np.abs(mu))]
print('gap', round(GAP, 3), 'sigma in the middle of the gap', np.round(mid, 3), 'k_B T / gap', np.round(np.array(temps) / GAP, 2))
assert abs(GAP - 0.90) < 0.01 and abs(mu[np.argmin(np.abs(mu))]) < 1e-9
assert abs(mid[0] - 1) < 1e-3 and abs(mid[2] - 0.94) < 0.005 and abs(temps[2] / GAP - 0.22) < 0.005
assert np.abs(sigma[:, 0]).max() < 1e-3 and np.abs(sigma[:, -1]).max() < 1e-3

fig, ax = style.figure(height_cm=5.4, width_cm=10.5)
ax.set_xlim(-3.3, 3.3); ax.set_ylim(-0.05, 1.18)
ax.axvspan(-GAP / 2, GAP / 2, color=style.GRID, alpha=0.45, lw=0, zorder=0)
style.guide(ax, y=1, ls=':', color=style.MUTED)
colors = (style.ACCENT, style.LIGHT, style.WARM)
for T, s, col in reversed(list(zip(temps, sigma, colors))):
    ax.plot(mu, s, color=col, label=r'$k_BT=%g$' % T)
style.arrows(ax, xlabel=r'$\mu$', ylabel=r'$\sigma_{xy}$ in units of $e^2/h$')
ax.set_xticks([-3, 0, 3]); ax.set_xticklabels([r'$-3$', '0', '3'])
ax.set_yticks([0, 1]); ax.set_yticklabels(['0', '1']); ax.tick_params(length=2.5, width=0.6)
style.label(ax, 0, 0.22, 'gap', color=style.MUTED, fontsize=8.5)
h, l = ax.get_legend_handles_labels()
ax.legend(h[::-1], l[::-1], loc='upper right', bbox_to_anchor=(1.02, 0.86), handlelength=1.4)
style.save(fig, __file__)
