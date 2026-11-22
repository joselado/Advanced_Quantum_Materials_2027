"""Session 6, Section 6.4, the two solutions of the chain at U=4t, a ferromagnet at n=0.2 and an antiferromagnet at half
filling.

Both come from the downloadable pyqula script webnotes/scripts/session06/g2_chain_meanfield.py, which the student gets
under the figure. Panel (a) draws its bands of the ferromagnet, with the energy measured from the chemical potential,
and panel (b) is a drawing of the chain whose arrows have the length of its moment. The asserts are in
_g2_chain.check_meanfield, which compares pyqula with the closed forms and with the gap equation of _mf.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from matplotlib.patches import Circle, FancyArrow
import _g2_chain
from _g2_chain import style
plt = style.plt

d = style.run_script('session06/g2_chain_meanfield.py')
_g2_chain.check_meanfield(d)
ks, bfm = d['ks'], d['bands_fm']
lo, hi = bfm[:, 0].min(), bfm[:, 1].min()          # the bottoms of the spin-up and spin-down bands, -0.38 and 0.42
m_afm = abs(float(np.real(d['m_afm'][0])))          # 0.77

fig, axs = plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.8 * style.CM),
                        gridspec_kw=dict(width_ratios=[1, 1.45], wspace=0.32))
# (a) the bands of the ferromagnet, spin up filled up to mu and spin down empty
ax = axs[0]
style.guide(ax, y=0, color=style.MUTED, lw=0.9, ls=(0, (3, 2)))
ax.plot(ks, bfm[:, 0], color=style.ACCENT)
ax.plot(ks, bfm[:, 1], color=style.BROKEN)
filled = bfm[:, 0] <= 0
ax.plot(ks[filled], bfm[filled, 0], color=style.ACCENT, lw=4.5, alpha=0.35, solid_capstyle='butt')
ax.annotate('', xy=(0, hi), xytext=(0, lo), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.8, shrinkA=0, shrinkB=0))
style.label(ax, 0.0, 1.8, r'$Um=0.8t$', fontsize=8.5)
style.label(ax, -np.pi + 0.12, 0.3, r'$\mu$', fontsize=9, ha='left')
style.label(ax, 2.15, 4.4, r'$\downarrow$', color=style.BROKEN, fontsize=11)
style.label(ax, 2.8, 2.65, r'$\uparrow$', color=style.ACCENT, fontsize=11)
style.arrows(ax, xlabel=r'$k$', ylabel=r'$(E-\mu)/t$', ticks=True)
ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'])
ax.set_yticks([lo, hi]); ax.set_yticklabels([r'$%.2f$' % lo, r'$%.2f$' % hi])
ax.tick_params(length=2.5, width=0.6)
ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-0.9, 4.8)
style.label(ax, 0.0, -1.75, r'(a) $n=0.2$, $U=4t$', fontsize=8.5)

# (b) the antiferromagnet in real space, a unit cell of two sites, the arrow is proportional to the moment n_up - n_dn
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
