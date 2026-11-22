"""Session 1, two gaps that look alike. A band gap of the lattice and a pairing gap of the electrons.

Redrawn on 2026-11-21 with its axes, from the downloadable pyqula script webnotes/scripts/session01/g1_two_gaps.py.
On the left the chain with two sites per cell (geometry.bichain) with the hopping -1 and the onsite energies +-m,
m = 0.6, whose bands are +-sqrt(m^2 + 4t^2 cos^2 k). On the right the half-filled chain with one site per cell, the
band xi = -2t cos k, with the s-wave pairing h.add_swave(0.6), whose Bogoliubov-de Gennes bands are
+-sqrt(xi^2 + Delta^2). The momentum k is per site, from -pi to pi in both panels, so the chain with two sites per
cell is drawn over two of its zones, whose edges k = +-pi/2 are dashed. The grey lines are the bands without the gap,
+-2t cos k in both panels. For m = Delta the two spectra are the same curves, which is asserted below."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

d = style.run_script('session01/g1_two_gaps.py')
k, semi, sc = np.array(d['k']), np.array(d['semiconductor']), np.array(d['superconductor'])
m = Delta = 0.6
E = np.sqrt(m ** 2 + 4 * np.cos(k) ** 2)
assert np.allclose(semi, np.array([-1, 1]) * E[:, None], atol=1e-12)            # +-sqrt(m^2 + (2t cos k)^2)
assert np.allclose(sc, np.array([-1, -1, 1, 1]) * E[:, None], atol=1e-12)       # +-sqrt(xi^2 + Delta^2), twice
assert abs(d['gap_semiconductor'] - 2 * m) < 1e-12 and abs(d['gap_superconductor'] - 2 * Delta) < 1e-12
assert abs(d['gap_semiconductor'] - 1.2) < 1e-12                                 # both gaps are 1.2t
assert np.allclose(semi[:, 1], sc[:, 2], atol=1e-12)                              # the same curves for m = Delta
edges = k[np.isclose(semi[:, 1], semi[:, 1].min(), atol=1e-12)]
assert np.allclose(np.sort(edges), [-np.pi / 2, np.pi / 2], atol=1e-12)          # both gaps sit at k = +-pi/2
print('gaps', d['gap_semiconductor'], d['gap_superconductor'], 'at k =', edges)

FS = 11
fig, axs = plt.subplots(1, 2, figsize=(12.0 * style.CM, 5.6 * style.CM))
for ax, bands, title, name in ((axs[0], semi, 'semiconductor', r'$2m$'), (axs[1], sc[:, 1:3], 'superconductor', r'$2\Delta$')):
    ax.plot(k, 2 * np.cos(k), color=style.GRID, lw=1.2, zorder=1)
    ax.plot(k, -2 * np.cos(k), color=style.GRID, lw=1.2, zorder=1)
    ax.plot(k, bands[:, 0], color=style.ACCENT, zorder=2)
    ax.plot(k, bands[:, 1], color=style.ACCENT, zorder=2)
    style.arrows(ax, xlabel=r'$k$', ylabel=r'$E/t$', ticks=True)
    ax.spines['left'].set_visible(True); ax.spines['bottom'].set_visible(True)
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-2.5, 2.5)
    ax.set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
    ax.set_xticklabels([r'$-\pi$', r'$-\frac{\pi}{2}$', '0', r'$\frac{\pi}{2}$', r'$\pi$'], fontsize=FS)
    ax.set_yticks([-2, -0.6, 0.6, 2]); ax.set_yticklabels(['$-2$', '$-0.6$', '0.6', '2'], fontsize=FS)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_title(title, fontsize=FS + 0.5, pad=12)
    ax.annotate('', xy=(np.pi / 2, 0.6), xytext=(np.pi / 2, -0.6),
                arrowprops=dict(arrowstyle='<->', color=style.BROKEN, lw=0.9, shrinkA=0, shrinkB=0))
    style.label(ax, np.pi / 2 + 0.22, 0.0, name, color=style.BROKEN, ha='left', fontsize=FS + 0.5)
for x in (-np.pi / 2, np.pi / 2):
    axs[0].axvline(x, color=style.MUTED, lw=0.7, ls=(0, (2, 2)), zorder=0)
fig.subplots_adjust(wspace=0.48)
style.save(fig, __file__)
