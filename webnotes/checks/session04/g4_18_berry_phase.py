"""Session 4, the numbers and the steps that page 18 (Section 4.18, Berry phase, fractional charge and anyonic statistics)
quotes. One check script per page is the rule: every number of a key box, a fold, a feedback, a solution or a lab box is an
assert here, since the page has no figure script of its own (Figure 4.6 is a figure of the PDF).

The fold goes from the Berry phase of a quasihole on a loop to the charge (4.15). It uses three steps, each checked here.
The derivative of the factor prod_i (z_i - w) along the loop w = |w| e^(i theta), with sympy. The mean over the angle of
Re w/(z - w), which is -1 inside the loop and 0 outside, and which vanishes for a density that is round around w. And the
result, gamma = -2 pi <N_in>, computed with no approximation for m = 1, where the state with one quasihole is a Slater
determinant of the orbitals (z - w) z^k and the Berry phase is the phase of the product of the overlaps around the loop.
The phase there is followed continuously, so the integer part is seen too. <N_in> is the number of electrons inside the loop
for the density without the moving quasihole: the state with the quasihole has fewer inside, 2.71 against 3.125 at
|w| = 2.5 l_B, since part of its dimple lies inside the loop. With a second quasihole at the origin the phase
changes by 2 pi exactly, which is 2 pi/m for m = 1, the problem of the page. The sign of the phase
changes with the sense of the loop and, with the states of zbar of the other sign of the charge, with the charge. The braid
phase 2 pi/3 of m = 3 needs a Monte Carlo, which webnotes/checks/session04/conventions.py runs (within the noise), and the
page quotes from m = 3 only the charge that a quasihole removes from the discs of radius 5 to 8 l_B, asserted below with the
four pairs of runs of g4_quasihole_dimple.py. The lab box is checked against its stored source.
The convention of the Berry phase is that of the Zak phase (3.6), gamma = i oint <psi| d psi>, so for a discrete loop
gamma = -arg prod_j <psi_j|psi_j+1>. The script writes no file and takes about a minute."""
import os
import sys

import numpy as np
import sympy as sp

sys.dont_write_bytecode = True


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# ---------------------------------------------------------------- the steps of the fold
z = sp.symbols('z1:4')
rho, th = sp.symbols('rho theta', positive=True)
w = rho * sp.exp(sp.I * th)
prod = sp.prod([zi - w for zi in z])
rhs = prod * sum(-sp.I * w / (zi - w) for zi in z)
check('d/dtheta of prod_i (z_i - w) is the product times sum_i (-i w)/(z_i - w)', sp.simplify(sp.diff(prod, th) - rhs) == 0, 'N = 3, sympy')

wv = 3.0
ang = np.linspace(0, 2 * np.pi, 4001)[:-1]
inside = [np.mean(np.real(wv / (r * np.exp(1j * ang) - wv))) for r in (0.5, 1.5, 2.9)]
outside = [np.mean(np.real(wv / (r * np.exp(1j * ang) - wv))) for r in (3.1, 5.0, 9.0)]
check('the mean over the angle of Re w/(z - w) is -1 for |z| < |w| and 0 for |z| > |w|',
      np.allclose(inside, -1, atol=1e-6) and np.allclose(outside, 0, atol=1e-6), np.round(inside + outside, 6))
# a density that is round around w gives zero: z = w + u e^(i a), and the mean over a of w/(u e^(i a)) vanishes
uu = np.linspace(0.01, 6, 600)
dimple = sum(np.exp(-u ** 2 / 2) * np.mean(np.real(wv / (u * np.exp(1j * ang)))) * 2 * np.pi * u * (uu[1] - uu[0]) for u in uu)
check('a dimple round around w adds nothing to the mean of sum_i Re w/(z_i - w)', abs(dimple) < 1e-9, '%.1e' % dimple)
# so a uniform density n inside the loop gives -n pi |w|^2, the number of electrons inside with a minus sign
rr = (np.arange(8000) + 0.5) * 8 / 8000            # rings at the midpoints, none on the loop itself
fine = np.linspace(0, 2 * np.pi, 400001)[:-1]      # close to the loop the function is sharp in the angle
tot = sum(np.mean(np.real(wv / (r * np.exp(1j * (fine if abs(r - wv) < 0.05 else ang)) - wv))) * 2 * np.pi * r * (rr[1] - rr[0])
          for r in rr)
check('a uniform disc of radius 8 with the density 1 gives -pi |w|^2', abs(tot / (np.pi * wv ** 2) + 1) < 5e-3, round(tot / (np.pi * wv ** 2), 4))
# the mean number inside is the density 1/(2 pi m l_B^2) times pi |w|^2, which is nu times the flux in flux quanta
for m in (1, 3, 5):
    nin = 1 / (2 * np.pi * m) * np.pi * wv ** 2
    flux = wv ** 2 / 2                     # B pi |w|^2 over h/e, with 2 pi l_B^2 B = h/e
    assert abs(nin - flux / m) < 1e-12
check('<N_in> = nu Phi/Phi_0 with nu = 1/m, so the phase is 1/m of the Aharonov-Bohm phase of the charge e', True, 'm = 1, 3, 5')


# ---------------------------------------------------------------- the whole result for m = 1, with no approximation
def coeffs(wq, N, shift):
    """The orbitals (z - wq) z^(k + shift), k < N, in the orthonormal basis z^a / sqrt(2 pi 2^a a!), each one divided by a
    real constant that does not depend on wq, so that the phase of the overlaps does not change."""
    C = np.zeros((N + 1 + shift, N), complex)
    for k in range(N):
        C[k + shift, k] = -wq
        C[k + 1 + shift, k] = np.sqrt(2 * (k + 1 + shift))
    return C


def berry(radius, N=40, npts=3000, sense=1, shift=0, charge=1):
    """gamma = -sum_j arg det <psi_j|psi_j+1> on the loop w = radius e^(i sense theta), followed continuously. For
    charge=-1 the states of the lowest level are functions of zbar, so the quasihole is prod_i (zbar_i - wbar) and its
    orbitals are (zbar - wbar) zbar^k, whose coefficients in the basis zbar^a / sqrt(2 pi 2^a a!) are those of conj(w)."""
    ts = sense * np.linspace(0, 2 * np.pi, npts + 1)[:-1]
    Cs = [coeffs(radius * np.exp(1j * t) if charge > 0 else np.conj(radius * np.exp(1j * t)), N, shift) for t in ts]
    return -sum(np.angle(np.linalg.slogdet(Cs[j].conj().T @ Cs[(j + 1) % npts])[0]) for j in range(npts))


res = []
for radius in (2.5, 3.3):
    for sense in (1, -1):
        g = berry(radius, sense=sense)
        res.append((radius, sense, g / (2 * np.pi), -sense * radius ** 2 / 2))
check('m = 1, 40 electrons, the Berry phase of the loop is -2 pi times the electrons inside, |w|^2/2, and +2 pi times them '
      'for the loop taken the other way', all(abs(a[2] - a[3]) < 1e-4 for a in res),
      ', '.join('|w| = %.1f sense %+d: %.5f against %.5f' % a for a in res))

def inside_with_quasihole(radius, N=40):
    """The electrons inside |z| < |w| in the m = 1 state with the quasihole at w. The orbitals (z - w) z^k are made
    orthonormal, and the disc gives the weight P(a+1, |w|^2/2) to the basis state z^a, the probability that a Poisson
    variable of mean |w|^2/2 is at least a+1, with no weight between two different a."""
    Q, _ = np.linalg.qr(coeffs(radius + 0j, N, 0))
    x = radius ** 2 / 2
    cdf = np.cumsum([np.exp(-x + k * np.log(x) - sum(np.log(np.arange(1, k + 1)))) for k in range(N + 1)])
    return float(np.sum(np.sum(np.abs(Q) ** 2, 1) * (1 - cdf)))


nq = [inside_with_quasihole(radius) for radius in (2.5, 3.3)]
check('m = 1, the phase counts |w|^2/2, the electrons of the filled level inside the loop, 3.125 and 5.445, while the state with '
      'the quasihole at w has only 2.71 and 5.01 inside, since part of the dimple lies inside the loop',
      round(nq[0], 2) == 2.71 and round(nq[1], 2) == 5.01 and all(n < r ** 2 / 2 - 0.4 for n, r in zip(nq, (2.5, 3.3))),
      'inside with the quasihole %s, against %s' % (np.round(nq, 4), [2.5 ** 2 / 2, 3.3 ** 2 / 2]))
gm = [berry(radius, charge=-1) / (2 * np.pi) for radius in (2.5, 3.3)]
check('m = 1, for the other sign of the charge the same loop gives the opposite phase, +2 pi times the electrons inside',
      np.allclose(gm, [2.5 ** 2 / 2, 3.3 ** 2 / 2], atol=1e-4), np.round(gm, 5))
d = []
for radius in (5.0, 6.0):
    d.append((berry(radius, shift=1) - berry(radius)) / (2 * np.pi))
check('m = 1, a second quasihole at the origin changes the phase of the loop by 2 pi/m = 2 pi, so <N_in> goes down by 1/m = 1',
      np.allclose(d, 1, atol=1e-3), np.round(d, 5))

# ---------------------------------------------------------------- the numbers of the key boxes, the quizzes and the problem
check('the charge e/m and the braid phase 2 pi/m for m = 3', abs(1 / 3 - 0.3333) < 1e-4 and abs(2 * np.pi / 3 - 2.0944) < 1e-4, '1/3, 2 pi/3')
check('a full braid is two exchanges, so the exchange phase is pi/m, pi/3 for m = 3, and two exchanges of 2 pi/3 give 4 pi/3',
      abs(2 * (np.pi / 3) - 2 * np.pi / 3) < 1e-12 and abs(2 * (2 * np.pi / 3) - 4 * np.pi / 3) < 1e-12, 'pi/3, 4 pi/3')
check('m = 1 gives the braid phase 2 pi and the exchange phase pi, the factor exp(i pi) = -1 of fermions',
      abs(np.exp(1j * np.pi) + 1) < 1e-12, 'exp(i pi) = -1')
check('m = 100 gives exp(i pi/100), which is 1 within 0.04 and not -1', abs(np.exp(1j * np.pi / 100) - 1) < 0.04, np.round(np.exp(1j * np.pi / 100), 4))
for m in (3, 5, 7, 101):
    assert 0 < np.pi / m < np.pi
check('for every odd m > 1 the exchange phase pi/m is strictly between 0 and pi', True, 'm = 3, 5, 7, 101')
check('the problem, <N_in> goes down by 1/m, so the phase -2 pi <N_in> changes by 2 pi/m, 2 pi/3 for m = 3',
      abs(-2 * np.pi * (-1 / 3) - 2 * np.pi / 3) < 1e-12, '2 pi/3')
# the radius of the loop of the problem: for m = 3 and 20 electrons a quasihole at the origin removes about 1/3 of an
# electron from the discs of radius 5 to 8 l_B, 0.32 to 0.34 on average over the window in four runs, and a larger disc
# reaches the edge, where the count rises again. The four pairs of runs of g4_quasihole_dimple.py, seeds 1 to 4 without and
# 51 to 54 with the quasihole, with the helper of the figures of page 16.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'figures', 'session04'))
import _g4_laughlin_mc as mc  # noqa: E402
Rr = mc.RADII
dN = [mc.metropolis(20, 3, [], s)[2] - mc.metropolis(20, 3, [0j], s + 50)[2] for s in (1, 2, 3, 4)]
wmean = np.array([u[(Rr >= 5) & (Rr <= 8)].mean() for u in dN])
past = np.array([u[(Rr >= 8.5) & (Rr <= 10)].max() for u in dN])
check('m = 3, N = 20, the quasihole removes 0.32 to 0.34 of an electron on average over the discs of radius 5 to 8 l_B, four runs, '
      'and beyond 8 l_B the disc reaches the edge, where the count rises again above 0.39',
      round(wmean.min(), 2) == 0.32 and round(wmean.max(), 2) == 0.34 and np.all(past > 0.39),
      'window means %s, largest count for 8.5 <= R <= 10 %s' % (np.round(wmean, 3), np.round(past, 3)))

# ---------------------------------------------------------------- the lab box, against the stored source
src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'sources', 'session04',
                        'nakamura2020_arxiv2006.14115.txt'), encoding='utf-8').read()
check('the lab box: the stored abstract has the Fabry-Perot interferometer, the Aharonov-Bohm interference of the 1/3 edge mode '
      'and the phase slips with the anyonic phase 2 pi/3, which is (4.16) for m = 3',
      'electronic Fabry-Perot interferometer' in src and 'Strong Aharonov-Bohm interference of the ν=1/3 edge mode is punctuated by '
      'discrete phase slips consistent with an anyonic phase of θ anyon=2π/3' in src, '2 pi/3')
print('all checks of page 18 hold')
