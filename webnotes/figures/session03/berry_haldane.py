"""Session 3, section 3.5, the Berry curvature of the filled band of two gapped honeycomb lattices.

The calculation is the pyqula script webnotes/scripts/session03/berry_curvature_honeycomb.py, which the student
downloads under the figure. Panel (a) is the Haldane coupling h.add_haldane(0.1), which opens a gap of 0.9, and panel
(b) a staggered sublattice potential of 0.5, with a gap of 1.0. pyqula gives the curvature b per unit area of the
reduced zone, so the plotted b / 2 pi has the Chern number as its average over the zone. Its sign is the one of
Omega = -2 Im <d_kx u | d_ky u> of the page, checked with the Kubo form of Omega on the same Hamiltonian (C = +1 for
the coupling +0.1). The maps are in the extended zone, with the first Brillouin zone dashed, and the momenta are in
units of the inverse bond length."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

d = style.run_script('session03/berry_curvature_honeycomb.py')
g, kx, ky = d['g'], d['kx'], d['ky']
maps = (d['omega_haldane'] / (2 * np.pi), d['omega_staggered'] / (2 * np.pi))
cherns = (d['chern_haldane'], d['chern_staggered'])
print('Chern numbers', cherns, 'averages', [m.mean() for m in maps], 'largest values', [np.abs(m).max() for m in maps])
assert abs(cherns[0] - 1) < 1e-6 and abs(cherns[1]) < 1e-6
assert abs(maps[0].mean() - 1) < 1e-6 and abs(maps[1].mean()) < 1e-6

VMAX = 12
fig, axs = style.plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 6.6 * style.CM))
for ax, m, name in zip(axs, maps, ('(a) Haldane coupling, $C=1$', '(b) staggered potential, $C=0$')):
    im, B = style.pyqula_kmap(ax, g, kx, ky, m, half=3.3, cmap='RdBu_r', vmin=-VMAX, vmax=VMAX)
    style.kaxes(ax, ticks=2)
    ax.set_title(name, fontsize=9, pad=5)
corners = style.first_zone(B)
# the largest curvature of the Haldane lattice sits at a corner of the zone, which is a Dirac point
a = np.linalg.norm(np.asarray(g.a1, float)[:2])
i = np.argmax(maps[0]); peak = np.array([kx[i], ky[i]]) * 2 * np.pi / a
allc = np.array([c + s * B[0] + t * B[1] for c in corners for s in (-1, 0, 1) for t in (-1, 0, 1)])
assert np.linalg.norm(allc - peak, axis=1).min() < 0.1, peak
top = corners[np.argmax(corners[:, 1])]; bottom = corners[np.argmin(corners[:, 1])]
for ax in axs:
    ax.text(top[0] + 0.22, top[1] + 0.12, r'$K$', fontsize=8.5, ha='left', va='bottom')
    ax.text(bottom[0] + 0.22, bottom[1] - 0.12, r"$K'$", fontsize=8.5, ha='left', va='top')
fig.subplots_adjust(wspace=0.38)
cb = fig.colorbar(im, ax=list(axs), orientation='vertical', fraction=0.035, pad=0.04)
cb.set_ticks([-10, 0, 10]); cb.outline.set_visible(False)
cb.ax.tick_params(labelsize=8, length=2)
cb.set_label(r'$\Omega\,A_{\rm BZ}/2\pi$', fontsize=8.5)
style.save(fig, __file__)
