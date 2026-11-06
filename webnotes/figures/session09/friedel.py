"""Session 9, Eq. (9.9) in a chain, the density induced by one impurity, from exact diagonalization."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal
import style

N, v0 = 4001, 1.0
c = N // 2


def density(mu, v):
    d = np.zeros(N); d[c] = v
    e, w = eigh_tridiagonal(d, -np.ones(N - 1))
    return (np.abs(w[:, e < mu]) ** 2).sum(axis=1)


fig, axs = plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.0 * style.CM), sharey=True, gridspec_kw=dict(wspace=0.12))
xs = np.arange(1, 61)
res = []
for a, mu, col in zip(axs, (-1.6, -1.0), (style.ACCENT, style.BROKEN)):
    dn = density(mu, v0) - density(mu, 0.0)
    y = dn[c + xs]
    kF = np.arccos(-mu / 2)
    a.plot(xs, y, 'o-', color=col, ms=2.8, lw=0.6)
    C = (np.abs(y[3:]) * xs[3:]).max()
    env = C / xs      # guide, 1/x
    style.arrows(a, xlabel=r'$x$')
    style.guide(a, y=0, color=style.MUTED, lw=0.8)
    a.set_xlim(0, 62)
    a.plot(xs, env, color=style.GRID, lw=1.2, zorder=0); a.plot(xs, -env, color=style.GRID, lw=1.2, zorder=0)
    a.set_title(r'$k_F=%.2f$, period $\pi/k_F=%.1f$' % (kF, np.pi / kF), color=col, fontsize=8.5, pad=14)
    a.set_ylim(-0.012, 0.012) if False else None
    res.append((mu, kF, y))
Cm = max((np.abs(r[2][3:]) * xs[3:]).max() for r in res)
axs[0].set_ylim(-Cm / 2.5, Cm / 2.5)
axs[0].annotate(r'$\delta n(x)$', xy=(0, 1.0), xycoords='axes fraction', ha='center', va='bottom')
style.save(fig, __file__)
for mu, kF, y in res:
    # period from the positions of the zero crossings
    s = np.sign(y); z = np.where(s[1:] != s[:-1])[0]
    print(mu, kF, np.pi / kF, 'mean spacing of zero crossings x2 =', 2 * np.diff(z[:20]).mean(), 'amp x=10,20,40:', y[9], y[19], y[39])
