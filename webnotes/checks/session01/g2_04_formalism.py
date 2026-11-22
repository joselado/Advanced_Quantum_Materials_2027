"""Session 1, the numbers that page 04 (Section 1.4) quotes.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The figure of this page, fixed_vs_free_number, is a schematic with no number.
This script holds the numbers of the quiz and of the problem, in the order of the page. It writes no file.

Run it from anywhere:  python3 webnotes/checks/session01/g2_04_formalism.py"""
from itertools import combinations
from math import comb

import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# the quiz: an equal superposition of N=0 and N=2 has the mean 1, of N=1 and N=2 the mean 1.5, and the number of
# coordinates of a term is its number of electrons
for (n1, n2), mean in (((0, 2), 1.0), ((1, 2), 1.5), ((1, 1), 1.0)):
    m = 0.5 * n1 + 0.5 * n2
    check(f'quiz: equal superposition of N={n1} and N={n2} has the mean {mean}', np.isclose(m, mean), m)
check('quiz: zero and two electrons, mean 1, also have two terms with different numbers of coordinates, 0 and 2',
      0.5 * 0 + 0.5 * 2 == 1 and 0 != 2, (0, 2))


# the quiz, third option: one and two electrons have the parities (-1)^1 = -1 and (-1)^2 = +1, and every product of an
# even number of operators keeps the parity, so it has no matrix element between N=1 and N=2. Two sites, Jordan-Wigner.
def fermions(L):
    a, Zm, Im = np.array([[0., 1.], [0., 0.]]), np.diag([1., -1.]), np.eye(2)
    out = []
    for j in range(L):
        m = np.eye(1)
        for f in [Zm] * j + [a] + [Im] * (L - j - 1):
            m = np.kron(m, f)
        out.append(m)
    return out


cc = fermions(2)
ops = cc + [x.T for x in cc]
Nop = sum(x.T @ x for x in cc)
nocc = np.diag(Nop)
par = np.diag((-1.0) ** nocc)
check('quiz: the parity of one electron is -1 and of two electrons +1', (-1) ** 1 == -1 and (-1) ** 2 == 1
      and set(np.diag(par)[nocc == 1]) == {-1.0} and set(np.diag(par)[nocc == 2]) == {1.0}, (-1, 1))
even = [A @ B for A in ops for B in ops] + [A @ B @ C @ D for A in ops for B in ops for C in ops for D in ops]
s1, s2 = np.where(nocc == 1)[0], np.where(nocc == 2)[0]
worst = max(np.abs(E[np.ix_(s1, s2)]).max() for E in even)
check('quiz: every product of two or four operators has no matrix element between N=1 and N=2, it keeps the parity',
      worst == 0 and all(np.allclose(E @ par, par @ E) for E in even), worst)
odd_mix = max(np.abs(A[np.ix_(s1, s2)]).max() for A in ops)
check('quiz: a single operator does connect N=1 and N=2, so only an odd operator could mix the two terms', odd_mix > 0, odd_mix)

# the problem: L levels, each empty or occupied, binom(L, N) states with N electrons, 2^L in total
L = 4
counts = [len(list(combinations(range(L), N))) for N in range(L + 1)]
check('problem: L=4 gives 1, 4, 6, 4, 1 states for N=0..4', counts == [1, 4, 6, 4, 1], counts)
check('problem: the counts are binom(4, N)', counts == [comb(L, N) for N in range(L + 1)], counts)
check('problem: 6 states with N=2', counts[2] == 6, counts[2])
check('problem: 1+4+6+4+1 = 16 = 2^4', sum(counts) == 16 == 2 ** 4, sum(counts))
# the 16 occupation lists of four levels are all the lists of 0 and 1, so each level is free, and the sum is 2^L for
# every L
occ = {tuple(int(j in s) for j in range(L)) for N in range(L + 1) for s in combinations(range(L), N)}
check('problem: the 16 states are all the occupation lists of four levels', len(occ) == 16, len(occ))
check('problem: sum_N binom(L, N) = 2^L for L = 1..20', all(sum(comb(l, n) for n in range(l + 1)) == 2 ** l
                                                            for l in range(1, 21)), 2 ** 20)
# the 6 states with N=2 are the 6 Slater determinants of two of four orbitals, which span all the antisymmetric
# functions psi(x1, x2) built from the four levels: the antisymmetric part of the 4x4 product space has dimension 6
P = np.zeros((16, 16))
for i in range(4):
    for j in range(4):
        P[4 * i + j, 4 * j + i] = 1.0
anti = np.linalg.matrix_rank((np.eye(16) - P) / 2)
check('problem: the antisymmetric two-particle functions of four levels span 6 dimensions', anti == 6, anti)

# Section 1.4.2, the sentences corrected on 2026-11-22: for interacting electrons first quantization still works, with a
# wave function psi(x1, x2) of the coordinates of both. Two spinless electrons on an open chain of five sites with the
# hopping -t and the repulsion V n_i n_(i+1). Route 1 is first quantization, the 25 functions psi(x1, x2) and their
# antisymmetric part, route 2 the block with N=2 of the Fock space with the Jordan-Wigner operators. The two give the
# same 10 levels. At V = 0 the ground state is one Slater determinant, an antisymmetric 5x5 matrix of rank 2, and at
# V = 2t it is not, so the wave function depends on both coordinates at once.
L5, tt = 5, 1.0
h1 = np.zeros((L5, L5))
for i in range(L5 - 1):
    h1[i, i + 1] = h1[i + 1, i] = -tt
I5 = np.eye(L5)
Pex = np.zeros((L5 * L5, L5 * L5))
for i in range(L5):
    for j in range(L5):
        Pex[L5 * i + j, L5 * j + i] = 1.0
cf = fermions(L5)
nf = [x.T @ x for x in cf]
Nf = sum(nf)
blk = np.where(np.isclose(np.diag(Nf), 2))[0]
res = {}
for V in (0.0, 2.0):
    Vx = np.diag([V * (abs(i - j) == 1) for i in range(L5) for j in range(L5)])
    H1q = np.kron(h1, I5) + np.kron(I5, h1) + Vx
    w, v = np.linalg.eigh((np.eye(L5 * L5) - Pex) / 2)
    A = v[:, np.isclose(w, 1)]                                        # the antisymmetric functions psi(x1, x2)
    e1, u1 = np.linalg.eigh(A.T @ H1q @ A)
    H2q = sum(-tt * (cf[i].T @ cf[i + 1] + cf[i + 1].T @ cf[i]) + V * nf[i] @ nf[i + 1] for i in range(L5 - 1))
    e2 = np.linalg.eigvalsh(H2q[np.ix_(blk, blk)])
    psi = (A @ u1[:, 0]).reshape(L5, L5)
    res[V] = (A.shape[1], e1, e2, np.linalg.matrix_rank(psi, tol=1e-10), np.allclose(psi, -psi.T))
for V, (dim, e1, e2, rank, asym) in res.items():
    check(f'Section 1.4.2: at V = {V:g}t first quantization, psi(x1, x2) antisymmetric, has binom(5, 2) = 10 states and the '
          'same levels as the block N=2 of the Fock space', dim == comb(L5, 2) == len(e2) and np.allclose(e1, e2, atol=1e-12)
          and asym, np.round(e1[:3], 6).tolist())
check('Section 1.4.2: at V = 0 the ground state psi(x1, x2) is one Slater determinant, rank 2', res[0.0][3] == 2, res[0.0][3])
check('Section 1.4.2: at V = 2t it is not one Slater determinant, so it depends on both coordinates at once',
      res[2.0][3] > 2, res[2.0][3])
