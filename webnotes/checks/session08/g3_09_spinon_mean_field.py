"""Session 8, the numbers and the algebra that page 09 (Section 8.9, the mean-field spinon Hamiltonian and its classes
of bands) quotes, checked by a second route.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The figure scripts assert their own numbers: _g3_bands.check, which spinon_bands.py
and the three pictures of the quiz call (the crossings at +-pi/2, the gap 0.8 at +-pi, the touchings at 0 and +-pi with
the slope 2, the sign of the hopping), and g3_fermi_surface_triangular.py (the map against the band by hand, the filling
0.500 to 0.001, the sign of both hoppings, the contours around Gamma and K). This script checks the fold from (8.14) to
(8.15) with fermion matrices on two sites, the Lagrange multiplier on the chain and on the triangular lattice, the
problem of the self-consistent chain and the free loop that dimerizes with the sign of its start, the feedback of the
rewritten quiz, the densities of states of the new one, the symmetry around zero of the three models of the figure, and
the second gauge of the pi-flux lattice that the caption names. It writes no file, since pyqula runs in a temporary
folder."""
import itertools
import os
import tempfile

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def modes(m):
    """Annihilation operators of m fermion modes, with the Jordan-Wigner strings."""
    a, z = np.array([[0.0, 1.0], [0.0, 0.0]]), np.diag([1.0, -1.0])
    out = []
    for k in range(m):
        o = np.eye(1)
        for j in range(m):
            o = np.kron(o, z if j < k else (a if j == k else np.eye(2)))
        out.append(o.astype(complex))
    return out


def dag(x):
    return x.conj().T


# ------------------------------------------------------------------------------------------------------------------
# the fold "From the decoupling (8.14) to the hopping model (8.15)", on the 16 states of two sites
fiu, fid, fju, fjd = modes(4)
fi, fj = (fiu, fid), (fju, fjd)
I16 = np.eye(16)
chi = dag(fiu) @ fju + dag(fid) @ fjd                  # the bond operator (8.12), moves a fermion from j to i
rng = np.random.default_rng(5)
A = rng.standard_normal((16, 16)) + 1j * rng.standard_normal((16, 16))
rho = A @ dag(A); rho /= np.trace(rho)                  # some state, to take the expectation values in
c = np.trace(rho @ chi)                                 # <chi_ij>, a complex number
J = 0.7
dec = -J / 2 * (np.conj(c) * chi + c * dag(chi)) + J / 2 * abs(c) ** 2 * I16
check('fold: chi^dag chi minus its decoupling is the fluctuation (chi^dag - <chi>*)(chi - <chi>)',
      np.abs(dag(chi) @ chi - (np.conj(c) * chi + c * dag(chi) - abs(c) ** 2 * I16)
             - (dag(chi) - np.conj(c) * I16) @ (chi - c * I16)).max() < 1e-12, 'ok')
vac = np.zeros(16); vac[0] = 1.0
coef = {(a, b): vac @ fa @ dec @ dag(fb) @ vac for a, fa in (('i', fiu), ('j', fju)) for b, fb in (('i', fiu), ('j', fju))}
corr = sum(np.trace(rho @ dag(fj[s]) @ fi[s]) for s in range(2))     # sum_s <f^dag_js f_is>
check('fold: the coefficient of f^dag_is f_js is -(J/2)<chi_ij>* = -(J/2) sum_s <f^dag_js f_is>',
      abs(coef[('i', 'j')] + J / 2 * np.conj(c)) < 1e-12 and abs(np.conj(c) - corr) < 1e-12,
      np.round(coef[('i', 'j')], 6))
check('fold: the coefficient of f^dag_js f_is is its complex conjugate, and no onsite term appears',
      abs(coef[('j', 'i')] - np.conj(coef[('i', 'j')])) < 1e-12
      and abs(coef[('i', 'i')] - J / 2 * abs(c) ** 2) < 1e-12 and abs(coef[('j', 'j')] - J / 2 * abs(c) ** 2) < 1e-12,
      'the diagonal is only the constant (J/2)|<chi>|^2 = %.4f' % (J / 2 * abs(c) ** 2))
same_down = vac @ fid @ dec @ dag(fjd) @ vac
check('fold: the same coefficient for both spins s', abs(same_down - coef[('i', 'j')]) < 1e-12, np.round(same_down, 6))

# the Lagrange multiplier: zero on the chain, and on the triangular lattice the Fermi level of half filling
k = (np.arange(4000) + 0.5) / 4000 * 2 * np.pi
check('fold: the chain band 2 chi cos k is symmetric around zero, so half filling is at zero and lambda = 0',
      abs(np.median(2 * np.cos(k))) < 1e-12, np.median(2 * np.cos(k)))
c2 = lambda x: np.cos(2 * np.pi * x)
n = 2400
u = (np.arange(n) + 0.5) / n
U, V = np.meshgrid(u, u, indexing='ij')
tri = 2 * (c2(U) + c2(V) + c2(U + V))                  # geometry.triangular_lattice(), hopping +1, reduced momenta
tri_nodes = [2 * (c2(a) + c2(b) + c2(a + b)) for a, b in ((0, 0), (1 / 3, 1 / 3))]
ef_mesh, tri_min, tri_max = np.median(tri), tri.min(), tri.max()
del tri, U, V


def below(eps, nb=32000):
    """The fraction of the triangular band below eps, exact in the first reduced momentum a: at fixed b the band is
    4 cos(b/2) cos(a + b/2) + 2 cos b, and a runs over a whole period, so the fraction is an arccos."""
    b = 2 * np.pi * (np.arange(nb) + 0.5) / nb
    A, C = 4 * np.cos(b / 2), 2 * np.cos(b)
    y = np.clip((eps - C) / A, -1, 1)
    return np.mean(np.where(A > 0, 1 - np.arccos(y) / np.pi, np.arccos(y) / np.pi))


ef = brentq(lambda e: below(e) - 0.5, -2, 0, xtol=1e-12)
check('fold: the triangular band with the hopping 1 runs from -3 (at K) to 6 (at Gamma), and half filling is at -0.835, '
      'exact in one momentum and the median of a mesh of 2400 by 2400',
      np.allclose(tri_nodes, [6, -3]) and tri_min > -3 - 1e-9 and tri_max < 6 + 1e-9
      and abs(below(-3) - 0) < 1e-12 and abs(below(6) - 1) < 1e-12
      and abs(ef + 0.83475) < 2e-5 and abs(ef_mesh - ef) < 1e-4 and round(ef, 3) == -0.835, (round(ef, 6), round(ef_mesh, 6)))

# ------------------------------------------------------------------------------------------------------------------
# the problem: the self-consistent uniform chain
val = quad(np.cos, -np.pi / 2, np.pi / 2)[0] / (2 * np.pi)     # the imaginary part of e^{ik} integrates to zero
check('solution: <f^dag_i f_i+1> = int_{-pi/2}^{pi/2} e^{ik} dk / 2pi = 1/pi per spin', abs(val - 1 / np.pi) < 1e-12, val)
check('solution: <chi> = 2/pi = 0.64, chi = -J/pi = -0.32 J, and the width 4J/pi = 1.27 J',
      round(2 / np.pi, 2) == 0.64 and round(-1 / np.pi, 2) == -0.32 and round(4 / np.pi, 2) == 1.27,
      (2 / np.pi, -1 / np.pi, 4 / np.pi))
N = 98                                                   # a ring of 98 sites, 49 fermions per spin, a closed shell


def correlations(t):
    """<f^dag_i+1 f_i> for one spin at half filling of the ring with the hoppings t[i] between i and i+1."""
    M = np.zeros((N, N))
    for i in range(N):
        M[i, (i + 1) % N] = M[(i + 1) % N, i] = t[i]
    v = np.linalg.eigh(M)[1][:, :N // 2]
    G = v @ v.T                                          # G[a, b] = <f^dag_a f_b>
    return np.array([G[(i + 1) % N, i] for i in range(N)])


def step(t):
    """One step of the loop, J = 1: the new hopping on i, i+1 is -(J/2) sum_s <f^dag_i+1,s f_i,s>, both spins."""
    return -0.5 * 2 * correlations(t)


g = correlations(-np.ones(N) / np.pi)
check('solution: on a ring of 98 sites with the hopping -1/pi, <f^dag_i f_i+1> per spin is 1/pi to 1e-3',
      np.allclose(g, g[0]) and abs(g[0] - 1 / np.pi) < 1e-3, g[0])
fix = [step(s * np.ones(N) / np.pi) for s in (-1, 1)]
check('solution: -J/pi and +J/pi are both fixed points of the loop, |chi| = J/pi = 0.318 J',
      all(np.allclose(f, s / np.pi, atol=1e-3) for f, s in zip(fix, (-1, 1))), (fix[0][0], fix[1][0]))
stag = (-1.0) ** np.arange(N)
check('solution: f_j -> (-1)^j f_j changes the sign of every hopping of the chain',
      np.allclose(np.diag(stag) @ (np.diag(np.ones(N - 1), 1) + np.diag(np.ones(N - 1), -1)) @ np.diag(stag),
                  -(np.diag(np.ones(N - 1), 1) + np.diag(np.ones(N - 1), -1))), 'ok')
rng = np.random.default_rng(7)
t = -1 / np.pi + 1e-3 * rng.standard_normal(N)
for it in range(4000):
    new = step(t)
    if np.abs(new - t).max() < 1e-12:
        break
    t = 0.5 * new + 0.5 * t
bond = 2 * correlations(t)                               # <chi_i,i+1>, both spins
E_dim = np.mean(0.25 - 0.5 * bond ** 2)
E_uni = 0.25 - 0.5 * (2 / np.pi) ** 2
strong = t[np.abs(t) > 0.25]
check('solution: the free loop from the uniform chain with chi < 0 ends at the hoppings -J/2 and 0 on alternate bonds',
      np.allclose(np.sort(np.abs(t))[:N // 2], 0, atol=1e-6) and np.allclose(np.sort(np.abs(t))[N // 2:], 0.5, atol=1e-6)
      and np.allclose(np.abs(t[::2]), np.abs(t[0])) and np.allclose(np.abs(t[1::2]), np.abs(t[1]))
      and len(strong) == N // 2 and np.allclose(strong, -0.5, atol=1e-6), (it, t[:2].round(6)))
check('solution: the mean-field energy J/4 - (J/2)|<chi>|^2 is 0 per bond for it and 0.047 J for the uniform chain',
      abs(E_dim) < 1e-9 and round(E_uni, 3) == 0.047 and E_dim < E_uni, (E_dim, E_uni))

# ------------------------------------------------------------------------------------------------------------------
# the quiz on half filling, the feedback of the two wrong options
m = 400
q = 2 * np.pi * (np.arange(m) + 0.5) / m
QX, QY = np.meshgrid(q, q, indexing='ij')
sq = 2 * (np.cos(QX) + np.cos(QY))
sq2 = sq + 4 * 0.3 * np.cos(QX) * np.cos(QY)            # a second-neighbor hopping 0.3 on the square lattice
ph = lambda E: np.abs(np.sort(E.ravel()) + np.sort(E.ravel())[::-1] - 2 * np.median(E)).max()
check('quiz: a second-neighbor hopping breaks the particle-hole symmetry of the square lattice',
      ph(sq) < 1e-9 and ph(sq2) > 0.5, (ph(sq), round(ph(sq2), 3)))
e03 = np.quantile(sq, 0.3)
check('quiz: at the filling 0.3 the Fermi level is inside the band, so there is a Fermi surface',
      sq.min() + 0.5 < e03 < sq.max() - 0.5 and np.sum(np.abs(sq - e03) < 0.05) > 0, round(e03, 3))

# the picture quiz: the density of states at the Fermi level is finite for the chain and vanishes for the pi-flux lattice
cwd = os.getcwd()
with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    try:
        from pyqula import geometry
        h = geometry.square_lattice().get_supercell([1, 2]).get_hamiltonian(has_spin=False)
        h.add_orbital_magnetic_field(0.5)
        hk = h.get_hk_gen()
        ks = np.arange(80) / 80
        Ep = np.array([np.linalg.eigvalsh(hk([a, b, 0.])) for a in ks for b in ks])
        line = np.linspace(-0.5, 0.5, 401)                 # k_x from -pi to pi on the line k_y = pi/2 of the figure
        Ep_line = np.array([np.linalg.eigvalsh(hk([a, 0.5, 0.])) for a in line])
        hc = geometry.chain().get_hamiltonian(has_spin=False).get_hk_gen()
        hb = geometry.bichain().get_hamiltonian(has_spin=False)
        hb.intra = 0.6 * hb.intra
        hb = hb.get_hk_gen()
        q = np.arange(400) / 400                           # a whole period of the zone, with no point twice
        Ec = np.array([np.linalg.eigvalsh(hc([a, 0., 0.])) for a in q]).ravel()
        Eb = np.array([np.linalg.eigvalsh(hb([a, 0., 0.])) for a in q]).ravel()
    finally:
        os.chdir(cwd)
K1, K2 = np.meshgrid(ks, ks, indexing='ij')
closed = 2 * np.sqrt(np.sin(2 * np.pi * K1) ** 2 + np.cos(np.pi * K2) ** 2).ravel()
check('quiz: the pi-flux bands of pyqula are +-2 sqrt(sin^2 2 pi k1 + cos^2 pi k2), up to 2 sqrt 2, and touch at zero',
      np.abs(Ep[:, 1] - closed).max() < 1e-12 and np.allclose(Ep[:, 0], -Ep[:, 1]) and abs(closed.max() - 2 * np.sqrt(2)) < 1e-12
      and closed.min() < 1e-12, np.abs(Ep[:, 1] - closed).max())


def h_real(kx, ky):
    """The pi-flux lattice in a real gauge, a cell of two sites along y, the hopping (-1)^y along x on the row y and 1
    along y. kx is per site and ky per cell of two sites."""
    return np.array([[2 * np.cos(kx), 1 + np.exp(-1j * ky)], [1 + np.exp(1j * ky), -2 * np.cos(kx)]])


Er = np.array([np.linalg.eigvalsh(h_real(2 * np.pi * a, 2 * np.pi * b)) for a in ks for b in ks])
Er_line = np.array([np.linalg.eigvalsh(h_real(2 * np.pi * a, np.pi)) for a in line])
flux_real = [(-1.0) ** y * 1.0 * (-1.0) ** (y + 1) * 1.0 for y in range(4)]   # x bond, y bond, x bond back, y bond back
check('caption: the real gauge with (-1)^y along x has the flux -1 on every plaquette and the levels of pyqula on the '
      '80 by 80 mesh, and on the line k_y = pi/2 its Dirac points are at k_x = +-pi/2, while those of pyqula are at 0 and pi',
      np.allclose(flux_real, -1) and np.abs(np.sort(Ep.ravel()) - np.sort(Er.ravel())).max() < 1e-12
      and np.allclose(2 * line[np.abs(Er_line[:, 1]) < 1e-9], [-0.5, 0.5])
      and np.allclose(2 * line[np.abs(Ep_line[:, 1]) < 1e-9], [-1, 0, 1]),
      (np.abs(np.sort(Ep.ravel()) - np.sort(Er.ravel())).max(), 2 * line[np.abs(Er_line[:, 1]) < 1e-9]))
sym = lambda E: np.abs(np.sort(E) + np.sort(E)[::-1]).max()
check('caption and quiz: the levels of the uniform chain, of the dimerized chain and of the pi-flux lattice are symmetric '
      'around zero over the whole zone, so half filling puts the Fermi level at E = 0, unlike the triangular lattice',
      max(sym(Ec), sym(Eb), sym(Ep.ravel())) < 1e-12
      and all(np.mean(E < -1e-9) <= 0.5 <= np.mean(E < 1e-9) for E in (Ec, Eb, Ep.ravel())) and abs(ef) > 0.8,
      (sym(Ec), sym(Eb), sym(Ep.ravel())))
nd = 1200
u = (np.arange(nd) + 0.5) / nd
U1, U2 = np.meshgrid(u, u, indexing='ij')
E2 = 2 * np.sqrt(np.sin(2 * np.pi * U1) ** 2 + np.cos(np.pi * U2) ** 2)
kc = 2 * np.pi * (np.arange(200000) + 0.5) / 200000
E1 = np.abs(2 * np.cos(kc))
r1 = np.sum(E1 < 0.2) / np.sum(E1 < 0.1)
r2 = np.sum(E2 < 0.2) / np.sum(E2 < 0.1)
check('quiz: the states below |E| = eps grow as eps for the chain, a finite density at the Fermi level, and as eps^2 '
      'for the pi-flux lattice, a density that vanishes there', abs(r1 - 2) < 0.05 and abs(r2 - 4) < 0.2,
      (round(r1, 3), round(r2, 3)))

# corrected and decided on 2026-11-22, old text of the page
# the time-reversal sentence, the caption of Figure 8.4, the second quiz and the pointer of page 06: the same chi_ij for
# both spins gives <S_i> = 0 for any chi_ij, and real chi_ij give a state that time reversal maps to itself. A complex
# chi_ij can break time reversal with <S_i> = 0 on a lattice with triangles. The check is the scalar chirality
# <S_0.(S_1 x S_2)>, which time reversal turns into minus itself, in the half-filled mean-field state of four sites, with
# the parton spins (8.10) in the Fock space of eight modes. On the square ring with the flux pi/2 or pi/3 it is zero on
# every triple, so the flux alone does not break the symmetry there, while the ring with one diagonal, two triangles with
# the flux pi/4 and pi/6, has 0.050 and 0.056, and with real hoppings 0.
f8 = modes(8)
fm = lambda i_, s_: f8[2 * i_ + s_]
P3 = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], complex)]
Sp = [[0.5 * sum(P_[a, b] * dag(fm(i_, a)) @ fm(i_, b) for a in range(2) for b in range(2)) for P_ in P3] for i_ in range(4)]
N8 = np.real(np.diag(sum(dag(x) @ x for x in f8)))
sector = np.where(np.isclose(N8, 4))[0]


def mf_state(h4):
    H8 = sum(h4[i_, j_] * dag(fm(i_, s_)) @ fm(j_, s_) for i_ in range(4) for j_ in range(4) for s_ in range(2) if abs(h4[i_, j_]) > 0)
    w_, v_ = np.linalg.eigh(H8[np.ix_(sector, sector)])
    psi = np.zeros(256, complex)
    psi[sector] = v_[:, 0]
    return psi, w_[1] - w_[0]


def chirality(psi, i_, j_, k_):
    cr = [Sp[j_][1] @ Sp[k_][2] - Sp[j_][2] @ Sp[k_][1], Sp[j_][2] @ Sp[k_][0] - Sp[j_][0] @ Sp[k_][2],
          Sp[j_][0] @ Sp[k_][1] - Sp[j_][1] @ Sp[k_][0]]
    return np.vdot(psi, sum(Sp[i_][a] @ cr[a] for a in range(3)) @ psi).real


def ring4(phi, diag=0.0):
    h4 = np.zeros((4, 4), complex)
    for i_, j_ in ((0, 1), (1, 2), (2, 3), (3, 0)):
        h4[i_, j_] = np.exp(1j * phi / 4)
    h4[0, 2] = diag
    return h4 + dag(h4)


triples = list(itertools.combinations(range(4), 3))
ring_ok, tri_vals, mags = True, {}, 0.0
for phi in (np.pi / 2, np.pi / 3):
    psi, gap = mf_state(ring4(phi))
    ring_ok = ring_ok and gap > 0.5 and max(abs(chirality(psi, *t_)) for t_ in triples) < 1e-12
    psi, gap = mf_state(ring4(phi, 0.7))
    tri_vals[round(phi / np.pi, 3)] = round(chirality(psi, 0, 1, 2), 4)
    mags = max(mags, max(abs(np.vdot(psi, Sp[i_][a] @ psi)) for i_ in range(4) for a in range(3)))
psi0, gap0 = mf_state(ring4(0.0, 0.7))
check('corrected, time reversal of the spinon mean field: <S_i> = 0, the chirality is zero on the square ring with the flux '
      'pi/2 and pi/3, and 0.050 and 0.056 with one diagonal, while real hoppings give 0',
      ring_ok and mags < 1e-12 and abs(tri_vals[0.5] - 0.0504) < 1e-3 and abs(tri_vals[0.333] - 0.0564) < 1e-3
      and gap0 > 0.5 and abs(chirality(psi0, 0, 1, 2)) < 1e-12, (tri_vals, mags))
# the first quiz: the constraint holds on average in the mean-field state, and not exactly. On the half-filled chain each
# spin state of a site is filled with the probability 1/2, independently, so <n_i> = 1 with the variance 1/2, by Wick's
# theorem on a ring of 98 sites and by the binomial count.
Mr = np.zeros((N, N))
for i in range(N):
    Mr[i, (i + 1) % N] = Mr[(i + 1) % N, i] = -1.0
vr = np.linalg.eigh(Mr)[1][:, :N // 2]
Gr = vr @ vr.T
n_mean = 2 * Gr[0, 0]
n_var = 2 * Gr[0, 0] * (1 - Gr[0, 0])                    # two independent spins, each with <n> = G_00
binom = sum(p_ * (n_ - 1) ** 2 for n_, p_ in ((0, 0.25), (1, 0.5), (2, 0.25)))
check('corrected, first quiz: in the mean-field state <n_i> = 1 with the variance 1/2, so one f fermion per site only on average',
      abs(n_mean - 1) < 1e-12 and abs(n_var - 0.5) < 1e-12 and abs(binom - 0.5) < 1e-12, (n_mean, n_var))
# the word "real" removed from two sentences: the pi-flux lattice of the figure, in the gauge of pyqula, has the complex
# hoppings +i and -i, and its levels are those of a real gauge (the caption check above)
mc = {tuple(int(x) for x in t_.dir): np.asarray(t_.m.todense() if hasattr(t_.m, 'todense') else t_.m) for t_ in h.get_multicell().hopping}
imag_links = sorted(set(np.round(np.imag(mc[(1, 0, 0)][np.abs(mc[(1, 0, 0)]) > 1e-9]), 9).tolist()))
check('decided, the pi-flux hoppings of pyqula along x are +i and -i, so the Hamiltonian is not a real matrix',
      imag_links == [-1.0, 1.0], imag_links)
# the class bullets: the uniform chain has one band through the Fermi level and a finite density of states there, and the
# pi-flux lattice two bands that touch with a density of states that vanishes (the ratios r1 and r2 above)
check('corrected, class bullets: the chain has one band through zero and the ratio %.3f, the pi-flux lattice two bands that '
      'touch at zero and the ratio %.3f' % (r1, r2),
      np.asarray(hc([0.1, 0., 0.])).shape == (1, 1) and abs(r1 - 2) < 0.05 and abs(r2 - 4) < 0.2 and np.abs(Ep[:, 1] + Ep[:, 0]).max() < 1e-12
      and Ep[:, 1].min() < 1e-12, (round(r1, 3), round(r2, 3)))
print('all checks of page 09 hold')
