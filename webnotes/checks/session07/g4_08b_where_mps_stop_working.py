"""Session 7, the numbers that page 08b (Section 7.8b) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The figure quench_entropy.py asserts its own caption, the turn at t = 4 and the
first points of its grid above the three lines, and build.py --verify runs only this folder, so the quench runs here
again on a finer grid. This script holds, in the order of the page: the bound M >= e^S of the key box and the n
singlets of the fold, the times 1.5, 2.5 and 3.5 of the fold and the turn at t = 4 of the caption, the critical point
of the caption, the unitary evolution and the AKLT (6 and 8 sites, and any length), lattice and dimer statements of the two quizzes, and the numbers of
the problem on the strip. It finds the repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session07/g4_08b_where_mps_stop_working.py"""
import itertools
import sys
sys.dont_write_bytecode = True

import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spl
from scipy.sparse.linalg import expm_multiply

LN2 = np.log(2)


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def vn(p):
    p = np.asarray(p)
    p = p[p > 1e-14]
    return float(-np.sum(p * np.log(p)))


# the key box and the fold: S <= log M, so M >= e^S, and a cut through n singlets has S = n log 2 and needs M = 2^n
sing = np.array([0, 1, -1, 0]) / np.sqrt(2)
for n in (1, 2, 3):
    psi = sing
    for _ in range(n - 1):
        psi = np.kron(psi, sing)
    # the sites in the order (a1 b1 a2 b2 ...), the cut separates all a from all b
    t = psi.reshape([2] * (2 * n)).transpose(list(range(0, 2 * n, 2)) + list(range(1, 2 * n, 2))).reshape(2 ** n, 2 ** n)
    w = np.linalg.svd(t, compute_uv=False) ** 2
    rank = int(np.sum(w > 1e-12))
    check('key box and fold, n = %d cut singlets give S = n log 2 and the Schmidt rank 2^n = e^S' % n,
          abs(vn(w) - n * LN2) < 1e-12 and rank == 2 ** n and abs(np.exp(vn(w)) - 2 ** n) < 1e-9, (round(vn(w), 6), rank))

# the quench of the fold and of the caption: 12 sites from all spins up with -J sum sz sz - J sum sx, J = 1
L = 12
sx = sps.csr_matrix(np.array([[0, 1], [1, 0.]]))
sz = sps.csr_matrix(np.diag([1.0, -1]))
op = lambda o, i: sps.kron(sps.kron(sps.identity(2 ** i), o), sps.identity(2 ** (L - i - 1)), format='csr')
Hq = -sum(op(sz, i) @ op(sz, i + 1) for i in range(L - 1)) - sum(op(sx, i) for i in range(L))
p0 = np.zeros(2 ** L, complex)
p0[0] = 1
ts = np.linspace(0, 5, 1001)
traj = expm_multiply(-1j * Hq, p0, start=0, stop=5, num=1001, endpoint=True)
Sq = np.array([vn(np.linalg.svd(p.reshape(64, 64), compute_uv=False) ** 2) for p in traj]) / LN2
imax = int(np.argmax(Sq))
tc = np.array([float(np.interp(k, Sq[:imax], ts[:imax])) for k in (1, 2, 3)])
check('fold, S passes log 2, log 4, log 8 at t = 1.5, 2.5, 3.5 in units of hbar/J, within 0.05',
      np.allclose(tc, [1.5, 2.5, 3.5], atol=0.05) and np.all(np.diff(Sq[:imax]) > 0), tc.round(3))
check('fold, M roughly doubles at each unit of time, the steps between the crossings are 0.9 to 1.1',
      np.all((np.diff(tc) > 0.9) & (np.diff(tc) < 1.1)), np.diff(tc).round(3))
check('caption, it turns over at t = 4, below the 6 bits of half of 12 sites', abs(ts[imax] - 4.0) < 0.01
      and Sq.max() < 6, (ts[imax], round(Sq.max(), 3)))
norms = np.abs(np.linalg.norm(traj, axis=1) - 1).max()
check('first quiz, the evolution is unitary and the norm stays 1', norms < 1e-8, norms)


def tfim_gap(L, h):
    Ho = lambda o, i: sps.kron(sps.kron(sps.identity(2 ** i), o), sps.identity(2 ** (L - i - 1)), format='csr')
    H = -sum(Ho(sz, i) @ Ho(sz, (i + 1) % L) for i in range(L)) - h * sum(Ho(sx, i) for i in range(L))
    w = np.linalg.eigvalsh(H.toarray())               # the whole spectrum of the ring, at most 1024 levels
    return w[1] - w[0]


# the caption: J = h is the critical point of -J sum sz sz - h sum sx. On a ring the lowest gap closes as 1/L there,
# and stays near 2|h - J| away from it (here h = 2J, deep in the paramagnet)
g_crit = {Lr: tfim_gap(Lr, 1.0) for Lr in (6, 8, 10)}
g_para = {Lr: tfim_gap(Lr, 2.0) for Lr in (6, 8, 10)}
check('caption, h = J is the critical point, L times the gap stays constant there and the gap stays near 2|h - J| at h = 2J',
      max(Lr * g for Lr, g in g_crit.items()) / min(Lr * g for Lr, g in g_crit.items()) < 1.05
      and all(abs(g - 2.0) < 0.05 for g in g_para.values()), ({k: round(v, 4) for k, v in g_crit.items()},
                                                               {k: round(v, 4) for k, v in g_para.items()}))

# second quiz, the AKLT chain of spins 1 is an exact MPS with M = 2 (the matrices of the sheet), on 6 sites and on the 8
# sites of the sheet, with sparse matrices. The matrices do not depend on the length, so the same M = 2 holds for any L
Sz1 = sps.csr_matrix(np.diag([1.0, 0, -1]))
Sp1 = sps.csr_matrix(np.sqrt(2) * np.array([[0, 1, 0], [0, 0, 1], [0, 0, 0.]]))
Sm1 = Sp1.T.tocsr()
spl_ = np.array([[0, 1], [0, 0.]])
A = {+1: np.sqrt(2 / 3) * spl_, 0: -np.sqrt(1 / 3) * np.diag([1.0, -1]), -1: -np.sqrt(2 / 3) * spl_.T}
aklt = {}
for Lk in (6, 8):
    kr = lambda o, i: sps.kron(sps.kron(sps.identity(3 ** i), o), sps.identity(3 ** (Lk - i - 1)), format='csr')
    Hak = sps.csr_matrix((3 ** Lk, 3 ** Lk))
    for i in range(Lk - 1):
        SS = kr(Sz1, i) @ kr(Sz1, i + 1) + 0.5 * (kr(Sp1, i) @ kr(Sm1, i + 1) + kr(Sm1, i) @ kr(Sp1, i + 1))
        Hak = Hak + SS + SS @ SS / 3
    psi = np.array([(np.array([1, 0.]) @ np.linalg.multi_dot([A[m] for m in conf]) @ np.array([0, 1.]))
                    for conf in itertools.product((+1, 0, -1), repeat=Lk)])
    psi /= np.linalg.norm(psi)
    eak = psi @ (Hak @ psi)
    res = np.linalg.norm(Hak @ psi - eak * psi)
    e_low = spl.eigsh(Hak, k=1, which='SA')[0][0]
    aklt[Lk] = (eak, res, e_low)
check('second quiz, the AKLT MPS with M = 2 is a ground state at -2/3 (L - 1) on 6 and on 8 sites',
      all(r < 1e-10 and abs(e + 2 / 3 * (Lk - 1)) < 1e-10 and abs(el - e) < 1e-8 for Lk, (e, r, el) in aklt.items()),
      {Lk: (round(e, 8), float('%.1e' % r)) for Lk, (e, r, el) in aklt.items()})

# second quiz, "for 100 sites or for 10000": the statement for any length. The bond term S.S + (S.S)^2/3 is 2 P2 - 2/3, with
# P2 the projector on the total spin 2 of the two sites, and P2 removes the product A^a A^b of two neighboring matrices
# for every pair of matrix indices. So every bond term gives -2/3 on the MPS, whatever the length and the end vectors,
# and -2/3 is its lowest value, so the MPS with M = 2 is a ground state at -2/3 (L - 1) for every L
SS2 = (np.kron(Sz1.toarray(), Sz1.toarray()) + 0.5 * (np.kron(Sp1.toarray(), Sm1.toarray())
                                                      + np.kron(Sm1.toarray(), Sp1.toarray())))
wss, vss = np.linalg.eigh(SS2)
P2 = vss[:, np.abs(wss - 1) < 1e-9] @ vss[:, np.abs(wss - 1) < 1e-9].T
hb = SS2 + SS2 @ SS2 / 3
T2 = np.array([A[a] @ A[b] for a in (+1, 0, -1) for b in (+1, 0, -1)]).reshape(9, 4)
check('second quiz, for any length, the bond term is 2 P2 - 2/3 and P2 removes every product of two AKLT matrices',
      np.abs(hb - (2 * P2 - 2 / 3 * np.eye(9))).max() < 1e-12 and int(round(np.trace(P2))) == 5
      and np.abs(P2 @ T2).max() < 1e-12 and abs(np.linalg.eigvalsh(hb)[0] + 2 / 3) < 1e-12,
      (int(round(np.trace(P2))), float('%.1e' % np.abs(P2 @ T2).max())))

# second quiz, a cut through the middle of a 10 x 10 square lattice crosses ten bonds
bonds = [((x, y), (x + 1, y)) for x in range(9) for y in range(10)] + [((x, y), (x, y + 1)) for x in range(10) for y in range(9)]
cut = sum(1 for a, b in bonds if (a[0] < 5) != (b[0] < 5))
check('second quiz, the cut through the middle of a 10 x 10 lattice crosses 10 bonds', cut == 10, cut)

# second quiz, a product of dimers on 8 sites: every cut crosses at most one singlet, S <= log 2 and the rank is <= 2
dim = np.kron(np.kron(sing, sing), np.kron(sing, sing))
ent = []
ranks = []
for l in range(1, 8):
    w = np.linalg.svd(dim.reshape(2 ** l, -1), compute_uv=False) ** 2
    ent.append(vn(w))
    ranks.append(int(np.sum(w > 1e-12)))
check('second quiz, the dimer product has S <= log 2 at every cut and an exact MPS with M = 2',
      max(ent) < LN2 + 1e-12 and max(ranks) == 2, (np.round(np.array(ent) / LN2, 6), ranks))

# the problem: M = 2^W, 2 M^2 numbers per bulk tensor, 16 bytes per number
M10, M20 = 2 ** 10, 2 ** 20
n10, n20 = 2 * M10 ** 2, 2 * M20 ** 2
check('problem, W = 10 gives M = 1024 and 2M^2 = 2.1e6', M10 == 1024 and abs(n10 / 1e6 - 2.1) < 0.05, n10)
check('problem, W = 20 gives M = 2^20, about 1e6, and 2M^2 = 2.2e12, which is 35 TB at 16 bytes',
      abs(M20 / 1e6 - 1) < 0.05 and abs(n20 / 1e12 - 2.2) < 0.05 and abs(16 * n20 / 1e12 - 35) < 0.5, (M20, n20, 16 * n20))
check('problem, one tensor is about 1e6 times larger for the strip twice as wide', abs(n20 / n10 / 1e6 - 1) < 0.05,
      n20 // n10)


# the notebook box and the try-it, corrected on 2026-11-22. The open Heisenberg chain is gapless, so the entropy at its
# center grows slowly with L on each parity of L/2, and it does not saturate as the gapped chain of Section 7.6 does.
# Exact diagonalization in the sector S^z = 0, with site i as bit i.
def heis_open(L):
    st = np.array([s for s in range(2 ** L) if bin(s).count('1') == L // 2], dtype=np.int64)
    idx = -np.ones(2 ** L, dtype=np.int64)
    idx[st] = np.arange(len(st))
    rows, cols, vals, diag = [], [], [], np.zeros(len(st))
    for i in range(L - 1):
        a, b = (st >> i) & 1, (st >> (i + 1)) & 1
        diag += np.where(a == b, 0.25, -0.25)
        k = np.where(a != b)[0]
        rows.append(k); cols.append(idx[st[k] ^ (3 << i)]); vals.append(np.full(len(k), 0.5))
    H = sps.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(len(st),) * 2)
    e, v = spl.eigsh(H + sps.diags(diag), k=1, which='SA', tol=1e-12)
    psi = np.zeros(2 ** L)
    psi[st] = v[:, 0]
    return psi


def cut_weights(psi, L, l):
    return np.linalg.svd(psi.reshape(2 ** (L - l), 2 ** l), compute_uv=False) ** 2


cen = {L: vn(cut_weights(heis_open(L), L, L // 2)) for L in (8, 10, 12, 14, 16, 18)}
check('notebook box, the center of the open Heisenberg chain grows with L on each parity of L/2, 0.457, 0.537, 0.592 and '
      '0.738, 0.762, 0.784', cen[8] < cen[12] < cen[16] and cen[10] < cen[14] < cen[18]
      and np.allclose([cen[L] for L in (8, 12, 16, 10, 14, 18)], [0.457, 0.537, 0.592, 0.738, 0.762, 0.784], atol=5e-4),
      {L: round(x, 4) for L, x in cen.items()})
# the c/6 of the notebook for a cut with one end, from free fermions with c = 1, the XX chain: the left half of an open
# chain of L = 100 to 800 sites grows with the slope 0.169, close to 1/6
half = []
for L in (100, 200, 400, 800):
    Hf = -np.diag(np.ones(L - 1), 1); Hf = Hf + Hf.T
    w, v = np.linalg.eigh(Hf)
    Cf = v[:, :L // 2] @ v[:, :L // 2].T
    nu = np.clip(np.linalg.eigvalsh(Cf[:L // 2, :L // 2]), 1e-15, 1 - 1e-15)
    half.append(float(-np.sum(nu * np.log(nu) + (1 - nu) * np.log(1 - nu))))
slope6 = np.polyfit(np.log([100, 200, 400, 800]), half, 1)[0]
check('notebook box, a cut with one end grows as (c/6) ln L, the slope of the XX chain is 0.169 against 1/6',
      abs(slope6 - 1 / 6) < 5e-3, round(slope6, 4))
nbsrc = open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', '..',
                                        'jupyter-notebooks', 'session7.ipynb'), encoding='utf-8').read()
check('notebook box, the notebook writes (c/6) ln L with c = 1 for the Heisenberg chain',
      r'\\frac{c}{6}\\ln L' in nbsrc and 'which is $c=1$ for the Heisenberg chain' in nbsrc, 'c/6')
# the try-it, the cut of the cell after L/2 + 1 = 6 sites of 10: the exact entropy is 0.49, below ln 2, and the two
# largest Schmidt weights alone give 0.18, far below ln 2 (dmrgpy with maxm = 2 gives 0.271 on the conventions sheet)
w10 = cut_weights(heis_open(10), 10, 6)
two = w10[:2] / w10[:2].sum()
check('try-it, 10 sites at the cut of the cell: the exact 0.492 is below ln chi for every chi >= 2, the two largest weights '
      'give 0.176, far below ln 2', abs(vn(w10) - 0.4923) < 5e-4 and vn(w10) < LN2 and abs(vn(two) - 0.176) < 1e-3
      and vn(two) < 0.5 * LN2, (round(vn(w10), 4), round(vn(two), 4)))
print('all checks of page 08b passed')
