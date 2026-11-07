"""Session 9, Section 9.9, a local magnetic field in a mean-field spinon chain, the induced moment around it.

The spinon Hamiltonian of Section 8.9 for a chain, H = -sum_i chi_i (f^dag_{i,s} f_{i+1,s} + h.c.) with one spinon
per site on average (half filling), plus a field h on site 0 that couples to S^z_0 = (n_up - n_down)/2. The
induced moment is m_n = <S^z_n>. Uniform chi=1 gives the gapless spinon band, and chi alternating 1 and 0.6 gives
the gapped dimerized band of Section 8.9 (gap 0.8). An open chain of 2000 sites with the field in the middle, exact diagonalization of the
single-spinon problem for each spin, h=0.1."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from scipy.linalg import eigh_tridiagonal
import style
style.plt.rcParams.update({'font.size': 11, 'axes.labelsize': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5,
                           'legend.fontsize': 10.5})     # larger than the default, so that the labels read on a phone

N, h = 2000, 0.1
c = N // 2                      # the site of the field, open chain far from both ends


def moment(chi2):
    hop = np.array([1.0 if i % 2 == 0 else chi2 for i in range(N - 1)])
    m = np.zeros(N)
    for sg in (+1, -1):         # spin up feels -h/2, spin down +h/2
        d = np.zeros(N); d[c] = -sg * h / 2
        e, w = eigh_tridiagonal(d, -hop)
        n = (np.abs(w[:, :N // 2]) ** 2).sum(axis=1)        # half filling for each spin
        m += sg * n / 2
    return m


ns = np.arange(0, 41)
res = {}
for chi2 in (1.0, 0.6):
    m = moment(chi2)
    res[chi2] = m[c + ns]
    print('chi2', chi2, 'm_n n=0..6', np.round(m[c:c + 7], 5), 'n*|m_n| at n=5,11,21,31:',
          [round(float(n * abs(m[c + n])), 5) for n in (5, 11, 21, 31)])

fig, axs = style.plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.2 * style.CM),
                              gridspec_kw=dict(wspace=0.3))
ax = axs[0]
nn = np.arange(-12, 13)
ax.axhline(0, color=style.GRID, lw=1.0, zorder=0)
mu = moment(1.0)[c + nn]
md = moment(0.6)[c + nn]
ax.vlines(nn - 0.17, 0, mu, color=style.ACCENT, lw=2.2)
ax.vlines(nn + 0.17, 0, md, color=style.BROKEN, lw=2.2)
style.arrows(ax, xlabel=r'$n$')
ax.set_xlim(-13, 13)
ax.annotate(r'$\langle S^z_n\rangle$', xy=(0, 1.06), xycoords='axes fraction', ha='center', va='bottom')
ax.set_ylim(-0.012, 0.035)
print('m_0 uniform, dimer', mu[12], md[12])
ax.set_xticks([-10, 0, 10]); ax.tick_params(axis='x', length=2.5, pad=2)
style.label(ax, 0, 0.0335, 'field on site 0', fontsize=10.5, color=style.MUTED)

ax = axs[1]
nlog = np.arange(1, 41)
for chi2, col, name in ((1.0, style.ACCENT, 'gapless'), (0.6, style.BROKEN, 'gapped')):
    y = np.abs(res[chi2][1:])
    ok = y > 1e-14
    ax.semilogy(nlog[ok], y[ok], 'o', color=col, ms=2.8)
ax.semilogy(nlog, 0.9 * np.abs(res[1.0][1]) / nlog, color=style.GRID, lw=1.2, zorder=0)
style.arrows(ax, xlabel=r'$n$')
ax.set_xlim(0, 42); ax.set_ylim(1e-11, 0.05)
ax.annotate(r'$|\langle S^z_n\rangle|$', xy=(0, 1.06), xycoords='axes fraction', ha='center', va='bottom')
style.label(ax, 28, 2.5e-3, r'gapless, $1/n$', color=style.ACCENT, fontsize=11.5)
style.label(ax, 32, 1e-6, r'gapped, $e^{-n/\xi}$', color=style.BROKEN, fontsize=11.5)
style.save(fig, __file__)
