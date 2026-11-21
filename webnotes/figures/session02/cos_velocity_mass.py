"""Session 2, Section 2.9, the energy, the group velocity and the inverse effective mass of the chain band (2.8).

The calculation is the pyqula script webnotes/scripts/session02/g3_chain_velocity_mass.py, which the student downloads
under the figure: the band of the chain with the hopping -1, the sign of (2.5), and its first and second derivative by
finite differences, with t = hbar = a = 1. They are checked here against 2t sin(phi) and 2t cos(phi). Each panel names
its quantity with its unit on the vertical axis."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

d = style.run_script('session02/g3_chain_velocity_mass.py')
p, eps, v, im = d['phi'], np.asarray(d['e'], float), d['velocity'], d['inverse_mass']
assert np.isclose(p[0], -np.pi) and np.isclose(p[-1], np.pi)
assert np.allclose(eps, -2 * np.cos(p), atol=1e-12)                  # (2.8) with t = 1, the sign of the page
assert np.allclose(v, 2 * np.sin(p), atol=1e-4)                      # (2.17), largest in size at +-pi/2
assert np.allclose(im, 2 * np.cos(p), atol=1e-3)                     # (2.18), +2 at the bottom, -2 at the top
assert np.isclose(np.abs(p[np.argmax(v)]), np.pi / 2, atol=1e-2) and np.isclose(p[np.argmin(v)], -np.pi / 2, atol=1e-2)
assert np.isclose(v.max(), 2, atol=1e-4) and np.isclose(im[400], 2, atol=1e-4) and np.isclose(im[0], -2, atol=1e-3)
sign = np.sign(im[np.abs(im) > 1e-3])
change = p[np.abs(im) > 1e-3][np.nonzero(np.diff(sign))[0]]
assert len(change) == 2 and np.allclose(np.abs(change), np.pi / 2, atol=1e-2)   # the sign changes at +-pi/2

fig, axs = style.plt.subplots(1, 3, figsize=(style.WIDTH_CM * style.CM, 4.9 * style.CM))
names = (r'$\epsilon/t$', r'$\hbar v/ta$', r'$\hbar^2/m^\ast ta^2$')
for a, y, nm in zip(axs, (eps, v, im), names):
    a.plot(p, y, color=style.ACCENT)
    style.guide(a, y=0)
    for xx in (-np.pi / 2, np.pi / 2):
        style.guide(a, x=xx, ls=(0, (3, 3)))
    style.arrows(a, xlabel=r'$\varphi$', ylabel=nm)
    a.set_xlim(-np.pi - 0.15, np.pi + 0.15); a.set_ylim(-2.7, 2.7)
    a.set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
    a.set_xticklabels([r'$-\pi$', '', r'$0$', '', r'$\pi$'])
    a.set_yticks([-2, 0, 2]); a.set_yticklabels([r'$-2$', r'$0$', r'$2$'])
    a.tick_params(length=2.5, width=0.6, labelsize=8, pad=1.5)
axs[1].scatter([-np.pi / 2, np.pi / 2], [-2, 2], s=16, color=style.BROKEN, zorder=5)
axs[2].plot(np.where(im > 0, p, np.nan), im, color=style.LIGHT, lw=2.6)
axs[2].plot(np.where(im < 0, p, np.nan), im, color=style.BROKEN, lw=2.6)
for a, tag in zip(axs, ('(a)', '(b)', '(c)')):
    a.text(0.0, -0.3, tag, transform=a.transAxes, fontsize=8.5, ha='left')
fig.subplots_adjust(wspace=0.42)
style.save(fig, __file__)
