"""Session 1, the phase of a superconducting order parameter, uniform and with one vortex.

The arrow at each point is Delta(r) = |Delta(r)| exp(i theta(r)) drawn in the complex plane. Uniform state,
theta = 0. Vortex, theta = arg(x + i y) and |Delta| = tanh(r / xi), so the amplitude vanishes at the core
and the phase winds by 2 pi along any loop around it.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

FS = 10.5
xi = 0.9
g = np.linspace(-3, 3, 9)
X, Y = np.meshgrid(g, g)
R = np.hypot(X, Y)
TH = np.arctan2(Y, X)
amp = np.tanh(R / xi)
# the winding of the phase along a circle around the core, computed from the field itself
phi = np.linspace(0, 2 * np.pi, 400)
loop = np.angle(np.exp(1j * np.arctan2(2.2 * np.sin(phi), 2.2 * np.cos(phi))))
winding = np.sum(np.angle(np.exp(1j * np.diff(loop)))) / (2 * np.pi)
assert abs(winding - 1) < 1e-9

fig, axs = plt.subplots(1, 2, figsize=(12.5 * style.CM, 6.6 * style.CM))
fig.subplots_adjust(wspace=0.08, left=0.01, right=0.99, bottom=0.02, top=0.86)
kw = dict(angles='xy', scale_units='xy', scale=1.9, width=0.012, headwidth=3.6, headlength=3.6, headaxislength=3.2)
axs[0].quiver(X, Y, np.ones_like(X), np.zeros_like(Y), color=style.ACCENT, **kw)
axs[1].quiver(X, Y, amp * np.cos(TH), amp * np.sin(TH), color=style.ACCENT, **kw)
axs[1].plot(2.2 * np.cos(phi), 2.2 * np.sin(phi), color=style.BROKEN, lw=1.4, zorder=0)
axs[1].scatter([0], [0], s=40, facecolor='white', edgecolor=style.BROKEN, lw=1.2, zorder=4)
axs[0].set_title('uniform phase', fontsize=FS)
axs[1].set_title('one vortex', fontsize=FS)
style.label(axs[1], 0, -3.75, r'phase winds by $2\pi$', color=style.BROKEN, fontsize=FS)
style.label(axs[0], 0, -3.75, r'$\theta=0$ everywhere', color=style.INK, fontsize=FS)
for ax in axs:
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_xlim(-3.6, 3.6); ax.set_ylim(-4.2, 3.6)
style.save(fig, __file__)
