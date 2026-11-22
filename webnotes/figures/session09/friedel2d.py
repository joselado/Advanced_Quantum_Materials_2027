"""Session 9, the Friedel ripples of a single impurity in a square lattice, the change of the LDOS at one energy.

Redrawn on 2026-11-22 from the pyqula script webnotes/scripts/session09/g4_friedel_square.py, by the rules of
2026-11-21. On the left the Fermi contour at E = -3.4 of the band of the pyqula Hamiltonian, with the axes k_x and
k_y and the first Brillouin zone dashed. On the right the map of the energy -3.4 of the script, with the axes x and y
in sites and a colorbar. The numbers of the caption are asserted in _g4_ripples.check, and here the impurity of 3t, the
contour at k_F, the half width of 12 sites, the unit 10^-3/t of the map and where the colors saturate. The decay of the
LDOS as 1/r and the damping length of about 14 sites of the caption are asserted in checks/session09/g4_06_friedel_metal.py."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import style
import physcheck
import _g4_ripples

d = _g4_ripples.check(style.run_script('session09/g4_friedel_square.py'))     # the variables of the pyqula script
i = list(d['energies']).index(-3.4)
E, kF = d['energies'][i], d['kF'][i]
dv = d['hv'].intra - d['h'].intra
dv = np.asarray(dv.todense() if hasattr(dv, 'todense') else dv)
assert dv.shape == (1, 1) and abs(dv[0, 0] - 3.0) < 1e-12           # the caption: the impurity has the onsite energy 3t
M, c = _g4_ripples.grid(d, i)
assert c == 12                                                      # the map, and the quiz pictures, from -12 to 12 sites
ix, iy = np.round(d['x']).astype(int), np.round(d['y']).astype(int)
off = (ix != 0) | (iy != 0)
assert np.allclose(M[iy[off] + c, ix[off] + c], d['maps'][i][off] * 1e3, rtol=0, atol=1e-12)   # drawn in 10^-3/t
assert np.isnan(M[c, c])                                            # the impurity site is left out
r = np.hypot(*np.meshgrid(np.arange(-c, c + 1), np.arange(-c, c + 1)))
assert np.abs(M[(r > 0) & (r < 3)]).max() > _g4_ripples.VMAX       # the caption: the colors saturate close to the
assert np.abs(M[r >= 3]).max() < _g4_ripples.VMAX                  # impurity, and only there

fig, (a, b) = plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 6.0 * style.CM),
                           gridspec_kw=dict(width_ratios=[1, 1.18], wspace=0.42))

# the Fermi contour, from the band of the pyqula Hamiltonian of the script
hk, B = physcheck.from_pyqula(d['h'])
half = np.pi + 0.45
kk = np.linspace(-half, half, 181)
band = np.array([[hk((kx, ky))[0, 0].real for kx in kk] for ky in kk])
assert abs(band.min() + 4) < 0.01 and np.allclose(band, band.T)
cs = a.contour(kk, kk, band, levels=[E], colors=[style.ACCENT], linewidths=1.6, linestyles='solid')
xs = np.concatenate([p[:, 0] for p in cs.allsegs[0]])
assert abs(xs.max() - kF) < 0.01                     # the contour crosses the k_x axis at k_F = 0.80
style.draw_zone(a, B)
a.set_xlim(-half, half); a.set_ylim(-half, half); a.set_aspect('equal')
style.kaxes(a)
a.set_xticks([-np.pi, -kF, kF, np.pi]); a.set_xticklabels([r'$-\pi$', r'$-0.8$', r'$0.8$', r'$\pi$'])
a.set_yticks([-np.pi, 0, np.pi]); a.set_yticklabels([r'$-\pi$', r'$0$', r'$\pi$'])
a.tick_params(length=2.5, width=0.6, labelsize=8)
a.annotate('', xy=(kF, 0), xytext=(-kF, 0), arrowprops=dict(arrowstyle='<|-|>', color=style.BROKEN, lw=1.2,
                                                             mutation_scale=7, shrinkA=0, shrinkB=0))
style.label(a, 0, 0.42, r'$2k_F$', color=style.BROKEN, fontsize=9)
a.set_title('(a)', fontsize=9, pad=4)

# the change of the LDOS at the same energy, around the impurity
im = _g4_ripples.draw_map(b, d, i)
cblabel = r'$\delta\rho(\vec r,E)$ in $10^{-3}/t$'
assert '10^{-3}/t' in cblabel     # the unit of the caption; the LDOS of pyqula is per site and per t (g4_06_friedel_metal.py)
_g4_ripples.colorbar(fig, b, im, label=cblabel)
b.set_title('(b)', fontsize=9, pad=4)
style.save(fig, __file__)
