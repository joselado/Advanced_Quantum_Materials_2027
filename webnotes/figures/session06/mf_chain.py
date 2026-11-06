"""Session 6, the half-filled Hubbard chain in mean field, the antiferromagnetic gap and the energy it gains."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
import style

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

fig, axs = style.figure(height_cm=5.8, ncols=2)
# (a) bands, the folded zone of the two-site cell
ax = axs[0]
k = np.linspace(0, np.pi, 500)
eps = -2 * t * np.cos(k)
U0 = 4.0
D0 = gap_parameter(U0)
ax.plot(k, eps, color=style.MUTED, lw=1.0, ls=(0, (3, 2)))
ax.plot(k, -eps, color=style.MUTED, lw=1.0, ls=(0, (3, 2)))
ax.plot(k, np.sqrt(eps**2 + D0**2), color=style.ACCENT)
ax.plot(k, -np.sqrt(eps**2 + D0**2), color=style.ACCENT)
style.guide(ax, y=0)
ax.annotate('', xy=(np.pi / 2, D0), xytext=(np.pi / 2, -D0), arrowprops=dict(arrowstyle='<->', color=style.BROKEN, lw=0.9, shrinkA=0, shrinkB=0))
style.label(ax, np.pi / 2 + 0.12, 0.0, r'$Um$', color=style.BROKEN, ha='left', fontsize=8.5)
style.arrows(ax, xlabel=r'$k$', ylabel=r'$E$')
style.label(ax, 1.55, 3.5, r'(a) $U=4t$, grey $U=0$', fontsize=8.5)
ax.set_xlim(0, np.pi); ax.set_ylim(-3.9, 4.1)
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
