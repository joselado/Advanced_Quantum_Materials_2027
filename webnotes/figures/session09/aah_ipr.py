"""Session 9, Section 9.10a, the mean IPR (9.12) of the Aubry-Andre chain against the strength V0 of the potential.

H = -t sum (c^dag_n c_{n+1} + h.c.) + V0 sum cos(2 pi q n + phi) n_n with t=1, on rings of N = 55, 233 and 987 sites
(Fibonacci numbers) and q = F_{k-1}/F_k, the rational approximant of the golden ratio that keeps the ring
periodic. phi = 0.3. The IPR is averaged over all eigenstates. The calculation is the pyqula script
webnotes/scripts/session09/g6_aah_ipr.py, which the student downloads, and this file only draws it.

The asserts below back the caption. pyqula gives the numbers of the old numpy figure: the IPR above V0=2t agrees with a
numpy diagonalization to 1e-9, and below it to 2e-3, since the clean ring has degenerate pairs of levels there and the
IPR of such a pair depends on how the solver mixes the two states. N*IPR is 1.5 at V0=0, where the solver returns
standing waves, about 2 at V0=t for the three rings, and it grows to 4.5 to 6 at 1.9t. Above 2t the IPR does not depend
on N. The threads are pinned to one and MKL runs in its reproducible mode (MKL_CBWR), so that the mixing of the
degenerate pairs, and so the SVG, is the same at every run. Without it the mean IPR of the ring of 987 sites at V0=t
changes in the sixth digit from one run to the next, with the alignment of the arrays in memory."""
import os, sys
os.environ['OMP_NUM_THREADS'] = '1'          # one thread and the reproducible mode of MKL, so that the degenerate pairs
os.environ['OPENBLAS_NUM_THREADS'] = '1'     # are mixed in the same way at every run, which the alignment of the arrays
os.environ['MKL_NUM_THREADS'] = '1'          # changes otherwise
os.environ['MKL_CBWR'] = 'COMPATIBLE'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
style.plt.rcParams.update({'font.size': 11, 'axes.labelsize': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5,
                           'legend.fontsize': 10.5})     # larger than the default, so that the labels read on a phone

d = style.run_script('session09/g6_aah_ipr.py')
sizes, qs, V, ipr, phi = d['sizes'], d['qs'], d['V0s'], d['ipr'], d['phi']
assert list(sizes) == [55, 233, 987] and np.allclose(V, np.linspace(0, 4, 41)) and phi == 0.3


def numpy_ipr(N, q, V0):
    """The mean IPR of the same ring from numpy, as the old figure computed it."""
    H = np.diag(V0 * np.cos(2 * np.pi * q * np.arange(N) + phi))
    i = np.arange(N)
    H[i, (i + 1) % N] = H[(i + 1) % N, i] = -1.0
    _, w = np.linalg.eigh(H)
    return (np.abs(w) ** 4).sum(axis=0).mean()


for i, (N, q) in enumerate(zip(sizes, qs)):
    for j in (10, 20, 30):                      # V0 = t, 2t, 3t, the values that the old script printed
        ref = numpy_ipr(N, q, V[j])
        tol = 2e-3 if j < 20 else 1e-9
        assert abs(ipr[i, j] / ref - 1) < tol, (N, V[j], ipr[i, j], ref)
NI = ipr * np.array(sizes)[:, None]
assert np.all(np.abs(NI[:, 0] - 1.5) < 0.01), NI[:, 0]                       # standing waves at V0 = 0
assert np.all((NI[:, 10] > 1.99) & (NI[:, 10] < 2.11)), NI[:, 10]            # about 2 at V0 = t
assert np.all((NI[:, 19] > 4.4) & (NI[:, 19] < 6.0)), NI[:, 19]              # 4.5 to 6 at V0 = 1.9t
assert np.all(np.diff(ipr[:, 10]) < 0) and np.all(np.diff(ipr[:, 19]) < 0)   # the curves are apart below 2t
for j in range(22, 41):                                                      # on top of each other from 2.2t on
    assert np.ptp(ipr[:, j]) / ipr[2, j] < (0.06 if j < 25 else 0.03), (V[j], ipr[:, j])
assert np.allclose(ipr[:, 30], [0.549, 0.543, 0.542], atol=6e-4), ipr[:, 30]
assert np.allclose(ipr[:, 25], [0.418, 0.411, 0.409], atol=6e-4), ipr[:, 25]
for i in range(3):
    print(sizes[i], 'N*IPR at V0=0, t, 1.9t:', np.round(NI[i, [0, 10, 19]], 3), ' IPR at 2t, 2.5t, 3t:', np.round(ipr[i, [20, 25, 30]], 4))

fig, ax = style.figure(height_cm=5.8, width_cm=10.5)
cols = {55: style.LIGHT, 233: style.ACCENT, 987: style.INK}
for i, N in enumerate(sizes):
    ax.semilogy(V, ipr[i], 'o-', color=cols[N], ms=2.6, lw=1.0)
    style.label(ax, 0.15, ipr[i, 0] * 1.9, r'$N=%d$' % N, color=cols[N], fontsize=11, ha='left')
style.guide(ax, x=2.0, color=style.BROKEN, lw=1.0, ls=(0, (4, 2.5)))
style.arrows(ax, xlabel=r'$V_0/t$', ylabel=r'mean $\mathrm{IPR}$', ticks=True)
ax.set_xlim(0, 4.15)
ax.set_ylim(5e-4, 1.5)
ax.set_xticks([0, 1, 2, 3, 4]); ax.set_xticklabels(['0', '1', '2', '3', '4'])
ax.set_yticks([1e-3, 1e-2, 1e-1, 1]); ax.set_yticklabels([r'$10^{-3}$', r'$10^{-2}$', r'$10^{-1}$', r'$1$'])
ax.yaxis.set_minor_locator(style.plt.NullLocator())
ax.tick_params(length=2.5, pad=2)
style.label(ax, 2.08, 0.9, r'$V_0=2t$', color=style.BROKEN, fontsize=11.5, ha='left')
style.label(ax, 0.95, 0.12, 'extended', color=style.MUTED, fontsize=11.5)
style.label(ax, 3.2, 0.12, 'localized', color=style.MUTED, fontsize=11.5)
style.save(fig, __file__)
