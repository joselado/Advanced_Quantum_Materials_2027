"""Session 5, section 5.6, the probability of finding N electrons in the mean-field ground state of one site.

One site with spin has H = -mu (n_up + n_dn) + Delta (c_up^dag c_dn^dag + c_dn c_up), which is (5.4) with t=0 and without its
constant. The states with N=1 are not touched by the pairing term and have the energy -mu, so the problem is 2x2 in |0> and
|2> = c_up^dag c_dn^dag |0>, and its lower level is always below -mu. This is numpy, since the probabilities of N need the
many-body ground state, which the BdG bands of pyqula do not give directly. The bars are for Delta=0.5 at mu=0 and mu=0.5."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

D = 0.5


def ground(mu):
    """Energy and P(N=0), P(N=1), P(N=2) of the ground state of the four states of one site."""
    h = np.array([[0.0, D], [D, -2 * mu]])
    e, v = np.linalg.eigh(h)
    assert e[0] < -mu                                    # the even state is below the odd states
    g = v[:, 0]
    return e[0], np.array([g[0]**2, 0.0, g[1]**2])


e0, p0 = ground(0.0)
e1, p1 = ground(0.5)
assert abs(e0 + 0.5) < 1e-12 and np.allclose(p0, [0.5, 0, 0.5])
assert abs(e1 + 1.2071) < 1e-4 and np.allclose(p1, [0.1464, 0, 0.8536], atol=1e-4)
assert np.isclose(p1[2], 0.5 * (1 + 0.5 / np.hypot(0.5, D)))
print('mu=0: E', round(e0, 4), 'P', np.round(p0, 4), ' mu=0.5: E', round(e1, 4), 'P', np.round(p1, 4))

fig, ax = plt.subplots(figsize=(7.6 * style.CM, 5.0 * style.CM))
w = 0.34
x = np.arange(3)
ax.bar(x - w / 2, p0, w, color=style.ACCENT, label=r'$\mu=0$')
ax.bar(x + w / 2, p1, w, color=style.BROKEN, label=r'$\mu=0.5$')
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
ax.set_xticks(x); ax.set_xticklabels(['0', '1', '2'], fontsize=11)
ax.set_yticks([0, p1[0], 0.5, p1[2], 1]); ax.set_yticklabels(['0', '0.15', '0.5', '0.85', '1'], fontsize=10.5)
ax.tick_params(length=2.5, width=0.6, pad=2)
for y in (p1[0], 0.5, p1[2]):
    style.guide(ax, y=y, lw=0.7)
ax.set_ylim(0, 1.0); ax.set_xlim(-0.6, 2.6)
ax.set_xlabel(r'number of electrons $N$', fontsize=11, labelpad=1); ax.set_ylabel(r'$P(N)$', fontsize=11, labelpad=2)
ax.legend(loc='upper left', fontsize=10.5, ncol=1, handlelength=1.2, borderaxespad=0.2)
style.save(fig, __file__)
