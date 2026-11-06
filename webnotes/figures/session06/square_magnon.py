"""Session 6, the ferromagnetic magnon of the square lattice along the path Gamma, X, M, Gamma."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

z = 4
def E(kx, ky):
    return z * (1 - 0.5 * (np.cos(kx) + np.cos(ky)))       # in units of |J| S, from E = |J| S z (1 - gamma)
n = 100
seg = [((0, 0), (np.pi, 0)), ((np.pi, 0), (np.pi, np.pi)), ((np.pi, np.pi), (0, 0))]
xs, es = [], []
for i, (a, b) in enumerate(seg):
    s = np.linspace(0, 1, n, endpoint=False if i < 2 else True)
    kx = a[0] + (b[0] - a[0]) * s; ky = a[1] + (b[1] - a[1]) * s
    xs.append(i * n + s * n); es.append(E(kx, ky))
x = np.concatenate(xs); e = np.concatenate(es)
assert abs(E(0, 0)) < 1e-12 and abs(E(np.pi, 0) - 4) < 1e-12 and abs(E(np.pi, np.pi) - 8) < 1e-12
fig, ax = style.figure(height_cm=5.0, width_cm=10.5)
ax.plot(x, e, color=style.ACCENT)
for tk in (0, n, 2 * n, 3 * n):
    style.guide(ax, x=tk)
for val in (4, 8):
    style.guide(ax, y=val, color=style.MUTED, lw=0.8, ls=(0, (3, 2)))
    style.label(ax, 3 * n + 4, val, r'$%d|J|S$' % val, fontsize=8, ha='left')
style.arrows(ax, xlabel='', ylabel=r'$E$')
for tk, lab in zip((0, n, 2 * n, 3 * n), (r'$\Gamma$', r'$X$', r'$M$', r'$\Gamma$')):
    style.label(ax, tk, -0.75, lab, fontsize=8.5)
ax.plot([n, 2 * n], [4, 8], 'o', color=style.BROKEN, ms=3.5, zorder=5)
ax.plot([2 * n], [8], 'o', color=style.BROKEN, ms=3.5)
ax.set_xlim(0, 3 * n); ax.set_ylim(0, 9)
style.save(fig, __file__)
