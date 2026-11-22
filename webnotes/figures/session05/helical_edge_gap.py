"""Session 5, the helical edge of a quantum spin Hall insulator with a magnet and with pairing.

(a) The edge bands H0(k) = v k sigma_z, spin up moving right and spin down moving left, and the same edge under a
magnet, H0 + h sigma_x with h=0.7, where a gap 2h opens at k=0. E and v k are in the same unit.
(b) The BdG Hamiltonian of the edge in the Nambu basis (5.6), H = tau_z (v k sigma_z - mu) + h sigma_x + Delta tau_x,
diagonalized at k=0 as a function of h, for mu=0, in units of Delta. The four levels are +-h +- Delta, and the gap
closes at h=Delta. A region gapped by pairing (h<Delta) and a region gapped by the magnet (h>Delta) cannot be joined
without closing the gap, which is why a Majorana zero mode sits at the interface between a magnet and a superconductor.

Redrawn on 2026-11-21 with ticks at +-h in (a) and at +-1 and h/Delta=1 in (b), and with the units in the names of the
axes, which the old figure did not have. The model is the one of _g6_edge.py, which the quiz pictures of the page use.
It is a continuum model that pyqula does not have, so the figure is numpy and has no download."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g6_edge as edge
from _g6_edge import style, plt

v, mu, D = 1.0, 0.0, 1.0
k = np.linspace(-2.2, 2.2, 401)
h_a = 0.7
up, dn = v * k, -v * k                                   # the two helical branches, sigma_z = +1 and -1
mag = np.array([np.linalg.eigvalsh(v * kk * edge.SZ + h_a * edge.SX) for kk in k])
assert abs((mag[200, 1] - mag[200, 0]) - 2 * h_a) < 1e-12        # the gap 2h at k=0
assert np.allclose(mag[:, 1], np.sqrt((v * k)**2 + h_a**2))      # the solid lines are +-sqrt(v^2 k^2 + h^2)

hs = np.linspace(0, 2.2, 441)
lev = np.array([np.linalg.eigvalsh(edge.bdg(0.0, h, D, mu, v)) for h in hs])
# the full gap over k, not only at k=0, closes at h=Delta and nowhere else
kk = np.linspace(-3, 3, 1201)
gap = np.array([min(abs(np.linalg.eigvalsh(edge.bdg(q, h, D, mu, v))).min() for q in kk) for h in hs[::10]])
assert gap[np.argmin(abs(hs[::10] - D))] < 1e-9 and np.all(gap[abs(hs[::10] - D) > 0.05] > 0.04)
assert np.allclose(np.sort(lev, axis=1), np.sort(np.c_[hs + D, hs - D, -hs + D, -hs - D], axis=1))
assert np.allclose(np.sort(lev[0]), [-1, -1, 1, 1])               # at h=0 the levels are +-Delta, the ticks +-1

FS = 11
plt.rcParams.update({'font.size': FS})
fig, axs = plt.subplots(1, 2, figsize=(13.0 * style.CM, 6.0 * style.CM), gridspec_kw=dict(wspace=0.42))
ax = axs[0]
style.guide(ax, y=0)
ax.plot(k, up, color=style.BROKEN, lw=1.6, ls=(0, (4, 2)))
ax.plot(k, dn, color=style.ACCENT, lw=1.6, ls=(0, (4, 2)))
ax.plot(k, mag[:, 0], color=style.INK, lw=2.0)
ax.plot(k, mag[:, 1], color=style.INK, lw=2.0)
ax.annotate('', xy=(0, h_a), xytext=(0, -h_a), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.9, shrinkA=0, shrinkB=0))
style.label(ax, 0.42, 0.0, '$2h$', ha='left', fontsize=FS)
style.label(ax, 1.65, 2.2, r'$\uparrow$', color=style.BROKEN, fontsize=FS + 3)
style.label(ax, -1.65, 2.2, r'$\downarrow$', color=style.ACCENT, fontsize=FS + 3)
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.6, 2.6)
edge.frame(ax, [(-2, '$-2$'), (0, '0'), (2, '2')], [(-h_a, '$-0.7$'), (0, '0'), (h_a, '$0.7$')], r'$vk$', r'$E$', FS)
ax.text(-0.22, 1.04, '(a)', transform=ax.transAxes, fontsize=FS, ha='left', va='bottom')

ax = axs[1]
style.guide(ax, y=0)
style.guide(ax, x=D, color=style.MUTED, lw=0.8, ls=(0, (3, 2)))
for j in range(4):
    ax.plot(hs, lev[:, j], color=style.ACCENT, lw=1.6)
ax.plot(D, 0, 'o', color=style.BROKEN, ms=5, zorder=5)
style.label(ax, 0.45, -2.55, 'pairing', fontsize=FS - 1)
style.label(ax, 1.68, -1.75, 'magnet', fontsize=FS - 1)
ax.set_xlim(0, 2.2); ax.set_ylim(-3.3, 3.3)
edge.frame(ax, [(0, '0'), (1, '1'), (2, '2')], [(-2, '$-2$'), (-1, '$-1$'), (0, '0'), (1, '1'), (2, '2')],
           r'$h/\Delta$', r'$E/\Delta$', FS)
ax.text(-0.22, 1.04, '(b)', transform=ax.transAxes, fontsize=FS, ha='left', va='bottom')
style.save(fig, __file__)
