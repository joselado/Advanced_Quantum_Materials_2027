"""Session 10, Section 10.5, the self-consistent loop of (10.8) run on a lattice toy.

An open chain of 60 sites with hopping t=1 and 40 electrons, 20 of each spin. The external potential is a well
v_ext(i) = -2 exp(-((i-29.5)/7)^2). The effective potential keeps only a Hartree term on the lattice,
v_eff(i) = v_ext(i) + U n(i) with U=2 and n(i) the total density, so there is no v_xc. We start from the uniform
density, diagonalize H_KS, fill the lowest orbitals, and mix the new density into the old one with weight 0.3.
Left, the density at a few iterations. Right, the largest change of the density at each iteration, on a log scale.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
style.plt.rcParams.update({'font.size': 11, 'axes.labelsize': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5,
                           'legend.fontsize': 10.5})     # larger than the default, so that the labels read on a phone

N, NE, U, ALPHA = 60, 40, 2.0, 0.3
x = np.arange(N)
vext = -2.0 * np.exp(-((x - 29.5) / 7.0) ** 2)
T = -np.eye(N, k=1) - np.eye(N, k=-1)


def ks_density(n):
    e, w = np.linalg.eigh(T + np.diag(vext + U * n))
    return 2 * (np.abs(w[:, :NE // 2]) ** 2).sum(axis=1)


n = np.full(N, NE / N)
hist, res = [n.copy()], []
for it in range(60):
    nn = ks_density(n)
    res.append(np.abs(nn - n).max())
    n = (1 - ALPHA) * n + ALPHA * nn
    hist.append(n.copy())
    if res[-1] < 1e-10:
        break
res = np.array(res)
print('iterations to 1e-10:', len(res), 'residual at 1, 5, 10, 20:', [float('%.2g' % res[i]) for i in (0, 4, 9, 19)])
n0 = ks_density(np.zeros(N))
print('density at the center: start %.3f, no Hartree %.3f, converged %.3f' % (hist[0][30], n0[30], hist[-1][30]))

fig, axs = style.plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.2 * style.CM),
                              gridspec_kw=dict(wspace=0.3, width_ratios=[1.25, 1]))
ax = axs[0]
show = [(0, style.GRID, 'start'), (1, style.WARM, '1'), (3, style.LIGHT, '3'), (len(hist) - 1, style.ACCENT, 'converged')]
for i, col, lab in show:
    ax.plot(x, hist[i], color=col, lw=1.8 if i else 1.4)
ax.plot(x, 0.32 + 0.1 * vext, color=style.MUTED, lw=1.0, ls=(0, (3, 2)))
style.arrows(ax, xlabel=r'site $i$', ylabel=r'$n(i)$')
ax.set_xlim(0, N - 1); ax.set_ylim(0, 1.25)
ax.set_yticks([0, 0.5, 1]); ax.tick_params(axis='y', length=2.5, pad=2)
style.label(ax, 3, 0.2, r'$v_{\rm ext}(i)$', color=style.MUTED, fontsize=11.5, ha='left')
style.label(ax, 47, 1.12, 'iteration 1', color=style.WARM, fontsize=11)
style.label(ax, 47, 0.96, 'iteration 3', color=style.LIGHT, fontsize=11)
style.label(ax, 12, 1.12, 'converged', color=style.ACCENT, fontsize=11)
print('n at center after iteration 1 and 3:', round(float(hist[1][30]), 3), round(float(hist[3][30]), 3))

ax = axs[1]
it = np.arange(1, len(res) + 1)
ax.semilogy(it, res, 'o-', color=style.ACCENT, ms=2.6, lw=1.0)
style.arrows(ax, xlabel='iteration', ylabel=r'$\max_i|\Delta n(i)|$')
ax.set_xlim(0, len(res) + 2); ax.set_ylim(res.min() / 3, res.max() * 3)
ax.yaxis.set_minor_locator(style.plt.NullLocator())
ax.set_yticks([1e-9, 1e-5, 1e-1]); ax.tick_params(axis='y', length=2.5, pad=2)
ax.set_xticks([0, 10, 20, 30]); ax.tick_params(axis='x', length=2.5, pad=2)
style.save(fig, __file__)
