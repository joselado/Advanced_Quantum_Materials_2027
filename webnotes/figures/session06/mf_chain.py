"""Session 6, the half-filled Hubbard chain in mean field, the antiferromagnetic gap and the energy it gains.

Panel (a) is drawn from the downloadable pyqula script webnotes/scripts/session06/g2_chain_meanfield.py, the bands of
the antiferromagnet at U=4t and those of U=0, with the asserts of _g2_chain.check_meanfield. Panel (b) is the numpy
calculation of the first version of this figure, unchanged, since the uniform solution that it compares with is a point
that the lecturer decides (plan of Session 6, "Open for the lecturer", item 1)."""
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
# (b) the energy that the antiferromagnet gains over the uniform solution, per site
ax = axs[1]
Us = np.concatenate([np.linspace(1.2, 3.999, 40), np.linspace(4.0, 12, 60)])
dE = []
for U in Us:
    e, m, D = energy_afm(U)
    uniform = (-4 * t / np.pi + U / 4) if U < 4 * t else 0.0          # paramagnet below 4t, saturated ferromagnet above
    dE.append(uniform - e)
dE = np.array(dE)
lo, hi = Us < 4, Us >= 4
ax.plot(Us[lo], dE[lo], color=style.ACCENT); ax.plot(Us[hi], dE[hi], color=style.ACCENT)
Ut = np.linspace(4, 12, 100)
ax.plot(Ut, 2 * t**2 / Ut, color=style.BROKEN, lw=1.2, ls=(0, (3, 2)))
style.guide(ax, x=4.0, color=style.MUTED, lw=0.8, ls=(0, (3, 2)))
style.arrows(ax, xlabel=r'$U$', ylabel=r'$E_\mathrm{uniform}-E_\mathrm{AFM}$')
style.label(ax, 4.0, -0.04, r'$4t$', fontsize=8.5)
style.label(ax, 9.3, 0.33, r'$2t^2/U$', color=style.BROKEN, fontsize=8.5)
style.label(ax, 6.0, 0.62, '(b) per site', fontsize=8.5)
ax.set_xlim(0, 12); ax.set_ylim(0, 0.72)
style.save(fig, __file__)
