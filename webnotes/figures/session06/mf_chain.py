"""Session 6, the half-filled Hubbard chain in mean field, the antiferromagnetic gap and the energy it gains.

Panel (a) is drawn from the downloadable pyqula script webnotes/scripts/session06/g2_chain_meanfield.py, the bands of
the antiferromagnet at U=4t and those of U=0, with the asserts of _g2_chain.check_meanfield. Panel (b) is the numpy
calculation of the gap equation, against the lowest uniform solution, as decided on 2026-11-22 (plan of Session 6, "Open
for the lecturer"). The uniform solutions are the paramagnet, -4t/pi + U/4 per site, and the saturated ferromagnet, 0,
which is a solution from 4t on. The lower of the two changes at 16t/pi = 5.09t, so the curve has a kink there and no
jump. The first version switched at 4t and drew a jump of 0.27t."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
import style, _g2_chain

t = 1.0

def avg(f, D):
    """Average over the reduced zone k in (-pi/2, pi/2) of f(eps_k, D), with eps_k = -2t cos k."""
    return quad(lambda k: f(-2 * t * np.cos(k), D), -np.pi / 2, np.pi / 2, points=[0], limit=200, epsabs=1e-13, epsrel=1e-12)[0] / np.pi

def gap_parameter(U):
    """Delta = U m / 2 from the self-consistency m = <Delta/E>, that is 1 = (U/2) <1/E>."""
    return brentq(lambda D: (U / 2) * avg(lambda e, D: 1 / np.sqrt(e * e + D * D), D) - 1, 1e-9, 5 * U, xtol=1e-14)

def energy_afm(U):
    D = gap_parameter(U)
    m = 2 * D / U
    kin = -avg(lambda e, D: e * e / np.sqrt(e * e + D * D), D)       # kinetic energy per site, both spins
    return kin + U * (1 - m * m) / 4, m, D                           # interaction energy per site, U <n_up><n_down>

# the checks of the numbers of the text
assert abs(-avg(lambda e, D: abs(e), 0.0) + 4 / np.pi / t) < 1e-9    # U=0, -4t/pi per site
for U in (20.0, 40.0):
    e, m, D = energy_afm(U)
    assert abs(-e * U / t**2 - 2) < 0.1 and abs(m - 1) < 0.02        # E_FM - E_AFM -> 2t^2/U = J/2, with m -> 1

d = style.run_script('session06/g2_chain_meanfield.py')
_g2_chain.check_meanfield(d)

fig, axs = style.figure(height_cm=5.8, ncols=2)
# (a) the bands of the antiferromagnet at U=4t from pyqula, over the zone of the chain, and the crossing bands of U=0
ax = axs[0]
ks, baf, bpm = d['ks'], d['bands_afm'], d['bands_pm']
Delta = d['U'] * abs(float(np.real(d['m_afm'][0]))) / 2             # Um/2 = 1.54
for x in (-np.pi / 2, np.pi / 2):
    style.guide(ax, x=x, color=style.GRID, lw=0.8)
style.guide(ax, y=0)
ax.plot(ks, bpm[:, 0], color=style.MUTED, lw=1.0, ls=(0, (3, 2)))
ax.plot(ks, bpm[:, 3], color=style.MUTED, lw=1.0, ls=(0, (3, 2)))
ax.plot(ks, baf[:, 0], color=style.ACCENT)
ax.plot(ks, baf[:, 3], color=style.ACCENT)
ax.annotate('', xy=(np.pi / 2, Delta), xytext=(np.pi / 2, -Delta), arrowprops=dict(arrowstyle='<->', color=style.BROKEN, lw=0.9, shrinkA=0, shrinkB=0))
style.label(ax, np.pi / 2 + 0.42, 0.3, r'$Um$', color=style.BROKEN, ha='left', fontsize=8.5)   # right of the U=0 crossing
style.arrows(ax, xlabel=r'$k$', ylabel=r'$E/t$', ticks=True)
ax.set_xticks([-np.pi / 2, 0, np.pi / 2]); ax.set_xticklabels([r'$-\pi/2$', '0', r'$\pi/2$'])
ax.set_yticks([-Delta, Delta]); ax.set_yticklabels([r'$%.2f$' % -Delta, r'$%.2f$' % Delta])
ax.tick_params(length=2.5, width=0.6)
style.label(ax, 0.0, 3.6, r'(a) $U=4t$, grey $U=0$', fontsize=8.5)
ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-3.9, 4.1)
# (b) the energy that the antiferromagnet gains over the lowest uniform solution, per site
ax = axs[1]
Uk = 16 * t / np.pi                                                   # the paramagnet and the saturated ferromagnet cross
uniform = lambda U: min(-4 * t / np.pi + U / 4, 0.0)                 # the lower of the two uniform solutions
Us = np.concatenate([np.linspace(1.2, Uk, 50), np.linspace(Uk, 12, 60)[1:]])
dE = np.array([uniform(U) - energy_afm(U)[0] for U in Us])
# the checks of the caption: the lower uniform state is the paramagnet below 16t/pi and the saturated ferromagnet above,
# the curve has no jump at 16t/pi and is largest there, 0.378, and above it it approaches 2t^2/U, within 4 percent just
# above the kink and within 1 percent from 10t on
eps = 1e-6
assert abs(-4 * t / np.pi + Uk / 4) < 1e-12 and round(Uk, 2) == 5.09 and round(Uk, 1) == 5.1
assert all((-4 / np.pi + U / 4 < 0) == (U < Uk) for U in (4.0, 4.5, 5.0, 5.2, 6.0))
jump = abs((uniform(Uk - eps) - energy_afm(Uk - eps)[0]) - (uniform(Uk + eps) - energy_afm(Uk + eps)[0]))
assert jump < 1e-5 and int(np.argmax(dE)) == 49 and abs(dE[49] - 0.378) < 5e-4
ratio = dE / (2 * t**2 / Us)
assert np.all(ratio[Us > Uk] > 0.96) and np.all(ratio[Us >= 10] > 0.99) and np.all(ratio[Us > Uk] < 1)
ax.plot(Us, dE, color=style.ACCENT)
Ut = np.linspace(4, 12, 100)
ax.plot(Ut, 2 * t**2 / Ut, color=style.BROKEN, lw=1.2, ls=(0, (3, 2)))
style.guide(ax, x=Uk, color=style.MUTED, lw=0.8, ls=(0, (3, 2)))
style.arrows(ax, xlabel=r'$U/t$', ylabel=r'$(E_\mathrm{uniform}-E_\mathrm{AFM})/t$', ticks=True)
ax.set_xticks([0, 4, 8, 12]); ax.set_yticks([0, 0.2, 0.4])
ax.tick_params(length=2.5, width=0.6)
style.label(ax, Uk + 0.15, 0.445, r'$16t/\pi$', fontsize=8.5, ha='left')
style.label(ax, 9.6, 0.27, r'$2t^2/U$', color=style.BROKEN, fontsize=8.5)
style.label(ax, 2.6, 0.445, '(b) per site', fontsize=8.5)
ax.set_xlim(0, 12); ax.set_ylim(0, 0.5)
style.save(fig, __file__)
