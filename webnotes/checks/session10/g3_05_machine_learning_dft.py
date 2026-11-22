"""Session 10, the numbers that page 05 (Section 10.5, machine learning in density functional theory) quotes.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The figure ks_loop.py asserts the 36 iterations, the 0.99 and 1.21, the ratio
near one half, the curves that it draws and the center and width of its well. This script repeats its loop and asserts
the numbers of the caption again, with those of the quizzes and of the solution that use the same toy. It also checks
the steps from (10.7) to (10.8) on the lattice toy, where the Hartree energy is (U/2) sum_i n(i)^2 on the total density
n(i), with the orthogonality of the orbitals and the Hubbard term of the same state, the problem of the two sites, and
the counts of the quizzes. The hopping is -t with t=1, as in ks_loop.py. It imports nothing of the repository and
writes no file."""
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# ------------------------------------------------------------------ the loop of the figure ks_loop, as in ks_loop.py
N, NE, U, ALPHA = 60, 40, 2.0, 0.3
x = np.arange(N)
vext = -2.0 * np.exp(-((x - 29.5) / 7.0) ** 2)
T = -np.eye(N, k=1) - np.eye(N, k=-1)


def ks_density(n, U=U):
    w = np.linalg.eigh(T + np.diag(vext + U * n))[1]
    return 2 * (np.abs(w[:, :NE // 2]) ** 2).sum(axis=1)


n = np.full(N, NE / N)
hist, res = [n.copy()], []
for it in range(60):
    nn = ks_density(n)
    res.append(np.abs(nn - n).max())
    n = (1 - ALPHA) * n + ALPHA * nn
    hist.append(n.copy())
    if res[-1] < 1e-10:
        break
res = np.array(res)
n_conv, n_free = hist[-1], ks_density(np.zeros(N), U=0.0)
ratio = res[1:] / res[:-1]

check('the toy has 60 sites, 40 electrons, U=2t and 30 percent mixing, and the start is the uniform 40/60',
      N == 60 and NE == 40 and U == 2.0 and ALPHA == 0.3 and np.allclose(hist[0], 2 / 3), hist[0][0])
check('the largest difference max|n_out - n_in| reaches 1e-10 after 36 iterations, the caption of ks_loop as corrected on '
      '2026-11-22',
      len(res) == 36 and res[-1] < 1e-10 <= res[-2], (len(res), res[-2], res[-1]))
check('the density at the center ends at 0.99 with the Hartree term and is 1.21 for the well alone',
      round(n_conv[30], 2) == 0.99 and round(n_free[30], 2) == 1.21 and abs(n_conv[29] - n_conv[30]) < 1e-12,
      (n_conv[30], n_free[30]))
check('the largest change falls by about the same factor at every iteration, close to one half, a ratio between '
      '0.48 and 0.53', round(ratio.min(), 2) == 0.48 and round(ratio.max(), 2) == 0.53, (ratio.min(), ratio.max()))
check('the plotted change is the difference between the density of the diagonalization and the density that went in, '
      'and the well is centered at 29.5 with the width 7, the caption of ks_loop',
      np.allclose(vext, vext[::-1]) and np.isclose(np.log(vext[30] / vext[37]), 8 / 7)
      and np.isclose(res[0], np.abs(ks_density(hist[0]) - hist[0]).max()), (vext[30], vext[37], res[0]))
excess = (n_conv[30] - hist[0][30]) / (n_free[30] - hist[0][30])
check('the excess density at the center above the uniform 2/3 falls to about 0.6 of its value without U, the solution',
      round(excess, 1) == 0.6 and np.isclose(hist[0][30], 2 / 3), excess)
# The response of the chain: the Jacobian of n_in -> n_out at convergence. Its columns sum to zero, since the charge is
# fixed, so one eigenvalue is zero. The others set the error factor 0.7 + 0.3 lambda of the loop with 30 percent mixing.
Jac = np.zeros((N, N))
for j in range(N):
    e = np.zeros(N)
    e[j] = 1e-6
    Jac[:, j] = (ks_density(n_conv + e) - ks_density(n_conv - e)) / 2e-6
lam = np.linalg.eigvals(Jac).real
lam = lam[np.abs(lam) > 1e-6]
slow = np.abs(0.7 + 0.3 * lam).max()
check('on the chain the mixed loop multiplies the error by about one half and not by 0.1, since the response of the '
      'chain is not that of two sites, the solution', round(slow, 2) == 0.53 and abs(slow - ratio[-1]) < 0.01
      and lam.min() < -3 and len(lam) == N - 1 and np.abs(Jac.sum(axis=0)).max() < 1e-6,
      (slow, ratio[-1], lam.min(), lam.max()))
check('the electrons are conserved, 40 at convergence', abs(n_conv.sum() - 40) < 1e-9, n_conv.sum())
check('the well is the same at every iteration, while the density at the center goes from 0.67 to 0.99',
      round(hist[0][30], 2) == 0.67 and round(hist[-1][30], 2) == 0.99, (hist[0][30], hist[-1][30]))

# ------------------------------------------------------------------ the steps from (10.7) to (10.8) on the toy
rng = np.random.default_rng(0)
n0 = rng.uniform(0, 2, N)
E_H = lambda m: U / 2 * (m ** 2).sum()
grad = np.array([(E_H(n0 + 1e-6 * e) - E_H(n0 - 1e-6 * e)) / 2e-6 for e in np.eye(N)])
check('the derivative of the Hartree energy (U/2) sum n(i)^2 is U n(i), with no factor 1/2',
      np.abs(grad - U * n0).max() < 1e-6, np.abs(grad - U * n0).max())


def energy(W):
    """E = T_s + sum v_ext n + E_H with the 20 lowest columns of W filled with two electrons each, n = 2 sum |phi|^2."""
    occ = W[:, :NE // 2]
    m = 2 * (occ ** 2).sum(axis=1)
    return 2 * np.einsum('ik,ij,jk->', occ, T + np.diag(vext), occ) + E_H(m), m


w_conv = np.linalg.eigh(T + np.diag(vext + U * n_conv))[1]
check('the orbitals of H_KS at convergence give back the density of the loop, with n = 2 sum |phi|^2',
      np.abs(energy(w_conv)[1] - n_conv).max() < 1e-9, np.abs(energy(w_conv)[1] - n_conv).max())
d1, d2, d1_free = [], [], []
for k in range(10):
    G = np.zeros((N, N))
    G[:NE // 2, NE // 2:] = rng.normal(size=(NE // 2, N - NE // 2))
    G = G - G.T                                 # a rotation that mixes the filled and the empty orbitals
    h = 1e-4
    for W, out in ((w_conv, 'conv'), (np.linalg.eigh(T + np.diag(vext))[1], 'free')):
        f = lambda th: energy(W @ expm(th * G))[0]
        if out == 'conv':
            d1.append((f(h) - f(-h)) / (2 * h))
            d2.append((f(h) - 2 * f(0) + f(-h)) / h ** 2)
        else:
            d1_free.append((f(h) - f(-h)) / (2 * h))
check('the self-consistent orbitals are a minimum of E[n] in 10 random rotations, no first-order change and a '
      'positive second order, while the orbitals of the well alone have a first-order change',
      max(abs(np.array(d1))) < 1e-4 and min(d2) > 1 and min(abs(np.array(d1_free))) > 0.1,
      (max(abs(np.array(d1))), min(d2), min(abs(np.array(d1_free)))))
# The second order for any rotation K (filled i, empty a) is 2 sum K_ia^2 (eps_a - eps_i) + (U/2) sum delta n^2, with
# delta n = 4 sum K_ia phi_i phi_a, so it is positive for every K when the gap and U are positive: a minimum in all
# directions, and not only in the random ones above.
eps = np.linalg.eigh(T + np.diag(vext + U * n_conv))[0]
occ, vir = w_conv[:, :NE // 2], w_conv[:, NE // 2:]
agree = []
for k in range(5):
    K = rng.normal(size=(NE // 2, N - NE // 2))
    G = np.zeros((N, N))
    G[:NE // 2, NE // 2:] = K
    G = G - G.T
    h = 1e-3
    f = lambda th: energy(w_conv @ expm(th * G))[0]
    fd = (f(h) + f(-h) - 2 * f(0)) / (2 * h * h)
    dn = 4 * np.einsum('ia,ri,ra->r', K, occ, vir)
    agree.append(fd / (2 * np.sum(K ** 2 * (eps[None, NE // 2:] - eps[:NE // 2, None])) + U / 2 * np.sum(dn ** 2)))
check('the second order of a rotation is 2 sum K^2 (eps_a - eps_i) + (U/2) sum dn^2, positive since every empty '
      'orbital lies above every filled one (gap %.4f) and U>0, so the loop ends at a minimum' % (eps[20] - eps[19]),
      np.allclose(agree, 1, atol=1e-4) and eps[NE // 2] - eps[NE // 2 - 1] > 0.05 and U > 0, agree)

# The same with one set of orbitals per spin, Wu and Wd, 20 electrons each. With the Hartree term on the total density
# the second order is sum_s sum K_s^2 (eps_a - eps_i) + (U/2) sum (dn_up + dn_dn)^2, and with a Hubbard term
# U_H sum n_up n_dn it is the same first part + U_H sum dn_up dn_dn, with dn_s = 2 sum K_s phi_i phi_a.
UH = 2 * U
H0 = T + np.diag(vext)


def energy_spin(Wu, Wd, kind):
    ou, od = Wu[:, :NE // 2], Wd[:, :NE // 2]
    nu, nd = (ou ** 2).sum(axis=1), (od ** 2).sum(axis=1)
    kin = np.einsum('ik,ij,jk->', ou, H0, ou) + np.einsum('ik,ij,jk->', od, H0, od)
    return kin + (U / 2 * ((nu + nd) ** 2).sum() if kind == 'hartree' else UH * (nu * nd).sum())


def rotation(K):
    G = np.zeros((N, N))
    G[:NE // 2, NE // 2:] = K
    return G - G.T


E0 = energy(w_conv)[0]
Q = np.linalg.qr(rng.normal(size=(NE // 2, NE // 2)))[0]
w_rot = w_conv.copy()
w_rot[:, :NE // 2] = w_conv[:, :NE // 2] @ Q
check('E does not change under a rotation among the filled orbitals of one spin, so the multipliers can be diagonal',
      abs(energy_spin(w_rot, w_conv, 'hartree') - E0) < 1e-10 and abs(energy_spin(w_conv, w_conv, 'hartree') - E0) < 1e-10,
      (E0, energy_spin(w_rot, w_conv, 'hartree')))
# Only the normalization as a constraint: 4 electrons in one shared orbital have a lower E than in orthogonal orbitals.
n4 = np.full(N, 4 / N)
for k in range(3000):
    n4 = 0.7 * n4 + 0.3 * 2 * (np.linalg.eigh(T + np.diag(vext + U * n4))[1][:, :2] ** 2).sum(axis=1)
o4 = np.linalg.eigh(T + np.diag(vext + U * n4))[1][:, :2]
E4 = 2 * np.einsum('ik,ij,jk->', o4, H0, o4) + U / 2 * (n4 ** 2).sum()
E_shared = lambda p: 4 * (p / np.linalg.norm(p)) @ H0 @ (p / np.linalg.norm(p)) + U / 2 * ((4 * p ** 2 / (p @ p)) ** 2).sum()
b4 = minimize(E_shared, o4[:, 0], method='BFGS').fun
check('without the orthogonality the minimum is not the Kohn-Sham state, since 4 electrons in one shared orbital have '
      'a lower E than in two orbitals of opposite spin each', b4 < E4 - 0.2, (b4, E4))
fd_h, an_h, an_u = [], [], []
for k in range(6):
    Ku, Kd = rng.normal(size=(NE // 2, N - NE // 2)), rng.normal(size=(NE // 2, N - NE // 2))
    h = 1e-3
    dnu = 2 * np.einsum('ia,ri,ra->r', Ku, occ, vir)
    dnd = 2 * np.einsum('ia,ri,ra->r', Kd, occ, vir)
    gapterm = np.sum((Ku ** 2 + Kd ** 2) * (eps[None, NE // 2:] - eps[:NE // 2, None]))
    for kind, store, an in (('hartree', fd_h, an_h), ('hubbard', [], an_u)):
        f = lambda th: energy_spin(w_conv @ expm(th * rotation(Ku)), w_conv @ expm(th * rotation(Kd)), kind)
        fd = (f(h) + f(-h) - 2 * f(0)) / (2 * h * h)
        a = gapterm + (U / 2 * np.sum((dnu + dnd) ** 2) if kind == 'hartree' else UH * np.sum(dnu * dnd))
        store.append(fd)
        an.append(fd / a)
check('with one set of orbitals per spin the second order is the gap term plus (U/2) sum dn^2 on the total density, '
      'positive in 6 random rotations', np.allclose(an_h, 1, atol=1e-3) and np.allclose(an_u, 1, atol=1e-3)
      and min(fd_h) > 0, (min(fd_h), an_h, an_u))
Kone = np.zeros((NE // 2, N - NE // 2))
Kone[-1, 0] = 1.0                       # from the last filled orbital to the first empty one
second = {}
for kind in ('hartree', 'hubbard'):
    f = lambda th: energy_spin(w_conv @ expm(th * rotation(Kone)), w_conv @ expm(-th * rotation(Kone)), kind)
    second[kind] = (f(1e-3) + f(-1e-3) - 2 * f(0)) / 1e-6
check('a Hubbard term U_H sum n_up n_dn with U_H = 2U has the same converged state and energy, since each spin feels '
      'U_H n/2 = U n, but there it is a saddle point, since opposite changes of n_up and n_dn lower E, while with the '
      'Hartree term on the total density the same rotation raises E',
      np.allclose(vext + UH * n_conv / 2, vext + U * n_conv) and abs(energy_spin(w_conv, w_conv, 'hubbard') - E0) < 1e-10
      and second['hubbard'] < -0.2 and second['hartree'] > 0.2, (E0, second))
check('the well of the caption is -2t exp(-((i-29.5)/7)^2) with the hopping -t, t=1',
      abs(vext.min() + 2 * np.exp(-(0.5 / 7) ** 2)) < 1e-12 and T[0, 1] == -1.0, (vext.min(), T[0, 1]))
nloop, r = np.full(N, NE / N), []
for it in range(300):
    nn = ks_density(nloop)
    r.append(np.abs(nn - nloop).max())
    nloop = nn
check('the loop of the chain does not converge without mixing, the largest change stays above 1 after 300 '
      'iterations', min(r[-20:]) > 1, (min(r[-20:]), max(r[-20:])))

# ------------------------------------------------------------------ the simplest case of the fold, and the problem
t = 1.0


def dimer(D, U, mix=0.3, steps=4000):
    """Two sites with hopping -t, v_ext = (D/2, -D/2), two electrons of opposite spin in the lowest orbital,
    v_eff(i) = v_ext(i) + U n(i), and the new density mixed with the weight mix."""
    v, n = np.array([D / 2, -D / 2]), np.array([1.0, 1.0])
    for k in range(steps):
        phi = np.linalg.eigh(np.array([[v[0] + U * n[0], -t], [-t, v[1] + U * n[1]]]))[1][:, 0]
        n = (1 - mix) * n + mix * 2 * phi ** 2
    return n


a = np.linspace(0, np.pi, 200001)
D, Ud = 0.3, 2.0
phis = np.array([np.cos(a), np.sin(a)])
dens = 2 * phis ** 2
E_one = 2 * (-2 * t * phis[0] * phis[1] + D / 2 * (phis[0] ** 2 - phis[1] ** 2)) + Ud / 2 * (dens ** 2).sum(axis=0)
best = dens[:, np.argmin(E_one)]
check('one orbital with two electrons, the minimum of E over normalized phi is the self-consistent solution of H_KS',
      np.abs(best - dimer(D, Ud)).max() < 1e-4, (best, dimer(D, Ud)))

D = 1e-4
lin = {}
for Uv in (0.0, 0.5, 1.0, 2.0, 4.0):
    m = dimer(D, Uv)
    lin[Uv] = (m[0] - m[1]) / (-D / (t + Uv))
check('n1 - n2 = -Delta/(t+U) to first order in Delta, so -Delta/t without U',
      all(abs(r - 1) < 1e-6 for r in lin.values()), lin)
m2, m0 = dimer(D, 2.0), dimer(D, 0.0)
third = (m2[0] - m2[1]) / (m0[0] - m0[1])
check('for U=2t the difference is a third of the one without U, 0.333', round(third, 3) == 0.333, third)
check('the site with the higher v_ext has fewer electrons', m2[0] < m2[1] and m0[0] < m0[1], (m0, m2))
m = dimer(0.1, 2.0)
check('the first order holds for Delta much smaller than t, within 0.1 percent at Delta=0.1t',
      abs((m[0] - m[1]) / (-0.1 / 3) - 1) < 1e-3, (m[0] - m[1]) / (-0.1 / 3))
sz = []
for dl in (0.05, 0.4, -1.3):
    phi = np.linalg.eigh(-t * np.array([[0, 1], [1, 0]]) + dl / 2 * np.diag([1, -1]))[1][:, 0]
    sz.append((phi[0] ** 2 - phi[1] ** 2, -(dl / 2) / np.sqrt(t ** 2 + dl ** 2 / 4)))
check('the lowest orbital of -t sigma_x + (delta/2) sigma_z has <sigma_z> = -(delta/2)/sqrt(t^2+delta^2/4)',
      all(abs(a - b) < 1e-12 for a, b in sz), sz)
D = 1e-4
m = dimer(D, 2.0)
delta = D + 2.0 * (m[0] - m[1])
check('with U the difference of potential that the electrons feel is Delta t/(t+U), a third of Delta for U=2t',
      abs(delta / (D * t / (t + 2.0)) - 1) < 1e-6, delta / D)


def error_ratios(mix, Uv=2.0, D=1e-6, steps=4):
    dstar = -D / (t + Uv)
    v, n = np.array([D / 2, -D / 2]), np.array([1 + dstar / 2 + 1e-7, 1 - dstar / 2 - 1e-7])
    errs = []
    for k in range(steps):
        phi = np.linalg.eigh(np.array([[v[0] + Uv * n[0], -t], [-t, v[1] + Uv * n[1]]]))[1][:, 0]
        n = (1 - mix) * n + mix * 2 * phi ** 2
        errs.append(n[0] - n[1] - dstar)
    errs = np.array(errs)
    return errs[1:] / errs[:-1]


plain, mixed = error_ratios(1.0), error_ratios(0.3)
check('near the solution the loop with no mixing multiplies the error by -U/t = -2 at U=2t, and with 30 percent '
      'mixing by 0.7 - 0.3 U/t = 0.1', np.allclose(plain, -2, atol=1e-4) and np.allclose(mixed, 0.1, atol=1e-4),
      (plain, mixed))

# ------------------------------------------------------------------ the quiz on v_xc
# corrected on 2026-11-22: the size is the number M of grid points, the dense diagonalization of an M x M matrix
# costs about M^3 and a local v_xc one value per point; the time of numpy grows by about 8 when M doubles
check('for M=1000 grid points M^3 is 1e9 and M is 1e3', 1000 ** 3 == 10 ** 9 and 1000 == 10 ** 3, (1000 ** 3, 1000))
check('a local v_xc(n) takes one value per grid point, M values for M points', np.tanh(np.ones(1000)).size == 1000, 1000)

# corrected on 2026-11-22, the Hohenberg-Kohn sentence: a degenerate ground state is not fixed by its density. One
# electron on a ring of 3 sites with the hopping +1 has the level -1 twice, with the two orthogonal states
# exp(+-2 pi i j/3)/sqrt3, which have the same density 1/3 on every site. First route: the eigenvalues of the matrix.
# Second route: the two states by hand and their overlap.
H3 = np.ones((3, 3)) - np.eye(3)
e3 = np.linalg.eigvalsh(H3)
ka = np.exp(2j * np.pi * np.arange(3) / 3) / np.sqrt(3)
kb = ka.conj()
check('a ring of 3 sites with the hopping +1 has a degenerate ground level -1, and its two orthogonal ground states have '
      'the same density 1/3, so the density does not fix the state', np.allclose(e3, [-1, -1, 2])
      and np.allclose(H3 @ ka, -ka) and np.allclose(H3 @ kb, -kb) and abs(np.vdot(ka, kb)) < 1e-12
      and np.allclose(np.abs(ka) ** 2, 1 / 3) and np.allclose(np.abs(kb) ** 2, 1 / 3), e3)

# ------------------------------------------------------------------ the counts of the body and of the quiz on the arrows
check('psi_0 of N electrons has 3N coordinates, and the density integrates over N-1 of them, a 3N -> 3 integral',
      all(3 * Ne - 3 * (Ne - 1) == 3 for Ne in range(1, 50)), [3 * Ne - 3 * (Ne - 1) for Ne in (1, 2, 10)])
M = 6
one = rng.normal(size=M) + 1j * rng.normal(size=M)
one /= np.linalg.norm(one)
two = rng.normal(size=(M, M)) + 1j * rng.normal(size=(M, M))
two = (two + two.T) / np.sqrt(2)
two /= np.linalg.norm(two)
ph = rng.uniform(0, 2 * np.pi, (M, M))
two_b = two * np.exp(1j * (ph + ph.T))                       # a phase phi(r1, r2), the same for both orders
dens = lambda p: 2 * (np.abs(p) ** 2).sum(axis=1)
check('on a lattice of M sites one electron is sqrt(n) up to a phase, while for N=2 the state has M^2 amplitudes, its '
      'density M values, and psi and psi exp(i phi(r1,r2)) are two states with the same n',
      np.allclose(np.abs(one), np.sqrt(np.abs(one) ** 2)) and two.size == M ** 2 and dens(two).size == M
      and np.isclose(dens(two).sum(), 2) and np.allclose(dens(two), dens(two_b))
      and abs(np.vdot(two, two_b)) < 0.9, (two.size, dens(two).size, abs(np.vdot(two, two_b))))
