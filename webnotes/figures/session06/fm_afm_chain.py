"""Session 6, the two solutions of the chain, a ferromagnet at 20% filling and an antiferromagnet at half filling."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow
import style, _mf

U, n = 4.0, 0.2
kF = np.pi * n                      # all electrons are spin up, so n = kF / pi
mu = -2 * np.cos(kF)
split = U * n                       # the down band is shifted by U n_up = U m, with m = n for the polarized state
# the polarized solution is self-consistent if the empty down band stays above mu
assert -2 + split > mu
m_afm = _mf.moment(U)

fig, axs = plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.4 * style.CM), gridspec_kw=dict(width_ratios=[1, 1.5]))
# (a) bands of the ferromagnet, spin up and spin down
ax = axs[0]
k = np.linspace(-np.pi, np.pi, 400)
ax.plot(k, -2 * np.cos(k), color=style.ACCENT)
ax.plot(k, -2 * np.cos(k) + split, color=style.BROKEN)
style.guide(ax, y=mu, color=style.MUTED, lw=0.9, ls=(0, (3, 2)))
kk = np.linspace(-kF, kF, 50)
ax.plot(kk, -2 * np.cos(kk), color=style.ACCENT, lw=4.0, alpha=0.35, solid_capstyle='butt')
ax.annotate('', xy=(0, -2 + split), xytext=(0, -2), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.8, shrinkA=0, shrinkB=0))
style.label(ax, 0.3, -1.38, r'$Um$', fontsize=8.5, ha='left')
style.label(ax, -np.pi + 0.15, mu + 0.3, r'$\mu$', fontsize=8.5, ha='left')
style.label(ax, 2.0, 1.2, r'$\downarrow$', color=style.BROKEN, fontsize=10)
style.label(ax, 2.35, -0.55, r'$\uparrow$', color=style.ACCENT, fontsize=10)
style.arrows(ax, xlabel=r'$k$', ylabel=r'$E$')
style.label(ax, 0.0, 2.9, r'(a) $n=0.2$, $U=4t$', fontsize=8.5)
ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-2.35, 3.3)

# (b) the antiferromagnet in real space, a unit cell of two sites, the arrow is proportional to the local moment n_up - n_down
ax = axs[1]
ax.axis('off'); ax.set_aspect('equal')
N = 8
for i in range(N):
    ax.add_patch(Circle((i, 0), 0.16, fc=style.INK, ec='none', zorder=3))
    s = 1 if i % 2 == 0 else -1
    L = 1.5 * m_afm
    ax.add_patch(FancyArrow(i, -s * L / 2, 0, s * L, width=0.07, head_width=0.26, head_length=0.22, length_includes_head=True,
                            fc=style.ACCENT if s > 0 else style.BROKEN, ec='none', zorder=4))
ax.plot([-0.4, N - 0.6], [0, 0], color=style.GRID, lw=2, zorder=1)
for c in (0, 2, 4, 6):
    ax.plot([c - 0.35, c + 1.35], [-1.05, -1.05], color=style.MUTED, lw=0.8)
    ax.plot([c - 0.35, c - 0.35], [-0.98, -1.12], color=style.MUTED, lw=0.8)
    ax.plot([c + 1.35, c + 1.35], [-0.98, -1.12], color=style.MUTED, lw=0.8)
style.label(ax, 3.5, -1.45, 'unit cell of two sites', fontsize=8, color=style.MUTED)
style.label(ax, 3.5, 1.75, r'(b) half filling, $U=4t$, $|m|=%.2f$ on every site' % m_afm, fontsize=8.5)
style.label(ax, 3.5, 1.35, r'net magnetization zero, staggered one finite', fontsize=8, color=style.INK)
ax.set_xlim(-0.6, N - 0.4); ax.set_ylim(-1.6, 2.0)
style.save(fig, __file__)
print('m(4t) =', m_afm)
