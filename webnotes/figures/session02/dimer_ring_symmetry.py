"""Session 2, eigenvalues of a symmetry operator on a dimer and on a ring of four sites."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

# the checks of the numbers that the figure prints
t = 1.0
H = t * np.array([[0, 1], [1, 0]]); M = np.array([[0, 1], [1, 0]])
e, v = np.linalg.eigh(H)
for ev, vec in zip(e, v.T):
    lam = vec @ M @ vec
    assert (abs(ev - t) < 1e-9 and abs(lam - 1) < 1e-9) or (abs(ev + t) < 1e-9 and abs(lam + 1) < 1e-9)
R = np.roll(np.eye(4), 1, axis=0)          # (R psi)_n = psi_{n-1}, a rotation by 90 degrees
s1 = np.array([1, -1, 1, -1], complex); s2 = np.array([1, -1j, -1, 1j])
assert np.allclose(R @ s1, -s1) and np.allclose(R @ s2, 1j * s2)

fig, axs = plt.subplots(1, 3, figsize=(style.WIDTH_CM * style.CM, 5.0 * style.CM), gridspec_kw=dict(width_ratios=[1.1, 1, 1]))
for ax in axs:
    ax.axis('off')
# (a) the two levels of the dimer, with the eigenvalue of the mirror
ax = axs[0]
for y, lab, s, lam in [(1.0, r'$c_1^\dagger+c_2^\dagger$', ('+', '+'), '+1'), (-1.0, r'$c_1^\dagger-c_2^\dagger$', ('+', '$-$'), '$-1$')]:
    ax.plot([-1, 1], [y, y], color=style.ACCENT, lw=1.8)
    for j in range(2):
        ax.scatter([-0.3 + 0.6 * j], [y + 0.5], s=90, facecolor=style.LIGHT, edgecolor=style.ACCENT, linewidths=1.0, zorder=3)
        style.label(ax, -0.3 + 0.6 * j, y + 0.49, s[j], color='white', fontsize=7.5, zorder=4)
    style.label(ax, 0, y + 1.0, lab, fontsize=8)
    style.label(ax, 1.15, y, r'mirror $%s$' % lam.replace('$', ''), color=style.BROKEN, ha='left', fontsize=8)
style.label(ax, -1.15, 1.0, r'$+t$', ha='right', fontsize=8.5)
style.label(ax, -1.15, -1.0, r'$-t$', ha='right', fontsize=8.5)
ax.set_xlim(-1.7, 3.0); ax.set_ylim(-2.4, 2.9)
style.label(ax, -1.7, 2.8, '(a)', ha='left', fontsize=9)
# (b), (c) a ring of four sites, the arrow on a site is the complex amplitude
ang = np.pi / 2 * np.arange(4)
pos = np.c_[np.cos(ang), np.sin(ang)]
for ax, psi, name, tag in [(axs[1], s1, r'$R=-1$', '(b)'), (axs[2], s2, r'$R=i$', '(c)')]:
    ax.set_aspect('equal')
    ring = np.r_[pos, pos[:1]]
    ax.plot(ring[:, 0], ring[:, 1], color=style.GRID, lw=2.0, zorder=1)
    for p, a in zip(pos, psi):
        ax.scatter(*p, s=60, color=style.INK, zorder=3)
        d = 0.55 * np.array([a.real, a.imag])
        ax.annotate('', xy=p + d, xytext=p, arrowprops=dict(arrowstyle='-|>', color=style.ACCENT, lw=1.6, mutation_scale=8, shrinkA=0, shrinkB=0), zorder=4)
    style.label(ax, 0, -1.95, name, color=style.BROKEN, fontsize=9)
    ax.set_xlim(-1.9, 1.9); ax.set_ylim(-2.3, 1.9)
    style.label(ax, -1.9, 1.8, tag, ha='left', fontsize=9)
fig.subplots_adjust(wspace=0.05, left=0.0, right=1.0)
style.save(fig, __file__)
