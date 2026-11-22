"""Session 9, Section 9.4b, the static Lindhard function (9.4) of the square lattice over the plane of q.

The calculation is the pyqula script webnotes/scripts/session09/g2_lindhard_square.py: eps(k) = -2t(cos kx + cos ky) with
t=1, T=0.1t, a 31x31 k-mesh with the triangle integration of h.get_chi, and the points q = 2 pi (i, j)/20 with
0 <= qy <= qx <= pi, one eighth of the zone. The symmetry of the square gives the rest of the zone, and the map is drawn in
the extended zone with the first zone dashed. Both panels show chi_0(q)/chi_0(0) on one color scale. Left, a low filling
(mu=-3t), where the Fermi surface is close to a circle of radius kF and chi_0(q) is a plateau for |q| < 2kF that falls
outside. Right, half filling (mu=0), where the diamond is nested by Q=(pi,pi) and chi_0 has its maximum there, 2.6 times
chi_0(0). The numbers that the caption and the sheet webnotes/conventions/session09.md state are asserted below."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import style
style.plt.rcParams.update({'font.size': 12, 'axes.labelsize': 12.5, 'xtick.labelsize': 11.5, 'ytick.labelsize': 11.5})

d = style.run_script('session09/g2_lindhard_square.py')
n, qs, mus, chi = d['n'], np.array(d['qs']), list(d['mus']), [np.asarray(c) for c in d['chi']]
assert mus == [-3.0, 0.0] and abs(d['T'] - 0.1) < 1e-12 and n == 20 and d['nk'] == 31   # the parameters of the caption
index = {(int(round(qx * n)), int(round(qy * n))): m for m, (qx, qy) in enumerate(qs)}


def full(values):
    """The values on the n x n points q = 2 pi (i, j)/n of the zone, from the eighth 0 <= qy <= qx <= 1/2."""
    out = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            a, b = min(i, n - i), min(j, n - j)
            out[i, j] = values[index[(max(a, b), min(a, b))]]
    return out


# ---- the numbers of the caption and of the sheet, at half filling
half = chi[1]
c0, cM = half[index[(0, 0)]], half[index[(n // 2, n // 2)]]
ratio = cM / c0
print('half filling: chi0(0) = %.4f, chi0(pi,pi) = %.4f, ratio %.3f' % (c0, cM, ratio))
assert abs(c0 - 0.264) < 2e-3 and abs(cM - 0.677) < 2e-3                  # the sheet, 0.264/t and 0.677/t at T=0.1t
assert abs(ratio - 2.57) < 0.02 and f'{ratio:.1f}' == '2.6'                # the 2.6 of the caption
assert np.argmax(half) == index[(n // 2, n // 2)]                         # the maximum is at Q=(pi,pi)
assert abs(d['ratio'] - ratio) < 1e-12

# ---- low filling: k_F from the area of the Fermi sea, pi kF^2 = (2 pi)^2 n, and the plateau inside |q| = 2 kF
low = chi[0] / chi[0][index[(0, 0)]]
kk = 2 * np.pi * (np.arange(600) + 0.5) / 600 - np.pi
KX, KY = np.meshgrid(kk, kk, indexing='ij')
kF = np.sqrt(4 * np.pi * (-2 * (np.cos(KX) + np.cos(KY)) < -3.0).mean())
print('low filling: kF = %.3f, 2kF = %.3f' % (kF, 2 * kF))
assert abs(kF - 1.03) < 5e-3                                              # the sheet, kF = 1.03
qabs = 2 * np.pi * np.hypot(qs[:, 0], qs[:, 1])
inside, outside = low[qabs < 0.95 * 2 * kF], low[qabs > 1.2 * 2 * kF]
print('low filling: chi0(q)/chi0(0) from %.3f to %.3f inside |q| < 0.95*2kF, at most %.3f outside 1.2*2kF'
      % (inside.min(), inside.max(), outside.max()))
assert inside.min() > 0.99 and inside.max() < 1.08                        # almost flat inside the circle
assert outside.max() < 0.75                                               # and it falls outside it
row = np.array([low[index[(i, 0)]] for i in range(n // 2 + 1)])           # along q_x
qx = 2 * np.pi * np.arange(n // 2 + 1) / n
along = [float(np.interp(f * 2 * kF, qx, row)) for f in (0.5, 0.9, 1.2, 1.5)]
print('low filling, along q_x at 0.5, 0.9, 1.2, 1.5 times 2kF:', np.round(along, 3))
assert np.allclose(along, [1.03, 1.06, 0.68, 0.56], atol=0.04)           # the sheet, on its 200x200 mesh

# ---- the drawing
B = 2 * np.pi * np.eye(2)
cmap = LinearSegmentedColormap.from_list('aqm', ['white', style.LIGHT, style.ACCENT])
VMAX = 2.6
fig, axs = style.plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 7.4 * style.CM),
                              gridspec_kw=dict(wspace=0.42))
for ax, values, title in zip(axs, (low, half / c0), (r'$\mu=-3t$', r'$\mu=0$')):
    im = style.kmap(ax, B, full(values), half=1.2 * np.pi, cmap=cmap, vmin=0, vmax=VMAX, shading='gouraud')
    style.kaxes(ax, fontsize=12.5)
    ax.set_xlabel(r'$q_x$', fontsize=12.5, labelpad=1); ax.set_ylabel(r'$q_y$', fontsize=12.5, labelpad=-2)
    ax.set_xticks([-np.pi, 0, np.pi]); ax.set_yticks([-np.pi, 0, np.pi])
    ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$']); ax.set_yticklabels([r'$-\pi$', '0', r'$\pi$'])
    ax.tick_params(length=2.5, width=0.6)
    ax.set_title(title, fontsize=12.5, pad=6)
th = np.linspace(0, 2 * np.pi, 200)
axs[0].plot(2 * kF * np.cos(th), 2 * kF * np.sin(th), color=style.BROKEN, lw=1.2, ls=(0, (4, 2.5)), zorder=6)
style.label(axs[0], 0, 2 * kF + 0.45, r'$|q|=2k_F$', color=style.BROKEN, fontsize=12, zorder=7)
axs[1].annotate('', xy=(np.pi * 0.97, np.pi * 0.97), xytext=(0, 0), zorder=7,
                arrowprops=dict(arrowstyle='-|>', color=style.BROKEN, lw=1.3, mutation_scale=10, shrinkA=0, shrinkB=0))
style.label(axs[1], 1.05, 1.95, r'$Q$', color=style.BROKEN, fontsize=13, zorder=7)
cb = fig.colorbar(im, ax=list(axs), fraction=0.035, pad=0.03, ticks=[0, 1, 2, 2.6])
cb.ax.set_yticklabels(['0', '1', '2', '2.6'])
cb.ax.tick_params(labelsize=11.5, length=2.5, width=0.6)
cb.outline.set_linewidth(0.6)
cb.set_label(r'$\chi_0(q)/\chi_0(0)$', fontsize=12.5)
style.save(fig, __file__)
