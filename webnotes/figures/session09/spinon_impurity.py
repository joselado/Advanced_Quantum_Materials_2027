"""Session 9, Section 9.9, a local magnetic field in a mean-field spinon chain, the induced moment around it.

The data come from the downloadable script webnotes/scripts/session09/g5_spinon_chain_field.py. It is the spinon
Hamiltonian (8.15) of Section 8.9 for a chain, with the same chi for the two spin species, half filling (one spinon per
site), and a field h on site 0 that couples to S^z_0 = (n_up - n_down)/2, so that the up spinons get -h/2 and the down ones
+h/2 on that site. The induced moment is m_n = <S^z_n>. Uniform chi=1 gives the gapless spinon band, and chi alternating
1 and 0.6 gives the gapped dimerized band of Section 8.9 (gap 2(1-0.6) = 0.8). An open chain of 2000 sites with the field
in the middle, whose bond to the right is the strong one, h=0.1, each species diagonalized as a pyqula chain with the
hopping +1, which on the bipartite chain gives the same densities as the -1 of the numpy script of before, to 1e-15.

The values near the floor of the logarithmic panel change by about 1e-3 of themselves with the number of threads of the
diagonalization, so the logarithmic panel draws only the points above 1e-8, and the drawn values are rounded, to 0.01 of
a decade on the logarithmic panel and to 1e-7 on the left one, which gives the same SVG at every run. The numbers that the
caption quotes are asserted below. The quiz pictures g5_quiz_spinon_*.py draw the three dimerized chains of the script."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
style.plt.rcParams.update({'font.size': 11, 'axes.labelsize': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5,
                           'legend.fontsize': 10.5})     # larger than the default, so that the labels read on a phone

d = style.run_script('session09/g5_spinon_chain_field.py')
c, mom = d['c'], d['moments']
assert d['N'] == 2000 and abs(d['field'] - 0.1) < 1e-12 and c == 1000
mu, md = mom[1.0], mom[0.6]
# the uniform chain: the moment changes sign on every site, and n |m_n| is between 0.0038 and 0.0045 for n = 2 to 31
assert all(mu[c + n] * mu[c + n + 1] < 0 for n in range(0, 40)) and all(md[c + n] * md[c + n + 1] < 0 for n in range(0, 40))
ns = np.arange(2, 32)
nm = ns * np.abs(mu[c + ns])
assert 0.0037 < nm.min() < 0.0038 and 0.0044 < nm.max() < 0.0045
# the dimerized chain: the gap 0.8, the partner of site 0 has -0.81 of its moment, 0.66 of all the moment off site 0
k = np.linspace(-np.pi, np.pi, 2001)
assert abs(2 * np.min(np.abs(1 + 0.6 * np.exp(1j * k))) - 0.8) < 1e-9
win = md[c - 40:c + 41]
assert abs(md[c + 1] / md[c] + 0.81) < 0.005 and abs(md[c - 1] / md[c] + 0.05) < 0.005
assert abs(abs(md[c + 1]) / (np.abs(win).sum() - abs(md[c])) - 0.66) < 0.005
# on the logarithmic panel the points of each sublattice of the dimerized chain lie close to a straight line: from n=4 to
# the floor 1e-8 they span four and five decades, and they leave the line of their fit by less than 0.1 of a decade
for p in (0, 1):
    n = np.arange(4 + p, 41, 2)
    n = n[np.abs(md[c + n]) >= 1e-8]
    y = np.log10(np.abs(md[c + n]))
    fit = np.polyfit(n, y, 1)
    assert y.max() - y.min() > 3.9 and np.abs(np.polyval(fit, n) - y).max() < 0.1
print('n|m_n| of the uniform chain', round(nm.min(), 5), round(nm.max(), 5), 'partner', round(md[c + 1] / md[c], 3))

fig, axs = style.plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.6 * style.CM), gridspec_kw=dict(wspace=0.42))
ax = axs[0]
nn = np.arange(-12, 13)
ax.axhline(0, color=style.GRID, lw=1.0, zorder=0)
ax.vlines(nn - 0.17, 0, np.round(mu[c + nn], 7), color=style.ACCENT, lw=2.2)
ax.vlines(nn + 0.17, 0, np.round(md[c + nn], 7), color=style.BROKEN, lw=2.2)
ax.set_xlim(-13, 13); ax.set_ylim(-0.012, 0.0165)
ax.set_xticks([-10, 0, 10]); ax.set_yticks([-0.01, 0, 0.01]); ax.set_yticklabels(['$-0.01$', '$0$', '$0.01$'])
ax.set_xlabel(r'$n$', labelpad=1)
ax.set_ylabel(r'$\langle S^z_n\rangle$', labelpad=1)
style.label(ax, 0, 0.0155, 'field on site 0', fontsize=10.5, color=style.MUTED)
assert max(abs(mu[c]), abs(md[c])) < 0.0145 and min(md[c + nn].min(), mu[c + nn].min()) > -0.012

ax = axs[1]
nlog = np.arange(1, 41)
floor = 1e-8
for m, col in ((mu, style.ACCENT), (md, style.BROKEN)):
    y = np.abs(m[c + nlog])
    keep = y >= floor
    ax.semilogy(nlog[keep], 10 ** np.round(np.log10(y[keep]), 2), 'o', color=col, ms=2.8)
ax.semilogy(nlog, 0.9 * np.abs(mu[c + 1]) / nlog, color=style.GRID, lw=1.2, zorder=0)
ax.set_xlim(0, 42); ax.set_ylim(floor, 0.05)
ax.set_xticks([0, 10, 20, 30, 40]); ax.set_yticks([1e-8, 1e-6, 1e-4, 1e-2])
ax.minorticks_off()
ax.set_xlabel(r'$n$', labelpad=1)
ax.set_ylabel(r'$|\langle S^z_n\rangle|$', labelpad=1)
style.label(ax, 27, 1.2e-3, r'gapless, $1/n$', color=style.ACCENT, fontsize=11)
style.label(ax, 30, 1e-6, r'gapped, $e^{-n/\xi}$', color=style.BROKEN, fontsize=11)
for a in axs:
    for s in ('top', 'right'):
        a.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        a.spines[s].set_linewidth(0.6)
    a.tick_params(length=2.5, width=0.6, pad=2)
style.save(fig, __file__)
