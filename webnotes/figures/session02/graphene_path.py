"""Session 2, Section 2.11a, the bands of graphene from (2.19) along Gamma-K-M-Gamma, with the Dirac cone (2.21) at K.

The bands are computed by the pyqula script webnotes/scripts/session02/g4_graphene_bands.py, which the student
downloads under the figure: the honeycomb lattice with the bond length a = 1 and the default first-neighbor hopping +1,
the +t of (2.19). The path is given in reduced momenta, K = (2/3, -1/3) and M = (1/2, -1/2), which are the corner
K = (2 pi/3, 2 pi/3 sqrt3) and the point M = (2 pi/3, 0) of the notes in the frame of pyqula, with one bond along x.
The red dashed lines are the cone +-hbar v_F |q| with hbar v_F = 3ta/2 of (2.20). The asserts check the energies at
Gamma, K and M, the range of the bands and the slope at K, so that the caption can state them."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

d = style.run_script('session02/g4_graphene_bands.py')
g, bands, steps = d['g'], d['bands'], d['steps']
A = np.array([g.a1[:2], g.a2[:2]])
B = 2 * np.pi * np.linalg.inv(A).T                               # reciprocal vectors as rows, a_i . b_j = 2 pi delta_ij
kc = np.array([np.asarray(k)[:2] @ B for k in d['kpath']])       # Cartesian momentum of each step, in units of 1/a
K, M = d['K'][:2] @ B, d['M'][:2] @ B
assert np.allclose(K, [2 * np.pi / 3, 2 * np.pi / (3 * np.sqrt(3))]) and np.allclose(M, [2 * np.pi / 3, 0.])
iK, iM = steps[0], steps[0] + steps[1]
assert np.allclose(kc[iK], K) and np.allclose(kc[iM], M) and len(kc) == len(bands) == sum(steps) + 1
assert np.allclose(bands[0], [-3, 3]) and np.allclose(bands[-1], [-3, 3])          # |f| = 3t at Gamma
assert np.abs(bands[iK]).max() < 1e-9                                               # f(K) = 0, the bands touch
assert np.allclose(bands[iM], [-1, 1])                                              # |f| = t at M
assert abs(bands.min() + 3) < 1e-9 and abs(bands.max() - 3) < 1e-9                  # the bands span -3t to 3t
vF = 1.5                                                                            # 3 t a / 2 hbar for t = a = 1
dK = np.linalg.norm(kc - K, axis=1)
near = (dK > 0) & (dK < 0.03)                     # the two steps next to K, one on each side, 0.02 away from it
assert near.sum() == 2 and abs(np.mean(bands[near, 1] / dK[near]) - vF) < 1e-3      # the slope of the cone at K
hk = g.get_hamiltonian(has_spin=False).get_hk_gen()                                 # the same Hamiltonian, no file written
for th in np.linspace(0, 2 * np.pi, 7)[:-1]:                                        # the slope 3/2 in every direction
    q = 1e-5 * np.array([np.cos(th), np.sin(th)])
    kr = A @ (K + q) / (2 * np.pi)
    assert abs(np.linalg.eigvalsh(hk([kr[0], kr[1], 0.]))[1] / 1e-5 - vF) < 1e-4
x = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(kc, axis=0), axis=1))])   # distance along the path
xt = [x[0], x[iK], x[iM], x[-1]]

fig, ax = style.figure(height_cm=6.6, width_cm=12.5)
ax.plot(x, bands[:, 1], color=style.ACCENT); ax.plot(x, bands[:, 0], color=style.ACCENT)
cone = dK < 0.75
for side in (x < x[iK] + 1e-9, x > x[iK] - 1e-9):
    sel = cone & side
    ax.plot(x[sel], vF * dK[sel], color=style.BROKEN, ls=(0, (4, 2)), lw=1.5)
    ax.plot(x[sel], -vF * dK[sel], color=style.BROKEN, ls=(0, (4, 2)), lw=1.5)
for xv in xt:
    style.guide(ax, x=xv)
style.guide(ax, y=0)
style.arrows(ax, xlabel=r'$\mathbf{k}$', ylabel=r'$E$ in units of $t$', ticks=True)
ax.set_xticks(xt); ax.set_xticklabels([r'$\Gamma$', r'$K$', r'$M$', r'$\Gamma$'])
ax.set_yticks([-3, -1, 0, 1, 3]); ax.set_yticklabels([r'$-3$', r'$-1$', '0', '1', '3'])
ax.tick_params(labelsize=10.5, length=2.5)
ax.spines['left'].set_visible(True)
ax.set_xlim(0, xt[-1]); ax.set_ylim(-3.4, 3.6)
style.label(ax, x[iK] + 0.55, 1.75, r'$\pm\hbar v_F|\mathbf{q}|$', color=style.BROKEN, fontsize=10.5, ha='left')
style.label(ax, 0.35, 2.15, r'$\pm|f(\mathbf{k})|$', color=style.ACCENT, fontsize=10.5, ha='left')
style.save(fig, __file__)
