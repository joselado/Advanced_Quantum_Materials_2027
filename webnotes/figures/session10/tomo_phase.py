"""Session 10, quiz of Section 10.3b, the states (|up> +- |down>)/sqrt(2) measured along z and along x.

The probabilities are the Born rule in the two bases. Along z both states give 0.5 and 0.5, along x the state with +
gives the outcome + with probability 1 and the state with - gives the outcome -, as the conventions sheet says."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import style

up = np.array([1, 0]); dn = np.array([0, 1])
plus = (up + dn) / np.sqrt(2); minus = (up - dn) / np.sqrt(2)
xp = (up + dn) / np.sqrt(2); xm = (up - dn) / np.sqrt(2)
pz = lambda psi: [abs(up @ psi) ** 2, abs(dn @ psi) ** 2]
px = lambda psi: [abs(xp @ psi) ** 2, abs(xm @ psi) ** 2]
assert np.allclose(pz(plus), [0.5, 0.5]) and np.allclose(pz(minus), [0.5, 0.5])
assert np.allclose(px(plus), [1, 0]) and np.allclose(px(minus), [0, 1])

fig, axs = plt.subplots(1, 2, figsize=(9.0 * style.CM, 5.0 * style.CM), gridspec_kw=dict(wspace=0.45))
for ax, f, names, title in zip(axs, (pz, px), ((r'$\uparrow$', r'$\downarrow$'), (r'$+$', r'$-$')),
                               ('measured along $z$', 'measured along $x$')):
    style.arrows(ax, ylabel='probability', ticks=True)
    for j, (psi, c) in enumerate(((plus, style.ACCENT), (minus, style.BROKEN))):
        ax.bar(np.arange(2) + (j - 0.5) * 0.36, f(psi), width=0.34, color=c)
    ax.set_xlim(-0.6, 1.6); ax.set_ylim(0, 1.12)
    ax.set_xticks([0, 1]); ax.set_xticklabels(names, fontsize=10)
    ax.set_yticks([0, 0.5, 1]); ax.set_yticklabels(['0', '0.5', '1'])
    ax.tick_params(direction='out', length=3, width=0.6)
    ax.set_title(title, fontsize=8.5, color=style.INK, pad=24)
fig.legend(handles=[Patch(color=style.ACCENT, label=r'$(|\uparrow\rangle+|\downarrow\rangle)/\sqrt{2}$'),
                    Patch(color=style.BROKEN, label=r'$(|\uparrow\rangle-|\downarrow\rangle)/\sqrt{2}$')],
           loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=8, handlelength=1.0, columnspacing=1.2)
style.save(fig, __file__)
