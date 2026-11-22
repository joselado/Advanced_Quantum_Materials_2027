"""Session 4, Section 4.4, the Landau levels of a square lattice are flat bands, and the Hall conductivity counts them.

Redrawn on 2026-11-21 from the pyqula script webnotes/scripts/session04/g1_landau_levels_square.py, which the student
downloads under the figure, in place of the numpy model of the first version. The model is the square lattice with
tij=[-1.], the band from -4t to 4t, and h.add_orbital_magnetic_field(1/20), the flux 1/20 per plaquette, in the
magnetic cell geometry.square_lattice().get_supercell((1, 20)) of 20 sites along y. pyqula puts the Peierls phases
on the bonds along x, so the momentum k_x is the good quantum number along the vector potential, the k_y of the
Landau gauge of Section 4.8. Panel (a) is the four lowest bands against k_x a at k_y = 0, with the dashed lines at
-4t + hbar omega_c (n + 1/2), hbar omega_c = 4 pi t / 20. Panel (b) is the Hall conductivity in units of e^2/h,
the Chern number h.get_chern() of the filled bands with the Fermi energy in each gap, drawn as the staircase of a
clean system at zero temperature, with the steps at the energies of the flat bands. The signs are those that pyqula
gives for its positive field, and the caption says so. The asserts check every number of the caption."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

d = style.run_script('session04/g1_landau_levels_square.py')
q, nb = 20, 4
kx = np.asarray(d['kx']) * 2 * np.pi              # k_x a, from -pi to pi
bands, lev, sig = np.asarray(d['bands'][q]), np.asarray(d['levels'][q]), np.asarray(d['sigma_xy'][q])
wc = 4 * np.pi / q
cont = -4 + wc * (np.arange(nb) + 0.5)
C = np.diff(sig)
ylo, yhi = -4.05, -1.75
print('levels', np.round(lev[:nb + 1], 4), 'sigma_xy in the gaps', np.round(sig, 6), 'C', np.round(C, 6))
print('below the dashed lines by', np.round(cont - lev[:nb], 3), 'of the spacing', np.round((cont - lev[:nb]) / wc, 2))
# the Hall conductivity in the gaps is 0, 1, 2, 3, 4, so each of the four bands has C = 1, with the sign of pyqula
assert len(sig) == nb + 1 and np.allclose(sig, np.arange(nb + 1), atol=1e-6) and np.allclose(C, 1, atol=1e-6)
# the bands are flat along k_x, the dashed lines are the continuum, and the shifts are those of the caption
assert np.ptp(bands[:, :nb], axis=0).max() < 1e-5
assert abs(wc - 0.628) < 5e-4 and round(wc, 2) == 0.63
assert np.allclose(lev[:nb], [-3.698, -3.118, -2.584, -2.096], atol=1e-3)
assert np.allclose(cont - lev[:nb], [0.012, 0.060, 0.155, 0.295], atol=1e-3) and np.all(cont > lev[:nb])
assert round(cont[0] - lev[0], 2) == 0.01 and round(cont[3] - lev[3], 2) == 0.30 and abs((cont[3] - lev[3]) / wc - 0.47) < 0.005
# the window holds the four bands and their four dashed lines, and no other band or line
assert lev[nb - 1] < cont[nb - 1] < yhi < lev[nb] and -4 + wc * (nb + 0.5) > yhi and ylo < lev[0]

fig, axs = plt.subplots(1, 2, figsize=(12.6 * style.CM, 5.6 * style.CM), gridspec_kw=dict(wspace=0.55, width_ratios=[1.3, 1]))
ax = axs[0]
for n in range(nb):
    style.guide(ax, y=cont[n], ls='--', color=style.MUTED, lw=0.8)
    ax.plot(kx, bands[:, n], color=style.ACCENT)
    style.label(ax, 2.05, lev[n] - 0.17, r'$C=%d$' % round(C[n]), fontsize=10, color=style.ACCENT)
ax.set_xlim(-np.pi, np.pi); ax.set_ylim(ylo, yhi)
style.arrows(ax, xlabel=r'$k_x a$', ylabel=r'$E/t$', ticks=True)
ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'])
ax.set_yticks([-4, -3, -2]); ax.set_yticklabels(['$-4$', '$-3$', '$-2$']); ax.tick_params(length=2.5, width=0.6)
ax.text(0.5, -0.2, '(a)', transform=ax.transAxes, ha='center', va='top')

ax = axs[1]
# the staircase: sigma = N for E_F in the gap above N filled bands, and a jump of one at the energy of each flat band
xs, ys = [0, 0], [ylo, lev[0]]
for n in range(nb):
    top = lev[n + 1] if n + 1 < nb else yhi
    xs += [n + 1, n + 1]; ys += [lev[n], top]
for n in range(nb):
    style.guide(ax, y=lev[n], color=style.GRID, lw=0.8)
ax.plot(xs, ys, color=style.BROKEN, lw=1.8)
ax.set_xlim(-0.3, 4.6); ax.set_ylim(ylo, yhi)
style.arrows(ax, xlabel=r'$\sigma_{xy}\,h/e^2$', ylabel=r'$E_F/t$', ticks=True)
ax.set_xticks([0, 1, 2, 3, 4]); ax.set_xticklabels(['0', '1', '2', '3', '4'])
ax.set_yticks([-4, -3, -2]); ax.set_yticklabels(['$-4$', '$-3$', '$-2$']); ax.tick_params(length=2.5, width=0.6)
ax.text(0.5, -0.2, '(b)', transform=ax.transAxes, ha='center', va='top')
style.save(fig, __file__)
