"""Session 5, the electron and the hole band of the Nambu doubling, and the gap that pairing opens at their crossing."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgb
import style

t, mu, Delta = 1.0, -1.0, 0.45
k = np.linspace(-np.pi, np.pi, 801)
eps = -2 * t * np.cos(k) - mu            # the chain dispersion of (5.8), with a single orbital
kF = np.arccos(-mu / (2 * t))            # eps(kF)=0
# the checks of what the figure says
E = np.sqrt(eps**2 + Delta**2)           # (5.9)
assert abs(eps[np.argmin(abs(k - kF))]) < 0.02 and abs(2 * E.min() - 2 * Delta) < 1e-3

def mix(w):
    a, b = np.array(to_rgb(style.ACCENT)), np.array(to_rgb(style.BROKEN))
    return [tuple(w_ * a + (1 - w_) * b) for w_ in w]

def colored(ax, x, y, w):
    pts = np.c_[x, y].reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    ax.add_collection(LineCollection(segs, colors=mix(0.5 * (w[:-1] + w[1:])), linewidths=2.0, capstyle='round'))

fig, axs = style.figure(height_cm=5.6, ncols=2)
ax = axs[0]
colored(ax, k, eps, np.ones_like(k))
colored(ax, k, -eps, np.zeros_like(k))
style.guide(ax, y=0)
for s in (-1, 1):
    ax.plot([s * kF], [0], 'o', color=style.INK, ms=3.5, zorder=5)
style.arrows(ax, xlabel=r'$k$', ylabel=r'$E$')
style.label(ax, -1.7, 3.85, r'electron, $\varepsilon(k)$', color=style.ACCENT, fontsize=8.5)
style.label(ax, -1.7, -3.55, r'hole, $-\varepsilon(k)$', color=style.BROKEN, fontsize=8.5)
style.label(ax, 0, 4.9, r'(a) $\Delta=0$', fontsize=9)
ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-4.0, 4.4)

ax = axs[1]
w = 0.5 * (1 + eps / E)                  # the electron weight u^2 of the upper branch
colored(ax, k, E, w)
colored(ax, k, -E, 1 - w)
style.guide(ax, y=0)
for s in (-1, 1):
    x0 = s * kF
    ax.annotate('', xy=(x0, Delta), xytext=(x0, -Delta), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.8, shrinkA=0, shrinkB=0))
style.label(ax, kF + 0.12, 0.0, r'$2|\Delta|$', ha='left', fontsize=8.5)
style.arrows(ax, xlabel=r'$k$', ylabel=r'$E$')
style.label(ax, 0, 4.9, r'(b) $\Delta\neq0$', fontsize=9)
style.label(ax, 0, -3.55, r'$E=\pm\sqrt{\varepsilon^2+|\Delta|^2}$', fontsize=8.5)
ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-4.0, 4.4)
style.save(fig, __file__)
