"""Session 9, the localization length of the 1D random chain, xi(W) from a transfer matrix at E=0, in units of the lattice constant."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

rng = np.random.default_rng(7)
Ws = np.logspace(np.log10(0.25), np.log10(4.0), 14)
E, L, ns = 0.0, 200000, 8
W = np.repeat(Ws, ns)
psi0 = np.ones_like(W); psi1 = np.zeros_like(W) + 0.3
ly = np.zeros_like(W)
for n in range(L):
    w = W * (2 * rng.random(W.size) - 1)          # uniform in [-W, W], as in the page
    psi0, psi1 = (w - E) * psi0 - psi1, psi0
    if n % 50 == 49:
        s = np.hypot(psi0, psi1); ly += np.log(s); psi0 /= s; psi1 /= s
gamma = (ly / L).reshape(len(Ws), ns).mean(axis=1)
xi = 1 / gamma
slope = np.polyfit(np.log(Ws[:8]), np.log(xi[:8]), 1)[0]
print('xi', np.round(xi, 1)); print('slope at weak disorder', slope)

fig, ax = plt.subplots(figsize=(style.WIDTH_CM * style.CM, 5.4 * style.CM))
style.arrows(ax, xlabel=r'$W/t$', ylabel=r'$\xi$ (sites)')
ax.set_xscale('log'); ax.set_yscale('log')
ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
ax.plot(Ws, xi, 'o', color=style.ACCENT, ms=4)
Wg = np.array([0.22, 1.2])
C = xi[2] * Ws[2] ** 2
ax.plot(Wg, C / Wg ** 2, color=style.MUTED, lw=1.0, ls=(0, (4, 3)))
style.label(ax, 0.42, C / 0.42 ** 2 * 1.9, r'$\xi\propto(t/W)^2$', color=style.MUTED, ha='left', fontsize=8.5)
Lsamp = 100
style.guide(ax, y=Lsamp, color=style.BROKEN, ls=(0, (4, 3)), lw=1.0)
style.label(ax, 3.2, Lsamp * 1.6, r'sample length $100$', color=style.BROKEN, ha='center', fontsize=8.5)
ax.set_xlim(0.2, 5); ax.set_ylim(1, xi.max() * 2)
style.label(ax, 1.0, 0.55, r'$1$', fontsize=8) if False else None
ax.set_xticks([0.25, 0.5, 1, 2, 4]); ax.set_xticklabels(['0.25', '0.5', '1', '2', '4'], fontsize=8)
ax.tick_params(axis='x', length=2.5)
ax.set_yticks([1, 10, 100, 1000]); ax.set_yticklabels(['1', '10', '100', '1000'], fontsize=8)
ax.tick_params(axis='y', length=2.5)
ax.minorticks_off()
style.save(fig, __file__)
