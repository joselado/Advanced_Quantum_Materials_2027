"""Session 4, section 4.10, the Landau levels at one fixed field, for Schrodinger and for Dirac electrons.

Panel (a) is E_n = hbar omega_c (n+1/2) of (4.6), in units of hbar omega_c. Panel (b) is E_n = sgn(n) sqrt(|n|) E_1 of (4.7), with
E_1 = sqrt(2) hbar v_F / l_B, in units of E_1. Each Dirac level is a bar of length one, split into the weight of the upper
component of the spinor, from 0, and of the lower one. The weights are found below by diagonalizing H = [[0, a^dagger],
[a, 0]] in a basis of 60 oscillator states, where the level n=0 has only the upper component and every other level has
1/2 in each. The cut basis has a second zero mode, the top state of the lower component, which is left out. This is the charge +e with the field along +z of the pages, qB > 0, as the conventions sheet says. Redrawn
on 2026-11-21 under the same name, with the axes E/hbar omega_c, E/E_1 and the weight, and their ticks."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, readable on a phone

M = 60
assert M == 60                                      # the 60 oscillator states of the caption
a = np.diag(np.sqrt(np.arange(1, M)), 1)            # lowering operator
H = np.block([[np.zeros((M, M)), a.T], [a, np.zeros((M, M))]])
w, v = np.linalg.eigh(H)
# the zero space of the cut basis is twofold: the physical zero mode (|0>, 0) and the extra mode (0, |M-1>), since
# a^dagger of the cut basis kills its top state. eigh may mix the two, so the upper-component projector is
# diagonalized inside the zero space, and the mode with the upper weight 1 is the physical one (caption)
Z = v[:, np.abs(w) < 1e-8]
pw, pv = np.linalg.eigh(Z[:M].T @ Z[:M])
zero, extra = Z @ pv[:, -1], Z @ pv[:, 0]
assert Z.shape[1] == 2 and abs(pw[-1] - 1) < 1e-9 and abs(pw[0]) < 1e-9
assert abs(zero[0]) ** 2 > 1 - 1e-9 and abs(extra[2 * M - 1]) ** 2 > 1 - 1e-9     # |0> upper, |M-1> lower, the top
nz = 4
levels = {}
for n in range(-nz, nz + 1):
    target = np.sign(n) * np.sqrt(abs(n))
    if n == 0:
        levels[n] = (0.0, (np.abs(zero[:M]) ** 2).sum())
        continue
    i = np.argmin(np.abs(w - target))
    assert abs(w[i] - target) < 1e-8, (n, w[i])
    up = (np.abs(v[:M, i]) ** 2).sum()
    levels[n] = (w[i], up)
print({n: round(levels[n][1], 3) for n in levels})
assert len(levels) == 9                                               # the alt, nine Dirac levels in (b)
parabolic = [n + 0.5 for n in range(0, 5)]
assert len(parabolic) == 5 and np.allclose(np.diff(parabolic), 1)    # the alt, five equally spaced levels in (a)
assert abs(levels[0][1] - 1) < 1e-9                                   # the zero mode is fully in the upper component
assert all(abs(levels[n][1] - 0.5) < 1e-9 for n in levels if n)      # every other level has 1/2 in each
assert abs(levels[4][0] - 2 * levels[1][0]) < 1e-9                    # E_4 = 2 E_1

fig, axs = plt.subplots(1, 2, figsize=(11.5 * style.CM, 6.4 * style.CM),
                        gridspec_kw=dict(wspace=0.55, width_ratios=[0.8, 1.35]))
ax = axs[0]
ax.set_xlim(0, 1); ax.set_ylim(0, 5.2)
for n, e in enumerate(parabolic):
    ax.hlines(e, 0.1, 0.7, color=style.ACCENT, lw=2.0)
    style.label(ax, 0.78, e, r'$%d$' % n, fontsize=9.5, color=style.MUTED, ha='left')
ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5]); ax.set_yticklabels(['0.5', '1.5', '2.5', '3.5', '4.5'])
ax.set_xticks([])
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False); ax.spines['bottom'].set_visible(False)
ax.set_ylabel(r'$E/\hbar\omega_c$', labelpad=2)
ax.tick_params(length=2.5, width=0.6, labelsize=10)
ax = axs[1]
ax.set_xlim(0, 1.25); ax.set_ylim(-2.35, 2.35)
for n, (e, up) in levels.items():
    ax.hlines(e, 0, up, color=style.ACCENT, lw=2.0)
    if up < 1:
        ax.hlines(e, up, 1, color=style.WARM, lw=2.0)
    style.label(ax, 1.06, e, r'$%d$' % n, fontsize=9.5, color=style.MUTED, ha='left')
ax.set_yticks([-2, -1, 0, 1, 2]); ax.set_yticklabels(['$-2$', '$-1$', '0', '1', '2'])
ax.set_xticks([0, 0.5, 1]); ax.set_xticklabels(['0', '0.5', '1'])
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
ax.spines['bottom'].set_position(('data', -2.35))
ax.set_ylabel(r'$E/E_1$', labelpad=2)
ax.set_xlabel('weight of the upper component', fontsize=10, labelpad=2)
ax.xaxis.set_label_coords(0.42, -0.13)
ax.tick_params(length=2.5, width=0.6, labelsize=10)
for ax, name, xc in ((axs[0], '(a) parabolic', 0.45), (axs[1], '(b) Dirac', 0.42)):
    ax.text(xc, -0.25, name, transform=ax.transAxes, ha='center', va='top', fontsize=11)
style.save(fig, __file__)
