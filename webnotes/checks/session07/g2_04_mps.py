"""Session 7, the numbers that page 04 (Sections 7.4 and 7.5) quotes, checked in the order of the page.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or
in the figure script that draws it. The entropies are in nats, with the natural logarithm of (7.6). A two-spin state is
stored as the table psi[s1, s2], with up as index 0, so rho_A = psi psi^dagger is the trace over the second spin. The
CHSH values of the lab box are not on the conventions sheet, so they are checked on two routes, with the explicit axes
and with the largest value over all axes from the correlation matrix T_ij = <sigma_i sigma_j>. The lab box is checked
against the stored source. The script finds the repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session07/g2_04_mps.py"""
import os, sys
sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
assert os.path.exists(os.path.join(REPO, 'webnotes', 'pages', 'session07'))

import numpy as np
from scipy.optimize import minimize


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def mps_numbers(L, M, d=2, full=False):
    """Numbers of an open MPS, sum_i d D_{i-1} D_i with D_0 = D_L = 1, every inner bond M or min(M, d^i, d^(L-i))."""
    D = [1] + [M if full else min(M, d ** i, d ** (L - i)) for i in range(1, L)] + [1]
    return sum(d * D[i] * D[i + 1] for i in range(L))


def entropy(psi):
    psi = np.asarray(psi, dtype=complex).reshape(2, 2)
    psi = psi / np.linalg.norm(psi)
    p = np.linalg.eigvalsh(psi @ psi.conj().T)
    p = p[p > 1e-14]
    return float(-np.sum(p * np.log(p))), np.sort(np.linalg.eigvalsh(psi @ psi.conj().T))[::-1]


ln2 = np.log(2)

# the opener and the key box: about 2 L M^2 numbers instead of 2^L
for L, M in ((100, 10),):
    a, b = mps_numbers(L, M, full=True), mps_numbers(L, M)
    check(f'key box, L={L}, M={M}: the open MPS stores {a} or {b} numbers, about 2 L M^2 = {2 * L * M * M}',
          abs(a / (2 * L * M * M) - 1) < 0.06 and abs(b / (2 * L * M * M) - 1) < 0.06, (a, b))

# the first quiz: 2^100 = 1.3e30, 2 L M^2 = 2e4, the product state M=1 has 2 numbers per site, 200 for 100 sites,
# and doubling the chain doubles the storage
check('quiz 1, 2^100 is about 1.3e30', round(2 ** 100 / 1e30, 1) == 1.3, 2 ** 100)
check('quiz 1, 2 L M^2 = 2e4 for L=100 and M=10, with M^2 = 100 entries per matrix', 2 * 100 * 10 ** 2 == 20000, 20000)
check('quiz 1, M=1 stores 2 numbers per site, 200 for 100 sites', mps_numbers(100, 1) == 200, mps_numbers(100, 1))
# the question: with vectors at the two ends the product is a number, and the count is still about 2e4
rngq = np.random.default_rng(11)
ends = [rngq.normal(size=(1, 10))] + [rngq.normal(size=(10, 10)) for _ in range(98)] + [rngq.normal(size=(10, 1))]
prodq = ends[0]
for A in ends[1:]:
    prodq = prodq @ A
check('quiz 1, with vectors at the two ends the product of the 100 factors is a 1 x 1 number, and 19640 is about 2e4',
      prodq.shape == (1, 1) and 2 * sum(A.size for A in ends) == mps_numbers(100, 10, full=True) == 19640, prodq.shape)
r = mps_numbers(200, 10, full=True) / mps_numbers(100, 10, full=True)
check('quiz 1, doubling the chain doubles the storage, exactly for 2 L M^2 and to 1 percent for the open MPS',
      2 * 200 * 100 == 2 * (2 * 100 * 100) and abs(r / 2 - 1) < 0.01, round(r, 4))

# Section 7.5: a product state has S = 0, the two examples |ud> and the product of two states along x
up_dn = np.array([[0, 1], [0, 0]])
xx = np.outer([1, 1], [1, 1]) / 2
check('text, |ud> and the product of two states along x have S = 0',
      abs(entropy(up_dn)[0]) < 1e-12 and abs(entropy(xx)[0]) < 1e-12, (entropy(up_dn)[0], entropy(xx)[0]))

# the singlet (7.3): rho_A = 1/2 1, S = log 2 (7.7), and log d is the largest entropy of one site
singlet = np.array([[0, 1], [-1, 0]]) / np.sqrt(2)          # psi[s1, s2], C(ud) = 1/sqrt2, C(du) = -1/sqrt2
rhoA = singlet @ singlet.conj().T
check('text and fold, the singlet gives rho_A = (1/2)(|u><u| + |d><d|) and S = log 2 = 0.6931',
      np.allclose(rhoA, np.eye(2) / 2) and abs(entropy(singlet)[0] - ln2) < 1e-12, round(entropy(singlet)[0], 4))
rng = np.random.default_rng(7)
Smax = max(entropy(rng.normal(size=4) + 1j * rng.normal(size=4))[0] for _ in range(2000))
check('text, no state of two spins has more than log 2 on one site', Smax <= ln2 + 1e-12, round(Smax, 4))

# the fold: the product state |ud> gives the eigenvalues 1 and 0, and the cross terms of the singlet drop out
check('fold, |ud> gives rho_A with the eigenvalues 1 and 0', np.allclose(entropy(up_dn)[1], [1, 0]), entropy(up_dn)[1])
rho = np.kron(singlet.reshape(4), singlet.reshape(4).conj()).reshape(2, 2, 2, 2)       # rho[a, b, a', b']
cross = rho.copy(); cross[:, 0, :, 0] = 0; cross[:, 1, :, 1] = 0                       # the terms with b != b'
check('fold, the terms with a different second spin do not reach rho_A',
      np.allclose(np.einsum('abcb->ac', cross), 0) and np.allclose(np.einsum('abcb->ac', rho), np.eye(2) / 2), True)

# the figure singlet_entropy: 0 at the product states, log 2 at pi/4, and the singlet at -pi/4 with the same value
th = lambda t: np.array([[0, np.cos(t)], [np.sin(t), 0]])
check('caption, S(0) = S(pi/2) = 0, S(pi/4) = S(-pi/4) = log 2, and -pi/4 is the singlet',
      abs(entropy(th(0))[0]) < 1e-12 and abs(entropy(th(np.pi / 2))[0]) < 1e-12
      and abs(entropy(th(np.pi / 4))[0] - ln2) < 1e-12 and abs(entropy(th(-np.pi / 4))[0] - ln2) < 1e-12
      and np.allclose(th(-np.pi / 4), singlet), True)

# the lab box: CHSH = E(a,b) + E(a,b') + E(a',b) - E(a',b'), at most 2 for product states and 2 sqrt 2 for the singlet
pauli = [np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]), np.diag([1.0, -1.0])]


def T(psi):
    v = np.asarray(psi, dtype=complex).reshape(4)
    v = v / np.linalg.norm(v)
    return np.array([[np.vdot(v, np.kron(a, b) @ v).real for b in pauli] for a in pauli])


def chsh_best(psi):
    """Largest CHSH value over all axes, 2 sqrt(m1 + m2) with m1, m2 the largest eigenvalues of T^T T."""
    m = np.sort(np.linalg.eigvalsh(T(psi).T @ T(psi)))[::-1]
    return 2 * np.sqrt(m[0] + m[1])


def chsh(psi, a, a2, b, b2):
    t = T(psi)
    E = lambda x, y: x @ t @ y
    return E(a, b) + E(a, b2) + E(a2, b) - E(a2, b2)


z, x = np.array([0, 0, 1.0]), np.array([1.0, 0, 0])
d1, d2 = (z + x) / np.sqrt(2), (z - x) / np.sqrt(2)
v_axes = abs(chsh(singlet, z, x, d1, d2))
check('lab box, route 1: the singlet with the axes z, x and the two diagonals gives 2 sqrt 2 = 2.83',
      abs(v_axes - 2 * np.sqrt(2)) < 1e-12 and round(v_axes, 2) == 2.83, round(v_axes, 4))
check('lab box, route 2: the largest value over all axes for the singlet is 2 sqrt 2',
      abs(chsh_best(singlet) - 2 * np.sqrt(2)) < 1e-12, round(chsh_best(singlet), 4))


def random_unit(n):
    v = rng.normal(size=3)
    return v / np.linalg.norm(v)


def spinor(n):
    th, ph = np.arccos(np.clip(n[2], -1, 1)), np.arctan2(n[1], n[0])
    return np.array([np.cos(th / 2), np.exp(1j * ph) * np.sin(th / 2)])


best2, best1 = 0.0, 0.0
for _ in range(20):
    prod = np.outer(spinor(random_unit(3)), spinor(random_unit(3)))
    best2 = max(best2, chsh_best(prod))
    angles = lambda p: [np.array([np.sin(p[2 * k]) * np.cos(p[2 * k + 1]), np.sin(p[2 * k]) * np.sin(p[2 * k + 1]),
                                  np.cos(p[2 * k])]) for k in range(4)]
    res = minimize(lambda p: -chsh(prod, *angles(p)), rng.uniform(0, np.pi, 8), method='Nelder-Mead',
                   options={'maxiter': 1500, 'xatol': 1e-7, 'fatol': 1e-9})
    best1 = max(best1, -res.fun)
check('lab box, product states: the largest value over all axes is 2, by both routes',
      best2 <= 2 + 1e-9 and best1 <= 2 + 1e-6 and best2 > 2 - 1e-9, (round(best1, 6), round(best2, 6)))
src = open(os.path.join(REPO, 'webnotes', 'sources', 'session07', 'hensen2015_arxiv1508.05949.txt'),
           encoding='utf-8').read()
check('lab box, the source states 1.3 km, 245 trials, S <= 2 and S = 2.42 +- 0.20, random basis selection',
      'separated by 1.3 km' in src and '245 trials testing the CHSH-Bell inequality S ≤ 2 and find S = 2.42 ± 0.20' in src
      and 'random basis selection and readout' in src and 'any local realist theory' in src, 'hensen2015')

# the second quiz: the state with a plus sign has log 2, it is not a product, and log 2 is the most for one spin
plus = np.array([[0, 1], [1, 0]]) / np.sqrt(2)
check('quiz 2, (|ud> + |du>)/sqrt2 has S = log 2, as the singlet', abs(entropy(plus)[0] - ln2) < 1e-12,
      round(entropy(plus)[0], 4))
check('quiz 2, it is not a product: its table has rank 2', np.linalg.matrix_rank(plus) == 2, 2)
# the second wrong option: 2 log 2 is log 4, the entropy of four equal weights, which one site with two states cannot
# hold, since its rho_A is 2 x 2
check('quiz 2, 2 log 2 = log 4 needs four equal weights, and a 2 x 2 rho_A has at most log 2',
      abs(2 * ln2 - np.log(4)) < 1e-15 and abs(-np.sum(np.full(4, 0.25) * np.log(np.full(4, 0.25))) - 2 * ln2) < 1e-14
      and Smax <= ln2 + 1e-12, round(2 * ln2, 4))

# the third quiz: (|uu> + |dd>)/sqrt2 has log 2, the sum of the four states is a product along x with S = 0, and
# (|uu> + |ud> + |du>)/sqrt3 has the eigenvalues 0.873 and 0.127 and S = 0.381 = 0.55 log 2
ghz = np.array([[1, 0], [0, 1]]) / np.sqrt(2)
allfour = np.ones((2, 2)) / 2
three = np.array([[1, 1], [1, 0]]) / np.sqrt(3)
S3, p3 = entropy(three)
check('quiz 3, (|uu> + |dd>)/sqrt2 has rho_A = 1/2 and S = log 2',
      np.allclose(ghz @ ghz.T, np.eye(2) / 2) and abs(entropy(ghz)[0] - ln2) < 1e-12, round(entropy(ghz)[0], 4))
check('quiz 3, the sum of the four states is the product of two states along x, S = 0',
      np.allclose(allfour, np.outer([1, 1], [1, 1]) / 2) and abs(entropy(allfour)[0]) < 1e-12, entropy(allfour)[0])
check('quiz 3, the state of three terms has C(uu)C(dd) = 0 and C(ud)C(du) = 1/3',
      abs(three[0, 0] * three[1, 1]) < 1e-12 and abs(three[0, 1] * three[1, 0] - 1 / 3) < 1e-12, 1 / 3)
check('quiz 3, its rho_A has the eigenvalues 0.873 and 0.127, and S = 0.381 = 0.55 log 2',
      np.allclose(np.round(p3, 3), [0.873, 0.127]) and round(S3, 3) == 0.381 and round(S3 / ln2, 2) == 0.55,
      (np.round(p3, 4), round(S3, 4), round(S3 / ln2, 4)))
pa = np.array([(3 + np.sqrt(5)) / 6, (3 - np.sqrt(5)) / 6])         # rho_A = [[2, 1], [1, 1]] / 3 by hand
check('quiz 3, second route: rho_A = [[2,1],[1,1]]/3 has the eigenvalues (3 +- sqrt5)/6, the same S',
      np.allclose(three @ three.T, np.array([[2, 1], [1, 1]]) / 3) and np.allclose(pa, p3)
      and abs(-np.sum(pa * np.log(pa)) - S3) < 1e-12, np.round(pa, 4))

# the problem: the vectors give the singlet, M=1 would need 0 = -1/2, and 8 numbers against 4 coefficients
v = {'u': np.array([1.0, 0]), 'd': np.array([0, 1.0])}
w = {'u': np.array([0, -1 / np.sqrt(2)]), 'd': np.array([1 / np.sqrt(2), 0])}
C = np.array([[v[a] @ w[b] for b in 'ud'] for a in 'ud'])
check('problem, v.w gives C(uu) = 0, C(ud) = 1/sqrt2, C(du) = -1/sqrt2, C(dd) = 0, the singlet',
      np.allclose(C, singlet), np.round(C, 4))
check('problem, M=1 needs C(uu)C(dd) = C(ud)C(du), which is 0 = -1/2 for the singlet',
      abs(singlet[0, 0] * singlet[1, 1]) < 1e-12 and abs(singlet[0, 1] * singlet[1, 0] + 0.5) < 1e-12, -0.5)
sv = np.linalg.svd(singlet, compute_uv=False)
check('problem, second route: the singlet has two equal Schmidt weights, so M=2 is the smallest and S = log 2 = log M',
      np.allclose(sv ** 2, [0.5, 0.5]) and abs(entropy(singlet)[0] - np.log(2)) < 1e-12, sv ** 2)
check('problem, the MPS of two sites with M=2 stores 8 numbers, against 4 coefficients',
      sum(len(x) for x in list(v.values()) + list(w.values())) == 8 == mps_numbers(2, 2, full=True), 8)
print('all checks of page 04 hold')
