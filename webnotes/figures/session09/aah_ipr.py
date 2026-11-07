"""Session 9, Section 9.10a, the mean IPR (9.12) of the Aubry-Andre chain against the strength V0 of the potential.

H = -t sum (c^dag_n c_{n+1} + h.c.) + V0 sum cos(2 pi q n + phi) n_n with t=1, on rings of N = 55, 233 and 987 sites
(Fibonacci numbers) and q = F_{k-1}/F_k, the rational approximant of the golden ratio that keeps the ring
periodic. phi = 0.3. The IPR is averaged over all eigenstates. Below V0=2t it falls as 1/N, above it does not
depend on N, and the curves separate at the self-dual point V0=2t."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
style.plt.rcParams.update({'font.size': 11, 'axes.labelsize': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5,
                           'legend.fontsize': 10.5})     # larger than the default, so that the labels read on a phone

FIB = {55: 34, 233: 144, 987: 610}
V = np.linspace(0.0, 4.0, 41)


def mean_ipr(N, V0, phi=0.3):
    q = FIB[N] / N
    H = np.diag(V0 * np.cos(2 * np.pi * q * np.arange(N) + phi))
    i = np.arange(N)
    H[i, (i + 1) % N] = H[(i + 1) % N, i] = -1.0
    _, w = np.linalg.eigh(H)
    return (np.abs(w) ** 4).sum(axis=0).mean()


fig, ax = style.figure(height_cm=5.4, width_cm=10.5)
cols = {55: style.LIGHT, 233: style.ACCENT, 987: style.INK}
for N in (55, 233, 987):
    y = np.array([mean_ipr(N, v) for v in V])
    ax.semilogy(V, y, 'o-', color=cols[N], ms=2.6, lw=1.0)
    print(N, 'IPR at V0=1:', round(float(y[10]), 5), 'N*IPR:', round(float(N * y[10]), 2), ' at V0=2:', round(float(y[20]), 4),
          ' at V0=3:', round(float(y[30]), 4))
    style.label(ax, 0.15, y[0] * 1.9, r'$N=%d$' % N, color=cols[N], fontsize=11, ha='left')
style.guide(ax, x=2.0, color=style.BROKEN, lw=1.0, ls=(0, (4, 2.5)))
style.arrows(ax, xlabel=r'$V_0/t$', ylabel=r'$\overline{\mathrm{IPR}}$')
ax.set_xlim(0, 4.15)
ax.set_xticks([0, 1, 2, 3, 4]); ax.tick_params(axis='x', length=2.5, pad=2)
ax.set_ylim(5e-4, 1.5)
ax.yaxis.set_minor_locator(style.plt.NullLocator())
style.label(ax, 2.08, 0.9, r'$V_0=2t$', color=style.BROKEN, fontsize=11.5, ha='left')
style.label(ax, 0.95, 0.12, 'extended', color=style.MUTED, fontsize=11.5)
style.label(ax, 3.2, 0.12, 'localized', color=style.MUTED, fontsize=11.5)
style.save(fig, __file__)
