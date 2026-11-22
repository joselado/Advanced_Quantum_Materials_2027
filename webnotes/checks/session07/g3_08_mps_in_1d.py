"""Session 7, the numbers that page 08 (Section 7.8a) quotes, checked in the order of the page.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or
in the figure script that draws it. The fold is checked on random weights, the Schmidt weights of the figure
schmidt_spectrum are computed again by exact diagonalization in the sector S^z_tot = 0, with site i as bit i of the
index, and the AKLT chain of the first quiz is checked as an MPS with M = 2. It finds the repository from its own path
and writes no file.

Run it from anywhere:  python3 webnotes/checks/session07/g3_08_mps_in_1d.py"""
import os, sys
sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
assert os.path.exists(os.path.join(REPO, 'webnotes', 'pages', 'session07'))

import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spl
from functools import reduce

ln2 = np.log(2)


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def entropy(p):
    p = np.asarray(p, float)
    p = p[p > 1e-15]
    return float(-np.sum(p * np.log(p)))


# the fold: M = 2 first, S(p) is largest at p = 1/2 with log 2, and the derivative is log((1-p)/p)
p = np.linspace(1e-6, 1 - 1e-6, 200001)
Sp = -p * np.log(p) - (1 - p) * np.log(1 - p)
check('fold, M=2: S(p) is largest at p=1/2, with log 2', abs(p[np.argmax(Sp)] - 0.5) < 1e-5 and abs(Sp.max() - ln2) < 1e-10,
      (p[np.argmax(Sp)], Sp.max()))
h = 1e-6
for q in (0.2, 0.5, 0.7):
    d = (entropy([q + h, 1 - q - h]) - entropy([q - h, 1 - q + h])) / (2 * h)
    check(f'fold, dS/dp = log((1-p)/p) at p={q}', abs(d - np.log((1 - q) / q)) < 1e-6, round(d, 8))
# the fold: the second derivative of S with respect to p_alpha is -1/p_alpha < 0, so the point of equal weights is a maximum
for q in (0.1, 0.25, 0.5):
    hh = 1e-4
    f = lambda x: -x * np.log(x)
    d2 = (f(q + hh) - 2 * f(q) + f(q - hh)) / hh ** 2
    check(f'fold, d2S/dp^2 = -1/p at p={q}', abs(d2 + 1 / q) < 1e-5 and d2 < 0, round(d2, 6))
# the fold: for M weights the largest S is log M, at equal weights, and a lower rank gives less
rng = np.random.default_rng(3)
for M in (2, 4, 16):
    best = max(entropy(w / w.sum()) for w in rng.random((4000, M)))
    check(f'fold, M={M}: random weights stay below log M, equal ones reach it', best < np.log(M) and
          abs(entropy(np.ones(M) / M) - np.log(M)) < 1e-12, (round(best, 4), round(np.log(M), 4)))

# the key box: a random state has the Schmidt rank 2^(L/2) at the middle, the M ~ 2^(L/2) of a volume law
L = 10
psi = rng.normal(size=2 ** L) + 1j * rng.normal(size=2 ** L)
rank = np.linalg.matrix_rank(psi.reshape(2 ** (L // 2), -1))
check('key box, a random state of 10 spins has the Schmidt rank 2^(L/2)=32 at the middle', rank == 32, rank)

# the steps and the second quiz: log 16 = 4 log 2, 16 log 2 = log 65536, 8 log 2 = log 256
check('second quiz, log 16 = 4 log 2 = 2.7726', abs(np.log(16) - 4 * ln2) < 1e-12 and round(np.log(16), 4) == 2.7726,
      np.log(16))
check('second quiz, 16 log 2 = log 65536 and 8 log 2 = log 256',
      abs(16 * ln2 - np.log(65536)) < 1e-12 and abs(8 * ln2 - np.log(256)) < 1e-12 and 2 ** 16 == 65536, True)

# the problem: weights 1/2, 1/4, 1/8, 1/8
w = np.array([1 / 2, 1 / 4, 1 / 8, 1 / 8])
S = entropy(w)
check('problem, S = 1.75 log 2 = 1.21', abs(S - 1.75 * ln2) < 1e-12 and round(S, 2) == 1.21, S)
check('problem, log 4 = 2 log 2 = 1.39', round(np.log(4), 2) == 1.39, np.log(4))
check('problem, the dropped weight with M=2 is 0.25', abs(w[2:].sum() - 0.25) < 1e-15, w[2:].sum())
U = np.linalg.qr(rng.normal(size=(4, 4)))[0]
V = np.linalg.qr(rng.normal(size=(4, 4)))[0]
full = U @ np.diag(np.sqrt(w)) @ V.T
kept = U[:, :2] @ np.diag(np.sqrt(w[:2])) @ V[:, :2].T
check('problem, before we normalize it, the squared norm of the difference is the dropped weight',
      abs(np.sum((full - kept) ** 2) - 0.25) < 1e-12, np.sum((full - kept) ** 2))
kept_n = kept / np.linalg.norm(kept)
overlap2 = np.sum(full * kept_n) ** 2
check('problem, after we normalize it, the overlap squared with the exact state is 1 - 0.25 = 0.75', abs(overlap2 - 0.75) < 1e-12,
      (overlap2, np.sum((full - kept_n) ** 2)))


# the figure schmidt_spectrum: the open Heisenberg chain of 16 sites, J1 = 1 on (0,1), (2,3), ... and J2 on the others
def heisenberg(L, J):
    states = np.array([s for s in range(2 ** L) if bin(s).count('1') == L // 2], dtype=np.int64)
    index = -np.ones(2 ** L, dtype=np.int64)
    index[states] = np.arange(len(states))
    rows, cols, vals = [], [], []
    diag = np.zeros(len(states))
    for i in range(L - 1):
        a, b = (states >> i) & 1, (states >> (i + 1)) & 1
        diag += J[i] * np.where(a == b, 0.25, -0.25)
        k = np.where(a != b)[0]
        rows.append(k); cols.append(index[states[k] ^ (3 << i)]); vals.append(np.full(len(k), 0.5 * J[i]))
    H = sps.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(len(states),) * 2)
    return H + sps.diags(diag), states


def ground_state(L, J2):
    H, states = heisenberg(L, [1.0 if i % 2 == 0 else J2 for i in range(L - 1)])
    e, v = spl.eigsh(H, k=1, which='SA', tol=1e-13)
    psi = np.zeros(2 ** L)
    psi[states] = v[:, 0]
    return psi


L = 16
tail, tail10, tail100, gs16 = {}, {}, {}, {}
for J2 in (1.0, 0.5):
    psi = gs16[J2] = ground_state(L, J2)
    lam2 = np.linalg.svd(psi.reshape(2 ** (L // 2), 2 ** (L // 2)), compute_uv=False) ** 2
    tail[J2], tail10[J2], tail100[J2] = lam2[16:].sum(), lam2[10:].sum(), lam2[100:].sum()
    check(f'schmidt_spectrum, J2={J2}: the weights sum to 1', abs(lam2.sum() - 1) < 1e-9, lam2.sum())
check('schmidt_spectrum caption, the central cut after 8 sites is the bond (7,8), a J2 bond', 7 % 2 == 1, '(7,8)')
check('schmidt_spectrum caption, the weight beyond M=16 is 2e-7 for the uniform chain', 1.5e-7 < tail[1.0] < 2.5e-7, tail[1.0])
check('schmidt_spectrum caption, the weight beyond M=16 is 3e-11 for the dimerized chain', 2.5e-11 < tail[0.5] < 3.5e-11,
      tail[0.5])
check('text, the weights fall faster for the dimerized chain', tail[0.5] < 1e-3 * tail[1.0], tail[0.5] / tail[1.0])
# the old text, "M ~ 10, 100" is a moderate bond dimension: at the center of 16 sites M = 10 drops less than 1e-5 of the weight,
# and M = 100 less than 1e-12, which is only an upper bound, since eigsh has the tolerance 1e-13
check('text, M ~ 10: the weight beyond 10 at the center of 16 sites is below 1e-5, uniform and dimerized',
      tail10[1.0] < 1e-5 and tail10[0.5] < 1e-8, (tail10[1.0], tail10[0.5]))
check('text, M ~ 100: the weight beyond 100 at the center of 16 sites is below 1e-12', max(tail100.values()) < 1e-12,
      max(tail100.values()))

# the key box, "longer than its correlation length, the same M for the same error at each bond": the dimerized chain with
# J2 = 0.5 has, at the cut after 6 sites, the same entropy and the same weight beyond M = 4 for 12, 14 and 16 sites
cut = {}
for Lc in (12, 14, 16):
    psi = gs16[0.5] if Lc == 16 else ground_state(Lc, 0.5)
    lam2 = np.linalg.svd(psi.reshape(-1, 2 ** 6), compute_uv=False) ** 2
    cut[Lc] = (entropy(lam2) / ln2, lam2[4:].sum())
Sc, tc = np.array([c[0] for c in cut.values()]), np.array([c[1] for c in cut.values()])
check('key box, the cut after 6 sites of 12, 14 and 16 sites: the same entropy to 1e-4 log 2 and the same weight beyond M=4 to 3 percent',
      np.ptp(Sc) < 1e-4 and np.ptp(tc) < 0.03 * tc.min(), cut)

# the first quiz: the AKLT chain is an MPS with M = 2, exact for any length, checked on 6 and 8 sites of spin 1
s1 = {'x': np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) / np.sqrt(2), 'y': np.array([[0, -1j, 0], [1j, 0, -1j], [0, 1j, 0]]) / np.sqrt(2),
      'z': np.diag([1., 0, -1])}
sp, sz = np.array([[0, 1.], [0, 0]]), np.diag([1., -1])
A = {0: np.sqrt(2 / 3) * sp, 1: -np.sqrt(1 / 3) * sz, 2: -np.sqrt(2 / 3) * sp.T}         # m = +1, 0, -1
for L in (6, 8):
    psi = np.zeros(3 ** L)
    for n in range(3 ** L):
        m = [(n // 3 ** (L - 1 - i)) % 3 for i in range(L)]
        psi[n] = reduce(np.dot, [A[x] for x in m])[0, 0]
    psi /= np.linalg.norm(psi)
    I3 = sps.identity(3, format='csr')
    op = lambda o, i: reduce(lambda a, b: sps.kron(a, b, format='csr'), [sps.csr_matrix(o) if j == i else I3 for j in range(L)])
    H = 0
    for i in range(L - 1):
        SS = sum(op(s1[a], i) @ op(s1[a], i + 1) for a in 'xyz')
        H = H + SS + SS @ SS / 3
    E = np.real(np.vdot(psi, H @ psi))
    res = np.linalg.norm(H @ psi - E * psi)
    check(f'first quiz, the AKLT MPS with M=2 is an eigenstate on {L} sites at -2/3 (L-1)',
          res < 1e-10 and abs(E + 2 / 3 * (L - 1)) < 1e-10, (round(E, 6), res))
    S_full = entropy(np.linalg.svd(psi.reshape(3 ** (L // 2), -1), compute_uv=False) ** 2)

# the key box and the first quiz, 50 and 500 sites: the two-site tensor A^m A^m' has no part of total spin 2, so that
# (h + 2/3) A A = 0 on every bond and the MPS with M=2 is an eigenstate for any length. The Schmidt weights of the central
# bond come from the transfer matrix, checked against the full vector of 8 sites, and they are 1/2 and 1/2 for 50 and 500
SS = sum(np.kron(s1[a], s1[a]) for a in 'xyz').real
B = np.array([[A[i] @ A[j] for j in range(3)] for i in range(3)]).reshape(9, 4)
check('key box, the AKLT bond term gives (h + 2/3) A A = 0, so M=2 is exact for any length', np.abs((SS + SS @ SS / 3) @ B + 2 / 3 * B).max()
      < 1e-12, np.abs((SS + SS @ SS / 3) @ B + 2 / 3 * B).max())


def aklt_central_weights(L):
    El, Er = np.outer([1., 0], [1., 0]), np.outer([1., 0], [1., 0])     # the end vectors (1, 0), as in the vector above
    for _ in range(L // 2):
        El = sum(a.T @ El @ a for a in A.values())
    for _ in range(L - L // 2):
        Er = sum(a @ Er @ a.T for a in A.values())
    w, U = np.linalg.eigh(El)
    r = U @ np.diag(np.sqrt(np.clip(w, 0, None))) @ U.T
    p = np.linalg.eigvalsh(r @ Er @ r)
    return p / p.sum()


check('key box, the transfer matrix gives the central entropy of the full vector of 8 sites', abs(entropy(aklt_central_weights(8)) - S_full)
      < 1e-10, (entropy(aklt_central_weights(8)), S_full))
w50, w500 = aklt_central_weights(50), aklt_central_weights(500)
check('key box and first quiz, 50 and 500 sites: M=2 with the central weights 1/2 and 1/2, the same S = log 2',
      np.allclose(w50, 0.5, atol=1e-12) and np.allclose(w500, 0.5, atol=1e-12), (w50, w500))

# the caption of Figure 7.3, old and drawn by hand: the bars log2 M are 2 and 4 bits for M = 4 and 16. The volume law
# l log 2 goes above the bar of M = 16 after 5 sites and above an M of 10^4 after 14. The critical curve has c = 1, the
# central charge of the XX chain, from the slope c/3 of the entropy of a block of free fermions at half filling
check('Figure 7.3, the bars log2 M = 2 and 4 bits for M = 4 and 16', np.log2(4) == 2 and np.log2(16) == 4, True)
cross = [next(l for l in range(1, 100) if l * ln2 > np.log(Mx)) for Mx in (16, 1e4)]
check('Figure 7.3, the volume law goes above M = 16 at l = 5 and above M = 10^4 at l = 14', cross == [5, 14], cross)
Sff = []
for l in (10, 100):
    d = np.subtract.outer(np.arange(l), np.arange(l)).astype(float)
    C = np.where(d == 0, 0.5, np.sin(np.pi * d / 2) / (np.pi * np.where(d == 0, 1, d)))
    nu = np.clip(np.linalg.eigvalsh(C), 1e-15, 1 - 1e-15)
    Sff.append(float(-np.sum(nu * np.log(nu) + (1 - nu) * np.log(1 - nu))))
slope = (Sff[1] - Sff[0]) / np.log(10)
check('Figure 7.3, c = 1: the free-fermion block entropy grows as (c/3) log l with slope 1/3', abs(3 * slope - 1) < 0.01,
      (Sff, 3 * slope))

# the try-it box: ln 2 = 0.69
check('try-it, ln 2 = 0.69', round(ln2, 2) == 0.69, ln2)

# the try-it and the notebook box, corrected on 2026-11-22, by exact diagonalization of the 20 sites of the cells, which
# run dmrgpy (the conventions sheet gives the same 0.7924 and 0.6346 with maxm=20). The largest entropy sits on the cuts
# after 9 and 11 sites, the two bonds next to the central cut after 10 sites, which is below them. The bound (7.10) allows
# M = 3 already, since 0.79 < ln 3, but M = 3 drops 6e-2 of the weight, and only at M = 11 the dropped weight is below 1e-5
psi20 = ground_state(20, 1.0)
lam20 = [np.linalg.svd(psi20.reshape(2 ** (20 - l), 2 ** l), compute_uv=False) ** 2 for l in range(1, 20)]
S20 = np.array([entropy(x) for x in lam20])
big = [l + 1 for l in np.where(S20 > S20.max() - 1e-9)[0]]
check('try-it, 20 sites: the largest entropy is on the cuts after 9 and 11 sites, and the central cut after 10 sites is lower',
      big == [9, 11] and S20[9] < S20[8] - 0.1 and abs(S20[8] - 0.7924) < 5e-4 and abs(S20[9] - 0.6346) < 5e-4,
      (big, round(S20[8], 4), round(S20[9], 4)))
drop = {M: max(x[M:].sum() for x in lam20) for M in (3, 11)}
check('notebook box, 20 sites: the bound allows M = 3, which drops 6e-2 of the weight, and M = 11 drops less than 1e-5',
      int(np.ceil(np.exp(S20.max()))) == 3 and S20.max() < np.log(3) and drop[3] > 1e-2 and drop[11] < 1e-5, drop)
print('all checks of page 08 hold')
