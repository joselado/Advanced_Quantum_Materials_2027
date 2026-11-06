"""Session 8, quiz of 8.10, the phases picked up around a plaquette after a gauge rotation add up to zero."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
from matplotlib.patches import Circle, FancyArrowPatch

rng = np.random.default_rng(2)
theta = rng.uniform(0, 2 * np.pi, 4)
dphi = [theta[i] - theta[(i + 1) % 4] for i in range(4)]       # chi_ij -> exp(i(theta_i - theta_j)) chi_ij around the loop 1->2->3->4->1
assert abs(np.exp(1j * sum(dphi)) - 1) < 1e-12

fig, ax = style.plt.subplots(figsize=(7.6 * style.CM, 6.0 * style.CM))
ax.set_xlim(-2.7, 2.7); ax.set_ylim(-2.7, 1.95); ax.set_aspect('equal'); ax.axis('off')
P = [(-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0)]
names = [r'$\theta_1$', r'$\theta_2$', r'$\theta_3$', r'$\theta_4$']
for i in range(4):
    a = np.array(P[i]); b = np.array(P[(i + 1) % 4])
    ax.add_patch(FancyArrowPatch(a + 0.22 * (b - a) / 2, b - 0.22 * (b - a) / 2, arrowstyle='-|>', mutation_scale=10, color=style.MUTED, lw=1.4))
    mid = (a + b) / 2; out = mid / np.linalg.norm(mid)
    style.label(ax, *(mid + 0.5 * out * (1 if i % 2 == 0 else 1)), r'$\theta_%d-\theta_%d$' % (i + 1, (i + 1) % 4 + 1), fontsize=8.0, color=style.BROKEN)
for p, n in zip(P, names):
    ax.add_patch(Circle(p, 0.2, facecolor=style.ACCENT, edgecolor='none', zorder=3))
    q = np.array(p) * 1.0
    style.label(ax, p[0] + 0.0, p[1] + (-0.42 if p[1] < 0 else 0.42), n, fontsize=8.5, color=style.ACCENT)
style.label(ax, 0, -2.05, r'the four phases add up to $0$', fontsize=8.8, color=style.INK)
style.label(ax, 0, -2.5, r'so $\Phi$ is unchanged', fontsize=8.8, color=style.INK)
style.save(fig, __file__)
