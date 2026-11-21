"""Session 2, section 2.7, the uniform chain described with a cell of three sites, in the feedback of a quiz. The band
folds into three bands.

The bands come from the pyqula script webnotes/scripts/session02/g2_chain_fold.py, chain().get_supercell(3) with
tij=[-1.], the sign of (2.5), and they are asserted against the branches -2t cos[(phi + 2 pi m)/3]. The left panel is a
drawing of the chain with no axes."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

t = 1.0
d = style.run_script('session02/g2_chain_fold.py')
p, B = d['phi'], d['bands']                                         # phase of the large cell, phi = 3 k a
ref = np.sort(np.array([[-2 * t * np.cos((f + 2 * np.pi * m) / 3) for m in range(3)] for f in p]), axis=1)
assert np.allclose(B, ref, atol=1e-9)                                # the folded cosine
assert np.isclose(p[200], 0) and np.allclose(B[200], [-2, 1, 1])      # phi=0 gives -2t, t, t as in the quiz
fig = plt.figure(figsize=(9.6 * style.CM, 4.0 * style.CM))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.0], wspace=0.35)
axL = fig.add_subplot(gs[0]); axR = fig.add_subplot(gs[1])
axL.axis('off'); axL.set_aspect('equal')
x = np.arange(9)
axL.plot([-0.5, 8.5], [0, 0], color=style.INK, lw=1.8)
axL.scatter(x, np.zeros(9), s=34, color=style.ACCENT, zorder=3)
for c in range(3):
    axL.add_patch(plt.Rectangle((3 * c - 0.4, -0.45), 2.8, 0.9, facecolor='none', edgecolor=style.BROKEN, lw=1.0, ls=(0, (4, 2))))
style.label(axL, 1.0, 0.95, 'unit cell', color=style.BROKEN, fontsize=8.5)
axL.set_xlim(-0.8, 8.8); axL.set_ylim(-1.0, 1.4)
for j, c in enumerate((style.ACCENT, style.LIGHT, style.BROKEN)):
    axR.plot(p, B[:, j], color=c)
style.guide(axR, y=0)
style.arrows(axR, xlabel=r'$\varphi$', ylabel=r'$\epsilon/t$')
axR.set_xlim(-np.pi, np.pi); axR.set_ylim(-2.6, 2.6)
axR.set_xticks([-np.pi, 0, np.pi]); axR.set_xticklabels([r'$-\pi$', r'$0$', r'$\pi$'])
axR.set_yticks([-2, 1, 2]); axR.set_yticklabels(['$-2$', '$1$', '$2$'])
axR.tick_params(length=2.5, labelsize=8.5)
axR.spines['bottom'].set_visible(True); axR.spines['left'].set_visible(True)
style.save(fig, __file__)
