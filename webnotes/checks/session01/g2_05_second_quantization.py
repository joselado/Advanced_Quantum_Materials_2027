"""Session 1, the numbers and the identities that page 05 (Sections 1.5, 1.6 and 1.7) quotes.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The energies of the figure dimer_fock are asserted in dimer_fock.py and those of
boson_fermion_pair in boson_fermion_pair.py, and they are repeated here since the fold and the quizzes quote them. The
operators are the Jordan-Wigner matrices of the conventions sheet, c_j with the sign (-1)^(n_0+...+n_(j-1)), in the
basis |n_0 n_1 ...> with site 0 first. This script holds the checks in the order of the page. It writes no file.

Run it from anywhere:  python3 webnotes/checks/session01/g2_05_second_quantization.py"""
from functools import reduce

import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def fermions(L):
    """The annihilation operators of L spinless sites, Jordan-Wigner, basis |n_0 ... n_(L-1)>."""
    a, Z, I = np.array([[0., 1.], [0., 0.]]), np.diag([1., -1.]), np.eye(2)
    return [reduce(np.kron, [Z] * j + [a] + [I] * (L - j - 1)) for j in range(L)]


def anti(A, B):
    return A @ B + B @ A


def ket(L, occ):
    """The basis state |n_0 ... n_(L-1)>, which is (c_0^+)^n_0 ... |0> with the creation operators in site order."""
    v = np.zeros(2 ** L)
    v[int(''.join(map(str, occ)), 2)] = 1.0
    return v


L = 2
c = fermions(L)
cd = [x.T for x in c]
vac = ket(L, [0, 0])
I4 = np.eye(4)

# (1.1) and (1.3)
check('(1.1): c_i|0> = 0 for both sites', all(np.allclose(x @ vac, 0) for x in c), 0)
ok13 = all(np.allclose(anti(c[i], cd[j]), (i == j) * I4) and np.allclose(anti(c[i], c[j]), 0)
           and np.allclose(anti(cd[i], cd[j]), 0) for i in range(L) for j in range(L))
check('(1.3) holds for the Jordan-Wigner matrices of two sites', ok13, ok13)
c3 = fermions(3)
ok3 = all(np.allclose(anti(c3[i], c3[j].T), (i == j) * np.eye(8)) and np.allclose(anti(c3[i], c3[j]), 0)
          for i in range(3) for j in range(3))
check('(1.3) holds for three sites too', ok3, ok3)
check('c_0^+ c_1^+|0> = |11>, the order of the conventions sheet', np.allclose(cd[0] @ cd[1] @ vac, ket(L, [1, 1])), 1)

# the key box and the fold: (c_i^+)^2 = 0, n_i^2 = n_i with the eigenvalues 0 and 1, and the antisymmetry
for i in range(L):
    n = cd[i] @ c[i]
    check(f'fold: (c_{i}^+)^2 = 0', np.allclose(cd[i] @ cd[i], 0), 0)
    check(f'fold: c_{i} c_{i}^+ = 1 - n_{i}', np.allclose(c[i] @ cd[i], I4 - n), 0)
    check(f'fold: n_{i}^2 = n_{i}, eigenvalues 0 and 1', np.allclose(n @ n, n)
          and set(np.round(np.linalg.eigvalsh(n), 12)) == {0.0, 1.0}, sorted(set(np.round(np.linalg.eigvalsh(n), 12))))
check('fold: c_1^+ c_0^+|0> = -c_0^+ c_1^+|0>', np.allclose(cd[1] @ cd[0] @ vac, -cd[0] @ cd[1] @ vac), -1)

# the fold: the two sites of (1.2), for both signs of t, since the set of levels does not depend on it
for t in (1.0, -0.7):
    H = t * (cd[0] @ c[1] + cd[1] @ c[0])
    check(f'fold t={t}: H_hop|0> = 0', np.allclose(H @ vac, 0), 0)
    b1 = [cd[0] @ vac, cd[1] @ vac]
    M = np.array([[u @ H @ w for w in b1] for u in b1])
    check(f'fold t={t}: one electron, H_hop is [[0, t], [t, 0]]', np.allclose(M, [[0, t], [t, 0]]), M.tolist())
    check(f'fold t={t}: H_hop takes c_1^+|0> to t c_0^+|0>', np.allclose(H @ b1[1], t * b1[0]), t)
    ev = np.linalg.eigvalsh(M)
    check(f'fold t={t}: the one-electron levels are -|t| and +|t|', np.allclose(ev, [-abs(t), abs(t)]), ev)
    full = cd[0] @ cd[1] @ vac
    check(f'fold t={t}: H_hop c_0^+ c_1^+|0> = 0, the energy of the full state is 0', np.allclose(H @ full, 0), 0)
first = cd[0] @ c[1] @ cd[0] @ cd[1] @ vac
check('fold: c_0^+ c_1 c_0^+ c_1^+|0> = -(c_0^+)^2 c_1 c_1^+|0> = 0',
      np.allclose(first, -cd[0] @ cd[0] @ c[1] @ cd[1] @ vac) and np.allclose(first, 0), 0)
second = cd[1] @ c[0] @ cd[0] @ cd[1] @ vac
check('fold: c_1^+ c_0 c_0^+ c_1^+|0> = (c_1^+)^2|0> - c_1^+ c_0^+ c_0 c_1^+|0> = 0',
      np.allclose(second, cd[1] @ cd[1] @ vac - cd[1] @ cd[0] @ c[0] @ cd[1] @ vac) and np.allclose(second, 0)
      and np.allclose(c[0] @ cd[1] @ vac, -cd[1] @ c[0] @ vac), 0)
# the four energies by sector, 0, -t and +t, 0, from the matrices
t = 1.0
H = t * (cd[0] @ c[1] + cd[1] @ c[0])
N = sum(cd[i] @ c[i] for i in range(L))
sectors = {k: np.round(np.linalg.eigvalsh(H[np.ix_(np.isclose(np.diag(N), k), np.isclose(np.diag(N), k))]), 12).tolist()
           for k in (0, 1, 2)}
check('fold: the energies are 0, -t and +t, and 0 for N = 0, 1, 2', sectors == {0: [0.0], 1: [-1.0, 1.0], 2: [0.0]},
      sectors)

# the quiz of Section 1.6: the full state has the energy 0 = (-t) + (+t), and (c_+^+)^2 = 0 for the level +t
cp = (cd[0] + cd[1]) / np.sqrt(2)
check('quiz 1: c_+^+ = (c_0^+ + c_1^+)/sqrt2 creates the level +t for t>0', np.allclose(H @ cp @ vac, +t * cp @ vac), t)
check('quiz 1: (c_+^+)^2 = 0', np.allclose(cp @ cp, 0), 0)
check('quiz 1: the two-electron sector has one state, at 0 = (-t)+(+t), not -t or 2t',
      sectors[2] == [0.0] and np.isclose(-t + t, 0) and -t not in sectors[2] and 2 * t not in sectors[2], sectors[2])
# the question says t>0: for t>0 the lower level of one electron is -t, on the antisymmetric state, and for t<0 the level
# -t is the upper one, so the feedback "-t belongs to the lower level" needs t>0, while the answer 0 does not
cm = (cd[0] - cd[1]) / np.sqrt(2)
for tt in (1.0, -0.7):
    Ht = tt * (cd[0] @ c[1] + cd[1] @ c[0])
    low = np.linalg.eigvalsh(Ht[np.ix_([1, 2], [1, 2])])[0]
    check(f'quiz 1, t={tt}: the lower one-electron level is {"-t" if tt > 0 else "+t"}, the full state has 0',
          np.isclose(low, -abs(tt)) and np.isclose(low, -tt) == (tt > 0) and np.allclose(Ht @ (cd[0] @ cd[1] @ vac), 0),
          low)
check('quiz 1, t>0: the antisymmetric state (c_0^+ - c_1^+)|0>/sqrt2 has -t', np.allclose(H @ cm @ vac, -t * cm @ vac), -t)

# the problem: <N> = 1 and (Delta N)^2 = 1 in (|0> + c_0^+ c_1^+|0>)/sqrt2, with an even parity in both terms
full = cd[0] @ cd[1] @ vac
check('problem: N c_0^+ c_1^+|0> = 2 c_0^+ c_1^+|0>, N|0> = 0', np.allclose(N @ full, 2 * full) and np.allclose(N @ vac, 0), 2)
psi = (vac + full) / np.sqrt(2)
mN, mN2 = psi @ N @ psi, psi @ N @ N @ psi
check('problem: <N> = 1', np.isclose(mN, 1), mN)
check('problem: <N^2> = 2', np.isclose(mN2, 2), mN2)
check('problem: (Delta N)^2 = 1', np.isclose(mN2 - mN ** 2, 1), mN2 - mN ** 2)
check('problem and Section 1.5: each term has the probability 1/2, the 50% of zero and of two electrons',
      np.isclose((psi @ vac) ** 2, 0.5) and np.isclose((psi @ full) ** 2, 0.5), 0.5)
par = np.diag((-1.0) ** np.diag(N))
check('problem: the parity (-1)^N is +1 in both terms', np.allclose(par @ psi, psi), 1)
P = cd[0] @ cd[1] + c[1] @ c[0]
check('problem: the pairing term c_0^+ c_1^+ + c_1 c_0 is Hermitian', np.allclose(P, P.T), 0)
for s in (+1, -1):
    v = (vac + s * full) / np.sqrt(2)
    check(f'problem: (|0> {"+" if s > 0 else "-"} c_0^+ c_1^+|0>)/sqrt2 is an eigenstate of the pairing term with {s}',
          np.allclose(P @ v, s * v), s)
evP = np.round(np.linalg.eigvalsh(P), 12).tolist()
check('problem: the pairing term has the eigenvalues -1, 0, 0, +1 on the four Fock states', evP == [-1.0, 0.0, 0.0, 1.0], evP)
check('problem: the eigenvalues +1 and -1 are in the even sector, the one-electron states give 0',
      np.allclose(P @ (cd[0] @ vac), 0) and np.allclose(P @ (cd[1] @ vac), 0), 0)

# the boson quiz and the figure: the one-boson levels are -t and +t, two bosons have -2t, 0 and 2t
b = np.diag(np.sqrt([1., 2.]), 1)
b0, b1 = np.kron(b, np.eye(3)), np.kron(np.eye(3), b)
Hb = t * (b0.T @ b1 + b1.T @ b0)
Nb = b0.T @ b0 + b1.T @ b1
eb = {k: np.round(np.linalg.eigvalsh(Hb[np.ix_(np.isclose(np.diag(Nb), k), np.isclose(np.diag(Nb), k))]), 12).tolist()
      for k in (1, 2)}
check('boson quiz: the bosonic operators commute, b_0 b_1 = b_1 b_0', np.allclose(b0 @ b1, b1 @ b0), 0)
check('boson quiz: one boson has the levels -t and +t, as one fermion', eb[1] == [-1.0, 1.0], eb[1])
check('figure: two bosons have -2t, 0 and +2t, two fermions only 0', eb[2] == [-2.0, 0.0, 2.0] and sectors[2] == [0.0], eb[2])
check('boson quiz: (b^+)^2 does not vanish', not np.allclose(b0.T @ b0.T, 0), 0)

# the quiz on (1.3): c_i c_i^+ = 1 - n_i gives 0 on c_i^+|0>, and c_j c_i^+ = -c_i^+ c_j for i != j
for i, j in ((0, 1), (1, 0)):
    occ = cd[i] @ vac
    check(f'quiz 3: c_{i} c_{i}^+ gives 0 on c_{i}^+|0>, not 1', np.allclose(c[i] @ cd[i] @ occ, 0), 0)
    check(f'quiz 3: c_{j} c_{i}^+ = -c_{i}^+ c_{j}', np.allclose(c[j] @ cd[i], -cd[i] @ c[j]), -1)
    lhs, rhs = cd[i] @ c[j] @ (cd[j] @ vac), c[j] @ cd[i] @ (cd[j] @ vac)
    check(f'quiz 3: on c_{j}^+|0>, c_{i}^+ c_{j} gives c_{i}^+|0> and c_{j} c_{i}^+ gives -c_{i}^+|0>',
          np.allclose(lhs, cd[i] @ vac) and np.allclose(rhs, -cd[i] @ vac), 0)
# the closing line of quiz 3: for every pair A, B of the operators c_i, c_i^+ of two sites, AB + BA is 0 or 1, so the
# relations fix BA = -AB + {A, B} when we swap the order, while the product AB itself is not a number, as c_i c_i^+ = 1 - n_i
allops = c + cd
consts = set()
for A in allops:
    for B in allops:
        S = anti(A, B)
        k = S[0, 0]
        assert np.allclose(S, k * I4)
        consts.add(round(float(k), 12))
check('quiz 3: every anticommutator of two of c_0, c_1, c_0^+, c_1^+ is 0 or 1 times the identity', consts == {0.0, 1.0},
      sorted(consts))
check('quiz 3: the product c_0 c_0^+ itself is not a multiple of the identity', not np.allclose(c[0] @ cd[0], (c[0] @ cd[0])[0, 0] * I4),
      np.diag(c[0] @ cd[0]).tolist())
