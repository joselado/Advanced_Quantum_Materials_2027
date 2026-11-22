"""Session 5, Section 5.16, the open Kitaev chain at Delta=t and mu=0: its BdG levels and where the two zero levels sit.

The exact chain (5.19) in numpy, from _g5_kitaev.bdg, with N=20 sites. (a) The 40 BdG levels against their index, two at zero
and 19 at each of +-2t. (b) The weight on each site of the two zero levels, averaged over the two, half on the first site and
half on the last, which are gamma_1 and gamma_2N of (5.21)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import _g5_kitaev as kc
style = kc.style

N, t, mu, D = 20, 1.0, 0.0, 1.0
e = kc.levels(N, t, mu, D)
w, nzero = kc.zero_weight(N, t, mu, D)
# the numbers of the caption: two levels at zero, 19 at -2t and 19 at +2t, half of the weight on site 1 and half on site N
assert nzero == 2 and np.sum(np.abs(e) < 1e-12) == 2
assert np.sum(np.abs(e - 2 * t) < 1e-12) == N - 1 and np.sum(np.abs(e + 2 * t) < 1e-12) == N - 1
assert abs(w[0] - 0.5) < 1e-12 and abs(w[-1] - 0.5) < 1e-12 and w[1:-1].max() < 1e-12
print('zero levels', nzero, 'levels at +2t', int(np.sum(np.abs(e - 2) < 1e-12)), 'weight on site 1 and N', w[0], w[-1])

plt.rcParams.update({'font.size': 10.5})
fig, axs = plt.subplots(1, 2, figsize=(12.6 * style.CM, 5.0 * style.CM), gridspec_kw=dict(wspace=0.42))
kc.draw_levels(axs[0], e, (-2.6, 2.6), [(-2, '$-2$'), (0, '$0$'), (2, '$2$')])
kc.draw_weight(axs[1], w, (0, 0.6), [(0, '$0$'), (0.5, '$0.5$')], lw=2.4)
for ax, tag in ((axs[0], '(a)'), (axs[1], '(b)')):
    ax.text(0.5, 1.04, tag, transform=ax.transAxes, ha='center', va='bottom', fontsize=10.5)
style.save(fig, __file__)
