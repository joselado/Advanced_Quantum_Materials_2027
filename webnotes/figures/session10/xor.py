"""Session 10, quiz of Section 10.2, XOR with no hidden layer and with one hidden layer of two neurons.

The four inputs (x1, x2) of XOR, with the label y=0 as circles and y=1 as squares. On the left two straight lines
that fail, on the right the two lines x1+x2=1/2 and x1+x2=3/2 of two hidden step neurons, whose difference is XOR.
Redrawn on 2026-11-22 with the axes x1 and x2, the ticks 0 and 1 and a key of the two labels."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import style

A = [(0, 0), (1, 1)]          # label y=0
B = [(0, 1), (1, 0)]          # label y=1
X = np.array(A + B, float)
Y = np.array([0, 0, 1, 1])

# no line w.x+b separates the classes: the two points of each class have the same sum, (1,1), so w.x+b summed over
# a class is the same number for both classes and cannot be negative for one and positive for the other
assert np.allclose(X[Y == 0].sum(0), X[Y == 1].sum(0))
rng = np.random.default_rng(0)
w = rng.normal(size=(200000, 2)); b = rng.normal(size=200000) * 2
s = X @ w.T + b
sep = np.all(s[Y == 1] > 0, axis=0) & np.all(s[Y == 0] < 0, axis=0)
sep |= np.all(s[Y == 1] < 0, axis=0) & np.all(s[Y == 0] > 0, axis=0)
assert not sep.any()
# the two tries of the left panel, x2=1/2 and x1+x2=1.1, each put points of both labels on one side
for side in (X[:, 1] > 0.5, X.sum(1) > 1.1):
    assert len(set(Y[side])) == 2 or len(set(Y[~side])) == 2
# two hidden step neurons on the lines x1+x2=1/2 and x1+x2=3/2, and the output their difference, give XOR exactly,
# and the band between the two lines holds exactly the inputs with y=1
step = lambda z: (z > 0).astype(int)
out = step(X.sum(1) - 0.5) - step(X.sum(1) - 1.5)
assert np.array_equal(out, Y)
assert np.array_equal(((X.sum(1) > 0.5) & (X.sum(1) < 1.5)).astype(int), Y)

fig, axs = plt.subplots(1, 2, figsize=(9.4 * style.CM, 5.6 * style.CM), gridspec_kw=dict(wspace=0.45))
xs = np.linspace(-0.2, 1.2, 300)
cl = lambda y: np.clip(y, -0.2, 1.2)


def seg(ax, y, **kw):
    m = (y >= -0.2) & (y <= 1.2)
    ax.plot(xs[m], y[m], **kw)


for ax in axs:
    ax.set_aspect('equal')
    ax.set_xlim(-0.2, 1.2); ax.set_ylim(-0.2, 1.2)
    for s_ in ('top', 'right'):
        ax.spines[s_].set_visible(False)
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$x_1$', labelpad=0); ax.set_ylabel(r'$x_2$', labelpad=1)
    ax.plot(*zip(*A), 'o', color=style.ACCENT, ms=7, zorder=3, clip_on=False)
    ax.plot(*zip(*B), 's', color=style.BROKEN, ms=7, zorder=3, clip_on=False)
a = axs[0]
seg(a, 0.5 + 0.0 * xs, color=style.MUTED, lw=1, ls=(0, (4, 3)))
seg(a, 1.1 - xs, color=style.MUTED, lw=1, ls=(0, (4, 3)))
a.set_title('no hidden layer', fontsize=8.5, color=style.INK, pad=4)
b = axs[1]
seg(b, 0.5 - xs, color=style.INK, lw=1.2)
seg(b, 1.5 - xs, color=style.INK, lw=1.2)
b.fill_between(xs, cl(0.5 - xs), cl(1.5 - xs), color=style.WARM, alpha=0.3, lw=0)
b.set_title('one hidden layer', fontsize=8.5, color=style.INK, pad=4)
keys = [Line2D([], [], ls='', marker='o', color=style.ACCENT, ms=6, label=r'$y=0$'),
        Line2D([], [], ls='', marker='s', color=style.BROKEN, ms=6, label=r'$y=1$')]
fig.legend(handles=keys, loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.1), handletextpad=0.2,
           columnspacing=1.5, fontsize=9)
style.save(fig, __file__)
