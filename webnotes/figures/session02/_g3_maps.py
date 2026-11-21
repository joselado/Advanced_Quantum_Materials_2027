"""Maps of an energy over the Brillouin zone of the square lattice, for Section 2.8, the redrawn square_bands and
decoupled_chains and the three picture options of the quiz on the hopping along y.

The lattice constant is 1, so the phases of the page are phi_x = k_x and phi_y = k_y, and the first Brillouin zone is
the square |phi_x|, |phi_y| < pi, drawn dashed. The maps are in the extended zone, up to HALF in each direction. The
energy is in units of t, on one diverging scale from -VMAX to VMAX with white at zero, blue below and red above,
the same in every map of the page so that the maps can be compared. The grid is the one of h.get_bands_map of the
pyqula script webnotes/scripts/session02/g3_square_lattice.py, nk by nk points from -2 pi to 2 pi without the end.
This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

VMAX = 4.0
HALF = 1.5 * np.pi
CMAP = 'RdBu_r'
B = 2 * np.pi * np.eye(2)                     # reciprocal vectors of the square lattice with a = 1
NK = 80                                       # the nk of the pyqula script
XS = -2 * np.pi + 4 * np.pi * np.arange(NK) / NK   # the axis of its map, in true momenta


def grid(d):
    """The map grid of the variables d of the pyqula script, which the figure script gets with
    style.run_script('session02/g3_square_lattice.py'): the 1D axes in true momenta and the band on them."""
    nk = d['nk']
    assert nk == NK
    kx, ky, band = d['kx'].reshape(nk, nk), d['ky'].reshape(nk, nk), d['band'].reshape(nk, nk)
    # the first index of pyqula runs along kx, and the window holds two zones per side, with no end point
    assert np.allclose(kx[:, 0], kx[:, -1]) and np.allclose(ky[0, :], ky[-1, :])
    xs, ys = kx[:, 0], ky[0, :]
    assert np.allclose(xs, XS) and np.allclose(ys, XS)
    # the band of pyqula is (2.14) with t = 1 at every point of the map, so the sign is the one of the page
    assert np.allclose(band, -2 * (np.cos(kx) + np.cos(ky)), atol=1e-10)
    return xs, ys, band


def phi_axes(ax, ticks=True, fontsize=8.5):
    """A thin box with the names phi_x and phi_y, and ticks at -pi, 0, pi."""
    style.kaxes(ax, ticks=None, fontsize=fontsize)
    ax.set_xlabel(r'$\varphi_x$', fontsize=fontsize, labelpad=1)
    ax.set_ylabel(r'$\varphi_y$', fontsize=fontsize, labelpad=0)
    if ticks:
        for f in (ax.set_xticks, ax.set_yticks):
            f([-np.pi, 0, np.pi])
        ax.set_xticklabels([r'$-\pi$', r'$0$', r'$\pi$']); ax.set_yticklabels([r'$-\pi$', r'$0$', r'$\pi$'])
        ax.tick_params(length=2.5, width=0.6, labelsize=fontsize - 0.5, pad=1.5)
    return ax


def energy_map(ax, xs, ys, values, half=HALF):
    """The energy values[i, j] at (xs[i], ys[j]) on the diverging scale, cut to |phi| < half, with the dashed zone."""
    im = ax.pcolormesh(xs, ys, np.asarray(values).T, cmap=CMAP, vmin=-VMAX, vmax=VMAX, shading='nearest', rasterized=True)
    ax.set_xlim(-half, half); ax.set_ylim(-half, half); ax.set_aspect('equal')
    style.draw_zone(ax, B)
    return im


def stripes_x():
    """The band with the hopping along y switched off, -2t cos(phi_x) with t = 1, on the grid of the map. numpy, since
    the square lattice of pyqula has no simple call that removes the bonds along one direction."""
    return np.repeat((-2 * np.cos(XS))[:, None], NK, axis=1)


def option(script, values):
    """One picture option of the quiz: the map values[i, j] at (XS[i], XS[j]) alone, with its axes and no other text."""
    fig, ax = style.plt.subplots(figsize=(4.6 * style.CM, 4.6 * style.CM))
    energy_map(ax, XS, XS, values)
    phi_axes(ax)
    style.save(fig, script)
