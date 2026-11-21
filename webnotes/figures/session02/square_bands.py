"""Session 2, Section 2.8, the band (2.14) of the square lattice along a path and over the Brillouin zone.

The calculation is the pyqula script webnotes/scripts/session02/g3_square_lattice.py, which the student downloads under
the figure, with the hopping -1, the sign of (2.14), and t = 1, a = 1. Panel (a) is the band on the path Gamma, X, M,
Gamma, given as reduced momenta, and panel (b) the same band from h.get_bands_map on 80 by 80 points over two zones
per side, in the extended zone with the first zone dashed, on the diverging scale of _g3_maps.py. The contour lines
are at -3 to 3 in steps of 1, and the line of zero energy is the black one, the square |phi_x| + |phi_y| = pi."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
import _g3_maps as maps

d = style.run_script('session02/g3_square_lattice.py')
xs, ys, band = maps.grid(d)
kp, e = np.asarray(d['kpath'], float), np.asarray(d['e'], float)
# the path: steps 0, 100, 200, 300 are Gamma, X, M, Gamma, and the band there is -4, 0, 4, -4 in units of t
assert len(e) == 301 and np.allclose(e[[0, 100, 200, 300]], [-4, 0, 4, -4], atol=1e-12)
assert np.allclose(e, -2 * (np.cos(2 * np.pi * kp[:, 0]) + np.cos(2 * np.pi * kp[:, 1])), atol=1e-12)
assert np.isclose(e.min(), -4) and np.isclose(e.max(), 4)
x = np.r_[0, np.cumsum(np.linalg.norm(np.diff(kp[:, :2], axis=0), axis=1))] * 2 * np.pi
marks = x[[0, 100, 200, 300]]
assert np.allclose(marks, [0, np.pi, 2 * np.pi, (2 + np.sqrt(2)) * np.pi])
# the map: -4 at Gamma, 0 at X, 4 at M, on points of the mesh
i0, ip = np.argmin(np.abs(xs)), np.argmin(np.abs(xs - np.pi))
assert np.isclose(xs[ip], np.pi) and np.allclose([band[i0, i0], band[ip, i0], band[ip, ip]], [-4, 0, 4])
# the zero line is the square |phi_x| + |phi_y| = pi, and the band is periodic across the dashed border
on = np.abs(np.abs(xs[:, None]) + np.abs(ys[None, :]) - np.pi) < 1e-9
assert on.sum() > 0 and np.allclose(band[on], 0, atol=1e-12)
assert np.allclose(np.roll(band, len(xs) // 2, axis=0), band) and np.allclose(np.roll(band, len(xs) // 2, axis=1), band)

fig = style.plt.figure(figsize=(style.WIDTH_CM * style.CM, 6.0 * style.CM))
gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1], wspace=0.42)
ax = fig.add_subplot(gs[0])
ax.plot(x, e, color=style.ACCENT)
for xx in marks:
    style.guide(ax, x=xx)
style.guide(ax, y=0)
style.arrows(ax, ylabel=r'$\epsilon/t$')
ax.set_xticks(marks); ax.set_xticklabels([r'$\Gamma$', r'$X$', r'$M$', r'$\Gamma$'])
ax.set_yticks([-4, 0, 4]); ax.set_yticklabels([r'$-4$', r'$0$', r'$4$'])
ax.tick_params(length=2.5, width=0.6, pad=2)
ax.set_xlim(0, marks[-1]); ax.set_ylim(-4.7, 4.7)
ax.text(-0.02, -0.2, '(a)', transform=ax.transAxes, fontsize=8.5, ha='left')

ax = fig.add_subplot(gs[1])
im = maps.energy_map(ax, xs, ys, band)
levels = [-3, -2, -1, 1, 2, 3]
assert np.isclose(maps.HALF, 1.5 * np.pi)                             # the caption: drawn up to 3 pi/2
assert np.allclose(levels, [x for x in np.arange(-3, 4) if x != 0]) and len(xs) == 80   # the caption: -3t to 3t, 80 by 80
ax.contour(xs, ys, band.T, levels=levels, colors=style.INK, linewidths=0.5, alpha=0.55, linestyles='solid')
cz = ax.contour(xs, ys, band.T, levels=[0], colors='black', linewidths=1.3)
maps.phi_axes(ax)
box = dict(boxstyle='round,pad=0.12', fc='white', ec='none', alpha=0.85)
for (px, py, s, dx, dy) in ((0, 0, r'$\Gamma$', 0.42, -0.5), (np.pi, 0, r'$X$', -0.42, -0.5), (np.pi, np.pi, r'$M$', -0.45, -0.5)):
    ax.scatter([px], [py], s=9, color='black', zorder=6, clip_on=False)
    style.label(ax, px + dx, py + dy, s, fontsize=8.5, zorder=7, bbox=box)
ax.text(-0.02, -0.29, '(b)', transform=ax.transAxes, fontsize=8.5, ha='left')
cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.05)
cb.set_ticks([-4, -2, 0, 2, 4]); cb.outline.set_visible(False)
cb.ax.tick_params(labelsize=8, length=2)
cb.set_label(r'$\epsilon/t$', fontsize=8.5, labelpad=2)
cb.add_lines(cz)
style.save(fig, __file__)
