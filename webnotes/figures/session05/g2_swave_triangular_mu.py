"""Session 5, section 5.9, the BdG bands of the triangular lattice with a uniform s-wave pairing at three chemical potentials,
colored by the electron weight.

The data come from the downloadable script webnotes/scripts/session05/g2_swave_triangular_mu.py, which calls pyqula, with the
pairing of the notebook cell "Gapped and nodal superconducting orders", add_pairing(mode="swave", delta=0.4). pyqula takes the
hopping as +1, so the band runs from -3 at K to 6 at Gamma, with -2 at M, and add_onsite(x) is the chemical potential mu=-x. The
three chemical potentials mu = 3, 0 and -2.5 put the crossings of the electron and the hole band at different momenta, on
Gamma-K and M-Gamma for the first two and on both sides of K for the last one. The smallest |E| is 0.4 in the three cases, from a
minimization over the whole zone, and the path gives at most 0.4001."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import _g2_bdg as b
style = b.style

d = style.run_script('session05/g2_swave_triangular_mu.py')
A = np.array([[1., 0.], [-0.5, np.sqrt(3) / 2]])                          # the lattice vectors of geometry.triangular_lattice()
B = 2 * np.pi * np.linalg.inv(A).T
kp = np.array(d['kpath'])
x = b.path_x(kp, B)
corners = [0, 150, 300, 450]
assert np.allclose(kp[corners, :2], [[0, 0], [1 / 3, 1 / 3], [0.5, 0], [0, 0]])
assert abs(np.linalg.norm(kp[150, :2] @ B) - 4 * np.pi / 3) < 1e-9 and abs(np.linalg.norm(kp[300, :2] @ B) - 2 * np.pi / np.sqrt(3)) < 1e-9


def band(r):
    """The band of pyqula with the hopping +1, at the momentum r in units of the reciprocal vectors."""
    k1, k2 = 2 * np.pi * r[..., 0], 2 * np.pi * r[..., 1]
    return 2 * (np.cos(k1) + np.cos(k2) + np.cos(k1 + k2))


assert abs(band(kp[0, :2]) - 6) < 1e-9 and abs(band(kp[150, :2]) + 3) < 1e-9 and abs(band(kp[300, :2]) + 2) < 1e-9
D = 0.4
crossings = []
for x0, e, w in zip(d['onsites'], d['energies'], d['weights']):
    b.check(e, w)
    eps = band(kp[:, :2]) + x0
    assert np.allclose(e[:, 2], np.sqrt(eps**2 + D**2), atol=1e-9)        # (5.9) along the whole path
    cross = np.where(np.diff(np.sign(eps)) != 0)[0]
    crossings.append(cross)
    best = min(minimize(lambda r: (band(r) + x0) ** 2, r0, method='Nelder-Mead').fun for r0 in
               ([0.1, 0.1], [0.3, 0.3], [0.4, 0.05], [0.2, 0.0]))                       # eps^2 at its zero on the Fermi surface
    assert best < 1e-12                                                     # the Fermi surface exists, so min E = Delta
assert [len(c) for c in crossings] == [2, 2, 2]
assert all(0 < c[0] < 150 and 300 <= c[1] < 450 for c in crossings[:2])     # on Gamma-K and on M-Gamma
assert 0 < crossings[2][0] < 150 <= crossings[2][1] < 300                   # on both sides of K
assert np.allclose(d['smallest'], D, atol=2e-4)
# the arrows of the caption: the two drawn branches, bands 1 and 2, are 2|Delta| = 0.8 apart at every crossing. The path has
# no point exactly on the Fermi surface, so on it the distance is at least 0.8 and at most 0.805 (0.804 on Gamma-K for mu=3)
apart = [[np.min(e[c - 5:c + 6, 2] - e[c - 5:c + 6, 1]) for c in cross] for e, cross in zip(d['energies'], crossings)]
assert np.min(apart) > 2 * D - 1e-9 and np.max(apart) < 2 * D + 5e-3 and abs(2 * D - 0.8) < 1e-12
print('mu', [-o for o in d['onsites']], 'crossings at steps', [list(c) for c in crossings], 'smallest |E| on the path',
      np.round(d['smallest'], 5), 'branches apart at the crossings', np.round(apart, 4))

plt.rcParams.update({'font.size': 12})
fig, axs = plt.subplots(1, 3, figsize=(14.2 * style.CM, 5.6 * style.CM), sharey=True, gridspec_kw=dict(wspace=0.22))
kt = [(x[c], l) for c, l in zip(corners, (r'$\Gamma$', r'$K$', r'$M$', r'$\Gamma$'))]
et = [(-1.5, '$-1.5$'), (-0.4, '$-0.4$'), (0.4, '$0.4$'), (1.5, '$1.5$')]
tags = (r'$\mu=3$', r'$\mu=0$', r'$\mu=-2.5$')
for ax, e, w, tag, cross in zip(axs, d['energies'], d['weights'], tags, crossings):
    style.guide(ax, y=0)
    for c in corners[1:3]:
        style.guide(ax, x=x[c], lw=0.6)
    b.bands(ax, x, e, w, lw=1.7)
    ax.set_xlim(0, x[-1]); ax.set_ylim(-1.9, 1.9)
    b.frame(ax, kt, et, r'$\mathbf{k}$', r'$E/|t|$' if ax is axs[0] else None, fontsize=12)
    ax.text(x[-1] / 2, 2.05, tag, ha='center', va='bottom', fontsize=12)
    for c in cross:
        ax.annotate('', xy=(x[c], D), xytext=(x[c], -D),
                    arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.7, shrinkA=0, shrinkB=0))
b.colorbar(fig, list(axs), fontsize=11.5)
style.save(fig, __file__)
