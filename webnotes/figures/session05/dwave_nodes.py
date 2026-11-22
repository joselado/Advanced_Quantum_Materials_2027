"""Session 5, the d-wave gap (5.13) on the Fermi surface of the square lattice, and where the spectrum is gapless.

Redrawn on 2026-11-21 from the downloadable pyqula script g3_dwave_square.py, with the axes k_x and k_y, the first
Brillouin zone dashed and E_min in units of Delta0, which the old figure did not have. The model is the square lattice
with t=1 (tij=[-1.]), mu=-t (add_onsite(1.0)) and add_pairing(mode="dx2y2", delta=0.1), which is Delta0 = 2 delta = 0.2
of (5.13), as webnotes/conventions/session05.md says. The s-wave reference is add_swave(0.2).
(a) Delta_d(k)/Delta0 over reciprocal space, in the extended zone, with the Fermi surface eps(k)=0 as a black line and
the nodes, where the Fermi surface crosses the diagonals, as dots.
(b) The smallest quasiparticle energy along each direction from Gamma, at the angle theta, in units of Delta0, for the
d-wave and for the s-wave pairing. It is taken on the mesh of each direction of the script.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
plt = style.plt

d = style.run_script('session05/g3_dwave_square.py')
t, mu, D0 = 1.0, -1.0, 0.2
ks, P, E = np.array(d['ks']), np.array(d['pairing']), np.array(d['band'])
th, Ed, Es = np.array(d['thetas']), np.array(d['smallest_d']), np.array(d['smallest_s'])

# the checks of the model against (5.13) and the band of the notes, on the grid of the script
KX, KY = np.meshgrid(2 * np.pi * ks, 2 * np.pi * ks, indexing='ij')       # the first index runs along k_x
assert np.allclose(P, D0 * (np.cos(KX) - np.cos(KY)), atol=1e-12)          # Delta_0 = 2 delta = 0.2
assert np.allclose(E, -2 * t * (np.cos(KX) + np.cos(KY)) - mu, atol=1e-12)  # eps(k) with mu = -t
# the nodes: on the diagonal eps = -4t cos k0 - mu = 0, so cos k0 = 1/4, k0 = 1.318, where Delta_d = 0
k0 = np.arccos(-mu / (4 * t))
assert round(k0, 3) == 1.318
# (b) zero at the four nodes, below 0.01 Delta0 on the mesh, and 1.49 Delta0 along the axes, s-wave Delta0 everywhere
nodes = [np.argmin(abs(th - a)) for a in (np.pi / 4, 3 * np.pi / 4, 5 * np.pi / 4, 7 * np.pi / 4)]
assert np.allclose(th[nodes], np.pi / 4 * np.array([1, 3, 5, 7]), atol=1e-12)
assert np.all(Ed[nodes] / D0 < 0.01), Ed[nodes] / D0
assert abs(Ed.max() / D0 - 1.49) < 0.005 and abs(Ed[0] - Ed.max()) < 1e-9
assert np.allclose(Es / D0, 1, atol=1e-4)
# the smallest energy along a direction is reached next to the Fermi surface, at most one step of the mesh from it
rs = 2 * np.pi * np.array(d['rs'])
for a, e in zip(th[::6], Ed[::6]):
    kF = rs[np.argmin(abs(-2 * t * (np.cos(rs * np.cos(a)) + np.cos(rs * np.sin(a))) - mu))]
    assert abs(np.sqrt((D0 * (np.cos(kF * np.cos(a)) - np.cos(kF * np.sin(a)))) ** 2) - e) < 0.02 * D0 + 1e-3

FS = 13.5
fig = plt.figure(figsize=(14.2 * style.CM, 6.6 * style.CM))
ax = fig.add_axes([0.07, 0.17, 0.33, 0.73])
cax = fig.add_axes([0.415, 0.17, 0.018, 0.73])
bx = fig.add_axes([0.62, 0.17, 0.35, 0.66])

# (a) the map in the extended zone: the grid of the script without its last row is one period
N = len(ks) - 1
idx = np.arange(-58, 59)                                                  # about 1.16 pi on each side
sel = (idx + N // 2) % N
X = 2 * np.pi * idx / N
Pe, Ee = (P[:-1, :-1] / D0)[np.ix_(sel, sel)], E[:-1, :-1][np.ix_(sel, sel)]
assert np.allclose(Pe, np.cos(X)[:, None] - np.cos(X)[None, :], atol=1e-12)
im = ax.pcolormesh(X, X, Pe.T, shading='nearest', cmap='RdBu_r', vmin=-2, vmax=2, rasterized=True)
ax.contour(X, X, Ee.T, levels=[0], colors=style.INK, linewidths=1.4)
style.draw_zone(ax, 2 * np.pi * np.eye(2))
for sx in (1, -1):
    for sy in (1, -1):
        ax.plot(sx * k0, sy * k0, 'o', color=style.INK, ms=4.5, zorder=6)
ax.set_aspect('equal'); ax.set_xlim(X[0], X[-1]); ax.set_ylim(X[0], X[-1])
style.kaxes(ax, ticks=np.pi, fontsize=FS)
ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$']); ax.set_yticklabels([r'$-\pi$', '0', r'$\pi$'])
ax.text(0.0, 1.05, '(a)', transform=ax.transAxes, fontsize=FS, ha='left', va='bottom')
cb = fig.colorbar(im, cax=cax, ticks=[-2, 0, 2])
cb.ax.set_yticklabels(['$-2$', '0', '2'], fontsize=FS - 1)
cb.set_label(r'$\Delta_d/\Delta_0$', fontsize=FS, labelpad=-2)
cb.outline.set_linewidth(0.5); cb.ax.tick_params(length=2, width=0.5)

# (b) the smallest energy against the direction
for a in th[nodes]:
    style.guide(bx, x=a)
    bx.plot(a, 0, 'o', color=style.INK, ms=4.5, zorder=5, clip_on=False)
bx.plot(th, Es / D0, color=style.MUTED, lw=1.6)
bx.plot(th, Ed / D0, color=style.ACCENT, lw=1.8)
for s in ('top', 'right'):
    bx.spines[s].set_visible(False)
for s in ('left', 'bottom'):
    bx.spines[s].set_linewidth(0.6)
bx.set_xlim(0, 2 * np.pi); bx.set_ylim(0, 1.75)
bx.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
bx.set_xticklabels(['0', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$'], fontsize=FS - 1)
bx.set_yticks([0, 0.5, 1, 1.5]); bx.set_yticklabels(['0', '0.5', '1', '1.5'], fontsize=FS - 1)
bx.tick_params(length=2.5, width=0.6, pad=2)
bx.set_xlabel(r'$\theta$', fontsize=FS, labelpad=1)
bx.set_ylabel(r'$E_{\min}/\Delta_0$', fontsize=FS, labelpad=2)
style.label(bx, 2 * np.pi + 0.15, 1.0, r'$s$', color=style.MUTED, fontsize=FS, ha='left', clip_on=False)
style.label(bx, 2 * np.pi + 0.15, 1.49, r'$d$', color=style.ACCENT, fontsize=FS, ha='left', clip_on=False)
bx.text(0.0, 1.13, '(b)', transform=bx.transAxes, fontsize=FS, ha='left', va='bottom')
style.save(fig, __file__)
