"""Session 4, the numbers and the steps that page 16 (Sections 4.16 and 4.17, the Laughlin state and its quasiholes) quotes.
One check script per page is the rule: every number of a key box, a fold, a feedback, a caption, a solution is an assert
here or in the figure script that draws it. The figure scripts of the page assert their own numbers: laughlin_pair.py (the
maxima 2.45, 3.74 and 4.69 l_B), g4_quasihole_dimple.py (the charge 0.32 to 0.34 that a quasihole removes from the discs of
radius 5 to 8 l_B in four runs, about 0.4 at 3 l_B, the count back at zero for the whole droplet) and the three pictures
g4_quiz_density_*.py of the quiz (1 for the filled level, 1/3 for the Laughlin state, 0 at the quasihole). This script
checks the counting of the orbitals of the fold, of the problem and of the quizzes with sympy, the identity behind the quiz
on three quasiholes, the sign of the charge of a quasihole of the key box by two exact routes for m = 1, the direct integral
of |Psi|^2 that the caption of laughlin_pair names, and the sentence of the lab box in the stored source. It writes no file
and takes about 25 s.

The blocks marked "corrected on 2026-11-22" back the sentences of the old text that were corrected on that day, after
the lecturer chose to fix the errors of the old text. The block marked "decided on 2026-11-22" backs the opening
argument of Section 4.16, decided that day by the rule of the coordinator: the example is one orbital out of every
three, and the lumps come from an irregular choice of the empty orbitals, more than 20 percent away from 1/3 for the
seeds 0 to 209. The last block backs the charge e/m written as a magnitude on the page, after an independent check."""
import os

import numpy as np
import sympy as sp


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


zs = sp.symbols('z1:6')


def laughlin(N, m):
    return sp.prod([(zs[i] - zs[j]) ** m for i in range(N) for j in range(i + 1, N)])


def powers(N, m):
    """The highest and the lowest power of z1 in the expanded polynomial of (4.12)."""
    p = sp.Poly(sp.expand(laughlin(N, m)), zs[0])
    return p.degree(), min(mon[0] for mon in p.monoms())


# ---------------------------------------------------------------- the fold and the problem
d2 = powers(2, 3)
check('N = 2, m = 3: (z1 - z2)^3 has z1 to the powers 0 to 3, so 4 orbitals and the filling 2/4 = 1/2', d2 == (3, 0), d2)
d3 = powers(3, 3)
check('N = 3, m = 3: the powers of z1 go from 0 to 6, so 7 orbitals and the filling 3/7', d3 == (6, 0) and abs(3 / 7 - 0.43) < 0.005, (d3, round(3 / 7, 3)))
d4 = powers(4, 3)
check('N = 4, m = 3: the highest power is 9 = m(N-1)', d4[0] == 9, d4)
fN = {N: N / (3 * (N - 1) + 1) for N in (2, 3, 20, 10 ** 6)}
check('the filling N/(m(N-1)+1) for m = 3 is 1/2, 3/7, 20/58 = 0.345 and goes to 1/3',
      abs(fN[2] - 0.5) < 1e-12 and abs(fN[3] - 3 / 7) < 1e-12 and round(fN[20], 3) == 0.345 and abs(fN[10 ** 6] - 1 / 3) < 1e-6,
      {N: round(v, 4) for N, v in fN.items()})
dq = sp.Poly(sp.expand(laughlin(4, 3) * sp.prod(zs[:4])), zs[0]).degree()
check('the factor prod_i z_i of a quasihole at the origin raises the highest power by one, 9 to 10 for N = 4', dq == 10, dq)

# ---------------------------------------------------------------- the quizzes on the exponent
swap = lambda ex: ex.subs({zs[0]: zs[1], zs[1]: zs[0]}, simultaneous=True)
anti = {m: sp.expand(swap(laughlin(3, m)) + laughlin(3, m)) == 0 for m in (1, 3, 5)}
sym = {m: sp.expand(swap(laughlin(3, m)) - laughlin(3, m)) == 0 for m in (2, 4)}
check('odd m gives an antisymmetric state and even m a symmetric one', all(anti.values()) and all(sym.values()), (anti, sym))
d5 = powers(3, 5)
check('m = 5: the highest power of z1 is 5(N-1) = 10 for N = 3, so the filling goes to 1/5', d5[0] == 10, d5)
d4b = powers(3, 4)
check('the power 4: the highest power of z1 is 4(N-1) = 8 for N = 3, so the filling of these bosons goes to 1/4', d4b[0] == 8, d4b)
# (z1 - z2)^(1/5) when z1 goes once around z2: the phase of z1 - z2 grows by 2 pi, so the function gets exp(2 pi i/5)
t = np.linspace(0, 2 * np.pi, 2001)
ph = np.unwrap(np.angle(np.exp(1j * t)))                 # z1 - z2 = e^(i t), followed continuously
fac = np.exp(1j * (ph[-1] - ph[0]) / 5)
check('(z1 - z2)^(1/5) gets the factor exp(2 pi i/5) after one turn, so it is not single valued', abs(fac - np.exp(2j * np.pi / 5)) < 1e-9 and abs(fac - 1) > 0.5, np.round(fac, 4))
d2b = powers(3, 2)
f2 = [N / (2 * (N - 1) + 1) for N in (3, 20, 10 ** 6)]
check('the old quiz: m = 2 has the highest power 2(N-1) = 4 for N = 3, so the filling N/(2(N-1)+1) goes to 1/2, below one',
      d2b[0] == 4 and abs(f2[-1] - 0.5) < 1e-6 and all(v < 1 for v in f2), (d2b, np.round(f2, 4)))

# ---------------------------------------------------------------- the quiz on three quasiholes
# Three quasiholes at one point w = 0 are the factor prod_i z_i^3. For N = 3 this is the Laughlin state of N + 1 = 4
# electrons with the fourth one at the origin, so the three of them make the room of exactly one electron, and the highest
# power goes up by m = 3, from 6 to 9, which is the highest power of the state of 4 electrons.
three = sp.expand(laughlin(3, 3) * (zs[0] * zs[1] * zs[2]) ** 3 - laughlin(4, 3).subs(zs[3], 0))
dq3 = sp.Poly(sp.expand(laughlin(3, 3) * (zs[0] * zs[1] * zs[2]) ** 3), zs[0]).degree()
check('three quasiholes at the origin: prod_i z_i^3 Psi_3(z1, z2, z3) = Psi_3(z1, z2, z3, 0), the top power goes from 6 to 9',
      three == 0 and dq3 == 9 == powers(4, 3)[0], (three, dq3))
check('so one quasihole is a third of the charge of one electron, e/3, while e/9 would add up to e/3 and e to 3e',
      sp.Rational(1, 3) * 3 == 1 and sp.Rational(1, 9) * 3 == sp.Rational(1, 3), 'e/3')

# ---------------------------------------------------------------- the sign of the charge of a quasihole, the key box of (4.14)
# The charge is e/m in size, with the sign opposite to the charge +e of the electrons. Two routes, both for m = 1, where
# every state is exact. First, the deficit: a quasihole at the origin, prod_i z_i, moves every orbital z^k to z^(k+1), so
# the disc of radius R holds sum_k P(k+1, R^2/2) - P(k+2, R^2/2) = P(1, R^2/2) - P(N+1, R^2/2) electrons less, with P the
# regularized lower incomplete gamma, which is 1 - exp(-R^2/2) in the bulk, a positive count of missing electrons.
def poisson_cdf_upper(k, x):
    """P(k, x) for an integer k, the probability that a Poisson variable of mean x is at least k."""
    return 1 - sum(np.exp(-x) * x ** j / float(sp.factorial(j)) for j in range(k))


Nq = 40
deficit = [poisson_cdf_upper(1, R ** 2 / 2) - poisson_cdf_upper(Nq + 1, R ** 2 / 2) for R in (2.0, 3.0, 5.0)]
check('m = 1, a quasihole at the origin leaves 1 - exp(-R^2/2) electrons less in the disc of radius R, positive and 1 in the bulk',
      np.allclose(deficit, [1 - np.exp(-R ** 2 / 2) for R in (2.0, 3.0, 5.0)], atol=1e-9) and min(deficit) > 0, np.round(deficit, 5))


# Second, the Berry phase on the same counterclockwise loop. One electron of charge +e in the lowest level, the coherent
# state at w with the coefficients exp(-|w|^2/4) conj(w)^a / sqrt(2^a a!) in the basis z^a/sqrt(2 pi 2^a a!), gets
# +|w|^2/2 in units of 2 pi, the flux inside in flux quanta. The quasihole of m = 1, the Slater determinant of the orbitals
# (z - w) z^k of g4_18_berry_phase.py, gets -|w|^2/2. The convention is that of (3.6), gamma = -sum_j arg <psi_j|psi_j+1>.
def loop_phase(states):
    n = len(states)
    return -sum(np.angle(np.linalg.slogdet(np.atleast_2d(states[j].conj().T @ states[(j + 1) % n]))[0]) for j in range(n))


wv, npts = 2.5, 1200
ts = np.linspace(0, 2 * np.pi, npts + 1)[:-1]
a = np.arange(120)
lf = np.array([float(sp.log(sp.factorial(int(k)))) for k in a])
coh = []
for t in ts:
    c = np.exp(a * np.log(np.conj(wv * np.exp(1j * t)) + 0j) - 0.5 * (a * np.log(2) + lf) - wv ** 2 / 4)
    coh.append((c / np.linalg.norm(c))[:, None])
qh = []
for t in ts:
    C = np.zeros((Nq + 1, Nq), complex)
    for k in range(Nq):
        C[k, k] = -wv * np.exp(1j * t)
        C[k + 1, k] = np.sqrt(2 * (k + 1))
    qh.append(C)
g_e, g_qh = loop_phase(coh) / (2 * np.pi), loop_phase(qh) / (2 * np.pi)
check('on the same counterclockwise loop of radius 2.5 l_B one electron of charge +e gets +|w|^2/2 = 3.125 and the quasihole '
      'of m = 1 gets -3.125, so the charge of the quasihole has the opposite sign',
      abs(g_e - wv ** 2 / 2) < 1e-4 and abs(g_qh + wv ** 2 / 2) < 1e-4, (round(g_e, 5), round(g_qh, 5)))

# ---------------------------------------------------------------- the caption of laughlin_pair, a direct integral of |Psi|^2
# The caption says that the distribution r^(2m+1) exp(-r^2/4) was checked against a direct integral of |Psi|^2. Here
# |Psi(z1, z2)|^2 = |z1 - z2|^(2m) exp(-(|z1|^2 + |z2|^2)/2) is summed on a grid of the four coordinates x1, y1, x2, y2, with
# no change of variables, and its moments in r = |z1 - z2| are compared with those of the formula. The second moment is
# 4(m+1) with the factor r of the measure, and it would be 4(m+1/2) without it. The largest weight on bins of 0.5 l_B is in
# the bin of the maximum sqrt(2(2m+1)).
g4 = np.linspace(-9, 9, 61)
X2, Y2 = np.meshgrid(g4, g4, indexing='ij')
zb2 = (X2 + 1j * Y2).ravel()
bins = np.arange(0, 12.01, 0.5)
rr = np.linspace(0, 40, 400001)
pair = {}
for m in (1, 3, 5):
    tot = m1 = m2 = 0.0
    hist = np.zeros(len(bins) - 1)
    for x1 in g4:
        za = x1 + 1j * g4
        dd = np.abs(za[:, None] - zb2[None, :])
        ww = dd ** (2 * m) * np.exp(-(np.abs(za[:, None]) ** 2 + np.abs(zb2[None, :]) ** 2) / 2)
        tot += ww.sum(); m1 += (ww * dd).sum(); m2 += (ww * dd ** 2).sum()
        hist += np.histogram(dd.ravel(), bins, weights=ww.ravel())[0]
    Pm = rr ** (2 * m + 1) * np.exp(-rr ** 2 / 4) / (2 * 4 ** m * float(sp.factorial(m)))
    top = np.argmax(hist)
    pair[m] = (m1 / tot, np.trapezoid(rr * Pm, rr), m2 / tot, bins[top] <= np.sqrt(2 * (2 * m + 1)) < bins[top + 1])
check('laughlin_pair: the grid sum of |Psi|^2 over x1, y1, x2, y2 gives the mean distance and the second moment 4(m+1) of '
      'r^(2m+1) exp(-r^2/4), and its largest bin holds sqrt(2(2m+1)), for m = 1, 3, 5',
      all(abs(v[0] / v[1] - 1) < 1e-3 and abs(v[2] - 4 * (m + 1)) < 1e-2 and v[3] for m, v in pair.items()),
      {m: (round(v[0], 4), round(v[1], 4), round(v[2], 4), v[3]) for m, v in pair.items()})

# ---------------------------------------------------------------- the lab box of Section 4.17, against the stored source
src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'sources', 'session04',
                        'saminadayar1997_arxivcond-mat-9706307.txt'), encoding='utf-8').read()
check('the lab box: the stored abstract measures the shot noise of tunneling at the filling 1/3 and finds e*=e/3, which is e/m for m = 3',
      'shot noise associated with tunneling in the fractional quantum Hall regime at Landau level filling factor 1/3' in src
      and 'which is found to be e*=e/3' in src and '2-D electron system in high magnetic field' in src, 'e*=e/3')

# ---------------------------------------------------------------- the old text of Section 4.16, corrected on 2026-11-22
# "the exact ground state of a strongly interacting many-body problem" became "an exact ground state of a repulsion of
# very short range", the densest of its states of zero energy, which for m = 3 and at the same total angular momentum
# 3N(N-1)/2 in units of hbar is very close to the Coulomb ground state, with the overlap 0.99 for three electrons and 0.98
# for four on a disc. We diagonalize N electrons in the lowest level at a fixed total angular momentum L, with the
# pseudopotentials V_m of the two-body interaction: V_1 = 1 and the others zero for the short-range repulsion, and
# V_m = Gamma(m + 1/2)/(2 m!) in units of e^2/(eps l_B) for the Coulomb one. On a disc with no confinement the Coulomb
# energy keeps falling with L, so the comparison is made only at the L of the Laughlin state.
import itertools  # noqa: E402
from math import factorial, gamma, lgamma, sqrt  # noqa: E402
from scipy.integrate import quad  # noqa: E402
from scipy.special import gammainc  # noqa: E402

coulomb = lambda mm: gamma(mm + 0.5) / (2 * factorial(mm))
vm_int = [quad(lambda u, mm=mm: u ** mm * np.exp(-u) / factorial(mm) / np.sqrt(4 * u), 0, np.inf)[0] for mm in range(6)]
check('the Coulomb pseudopotentials Gamma(m + 1/2)/(2 m!) agree with the integral of 1/|z1 - z2| over the relative orbital',
      np.allclose(vm_int, [coulomb(mm) for mm in range(6)], atol=1e-9), np.round(vm_int, 6))
Rs, rs = sp.symbols('R r')


_pair_transform = {}


def pair_matrix(L, V):
    """The two-body interaction on the pairs (a, L - a): <M, m|a, b> from (R + r)^a (R - r)^b with R, r = (z1 +- z2)/sqrt 2.
    The transform depends only on L, so it is kept once computed."""
    if L not in _pair_transform:
        U = np.zeros((L + 1, L + 1))
        for a in range(L + 1):
            poly = sp.Poly(sp.expand((Rs + rs) ** a * (Rs - rs) ** (L - a)), Rs, rs)
            for (M, mm), c in zip(poly.monoms(), poly.coeffs()):
                U[a, mm] = float(c) * sqrt(factorial(M) * factorial(mm) / (factorial(a) * factorial(L - a))) / 2 ** (L / 2)
        assert np.allclose(U @ U.T, np.eye(L + 1))
        _pair_transform[L] = U
    U = _pair_transform[L]
    return U @ np.diag([V(mm) for mm in range(L + 1)]) @ U.T


def slater_hamiltonian(N, Ltot, V):
    """sum_{i<j} V(z_i - z_j) on the Slater determinants of N orbitals with the total angular momentum Ltot. Two occupied
    orbitals c and d of such a determinant have c + d <= Ltot, so the pairs up to Ltot are enough."""
    pm = {L: pair_matrix(L, V) for L in range(Ltot + 1)}
    basis = [s for s in itertools.combinations(range(Ltot + 1), N) if sum(s) == Ltot]
    idx = {s: i for i, s in enumerate(basis)}
    Hs = np.zeros((len(basis), len(basis)))
    for j, s in enumerate(basis):
        for c, d in itertools.combinations(s, 2):
            for a in range(c + d + 1):
                b = c + d - a
                if a == b or b > Ltot or a > Ltot:
                    continue
                st, sign = list(s), 1
                for op in (c, d):                        # c_d c_c, then c+_b c+_a, with the signs of the ordering
                    k = st.index(op); sign *= (-1) ** k; st.pop(k)
                if a in st or b in st:
                    continue
                for op in (b, a):
                    k = sum(1 for o in st if o < op); sign *= (-1) ** k; st.insert(k, op)
                Hs[idx[tuple(st)], j] += 0.5 * sign * (pm[c + d][a, c] - pm[c + d][a, d])
    return basis, Hs


def state_vector(poly_expr, N, basis):
    """The amplitudes of an antisymmetric polynomial times the Gaussian on the normalized Slater determinants."""
    P = sp.Poly(sp.expand(poly_expr), *zs[:N])
    coef = dict(zip(P.monoms(), P.coeffs()))
    v = np.array([float(coef.get(tuple(reversed(s)), 0)) * np.prod([sqrt(2.0 ** k * factorial(k)) for k in s]) for s in basis])
    return v / np.linalg.norm(v)


v1_only = lambda mm: 1.0 if mm == 1 else 0.0
ed = {}
for N in (3, 4):
    Ltot = 3 * N * (N - 1) // 2
    psi_expr = sp.prod([(zs[i] - zs[j]) ** 3 for i in range(N) for j in range(i + 1, N)])
    assert sp.Poly(sp.expand(psi_expr), *zs[:N]).total_degree() == Ltot   # the L of the Laughlin state is 3N(N-1)/2
    for name, V in (('V1', v1_only), ('Coulomb', coulomb)):
        basis, Hs = slater_hamiltonian(N, Ltot, V)
        w, U = np.linalg.eigh(Hs)
        psi = state_vector(psi_expr, N, basis)
        ed[(N, name)] = (w[0], w[1], float(psi @ Hs @ psi), abs(float(U[:, 0] @ psi)))
check('the Laughlin state with m = 3 is the exact zero-energy ground state of V_1 for 3 and 4 electrons, with a gap above it',
      all(abs(ed[(N, 'V1')][0]) < 1e-10 and abs(ed[(N, 'V1')][2]) < 1e-10 and ed[(N, 'V1')][1] > 0.4
          and abs(ed[(N, 'V1')][3] - 1) < 1e-10 for N in (3, 4)), {N: np.round(ed[(N, 'V1')], 4) for N in (3, 4)})
check('for the Coulomb repulsion its overlap with the ground state is 0.99 for 3 electrons and 0.98 for 4, and not 1',
      round(ed[(3, 'Coulomb')][3], 2) == 0.99 and round(ed[(4, 'Coulomb')][3], 2) == 0.98
      and all(ed[(N, 'Coulomb')][3] < 0.995 and ed[(N, 'Coulomb')][2] > ed[(N, 'Coulomb')][0] + 1e-4 for N in (3, 4)),
      {N: np.round(ed[(N, 'Coulomb')], 6) for N in (3, 4)})
# "the densest of its states of zero energy": V_1 has no negative eigenvalue, so its states of zero energy are its ground
# states. Below L = 3N(N-1)/2, where the electrons sit closer to the center, it has none, at that L it has one, the Laughlin
# state above, and above that L it has more, 1, 1, 2, 3 for three electrons at L = 9 to 12, the Laughlin state with
# quasiholes.
zero_modes, lowest = {}, {}
for N, Lmax in ((3, 12), (4, 18)):
    for L in range(N * (N - 1) // 2, Lmax + 1):
        w = np.linalg.eigvalsh(slater_hamiltonian(N, L, v1_only)[1])
        zero_modes[(N, L)], lowest[(N, L)] = int(np.sum(np.abs(w) < 1e-9)), w[0]
check('V_1 alone: no negative energy, no state of zero energy below L = 3N(N-1)/2 = 9 and 18, one at it, and 1, 1, 2, 3 '
      'for three electrons at L = 9 to 12',
      min(lowest.values()) > -1e-9 and all(zero_modes[(N, L)] == 0 and lowest[(N, L)] > 0.05 for (N, L) in zero_modes
                                            if L < 3 * N * (N - 1) // 2)
      and zero_modes[(4, 18)] == 1 and [zero_modes[(3, L)] for L in range(9, 13)] == [1, 1, 2, 3],
      ({k: v for k, v in zero_modes.items() if v}, round(min(v for (N, L), v in lowest.items() if L < 3 * N * (N - 1) // 2), 4)))
# second route for three electrons: the full space of three distinguishable particles in 10 orbitals, the interaction on
# every pair, projected on the antisymmetric states, which does not use the signs of the Slater determinants above
n10 = 10
V2 = np.zeros((n10 * n10, n10 * n10))
for L in range(n10):
    pmL = pair_matrix(L, coulomb)
    for a in range(L + 1):
        for c in range(L + 1):
            V2[a * n10 + (L - a), c * n10 + (L - c)] = pmL[a, c]
perm = {}
for name, order in (('12', (1, 0, 2)), ('23', (0, 2, 1))):
    Pm = np.zeros((n10 ** 3, n10 ** 3))
    for t3 in itertools.product(range(n10), repeat=3):
        src = t3[0] * n10 * n10 + t3[1] * n10 + t3[2]
        dst = t3[order[0]] * n10 * n10 + t3[order[1]] * n10 + t3[order[2]]
        Pm[dst, src] = 1
    perm[name] = Pm
H12 = np.kron(V2, np.eye(n10))
H13 = perm['23'] @ H12 @ perm['23']
Hfull = H12 + H13 + perm['12'] @ H13 @ perm['12']
basis3 = [s for s in itertools.combinations(range(10), 3) if sum(s) == 9]
Q = np.zeros((n10 ** 3, len(basis3)))
for j, s in enumerate(basis3):
    for p in itertools.permutations(range(3)):
        sgn = round(np.linalg.det(np.eye(3)[list(p)]))
        Q[s[p[0]] * n10 * n10 + s[p[1]] * n10 + s[p[2]], j] += sgn / sqrt(6)
w3, U3 = np.linalg.eigh(Q.T @ Hfull @ Q)
psi3 = state_vector(sp.prod([(zs[i] - zs[j]) ** 3 for i in range(3) for j in range(i + 1, 3)]), 3, basis3)
check('second route, three electrons in the full product space: the same Coulomb ground energy and the overlap 0.99',
      abs(w3[0] - ed[(3, 'Coulomb')][0]) < 1e-10 and abs(abs(U3[:, 0] @ psi3) - ed[(3, 'Coulomb')][3]) < 1e-10,
      (round(w3[0], 6), round(abs(U3[:, 0] @ psi3), 6)))

# "an excitation with the opposite fractional charge, which has the sign of the charge of the electrons", corrected on
# 2026-11-22 from "the opposite, negative, fractional charge": for N = 4 and m = 3 the quasielectron prod_i d/dz_i Psi_3
# holds more electrons near the origin than Psi_3, and the quasihole prod_i z_i Psi_3 fewer. Two routes: the number of
# electrons in a disc of radius R from the occupations of the orbitals, and the total angular momentum, 18 - 4 and 18 + 4.
N, Ltot = 4, 18
psi_expr = sp.prod([(zs[i] - zs[j]) ** 3 for i in range(N) for j in range(i + 1, N)])
qe_expr = psi_expr
for i in range(N):
    qe_expr = sp.diff(qe_expr, zs[i])
qh_expr = sp.prod(zs[:N]) * psi_expr
inside = {}
for name, expr, L in (('Laughlin', psi_expr, Ltot), ('quasielectron', qe_expr, Ltot - N), ('quasihole', qh_expr, Ltot + N)):
    basis = [s for s in itertools.combinations(range(L + 1), N) if sum(s) == L]
    v = state_vector(expr, N, basis)
    occ = np.zeros(L + 1)
    for amp, s in zip(v, basis):
        occ[list(s)] += amp ** 2
    inside[name] = (round(float(occ @ np.arange(L + 1)), 6), [float(occ @ gammainc(np.arange(L + 1) + 1, R ** 2 / 2)) for R in (1.5, 2.0, 2.5)])
check('the quasielectron puts more electrons in the discs of radius 1.5, 2 and 2.5 l_B around the origin and the quasihole '
      'fewer, with the total angular momentum 14 and 22 against 18',
      inside['Laughlin'][0] == 18 and inside['quasielectron'][0] == 14 and inside['quasihole'][0] == 22
      and all(qe > la > qh for qe, la, qh in zip(inside['quasielectron'][1], inside['Laughlin'][1], inside['quasihole'][1])),
      {k: (v[0], np.round(v[1], 4).tolist()) for k, v in inside.items()})

# ---------------------------------------------------------------- the opening argument of Section 4.16, decided on 2026-11-22
# "for example one out of every three", and "if we leave the orbitals empty in an irregular way, we obtain a density
# that is clearly not uniform and has lumps". The density of a Slater determinant of the orbitals S, times 2 pi l_B^2, is
# the sum over S of u^m e^-u/m! with u = r^2/2 l_B^2. Every third orbital, m = 0, 3, ..., 57 for 20 electrons, is flat at
# 1/3 within 3 percent between 2 l_B and 2 l_B inside the edge, and irregular choices of 20 of the orbitals 0 to 57, each
# with the orbital 57, deviate there from 1/3 by more than 20 percent. An independent check showed that the upper end
# depends on the seeds: 24.0 to 185.2 percent for the seeds 0 to 209, 22 of them above 100 percent, while ten seeds gave
# 26.8 to 99.9 percent. The minimum falls slowly with more seeds, to 19.5 percent over 1000, so the assert is on the
# seeds 0 to 209 and only on the lower bound, which is what "lumps" needs.
def slater_density(S, r):
    u = r ** 2 / 2
    return sum(np.exp(m * np.log(u) - u - lgamma(m + 1)) for m in S)


rr = np.linspace(0.01, 12, 4800)
bulk = (rr > 2) & (rr < np.sqrt(2 * 57) - 2)
third = slater_density(range(0, 58, 3), rr)[bulk]
devs = []
for seed in range(210):
    S = np.sort(np.append(np.random.default_rng(seed).choice(57, 19, replace=False), 57))
    dd = slater_density(S, rr)[bulk]
    devs.append(np.abs(3 * dd - 1).max())
check('decided on 2026-11-22: every third orbital gives 0.324 to 0.333 between 2 l_B and 2 l_B inside the edge, and the '
      '210 irregular choices of 20 of the orbitals 0 to 57 with the seeds 0 to 209 all deviate there from 1/3 by more than '
      '20 percent, which are the lumps',
      len(range(0, 58, 3)) == 20 and 0.324 < third.min() and third.max() < 0.3334 and np.abs(3 * third - 1).max() < 0.03
      and len(devs) == 210 and min(devs) > 0.2,
      (round(third.min(), 4), round(third.max(), 4), 'range %.3f to %.3f, %d above 1' % (min(devs), max(devs), sum(d > 1 for d in devs))))
check('decided on 2026-11-22: one out of every three orbitals is the filling 1/m = 1/3 of the state of the page, 20 electrons in '
      'the 58 orbitals 0 to 57, the count of the fold', 20 / 58 == 20 / (3 * 19 + 1) and abs(20 / 58 - 0.345) < 5e-4, round(20 / 58, 4))
# ---------------------------------------------------------------- the charge e/m as a magnitude, decided on 2026-11-22
# After an independent check the opener, the caption of the quasihole dimple, the first quiz of Section 4.17 and the
# comesback box give e/m as the magnitude of the charge, as the key box of (4.14) does, since the deficit above makes it
# -e/m for the charge +e. The lab box keeps "the charge e/m of a quasihole", since its electron system has the charge -e.
page16 = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'pages', 'session04',
                           '16-fractional-filling-and-the-laughlin-wavefunction.md'), encoding='utf-8').read()
check('decided on 2026-11-22: page 16 writes the charge e/m of a quasihole as a magnitude, and the deficit is positive',
      'carry a charge of magnitude $e/m$' in page16 and 'What is the magnitude of the charge of one quasihole?' in page16
      and 'so each one removes $e/3$' in page16 and 'confirms that the charge of the quasihole has the magnitude $e/m$' in page16
      and 'its height is the magnitude of the charge of the quasihole' in page16 and 'carry the charge $e/m$' not in page16
      and min(deficit) > 0, True)
print('all checks of page 16 hold')
