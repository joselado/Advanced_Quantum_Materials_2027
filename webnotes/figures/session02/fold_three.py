"""Session 2, the uniform chain described with a cell of three sites, the band folds into three bands."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

t = 1.0
p = np.linspace(-np.pi, np.pi, 601)                                # phase of the large cell, phi = 3 k a
def bands(phi):
    H = np.zeros((3, 3), complex)
    for i in range(3):
        H[i, (i + 1) % 3] += -t * (np.exp(1j * phi) if i == 2 else 1)
        H[(i + 1) % 3, i] += -t * (np.exp(-1j * phi) if i == 2 else 1)
    return np.linalg.eigvalsh(H)
B = np.array([bands(f) for f in p])
ref = np.sort(np.array([[-2 * t * np.cos((f + 2 * np.pi * m) / 3) for m in range(3)] for f in p]), axis=1)
assert np.allclose(B, ref, atol=1e-9)                                # the folded cosine
assert np.allclose(B[300], [-2, 1, 1])                               # phi=0 gives -2t, t, t as in the quiz
fig = plt.figure(figsize=(9.6 * style.CM, 4.0 * style.CM))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.0], wspace=0.3)
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
axR.set_xticks([-np.pi, 0, np.pi]); axR.set_xticklabels([r'$-\pi$', r'$0$', r'$\pi$']); axR.tick_params(axis='x', length=2.5); axR.spines['bottom'].set_visible(True)
style.save(fig, __file__)
