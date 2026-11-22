"""Session 7, the numbers that page 06 (Section 7.6) quotes, checked in the order of the page.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or
in the figure script that draws it. The figure dimer_entropy asserts its own curve. The product of singlets (7.8) is
built with np.kron, site 0 as the first factor, as in the figure. The copper nitrate values of the lab box come from
exact diagonalization of the open chain of 16 spins in the sector S^z_tot = 0, with site i as bit i of the index, so the
first l sites are psi.reshape(-1, 2**l), and the bonds (0,1), (2,3), ... are the strong ones, as on the conventions
sheet. It finds the repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session07/g3_06_dimerized_chain.py"""
import os, sys
sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
assert os.path.exists(os.path.join(REPO, 'webnotes', 'pages', 'session07'))

import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spl

ln2 = np.log(2)


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def entropy_of(p):
    p = np.asarray(p)
    p = p[p > 1e-14]
    return float(-np.sum(p * np.log(p)))


singlet = np.array([0, 1, -1, 0]) / np.sqrt(2)          # (|ud> - |du>)/sqrt(2)


def dimer_state(N):
    psi = np.array([1.0])
    for n in range(N // 2):
        psi = np.kron(psi, singlet)
    return psi.reshape((2,) * N)


def block_entropy(psi, sites):
    N = psi.ndim
    rest = [i for i in range(N) if i not in sites]
    m = np.transpose(psi, list(sites) + rest).reshape(2 ** len(sites), -1)
    return entropy_of(np.linalg.svd(m, compute_uv=False) ** 2)


def ncut(lo, hi, N):
    return sum((lo <= a <= hi) != (lo <= a + 1 <= hi) for a in range(0, N, 2))


# the recall box: one spin of the singlet is in the state 1/2, and S = log 2
rho = np.outer(singlet, singlet).reshape(2, 2, 2, 2)
rho_a = np.einsum('ijkj->ik', rho)
check('recall and fold, one spin of the singlet has rho = 1/2 and S = log 2', np.allclose(rho_a, np.eye(2) / 2) and
      abs(entropy_of(np.linalg.eigvalsh(rho_a)) - ln2) < 1e-12, np.diag(rho_a))

# the opener and the key box: every block of consecutive sites has S = n_cut log 2, at most 2 log 2
N = 12
psi = dimer_state(N)
worst, top = 0.0, 0.0
for lo in range(N):
    for hi in range(lo, N):
        S = block_entropy(psi, list(range(lo, hi + 1)))
        worst = max(worst, abs(S - ncut(lo, hi, N) * ln2))
        top = max(top, S)
check('key box, every block of 12 sites has S = n_cut log 2', worst < 1e-10, worst)
check('opener and key box, a block of consecutive sites has at most 2 log 2', abs(top - 2 * ln2) < 1e-10, top / ln2)

# the fold: the entropy of a product is the sum of the entropies
rng = np.random.default_rng(5)
def random_rho(d):
    X = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    r = X @ X.conj().T
    return r / np.trace(r).real
r1, r2 = random_rho(3), random_rho(4)
S1, S2, S12 = (entropy_of(np.linalg.eigvalsh(r)) for r in (r1, r2, np.kron(r1, r2)))
check('fold, S(rho x sigma) = S(rho) + S(sigma)', abs(S12 - S1 - S2) < 1e-10, (S12, S1 + S2))
# the fold: the sum needs each factor to have trace 1, -sum p_i q_j log(p_i q_j) = S(p) sum q + S(q) sum p
p, q = np.array([0.3, 0.5]), np.array([0.2, 0.4, 0.9])          # weights that do not add up to 1
pq = np.outer(p, q).ravel()
S_pq, S_p, S_q = (float(-np.sum(x * np.log(x))) for x in (pq, p, q))
check('fold, the additivity uses trace 1: with other traces S(p x q) = S(p) Tr q + S(q) Tr p, not S(p) + S(q)',
      abs(S_pq - S_p * q.sum() - S_q * p.sum()) < 1e-12 and abs(S_pq - S_p - S_q) > 0.1, (S_pq, S_p + S_q))
proj = np.outer(singlet, singlet)
check('fold, the factors have trace 1: the singlet projector and 1/2', abs(np.trace(proj) - 1) < 1e-12 and
      abs(np.trace(np.eye(2) / 2) - 1) < 1e-12, (np.trace(proj), np.trace(np.eye(2) / 2)))

# the two quizzes, on the chain of 8 sites
psi8 = dimer_state(8)
want = {(1, 4): 2, (2, 5): 0, (3, 6): 2, (1, 3): 1}
for (lo, hi), n in want.items():
    S = block_entropy(psi8, list(range(lo, hi + 1)))
    check(f'quizzes, the block of the sites {lo} to {hi} has S = {n} log 2', abs(S - n * ln2) < 1e-10, S / ln2)

# the problem: S0.S1 = (S_tot^2 - 3/2)/2, the singlet at -3J/4 and the triplet at J/4, the gap J
sx = np.array([[0, 1], [1, 0]]) / 2; sy = np.array([[0, -1j], [1j, 0]]) / 2; sz = np.diag([0.5, -0.5])
SS = sum(np.kron(s, s) for s in (sx, sy, sz)).real
Stot2 = sum((np.kron(s, np.eye(2)) + np.kron(np.eye(2), s)) @ (np.kron(s, np.eye(2)) + np.kron(np.eye(2), s)) for s in (sx, sy, sz)).real
check('problem, S_i^2 = 3/4', np.allclose(sum(s @ s for s in (sx, sy, sz)).real, 0.75 * np.eye(2)), 0.75)
check('problem, S0.S1 = (S_tot^2 - 3/2)/2', np.allclose(SS, (Stot2 - 1.5 * np.eye(4)) / 2), True)
e = np.linalg.eigvalsh(SS)
check('problem, the levels are -3/4 once and 1/4 three times, with the sum 0', np.allclose(e, [-0.75, 0.25, 0.25, 0.25])
      and abs(e.sum()) < 1e-12, e)


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


# the problem: the decoupled dimers of 8 sites have the gap J, the cost of one triplet
H, _ = heisenberg(8, [1.0 if i % 2 == 0 else 0.0 for i in range(7)])
e = np.sort(np.linalg.eigvalsh(H.toarray()))
check('problem, decoupled dimers of 8 sites: ground state -3 J and the gap J', abs(e[0] + 3) < 1e-12 and
      abs(e[np.argmax(e > e[0] + 1e-9)] - e[0] - 1) < 1e-12, e[:2])

# the lab box, ours: the open chain of 16 spins with J2 = 0.24 J1
L = 16
H, states = heisenberg(L, [1.0 if i % 2 == 0 else 0.24 for i in range(L - 1)])
ev, v = spl.eigsh(H, k=1, which='SA', tol=1e-13)
gs = np.zeros(2 ** L)
gs[states] = v[:, 0]
S = np.array([entropy_of(np.linalg.svd(gs.reshape(-1, 2 ** l), compute_uv=False) ** 2) for l in range(1, L)]) / ln2
strong, weak = S[0::2], S[1::2]           # a cut after an odd number of sites goes through a strong bond
check('lab box, a cut through a strong bond gives 1.00 log 2', np.all(np.round(strong, 2) == 1.00), (strong.min(), strong.max()))
check('lab box, a cut through a weak bond gives 0.035 log 2', np.all(np.round(weak, 3) == 0.035), (weak.min(), weak.max()))
print('all checks of page 06 hold')
