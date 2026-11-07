"""Session 8, the levels of the mean-field spinon hopping on an open 6x6 square lattice, chi_ij = 1 on every bond,
compared with the same hopping after a random gauge rotation (8.16), and with one plaquette of flux -1, a vison."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

L = 6
N = L * L
idx = lambda x, y: x + L * y
bonds = [(idx(x, y), idx(x + 1, y)) for x in range(L - 1) for y in range(L)] + \
        [(idx(x, y), idx(x, y + 1)) for x in range(L) for y in range(L - 1)]

def levels(chi):
    H = np.zeros((N, N), complex)
    for i, j in bonds:
        H[i, j] = chi.get((i, j), 1.0)
        H[j, i] = np.conj(H[i, j])
    return np.linalg.eigvalsh(H)

def flux(chi, x, y):
    """Product of the link phases around the plaquette with lower left corner (x, y), counterclockwise."""
    c = lambda i, j: chi.get((i, j), 1.0) if (i, j) in chi or (i, j) in bonds else np.conj(chi.get((j, i), 1.0))
    a, b, d, e = idx(x, y), idx(x + 1, y), idx(x + 1, y + 1), idx(x, y + 1)
    return c(a, b) * c(b, d) * c(d, e) * c(e, a)

E0 = levels({})
theta = np.random.default_rng(1).uniform(0, 2 * np.pi, N)
gauge = {(i, j): np.exp(1j * (theta[i] - theta[j])) for i, j in bonds}
vison = {(idx(x, 2), idx(x, 3)): -1.0 for x in range(3)}     # a string of three vertical links from the left edge
Eg, Ev = levels(gauge), levels(vison)
fl_g = np.array([[flux(gauge, x, y) for x in range(L - 1)] for y in range(L - 1)])
fl_v = np.array([[flux(vison, x, y) for x in range(L - 1)] for y in range(L - 1)])
assert np.allclose(fl_g, 1) and np.isclose(fl_v[2, 2], -1) and np.isclose(fl_v.real.sum(), 23)
assert np.abs(Eg - E0).max() < 1e-12 and np.abs(Ev - E0).max() > 0.3

n = np.arange(1, N + 1)
fig, ax = style.figure(height_cm=6.0, width_cm=12.0)
style.guide(ax, y=0)
ax.plot(n, Ev - E0, 'o', ms=4, color=style.BROKEN, zorder=3)
ax.plot(n, Eg - E0, 'o', ms=4.5, mfc='white', mec=style.ACCENT, mew=1.1, zorder=4)
ax.set_xlim(0, N + 1.5); ax.set_ylim(-0.5, 0.62)
style.arrows(ax, xlabel=r'$n$', ylabel=r'$E_n-E_n^{(0)}$')
ax.set_xticks([1, 18, 36]); ax.set_yticks([-0.3, 0, 0.3]); ax.set_yticklabels([r'$-0.3$', r'$0$', r'$0.3$'])
ax.tick_params(length=2.5, pad=2, labelsize=9.5)
ax.plot([2.0], [0.53], 'o', ms=4.5, mfc='white', mec=style.ACCENT, mew=1.1)
style.label(ax, 3.2, 0.53, 'after a gauge rotation', ha='left', fontsize=9.5, color=style.ACCENT)
ax.plot([20.0], [0.53], 'o', ms=4, color=style.BROKEN)
style.label(ax, 21.2, 0.53, 'one vison', ha='left', fontsize=9.5, color=style.BROKEN)
style.save(fig, __file__)
