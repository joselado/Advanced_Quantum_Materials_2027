"""Session 2, the geometry of ARPES and the momentum along the surface, k = sqrt(2 m E_kin) sin(theta) / hbar."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

HB2_2M = 3.80998                                   # hbar^2 / 2 m in eV Angstrom^2
kpar = lambda Ekin, th: np.sqrt(Ekin / HB2_2M) * np.sin(np.radians(th)) * 10      # in nm^-1
assert abs(kpar(20, 10) - 3.98) < 0.02 and abs(kpar(20, 20) - 7.83) < 0.02         # the numbers of the quiz
fig = plt.figure(figsize=(style.WIDTH_CM * style.CM, 5.4 * style.CM))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.0], wspace=0.35)
axL = fig.add_subplot(gs[0]); axR = fig.add_subplot(gs[1])
axL.axis('off'); axL.set_aspect('equal')
# (a) geometry: a sample surface, a photon in, an electron out at the angle theta from the normal
axL.add_patch(plt.Rectangle((-2.4, -1.0), 4.8, 1.0, facecolor=style.LIGHT, alpha=0.35, edgecolor=style.ACCENT, lw=1.0))
style.label(axL, -1.2, -0.62, 'material', color=style.ACCENT, fontsize=8.5)
style.label(axL, 1.3, -0.62, r'$k_\parallel$', color=style.BROKEN, fontsize=9)
axL.plot([0, 0], [0, 2.4], color=style.GRID, lw=0.9, ls=(0, (4, 3)))
th = np.radians(35)
axL.annotate('', xy=(0, 0), xytext=(-2.1, 1.5), arrowprops=dict(arrowstyle='-|>', color=style.WARM, lw=1.4, mutation_scale=9, shrinkA=0, shrinkB=0))
style.label(axL, -1.75, 1.95, r'photon $\hbar\omega$', color=style.WARM, fontsize=8.5)
axL.annotate('', xy=(2.2 * np.sin(th), 2.2 * np.cos(th)), xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color=style.ACCENT, lw=1.6, mutation_scale=9, shrinkA=0, shrinkB=0))
style.label(axL, 1.65, 2.35, r'electron, $E_{\rm kin}$', color=style.ACCENT, fontsize=8.5)
from matplotlib.patches import Arc
axL.add_patch(Arc((0, 0), 1.7, 1.7, theta1=90 - 35, theta2=90, color=style.INK, lw=0.8))
style.label(axL, 0.3, 1.0, r'$\theta$', fontsize=9)
axL.annotate('', xy=(2.2 * np.sin(th), -0.3), xytext=(0, -0.3), arrowprops=dict(arrowstyle='-|>', color=style.BROKEN, lw=1.0, mutation_scale=7, shrinkA=0, shrinkB=0))
axL.plot([2.2 * np.sin(th)] * 2, [-0.3, 2.2 * np.cos(th)], color=style.GRID, lw=0.7, ls=(0, (2, 2)))
axL.set_xlim(-2.5, 2.7); axL.set_ylim(-1.15, 2.7)
# (b) k parallel against the angle for E_kin = 20 eV
th_ = np.linspace(0, 40, 200)
axR.plot(th_, kpar(20, th_), color=style.ACCENT)
for tt in (10, 20):
    axR.plot([tt, tt], [0, kpar(20, tt)], color=style.GRID, lw=0.9); axR.plot([0, tt], [kpar(20, tt)] * 2, color=style.GRID, lw=0.9)
    axR.scatter([tt], [kpar(20, tt)], s=18, color=style.BROKEN, zorder=5)
style.arrows(axR, xlabel=r'$\theta$', ylabel=r'$k_\parallel\ ({\rm nm}^{-1})$')
axR.set_xlim(0, 41); axR.set_ylim(0, 16)
axR.set_xticks([10, 20]); axR.set_xticklabels([r'$10^\circ$', r'$20^\circ$']); axR.set_yticks([kpar(20, 10), kpar(20, 20)]); axR.set_yticklabels(['4.0', '7.8'])
axR.tick_params(length=2.5); axR.spines['bottom'].set_visible(True); axR.spines['left'].set_visible(True)
style.label(axR, 33, 9.0, r'$E_{\rm kin}=20$ eV', color=style.ACCENT, fontsize=8.5)
style.save(fig, __file__)
