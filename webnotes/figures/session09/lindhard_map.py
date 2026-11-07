"""Session 9, Section 9.4b, the static Lindhard function (9.4) of the square lattice over the whole (qx, qy) zone.

eps(k) = -2t(cos kx + cos ky) with t=1, on a 200x200 k-mesh with T=0.1t. The q-points are points of the same
mesh, so that k+q is a shift of the arrays. Left, a low filling (mu=-3t), where the Fermi surface is close to a
circle of radius kF and chi0(q) is a plateau for |q| < 2kF that falls outside. Right, half filling (mu=0), where
the diamond is nested by Q=(pi,pi) and chi0 has its maximum there. The map is drawn with imshow, as one
embedded image, so that the SVG stays small."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import style
style.plt.rcParams.update({'font.size': 11, 'axes.labelsize': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5,
                           'legend.fontsize': 10.5})     # larger than the default, so that the labels read on a phone

NK, T = 200, 0.1
k = 2 * np.pi * np.arange(NK) / NK - np.pi
KX, KY = np.meshgrid(k, k, indexing='ij')
E = -2 * (np.cos(KX) + np.cos(KY))


def fermi(e, mu):
    return 0.5 * (1 - np.tanh((e - mu) / (2 * T)))


def chi0(mu, step=4):
    f = fermi(E, mu)
    dfde = -f * (1 - f) / T                        # n_F' for the terms with equal energies
    idx = np.arange(0, NK, step)
    out = np.zeros((len(idx), len(idx)))
    for a, i in enumerate(idx):
        Ei = np.roll(E, -i, axis=0); fi = np.roll(f, -i, axis=0)
        for b, j in enumerate(idx):
            Eq = np.roll(Ei, -j, axis=1); fq = np.roll(fi, -j, axis=1)
            de = Eq - E
            small = np.abs(de) < 1e-9
            term = np.where(small, -dfde, (f - fq) / np.where(small, 1.0, de))
            out[a, b] = term.mean()
    q = k[idx] + np.pi                             # the shift i corresponds to q = 2 pi i / NK
    q = np.where(q > np.pi + 1e-12, q - 2 * np.pi, q)
    order = np.argsort(q)
    return q[order], out[np.ix_(order, order)]


cmap = LinearSegmentedColormap.from_list('aqm', ['white', style.LIGHT, style.ACCENT])
fig, axs = style.plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 6.6 * style.CM),
                              gridspec_kw=dict(wspace=0.32))
res = {}
for ax, mu, title in zip(axs, (-3.0, 0.0), (r'low filling, $\mu=-3t$', r'half filling, $\mu=0$')):
    q, c = chi0(mu)
    res[mu] = (q, c)
    ax.imshow(c.T, origin='lower', extent=(q[0], q[-1], q[0], q[-1]), cmap=cmap, interpolation='bilinear',
              vmin=0, vmax=c.max())
    style.arrows(ax, xlabel=r'$q_x$', ylabel=r'$q_y$')
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-np.pi, np.pi); ax.set_aspect('equal')
    ax.set_title(title, fontsize=11.5, pad=16)
    for s in (-np.pi, np.pi):
        style.label(ax, s, -np.pi - 0.45, r'$-\pi$' if s < 0 else r'$\pi$', fontsize=10.5)
        style.label(ax, -np.pi - 0.45, s, r'$-\pi$' if s < 0 else r'$\pi$', fontsize=10.5)
    i0 = np.argmin(np.abs(q))
    print(mu, 'chi0(0)=%.3f max=%.3f at q=(%.2f,%.2f)' % (c[i0, i0], c.max(), *q[list(np.unravel_index(c.argmax(), c.shape))]))

# low filling: the circle |q| = 2 kF, with kF from the area of the Fermi sea
mu = -3.0
nocc = (E < mu).mean()                             # filling per spin, area pi kF^2 / (2 pi)^2
kF = np.sqrt(4 * np.pi * nocc)
th = np.linspace(0, 2 * np.pi, 200)
axs[0].plot(2 * kF * np.cos(th), 2 * kF * np.sin(th), color=style.BROKEN, lw=1.1, ls=(0, (4, 2.5)))
style.label(axs[0], 2.0, 2.95, r'$|q|=2k_F$', color=style.BROKEN, fontsize=11)
q, c = res[mu]
i0 = np.argmin(np.abs(q))
row = c[:, i0]
print('kF=%.3f 2kF=%.3f; chi0 along qx at 0, kF, 1.8kF, 2.4kF:' % (kF, 2 * kF),
      [round(float(np.interp(x, q, row)), 3) for x in (0, kF, 1.8 * kF, 2.4 * kF)])
# half filling: the vector Q to the corner
axs[1].annotate('', xy=(np.pi * 0.97, np.pi * 0.97), xytext=(0, 0),
                arrowprops=dict(arrowstyle='-|>', color=style.BROKEN, lw=1.3, mutation_scale=9, shrinkA=0, shrinkB=0))
style.label(axs[1], 0.95, 1.75, r'$Q$', color=style.BROKEN, fontsize=12)
style.save(fig, __file__)
