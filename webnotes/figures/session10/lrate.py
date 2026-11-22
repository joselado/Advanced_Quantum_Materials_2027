"""Session 10, quiz of Section 10.2, gradient descent on L=theta^2/2 for three learning rates.

The update of (10.1) is theta -> theta - eta dL/dtheta = (1-eta) theta, from theta=1. Redrawn on 2026-11-22 with ticks
on both axes, so that the values +-1 and the factor 1.5 of the caption are read on the axes."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

L = lambda th: th ** 2 / 2
grad = lambda th, d=1e-6: (L(th + d) - L(th - d)) / (2 * d)     # a numerical gradient, not the formula


def run(eta, n=4, th=1.0):
    out = [th]
    for _ in range(n):
        th = th - eta * grad(th)
        out.append(th)
    return np.array(out)


n = np.arange(0, 5)
# the gradient of theta^2/2 is theta, so the update is theta -> (1-eta) theta
for eta in (0.5, 1.0, 2.0, 2.5):
    assert np.allclose(run(eta), (1 - eta) ** n, atol=1e-8)
# eta=0.5 halves theta, eta=1 reaches the minimum in one step, eta=2 jumps between +1 and -1, eta=2.5 multiplies
# theta by -1.5 and the loss by 2.25 at every step
assert np.allclose(run(0.5)[1:] / run(0.5)[:-1], 0.5, atol=1e-6)
assert abs(run(1.0)[1]) < 1e-8
assert np.allclose(run(2.0), [1, -1, 1, -1, 1], atol=1e-6)
th = run(2.5)
assert np.allclose(th[1:] / th[:-1], -1.5, atol=1e-6) and np.allclose(L(th[1:]) / L(th[:-1]), 2.25, atol=1e-6)
assert abs(th[-1] - 5.0625) < 1e-6 and th.min() > -3.6 and th.max() < 5.2     # the points fit in the window
assert run(0.5)[-1] < 0.07                                                    # 1/16 at the last step

fig, ax = style.figure(height_cm=6.2, width_cm=8.8)
style.arrows(ax, xlabel=r'step $n$', ylabel=r'$\theta$', ticks=True)
for eta, c in ((0.5, style.ACCENT), (2.0, style.MUTED), (2.5, style.BROKEN)):
    ax.plot(n, run(eta), '-o', color=c, ms=3.5, lw=1.4)
    print(eta, np.round(run(eta), 4))
style.guide(ax, y=0)
style.guide(ax, y=1, ls=(0, (2, 2))); style.guide(ax, y=-1, ls=(0, (2, 2)))
ax.set_xlim(-0.25, 5.3); ax.set_ylim(-3.9, 5.6)
ax.set_xticks([0, 1, 2, 3, 4])
ax.set_yticks([-3, -2, -1, 0, 1, 2, 3, 4, 5])
ax.set_yticklabels(['$-3$', '$-2$', '$-1$', '0', '1', '2', '3', '4', '5'])
ax.tick_params(length=2.5, width=0.6, pad=2)
style.label(ax, 4.2, 0.0, r'$\eta=0.5$', color=style.ACCENT, fontsize=8.5, ha='left')
style.label(ax, 4.2, 1.15, r'$\eta=2$', color=style.MUTED, fontsize=8.5, ha='left')
style.label(ax, 4.2, 5.06, r'$\eta=2.5$', color=style.BROKEN, fontsize=8.5, ha='left')
style.save(fig, __file__)
