"""Session 6, the moment of the half-filled chain against U, and the fraction of doubly occupied sites that is left."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import style, _mf

Us = np.concatenate([np.linspace(0.4, 4, 25), np.linspace(4.5, 24, 60)])
m = np.array([_mf.moment(U) for U in Us])
assert m[-1] > 0.98 and np.all(np.diff(m) > 0) and abs(_mf.moment(4.0) - 0.7) < 0.2
double = (1 - m**2) / 4          # <n_up n_down> per site in the mean-field state, n_up,down = (1 +- m)/2 on a site
fig, ax = style.figure(height_cm=5.4)
ax.plot(Us, m, color=style.ACCENT)
ax.plot(Us, 4 * double, color=style.BROKEN)
style.guide(ax, y=1.0, color=style.MUTED, lw=0.8, ls=(0, (3, 2)))
style.arrows(ax, xlabel=r'$U/t$', ylabel='')
style.label(ax, 14.5, 0.86, r'$|m|$, the moment on a site', color=style.ACCENT, fontsize=8.5)
style.label(ax, 11.8, 0.20, r'$4\langle n_\uparrow n_\downarrow\rangle=1-m^2$', color=style.BROKEN, fontsize=8.5)
style.label(ax, 0.2, 1.05, r'$1$', fontsize=8.5, color=style.MUTED)
ax.set_xticks([4, 16]); ax.set_xticklabels(['4', '16']); ax.tick_params(axis='x', length=2)
ax.set_xlim(0, 24); ax.set_ylim(0, 1.12)
style.save(fig, __file__)
print('m at U=4,8,16,24:', [round(_mf.moment(U), 3) for U in (4, 8, 16, 24)])
