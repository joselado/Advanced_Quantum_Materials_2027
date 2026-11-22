"""Session 5, where the lowest state of an open Kitaev chain sits, in the topological and in the trivial phase.

The exact chain (5.19) in numpy, from _g5_kitaev.bdg, with N=40 sites and Delta=0.5t, at mu=t and mu=2.5t. The weight on site n
is |u_n|^2+|v_n|^2 of the lowest state with E>0. Redrawn on 2026-11-21 with the weight and the site as named axes with ticks,
on a scale that the two panels share, under the same name."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import _g5_kitaev as kc
style = kc.style

N, t, D = 40, 1.0, 0.5
w1, e1 = kc.lowest_state(N, t, 1.0, D)
w2, e2 = kc.lowest_state(N, t, 2.5, D)
assert abs(w1.sum() - 1) < 1e-9 and e1 < 1e-4 and e2 > 0.3
assert w1[:4].sum() + w1[-4:].sum() > 0.9 and w2[N // 2 - 8:N // 2 + 8].sum() > 0.5
# the numbers of the caption and of the panels: E below 1e-9 t at mu=t, and 0.51t at mu=2.5t
assert e1 < 1e-9 and abs(e2 - 0.51) < 0.005, (e1, e2)
assert np.allclose(w1, w1[::-1], atol=1e-5) and np.allclose(w2, w2[::-1], atol=1e-9)
print('E at mu=t', e1, 'E at mu=2.5t', round(e2, 4), 'largest weight', round(w1.max(), 4), round(w2.max(), 4))

plt.rcParams.update({'font.size': 10.5})
fig, axs = plt.subplots(2, 1, figsize=(13.0 * style.CM, 7.2 * style.CM), sharex=True, gridspec_kw=dict(hspace=0.45))
yt = [(0, '$0$'), (0.1, '$0.1$'), (0.2, '$0.2$'), (0.3, '$0.3$')]
for ax, w, col, ttl in ((axs[0], w1, style.ACCENT, r'(a) $\mu=t$, topological, $E\approx 0$'),
                        (axs[1], w2, style.BROKEN, r'(b) $\mu=2.5t$, trivial, $E=%.2ft$' % e2)):
    kc.draw_weight(ax, w, (0, 0.38), yt, color=col, lw=2.2)
    ax.text(0.5, 1.02, ttl, transform=ax.transAxes, ha='center', va='bottom', fontsize=10.5)
axs[0].set_xlabel('')
axs[0].tick_params(labelbottom=True)
axs[1].set_xticks([1, 20, 40]); axs[1].set_xticklabels(['1', '20', '40'])
axs[0].set_xticks([1, 20, 40]); axs[0].set_xticklabels(['1', '20', '40'])
style.save(fig, __file__)
