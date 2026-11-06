"""Session 4, section 4.10, the Landau levels at one fixed field, for Schrodinger and for Dirac electrons.

Panel (a) is E_n = hbar omega_c (n+1/2) of (4.6), in units of hbar omega_c. Panel (b) is E_n = sgn(n) sqrt(|n|) E_1 of (4.7), with
E_1 = sqrt(2) hbar v_F / l_B. Each Dirac level is drawn in two colors, the weight of the upper and of the lower
component of the spinor. They are found below by diagonalizing H = [[0, a^dagger], [a, 0]] in a basis of 60 oscillator
states, where the level n=0 has only the upper component."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

M = 60
a = np.diag(np.sqrt(np.arange(1, M)), 1)            # lowering operator
H = np.block([[np.zeros((M, M)), a.T], [a, np.zeros((M, M))]])
w, v = np.linalg.eigh(H)
nz = 4
levels = {}
for n in range(-nz, nz + 1):
    target = np.sign(n) * np.sqrt(abs(n))
    i = np.argmin(np.abs(w - target))
    assert abs(w[i] - target) < 1e-8, (n, w[i])
    up = (np.abs(v[:M, i]) ** 2).sum()
    levels[n] = (w[i], up)
print({n: round(levels[n][1], 3) for n in levels})
assert abs(levels[0][1] - 1) < 1e-9
assert all(abs(levels[n][1] - 0.5) < 1e-9 for n in levels if n)

fig, axs = style.figure(ncols=2, height_cm=6.8, gridspec_kw=dict(wspace=0.35, width_ratios=[1, 1.35]))
ax = axs[0]
ax.set_xlim(0, 1)
ax.set_ylim(0, 5.9)
for n in range(0, 5):
    ax.hlines(n + 0.5, 0.25, 0.95, color=style.ACCENT, lw=2.0)
    style.label(ax, 0.12, n + 0.5, r'$%d$' % n, fontsize=8.5, color=style.MUTED)
ax.annotate('', xy=(1.07, 1.5), xytext=(1.07, 0.5), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.7, shrinkA=0, shrinkB=0), annotation_clip=False)
ax.annotate('', xy=(1.07, 4.5), xytext=(1.07, 3.5), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.7, shrinkA=0, shrinkB=0), annotation_clip=False)
style.label(ax, 1.12, 1.0, r'$\hbar\omega_c$', fontsize=8.5, ha='left')
style.label(ax, 1.12, 4.0, r'$\hbar\omega_c$', fontsize=8.5, ha='left')
style.arrows(ax, ylabel=r'$E$')
ax.text(0.5, -0.06, '(a) parabolic electrons', transform=ax.transAxes, ha='center', va='top', fontsize=8.5)
ax = axs[1]
ax.set_xlim(0, 1); ax.set_ylim(-2.95, 2.3)
for n, (e, up) in levels.items():
    ax.hlines(e, 0.25, 0.25 + 0.7 * up, color=style.ACCENT, lw=2.0)
    ax.hlines(e, 0.25 + 0.7 * up, 0.95, color=style.WARM, lw=2.0)
    style.label(ax, 0.12, e, r'$%d$' % n, fontsize=7.5, color=style.MUTED)
style.label(ax, 1.0, levels[1][0], r'$E_1$', fontsize=8.5, ha='left')
style.label(ax, 1.0, levels[4][0], r'$E_4=2E_1$', fontsize=8.5, ha='left')
style.arrows(ax, ylabel=r'$E$')
ax.text(0.5, -0.06, '(b) Dirac electrons', transform=ax.transAxes, ha='center', va='top', fontsize=8.5)
style.label(ax, 0.6, 0.3, '$n=0$, upper only', color=style.ACCENT, fontsize=7.5)
ax.hlines(-2.65, 0.25, 0.45, color=style.ACCENT, lw=2.0); style.label(ax, 0.5, -2.65, 'upper', fontsize=7.5, ha='left')
ax.hlines(-2.65, 0.68, 0.88, color=style.WARM, lw=2.0); style.label(ax, 0.93, -2.65, 'lower', fontsize=7.5, ha='left')
style.save(fig, __file__)
