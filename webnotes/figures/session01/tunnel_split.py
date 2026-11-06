"""Session 1, the two lowest states of a double well, with the splitting that a finite barrier gives."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

x = np.linspace(-2.2, 2.2, 1200); dx = x[1] - x[0]
V0 = 8.0
V = V0 * (x ** 2 - 1) ** 2
# H = -d^2/dx^2 + V, finite differences
H = np.diag(2 / dx ** 2 + V) - (np.eye(len(x), k=1) + np.eye(len(x), k=-1)) / dx ** 2
w, v = np.linalg.eigh(H)
psi0, psi1 = v[:, 0] / np.sqrt(dx), v[:, 1] / np.sqrt(dx)
if psi0.sum() < 0: psi0 = -psi0
if psi1[x > 0].sum() < 0: psi1 = -psi1
assert np.allclose(psi0, psi0[::-1], atol=1e-3) and np.allclose(psi1, -psi1[::-1], atol=1e-3)   # even and odd
fig, axs = plt.subplots(2, 1, figsize=(style.WIDTH_CM * style.CM * 0.62, 7.0 * style.CM), gridspec_kw=dict(height_ratios=[1, 1.3], hspace=0.12), sharex=True)
for a in axs:
    for s in ('top', 'right'): a.spines[s].set_visible(False)
    a.spines['left'].set_color(style.INK); a.spines['bottom'].set_color(style.INK)
a = axs[0]
a.plot(x, psi0, color=style.ACCENT); a.plot(x, psi1 - 1.6, color=style.BROKEN)
a.axhline(0, color=style.GRID, lw=0.8, zorder=0); a.axhline(-1.6, color=style.GRID, lw=0.8, zorder=0)
a.set_yticks([]); a.spines['bottom'].set_visible(False); a.tick_params(bottom=False)
style.label(a, -2.15, 0.9, r'$\psi_+$, even', color=style.ACCENT, ha='left', fontsize=8.5)
style.label(a, -2.15, -2.5, r'$\psi_-$, odd', color=style.BROKEN, ha='left', fontsize=8.5)
a.set_ylim(-3.0, 1.6)
b = axs[1]
b.plot(x, V, color=style.GRID, lw=1.4)
b.plot([-1.7, 1.7], [w[0]] * 2, color=style.ACCENT, lw=1.4)
b.plot([-1.7, 1.7], [w[1]] * 2, color=style.BROKEN, lw=1.4)
b.set_xlim(-2.2, 2.2); b.set_ylim(0, 9.5); b.set_yticks([]); b.set_xticks([])
b.set_ylabel(r'$E$', rotation=0, labelpad=6)
b.annotate('', xy=(0.0, w[1]), xytext=(0.0, w[0]), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.8, shrinkA=0, shrinkB=0))
style.label(b, 0.12, (w[0] + w[1]) / 2, r'$2\Delta$', ha='left', fontsize=8.5)
style.label(b, 0, 8.0, 'barrier', color=style.MUTED, fontsize=8)
print('levels', w[:2], 'split', w[1] - w[0])
style.save(fig, __file__)
