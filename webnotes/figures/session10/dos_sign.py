"""Session 10, quiz of Section 10.7, the chains with t=+1 and t=-1 have different bands and the same density of states."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

k = np.linspace(-np.pi, np.pi, 4001)
fig, axs = plt.subplots(1, 2, figsize=(9.0 * style.CM, 4.6 * style.CM), gridspec_kw=dict(wspace=0.25))
for a in axs:
    style.arrows(a)
a, b = axs
for t, c in ((1, style.ACCENT), (-1, style.BROKEN)):
    a.plot(k, -2 * t * np.cos(k), color=c, lw=1.6 if t > 0 else 1.2, ls='-' if t > 0 else (0, (4, 2)))
a.set_ylim(-2.6, 2.9)
style.arrows(a, xlabel=r'$k$', ylabel=r'$\epsilon$')
style.label(a, 0, -2.3, r'$t=1$', color=style.ACCENT, fontsize=8)
style.label(a, 0, 2.35, r'$t=-1$', color=style.BROKEN, fontsize=8)
E = np.linspace(-1.95, 1.95, 400)
dos = 1 / (np.pi * np.sqrt(4 - E ** 2))
h, ed = np.histogram(-2 * np.cos(np.linspace(-np.pi, np.pi, 2000001)), bins=40, range=(-1.9, 1.9), density=True)
mid = 0.5 * (ed[1:] + ed[:-1])
exact = 1 / (np.pi * np.sqrt(4 - mid ** 2))
print('histogram against closed form, largest relative deviation:', np.abs(h * (1 - 0.0) / 1 * 0 + h / h.sum() / (exact / exact.sum()) - 1).max())
b.plot(dos, E, color=style.ACCENT, lw=2.4)
b.plot(dos, E, color=style.BROKEN, lw=1.0, ls=(0, (4, 2)))
b.set_ylim(-2.6, 2.9); b.set_xlim(0, 0.9)
style.arrows(b, xlabel='DOS', ylabel=r'$E$')
style.label(b, 0.55, 0, r'the same for $\pm t$', color=style.INK, fontsize=8)
style.save(fig, __file__)
