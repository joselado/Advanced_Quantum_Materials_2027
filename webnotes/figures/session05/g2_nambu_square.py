"""Session 5, section 5.8, the BdG bands of the square lattice of the notebook, without and with s-wave pairing, colored by the
electron weight.

The data come from the downloadable script webnotes/scripts/session05/g2_nambu_square.py, which calls pyqula with the calls of
the notebook cell "Nambu electronic structure with superconductivity". pyqula takes the hopping as +1, so the band is
2 (cos kx + cos ky), which is eps(k) of (5.7) with t=-1, with its bottom -4 at M. set_filling(0.2, nk=20) adds the onsite energy
1.902, which is mu=-1.902, so the electron band runs from -2.098 at M to 5.902 at Gamma and the Fermi surface is a pocket of
filled states around M. It crosses the path between X and M and between M and Gamma. Panel (a) has Delta=0 and panel (b) the
add_swave(0.8) of the cell. The path holds no point exactly on the Fermi surface, so the smallest |E| on it is a bound from
above, 0.8001 against 0.8 of (5.9) on the Fermi surface."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import _g2_bdg as b
style = b.style

d = style.run_script('session05/g2_nambu_square.py')
assert abs(d['onsite'] - 1.902) < 1e-3
kp = np.array(d['kpath'])
x = b.path_x(kp, 2 * np.pi * np.eye(2))
corners = [0, 150, 300, 450]
assert np.allclose(kp[corners, :2], [[0, 0], [0.5, 0], [0.5, 0.5], [0, 0]])
k = 2 * np.pi * kp[:, :2]
eps = 2 * (np.cos(k[:, 0]) + np.cos(k[:, 1])) + d['onsite']               # the electron band of the script
assert abs(eps[300] + 2.098) < 1e-3 and abs(eps[0] - 5.902) < 1e-3
for D, e, w in zip(d['deltas'], d['energies'], d['weights']):
    b.check(e, w)
    assert np.allclose(e[:, 2], np.sqrt(eps**2 + D**2), atol=1e-9)        # (5.9) along the whole path
# the electron band crosses the Fermi level once between X and M and once between M and Gamma
cross = np.where(np.diff(np.sign(eps)) != 0)[0]
assert len(cross) == 2 and 150 <= cross[0] < 300 and 300 <= cross[1] < 450
e8 = d['energies'][3][:, 2]
near = [np.min(e8[c - 5:c + 6]) for c in cross]
assert np.allclose(near, 0.8, atol=2e-3) and abs(d['smallest'][3] - 0.8) < 2e-3    # the smallest energy 0.8 at both crossings
assert np.allclose(d['smallest'], [0, 0.2, 0.4, 0.8], atol=2e-2)
# the caption: the two drawn branches, bands 1 and 2, are 2|Delta| = 1.6 apart at both crossings
e3 = d['energies'][3]
apart = [np.min(e3[c - 5:c + 6, 2] - e3[c - 5:c + 6, 1]) for c in cross]
assert np.allclose(apart, 1.6, atol=4e-3) and abs(2 * d['deltas'][3] - 1.6) < 1e-12
print('onsite', round(d['onsite'], 4), 'crossings at steps', cross, 'smallest |E| near them for Delta=0.8', np.round(near, 4),
      'branches apart there', np.round(apart, 4), 'smallest on the path', np.round(d['smallest'], 4))

plt.rcParams.update({'font.size': 11.5})
fig, axs = plt.subplots(1, 2, figsize=(12.6 * style.CM, 5.8 * style.CM), sharey=True, gridspec_kw=dict(wspace=0.22))
kt = [(x[c], l) for c, l in zip(corners, (r'$\Gamma$', r'$X$', r'$M$', r'$\Gamma$'))]
et = [(-3, '$-3$'), (-0.8, '$-0.8$'), (0.8, '$0.8$'), (3, '$3$')]
for ax, i, tag in ((axs[0], 0, r'(a) $\Delta=0$'), (axs[1], 3, r'(b) $\Delta=0.8$')):
    style.guide(ax, y=0)
    for c in corners[1:3]:
        style.guide(ax, x=x[c], lw=0.6)
    b.bands(ax, x, d['energies'][i], d['weights'][i])
    ax.set_xlim(0, x[-1]); ax.set_ylim(-3.6, 3.6)
    b.frame(ax, kt, et, r'$\mathbf{k}$', r'$E/|t|$' if ax is axs[0] else None)
    ax.text(x[-1] / 2, 3.95, tag, ha='center', va='bottom', fontsize=11.5)
for c in cross:
    xc = x[c]
    axs[1].annotate('', xy=(xc, 0.8), xytext=(xc, -0.8),
                    arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.8, shrinkA=0, shrinkB=0))
axs[1].text(x[cross[1]] + 0.3, 0, r'$2|\Delta|$', ha='left', va='center', fontsize=11.5)
b.colorbar(fig, list(axs), fontsize=11)
style.save(fig, __file__)
