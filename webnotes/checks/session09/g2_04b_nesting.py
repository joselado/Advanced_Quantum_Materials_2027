"""Session 9, the numbers that page 04b (Section 9.4b) states and that no figure script asserts.

The numbers of the redrawn map lindhard_map (2.6 at half filling, chi_0 = 0.264/t and 0.677/t, k_F = 1.03 and the plateau
inside |q| = 2k_F) are asserted in webnotes/figures/session09/lindhard_map.py, on the data of the pyqula script
webnotes/scripts/session09/g2_lindhard_square.py. The numbers of the Fermi surface quiz (k_F = 1.03, 2.09 and 1.86) are
asserted in webnotes/figures/session09/_g2_fermi.py. This script holds the rest, the steps fold, the two old quizzes, the
problem, the sentence of the lab box that is ours, the symmetry of the square that lindhard_map uses to unfold one eighth
of the zone, and the first key box, with the growth as ln(1/T) and ln^2(1/T) at half filling and the finite maximum at
mu = -t, where no saddle point sits at the Fermi level. It uses numpy only and writes no file.

Run it from anywhere:  python3 webnotes/checks/session09/g2_04b_nesting.py"""
import numpy as np
from scipy.integrate import quad


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def nF(e, mu, T):
    return 0.5 * (1 - np.tanh((e - mu) / (2 * T)))


def chi0_chain(q, mu, T, N=200000):
    """(9.4) for the chain eps = -2t cos k, t=1, on N momenta."""
    k = 2 * np.pi * (np.arange(N) + 0.5) / N
    e1, e2 = -2 * np.cos(k), -2 * np.cos(k + q)
    f1, f2 = nF(e1, mu, T), nF(e2, mu, T)
    de = e2 - e1
    small = np.abs(de) < 1e-12
    return np.where(small, f1 * (1 - f1) / T, (f1 - f2) / np.where(small, 1, de)).mean()


# ---- the steps fold: the linearized term, its value 1/(4T) at p = 0, and the integral of tanh x / x
vF, T = 1.3, 0.05
for p in (0.2, 0.01, 1e-7):
    term = (nF(-vF * p, 0, T) - nF(vF * p, 0, T)) / (2 * vF * p)
    check(f'fold: [n_F(-v_F p) - n_F(v_F p)]/(2 v_F p) = tanh(v_F p/2T)/(2 v_F p) at p={p}',
          np.isclose(term, np.tanh(vF * p / (2 * T)) / (2 * vF * p)), term)
check('fold: the term is 1/(4T) at p = 0', np.isclose(np.tanh(vF * 1e-9 / (2 * T)) / (2 * vF * 1e-9), 1 / (4 * T)), 1 / (4 * T))
consts = [quad(lambda x: np.tanh(x) / x, 0, X, limit=400)[0] - np.log(X) for X in (50., 500., 5000.)]
check('fold: the integral of tanh x / x up to X grows as ln X, plus a constant', np.ptp(consts) < 1e-6
      and abs(consts[-1] - np.log(4 * np.exp(np.euler_gamma) / np.pi)) < 1e-6, np.round(consts, 6))

# ---- the steps fold: the slope of chi_0(2k_F) against ln(1/T) is D/2 at quarter filling and D at half filling
for name, kF, factor, text in (('quarter filling', np.pi / 4, 0.5, '0.113'), ('half filling', np.pi / 2, 1.0, '0.159')):
    D = 1 / (np.pi * 2 * np.sin(kF))
    mu = -2 * np.cos(kF)
    Ts = np.array([0.02, 0.01, 0.005])
    c = np.array([chi0_chain(2 * kF, mu, T) for T in Ts])
    slope = np.polyfit(np.log(1 / Ts), c, 1)[0]
    check(f'fold: {name}, the slope of chi_0(2k_F) against ln(1/T) is {factor} D(E_F) = {text}/t', abs(slope - factor * D) < 3e-3
          and f'{factor * D:.3f}' == text, (round(slope, 4), round(factor * D, 4)))
check('fold: at k_F = pi/2 the points 3k_F and -k_F are the same point of the zone', np.isclose(np.exp(3j * np.pi / 2), np.exp(-1j * np.pi / 2)),
      '3 pi/2 = -pi/2 + 2 pi')
for T, text in ((0.02, '0.863'), (0.01, '0.974')):
    c = chi0_chain(np.pi, 0., T)
    check(f'fold: the half-filled chain has chi_0(pi) = {text}/t at T = {T}t', f'{c:.3f}' == text, c)

# ---- the first quiz: quarter filling, the maximum of chi_0(q) at q = pi/2 = 2k_F at T = 0.01t, and the energies of the feedback
qs = np.linspace(0.05, np.pi, 316)
c = np.array([chi0_chain(q, -np.sqrt(2), 0.01, N=40000) for q in qs])
check('quiz 1: at quarter filling chi_0(q) is largest at q = pi/2 = 2k_F', abs(qs[np.argmax(c)] - np.pi / 2) < 0.02, qs[np.argmax(c)])
check('quiz 1: eps(0) = -2t, the Fermi level -sqrt2 t, and eps(5 pi/4) = +sqrt2 t', np.isclose(-2 * np.cos(0), -2)
      and np.isclose(-2 * np.cos(np.pi / 4), -np.sqrt(2)) and np.isclose(-2 * np.cos(5 * np.pi / 4), np.sqrt(2)), 'ok')

# ---- the second quiz and the problem: eps(k + Q) = -eps(k) for Q = (pi, pi), at every filling
rng = np.random.default_rng(2)
k = rng.uniform(-np.pi, np.pi, (1000, 2))
eps = lambda kx, ky: -2 * (np.cos(kx) + np.cos(ky))
check('quiz 2 and problem: eps(k + Q) = -eps(k) for Q = (pi, pi)', np.allclose(eps(k[:, 0] + np.pi, k[:, 1] + np.pi), -eps(k[:, 0], k[:, 1])),
      'on 1000 random momenta')
check('quiz 2: at mu = 0.5t, Q maps the contour eps = 0.5 to eps = -0.5, another curve', np.isclose(-0.5, -(0.5)), '-0.5 != 0.5')

# ---- the problem: 1/3 of an electron per site
N = 300000
kk = 2 * np.pi * (np.arange(N) + 0.5) / N - np.pi
kF = np.pi / 3
check('problem: k_F = pi/3 holds 1/3 of the states', abs((np.abs(kk) < kF).mean() - 1 / 3) < 1e-5, (np.abs(kk) < kF).mean())
check('problem: the Fermi level is -2t cos(pi/3) = -t', np.isclose(-2 * np.cos(kF), -1), -2 * np.cos(kF))
qstar = 2 * kF
x = np.arange(12)
check('problem: q* = 2 pi/3, and cos(q* x) repeats after 3 sites', np.isclose(qstar, 2 * np.pi / 3) and np.allclose(np.cos(qstar * (x + 3)),
      np.cos(qstar * x)) and not np.allclose(np.cos(qstar * (x + 1)), np.cos(qstar * x)), 2 * np.pi / qstar)
c = np.array([chi0_chain(q, -1., 0.01, N=40000) for q in qs])
check('problem: at mu = -t the chain chi_0(q) is largest at q* = 2 pi/3', abs(qs[np.argmax(c)] - 2 * np.pi / 3) < 0.02, qs[np.argmax(c)])
# the text after the steps of 9.4b: the Peierls instability gives a charge density wave with the period pi/k_F, three
# sites at mu = -t as above, and at half filling, where chi_0(q) is largest at q = pi, two sites, the order of Section 1.13
c_half = np.array([chi0_chain(q, 0., 0.01, N=40000) for q in qs])
check('text: at half filling chi_0(q) of the chain is largest at 2k_F = pi, so the period pi/k_F is two sites',
      abs(qs[np.argmax(c_half)] - np.pi) < 0.02 and np.isclose(np.pi / (np.pi / 2), 2.0), qs[np.argmax(c_half)])
kp = np.linspace(0, 2 * np.pi, 600001)
zeros = kp[np.where(np.diff(np.sign(2 * np.cos(kp) + 1.0)))[0]] / (2 * np.pi)
check('problem: with mu = 1. of pyqula, the band 2 cos k + 1 crosses zero at 1/3 and 2/3 of 2 pi, the vector 1/3', np.allclose(zeros, [1 / 3, 2 / 3],
      atol=1e-5), zeros)

# ---- the lab box, the sentence that is ours: the continuum of the half-filled chain lies between 2t sin q and 4t sin(q/2)
k = np.linspace(-np.pi, np.pi, 200001)
for q in (0.3, np.pi / 2, 2.5):
    e1, e2 = -2 * np.cos(k), -2 * np.cos(k + q)
    ok = (e1 < 0) & (e2 > 0)
    w = e2[ok] - e1[ok]
    check(f'lab: half-filled chain, the particle-hole energies at q={q:.3f} lie between 2 sin q and 4 sin(q/2)',
          abs(w.min() - 2 * np.sin(q)) < 1e-3 and abs(w.max() - 4 * np.sin(q / 2)) < 1e-6, (round(w.min(), 4), round(w.max(), 4)))
check('lab: at q = pi/2 the continuum is from 2t to 2.83t', np.isclose(2 * np.sin(np.pi / 2), 2) and f'{4 * np.sin(np.pi / 4):.2f}' == '2.83',
      4 * np.sin(np.pi / 4))

# ---- lindhard_map: chi_0(q) of the square lattice has the symmetry of the square, which unfolds one eighth of the zone
NK, T = 120, 0.1
kk = 2 * np.pi * np.arange(NK) / NK
KX, KY = np.meshgrid(kk, kk, indexing='ij')


def chi0_square(qx, qy, mu):
    e1, e2 = eps(KX, KY) - mu, eps(KX + qx, KY + qy) - mu
    f1, f2 = nF(e1, 0, T), nF(e2, 0, T)
    de = e2 - e1
    small = np.abs(de) < 1e-12
    return np.where(small, f1 * (1 - f1) / T, (f1 - f2) / np.where(small, 1, de)).mean()


for mu in (-3.0, 0.0):
    qx, qy = 0.7, 0.3
    vals = [chi0_square(a, b, mu) for a, b in ((qx, qy), (qy, qx), (-qx, qy), (qx, -qy), (-qy, -qx), (qx + 2 * np.pi, qy))]
    check(f'lindhard_map: chi_0(q) at mu={mu} is the same at the 8 images of q under the symmetry of the square, and periodic',
          np.ptp(vals) < 1e-10, np.round(vals, 6))


# ---- the first key box: the condition of no saddle point at the Fermi level, and the half-filled square lattice
def chi0_sq(qx, qy, mu, T):
    """(9.4) of the square lattice on a midpoint mesh of max(240, 40/T) points per side, fine enough for T."""
    N = int(max(240, 40 / T))
    k = 2 * np.pi * (np.arange(N) + 0.5) / N
    KX, KY = np.meshgrid(k, k, indexing='ij')
    e1, e2 = eps(KX, KY) - mu, eps(KX + qx, KY + qy) - mu
    f1, f2 = nF(e1, 0, T), nF(e2, 0, T)
    de = e2 - e1
    small = np.abs(de) < 1e-12
    return np.where(small, f1 * (1 - f1) / T, (f1 - f2) / np.where(small, 1, de)).mean()


check('key box: at half filling the saddle points (pi,0) and (0,pi) sit at the Fermi level eps = 0',
      np.isclose(eps(np.pi, 0), 0) and np.isclose(eps(0, np.pi), 0), (eps(np.pi, 0), eps(0, np.pi)))
Ts = [0.2, 0.1, 0.05, 0.025]
c0 = np.array([chi0_sq(0, 0, 0., T) for T in Ts])
cQ = np.array([chi0_sq(np.pi, np.pi, 0., T) for T in Ts])
check('key box: at half filling chi_0(0) grows as ln(1/T), by ln2/(2 pi^2) = 0.035 for each halving of T',
      np.allclose(np.diff(c0), np.log(2) / (2 * np.pi**2), atol=1e-3), np.round(c0, 4))
check('key box: at half filling chi_0(pi,pi) grows as ln^2(1/T), second differences ln^2 2/(2 pi^2) = 0.024',
      np.allclose(np.diff(cQ, 2), np.log(2)**2 / (2 * np.pi**2), atol=1e-3) and np.all(np.diff(cQ, 2) > 0.02), np.round(cQ, 4))
# at mu = -t the largest chi_0 is not on the axis or on the diagonal but on the zone boundary, near q = (pi, 1.93). So the
# whole wedge 0 <= q_y <= q_x <= pi is scanned at T = 0.1t, and then the line (pi, q_y) around the maximum at four
# temperatures. The maximum saturates, with steps that shrink at each halving of T, while chi_0(0) at half filling
# grows by the constant 0.035, and chi_0(pi,pi) by more and more.
grid = np.linspace(0, np.pi, 13)
wedge = [(a, b) for a in grid for b in grid if b <= a + 1e-12]
vals = [chi0_sq(a, b, -1., 0.1) for a, b in wedge]
qmax = wedge[int(np.argmax(vals))]
check('key box: at mu = -t the largest chi_0 of the wedge sits on the zone boundary q_x = pi, away from the axis and the diagonal',
      abs(qmax[0] - np.pi) < 1e-12 and 0.3 < qmax[1] < np.pi - 0.3, np.round(qmax, 3))
from scipy.optimize import minimize_scalar
growth = [-minimize_scalar(lambda b: -chi0_sq(np.pi, b, -1., T), bounds=(qmax[1] - 0.5, np.pi), method='bounded',
                           options={'xatol': 1e-3}).fun for T in (0.1, 0.05, 0.025, 0.0125)]
steps = np.diff(growth)
check('key box: at mu = -t, with no saddle point at E_F and no nesting, the largest chi_0 saturates, with steps that '
      'shrink at each halving of T, while chi_0(0) at half filling grows by 0.035 each time',
      np.all(steps > 0) and steps[1] < 0.75 * steps[0] and steps[2] < 0.75 * steps[1] and steps[2] < 0.5 * np.log(2) / (2 * np.pi ** 2)
      and growth[1] / growth[0] < 1.05, (np.round(growth, 4), np.round(steps, 4)))
check('key box: at half filling chi_0(pi,pi) grows by more than 25% over the same cooling', cQ[2] / cQ[1] > 1.25, cQ[2] / cQ[1])
print('all checks of page 04b hold')
