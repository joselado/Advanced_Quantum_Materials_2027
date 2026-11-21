"""Session 2, section 2.5, the chain with a second-neighbor hopping eta, and the band of (2.9) for three values of eta.

The bands are the pyqula script webnotes/scripts/session02/g2_chain_second_neighbor.py, which the student downloads
under the figure. It takes tij=[-1., -eta], the sign of (2.5), so the band is -2t cos(phi) - 2 eta cos(2 phi) with t=1,
which is asserted below against the closed form. The left panel is a drawing of the chain with no axes."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

plt.rcParams['font.size'] = 10.5                                  # the names at the arrow tips, read at 390 px
d = style.run_script('session02/g2_chain_second_neighbor.py')
p, bands = d['phi'], d['bands']
t = 1.0
for eta, e in bands.items():                                       # pyqula gives (2.9) with t = 1
    assert np.allclose(e, -2 * t * np.cos(p) - 2 * eta * np.cos(2 * p), atol=1e-12), eta
assert np.isclose(p[0], -np.pi) and np.isclose(p[-1], np.pi)
# interior extrema: one for eta=0 and eta=0.2 (the minimum at 0), three for eta=0.5 (the minimum and two new maxima)
n_ext = lambda e: np.sum(np.diff(np.sign(np.diff(e))) != 0)
assert n_ext(bands[0.0]) == 1 and n_ext(bands[0.2]) == 1 and n_ext(bands[0.5]) == 3
# the caption: eta=0.5 is above t/4, phi=pi is a local minimum at 1 with two maxima at 1.5 next to it, cos(phi)=-1/2
e5 = bands[0.5]
assert 0.5 > t / 4 > 0.2
assert np.isclose(e5[-1], 1.0) and np.isclose(e5.max(), 1.5, atol=1e-4) and np.isclose(e5.min(), -3.0)
assert np.isclose(np.cos(p[np.argmax(e5)]), -0.5, atol=0.01)
assert np.isclose(bands[0.2][-1], bands[0.2].max())                 # for eta=0.2 phi=pi is still the maximum

fig = plt.figure(figsize=(style.WIDTH_CM * style.CM, 5.0 * style.CM))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.15], wspace=0.3)
axL = fig.add_subplot(gs[0]); axR = fig.add_subplot(gs[1])
axL.axis('off'); axL.set_aspect('equal')
N = 7
x = np.arange(N)
axL.plot([x[0] - 0.6, x[-1] + 0.6], [0, 0], color=style.GRID, lw=1.2, zorder=1)
axL.scatter(x, np.zeros(N), s=40, color=style.ACCENT, zorder=3)
for i in range(N - 1):                                             # nearest neighbor t, straight bond
    axL.plot([x[i], x[i + 1]], [0, 0], color=style.INK, lw=1.8, zorder=2)
style.label(axL, 1.5, -0.4, r'$t$', fontsize=10.5)
for i in range(N - 2):                                             # second neighbor eta, arc above
    c = style.BROKEN if i in (1,) else style.LIGHT
    th = np.linspace(0, np.pi, 40)
    axL.plot(x[i] + 1 + np.cos(th), 0.12 + 0.75 * np.sin(th), color=c, lw=1.2 if i != 1 else 1.8, zorder=2)
style.label(axL, 3.0, 1.2, r'$\eta$', color=style.BROKEN, fontsize=10.5)
axL.set_xlim(-0.8, N - 0.2); axL.set_ylim(-0.9, 1.5)
# bands
for eta, col, lw in ((0.0, style.MUTED, 1.4), (0.2, style.LIGHT, 1.8), (0.5, style.ACCENT, 1.8)):   # eta=0 in the colour of its key
    axR.plot(p, bands[eta], color=col, lw=lw)
style.guide(axR, y=0)
style.arrows(axR, xlabel=r'$\varphi$', ylabel=r'$\epsilon/t$')
axR.set_xlim(-np.pi, np.pi); axR.set_ylim(-3.2, 2.4)
axR.set_xticks([-np.pi, 0, np.pi]); axR.set_xticklabels([r'$-\pi$', r'$0$', r'$\pi$'])
axR.set_yticks([-3, -2, 0, 1, 2]); axR.set_yticklabels(['$-3$', '$-2$', '$0$', '$1$', '$2$'])
axR.tick_params(length=2.5, labelsize=10)
axR.spines['bottom'].set_visible(True); axR.spines['left'].set_visible(True)
for y0, col, txt in ((-1.45, style.MUTED, r'$\eta=0$'), (-2.0, style.LIGHT, r'$\eta=0.2$'), (-2.55, style.ACCENT, r'$\eta=0.5$')):
    axR.plot([-3.0, -2.55], [y0, y0], color=col, lw=1.8)
    style.label(axR, -2.45, y0, txt, color=col, fontsize=10, ha='left')
axR.scatter([np.pi], [e5[-1]], s=18, color=style.ACCENT, zorder=5, clip_on=False)
axR.annotate('new minimum', xy=(np.pi, e5[-1]), xytext=(1.25, -2.45), fontsize=10, color=style.INK, ha='left',
             arrowprops=dict(arrowstyle='-', color=style.MUTED, lw=0.7))
style.save(fig, __file__)
