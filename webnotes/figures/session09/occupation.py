"""Session 9, Eq. (9.4) for the chain, the states that contribute to the static Lindhard function.

The half-filled chain eps(k) = -2t cos k with t=1, so k_F = pi/2, at q=0.5 and T=0.02t. Left, the band in units of t with
the occupied states thick. Right, the summand (n_F(eps(k)) - n_F(eps(k+q)))/(eps(k+q) - eps(k)) of (9.4) in units of 1/t.
It is different from zero only in the windows (k_F - q, k_F) and (-k_F - q, -k_F), which is asserted below. A summand is not
an output of pyqula, so this is numpy."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11, 'axes.labelsize': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5})

t, mu, T, q = 1.0, 0.0, 0.02, 0.5
assert (q, T, mu) == (0.5, 0.02, 0.0)                                    # the parameters of the caption, half filling
k = np.linspace(-np.pi, np.pi, 4001)
eps = lambda k: -2 * t * np.cos(k) - mu
nF = lambda e: 0.5 * (1 - np.tanh(e / (2 * T)))
num = nF(eps(k)) - nF(eps(k + q))
den = eps(k + q) - eps(k)
summand = np.where(np.abs(den) > 1e-9, num / np.where(np.abs(den) > 1e-9, den, 1), 0.0)
kF = np.arccos(-mu / (2 * t))    # eps(kF)=0 for mu=0 gives kF=pi/2

# ---- the two windows of width q, next to the Fermi points, and nothing elsewhere
win = ((k > kF - q) & (k < kF)) | ((k > -kF - q) & (k < -kF))
margin = ((k > kF - q - 0.15) & (k < kF + 0.15)) | ((k > -kF - q - 0.15) & (k < -kF + 0.15))
assert abs(kF - np.pi / 2) < 1e-12
assert np.all(summand >= -1e-12)                                         # every term of (9.4) is positive
assert summand[~margin].max() < 1e-3                                     # zero away from the windows
inner = ((k > kF - q + 0.1) & (k < kF - 0.1)) | ((k > -kF - q + 0.1) & (k < -kF - 0.1))
assert summand[inner].min() > 0.9 and summand.max() < 1.1                # about 1/t inside, the scale of the axis
print('summand inside the windows from %.3f to %.3f, at most %.1e outside' % (summand[inner].min(), summand.max(),
                                                                              summand[~margin].max()))

ticks = [-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi]
ticklabels = [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$\pi/2$', r'$\pi$']
fig, axs = plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 6.0 * style.CM), gridspec_kw=dict(wspace=0.38))
for a in axs:
    for s in ('top', 'right'):
        a.spines[s].set_visible(False)
    a.spines['left'].set_linewidth(0.7); a.spines['bottom'].set_linewidth(0.7)
    a.tick_params(length=2.5, width=0.6)
    a.set_xlim(-np.pi, np.pi)
    a.set_xticks(ticks); a.set_xticklabels(ticklabels)
    a.set_xlabel(r'$k$', labelpad=1)
a0, a1 = axs
kp, sp = k[::5], summand[::5]                                           # a coarser grid for the drawing
a0.plot(kp, eps(kp), color=style.ACCENT, lw=1.4)
occ = eps(kp) < 0
a0.plot(kp[occ], eps(kp)[occ], color=style.ACCENT, lw=3.6)
style.guide(a0, y=0)
a0.set_ylim(-2.3, 2.6)
a0.set_yticks([-2, 0, 2]); a0.set_yticklabels([r'$-2$', r'$0$', r'$2$'])
a0.set_ylabel(r'$\varepsilon(k)$ in units of $t$', labelpad=2)
a0.plot([kF - q, kF], [-0.55, -0.55], color=style.BROKEN, lw=1.2)
a0.plot([kF - q, kF - q], [-0.7, -0.4], color=style.BROKEN, lw=1.2)
a0.plot([kF, kF], [-0.7, -0.4], color=style.BROKEN, lw=1.2)
style.label(a0, kF - q / 2, -0.95, r'$q$', color=style.BROKEN)
style.label(a0, 0, -0.85, r'occupied', color=style.ACCENT, fontsize=10)
style.label(a0, 2.15, 2.3, r'empty', color=style.MUTED, fontsize=10)
a1.plot(kp, sp, color=style.BROKEN, lw=1.4)
a1.fill_between(kp, 0, sp, color=style.BROKEN, alpha=0.15, lw=0)
a1.set_ylim(0, 1.45)
a1.set_yticks([0, 0.5, 1]); a1.set_yticklabels([r'$0$', r'$0.5$', r'$1$'])
a1.set_ylabel(r'summand in units of $1/t$', labelpad=2)
style.label(a1, kF - q / 2, 1.25, r'width $q$', color=style.BROKEN, fontsize=10)
style.label(a1, -kF - q / 2, 1.25, r'width $q$', color=style.BROKEN, fontsize=10)
style.save(fig, __file__)
