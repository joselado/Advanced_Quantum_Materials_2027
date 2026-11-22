"""Session 8, Section 8.9, the spinon Fermi surface of (8.15) on the triangular lattice at half filling, for t2/t1 = -0.5,
0 and 0.5, as the notebook cell "Spinon Fermi surface in gapless quantum spin liquids" computes it.

The calculation is the pyqula script webnotes/scripts/session08/g3_spinon_fermi_surface.py, which the student downloads
under the figure. It has the hopping +1 of pyqula to the first neighbors and t2 to the second ones, the two spins, and
the Fermi level from set_filling(0.5, nk=101). get_fermi_surface returns its map on the square window kx, ky from -1 to
1 with both ends, in units of 2 pi over the lattice constant, with the first index along kx. On the triangular lattice
this window is not a period along y, so style.pyqula_kmap refuses it, and the window is drawn as it is, which holds
the first Brillouin zone, dashed, and parts of the neighboring zones. The weight is sum_n delta/(E_n^2 + delta^2) over
both spins, so 2/delta on the Fermi surface, and the figure draws it divided by 2/delta.

The asserts below check the units, the orientation and the factor two of the spins against the band written by hand,
the filling on two dense meshes, that the map does not change when both hoppings change sign, and the number of
contours, one around Gamma, and one around each corner K for t2 = 0.5, counted on the periodic zone."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from scipy import ndimage
import style

d = style.run_script('session08/g3_spinon_fermi_surface.py')
g, kx, ky, maps, delta, nk, t2s = d['g'], d['kx'], d['ky'], d['maps'], d['delta'], d['nk'], d['t2s']
# the parameters of the caption: t1 = 1, t2 = -0.5, 0, 0.5, delta = 0.15, a map of 151 by 151 and set_filling with nk=101
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts', 'session08',
                        'g3_spinon_fermi_surface.py')).read()
assert nk == 151 and abs(delta - 0.15) < 1e-12 and list(t2s) == [-0.5, 0., 0.5] and len(maps) == 3
assert 'tij=[1., t2]' in src and 'set_filling(0.5, nk=101)' in src
A = np.array([np.asarray(g.a1, float)[:2], np.asarray(g.a2, float)[:2]])
B = 2 * np.pi * np.linalg.inv(A).T                      # rows b1, b2, in units of the inverse lattice constant
assert np.allclose(A, [[1, 0], [-0.5, np.sqrt(3) / 2]])
xs = np.unique(np.round(np.asarray(kx, float), 9))
assert len(xs) == nk and abs(xs[0] + 1) < 1e-12 and abs(xs[-1] - 1) < 1e-12


def band(KX, KY, t1, t2):
    """The band of geometry.triangular_lattice() with the hoppings t1 and t2, at the Cartesian momentum, by hand."""
    k1 = (KX * A[0, 0] + KY * A[0, 1]) / (2 * np.pi)
    k2 = (KX * A[1, 0] + KY * A[1, 1]) / (2 * np.pi)
    c = lambda x: np.cos(2 * np.pi * x)
    return 2 * t1 * (c(k1) + c(k2) + c(k1 + k2)) + 2 * t2 * (c(2 * k1 + k2) + c(k1 + 2 * k2) + c(k1 - k2))


def half_filling(t1, t2, n=600):
    """The Fermi level of half filling, the median of the band on a dense mesh that avoids Gamma."""
    u = (np.arange(n) + 0.5) / n
    U, V = np.meshgrid(u, u, indexing='ij')
    KX, KY = U * B[0, 0] + V * B[1, 0], U * B[0, 1] + V * B[1, 1]
    return np.median(band(KX, KY, t1, t2))


KX, KY = np.meshgrid(2 * np.pi * xs, 2 * np.pi * xs, indexing='ij')   # the first index along kx, as in pyqula


def pyqula_fermi_level(t1, t2):
    """The Fermi level that set_filling(0.5, nk=101) of the script chooses, read from the shifted level at Gamma,
    where the band is 6 (t1 + t2). pyqula runs in a temporary folder, so that no file is written here."""
    import tempfile
    from pyqula import geometry
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            h = geometry.triangular_lattice().get_hamiltonian(tij=[t1, t2])
            h.set_filling(0.5, nk=101)
            e0 = np.linalg.eigvalsh(h.get_hk_gen()([0., 0., 0.]))[0]
        finally:
            os.chdir(cwd)
    return 6 * (t1 + t2) - e0


def filling_at(mu, t2, n):
    """The fraction of the states below mu on a midpoint mesh of n by n reduced momenta, in blocks of rows."""
    u = (np.arange(n) + 0.5) / n
    below = 0
    for i0 in range(0, n, 500):
        U, V = np.meshgrid(u[i0:i0 + 500], u, indexing='ij')
        below += np.sum(band(U * B[0, 0] + V * B[1, 0], U * B[0, 1] + V * B[1, 1], 1., t2) < mu)
    return below / n ** 2


def torus_parts(mask):
    """The connected parts of a boolean array of the periodic zone, with 4 neighbors, joined across the edges."""
    lab, nl = ndimage.label(mask)
    parent = list(range(nl + 1))

    def root(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for a, b in list(zip(lab[0, :], lab[-1, :])) + list(zip(lab[:, 0], lab[:, -1])):
        if a and b:
            parent[root(a)] = root(b)
    return lab, root, {root(a) for a in range(1, nl + 1)}


mus = []
for t2, m in zip(t2s, maps):
    mu, mu_dense = pyqula_fermi_level(1., t2), half_filling(1., t2)
    mus.append(mu)
    filling, filling2 = filling_at(mu, t2, 1500), filling_at(mu, t2, 3000)
    assert abs(filling - filling2) < 5e-5                                # the mesh of 1500 is converged
    hand = 2 * delta / ((band(KX, KY, 1., t2) - mu) ** 2 + delta ** 2)
    # both hoppings with the opposite sign fill the complementary half of the zone, so the Fermi surface is the same
    mu_flip = pyqula_fermi_level(-1., -t2)
    flip = 2 * delta / ((band(KX, KY, -1., -t2) - mu_flip) ** 2 + delta ** 2)
    print('t2 = %+.1f: Fermi level %.4f, half filling of a dense mesh %.4f, filling %.4f, map against the hand band %.1e, '
          'Fermi level with both signs changed %.4f, the two maps differ by %.3f of the largest weight'
          % (t2, mu, mu_dense, filling, np.abs(m - hand).max() / m.max(), mu_flip, np.abs(flip - hand).max() / hand.max()))
    assert abs(filling - 0.5) < 0.001 and abs(mu - mu_dense) < 0.01               # the caption: 0.500 to 0.001
    assert np.abs(m - hand).max() < 1e-6 * m.max()                       # units, orientation and the two spins
    assert abs(m.max() * delta / 2 - 1) < 1e-3                           # the largest weight is 2/delta
    assert abs(mu_flip + mu_dense) < 0.01 and np.abs(flip - hand).max() < 0.15 * hand.max()
# the relative sign of t2 changes the Fermi surface, the maps of -0.5 and +0.5 differ
assert np.abs(maps[0] - maps[2]).max() > 0.5 * maps[0].max()
# what the caption says of the contours: Gamma is above the Fermi level for the three t2, and so a contour goes around
# it, M is below it, and K is below it for t2 = -0.5 and 0 and above it for 0.5, where a pocket goes around each corner K
Gam, Kpt, Mpt = np.zeros(2), (2 * B[0] - B[1]) / 3, B[0] / 2
assert np.isclose(np.linalg.norm(Kpt), 4 * np.pi / 3) and np.isclose(np.linalg.norm(Mpt), 2 * np.pi / np.sqrt(3))
for t2, K_above in zip(t2s, (False, False, True)):
    ef = half_filling(1., t2)
    eG, eK, eM = (band(p[0], p[1], 1., t2) - ef for p in (Gam, Kpt, Mpt))
    print('t2 = %+.1f: E - E_F at Gamma, K, M = %.3f %.3f %.3f' % (t2, eG, eK, eM))
    assert eG > 0 and eM < 0 and (eK > 0) == K_above
# the contours themselves: on a periodic mesh of 300 by 300 reduced momenta, which holds Gamma, K, K' and M, the empty
# states form one part around Gamma, plus one around K and one around K' for t2 = 0.5, and the filled states are one
# connected part. So each empty part is a closed pocket with one contour. The part around Gamma does not reach the Gamma
# of the next zone, so it is bounded. This holds at the Fermi level of the map and 0.01 above and below it, which also
# covers the median of a dense mesh.
n = 300
u = np.arange(n) / n
U, V = np.meshgrid(u, u, indexing='ij')
E = band(U * B[0, 0] + V * B[1, 0], U * B[0, 1] + V * B[1, 1], 1., 0.)
assert abs(E[0, 0] - 6) < 1e-12 and abs(E[100, 100] + 3) < 1e-12 and abs(E[200, 200] + 3) < 1e-12 and abs(E[150, 0] + 2) < 1e-12
for t2, mu, K_pockets in zip(t2s, mus, (False, False, True)):
    E = band(U * B[0, 0] + V * B[1, 0], U * B[0, 1] + V * B[1, 1], 1., t2)
    for shift in (-0.01, 0., 0.01):
        empty = E > mu + shift
        lab, root, parts = torus_parts(empty)
        filled = torus_parts(~empty)[2]
        at = {name: (root(lab[p]) if lab[p] else None) for name, p in
              (('Gamma', (0, 0)), ('K', (100, 100)), ("K'", (200, 200)), ('M', (150, 0)))}
        big = ndimage.label(np.tile(empty, (3, 3)))[0]
        bounded = big[n, n] != big[2 * n, n] and big[n, n] != big[n, 2 * n]
        assert len(filled) == 1 and bounded and at['Gamma'] is not None and at['M'] is None
        if K_pockets:
            assert len(parts) == 3 and len({at['Gamma'], at['K'], at["K'"]}) == 3
        else:
            assert len(parts) == 1 and at['K'] is None and at["K'"] is None
    print('t2 = %+.1f: the number of contours is %d, around Gamma%s' % (t2, len(parts), ', K and K\'' if K_pockets else ''))

HALF = 5.4
fig, axs = style.plt.subplots(1, 3, figsize=(style.WIDTH_CM * style.CM, 5.6 * style.CM))
X = 2 * np.pi * xs
for ax, t2, m in zip(axs, t2s, maps):
    im = ax.pcolormesh(X, X, (m * delta / 2).T, shading='nearest', rasterized=True, cmap='Blues', vmin=0, vmax=1)
    style.draw_zone(ax, B)
    ax.set_xlim(-HALF, HALF); ax.set_ylim(-HALF, HALF); ax.set_aspect('equal')
    style.kaxes(ax, ticks=4, fontsize=10)
    ax.set_title(r'$t_2/t_1=%s$' % ('%g' % t2).replace('-', r'-'), fontsize=10.5, pad=4)
corners = style.first_zone(B)
top = corners[np.argmax(corners[:, 1] + 1e-6 * corners[:, 0])]
for ax in axs:
    ax.text(top[0] + 0.15, top[1] + 0.15, r'$K$', fontsize=10, ha='left', va='bottom')
fig.subplots_adjust(wspace=0.42)
cb = fig.colorbar(im, ax=list(axs), orientation='vertical', fraction=0.03, pad=0.03)
cb.set_ticks([0, 0.5, 1]); cb.outline.set_visible(False)
cb.ax.tick_params(labelsize=9.5, length=2)
cb.set_label(r'weight at $E_F$, in units of $2/\delta$', fontsize=9.5)
style.save(fig, __file__)
