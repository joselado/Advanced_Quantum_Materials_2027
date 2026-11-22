"""Session 9, Eq. (9.3), the mixing coefficient of a state with every other state, computed for one matrix element.

Five levels of H_0, |n> at 0 and |m_1>..|m_4> at 0.35, 1.2, -0.8 and -2.0, in units of t, and the same matrix element
<m|V|n> = 0.1t for the four. The coefficient of |m> in (9.3) with lambda = 1 is <m|V|n>/(E_n - E_m). It is checked
against the exact eigenvector of H_0 + lambda V for a small lambda, as the sheet webnotes/conventions/session09.md says.
This is a formula on five levels, so it is numpy."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 11, 'axes.labelsize': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5})

En = 0.0
Em = np.array([0.35, 1.2, -0.8, -2.0])
V = 0.1                                  # the same matrix element for all, in units of t
LAMBDA = 1.0                             # the coupling constant of (9.2), set to one
assert V == 0.1 and LAMBDA == 1.0 and Em[0] == 0.35                     # the parameters of the caption
coef = LAMBDA * V / (En - Em)            # coefficient of |m> in Eq. (9.3)

# ---- the exact eigenvector of H_0 + lambda V for lambda = 1e-3, with the coefficient of |n> set to 1
H0 = np.diag(np.r_[En, Em])
Vm = np.zeros((5, 5)); Vm[0, 1:] = V; Vm[1:, 0] = V
lam = 1e-3
w, U = np.linalg.eigh(H0 + lam * Vm)
psi = U[:, np.argmin(np.abs(w - En))]
psi = psi / psi[0]
assert np.allclose(psi[1:] / lam, coef, rtol=1e-3), (psi[1:] / lam, coef)
assert np.allclose(coef, [-0.286, -0.083, 0.125, 0.05], atol=1e-3)       # the numbers on the bars
assert np.argmax(np.abs(coef)) == 0 and np.all((coef < 0) == (Em > En))   # |m_1> mixes most, the levels above are negative
print('coefficients', np.round(coef, 3), 'exact', np.round(psi[1:] / lam, 3))

fig, axs = plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 6.6 * style.CM), sharey=True,
                        gridspec_kw=dict(width_ratios=[0.8, 1.25], wspace=0.08))
a0, a1 = axs
for a in axs:
    for s in ('top', 'right'):
        a.spines[s].set_visible(False)
    a.spines['left'].set_linewidth(0.7); a.spines['bottom'].set_linewidth(0.7)
    a.tick_params(length=2.5, width=0.6)
a0.set_ylim(-2.4, 1.6)
a0.set_xlim(0, 1)
a0.set_xticks([])
a0.spines['bottom'].set_visible(False)
a0.set_yticks(np.r_[Em, En])
a0.set_yticklabels([r'$0.35$', r'$1.2$', r'$-0.8$', r'$-2$', r'$0$'])
a0.set_ylabel(r'$E^{(0)}$ in units of $t$')
for e in Em:
    a0.plot([0.1, 0.62], [e, e], color=style.LIGHT, lw=2.2)
a0.plot([0.1, 0.62], [En, En], color=style.ACCENT, lw=2.8)
style.label(a0, 0.7, En, r'$|n\rangle$', color=style.ACCENT, ha='left')
for i, e in enumerate(Em):
    style.label(a0, 0.7, e, r'$|m_%d\rangle$' % (i + 1), color=style.MUTED, ha='left')
a1.axvline(0, color=style.INK, lw=0.7)
for e, c in zip(Em, coef):
    a1.barh(e, c, height=0.17, color=style.BROKEN if c < 0 else style.ACCENT)
    style.label(a1, c + (0.015 if c > 0 else -0.015), e, r'$%.3f$' % c, ha='left' if c > 0 else 'right', fontsize=10.5)
a1.set_xlim(-0.40, 0.22)
a1.set_xticks([-0.3, -0.2, -0.1, 0, 0.1])
a1.set_xticklabels([r'$-0.3$', r'$-0.2$', r'$-0.1$', r'$0$', r'$0.1$'])
a1.spines['left'].set_visible(False)
a1.tick_params(axis='y', left=False)
a1.set_xlabel(r'coefficient of $|m\rangle$, with $\langle m|V|n\rangle=0.1t$')
style.save(fig, __file__)
