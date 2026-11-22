"""Session 9, the mean-field susceptibility of Eq. (9.1), drawn as 1/chi, which is a straight line in each case.

Redrawn on 2026-11-22 with the axes of the rule of 2026-11-21: the temperature and 1/chi in units of T_c, with ticks,
in the units of the steps fold of Section 9.2, where the field and T have the same unit and a free spin has chi = 1/T.
The dots are the self-consistent two-sublattice mean field of _g1_curie.loop in a small field, which falls on the
lines. The disordered phase of both magnets starts at T_c, since the antiferromagnet orders at T_c too, so both lines
are solid above T_c and dashed below it. The old figure drew the line of the antiferromagnet solid from T = 0."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
import _g1_curie

_g1_curie.check_fold()
TDOTS = np.array([1.5, 2.0, 2.5, 3.0])
dots = {name: np.array([_g1_curie.loop(T, zJ) for T in TDOTS]) for name, zJ in
        (('para', 0.0), ('ferro', 1.0), ('anti', -1.0))}
assert np.allclose(dots['para'], TDOTS, atol=1e-5) and np.allclose(dots['ferro'], TDOTS - 1, atol=1e-5)
assert np.allclose(dots['anti'], TDOTS + 1, atol=1e-5)

T = np.linspace(-1.3, 3.2, 400)
fig, ax = style.figure(height_cm=5.8)
style.arrows(ax, xlabel=r'$T$', ylabel=r'$1/\chi$', ticks=True)
ax.set_xlim(-1.4, 4.1); ax.set_ylim(-0.25, 4.4)
style.guide(ax, y=0)
for sh, col, tmin, key in ((0.0, style.MUTED, 0.0, 'para'), (-1.0, style.ACCENT, 1.0, 'ferro'),
                           (+1.0, style.BROKEN, 1.0, 'anti')):
    inv = T + sh
    full = T >= tmin
    keep = inv >= -0.25
    ax.plot(T[full], inv[full], color=col)
    ax.plot(T[~full & keep], inv[~full & keep], color=col, ls=(0, (3, 3)), lw=1.2)
    ax.plot(TDOTS, dots[key], 'o', color=col, ms=4.2, mfc='white', mew=1.3, zorder=5)
ax.plot([1.0], [0], 'o', color=style.ACCENT, ms=4.5, zorder=6)
ax.plot([-1.0], [0], 'o', color=style.BROKEN, ms=4.5, zorder=6)
ax.set_xticks([-1, 0, 1, 2, 3])
ax.set_xticklabels([r'$-T_c$', r'$0$', r'$T_c$', r'$2T_c$', r'$3T_c$'])
ax.set_yticks([0, 1, 2, 3, 4])
ax.set_yticklabels([r'$0$', r'$T_c$', r'$2T_c$', r'$3T_c$', r'$4T_c$'])
ax.tick_params(length=2.5, width=0.6, pad=2)
style.label(ax, 3.28, 2.2, r'ferromagnet', color=style.ACCENT, ha='left', fontsize=8.5)
style.label(ax, 3.28, 4.2, r'antiferromagnet', color=style.BROKEN, ha='left', fontsize=8.5)
style.label(ax, 3.28, 3.2, r'paramagnet', color=style.MUTED, ha='left', fontsize=8.5)
print('1/chi of the loop at T =', TDOTS, {k: np.round(v, 4).tolist() for k, v in dots.items()})
style.save(fig, __file__)
