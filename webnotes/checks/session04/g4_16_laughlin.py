"""Session 4, the numbers and the steps that page 16 (Sections 4.16 and 4.17, the Laughlin state and its quasiholes) quotes.
One check script per page is the rule: every number of a key box, a fold, a feedback, a caption, a solution is an assert
here or in the figure script that draws it. The figure scripts of the page assert their own numbers: laughlin_pair.py (the
maxima 2.45, 3.74 and 4.69 l_B), g4_quasihole_dimple.py (the charge 0.32 to 0.34 that a quasihole removes from the discs of
radius 5 to 8 l_B in four runs, about 0.4 at 3 l_B, the count back at zero for the whole droplet) and the three pictures
g4_quiz_density_*.py of the quiz (1 for the filled level, 1/3 for the Laughlin state, 0 at the quasihole). This script
checks the counting of the orbitals of the fold, of the problem and of the quizzes with sympy, the identity behind the quiz
on three quasiholes, the sign of the charge of a quasihole of the key box by two exact routes for m = 1, the direct integral
of |Psi|^2 that the caption of laughlin_pair names, and the sentence of the lab box in the stored source. It writes no file
and takes about 20 s."""
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
print('all checks of page 16 hold')
