"""Session 10, quiz of Section 10.2, gradient descent on L=theta^2/2 for three learning rates."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

n = np.arange(0, 6)
fig, ax = style.figure(height_cm=5.0, width_cm=8.8)
for eta, c, lab in ((0.5, style.ACCENT, r'$\eta=0.5$'), (2.0, style.MUTED, r'$\eta=2$'), (2.5, style.BROKEN, r'$\eta=2.5$')):
    th = (1 - eta) ** n
    ax.plot(n, th, '-o', color=c, ms=3.5, lw=1.4)
    print(eta, th)
style.guide(ax, y=0)
ax.set_xlim(-0.2, 5.9); ax.set_ylim(-8, 8)
style.arrows(ax, xlabel='step', ylabel=r'$\theta$')
style.label(ax, 5.55, 0.9, r'$\eta=0.5$', color=style.ACCENT, fontsize=8)
style.label(ax, 5.55, -2.3, r'$\eta=2$', color=style.MUTED, fontsize=8)
style.label(ax, 4.75, 6.6, r'$\eta=2.5$', color=style.BROKEN, fontsize=8)
style.save(fig, __file__)
