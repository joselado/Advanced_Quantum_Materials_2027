"""Session 1, the phase of a bilinear and of a pairing term under the gauge transformation (1.10)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

fig, axs = plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.6 * style.CM))
th = np.linspace(0, 2 * np.pi, 200)
arrow = lambda ax, d, **kw: ax.annotate('', xy=d, xytext=(0, 0), arrowprops=dict(dict(arrowstyle='-|>', lw=1.5, mutation_scale=9, shrinkA=0, shrinkB=0), **kw))
for ax in axs:
    ax.set_aspect('equal'); ax.axis('off')
    ax.plot(np.cos(th), np.sin(th), color=style.GRID, lw=1.0)
    ax.plot([-1.35, 1.35], [0, 0], color=style.GRID, lw=0.8); ax.plot([0, 0], [-1.35, 1.35], color=style.GRID, lw=0.8)
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.55, 1.55)
phi = np.pi / 2
# (a) c^dagger c: the phases e^{-i phi} and e^{i phi} cancel, the term stays at 1
ax = axs[0]
arrow(ax, (1, 0), color=style.ACCENT)
for s, c in ((1, style.LIGHT), (-1, style.WARM)):
    ax.add_patch(plt.matplotlib.patches.Arc((0, 0), 0.7, 0.7, theta1=0, theta2=0, color=c))
ax.annotate('', xy=(np.cos(phi) * 0.75, np.sin(phi) * 0.75), xytext=(0.75, 0), arrowprops=dict(arrowstyle='-|>', color=style.LIGHT, lw=1.0, connectionstyle='arc3,rad=0.35', shrinkA=0, shrinkB=0, mutation_scale=7))
ax.annotate('', xy=(np.cos(-phi) * 0.75, np.sin(-phi) * 0.75), xytext=(0.75, 0), arrowprops=dict(arrowstyle='-|>', color=style.WARM, lw=1.0, connectionstyle='arc3,rad=-0.35', shrinkA=0, shrinkB=0, mutation_scale=7))
style.label(ax, -0.35, 1.0, r'$c\to c\,e^{i\varphi}$', color=style.LIGHT, fontsize=8.5, ha='right')
style.label(ax, -0.35, -1.0, r'$c^\dagger\to c^\dagger e^{-i\varphi}$', color=style.WARM, fontsize=8.5, ha='right')
style.label(ax, 1.1, 0.18, r'$c^\dagger c$', color=style.ACCENT, ha='left', fontsize=9)
style.label(ax, -1.55, 1.5, '(a)', ha='left', fontsize=9)
ax.set_title(r'phases cancel, $\varphi=\pi/2$', fontsize=8.5)
# (b) c c, with the factor e^{2 i phi}, for phi = pi/4 and pi/2
ax = axs[1]
arrow(ax, (1, 0), color=style.ACCENT)
style.label(ax, 1.1, 0.18, r'$\Delta$', color=style.ACCENT, ha='left', fontsize=9)
for ph, lab, pos in ((np.pi / 4, r'$\varphi=\pi/4$', (0.1, 1.2)), (np.pi / 2, r'$\varphi=\pi/2$', (-1.15, 0.2))):
    d = (np.cos(2 * ph), np.sin(2 * ph))
    arrow(ax, d, color=style.BROKEN, alpha=0.9)
    style.label(ax, pos[0], pos[1], lab, color=style.BROKEN, fontsize=8.5, ha='left' if ph < 1 else 'center')
ax.annotate('', xy=(np.cos(np.pi / 2) * 0.55, np.sin(np.pi / 2) * 0.55), xytext=(0.55, 0), arrowprops=dict(arrowstyle='-|>', color=style.MUTED, lw=0.9, connectionstyle='arc3,rad=0.3', shrinkA=0, shrinkB=0, mutation_scale=7))
ax.annotate('', xy=(-0.55, 0.0), xytext=(0.0, 0.55), arrowprops=dict(arrowstyle='-|>', color=style.MUTED, lw=0.9, connectionstyle='arc3,rad=0.3', shrinkA=0, shrinkB=0, mutation_scale=7))
style.label(ax, 0.65, 0.75, r'$2\varphi$', color=style.MUTED, fontsize=8.5)
style.label(ax, -1.55, 1.5, '(b)', ha='left', fontsize=9)
ax.set_title(r'$\Delta\to\Delta\,e^{2i\varphi}$', fontsize=8.5)
assert np.isclose(np.exp(2j * np.pi / 2), -1)
style.save(fig, __file__)
