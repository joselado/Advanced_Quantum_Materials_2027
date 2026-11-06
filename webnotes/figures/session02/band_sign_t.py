"""Session 2, the chain band for t=+1 and t=-1."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

p = np.linspace(-np.pi, np.pi, 600)
fig, ax = style.figure(height_cm=4.2, width_cm=9.6)
ax.plot(p, -2 * 1 * np.cos(p), color=style.ACCENT)
ax.plot(p, -2 * (-1) * np.cos(p), color=style.BROKEN)
style.guide(ax, y=0)
style.arrows(ax, xlabel=r'$\varphi$', ylabel=r'$\epsilon$')
ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-2.8, 2.8)
ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', r'$0$', r'$\pi$']); ax.tick_params(axis='x', length=2.5); ax.spines['bottom'].set_visible(True)
ax.scatter([0, 0], [-2, 2], s=16, color=style.INK, zorder=5)
style.label(ax, 0.35, -2.0, r'$-2$', ha='left', fontsize=8.5, color=style.ACCENT)
style.label(ax, 0.35, 2.0, r'$+2$', ha='left', fontsize=8.5, color=style.BROKEN)
style.label(ax, -2.4, 2.45, r'$t=+1$', color=style.ACCENT, fontsize=8.5)
style.label(ax, -2.4, -2.45, r'$t=-1$', color=style.BROKEN, fontsize=8.5)
style.save(fig, __file__)
