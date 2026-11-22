"""Session 8, the numbers that page 06 (Section 8.6) quotes, checked in the order of the page.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The figure rvb_plaquette asserts the numbers of its caption, and this script
asserts them again with the order of the pairs that the fold writes. The fermion operators carry the Jordan-Wigner
signs, with the modes (site, spin) in the order 0 up, 0 down, 1 up, ... The plaquette has the sites 0, 1, 2, 3 around
the square and J = 1 on its four bonds, and a singlet (ij) is (|up_i dn_j> - |dn_i up_j>)/sqrt 2 in the order of its
pair, as on the conventions sheet. The second quiz is checked on frozen coverings of an open dimerized chain of 12
sites, with <H> of each product state computed exactly. It finds the repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session08/g2_06_rvb_wavefunction.py"""
import os, sys, itertools
sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
assert os.path.exists(os.path.join(REPO, 'webnotes', 'pages', 'session08'))

import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# fermions of L sites with spin, Jordan-Wigner
def annihilators(nmodes):
    a = np.array([[0, 1], [0, 0]])
    zs = np.diag([1, -1])
    out = []
    for m in range(nmodes):
        mat = np.eye(1)
        for j in range(nmodes):
            mat = np.kron(mat, zs if j < m else (a if j == m else np.eye(2)))
        out.append(mat)
    return out


# the key box, the problem and the third quiz: n(2-n) on the four states of one site
c = annihilators(2)
n = sum(ci.T @ ci for ci in c)
I = np.eye(4)
pg1 = n @ (2 * I - n)
check('key box and problem, n on the four states is 0, 1, 1, 2', sorted(np.diag(n)) == [0, 1, 1, 2], np.diag(n))
check('key box, problem and third quiz, n(2-n) is 1 on one fermion and 0 on none or two',
      np.allclose(pg1, np.diag(np.diag(pg1)))
      and all(abs(pg1[k, k] - (1 if round(n[k, k]) == 1 else 0)) < 1e-12 for k in range(4)), np.diag(pg1))
check('problem, n(2-n) is a projector', np.allclose(pg1 @ pg1, pg1), np.diag(pg1 @ pg1))
dbl = n @ (n - I) / 2
emp = I - n
check('third quiz, n(n-1)/2 is 0, 0, 1 for n = 0, 1, 2',
      all(abs(dbl[k, k] - {0: 0, 1: 0, 2: 1}[int(round(n[k, k]))]) < 1e-12 for k in range(4)), np.diag(dbl))
check('third quiz, 1-n is 1, 0, -1 for n = 0, 1, 2, so it is not a projector',
      all(abs(emp[k, k] - (1 - n[k, k])) < 1e-12 for k in range(4)) and not np.allclose(emp @ emp, emp), np.diag(emp))

# the problem: P_G on four sites keeps 2^4 = 16 of the 4^4 = 256 states
c8 = annihilators(8)
ns = [c8[2 * i].T @ c8[2 * i] + c8[2 * i + 1].T @ c8[2 * i + 1] for i in range(4)]
PG = np.eye(256)
for ni in ns:
    PG = PG @ ni @ (2 * np.eye(256) - ni)
check('problem, the factors of different sites commute', all(np.allclose(a @ b, b @ a) for a in ns for b in ns), 'ok')
check('problem, P_G of four sites is a projector of rank 16 out of 256', np.allclose(PG @ PG, PG)
      and int(round(np.trace(PG))) == 16 and PG.shape[0] == 4 ** 4 and 2 ** 4 == 16, int(round(np.trace(PG))))

# the fold: the plaquette of four spins
up, dn = np.array([1., 0]), np.array([0, 1.])
S = [np.array([[0, .5], [.5, 0]]), np.array([[0, -.5j], [.5j, 0]]), np.diag([.5, -.5])]


def kron(vs):
    out = np.ones(1)
    for v in vs:
        out = np.kron(out, v)
    return out


def covering(pairs):
    psi = np.zeros(16)
    for flips in itertools.product((0, 1), repeat=len(pairs)):
        spins, sign = [None] * 4, 1
        for (i, j), f in zip(pairs, flips):
            spins[i], spins[j] = (dn, up) if f else (up, dn)
            sign *= -1 if f else 1
        psi += sign * kron(spins) / 2
    return psi


def op(o, i):
    return np.kron(np.kron(np.eye(2 ** i), o), np.eye(2 ** (3 - i)))


def SS(i, j):
    return sum(op(o, i) @ op(o, j) for o in S).real


def square(ops):
    tot = [sum(op(o, i) for i in ops) for o in S]
    return sum(t @ t for t in tot).real


H = sum(SS(i, (i + 1) % 4) for i in range(4))
a = covering([(0, 1), (2, 3)])
b = covering([(1, 2), (3, 0)])
b2 = covering([(1, 2), (0, 3)])
d = covering([(0, 2), (1, 3)])
check('fold, a single covering has -3/2, the two covered bonds give -3/4 each and the bond (12) gives 0',
      abs(a @ H @ a + 1.5) < 1e-12 and abs(b @ H @ b + 1.5) < 1e-12 and abs(a @ SS(1, 2) @ a) < 1e-12
      and abs(a @ SS(0, 1) @ a + 0.75) < 1e-12, a @ H @ a)
S2, SA2, SB2 = square(range(4)), square([0, 2]), square([1, 3])
check('fold, H = (S^2 - S_A^2 - S_B^2)/2 with A = {0, 2} and B = {1, 3}', np.allclose(H, (S2 - SA2 - SB2) / 2), 'ok')
w = np.linalg.eigvalsh(H)
check('fold, the lowest level is -2, nondegenerate', abs(w[0] + 2) < 1e-12 and w[1] > w[0] + 0.5, w[:2])
w2 = np.round(np.linalg.eigvalsh(S2), 8)
check('fold, four spins one half have S = 0 twice', int((w2 == 0).sum()) == 2, int((w2 == 0).sum()))
check('fold, <a|b> = +1/2 with (12)(30), and -1/2 with (12)(03)', abs(a @ b - 0.5) < 1e-12 and abs(a @ b2 + 0.5) < 1e-12,
      (a @ b, a @ b2))
p, m = a + b, a - b
Ep, Em = p @ H @ p / (p @ p), m @ H @ m / (m @ m)
check('fold, |a> + |b> is at -2 with S_A = S_B = 1 and S = 0, |a> - |b> is at 0', abs(Ep + 2) < 1e-12 and abs(Em) < 1e-12
      and abs(p @ SA2 @ p / (p @ p) - 2) < 1e-12 and abs(p @ SB2 @ p / (p @ p) - 2) < 1e-12
      and abs(p @ S2 @ p) < 1e-12, (Ep, Em))
mn = m / np.linalg.norm(m)
check('fold, |a> - |b> is the product of the singlets (02)(13) on the diagonals, with S_A = S_B = 0',
      abs(abs(mn @ d) - 1) < 1e-12 and abs(d @ SA2 @ d) < 1e-12 and abs(d @ H @ d) < 1e-12, mn @ d)
p2, m2 = a + b2, a - b2
check('fold, with (12)(03) the two combinations exchange their roles',
      abs(p2 @ H @ p2 / (p2 @ p2)) < 1e-12 and abs(m2 @ H @ m2 / (m2 @ m2) + 2) < 1e-12, 'ok')

# the second quiz: a frozen covering of the dimerized chain, with J on the strong bonds (2n, 2n+1) and J' on the weak
# bonds (2n+1, 2n+2). Two free spins, both up, sit at p = 2 and q = 2b + 1, so d = q - p apart, and the sites between
# them are paired on the weak bonds. We compute <H> of this product state exactly on the open chain of 12 sites.
L = 12


def apply(o, i, psi):
    t = np.tensordot(o, psi.reshape([2] * L), axes=([1], [i]))
    return np.moveaxis(t, 0, i).reshape(-1)


def product(pairs, free):
    psi = np.zeros(2 ** L)
    for flips in itertools.product((0, 1), repeat=len(pairs)):
        spins, sign = [up] * L, 1.0
        for (i, j), f in zip(pairs, flips):
            spins[i], spins[j] = (dn, up) if f else (up, dn)
            sign *= -1 if f else 1
        psi += sign * kron(spins)
    return psi / np.linalg.norm(psi)


def energy(psi, J, Jp):
    out = 0.0
    for i in range(L - 1):
        c = J if i % 2 == 0 else Jp
        out += c * sum((psi.conj() @ apply(o, i, apply(o, i + 1, psi))).real for o in S)
    return out


full = product([(2 * n, 2 * n + 1) for n in range(L // 2)], [])
worst, worst_count, worst_triplet, tension = 0.0, 0, 0.0, {}
for J, Jp in ((1.0, 0.0), (1.0, 0.5), (1.0, 1.0)):
    costs = []
    for bq in range(1, 6):
        p, q = 2, 2 * bq + 1
        d = q - p
        pairs = [(2 * n, 2 * n + 1) for n in range(L // 2) if 2 * n + 1 < p or 2 * n > q]
        pairs += [(k, k + 1) for k in range(p + 1, q, 2)]
        broken = sum(1 for n in range(L // 2) if (2 * n, 2 * n + 1) not in pairs)
        worst_count = max(worst_count, abs(broken - (d + 1) // 2))
        cost = energy(product(pairs, [p, q]), J, Jp) - energy(full, J, Jp)
        if d == 1:                      # the two free spins on one strong bond are its triplet, which costs J
            worst_triplet = max(worst_triplet, abs(cost - J))
            continue
        worst = max(worst, abs(cost - 3 / 8 * ((J - Jp) * d + (J + Jp))))
        costs.append(cost)
    tension[Jp] = np.round(np.diff(costs) / 2, 9)
check('second quiz, free spins d apart in a frozen covering leave (d + 1)/2 strong bonds without a singlet, d = 1 to 9',
      worst_count == 0, worst_count)
check('second quiz, at d = 1 the two free spins are the triplet of one bond, which costs J', worst_triplet < 1e-12,
      worst_triplet)
check('second quiz, for d = 3 to 9 the cost is (3/8)((J - J\')d + J + J\'), linear in d, at J\' = 0, 0.5J and J',
      worst < 1e-12, worst)
check('second quiz, the cost grows by 3(J - J\')/8 per site, and does not grow for equal bonds',
      all(np.allclose(tension[Jp], 3 / 8 * (1 - Jp)) for Jp in tension) and np.allclose(tension[1.0], 0), tension)
# the last site, 11, stays free in both states, next to a singlet, so it adds nothing to the difference
before = product([(1, 2)] + [(k, k + 1) for k in range(3, L - 1, 2)], [0, L - 1])
after = product([(0, 1)] + [(k, k + 1) for k in range(3, L - 1, 2)], [2, L - 1])
check('second quiz, re-pairing one singlet moves the free spin by two sites, from 0 to 2, at no cost for equal bonds',
      abs(energy(before, 1.0, 1.0) - energy(after, 1.0, 1.0)) < 1e-12
      and abs(apply(S[2], 0, before) @ before - 0.5) < 1e-12 and abs(apply(S[2], 2, after) @ after - 0.5) < 1e-12,
      (energy(before, 1.0, 1.0), energy(after, 1.0, 1.0)))

# the problem, on N sites: P_G keeps 2^N of the 4^N states, the fraction 2^-N
ranks = {}
for Ns in range(1, 6):
    cN = annihilators(2 * Ns)
    nN = [np.diag(cN[2 * i].T @ cN[2 * i] + cN[2 * i + 1].T @ cN[2 * i + 1]) for i in range(Ns)]
    pg = np.prod([x * (2 - x) for x in nN], axis=0)
    ranks[Ns] = (int(round(pg.sum())), len(pg))
check('problem, P_G keeps 2^N of the 4^N states for N = 1 to 5, the fraction 2^-N',
      all(r == 2 ** k and t == 4 ** k and abs(r / t - 2.0 ** -k) < 1e-15 for k, (r, t) in ranks.items()), ranks)

# decided on 2026-11-22, old text of the page: the first feedback of the first quiz writes the singlet pairing with the
# f operators of its question, and this pairing commutes with the three components of the spin of the site
a_ = np.array([[0.0, 1.0], [0.0, 0.0]]); z_ = np.diag([1.0, -1.0])
fu_, fd_ = np.kron(a_, np.eye(2)), np.kron(z_, a_)
pair = fu_.T @ fd_.T - fd_.T @ fu_.T
PA = [np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]])]
ff = (fu_, fd_)
Sf_ = [0.5 * sum(P_[x, y] * ff[x].T @ ff[y] for x in range(2) for y in range(2)) for P_ in PA]
check('decided, first quiz: Delta(f^dag_up f^dag_dn - f^dag_dn f^dag_up) commutes with S^x, S^y and S^z of the site',
      max(np.abs(s_ @ pair - pair @ s_).max() for s_ in Sf_) < 1e-14 and np.abs(pair).max() > 1, 'ok')
