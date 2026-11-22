"""Session 5, the lowest levels of an open Kitaev chain as a function of the chemical potential.

The exact chain (5.19) in numpy, from _g5_kitaev.bdg, with N=60 sites and Delta=0.7t, and the three lowest levels E>=0 at each
mu. Redrawn on 2026-11-21 with the axes mu/t and E/t and their ticks, under the same name."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import _g5_kitaev as kc
style = kc.style

N, t, D = 60, 1.0, 0.7
mus = np.linspace(-3.4, 3.4, 341)
low = np.array([np.sort(np.abs(kc.levels(N, t, mu, D)))[::2][:3] for mu in mus])   # the levels come in pairs +E, -E

# checks against the text, the zero modes of the sweet spot and the criterion (5.22)
assert np.sum(np.abs(kc.levels(N, t, 0.0, t)) < 1e-9) == 2
inside = low[abs(mus) < 1.8, 0]
outside = low[abs(mus) > 2.3, 0]
assert inside.max() < 1e-3 and outside.min() > 0.05, (inside.max(), outside.min())
# the numbers of the caption: the lowest bulk level 1.4t at mu=0, which is 2 Delta of the infinite chain, the pair below 0.003t
# up to |mu|=1.9t, and the lowest level 0.04t at |mu|=2t, where the gap of the infinite chain closes
l0 = np.sort(np.abs(kc.levels(N, t, 0.0, D)))[::2]
assert abs(l0[1] - 1.4) < 0.005 and abs(2 * D - 1.4) < 1e-12, l0[1]
assert low[abs(mus) <= 1.9 + 1e-9, 0].max() < 0.003, low[abs(mus) <= 1.9 + 1e-9, 0].max()
for m in (-2.0, 2.0):
    l2 = np.sort(np.abs(kc.levels(N, t, m, D)))[::2]
    assert abs(l2[0] - 0.04) < 0.005, l2[0]
k = np.linspace(-np.pi, np.pi, 4001)
for m, kc0 in ((-2.0, 0.0), (2.0, np.pi)):
    E = np.sqrt((2 * t * np.cos(k) + m)**2 + 4 * D**2 * np.sin(k)**2)
    assert E.min() < 1e-12 and abs(abs(k[np.argmin(E)]) - kc0) < 1e-9        # the infinite chain closes at k=0 and at k=pi
print('lowest bulk level at mu=0', round(l0[1], 4), 'pair up to |mu|=1.9', round(low[abs(mus) <= 1.9 + 1e-9, 0].max(), 5),
      'lowest level at |mu|=2', round(l2[0], 4))

plt.rcParams.update({'font.size': 10.5})
fig, ax = plt.subplots(figsize=(13.0 * style.CM, 5.8 * style.CM))
ax.axvspan(-2, 2, color=style.GRID, alpha=0.45, lw=0, zorder=0)
for x in (-2, 2):
    style.guide(ax, x=x, color=style.MUTED, lw=0.8, ls=(0, (3, 2)))
for j, a in enumerate((1.0, 0.55, 0.55)):
    ax.plot(mus, low[:, j], color=style.ACCENT, alpha=a, lw=1.8 if j == 0 else 1.2)
ax.set_xlim(-3.4, 3.4); ax.set_ylim(0, 1.75)
kc.frame(ax, [(-2, '$-2$'), (0, '$0$'), (2, '$2$')], [(0, '$0$'), (0.7, '$0.7$'), (1.4, '$1.4$')], r'$\mu/t$', r'$E/t$')
style.label(ax, 0, 0.55, r'topological, $|\mu|<2t$', fontsize=9.5)
style.label(ax, 0, 0.3, r'two states near $E=0$', fontsize=9.5, color=style.ACCENT)
for s in (-1, 1):
    style.label(ax, s * 2.85, 0.3, 'trivial', fontsize=9.5)
style.save(fig, __file__)
