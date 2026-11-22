"""Session 9, Section 9.10b, a sketch of the mobility edges of the three-dimensional Anderson model, w_n uniform in [-W,W].

The grey lines are the band edges +-(6t + W): the clean cubic lattice has its band in [-6t, 6t], and the random onsite
energy adds at most W in each direction. The asserts below check that every level of cubes of 8^3 sites lies inside
them, for W = 2t, 6t and 12t. The blue curve is a guide for the eye. Its end point is a number of numerical work on
the 3D Anderson model, W_c = 16.5t for the full width 2W of the box, so W_c = 8.25t, which the caption gives as about
8t. That number is not computed here. Its height at W = 5t is about 8t, above E = 7t, since the level statistics of
cubes of 10^3 and 12^3 sites at W = 5t are those of extended states up to E = 7t, which
webnotes/checks/session09/g6_10b_random_disorder.py asserts. The window from 7t to 8t gives 0.51 to 0.53, close to the
edge, and it is not asserted. The first guide, 6 sqrt(1 - (W/W_c)^2), stood at 4.7t there and put these extended states
outside the curve.
The axes have ticks at W = 0, 4, 8, 12 and E = +-6, +-12, +-18, and the window holds the band edges up to W = 12t."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

# every level of a disordered cube lies inside +-(6t + W)
L = 8
idx = np.arange(L ** 3).reshape(L, L, L)
H0 = np.zeros((L ** 3, L ** 3))
for axis in range(3):
    j = np.roll(idx, -1, axis=axis).ravel()
    H0[idx.ravel(), j] = H0[j, idx.ravel()] = -1.0
assert np.allclose(np.linalg.eigvalsh(H0)[[0, -1]], [-6, 6])          # the clean band, from -6t to 6t
rng = np.random.default_rng(3)
for Wt in (2.0, 6.0, 12.0):
    e = np.linalg.eigvalsh(H0 + np.diag(Wt * (2 * rng.random(L ** 3) - 1)))
    assert np.all(np.abs(e) < 6 + Wt), (Wt, e[0], e[-1])

Wc = 8.25      # 16.5 t for a box of full width 16.5 t, i.e. w_n in [-W,W] with W = 8.25 t (numerical result, band center)
W = np.linspace(0, Wc, 200)
Ec = (6 + 0.8 * W) * np.sqrt(1 - (W / Wc) ** 2)      # a guide for the eye, with its end point W_c and its height at 5t
Wl = np.linspace(0, 12, 200)
edge = 6 + Wl
assert abs(Ec[0] - 6) < 1e-12 and abs(Ec[-1]) < 1e-12                # the clean band edge at W = 0, and zero at W_c
assert np.all(Ec[1:] < 6 + W[1:])                                    # inside the band edges at every W
E5 = (6 + 0.8 * 5) * np.sqrt(1 - (5 / Wc) ** 2)
assert 7.8 < E5 < 8.1, E5                                             # about 8t at W = 5t, above the 7t of the caption

fig, ax = style.figure(height_cm=6.4, width_cm=10.5)
ax.fill_between(Wl, -edge, edge, color=style.WARM, alpha=0.18, lw=0, zorder=0)
ax.fill_between(W, -Ec, Ec, color=style.LIGHT, alpha=0.45, lw=0)
ax.plot(Wl, edge, color=style.MUTED, lw=1.0); ax.plot(Wl, -edge, color=style.MUTED, lw=1.0)
ax.plot(W, Ec, color=style.ACCENT); ax.plot(W, -Ec, color=style.ACCENT)
ax.set_xlim(0, 12.6); ax.set_ylim(-19.5, 19.5)
style.arrows(ax, xlabel=r'$W/t$', ylabel=r'$E/t$', ticks=True)
ax.set_xticks([0, 4, 8, 12]); ax.set_xticklabels(['0', '4', '8', '12'])
ax.set_yticks([-18, -12, -6, 0, 6, 12, 18]); ax.set_yticklabels(['$-18$', '$-12$', '$-6$', '0', '6', '12', '18'])
ax.tick_params(length=2.5, pad=2)
style.guide(ax, y=0)
style.label(ax, 2.6, 0, 'extended', color=style.ACCENT, fontsize=8.5)
style.label(ax, 7.6, 10.5, 'localized', color=style.BROKEN, fontsize=8.5)
style.label(ax, 6.3, 8.8, r'$E_c$', color=style.ACCENT, fontsize=8.5)
style.label(ax, 3.2, 12.6, r'$6t+W$', color=style.MUTED, fontsize=8.5)
style.label(ax, 9.7, -2.4, r'$W_c\approx8t$', color=style.INK, fontsize=8.5)
ax.plot([Wc], [0], 'o', color=style.ACCENT, ms=4)
ax.plot([10.5], [0], 'o', color=style.BROKEN, ms=4)
style.label(ax, 11.3, 1.6, r'$E_F$', color=style.BROKEN, fontsize=8.5)
style.save(fig, __file__)
