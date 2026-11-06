"""Session 9, the mean-field susceptibility of Eq. (9.1), drawn as 1/chi, which is a straight line in each case."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

Tc = 1.0
T = np.linspace(-1.3, 3.2, 400)
fig, ax = style.figure(height_cm=5.6)
style.arrows(ax, xlabel=r'$T$', ylabel=r'$1/\chi$')
ax.set_xlim(-1.4, 3.3); ax.set_ylim(-0.2, 4.4)
for sh, col, name, tmin in ((0.0, style.MUTED, r'paramagnet, $1/\chi\propto T$', 0.0),
                            (-Tc, style.ACCENT, r'ferromagnet, $T-T_c$', Tc),
                            (+Tc, style.BROKEN, r'antiferromagnet, $T+T_c$', 0.0)):
    inv = T + sh
    full = (T >= tmin) if sh != 0 else (T >= 0)
    ax.plot(T[full], inv[full], color=col)
    ax.plot(T[~full], inv[~full], color=col, ls=(0, (3, 3)), lw=1.2)
ax.plot([Tc], [0], 'o', color=style.ACCENT, ms=4)
ax.plot([-Tc], [0], 'o', color=style.BROKEN, ms=4)
style.label(ax, Tc, -0.45, r'$T_c$', color=style.ACCENT)
style.label(ax, -Tc, -0.45, r'$-T_c$', color=style.BROKEN)
style.label(ax, 0, -0.45, r'$0$')
style.label(ax, 2.55, 1.15, r'ferromagnet', color=style.ACCENT, ha='left', rotation=0, fontsize=8.5)
style.label(ax, 2.0, 3.7, r'antiferromagnet', color=style.BROKEN, ha='left', fontsize=8.5)
style.label(ax, 2.2, 2.15, r'paramagnet', color=style.MUTED, ha='left', fontsize=8.5)
style.save(fig, __file__)
