"""Session 4, section 4.17, the dimple of a quasihole at the origin of the Laughlin state with m = 3 and N = 20 electrons.

The density comes from the Metropolis sampling of _g4_laughlin_mc.py, with and without the factor prod_i z_i of (4.14) for
w = 0, in four runs of different seeds (1 to 4 without the quasihole, 51 to 54 with it). Panel (a) is 2 pi l_B^2 times
the density, the mean of the four runs. Panel (b) is the number of electrons that the quasihole removes from the disc of
radius R around the origin, Delta N(R) = N(R) without minus N(R) with the quasihole, one curve per pair of runs. The numbers
of the caption are asserted below. numpy, since pyqula has no many-body state of the continuum. The four pairs take about
40 s."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import style
import _g4_laughlin_mc as mc
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

N, M, SEEDS = 20, 3, (1, 2, 3, 4)
R = mc.RADII
runs = []
for s in SEEDS:
    rc, f0, n0 = mc.metropolis(N, M, [], s)
    _, f1, n1 = mc.metropolis(N, M, [0j], s + 50)
    runs.append((f0, f1, n0 - n1, n0, n1))
f0 = np.mean([u[0] for u in runs], 0)
f1 = np.mean([u[1] for u in runs], 0)

win = (R >= 5) & (R <= 8)
far = np.array([u[2][win].mean() for u in runs])
near = np.array([u[2][R <= 4].max() for u in runs])
at = np.array([R[R <= 4][np.argmax(u[2][R <= 4])] for u in runs])
edge = np.array([u[2][(R >= 8.5) & (R <= 10)].max() for u in runs])
edge_at = np.array([R[(R >= 8.5) & (R <= 10)][np.argmax(u[2][(R >= 8.5) & (R <= 10)])] for u in runs])
# where the density drops below half of 1/3, beyond 8 l_B, without and with the quasihole
out0 = np.array([rc[(rc > 8) & (u[0] < 1 / 6)][0] for u in runs])
out1 = np.array([rc[(rc > 8) & (u[1] < 1 / 6)][0] for u in runs])
# the electrons beyond 8 l_B without the quasihole, against a uniform 1/3 out to the last orbital 3(N-1), sqrt(2*58) l_B
beyond = np.array([N - u[3][R == 8][0] for u in runs])
sel = (rc > 4) & (rc < 7)
print('removed for 5 <= R <= 8, mean of each run', np.round(far, 3))
print('largest removed inside R = 4', np.round(near, 3), 'at R =', at, ', near the edge', np.round(edge, 3), 'at R =', edge_at)
print('density drops below 1/6 at', out0, 'without and', out1, 'with the quasihole')
print('electrons beyond 8 l_B', np.round(beyond, 3), 'against', round((3 * (N - 1) + 1 - 32) / 3, 3), 'for a uniform 1/3')
print('mean of four with the quasihole for 4 < r < 7', round(f1[sel].mean(), 4), 'without', round(f0[sel].mean(), 4))
for u in runs:
    assert abs(u[0][rc < 5].mean() - 1 / 3) < 0.01                  # the Laughlin state is flat at 1/3
    assert u[3][-1] > 19.99 and u[4][-1] > 19.99                    # the disc of radius 13 holds the 20 electrons
    assert abs(u[2][-1]) < 0.005                                    # so nothing is removed from it
assert round(far.min(), 2) == 0.32 and round(far.max(), 2) == 0.34    # "0.32 to 0.34" of the caption
assert np.all((near > 0.40) & (near < 0.43)) and np.all((at >= 2.5) & (at <= 3.0))   # "about 0.4 at about 3 l_B"
assert np.all((edge > 0.39) & (edge < 0.45)) and np.all((edge_at >= 8.75) & (edge_at <= 9.5))   # "rises again to about 0.4 near R = 9"
assert np.all(out1 > out0)                                          # the quasihole pushes the edge of the droplet outward
assert np.all(beyond > (3 * (N - 1) + 1 - 32) / 3 + 0.5)            # page 16, the solution: the extra charge of 20/58 is at the edge
assert all(u[0][rc > 8].max() > 1.25 / 3 for u in runs)              # where the density has a bump above 1/3
assert f1[0] < 0.01                                                 # the density vanishes at the quasihole
assert abs(f1[sel].mean() - 1 / 3) < 0.01 and np.abs(f1 - f0)[sel].mean() < 0.005   # "a few l_B away it is back at 1/3"
assert abs(np.sqrt(6 * N) - 11) < 0.05                              # the edge of the droplet, sqrt(6N) = 11 l_B

fig, (ax, bx) = style.figure(height_cm=9.4, width_cm=12, nrows=2)
fig.subplots_adjust(hspace=0.55)
ax.plot(rc, f0, color=style.MUTED, lw=1.4)
ax.plot(rc, f1, color=style.ACCENT)
style.guide(ax, y=1 / 3, ls=':')
ax.set_xlim(0, 13); ax.set_ylim(0, 0.6)
style.arrows(ax, xlabel=r'$r/\ell_B$', ylabel=r'$2\pi\ell_B^2\,\rho(r)$')
style.label(ax, 3.4, 0.5, 'no quasihole', color=style.MUTED, fontsize=11)
style.label(ax, 2.6, 0.12, 'quasihole at $r=0$', color=style.ACCENT, fontsize=11, ha='left')
ax.text(0.98, 1.02, '(a)', transform=ax.transAxes, fontsize=11, ha='right')

bx.axvspan(5, 8, color=style.GRID, alpha=0.45, lw=0, zorder=0)
for u in runs:
    bx.plot(R, u[2], color=style.ACCENT, lw=0.9)
style.guide(bx, y=1 / 3, ls=':')
bx.set_xlim(0, 13); bx.set_ylim(0, 0.5)
style.arrows(bx, xlabel=r'$R/\ell_B$', ylabel=r'$\Delta N(R)$, electrons removed inside $R$')
bx.text(0.98, 1.02, '(b)', transform=bx.transAxes, fontsize=11, ha='right')

for a in (ax, bx):
    a.set_yticks([0, 1 / 3]); a.set_yticklabels(['0', r'$1/3$'], fontsize=11)
    a.tick_params(length=2.5, width=0.6, pad=2)
ax.set_xticks([0, 5, 10]); ax.set_xticklabels(['0', '5', '10'], fontsize=11)
bx.set_xticks([0, 3, 5, 8, 11]); bx.set_xticklabels(['0', '3', '5', '8', '11'], fontsize=11)
style.save(fig, __file__)
