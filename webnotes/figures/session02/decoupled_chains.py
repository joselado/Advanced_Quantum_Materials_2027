"""Session 2, Section 2.8, a square lattice with the hopping along y switched off, and its band, in the feedback of the
quiz on the hopping along y.

Left, a drawing of the lattice, with the bonds along y dashed. Right, the band -2t cos(phi_x) with t = 1 over the zone,
in numpy, since the square lattice of pyqula has no simple call that removes the bonds along one direction. The map is
drawn as the other maps of the page (_g3_maps.py), in the extended zone with the first zone dashed, on the diverging
scale from -4 to 4 that the picture options of the quiz share, with its colorbar."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
import _g3_maps as maps

Z = maps.stripes_x()
# the same at every phi_y, -2 at phi_x = 0 and 2 at phi_x = pi
assert np.allclose(Z, Z[:, :1]) and np.isclose(Z[np.argmin(np.abs(maps.XS)), 0], -2) and np.isclose(Z[np.argmin(np.abs(maps.XS - np.pi)), 0], 2)

assert np.isclose(maps.HALF, 1.5 * np.pi)                             # the caption: drawn up to 3 pi/2
fig = style.plt.figure(figsize=(11.0 * style.CM, 4.6 * style.CM))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1], wspace=0.35)
axL = fig.add_subplot(gs[0]); axR = fig.add_subplot(gs[1])
axL.axis('off'); axL.set_aspect('equal')
for j in range(4):
    axL.plot([0, 4], [j, j], color=style.INK, lw=1.8, zorder=2)
    axL.scatter(np.arange(5), [j] * 5, s=30, color=style.ACCENT, zorder=3)
    for i in range(5):
        if j < 3:
            axL.plot([i, i], [j, j + 1], color=style.MUTED, lw=1.0, ls=(0, (3, 3)), zorder=1)
style.label(axL, 2.0, -0.6, r'$t$ along $x$, $0$ along $y$', fontsize=8.5)
axL.set_xlim(-0.4, 4.4); axL.set_ylim(-1.0, 3.4)

im = maps.energy_map(axR, maps.XS, maps.XS, Z)
maps.phi_axes(axR)
cb = fig.colorbar(im, ax=axR, fraction=0.046, pad=0.05)
cb.set_ticks([-4, -2, 0, 2, 4]); cb.outline.set_visible(False)
cb.ax.tick_params(labelsize=8, length=2)
cb.set_label(r'$\epsilon/t$', fontsize=8.5, labelpad=2)
style.save(fig, __file__)
