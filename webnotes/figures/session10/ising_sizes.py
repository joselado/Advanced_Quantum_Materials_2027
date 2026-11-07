"""Session 10, Section 10.6a, the order parameter of (10.9) on finite lattices, from Monte Carlo.

Metropolis updates on the two checkerboard sublattices of an L x L square lattice with periodic boundaries,
J=1, for L = 8, 16 and 32. At each temperature 1500 sweeps are thrown away and <|m|> is the mean over 3000
sweeps. The grey line is the exact result of Onsager for the infinite lattice. The seed is fixed, so that the
SVG is the same at every run."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
style.plt.rcParams.update({'font.size': 11, 'axes.labelsize': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5,
                           'legend.fontsize': 10.5})     # larger than the default, so that the labels read on a phone

rng = np.random.default_rng(7)
Ts = np.linspace(1.5, 3.5, 21)
TC = 2 / np.log(1 + np.sqrt(2))


def mean_absm(L, T, s, nth=1500, nme=3000):
    mask = (np.add.outer(np.arange(L), np.arange(L)) % 2).astype(bool)
    acc = 0.0
    for sweep in range(nth + nme):
        for sub in (mask, ~mask):
            nb = np.roll(s, 1, 0) + np.roll(s, -1, 0) + np.roll(s, 1, 1) + np.roll(s, -1, 1)
            dE = 2 * s * nb
            flip = sub & (rng.random((L, L)) < np.exp(-dE / T))
            s[flip] *= -1
        if sweep >= nth:
            acc += abs(s.mean())
    return acc / nme, s


fig, ax = style.figure(height_cm=5.2, width_cm=10.5)
Tf = np.linspace(1.5, 3.5, 400)
mex = np.where(Tf < TC, np.abs(1 - np.sinh(2 / np.minimum(Tf, TC - 1e-9)) ** -4) ** 0.125, 0.0)
ax.plot(Tf, mex, color=style.GRID, lw=2.4, zorder=0, label='exact')
cols = {8: style.LIGHT, 16: style.ACCENT, 32: style.INK}
for L in (8, 16, 32):
    s = np.ones((L, L), dtype=int)
    m = []
    for T in Ts:
        v, s = mean_absm(L, T, s)
        m.append(v)
    m = np.array(m)
    ax.plot(Ts, m, 'o-', color=cols[L], ms=2.6, lw=1.0, label=r'$L=%d$' % L)
    print(L, 'm at T=2.0, 2.3, 2.6, 3.0:', [round(float(np.interp(t, Ts, m)), 3) for t in (2.0, 2.3, 2.6, 3.0)])
style.guide(ax, x=TC, color=style.BROKEN, lw=1.0, ls=(0, (4, 2.5)))
style.arrows(ax, xlabel=r'$k_BT/J$', ylabel=r'$\langle|m|\rangle$')
ax.set_xlim(1.5, 3.55); ax.set_ylim(0, 1.08)
ax.set_xticks([1.5, 2.0, 2.5, 3.0, 3.5]); ax.set_yticks([0, 0.5, 1])
ax.tick_params(length=2.5, pad=2)
style.label(ax, TC + 0.04, 1.0, r'$T_c$', color=style.BROKEN, fontsize=11.5, ha='left')
ax.legend(loc='lower left', fontsize=11.5, handlelength=1.6, borderaxespad=0.2)
style.save(fig, __file__)
