"""Session 9, the numbers and the statements that page 02 (Section 9.2) quotes, in the steps fold, the caption of
curie_weiss, the three quizzes, the problem and the lab box.

The model is the mean-field Ising magnet of the steps fold, E = -J sum_<ij> s_i s_j - h sum_i s_i with J > 0 for a
ferromagnet, k_B = 1, and h and T in the same unit, so that a free spin has chi = 1/T. The figure scripts solve the
mean-field equations by iteration (webnotes/figures/session09/_g1_curie.py). Here they are solved by a root finder on
the nonlinear equations at a finite small field, which is a second route, and compared with the closed forms of the
steps, 1/chi = T, T - zJ, T + z|J| and the staggered T - z|J|. The exact T_c = 2.27 J of the square-lattice Ising
model is the self-dual point of Kramers and Wannier, found here by a root finder, and compared with 2/ln(1+sqrt 2).
Beyond mean field, the exact Ising model on a 4 x 4 torus, by enumeration of all its states, checks that far above T_c
the line 1/chi still extrapolates to zero at T = zJ, and that close to |theta| it bends, as the fold and the solution
of the problem say.

The lab box quotes -300 K and 50 mK from the stored abstract of arXiv:cond-mat/0610539, and this script finds both in
one sentence of the stored file webnotes/sources/session09/helton2007_arxivcond-mat-0610539.txt, with the kagome
lattice and the spin 1/2 of the box. The name herbertsmithite is not in the stored text, so the box does not give it.

It needs numpy and scipy, and writes no file.

Run it from anywhere:  python3 webnotes/checks/session09/g1_02_the_response_of_a_classical_magnet_as_a_first_example.py"""
import json, os, re, sys, warnings
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq, fsolve

WEBNOTES = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def inv_chi(T, zJ, staggered=False, h=1e-6):
    """1/chi of the two-sublattice mean field, from the roots of m_A = tanh((h_A + zJ m_B)/T) and the same for B."""
    hA, hB = h, (-h if staggered else h)
    # the unknowns are u = m/h, of order one, so that the root finder works at a small field
    eqs = lambda u: [u[0] - np.tanh((hA + zJ * h * u[1]) / T) / h, u[1] - np.tanh((hB + zJ * h * u[0]) / T) / h]
    with warnings.catch_warnings():      # fsolve warns when its first guess is already the root, the assert below decides
        warnings.simplefilter('ignore', RuntimeWarning)
        uA, uB = fsolve(eqs, [1 / T, (hB / h) / T], xtol=1e-13)
    assert np.allclose(eqs([uA, uB]), 0, atol=1e-9)
    return float(1 / ((uA - uB) / 2 if staggered else (uA + uB) / 2))


# ---------------------------------------------------------------------------------------------------------------
# the steps fold and (9.1), with zJ = T_c = 1
Ts = [1.1, 1.25, 1.5, 2.0, 2.5, 3.0, 5.0]
rows = [(T, inv_chi(T, 0.0), inv_chi(T, 1.0), inv_chi(T, -1.0), inv_chi(T, -1.0, staggered=True)) for T in Ts]
check('steps, 1/chi = T, T - T_c and T + T_c for the paramagnet, the ferromagnet and the antiferromagnet',
      all(abs(p - T) < 1e-6 and abs(f - (T - 1)) < 1e-6 and abs(a - (T + 1)) < 1e-6 for T, p, f, a, s in rows),
      [(T, round(p, 5), round(f, 5), round(a, 5)) for T, p, f, a, s in rows[:3]])
check('steps, the staggered response of the antiferromagnet is 1/(T - T_c), so it orders at T_c',
      all(abs(s - (T - 1)) < 1e-6 for T, p, f, a, s in rows), [(T, round(s, 5)) for T, p, f, a, s in rows[:3]])
check('steps, a free spin m = tanh(h/T), chi = 1/T at small h', abs(np.tanh(1e-6 / 0.7) / 1e-6 - 1 / 0.7) < 1e-9, 1 / 0.7)

# the paragraph after the figure: in mean field the exchange field of the neighbors, zJm, has the sign of a small uniform
# field h for the ferromagnet and the opposite sign for the antiferromagnet, at T = 1.5 T_c and 3 T_c, with zJ = +-T_c = +-1
h_ = 1e-6
ex = [(T, 1.0 * h_ / inv_chi(T, 1.0, h=h_) / h_, -1.0 * h_ / inv_chi(T, -1.0, h=h_) / h_) for T in (1.5, 3.0)]
check('text, the exchange field zJm reinforces a uniform field for the ferromagnet and opposes it for the antiferromagnet',
      all(f > 0 and a < 0 for T, f, a in ex) and abs(ex[0][1] - 2.0) < 1e-5 and abs(ex[0][2] + 0.4) < 1e-5,
      [(T, round(f, 5), round(a, 5)) for T, f, a in ex])

# the exact T_c of the square-lattice Ising model, by two routes, against zJ = 4J of mean field
Kc = brentq(lambda K: np.exp(-2 * K) - np.tanh(K), 0.1, 1.0)        # the self-dual point tanh K = e^{-2K}
Tc_exact = 1 / Kc
check('steps, the exact T_c of the square lattice is 2.27 J, below the 4 J of mean field',
      abs(Tc_exact - 2 / np.log(1 + np.sqrt(2))) < 1e-9 and round(Tc_exact, 2) == 2.27 and 4 * 1.0 > Tc_exact,
      round(Tc_exact, 5))

# beyond mean field: the exact Ising model on a 4 x 4 torus, all 2^16 states, chi = <M^2>/(N T) at h = 0. The high
# temperature series 1/chi = T - zJ + zJ^2/T + ... is the same as on the infinite square lattice up to the loops of
# length 4 that wind around the torus, so its intercept and its 1/T term are those of the infinite lattice.
LT = 4
spins = (((np.arange(2 ** (LT * LT))[:, None] >> np.arange(LT * LT)) & 1) * 2 - 1).reshape(-1, LT, LT)
bond_sum = ((spins * np.roll(spins, 1, axis=1)).sum(axis=(1, 2)) + (spins * np.roll(spins, 1, axis=2)).sum(axis=(1, 2)))
mag2 = spins.sum(axis=(1, 2)).astype(float) ** 2


def inv_chi_exact(T, J):
    x = J * bond_sum / T
    w = np.exp(x - x.max())
    return float(1 / ((w * mag2).sum() / w.sum() / (LT * LT * T)))


fits = {}
for Jx in (1.0, -1.0):
    TT = np.linspace(20, 160, 15)
    a, b, c = np.linalg.lstsq(np.vstack([TT, np.ones_like(TT), 1 / TT]).T, [inv_chi_exact(T, Jx) for T in TT], rcond=None)[0]
    fits[Jx] = (round(float(a), 5), round(float(-b), 4), round((inv_chi_exact(160.0, Jx) - 160 + 4 * Jx) * 160 / Jx ** 2, 3))
check('steps, far above T_c the line 1/chi of the exact model extrapolates to zero at T = zJ, with z = 4 and J = +-1',
      all(abs(fits[Jx][0] - 1) < 1e-3 and abs(fits[Jx][1] - 4 * Jx) < 0.01 and abs(fits[Jx][2] - 4) < 0.05 for Jx in fits),
      'slope, intercept and the coefficient of J^2/T: %s' % fits)

# the caption of curie_weiss: the dots at 1.5, 2, 2.5 and 3 T_c fall on the lines
dots = [(T, inv_chi(T, 0.0), inv_chi(T, 1.0), inv_chi(T, -1.0)) for T in (1.5, 2.0, 2.5, 3.0)]
check('caption of curie_weiss, the dots at 1.5, 2, 2.5 and 3 T_c are on the lines',
      all(abs(p - T) < 1e-6 and abs(f - T + 1) < 1e-6 and abs(a - T - 1) < 1e-6 for T, p, f, a in dots), 'ok')

# ---------------------------------------------------------------------------------------------------------------
# quiz 1: the line T + 30 against the paramagnet, in kelvin with C = 1
check('quiz 1, the measured line gives 90 at 60 K and the paramagnet 60', round(inv_chi(60.0, -30.0), 6) == 90
      and round(inv_chi(60.0, 0.0), 6) == 60, (round(inv_chi(60.0, -30.0), 6), round(inv_chi(60.0, 0.0), 6)))
check('quiz 1, a ferromagnet with T_c = 30 K has 1/chi = T - 30, zero at 30 K',
      all(abs(inv_chi(T, 30.0) - (T - 30)) < 1e-5 for T in (40.0, 60.0, 90.0)), 'ok')
check('quiz 1, the exchange only makes the uniform chi smaller than the chi = 1/T of a free spin, 1/chi = T + 30 K',
      all(inv_chi(T, -30.0) > T and abs(inv_chi(T, -30.0) - T - 30) < 1e-5 for T in (40.0, 60.0, 90.0, 120.0)), 'ok')

# quiz 2: the intercepts of the three lines, from a fit of the mean field at 60, 90 and 120 K
icpt = {}
for theta in (30.0, 0.0, -30.0):
    TT = np.array([60.0, 90.0, 120.0])
    slope, c = np.polyfit(TT, [inv_chi(T, theta) for T in TT], 1)
    icpt[theta] = (round(float(slope), 6), round(float(-c / slope), 4) + 0.0)
check('quiz 2, the three lines have the slope one and the intercepts 30, 0 and -30 K',
      all(icpt[th] == (1.0, th) or (icpt[th][0] == 1.0 and abs(icpt[th][1] - th) < 1e-4) for th in icpt), icpt)

# quiz 3: the numbers of the feedback
r15 = [round(inv_chi(1.5, s), 3) for s in (1.0, -1.0)]
r3 = [round(inv_chi(3.0, s), 3) for s in (0.0, 1.0, -1.0)]
check('quiz 3, at 1.5 T_c the ferromagnet has 1/chi = 0.5 T_c and the antiferromagnet 2.5 T_c', r15 == [0.5, 2.5], r15)
check('quiz 3, at 3 T_c the free spin has 3 T_c and the antiferromagnet 4 T_c', r3[0] == 3.0 and r3[2] == 4.0, r3)

# ---------------------------------------------------------------------------------------------------------------
# the problem: the line through (60 K, 90) and (90 K, 120)
invC = (120 - 90) / (90 - 60)
C = 1 / invC
theta = 60 - C * 90
J = abs(theta) / 4
check('problem, C = 1, theta = -30 K, |J| = 7.5 K for z = 4', C == 1 and theta == -30 and J == 7.5, (C, theta, J))
check('problem, the mean field with z|J| = 30 K goes through the two points',
      abs(inv_chi(60.0, -4 * J) - 90) < 1e-5 and abs(inv_chi(90.0, -4 * J) - 120) < 1e-5, 'ok')
check('problem, mean field puts the order at 30 K and the exact Ising model at 2.27 |J| = 17 K',
      4 * J == 30 and round(Tc_exact * J) == 17, round(Tc_exact * J, 3))


def theta_from(T1, T2, Jx):
    y1, y2 = inv_chi_exact(T1, Jx), inv_chi_exact(T2, Jx)
    Cx = (T2 - T1) / (y2 - y1)
    return T1 - Cx * y1


bend = [round(inv_chi_exact(T, -J) - T - 4 * J, 3) for T in (60.0, 90.0, 600.0)]
th_near, th_far = theta_from(60.0, 90.0, -J), theta_from(600.0, 900.0, -J)
check('problem, for |J| = 7.5 K the exact line bends near |theta|, and two points far above |theta| give theta = -30 K',
      bend[0] > bend[1] > bend[2] > 0 and abs(th_near + 30) > 6 and abs(th_far + 30) < 1,
      'exact 1/chi - T - 30 K at 60, 90, 600 K %s; theta from 60 and 90 K %.2f, from 600 and 900 K %.2f'
      % (bend, th_near, th_far))

# ---------------------------------------------------------------------------------------------------------------
# the lab box: the numbers are in one sentence of the stored abstract
src = os.path.join(WEBNOTES, 'sources', 'session09', 'helton2007_arxivcond-mat-0610539.txt')
text = open(src, encoding='utf-8').read()
abstract = text.split('[abstract', 1)[1]
sentence = [s for s in re.split(r'(?<=\.)\s', abstract) if '-300 K' in s]
check('lab, -300 K and 50 mK in one sentence of the stored abstract', len(sentence) == 1 and '50 mK' in sentence[0]
      and 'Curie-Weiss temperature' in sentence[0] and 'no magnetic order' in sentence[0], sentence[0] if sentence else None)
check('lab, the abstract names the S=1/2 kagome lattice antiferromagnet ZnCu3(OH)6Cl2',
      'S=1/2 kagome lattice antiferromagnet' in abstract and 'Cu_3 (OH)_6 Cl_2' in abstract
      and 'herbertsmithite' not in text.lower(), 'ok, and the name herbertsmithite is not in the stored text')
index = json.load(open(os.path.join(WEBNOTES, 'sources', 'index.json'), encoding='utf-8'))
check('lab, the link of the box is stored', index.get('https://arxiv.org/abs/cond-mat/0610539') ==
      'session09/helton2007_arxivcond-mat-0610539.txt', 'ok')
print('all checks of page 02 hold')
