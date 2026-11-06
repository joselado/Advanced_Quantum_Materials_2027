"""Session 5, the two signatures of the superconducting state, the resistance and the expulsion of the field."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import style

fig, axs = plt.subplots(1, 3, figsize=(style.WIDTH_CM * style.CM, 4.6 * style.CM),
                        gridspec_kw=dict(width_ratios=[1.15, 1, 1]))

# (a) the resistance, a metal that keeps a residual value and a superconductor that drops to zero at Tc
ax = axs[0]
style.arrows(ax, xlabel=r'$T$', ylabel=r'$R$')
Tc = 0.45
T = np.linspace(0, 1, 300)
Rn = 0.18 + 0.82 * T**2
ax.plot(T, Rn, color=style.MUTED, lw=1.2, ls=(0, (3, 2)))
Rs = np.where(T < Tc, 0.0, Rn)
ax.plot(T[T >= Tc], Rs[T >= Tc], color=style.ACCENT)
ax.plot(T[T < Tc], Rs[T < Tc], color=style.ACCENT)
ax.plot([Tc, Tc], [0, Rn[np.argmin(abs(T - Tc))]], color=style.ACCENT, lw=1.0)
style.guide(ax, x=Tc, color=style.MUTED, lw=0.8, ls=(0, (3, 2)))
style.label(ax, Tc, -0.09, r'$T_c$', fontsize=8.5)
style.label(ax, 0.72, 0.98, 'normal metal', color=style.MUTED, fontsize=8)
style.label(ax, 0.2, 0.12, r'$R=0$', color=style.ACCENT, fontsize=8)
style.label(ax, 0.5, 1.22, '(a) schematic', fontsize=8.5)
ax.set_xlim(0, 1.05); ax.set_ylim(-0.02, 1.15)

# (b), (c) a perfect diamagnet in a field along z: B_r = B0 cos(th)(1 - a^3/r^3), B_th = -B0 sin(th)(1 + a^3/2r^3), B=0 inside
def field(x, z, a, sc):
    r = np.hypot(x, z)
    th = np.arctan2(abs(x), z)
    sgn = np.where(x >= 0, 1.0, -1.0)
    if sc:
        Br = np.cos(th) * (1 - a**3 / r**3)
        Bt = -np.sin(th) * (1 + a**3 / (2 * r**3))
    else:
        Br, Bt = np.cos(th), -np.sin(th)
    Bx = (Br * np.sin(th) + Bt * np.cos(th)) * sgn
    Bz = Br * np.cos(th) - Bt * np.sin(th)
    if sc:
        inside = r < a
        Bx = np.where(inside, np.nan, Bx); Bz = np.where(inside, np.nan, Bz)
    return Bx, Bz

a = 1.0
g = np.linspace(-2.6, 2.6, 400)
X, Z = np.meshgrid(g, g)
for ax, sc, title in ((axs[1], False, r'(b) $T>T_c$'), (axs[2], True, r'(c) $T<T_c$')):
    Bx, Bz = field(X, Z, a, sc)
    if sc:
        # the field must vanish inside and be tangent on the surface
        r = np.hypot(X, Z); ring = (abs(r - a) < 0.01)
        Br_surf = (Bx * X + Bz * Z) / r
        assert np.nanmax(abs(Br_surf[ring])) < 0.04
    start = np.array([[x, -2.55] for x in np.linspace(-2.1, 2.1, 11)])
    ax.streamplot(X, Z, np.nan_to_num(Bx), np.nan_to_num(Bz), start_points=start, color=style.ACCENT, linewidth=1.0,
                  arrowsize=0.8, density=10, integration_direction='forward', broken_streamlines=False)
    ax.add_patch(Circle((0, 0), a, fc='#e6edf4' if not sc else style.LIGHT, ec=style.INK, lw=0.8, alpha=1.0, zorder=3))
    style.label(ax, 0, 0, 'sample', fontsize=8, zorder=4, color=style.INK if not sc else 'white')
    ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.6, 2.6); ax.set_aspect('equal'); ax.axis('off')
    style.label(ax, 0, 2.95, title, fontsize=8.5)
style.save(fig, __file__)
