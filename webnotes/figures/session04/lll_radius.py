"""Session 4, section 4.13, the radius of the maximum of |psi_m|^2 in the lowest Landau level.

|psi_m|^2 = r^(2m) exp(-r^2 / 2 l_B^2) of (4.10) in units of l_B, each curve divided by its own maximum. The maximum is at
r_m = sqrt(2m) l_B, which is 2 sqrt(2) for m=4, 4 for m=8 and 8 for m=32. A ring of radius r encloses r^2/2 l_B^2 flux
quanta, so the ring of the orbital m encloses m of them, 4 for 2 sqrt(2) and 32 for 8, the numbers of the feedback of the
quiz. Redrawn on 2026-11-21 with the ticks of both axes, under the same name."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

r = np.linspace(1e-6, 11, 2000)


def dens(m):
    lg = 2 * m * np.log(r) - r ** 2 / 2
    return np.exp(lg - lg.max())


for m in (4, 8, 32):
    assert abs(r[np.argmax(dens(m))] - np.sqrt(2 * m)) < 0.01           # the maximum at sqrt(2m)
    assert abs(np.sqrt(2 * m) ** 2 / 2 - m) < 1e-12                      # the ring encloses m flux quanta
assert abs(np.sqrt(2 * 8) - 4) < 1e-12 and abs(np.sqrt(2 * 4) - 2 * np.sqrt(2)) < 1e-12 and abs(np.sqrt(2 * 32) - 8) < 1e-12

fig, ax = style.figure(width_cm=10.5, height_cm=4.6)
ax.set_xlim(0, 11); ax.set_ylim(0, 1.3)
for m, col in ((4, style.LIGHT), (32, style.WARM), (8, style.ACCENT)):
    ax.plot(r, dens(m), color=col, lw=1.8 if m == 8 else 1.4)
    ax.vlines(np.sqrt(2 * m), 0, 1, color=style.MUTED, lw=0.8, ls=':', zorder=0)
style.label(ax, 2.2, 1.14, r'$m=4$', color=style.LIGHT, fontsize=11)
style.label(ax, 4.2, 1.14, r'$m=8$', color=style.ACCENT, fontsize=11)
style.label(ax, 8.0, 1.14, r'$m=32$', color=style.WARM, fontsize=11)
style.arrows(ax, xlabel=r'$r/\ell_B$', ylabel=r'$|\psi_m|^2$ over its maximum')
ax.set_xticks([0, 2 * np.sqrt(2), 4, 8]); ax.set_xticklabels(['0', r'$2\sqrt{2}$', '4', '8'], fontsize=11)
ax.set_yticks([0, 1]); ax.set_yticklabels(['0', '1'], fontsize=11)
ax.tick_params(length=2.5, width=0.6, pad=2)
style.save(fig, __file__)
