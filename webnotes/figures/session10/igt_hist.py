"""Session 10, Section 10.6b, the magnetization of single snapshots, for the Ising model (10.9) and the Ising
gauge theory (10.10), at a low and at a high temperature, from Monte Carlo.

Both on a 16 x 16 square lattice with periodic boundaries and J=1. The Ising side is the pyqula script
scripts/session10/g4_ising_snapshots.py, which style.run_script runs, single flips of Metropolis on the 256 site spins,
1000 snapshots every two sweeps after 500 sweeps, of which this figure takes k_BT = 1.5 and 3.5. pyqula has no four-spin
term, so the gauge theory is numpy. It has 512 link spins, and one sweep is 512 Metropolis flips of a random link plus
256 gauge flips of the four links at a random vertex, which change no plaquette and are always accepted, at k_BT = 0.2
and 5. After 500 sweeps, |m| is recorded every 2 sweeps, 1500 times. The seed is fixed. On 256 spins |m| takes the
values k/128 and on 512 spins k/256, so a bin holds three or six of these values and its edges sit between them. The
numbers of the caption are asserted below."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
style.plt.rcParams.update({'font.size': 11, 'axes.labelsize': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5,
                           'legend.fontsize': 10.5})     # larger than the default, so that the labels read on a phone

rng = np.random.default_rng(11)
L, NTH, NS, EVERY = 16, 500, 1500, 2


def gauge(T):
    h = np.ones((L, L), dtype=int)      # h[x, y], the link from (x, y) to (x+1, y)
    v = np.ones((L, L), dtype=int)      # v[x, y], the link from (x, y) to (x, y+1)

    def plaq(x, y):
        return h[x, y] * v[(x + 1) % L, y] * h[x, (y + 1) % L] * v[x, y]

    out, viol = [], []
    for sweep in range(NTH + NS * EVERY):
        links = rng.integers(0, 2 * L * L, size=2 * L * L)
        u = rng.random(2 * L * L)
        for k, r in zip(links, u):
            d, x, y = divmod(k, L * L)[0], (k % (L * L)) // L, k % L
            if d == 0:      # h[x, y] is in the plaquettes (x, y) and (x, y-1)
                P = plaq(x, y) + plaq(x, (y - 1) % L)
                if r < np.exp(-2 * P / T):
                    h[x, y] *= -1
            else:           # v[x, y] is in the plaquettes (x, y) and (x-1, y)
                P = plaq(x, y) + plaq((x - 1) % L, y)
                if r < np.exp(-2 * P / T):
                    v[x, y] *= -1
        for k in rng.integers(0, L * L, size=L * L):     # gauge flips at a vertex
            x, y = divmod(k, L)
            h[x, y] *= -1; h[(x - 1) % L, y] *= -1; v[x, y] *= -1; v[x, (y - 1) % L] *= -1
        if sweep >= NTH and (sweep - NTH) % EVERY == 0:
            out.append(abs((h.sum() + v.sum()) / (2 * L * L)))
            P = h * np.roll(v, -1, 0) * np.roll(h, -1, 1) * v
            viol.append((P < 0).mean())
    return np.array(out), np.array(viol)


absm = style.run_script('session10/g4_ising_snapshots.py')['absm']
data = {('ising', 'low'): absm[1.5], ('ising', 'high'): absm[3.5]}
data['gauge', 'low'], vl = gauge(0.2)
data['gauge', 'high'], vh = gauge(5.0)
for k, d in data.items():
    print(k, 'mean |m| = %.3f, std %.3f, from %.3f to %.3f' % (d.mean(), d.std(), d.min(), d.max()))
print('gauge theory, fraction of plaquettes with product -1: low T %.2e, high T %.3f' % (vl.mean(), vh.mean()))

# the caption: the Ising histograms do not overlap, the two of the gauge theory both sit at |m| of about 0.04
assert data['ising', 'high'].max() < data['ising', 'low'].min()
assert round(data['ising', 'low'].mean(), 2) == 0.99 and data['ising', 'high'].mean() < 0.15
for T in ('low', 'high'):
    assert abs(data['gauge', T].mean() - 0.04) < 0.008 and data['gauge', T].max() < 0.2
assert vl.mean() < 1e-3 and round(vh.mean(), 2) == 0.40       # the plaquettes at -1, (1 - tanh(J/T))/2 on the torus

bins = {'ising': (3 * np.arange(44) - 0.5) / 128, 'gauge': (6 * np.arange(44) - 0.5) / 256}
temps = {'ising': ('1.5', '3.5'), 'gauge': ('0.2', '5')}
dens = {k: np.histogram(d, bins=bins[k[0]], density=True)[0] for k, d in data.items()}
top = max(c.max() for c in dens.values())

fig, axs = style.plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.4 * style.CM), gridspec_kw=dict(wspace=0.32))
for ax, model, title in zip(axs, ('ising', 'gauge'), ('Ising model', 'Ising gauge theory')):
    for Tk, col, ls, T in (('low', style.ACCENT, '-', temps[model][0]), ('high', style.BROKEN, (0, (3, 1.6)), temps[model][1])):
        ax.stairs(dens[model, Tk], bins[model], color=col, lw=1.6, ls=ls, label=r'$k_BT=%sJ$' % T)
    style.arrows(ax, xlabel=r'$|m|$', ylabel=r'$p(|m|)$', ticks=True)
    ax.set_xlim(0, 1.04); ax.set_ylim(0, top * 1.08)
    ax.set_xticks([0, 0.5, 1]); ax.set_xticklabels(['0', '0.5', '1'])
    ax.set_yticks([0, 10, 20, 30] if top > 30 else [0, 10, 20])
    ax.tick_params(length=2.5, pad=2)
    ax.set_title(title, fontsize=11.5, pad=14)
    ax.legend(loc='upper center', bbox_to_anchor=(0.55, 0.98), fontsize=10.5, handlelength=1.6, borderaxespad=0.1)
style.save(fig, __file__)
