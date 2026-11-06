"""Session 10, quiz of Section 10.2, XOR with no hidden layer and with one hidden layer of two neurons."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

fig, axs = plt.subplots(1, 2, figsize=(9.0 * style.CM, 4.6 * style.CM), gridspec_kw=dict(wspace=0.15))
A = [(0, 0), (1, 1)]; B = [(0, 1), (1, 0)]
for ax in axs:
    ax.set_aspect('equal'); ax.axis('off')
    ax.plot([-0.1, 1.1, 1.1, -0.1, -0.1], [-0.1, -0.1, 1.1, 1.1, -0.1], color=style.GRID, lw=0.8)
    ax.plot(*zip(*A), 'o', color=style.ACCENT, ms=7)
    ax.plot(*zip(*B), 's', color=style.BROKEN, ms=7)
    ax.set_xlim(-0.3, 1.3); ax.set_ylim(-0.3, 1.3)
xs = np.linspace(-0.1, 1.1, 200)
cl = lambda y: np.clip(y, -0.1, 1.1)
def seg(ax, y, **kw):
    m = (y >= -0.1) & (y <= 1.1)
    ax.plot(xs[m], y[m], **kw)
a = axs[0]
seg(a, 0.5 + 0.0 * xs, color=style.MUTED, lw=1, ls=(0, (4, 3)))
seg(a, 1.1 - xs, color=style.MUTED, lw=1, ls=(0, (4, 3)))
a.set_title('no hidden layer', fontsize=8.5, color=style.INK, pad=2)
b = axs[1]
seg(b, 0.5 - xs, color=style.INK, lw=1.2)
seg(b, 1.5 - xs, color=style.INK, lw=1.2)
b.fill_between(xs, cl(0.5 - xs), cl(1.5 - xs), color=style.WARM, alpha=0.3, lw=0)
b.set_title('one hidden layer', fontsize=8.5, color=style.INK, pad=2)
style.save(fig, __file__)
