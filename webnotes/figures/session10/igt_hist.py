"""Session 10, Section 10.6b, the magnetization of single snapshots, for the Ising model (10.9) and the Ising
gauge theory (10.10), at a low and at a high temperature, from Monte Carlo.

Both on a 16 x 16 square lattice with periodic boundaries and J=1. The Ising model uses checkerboard Metropolis
updates of the 256 site spins. The gauge theory has 512 link spins, and one sweep is 512 Metropolis flips of a
random link plus 256 gauge flips of the four links at a random vertex, which change no plaquette and are always
accepted. Low T is 1.5 for the Ising model and 0.2 for the gauge theory, high T is 3.5 and 5 for both. After 500
sweeps, |m| is recorded every 2 sweeps, 1500 times. The seed is fixed."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
style.plt.rcParams.update({'font.size': 11, 'axes.labelsize': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5,
                           'legend.fontsize': 10.5})     # larger than the default, so that the labels read on a phone

rng = np.random.default_rng(11)
L, NTH, NS, EVERY = 16, 500, 1500, 2


def ising(T):
    s = np.ones((L, L), dtype=int)
    mask = (np.add.outer(np.arange(L), np.arange(L)) % 2).astype(bool)
    out = []
    for sweep in range(NTH + NS * EVERY):
        for sub in (mask, ~mask):
            nb = np.roll(s, 1, 0) + np.roll(s, -1, 0) + np.roll(s, 1, 1) + np.roll(s, -1, 1)
            flip = sub & (rng.random((L, L)) < np.exp(-2 * s * nb / T))
            s[flip] *= -1
        if sweep >= NTH and (sweep - NTH) % EVERY == 0:
            out.append(abs(s.mean()))
    return np.array(out)


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


data = {}
data['ising', 'low'] = ising(1.5)
data['ising', 'high'] = ising(3.5)
data['gauge', 'low'], vl = gauge(0.2)
data['gauge', 'high'], vh = gauge(5.0)
for k, d in data.items():
    print(k, 'mean |m| = %.3f, std %.3f' % (d.mean(), d.std()))
print('gauge theory, fraction of plaquettes with product -1: low T %.3f, high T %.3f' % (vl.mean(), vh.mean()))

fig, axs = style.plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.0 * style.CM), sharey=False,
                              gridspec_kw=dict(wspace=0.25))
bins = np.linspace(0, 1, 51)
for ax, model, title in zip(axs, ('ising', 'gauge'), ('Ising model', 'Ising gauge theory')):
    top = 0
    for Tk, col, lab in (('low', style.ACCENT, 'low $T$'), ('high', style.BROKEN, 'high $T$')):
        c, _ = np.histogram(data[model, Tk], bins=bins, density=True)
        ax.stairs(c, bins, color=col, lw=1.6, fill=False, label=lab)
        top = max(top, c.max())
    style.arrows(ax, xlabel=r'$|m|$')
    ax.set_xlim(0, 1.04); ax.set_ylim(0, top * 1.12)
    ax.set_xticks([0, 0.5, 1]); ax.tick_params(axis='x', length=2.5, pad=2)
    ax.set_title(title, fontsize=11.5, pad=10)
axs[0].legend(loc='upper center', fontsize=11.5, handlelength=1.4, borderaxespad=0.1)
style.label(axs[1], 0.5, axs[1].get_ylim()[1] * 0.55, 'both at $|m|\\approx0$', color=style.INK, fontsize=11.5,
            ha='left')
style.save(fig, __file__)
