"""Session 9, Eq. (9.9) in a chain, the density induced by one impurity, from exact diagonalization.

The chain has the hopping -t, the band -2t cos k, 4001 sites and one impurity v0 = t on the middle site, and the
states below the chemical potential mu are filled, mu = -1.6t on the left and -t on the right. The density stays
numpy and not pyqula, since the embedding of pyqula gives the LDOS at one energy, which in a chain does not fall as
1/x (webnotes/conventions/session09.md). Redrawn on 2026-11-22 with numbers on the axes, by the rules of 2026-11-21.
The asserts are the numbers of the caption and of the titles: k_F = 0.64 and 1.05, the periods pi/k_F = 4.9 and 3.0
sites, also from the zero crossings of the points, the power 1.00 of the envelope from a fit beyond 10 sites, the
parameters of the caption, the drawn sites x = 1 to 60, and dn(0) = -0.15 and -0.19 on the impurity site, which is not
drawn."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal
import style

N, v0, HOP, MUS = 4001, 1.0, -1.0, (-1.6, -1.0)
c = N // 2
# the caption: a chain of 4001 sites, the impurity v0 = t, the hopping -t, and mu = -1.6t and -t. On an open chain the
# density is the same for either sign of the hopping, so these are asserts of the parameters only
assert N == 4001 and v0 == 1.0 and HOP == -1.0 and MUS == (-1.6, -1.0)


def density(mu, v):
    d = np.zeros(N); d[c] = v
    e, w = eigh_tridiagonal(d, HOP * np.ones(N - 1))
    return (np.abs(w[:, e < mu]) ** 2).sum(axis=1)


def power(xs, y, q):
    """The power p of a fit of y by x^-p (A cos qx + B sin qx), with A and B linear, scanned over p."""
    ps = np.linspace(0.5, 1.5, 1001)
    res = []
    for p in ps:
        M = (xs ** -p)[:, None] * np.array([np.cos(q * xs), np.sin(q * xs)]).T
        cc = np.linalg.lstsq(M, y, rcond=None)[0]
        res.append(np.sum((M @ cc - y) ** 2) / np.sum(y ** 2))
    return ps[int(np.argmin(res))]


fig, axs = plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.2 * style.CM), sharey=True,
                        gridspec_kw=dict(wspace=0.15))
xs = np.arange(1, 61)
assert xs[0] == 1 and xs[-1] == 60                                     # the alt text: the sites x from 1 to 60
res = []
for a, mu, col in zip(axs, MUS, (style.ACCENT, style.BROKEN)):
    dn = density(mu, v0) - density(mu, 0.0)
    y = dn[c + xs]
    assert np.allclose(dn[c + xs], dn[c - xs], atol=1e-12)          # the same on the two sides of the impurity
    kF = np.arccos(-mu / 2)
    far = np.arange(10, 201)
    p = power(far, dn[c + far], 2 * kF)
    s = np.sign(y); z = np.where(s[1:] != s[:-1])[0]
    crossing = 2 * np.diff(z[:20]).mean()
    print(f'mu = {mu}: k_F = {kF:.3f}, pi/k_F = {np.pi / kF:.3f}, from the zero crossings {crossing:.2f}, '
          f'power of the envelope {p:.3f}, dn(0) = {dn[c]:.3f}')
    assert abs(p - 1) < 0.02 and abs(crossing / (np.pi / kF) - 1) < 0.05
    res.append((mu, kF, y, dn[c]))
    C = (np.abs(y[3:]) * xs[3:]).max()
    env = C / xs                                                      # guide, 1/x
    style.guide(a, y=0, color=style.MUTED, lw=0.8)
    a.plot(xs, env, color=style.GRID, lw=1.2, zorder=0); a.plot(xs, -env, color=style.GRID, lw=1.2, zorder=0)
    a.plot(xs, y, 'o-', color=col, ms=2.8, lw=0.6)
    a.set_xlim(0, 63)
    a.set_title(r'$k_F=%.2f$, period $\pi/k_F=%.1f$' % (kF, np.pi / kF), color=col, fontsize=8.5, pad=14)
assert [round(r[1], 2) for r in res] == [0.64, 1.05] and [round(np.pi / r[1], 1) for r in res] == [4.9, 3.0]
Cm = max((np.abs(r[2][3:]) * xs[3:]).max() for r in res)
lim = Cm / 2.5
axs[0].set_ylim(-lim, lim)
assert 0.035 < lim < 0.045, lim
# the caption: only the first site of the left plot, dn = -0.07, lies outside the plotted range
print("first site of the left plot", res[0][2][0]); assert round(res[0][2][0], 2) == -0.07 and res[0][2][0] < -lim
assert np.abs(res[0][2][1:]).max() < lim and np.abs(res[1][2]).max() < lim
# the caption: the impurity site x = 0 is not drawn, and it has dn = -0.15 on the left and -0.19 on the right
assert [round(r[3], 2) for r in res] == [-0.15, -0.19], [r[3] for r in res]
style.arrows(axs[0], xlabel=r'$x$', ylabel=r'$\delta n(x)$', ticks=True)
style.arrows(axs[1], xlabel=r'$x$', ticks=True)
for a in axs:
    a.set_xticks([0, 20, 40, 60])
    a.tick_params(length=2.5, width=0.6, labelsize=8)
    assert a.get_xlim() == (0, 63) and list(a.get_xticks()) == [0, 20, 40, 60]   # the x axis from 0, ticks to 60
axs[0].set_yticks([-0.04, -0.02, 0, 0.02, 0.04])
axs[0].set_yticklabels([r'$-0.04$', r'$-0.02$', r'$0$', r'$0.02$', r'$0.04$'])
axs[1].tick_params(labelleft=False)
style.save(fig, __file__)
