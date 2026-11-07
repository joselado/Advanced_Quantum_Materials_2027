"""Session 1, the Hubbard dimer at half filling, exact against mean field.

H = -t sum_s (c1s^+ c2s + h.c.) + U sum_i n_i,up n_i,dn with two electrons. The exact ground state energy
comes from diagonalizing the Fock space with two electrons (6 states), and it agrees with
U/2 - sqrt(U^2/4 + 4 t^2). The mean-field energy comes from the self-consistent loop with an
antiferromagnetic guess, n_i,up n_i,dn -> n_i,up <n_i,dn> + <n_i,up> n_i,dn - <n_i,up><n_i,dn>.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

t = 1.0
FS = 10.5

# exact, four spin-orbitals (1up, 1dn, 2up, 2dn) with the Jordan-Wigner signs
f, Z, I2 = np.array([[0., 1.], [0., 0.]]), np.diag([1., -1.]), np.eye(2)


def c(j):
    m = [Z] * j + [f] + [I2] * (3 - j)
    out = m[0]
    for x in m[1:]:
        out = np.kron(out, x)
    return out


c1u, c1d, c2u, c2d = (c(j) for j in range(4))
n = lambda a: a.T @ a
hop = -t * (c1u.T @ c2u + c2u.T @ c1u + c1d.T @ c2d + c2d.T @ c1d)
Nop = sum(n(a) for a in (c1u, c1d, c2u, c2d))
two = np.where(np.isclose(np.diag(Nop), 2))[0]


def exact(U):
    H = hop + U * (n(c1u) @ n(c1d) + n(c2u) @ n(c2d))
    return np.linalg.eigvalsh(H[np.ix_(two, two)])[0]


def meanfield(U, m0=0.9, iters=4000):
    """Unrestricted mean field with the guess <n_1up> = (1+m)/2, <n_1dn> = (1-m)/2 and the opposite on site 2."""
    m = m0
    for _ in range(iters):
        nu = np.array([(1 + m) / 2, (1 - m) / 2])            # <n_i,up> for i = 1, 2
        nd = 1 - nu                                           # <n_i,dn>
        Hu = np.array([[U * nd[0], -t], [-t, U * nd[1]]])     # the up electron feels the down density
        Hd = np.array([[U * nu[0], -t], [-t, U * nu[1]]])
        eu, vu = np.linalg.eigh(Hu); ed, vd = np.linalg.eigh(Hd)
        new_nu = vu[:, 0] ** 2                                # one up and one down electron, lowest level each
        m_new = new_nu[0] - new_nu[1]
        if abs(m_new - m) < 1e-12:
            break
        m = 0.5 * m + 0.5 * m_new
    E = eu[0] + ed[0] - U * np.sum(nu * nd)
    return E, abs(m)


Us = np.linspace(0, 8, 161)
Eex = np.array([exact(U) for U in Us])
assert np.allclose(Eex, Us / 2 - np.sqrt(Us ** 2 / 4 + 4 * t ** 2))
mf = np.array([meanfield(U) for U in Us])
Emf, mmf = mf[:, 0], mf[:, 1]
assert np.all(Emf >= Eex - 1e-9)                              # mean field is variational
assert np.all(mmf[Us < 1.95] < 1e-4) and np.all(mmf[Us > 2.1] > 0.05)   # the moment appears at U = 2t
assert np.allclose(Emf[Us < 1.95], -2 * t + Us[Us < 1.95] / 2)

fig = plt.figure(figsize=(12.5 * style.CM, 5.8 * style.CM))
gs = fig.add_gridspec(1, 2, wspace=0.42)
axE, axm = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
for ax in (axE, axm):
    style.arrows(ax, ticks=True)
    ax.tick_params(labelsize=FS, length=2.5)
    ax.spines['bottom'].set_visible(True); ax.spines['left'].set_visible(True)
    ax.set_xticks([0, 2, 4, 6, 8]); ax.set_xlim(0, 8.3)
    style.guide(ax, x=2)
axE.plot(Us, Eex, color=style.ACCENT)
axE.plot(Us, Emf, color=style.BROKEN, ls=(0, (4, 2)))
axE.set_ylim(-2.1, 0.05); axE.set_yticks([-2, -1, 0])
style.label(axE, 6.2, -0.95, 'exact', color=style.ACCENT, fontsize=FS)
style.label(axE, 3.0, -0.2, 'mean field', color=style.BROKEN, fontsize=FS)
axE.annotate(r'$E_0/t$', xy=(0, 1.06), xycoords='axes fraction', ha='center', va='bottom', fontsize=FS)
axE.annotate(r'$U/t$', xy=(1.03, 0), xycoords='axes fraction', ha='left', va='center', fontsize=FS)
axm.plot(Us, np.zeros_like(Us), color=style.ACCENT)
axm.plot(Us, mmf, color=style.BROKEN, ls=(0, (4, 2)))
axm.set_ylim(-0.05, 1.05); axm.set_yticks([0, 0.5, 1])
style.label(axm, 5.6, 0.12, 'exact', color=style.ACCENT, fontsize=FS)
style.label(axm, 4.6, 0.62, 'mean field', color=style.BROKEN, fontsize=FS)
axm.annotate(r'$m$', xy=(0, 1.06), xycoords='axes fraction', ha='center', va='bottom', fontsize=FS)
axm.annotate(r'$U/t$', xy=(1.03, 0), xycoords='axes fraction', ha='left', va='center', fontsize=FS)
style.save(fig, __file__)
