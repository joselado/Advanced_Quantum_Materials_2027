"""Session 9, Eq. (9.4) for the chain, the states that contribute to the static Lindhard function."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

t, mu, T, q = 1.0, 0.0, 0.02, 0.5
k = np.linspace(-np.pi, np.pi, 2001)
eps = lambda k: -2 * t * np.cos(k) - mu
nF = lambda e: 1 / (np.exp(e / T) + 1)
num = nF(eps(k)) - nF(eps(k + q))
den = eps(k + q) - eps(k)
summand = np.where(np.abs(den) > 1e-9, num / np.where(np.abs(den) > 1e-9, den, 1), 0.0)
kF = np.arccos(-mu / (2 * t))    # eps(kF)=0 for mu=0 gives kF=pi/2

fig, axs = plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.2 * style.CM), gridspec_kw=dict(wspace=0.28))
for a in axs:
    style.arrows(a)
a0, a1 = axs
a0.plot(k, eps(k), color=style.ACCENT)
occ = eps(k) < 0
a0.plot(k[occ], eps(k)[occ], color=style.ACCENT, lw=3.6)
style.guide(a0, y=0)
a0.set_ylim(-2.4, 2.9)
a0.plot([kF - q, kF], [-0.55, -0.55], color=style.BROKEN, lw=1.2)
a0.plot([kF - q, kF - q], [-0.7, -0.4], color=style.BROKEN, lw=1.2)
a0.plot([kF, kF], [-0.7, -0.4], color=style.BROKEN, lw=1.2)
style.label(a0, kF - q / 2, -0.95, r'$q$', color=style.BROKEN)
style.label(a0, kF, -2.7, r'$k_F$', color=style.INK)
style.label(a0, -kF, -2.7, r'$-k_F$', color=style.INK)
style.label(a0, 0, -0.45, r'occupied', color=style.ACCENT, fontsize=8)
style.label(a0, 2.3, 2.55, r'empty', color=style.MUTED, fontsize=8)
a0.annotate('', xy=(1.03, 0), xytext=(0, 0), xycoords='axes fraction', textcoords='axes fraction')
a0.annotate(r'$k$', xy=(1.03, 0.0), xycoords='axes fraction', ha='left', va='center')
a0.annotate(r'$\varepsilon(k)$', xy=(0, 1.06), xycoords='axes fraction', ha='center', va='bottom')
a1.plot(k, summand, color=style.BROKEN)
a1.fill_between(k, 0, summand, color=style.BROKEN, alpha=0.15, lw=0)
a1.set_ylim(0, summand.max() * 1.25)
style.label(a1, kF - q / 2, summand.max() * 1.12, r'width $q$', color=style.BROKEN, fontsize=8)
style.label(a1, -kF - q / 2, summand.max() * 1.12, r'width $q$', color=style.BROKEN, fontsize=8)
style.label(a1, kF, -summand.max() * 0.1, r'$k_F$', fontsize=8.5)
style.label(a1, -kF, -summand.max() * 0.1, r'$-k_F$', fontsize=8.5)
a1.annotate(r'$k$', xy=(1.03, 0.0), xycoords='axes fraction', ha='left', va='center')
a1.annotate(r'summand of Eq. (9.4)', xy=(0, 1.06), xycoords='axes fraction', ha='center', va='bottom')
style.save(fig, __file__)
