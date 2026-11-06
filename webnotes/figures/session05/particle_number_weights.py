"""Session 5, the probability of finding N electrons in the mean-field ground state of one site."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

# one site with spin, pairing term Delta (c_up^dag c_dn^dag + h.c.) and -mu n. N=1 is decoupled, so the problem is 2x2 in (|0>, |2>)
D = 0.5
def probs(mu):
    h = np.array([[0.0, D], [D, -2 * mu]])
    e, v = np.linalg.eigh(h)
    g = v[:, 0]
    return np.array([g[0]**2, 0.0, g[1]**2])      # P(N=0), P(N=1), P(N=2)

p0, p1 = probs(0.0), probs(0.5)
assert np.allclose(p0, [0.5, 0, 0.5]) and abs(p1.sum() - 1) < 1e-12
fig, ax = style.figure(height_cm=4.6, width_cm=8.5)
w = 0.34
x = np.arange(3)
ax.bar(x - w / 2, p0, w, color=style.ACCENT, label=r'$\mu=0$')
ax.bar(x + w / 2, p1, w, color=style.BROKEN, label=r'$\mu=0.5$')
style.arrows(ax, xlabel=r'$N$', ylabel=r'$P(N)$')
ax.set_xticks(x); ax.set_xticklabels(['0', '1', '2']); ax.tick_params(axis='x', length=2)
for xi in x:
    pass
ax.set_ylim(0, 0.95); ax.set_xlim(-0.6, 2.7)
ax.legend(loc='upper center', fontsize=8.5, ncol=2, bbox_to_anchor=(0.5, 1.08))
style.label(ax, 1, 0.07, 'no weight', fontsize=8, color=style.MUTED)
style.save(fig, __file__)
