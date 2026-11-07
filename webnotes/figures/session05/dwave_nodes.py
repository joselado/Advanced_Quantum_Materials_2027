"""Session 5, the d-wave gap (5.13) on the Fermi surface of the square lattice, and where the spectrum is gapless.

(a) The Fermi surface of eps(k) = -2t(cos kx + cos ky) - mu for mu = -t, drawn in the color of the sign of
Delta_d(k) = Delta0 (cos kx - cos ky), with the zone diagonals where Delta_d vanishes.
(b) The smallest quasiparticle energy E = sqrt(eps^2 + Delta^2) of (5.9) along each ray from Gamma, against the
angle of the ray, for the d-wave gap and for an s-wave gap of the same Delta0. The d-wave curve goes to zero on the
diagonals, which are the nodes.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from scipy.optimize import brentq
import style

t, mu, D0 = 1.0, -1.0, 0.2
eps = lambda kx, ky: -2 * t * (np.cos(kx) + np.cos(ky)) - mu
dd = lambda kx, ky: D0 * (np.cos(kx) - np.cos(ky))

th = np.linspace(0, 2 * np.pi, 721)
kF = np.array([brentq(lambda r: eps(r * np.cos(a), r * np.sin(a)), 1e-6, np.pi) for a in th])
fx, fy = kF * np.cos(th), kF * np.sin(th)
gap_on_fs = dd(fx, fy)

# the smallest E along each ray, computed on a fine radial mesh, not read off the Fermi surface
r = np.linspace(0, np.pi, 4001)
Emin_d = np.array([np.sqrt(eps(r * np.cos(a), r * np.sin(a))**2 + dd(r * np.cos(a), r * np.sin(a))**2).min() for a in th])
Emin_s = np.array([np.sqrt(eps(r * np.cos(a), r * np.sin(a))**2 + D0**2).min() for a in th])
# the checks of what the figure says: zero on the four diagonals, the s-wave gap is D0 everywhere
for a in (np.pi / 4, 3 * np.pi / 4, 5 * np.pi / 4, 7 * np.pi / 4):
    assert Emin_d[np.argmin(abs(th - a))] < 2e-3
assert np.allclose(Emin_s, D0, atol=1e-4) and abs(Emin_d.max() / D0 - 1.5) < 0.02

FS = 12
style.plt.rcParams['font.size'] = FS          # labels of the arrows too, for a phone
fig, axs = style.figure(height_cm=6.0, width_cm=13.0, ncols=2, gridspec_kw=dict(width_ratios=[1, 1.35], wspace=0.32))
ax = axs[0]
for t_ in list(ax.texts):                          # no arrow axes on the zone, it is a map of k
    t_.remove()
ax.set_aspect('equal')
L = np.pi
ax.plot([-L, L, L, -L, -L], [-L, -L, L, L, -L], color=style.MUTED, lw=0.8)
for s in (1, -1):
    ax.plot([-L, L], [-s * L, s * L], color=style.MUTED, lw=0.8, ls=(0, (3, 2)))
pos = np.where(gap_on_fs >= 0, 1.0, np.nan); neg = np.where(gap_on_fs <= 0, 1.0, np.nan)
ax.plot(fx * pos, fy * pos, color=style.ACCENT, lw=2.4)
ax.plot(fx * neg, fy * neg, color=style.BROKEN, lw=2.4)
for a in (np.pi / 4, 3 * np.pi / 4, 5 * np.pi / 4, 7 * np.pi / 4):
    i = np.argmin(abs(th - a))
    ax.plot(fx[i], fy[i], 'o', color=style.INK, ms=4.5, zorder=5)
sx = '$+$' if dd(2.0, 0) > 0 else '$-$'       # the sign along k_x, read from (5.13) and not assumed
sy = '$+$' if dd(0, 2.0) > 0 else '$-$'
cx = style.ACCENT if dd(2.0, 0) > 0 else style.BROKEN
cy = style.ACCENT if dd(0, 2.0) > 0 else style.BROKEN
for s_ in (1, -1):
    style.label(ax, s_ * 2.62, 0, sx, color=cx, fontsize=FS + 4)
    style.label(ax, 0, s_ * 2.62, sy, color=cy, fontsize=FS + 4)
style.label(ax, 0.62, 0, r'$\Gamma$', fontsize=FS + 1)
ax.plot(0, 0, 'o', color=style.INK, ms=2.5)
ax.text(0.0, 1.087, '(a)', transform=ax.transAxes, fontsize=FS, ha='left', va='center')
ax.set_xlim(-L - 0.1, L + 0.1); ax.set_ylim(-L - 0.1, L + 0.1)
ax.axis('off')

ax = axs[1]
ax.plot(th, Emin_s / D0, color=style.MUTED, lw=1.6)
ax.plot(th, Emin_d / D0, color=style.ACCENT)
for a in (np.pi / 4, 3 * np.pi / 4, 5 * np.pi / 4, 7 * np.pi / 4):
    style.guide(ax, x=a)
    ax.plot(a, 0, 'o', color=style.INK, ms=4.5, zorder=5, clip_on=False)
style.arrows(ax, xlabel=r'$\theta$', ylabel=r'$E_{\min}$')
for a, lab in ((0, '$0$'), (np.pi / 2, r'$\pi/2$'), (np.pi, r'$\pi$'), (3 * np.pi / 2, r'$3\pi/2$'), (2 * np.pi, r'$2\pi$')):
    style.label(ax, a, -0.17, lab, fontsize=FS - 0.5, va='top')
ax.text(-0.12, 1.0, '$1$', ha='right', va='center', fontsize=FS - 0.5)
style.label(ax, 2 * np.pi + 0.12, 1.0, r'$s$-wave', color=style.MUTED, fontsize=FS, ha='left')
style.label(ax, np.pi / 2, 1.75, r'$d$-wave', color=style.ACCENT, fontsize=FS)
style.label(ax, -1.85, 2.12, '(b)', fontsize=FS, ha='left')
ax.set_xlim(0, 2 * np.pi); ax.set_ylim(0, 1.95)
style.save(fig, __file__)
