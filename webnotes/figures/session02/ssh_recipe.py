"""Session 2, section 2.7, the recipe of the Bloch Hamiltonian (2.12) for the chain with alternating hoppings (2.13).

Left, two cells of the chain, the intracell hopping 1 and the intercell hopping eta, and where each one goes in the
2x2 matrix H(phi), a drawing with no axes. Right, the two bands for eta = 0.6 and for eta = 1, from the pyqula script
webnotes/scripts/session02/g2_ssh_bands.py, which the student downloads under the figure. The energies are in units
of the intracell hopping. The bands are asserted against +-|1 + eta exp(-i phi)| of (2.13), and the matrix of pyqula
against (2.13) entry by entry."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import style

FS = 10.5
d = style.run_script('session02/g2_ssh_bands.py')
p, bands, gap = d['phi'], d['bands'], d['gap']
for eta, E in bands.items():
    assert np.allclose(E[:, 1], np.abs(1 + eta * np.exp(-1j * p))) and np.allclose(E[:, 0], -E[:, 1]), eta
hk = d['h'].get_hk_gen()                                   # the last Hamiltonian of the script, eta = 1
for f in (0.3, 1.7):
    m = np.asarray(hk([f / (2 * np.pi), 0., 0.]))
    assert np.isclose(m[0, 1], 1 + 1.0 * np.exp(-1j * f)) and np.isclose(m[1, 0], 1 + 1.0 * np.exp(1j * f))
E06, E10 = bands[0.6], bands[1.0]
assert np.isclose(p[0], -np.pi) and np.isclose(p[-1], np.pi)
assert np.isclose(gap, 2 * abs(1 - 0.6)) and np.isclose(gap, 0.8)            # the caption: 0.8 at phi = +-pi
assert np.isclose(E06[-1, 1] - E06[-1, 0], 0.8) and np.isclose(E10[-1, 1], 0, atol=1e-12) and np.isclose(E10[0, 1], 0, atol=1e-12)
assert np.isclose(E10[200, 1], 2) and np.isclose(E06[200, 1], 1.6)            # the top of each band, at phi = 0

fig = plt.figure(figsize=(12.5 * style.CM, 6.4 * style.CM))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 0.92], wspace=0.45)
axL, axR = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
axL.axis('off'); axL.set_xlim(-0.4, 4.45); axL.set_ylim(-3.3, 1.4)
# the chain, two cells
xs = [0.3, 1.3, 2.7, 3.7]
for i, x in enumerate(xs):
    style.label(axL, x, 0.55, 'AB'[i % 2], fontsize=FS)
axL.plot([xs[0], xs[1]], [0, 0], color=style.ACCENT, lw=3.2)
axL.plot([xs[2], xs[3]], [0, 0], color=style.ACCENT, lw=3.2)
axL.plot([xs[1], xs[2]], [0, 0], color=style.BROKEN, lw=1.3)
axL.plot([-0.3, xs[0]], [0, 0], color=style.BROKEN, lw=1.3)
axL.plot([xs[3], 4.3], [0, 0], color=style.BROKEN, lw=1.3)
axL.scatter(xs, [0] * 4, s=50, color=[style.ACCENT, style.LIGHT] * 2, zorder=3, edgecolor=style.ACCENT, lw=0.8)
for x0 in (xs[0], xs[2]):
    axL.add_patch(Rectangle((x0 - 0.3, -0.32), 1.6, 1.25, fill=False, ec=style.MUTED, lw=0.7, ls=(0, (3, 2))))
style.label(axL, 0.8, -0.6, r'$1$', color=style.ACCENT, fontsize=FS)
style.label(axL, 2.0, -0.6, r'$\eta$', color=style.BROKEN, fontsize=FS)
# the matrix, entry by entry
style.label(axL, 0.25, -2.15, r'$H(\varphi)=$', fontsize=FS)
cy = [-1.55, -2.75]
for x in (0.95, 4.2):
    s_ = 1 if x < 2 else -1
    axL.plot([x + 0.12 * s_, x, x, x + 0.12 * s_], [-1.05, -1.05, -3.25, -3.25], color=style.INK, lw=0.9)
style.label(axL, 1.75, cy[0], r'$0$', fontsize=FS)
style.label(axL, 3.35, cy[1], r'$0$', fontsize=FS)
style.label(axL, 2.5, cy[0], r'$1$', color=style.ACCENT, fontsize=FS)
style.label(axL, 2.62, cy[0], r'$+\eta e^{-i\varphi}$', color=style.BROKEN, fontsize=FS, ha='left')
style.label(axL, 1.2, cy[1], r'$1$', color=style.ACCENT, fontsize=FS)
style.label(axL, 1.32, cy[1], r'$+\eta e^{i\varphi}$', color=style.BROKEN, fontsize=FS, ha='left')
# the bands
for E, col, lw in ((E10, style.MUTED, 1.5), (E06, style.ACCENT, 1.8)):   # eta=1 in the colour of its label
    axR.plot(p, E[:, 0], color=col, lw=lw); axR.plot(p, E[:, 1], color=col, lw=lw)
plt.rcParams['font.size'] = 10.5                                  # the name at the arrow tip, read at 390 px
style.arrows(axR, xlabel=r'$\varphi$')
axR.set_ylabel('$\\epsilon$ in units of\nthe intracell hopping', fontsize=10, labelpad=2)
axR.set_xticks([-np.pi, 0, np.pi]); axR.set_xticklabels([r'$-\pi$', r'$0$', r'$\pi$'])
axR.set_yticks([-2, 0, 2]); axR.tick_params(labelsize=FS, length=2.5)
axR.spines['bottom'].set_visible(True); axR.spines['left'].set_visible(True)
axR.set_xlim(-np.pi, np.pi + 0.15); axR.set_ylim(-2.3, 2.45)
axR.annotate('', xy=(np.pi - 0.12, E06[-1, 1]), xytext=(np.pi - 0.12, E06[-1, 0]),
             arrowprops=dict(arrowstyle='<->', color=style.BROKEN, lw=1.0, shrinkA=0, shrinkB=0))
style.label(axR, np.pi - 0.3, 0, r'$2|1-\eta|$', color=style.BROKEN, fontsize=FS, ha='right')
style.label(axR, 0, 1.25, r'$\eta=0.6$', color=style.ACCENT, fontsize=FS)
style.label(axR, -1.0, 2.15, r'$\eta=1$', color=style.MUTED, fontsize=FS)
style.save(fig, __file__)
