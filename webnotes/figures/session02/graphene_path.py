"""Session 2, the bands of graphene from (2.19) along Gamma-K-M-Gamma, with the Dirac cone (2.21) around K.

Bond length a = 1 and t = 1, so v_F = 3 t a / 2 in units of hbar = 1. The bands are +-|f(k)| with
f(k) = t sum_j exp(i k . delta_j). The script checks that f(K) = 0 and that the slope at K is 3 t a / 2.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

FS = 10.5
t, a = 1.0, 1.0
delta = a * np.array([[np.cos(th), np.sin(th)] for th in (0, 2 * np.pi / 3, 4 * np.pi / 3)])
f = lambda k: t * np.exp(1j * k @ delta.T).sum(-1)
G = np.array([0.0, 0.0])
K = np.array([2 * np.pi / 3, 2 * np.pi / (3 * np.sqrt(3))]) / a
M = np.array([2 * np.pi / 3, 0.0]) / a
assert abs(f(K)) < 1e-12
vF = 3 * t * a / 2
q = 1e-4 * np.array([0.6, 0.8])
assert abs(abs(f(K + q)) / np.linalg.norm(q) - vF) < 1e-3

nodes = [G, K, M, G]
ks, x, xt = [], [], [0.0]
for P, Q in zip(nodes[:-1], nodes[1:]):
    s = np.linspace(0, 1, 300)
    seg = P + s[:, None] * (Q - P)
    x0 = xt[-1]
    ks.append(seg); x.append(x0 + s * np.linalg.norm(Q - P))
    xt.append(x0 + np.linalg.norm(Q - P))
ks, x = np.vstack(ks), np.concatenate(x)
E = np.abs(f(ks))
# the cone, only close to K
dK = np.linalg.norm(ks - K, axis=1)
near = dK < 0.75
xK = xt[1]

fig, ax = style.figure(height_cm=6.6, width_cm=12.5)
ax.plot(x, E, color=style.ACCENT); ax.plot(x, -E, color=style.ACCENT)
for side in (x < xK, x > xK):
    sel = near & side
    ax.plot(x[sel], vF * dK[sel], color=style.BROKEN, ls=(0, (4, 2)), lw=1.5)
    ax.plot(x[sel], -vF * dK[sel], color=style.BROKEN, ls=(0, (4, 2)), lw=1.5)
for xv in xt:
    style.guide(ax, x=xv)
style.guide(ax, y=0)
style.arrows(ax, ylabel=r'$E/t$', ticks=True)
ax.set_xticks(xt); ax.set_xticklabels([r'$\Gamma$', r'$K$', r'$M$', r'$\Gamma$'])
ax.set_yticks([-3, 0, 3]); ax.tick_params(labelsize=FS, length=2.5)
ax.spines['left'].set_visible(True)
ax.set_xlim(0, xt[-1]); ax.set_ylim(-3.4, 3.6)
style.label(ax, xK + 0.55, 1.75, r'$\pm\hbar v_F|\mathbf{q}|$', color=style.BROKEN, fontsize=FS, ha='left')
style.label(ax, 0.35, 2.15, r'$\pm|f(\mathbf{k})|$', color=style.ACCENT, fontsize=FS, ha='left')
style.save(fig, __file__)
