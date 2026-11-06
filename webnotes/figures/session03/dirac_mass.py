"""Session 3, section 3.10, a gapped Dirac cone H = kx sx + lambda ky sy + m sz with lambda=+1, in units of |m|.

Panel (a) the bands +-sqrt(k^2+m^2), which are the same for m>0 and m<0. Panel (b) the Berry curvature of the lower
band, Omega = lambda m / (2 (k^2+m^2)^(3/2)), checked below against -2 Im <d_kx u|d_ky u> of (3.4) on the
eigenvectors. The integral of Omega over the plane divided by 2 pi is sgn(m) sgn(lambda) / 2, as in (3.8)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

sx = np.array([[0, 1], [1, 0]], complex); sy = np.array([[0, -1j], [1j, 0]]); sz = np.diag([1, -1]).astype(complex)


def lower(kx, ky, m, lam):
    v = np.linalg.eigh(kx * sx + lam * ky * sy + m * sz)[1][:, 0]
    return v * np.exp(-1j * np.angle(v[0]))          # smooth gauge away from the origin


def omega_numeric(kx, ky, m, lam, h=1e-5):
    dx = (lower(kx + h, ky, m, lam) - lower(kx - h, ky, m, lam)) / (2 * h)
    dy = (lower(kx, ky + h, m, lam) - lower(kx, ky - h, m, lam)) / (2 * h)
    return -2 * np.imag(np.vdot(dx, dy))


def omega(k, m, lam=1):
    return lam * m / (2 * (k ** 2 + m ** 2) ** 1.5)


for m in (0.5, -0.5, 1.0):
    for lam in (1, -1):
        assert abs(omega_numeric(0.3, 0.2, m, lam) - omega(np.hypot(0.3, 0.2), m, lam)) < 1e-4
# the integral over the plane, 2 pi k dk, divided by 2 pi
k = np.linspace(0, 400, 400_001)
for m in (1.0, -1.0):
    print('C =', np.trapezoid(omega(k, m) * k, k))

k = np.linspace(-4, 4, 600)
fig, axs = style.figure(ncols=2, height_cm=5.2, gridspec_kw=dict(wspace=0.32))
ax = axs[0]
ax.set_xlim(-4, 4); ax.set_ylim(-4.3, 4.6)
ax.plot(k, np.abs(k), color=style.GRID, lw=1.2, ls=':')
ax.plot(k, -np.abs(k), color=style.GRID, lw=1.2, ls=':')
E = np.sqrt(k ** 2 + 1)
ax.plot(k, E, color=style.ACCENT)
ax.plot(k, -E, color=style.ACCENT)
ax.annotate('', xy=(0, 1), xytext=(0, -1), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.7, shrinkA=0, shrinkB=0))
style.label(ax, 0.2, 0, r'$2|m|$', ha='left', fontsize=8.5)
style.arrows(ax, xlabel=r'$k_x$', ylabel=r'$E$')
ax.text(0.5, -0.05, '(a) the bands, the same for both signs of $m$', transform=ax.transAxes, ha='center', va='top', fontsize=8.5)
style.label(ax, 3.0, 1.9, 'massless', color=style.MUTED, fontsize=8, rotation=0)
ax = axs[1]
ax.set_xlim(-4, 4); ax.set_ylim(-0.62, 0.62)
kk = np.linspace(-4, 4, 600)
ax.fill_between(kk, 0, omega(np.abs(kk), 1), color=style.ACCENT, alpha=0.18, lw=0)
ax.fill_between(kk, 0, omega(np.abs(kk), -1), color=style.BROKEN, alpha=0.18, lw=0)
ax.plot(kk, omega(np.abs(kk), 1), color=style.ACCENT)
ax.plot(kk, omega(np.abs(kk), -1), color=style.BROKEN)
style.guide(ax, y=0, color=style.INK, lw=0.5, zorder=1)
style.arrows(ax, xlabel=r'$k_x$', ylabel=r'$\Omega$')
style.label(ax, 1.85, 0.36, r'$m>0$, $C=+\frac{1}{2}$', color=style.ACCENT, fontsize=8.5, ha='left')
style.label(ax, 1.85, -0.36, r'$m<0$, $C=-\frac{1}{2}$', color=style.BROKEN, fontsize=8.5, ha='left')
ax.text(0.5, -0.05, '(b) the Berry curvature of the lower band', transform=ax.transAxes, ha='center', va='top', fontsize=8.5)
style.save(fig, __file__)
