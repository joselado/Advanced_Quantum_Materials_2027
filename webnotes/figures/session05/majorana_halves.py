"""Session 5, one electron mode is two Majorana halves, and what matters is which halves are bound together."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
import style

# the algebra that the figure shows, checked on the two-dimensional Fock space of one mode
c = np.array([[0, 1], [0, 0]], complex)
gA, gB = c + c.conj().T, -1j * (c - c.conj().T)
assert np.allclose(gA @ gA, np.eye(2)) and np.allclose(gB @ gB, np.eye(2)) and np.allclose(gA @ gB + gB @ gA, 0)
assert np.allclose(0.5 * (gA + 1j * gB), c)
assert np.allclose(1j * gA @ gB, 2 * c.conj().T @ c - np.eye(2))     # the parity of the mode is i gamma_A gamma_B

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(style.WIDTH_CM * style.CM, 6.6 * style.CM))
ax.axis('off')
ax.set_aspect('equal')

def capsule(x0, x1, y, r=0.33, color=style.MUTED):
    ax.add_patch(FancyBboxPatch((x0 - r, y - r), x1 - x0 + 2 * r, 2 * r, boxstyle=f'round,pad=0,rounding_size={r}',
                                fc='none', ec=color, lw=1.0, ls=(0, (4, 2))))

def ball(x, y, name, col, r=0.2, free=False):
    ax.add_patch(Circle((x, y), r, fc=col, ec=style.INK, lw=0.7, zorder=3))
    style.label(ax, x, y - 0.52, name, fontsize=8)

# top row, one electron mode and its two halves
y = 3.3
ax.add_patch(Circle((0.6, y), 0.42, fc=style.LIGHT, ec=style.ACCENT, lw=1.2))
style.label(ax, 0.6, y, r'$c$', color='white', fontsize=11, zorder=4)
style.label(ax, 0.6, y - 0.95, 'one electron mode', fontsize=8)
ax.annotate('', xy=(3.9, y), xytext=(1.4, y), arrowprops=dict(arrowstyle='-|>', color=style.INK, lw=0.9, mutation_scale=9))
style.label(ax, 2.65, y + 0.45, r'$c=\frac{1}{2}(\gamma_A+i\gamma_B)$', fontsize=8.5)
ball(4.7, y, r'$\gamma_A$', style.ACCENT)
ball(5.7, y, r'$\gamma_B$', style.BROKEN)
capsule(4.7, 5.7, y)
style.label(ax, 5.2, y + 0.75, r'bound at one site', fontsize=8)
style.label(ax, 7.0, y, r'$\gamma_A^\dagger=\gamma_A$, $\gamma_A^2=1$' + '\n' + r'$i\gamma_A\gamma_B=2c^\dagger c-1$', fontsize=8.5, ha='left')

# bottom row, four sites, halves bound between neighboring sites, two halves left free
y = 0.0
xs = np.arange(8) * 1.0 + 0.6
for i, x in enumerate(xs):
    col = style.ACCENT if i % 2 == 0 else style.BROKEN
    ball(x, y, '', col)
for n in range(4):
    style.label(ax, xs[2 * n] + 0.5, y - 0.6, rf'site {n+1}', fontsize=7.5, color=style.MUTED)
for n in range(3):
    capsule(xs[2 * n + 1], xs[2 * n + 2], y)
for x in (xs[0], xs[-1]):
    ax.plot([x], [y + 0.52], marker='*', color=style.BROKEN, ms=7, ls='none')
style.label(ax, xs[0], y + 1.05, 'free', color=style.BROKEN, fontsize=8)
style.label(ax, xs[-1], y + 1.05, 'free', color=style.BROKEN, fontsize=8)
style.label(ax, 4.1, y + 1.05, r'halves bound between neighboring sites', fontsize=8)
ax.set_xlim(-0.3, 10.4); ax.set_ylim(-1.0, 4.5)
style.save(fig, __file__)
