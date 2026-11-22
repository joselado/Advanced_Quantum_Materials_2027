"""Session 8, Section 8.13, the bands of the Kondo lattice of the notebook cell "Quantum magnetism in the Kondo lattice",
for the three values JK = 0, 0.25 and 0.5 of the notebook, colored by their weight on the conduction electrons.

The data come from the downloadable script webnotes/scripts/session08/g4_kondo_lattice_bands.py, which calls pyqula:
the triangular lattice with the hopping +1, which is t = -1 in the sign of (8.18), add_onsite(-2.0) and H2HFH(h, JK=...).
JK is the hopping between a conduction site and its Kondo site, the hybridization gamma_K of (8.21) up to its sign. The
check script of Section 8.13 asserts these two signs and the gaps again with pyqula. The asserts here are the numbers
of the caption: the conduction band from -5 to 4 with the top at Gamma and the bottom at K, both outside the window of
the plot, the flat level at zero, the direct gaps 2 JK,
the indirect gaps 0.028 and 0.111 from the top of the lower bands at Gamma to the bottom of the upper bands at K, on
the path and on the mesh of 90 points per side, and the energy zero inside them. The 0.46 and 0.48 f fermions per site
below zero are computed on the mesh by the check script of the page, and this one asserts only that the f weight of the
lower bands on the path is below one half."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import _g4_kondo as kd
style = kd.style

d = style.run_script('session08/g4_kondo_lattice_bands.py')
A = np.array([[1., 0.], [-0.5, np.sqrt(3) / 2]])                    # the lattice vectors of geometry.triangular_lattice()
B = 2 * np.pi * np.linalg.inv(A).T
kp = np.array(d['kpath'])[:, :2]
kc = kp @ B
x = np.r_[0, np.cumsum(np.linalg.norm(np.diff(kc, axis=0), axis=1))]
corners = [0, 150, 300, 450]
assert np.allclose(kp[corners], [[0, 0], [1 / 3, 1 / 3], [0.5, 0], [0, 0]])
assert abs(np.linalg.norm(kc[150]) - 4 * np.pi / 3) < 1e-9 and abs(np.linalg.norm(kc[300]) - 2 * np.pi / np.sqrt(3)) < 1e-9
k1, k2 = 2 * np.pi * kp[:, 0], 2 * np.pi * kp[:, 1]
eps = 2 * (np.cos(k1) + np.cos(k2) + np.cos(k1 + k2)) - 2.0          # the conduction band with add_onsite(-2.0)
assert abs(eps[0] - 4) < 1e-12 and abs(eps[150] + 5) < 1e-12        # top 4 at Gamma, bottom -5 at K
YL = 1.4                                                            # the window of the plot, -YL to YL
assert eps.min() < -YL and eps.max() > YL                           # the caption: -5 and 4 lie outside the window
assert d['couplings'] == [0., 0.25, 0.5]
for JK, e, w, dg, ig in zip(d['couplings'], d['energies'], d['weights'], d['direct'], d['indirect']):
    assert e.shape == (451, 4) and np.allclose(e[:, 0], e[:, 1], atol=1e-9) and np.allclose(e[:, 2], e[:, 3], atol=1e-9)
    lo, up = kd.bands_formula(eps, JK)
    assert np.allclose(e[:, 1], lo, atol=1e-9) and np.allclose(e[:, 2], up, atol=1e-9)    # the 2x2 matrix of (8.21)
    assert abs(dg - 2 * JK) < 1e-9                                                         # direct gap 2 JK
    if JK > 0:
        assert np.argmax(e[:, 1]) == 0 and np.argmin(e[:, 2]) == 150                       # top at Gamma, bottom at K
        path_gap = e[:, 2].min() - e[:, 1].max()
        assert abs(path_gap - ig) < 1e-9 and e[:, 1].max() < 0 < e[:, 2].min()             # the same gap on the mesh
        # the f weight of the two lower bands, per spin, on the path: below one half, so less than one f per site
        assert np.mean(1 - w[:, 1]) < 0.5
    else:
        assert abs(ig) < 1e-12
assert abs(d['indirect'][1] - 0.028) < 5e-4 and abs(d['indirect'][2] - 0.111) < 5e-4
print('direct gaps', np.round(d['direct'], 4), 'indirect gaps on the path and the mesh', np.round(d['indirect'], 4))

plt.rcParams.update({'font.size': 12})
fig, axs = plt.subplots(1, 3, figsize=(14.2 * style.CM, 5.8 * style.CM), sharey=True, gridspec_kw=dict(wspace=0.2))
kt = [(x[c], l) for c, l in zip(corners, (r'$\Gamma$', r'$K$', r'$M$', r'$\Gamma$'))]
et = [(-1, r'$-1$'), (-0.5, r'$-0.5$'), (0, r'$0$'), (0.5, r'$0.5$'), (1, r'$1$')]
for ax, JK, e, w in zip(axs, d['couplings'], d['energies'], d['weights']):
    style.arrows(ax, xlabel=r'$\mathbf{k}$', ylabel=r'$E/|t|$' if ax is axs[0] else None)     # t = -1 here
    style.guide(ax, y=0, ls=(0, (3, 2)), color=style.MUTED, lw=0.8)
    for c in corners[1:3]:
        style.guide(ax, x=x[c], lw=0.6)
    for n in (1, 2):
        kd.colored(ax, x, e[:, n], w[:, n], lw=1.7)
    ax.set_xlim(0, x[-1]); ax.set_ylim(-YL, YL)
    kd.ticks(ax, kt, et, fontsize=11)
    if ax is not axs[0]:
        ax.tick_params(axis='y', left=False, labelleft=False)
    ax.text(x[-1] / 2, 1.5, r'$\mathtt{JK}=%g$' % JK, ha='center', va='bottom', fontsize=11.5)
    for t in ax.texts:
        t.set_fontsize(11.5)
kd.colorbar(fig, list(axs), fontsize=11)
style.save(fig, __file__)
