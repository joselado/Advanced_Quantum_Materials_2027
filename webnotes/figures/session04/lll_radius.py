"""Session 4, section 4.13, the radius of the maximum of |psi_m|^2 in the lowest Landau level.

|psi_m|^2 = r^(2m) exp(-r^2 / 2 l_B^2) of (4.10) in units of l_B, each curve divided by its own maximum. The maximum is at
r_m = sqrt(2m) l_B, which is 2 sqrt(2) for m=4, 4 for m=8 and 8 for m=32."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

r = np.linspace(1e-6, 11, 2000)


def dens(m):
    lg = 2 * m * np.log(r) - r ** 2 / 2
    return np.exp(lg - lg.max())


for m in (4, 8, 32):
    assert abs(r[np.argmax(dens(m))] - np.sqrt(2 * m)) < 0.01
fig, ax = style.figure(width_cm=10.5, height_cm=4.4)
ax.set_xlim(0, 11); ax.set_ylim(0, 1.3)
for m, col, lab in ((4, style.LIGHT, r'$m=4$'), (32, style.WARM, r'$m=32$'), (8, style.ACCENT, r'$m=8$')):
    ax.plot(r, dens(m), color=col, lw=1.8 if m == 8 else 1.4)
    rm = np.sqrt(2 * m)
    ax.vlines(rm, 0, 1, color=style.MUTED, lw=0.8, ls=':', zorder=0)
for m, txt, col, dx in ((4, r'$2\sqrt{2}$', style.LIGHT, 0), (8, '4', style.ACCENT, 0), (32, '8', style.WARM, 0)):
    ax.text(np.sqrt(2 * m), -0.06, txt, ha='center', va='top', fontsize=8.5, color=style.INK)
style.label(ax, 2.2, 1.12, r'$m=4$', color=style.LIGHT, fontsize=8.5)
style.label(ax, 4.0, 1.12, r'$m=8$', color=style.ACCENT, fontsize=8.5)
style.label(ax, 8.0, 1.12, r'$m=32$', color=style.WARM, fontsize=8.5)
style.arrows(ax, xlabel=r'$r/\ell_B$', ylabel=r'$|\psi_m|^2$, each divided by its maximum')
style.save(fig, __file__)
