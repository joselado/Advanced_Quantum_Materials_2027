"""Session 7, Section 7.11, the entropy of a block of l sites in the middle of an open chain of 3002 sites of free fermions
at half filling, critical (hopping 1) and dimerized (hoppings 1 and 0.6), from the pyqula script entropy_critical_chain.py.

Redrawn on 2026-11-22 under the same name, from pyqula instead of numpy, as the lecturer decided on 2026-11-21. The dashed
line is (1/3) log l + 0.73, the infinite chain, whose constant is computed here from its correlation matrix
C_ij = sin(pi (i-j)/2) / (pi (i-j)). Every number of the caption and of the feedback of the first quiz is asserted here."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

d = style.run_script('session07/entropy_critical_chain.py')
N = d['N']
ells = np.array(d['ells'], float)
Sc = np.array(d['S_critical'])
Sg = np.array(d['S_dimerized'])
print('l', ells, '\ncritical', np.round(Sc, 4), '\ndimerized', np.round(Sg, 4))

# the constant of the infinite chain, from its correlation matrix, the dashed line
L = 100
dd = np.arange(L)[:, None] - np.arange(L)[None, :]
with np.errstate(all='ignore'):
    C = np.where(dd == 0, 0.5, np.sin(np.pi * dd / 2) / (np.pi * dd))
nu = np.linalg.eigvalsh(C)
nu = nu[(nu > 1e-13) & (nu < 1 - 1e-13)]
const = -np.sum(nu * np.log(nu) + (1 - nu) * np.log(1 - nu)) - np.log(L) / 3
line = np.log(ells) / 3 + const
print('const', const, 'points minus line', np.round(Sc - line, 4))

# the numbers of the caption and of the quiz
assert N == 3002 and list(ells) == [10, 32, 100, 316, 1000]
assert abs(const - 0.73) < 0.005                               # the dashed line 1/3 log l + 0.73
assert abs(Sc[0] - 1.49) < 0.005                               # 1.49 at l=10
assert abs(Sc[-1] - 2.96) < 0.005                              # 2.96 at l=1000
assert np.all(np.abs(Sc[:-1] - line[:-1]) < 0.01)              # on the line up to l=316
assert -0.08 < Sc[-1] - line[-1] < -0.04                       # a little below it at l=1000
assert abs(N / ells[-1] - 3) < 0.01                            # the chain is three times longer than the largest block
assert abs((Sc[-1] - Sc[0]) - 1.5) < 0.05                      # the growth of about 1.5 in the feedback of the first quiz
slope = np.polyfit(np.log(ells[:-1]), Sc[:-1], 1)[0]
assert abs(slope - 1 / 3) < 0.01, slope                        # c=1
assert np.all(np.abs(Sg - 0.5) < 0.005)                        # the dimerized chain stays at about 0.5
assert all(s % 2 == 0 for s in d['starts']) and all(l % 2 == 0 for l in ells)   # whole cells, both ends on a bond 0.6

# second route for the dimerized chain: numpy on a ring of 600 sites with the hopping 1 on the bonds (2n, 2n+1) and 0.6 on
# the others, a block of 40 sites from an even site, so both ends cut a bond 0.6, as the conventions sheet says
t1, t2 = 1.0, 0.6
Nr = 600
Hr = np.zeros((Nr, Nr))
for i in range(Nr):
    Hr[i, (i + 1) % Nr] = Hr[(i + 1) % Nr, i] = -(t1 if i % 2 == 0 else t2)
w, v = np.linalg.eigh(Hr)
Cr = v[:, :Nr // 2] @ v[:, :Nr // 2].T
nu = np.linalg.eigvalsh(Cr[100:140, 100:140])
nu = nu[(nu > 1e-13) & (nu < 1 - 1e-13)]
Sring = -np.sum(nu * np.log(nu) + (1 - nu) * np.log(1 - nu))
print('numpy ring, block of 40 sites', Sring)
assert np.all(np.abs(Sg[1:] - Sring) < 1e-4)                    # pyqula bichain with h.inter*0.6 is this chain

fig, ax = style.figure(height_cm=5.6)
lfine = np.logspace(np.log10(5), np.log10(2000), 50)
ax.semilogx(lfine, np.log(lfine) / 3 + const, color=style.MUTED, lw=1.0, ls=(0, (3, 3)), zorder=0)
ax.semilogx(ells, Sc, color=style.ACCENT, marker='o', ms=3.4, lw=1.4)
ax.semilogx(ells, Sg, color=style.BROKEN, marker='o', ms=3.4, lw=1.4)
ax.set_xlim(5, 2000); ax.set_ylim(0, 3.4)
style.label(ax, 12, 2.45, r'critical chain', color=style.ACCENT, fontsize=9, ha='left')
style.label(ax, 400, 3.2, r'$\frac{1}{3}\log\ell+0.73$', color=style.MUTED, fontsize=9, ha='right')
style.label(ax, 20, 0.78, r'dimerized chain', color=style.BROKEN, fontsize=9, ha='left')
ax.set_xticks([10, 100, 1000]); ax.set_xticklabels([r'$10$', r'$10^2$', r'$10^3$']); ax.minorticks_off()
ax.set_yticks([0, 0.5, 1.49, 2.96]); ax.set_yticklabels([r'$0$', r'$0.5$', r'$1.49$', r'$2.96$'])
ax.tick_params(length=2.5, pad=2)
style.arrows(ax, xlabel=r'$\ell$', ylabel=r'$S$', ticks=True)
style.save(fig, __file__)
