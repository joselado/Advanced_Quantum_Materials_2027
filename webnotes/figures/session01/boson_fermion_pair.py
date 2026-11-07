"""Session 1, two particles on the two sites of H = t (c0^+ c1 + h.c.), for fermions and for bosons.

The fermionic operators anticommute, so (c^+)^2 = 0 and two fermions have one state. The bosonic ones commute,
so two bosons have three states. Both spectra are computed by exact diagonalization in the Fock space.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

t = 1.0
FS = 10.5


def sector(ops, n_target):
    """Energies of the hopping t (a0^+ a1 + h.c.) with exactly n_target particles."""
    a0, a1 = ops
    H = t * (a0.T @ a1 + a1.T @ a0)
    N = a0.T @ a0 + a1.T @ a1
    idx = np.where(np.isclose(np.diag(N), n_target))[0]
    assert np.allclose(N, np.diag(np.diag(N)))
    return np.linalg.eigvalsh(H[np.ix_(idx, idx)])


# fermions, with the Jordan-Wigner sign, basis |n0 n1>, n = 0, 1
f, Z, I2 = np.array([[0., 1.], [0., 0.]]), np.diag([1., -1.]), np.eye(2)
c0, c1 = np.kron(f, I2), np.kron(Z, f)
assert np.allclose(c0 @ c0, 0) and np.allclose(c0 @ c1 + c1 @ c0, 0)
Ef = sector((c0, c1), 2)
# bosons, occupation 0, 1, 2 per site, which is enough for two particles
b = np.diag(np.sqrt([1., 2.]), 1)
I3 = np.eye(3)
b0, b1 = np.kron(b, I3), np.kron(I3, b)
assert np.allclose(b0 @ b1 - b1 @ b0, 0)
Eb = sector((b0, b1), 2)
assert np.allclose(Ef, [0.0])
assert np.allclose(Eb, [-2 * t, 0.0, 2 * t])

fig, ax = plt.subplots(figsize=(12.5 * style.CM, 7.8 * style.CM))
ax.axis('off')
cols = {'f': 0.0, 'b': 5.0}
style.label(ax, cols['f'], 3.05, 'two fermions', fontsize=FS + 0.5)
style.label(ax, cols['b'], 3.05, 'two bosons', fontsize=FS + 0.5)
for key, E, col in (('f', Ef, style.ACCENT), ('b', Eb, style.BROKEN)):
    x0 = cols[key]
    for e in E:
        ax.plot([x0 - 1.1, x0 + 1.1], [e, e], color=col, lw=2.2)
        style.label(ax, x0 + 1.3, e, {-2: r'$-2t$', 0: r'$0$', 2: r'$+2t$'}[int(round(e))], ha='left', fontsize=FS)
# the ways to place two particles on two sites, under each column
def config(x, y, n0, n1, col):
    for j, n in enumerate((n0, n1)):
        xc = x + (j - 0.5) * 0.62
        ax.plot([xc - 0.24, xc + 0.24], [y - 0.2, y - 0.2], color=style.INK, lw=1.0)
        for k in range(n):
            ax.scatter([xc], [y + 0.02 + 0.3 * k], s=46, color=col, zorder=3)


config(cols['f'], -3.6, 1, 1, style.ACCENT)
for i, occ in enumerate(((2, 0), (1, 1), (0, 2))):
    config(cols['b'] + (i - 1) * 1.55, -3.6, *occ, style.BROKEN)
style.label(ax, cols['f'], -4.35, 'one state', fontsize=FS)
style.label(ax, cols['f'], -5.0, r'since $(c_i^\dagger)^2=0$', fontsize=FS, color=style.ACCENT)
style.label(ax, cols['b'], -4.35, 'three states', fontsize=FS)
ax.set_xlim(-1.6, 7.0)
ax.set_ylim(-5.4, 3.4)
style.save(fig, __file__)
