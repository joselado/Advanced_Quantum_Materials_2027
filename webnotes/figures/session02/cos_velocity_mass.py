"""Session 2, the energy, the group velocity and the inverse effective mass of the chain band (2.8)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

t = 1.0
p = np.linspace(-np.pi, np.pi, 801)
eps = -2 * t * np.cos(p)
v = 2 * t * np.sin(p)                 # (2.17) in units of a/hbar
im = 2 * t * np.cos(p)                # (2.18) in units of a^2/hbar^2
g1 = np.gradient(eps, p); g2 = np.gradient(g1, p)
assert np.allclose(v[2:-2], g1[2:-2], atol=3e-3) and np.allclose(im[2:-2], g2[2:-2], atol=3e-3)
fig, axs = style.figure(height_cm=4.6, ncols=3)
ttl = [r'energy $\epsilon_\varphi$', r'velocity $\propto\sin\varphi$', r'$1/m^\ast\propto\cos\varphi$']
for a, y, tt, c in zip(axs, (eps, v, im), ttl, (style.ACCENT, style.ACCENT, style.ACCENT)):
    a.plot(p, y, color=c)
    style.guide(a, y=0)
    style.arrows(a, xlabel=r'$\varphi$', ylabel='')
    a.set_xlim(-np.pi - 0.15, np.pi + 0.15); a.set_ylim(-2.7, 2.7)
    a.set_xticks([-np.pi, 0, np.pi]); a.set_xticklabels([r'$-\pi$', r'$0$', r'$\pi$']); a.tick_params(axis='x', length=2.5, labelsize=7.5); a.spines['bottom'].set_visible(True)
    a.set_title(tt, fontsize=8.5, pad=10)
for xx in (-np.pi / 2, np.pi / 2):
    for a in axs: style.guide(a, x=xx, ls=(0, (3, 3)))
axs[1].scatter([-np.pi / 2, np.pi / 2], [-2, 2], s=16, color=style.BROKEN, zorder=5)
axs[2].plot(np.where(im > 0, p, np.nan), im, color=style.LIGHT, lw=2.6)
axs[2].plot(np.where(im < 0, p, np.nan), im, color=style.BROKEN, lw=2.6)
fig.subplots_adjust(wspace=0.3)
style.save(fig, __file__)
