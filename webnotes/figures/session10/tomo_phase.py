"""Session 10, quiz of Section 10.3b, the states (|up> +- |down>)/sqrt(2) measured along z and along x."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

up = np.array([1, 0]); dn = np.array([0, 1])
plus = (up + dn) / np.sqrt(2); minus = (up - dn) / np.sqrt(2)
xp = (up + dn) / np.sqrt(2); xm = (up - dn) / np.sqrt(2)
pz = lambda psi: [abs(up @ psi) ** 2, abs(dn @ psi) ** 2]
px = lambda psi: [abs(xp @ psi) ** 2, abs(xm @ psi) ** 2]
fig, axs = plt.subplots(1, 2, figsize=(9.0 * style.CM, 4.4 * style.CM), gridspec_kw=dict(wspace=0.3), sharey=True)
for ax, f, names, title in zip(axs, (pz, px), ((r'$\uparrow$', r'$\downarrow$'), (r'$+$', r'$-$')), ('measure along $z$', 'measure along $x$')):
    style.arrows(ax)
    for j, (psi, c) in enumerate(((plus, style.ACCENT), (minus, style.BROKEN))):
        p = f(psi)
        ax.bar(np.arange(2) + (j - 0.5) * 0.36, p, width=0.34, color=c)
    ax.set_xlim(-0.6, 1.6); ax.set_ylim(0, 1.15)
    for i, nme in enumerate(names):
        style.label(ax, i, -0.1, nme, fontsize=9)
    ax.set_title(title, fontsize=8.5, color=style.INK, pad=3)
axs[0].text(0.0, -0.32, r'blue $(|\uparrow\rangle+|\downarrow\rangle)/\sqrt{2}$, red $(|\uparrow\rangle-|\downarrow\rangle)/\sqrt{2}$', transform=axs[0].transAxes, fontsize=7.5, color=style.INK)
style.save(fig, __file__)
