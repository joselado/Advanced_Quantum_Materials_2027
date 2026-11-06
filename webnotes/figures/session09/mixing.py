"""Session 9, Eq. (9.3), the mixing coefficient of a state with every other state, computed for one matrix element."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style
import matplotlib.pyplot as plt

En = 0.0
Em = np.array([0.35, 1.2, -0.8, -2.0])
V = 0.1                                  # the same matrix element for all
coef = V / (En - Em)                     # coefficient of |m> in Eq. (9.3), lambda = 1
fig, axs = plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.2 * style.CM), gridspec_kw=dict(width_ratios=[1, 1.15], wspace=0.15))
a0, a1 = axs
a0.set_xlim(0, 1); a0.set_ylim(-2.5, 1.7); a0.axis('off')
for e in Em:
    a0.plot([0.15, 0.75], [e, e], color=style.LIGHT, lw=2)
a0.plot([0.15, 0.75], [En, En], color=style.ACCENT, lw=2.6)
style.label(a0, 0.85, En, r'$|n\rangle$', color=style.ACCENT, ha='left')
for i, e in enumerate(Em):
    style.label(a0, 0.85, e, r'$|m_%d\rangle$' % (i + 1), color=style.MUTED, ha='left', fontsize=8.5)
style.label(a0, 0.45, 1.55, r'levels of $H_0$', fontsize=8.5)
a0.annotate('', xy=(0.05, 1.3), xytext=(0.05, -2.3), arrowprops=dict(arrowstyle='-|>', color=style.INK, lw=0.7, mutation_scale=7))
style.label(a0, 0.0, 1.5, r'$E$')
a1.set_xlim(-0.5, 0.5); a1.set_ylim(-2.5, 1.7)
a1.axis('off')
a1.plot([0, 0], [-2.3, 1.3], color=style.INK, lw=0.7)
for i, (e, c) in enumerate(zip(Em, coef)):
    a1.barh(e, c, height=0.16, color=style.BROKEN if c < 0 else style.ACCENT)
    style.label(a1, c + (0.03 if c > 0 else -0.03), e + 0.02, r'$%.2f$' % c, ha='left' if c > 0 else 'right', fontsize=8)
style.label(a1, 0, 1.6, r'coefficient of $|m\rangle$, with $\langle m|V|n\rangle=0.1$', fontsize=8.5)
style.save(fig, __file__)
