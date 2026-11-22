"""Session 7, the numbers and statements that page 09 (Section 7.9) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. This script holds, in the order of the page: the bond MD of the key box and of
the fold, from the MPO of the Heisenberg chain acting on a random MPS, the D = 5 of that MPO, the Schmidt rank of the
new state, at most MD, which is 12 for the Heisenberg MPO on an MPS with M = 4 of 10 sites and reaches MD = 20 for a
generic MPO, the product case M = D = 1, the dropped weight of the truncation before the state is normalized again and
that no state with M Schmidt terms is closer, the first quiz on product states, the counts of the second quiz, the free
legs of the three diagrams of the third quiz counted on what _g4_nets.build draws, and the numbers of the problem. It
finds the repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session07/g4_09_tensor_diagrams.py"""
import itertools
import os
import sys
sys.dont_write_bytecode = True

import numpy as np
import scipy.sparse as sps

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, '..', '..', 'figures', 'session07')
sys.path.insert(0, FIG)
sys.path.insert(0, os.path.join(FIG, '..'))


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


SP = np.array([[0, 1], [0, 0.]])
SM = SP.T
SZ = np.diag([0.5, -0.5])
SX = (SP + SM) / 2
SY = (SP - SM) / 2j
I2 = np.eye(2)


def site(o, i, L):
    m = np.eye(1)
    for j in range(L):
        m = np.kron(m, o if j == i else I2)
    return m


def heis(L):
    return sum(site(s, i, L) @ site(s, i + 1, L) for i in range(L - 1) for s in (SX, SY, SZ)).real


# the MPO of the Heisenberg chain, W[a, b, s, s'], with I, S+, S-, Sz in the first column and S-/2, S+/2, Sz, I in the
# last row, as on the sheet of the session
W = np.zeros((5, 5, 2, 2))
W[0, 0] = W[4, 4] = I2
W[1, 0], W[2, 0], W[3, 0] = SP, SM, SZ
W[4, 1], W[4, 2], W[4, 3] = SM / 2, SP / 2, SZ
L = 6
Wl, Wr = W[4:5], W[:, 0:1]                                     # the left end is the last row, the right end the first column
mpo = [Wl] + [W] * (L - 2) + [Wr]
T = np.ones((1, 1, 1))
for w in mpo:
    T = np.einsum('aio,abst->bisot', T, w).reshape(w.shape[1], T.shape[1] * 2, T.shape[2] * 2)
Hmpo = T[0]
Hd = heis(L)
check('problem, the MPO with D = 5 gives the Heisenberg chain of 6 sites exactly', np.abs(Hmpo - Hd).max() < 1e-12,
      np.abs(Hmpo - Hd).max())
op_rank = np.linalg.matrix_rank(Hd.reshape(8, 8, 8, 8).transpose(0, 2, 1, 3).reshape(64, 64), tol=1e-10)
check('problem, 5 is the operator Schmidt rank of H at the center, so D = 5 is the smallest', op_rank == 5, op_rank)

# the key box and the fold: the MPO on a random MPS with M = 4 gives an MPS whose bonds are M D = 20, and the result is
# H|psi>
rng = np.random.default_rng(3)
M = 4
Dm = [1] + [min(M, 2 ** min(k, L - k)) for k in range(1, L)] + [1]
A = [rng.normal(size=(Dm[k], 2, Dm[k + 1])) for k in range(L)]
psi = np.ones((1, 1))
for a in A:
    psi = np.einsum('xa,asb->xsb', psi, a).reshape(-1, a.shape[2])
psi = psi[:, 0]
N = []
for w, a in zip(mpo, A):
    n = np.einsum('abst,ctd->acsbd', w, a)                    # N^s_{(a c),(b d)} = sum_t W^{st}_{ab} M^t_{cd}
    N.append(n.reshape(w.shape[0] * a.shape[0], 2, w.shape[1] * a.shape[2]))
bonds = [n.shape[2] for n in N[:-1]]
out = np.ones((1, 1))
for n in N:
    out = np.einsum('xa,asb->xsb', out, n).reshape(-1, n.shape[2])
out = out[:, 0]
check('key box and fold, the MPO on an MPS with M = 4 has the bulk bonds M D = 20 and gives H|psi>',
      max(bonds) == 20 and bonds[2] == 20 and np.abs(out - Hd @ psi).max() < 1e-10, (bonds, np.abs(out - Hd @ psi).max()))



def mps_full(As):
    c = np.ones((1, 1))
    for a in As:
        c = np.einsum('xa,asb->xsb', c, a).reshape(-1, a.shape[2])
    return c[:, 0]


def apply_mpo(ws, As):
    out = []
    for w, a in zip(ws, As):
        n = np.einsum('abst,ctd->acsbd', w, a)
        out.append(n.reshape(w.shape[0] * a.shape[0], 2, w.shape[1] * a.shape[2]))
    return out


def schmidt_ranks(v, n):
    return [int(np.linalg.matrix_rank(v.reshape(2 ** l, -1), tol=1e-10 * np.linalg.norm(v))) for l in range(1, n)]


def sparse_heis(n):
    o = lambda m, i: sps.kron(sps.kron(sps.identity(2 ** i), sps.csr_matrix(m)), sps.identity(2 ** (n - i - 1)), format='csr')
    return sum(o(SZ, i) @ o(SZ, i + 1) + 0.5 * (o(SP, i) @ o(SM, i + 1) + o(SM, i) @ o(SP, i + 1)) for i in range(n - 1))


# the key box and the fold: the new state has at most M D Schmidt terms at a bond, and it can have fewer. On a random MPS
# with M = 4 of 10 sites the Heisenberg MPO gives the bond 20 and the largest Schmidt rank 12, and a generic MPO with
# D = 5 reaches M D = 20 at the center
L10 = 10
D10 = [1] + [min(M, 2 ** min(k, L10 - k)) for k in range(1, L10)] + [1]
A10 = [rng.normal(size=(D10[k], 2, D10[k + 1])) for k in range(L10)]
psi10 = mps_full(A10)
heis10 = [W[4:5]] + [W] * (L10 - 2) + [W[:, 0:1]]
N10 = apply_mpo(heis10, A10)
hpsi10 = mps_full(N10)
r_heis = schmidt_ranks(hpsi10, L10)
Wg = rng.normal(size=(5, 5, 2, 2))
gen10 = [Wg[0:1]] + [Wg] * (L10 - 2) + [Wg[:, 0:1]]
r_gen = schmidt_ranks(mps_full(apply_mpo(gen10, A10)), L10)
bonds10 = [n.shape[2] for n in N10[:-1]]
check('key box and fold, at most M D Schmidt terms: the Heisenberg MPO on M = 4 of 10 sites has the bond 20 and rank 12, '
      'a generic MPO with D = 5 reaches 20',
      np.abs(hpsi10 - sparse_heis(L10) @ psi10).max() < 1e-10 and max(bonds10) == 20 and max(r_heis) == 12
      and max(r_gen) == 20 and all(r <= b for r, b in zip(r_heis + r_gen, bonds10 + bonds10)), (bonds10, r_heis, r_gen))
# the fold, corrected on 2026-11-22: "the bonds in the bulk are 20", since the two end bonds are 2 x 5 = 10
check('fold, the joined bonds are 10 at the two ends and 20 in the bulk, and the Schmidt ranks are 2, 4, 8, 12, ..., 2',
      bonds10 == [10] + [20] * 7 + [10] and r_heis == [2, 4, 8, 12, 12, 12, 8, 4, 2], (bonds10, r_heis))

# the fold, the product case: a product state, M = 1, and the product operator prod sigma^x, D = 1, give a product state
prod = np.ones(1)
for _ in range(L):
    v = rng.normal(size=2)
    prod = np.kron(prod, v)
flip = np.ones((1, 1))
for _ in range(L):
    flip = np.kron(flip, 2 * SX)
res = flip @ prod
ranks = [np.linalg.matrix_rank(res.reshape(2 ** l, -1), tol=1e-10) for l in range(1, L)]
check('fold, M = 1 and D = 1 give again a product state, Schmidt rank 1 at every bond', max(ranks) == 1, ranks)

# the fold: truncating the Schmidt form to M terms, the squared distance before the state is normalized again is the
# dropped weight, and no state with M Schmidt terms is closer. The second part is the Eckart-Young theorem, tested by an
# alternating least-squares minimization of |C - X Y|^2 over all X (8 x M) and Y (M x 8) from 50 random starts
x = Hd @ psi
x /= np.linalg.norm(x)
C = x.reshape(8, 8)
U, s, Vt = np.linalg.svd(C)
Mk = 3
Ct = (U[:, :Mk] * s[:Mk]) @ Vt[:Mk]
dist2 = np.linalg.norm(C - Ct) ** 2
eps = np.sum(s[Mk:] ** 2)
best = np.inf
for _ in range(50):
    X = rng.normal(size=(8, Mk))
    for _it in range(300):
        Y = np.linalg.lstsq(X, C, rcond=None)[0]
        X = np.linalg.lstsq(Y.T, C.T, rcond=None)[0].T
    best = min(best, np.linalg.norm(C - X @ Y) ** 2)
ren = np.linalg.norm(C - Ct / np.linalg.norm(Ct)) ** 2
check('fold, before it is normalized again the squared distance is the dropped weight, and 50 minimizations over all '
      'states with 3 Schmidt terms find nothing closer; normalized again it is 2 - 2 sqrt(1 - eps), a little more',
      abs(dist2 - eps) < 1e-12 and best >= eps - 1e-12 and abs(best - eps) < 1e-9
      and abs(ren - (2 - 2 * np.sqrt(1 - eps))) < 1e-12 and ren > eps, (round(eps, 6), round(best, 6), round(ren, 6)))

# the first quiz: on a product state, M = 1, a product operator, D = 1, gives again Schmidt rank 1 (the fold above), where
# M + D would be 2. A generic MPO with D = 5 gives a bond as large as 1 x 5 = 5, where M^D would be 1, and the MPO of the
# Heisenberg chain gives 3 at the center
prod6 = [rng.normal(size=(1, 2, 1)) for _ in range(L)]
gen6 = [Wg[0:1]] + [Wg] * (L - 2) + [Wg[:, 0:1]]
r_gen6 = schmidt_ranks(mps_full(apply_mpo(gen6, prod6)), L)
r_heis6 = schmidt_ranks(mps_full(apply_mpo(mpo, prod6)), L)
check('first quiz, M = D = 1 gives rank 1 and not M + D = 2, and on a product state a generic MPO with D = 5 gives the '
      'bond 5 = 1 x 5 and not 1^5 = 1 (the Heisenberg MPO gives 3)',
      max(ranks) == 1 and max(r_gen6) == 5 and max(r_heis6) == 3 and 1 ** 5 == 1, (ranks, r_gen6, r_heis6))
# the second quiz: one number per combination of the indices
count = lambda dims: sum(1 for _ in itertools.product(*[range(d) for d in dims]))
check('second quiz, three legs of 4 give 64, legs 2,2,2 give 8 and not 6, four legs of 4 give 256, the sum is 12',
      count((4, 4, 4)) == 64 and count((2, 2, 2)) == 8 and 2 + 2 + 2 == 6 and count((4,) * 4) == 256 and 4 + 4 + 4 == 12,
      (count((4, 4, 4)), count((2, 2, 2)), count((4,) * 4)))
# the third quiz: the free legs of the three diagrams, counted on what _g4_nets.build draws, with no file written. A leg
# is a vertical line, and one of its ends is free when it touches no circle and no square
import _g4_nets as nets  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402


def free_ends(ax):
    shapes = []
    for p in ax.patches:
        if isinstance(p, Circle):
            shapes.append(('c', p.center[0], p.center[1], p.radius))
        elif isinstance(p, Rectangle):
            shapes.append(('r', p.get_x() + p.get_width() / 2, p.get_y() + p.get_height() / 2, p.get_width() / 2))

    def touches(x, y):
        for kind, cx, cy, r in shapes:
            if kind == 'c' and abs(np.hypot(x - cx, y - cy) - r) < 1e-9:
                return True
            if kind == 'r' and abs(x - cx) <= r + 1e-9 and abs(abs(y - cy) - r) < 1e-9:
                return True
        return False
    n = 0
    for line in ax.lines:
        xs, ys = line.get_xdata(), line.get_ydata()
        if xs[0] != xs[1]:
            continue
        n += sum(1 for y in ys if not touches(xs[0], y))
    return n


nf = {}
for kind in ('ket', 'norm', 'hpsi'):
    fig, ax, counted = nets.build(kind)
    nf[kind] = (free_ends(ax), counted)
    nets.plt.close(fig)
check('third quiz, the drawn diagrams have 4, 0 and 4 free legs, so 2^4 = 16 entries, a number, and 16 entries',
      nf == {'ket': (4, 4), 'norm': (0, 0), 'hpsi': (4, 4)} and 2 ** nf['ket'][0] == 16 and 2 ** nf['hpsi'][0] == 16, nf)
# the third quiz: a chain of four sites, the open diagram has 2^4 = 16 entries, the closed one is <psi|psi>
L4 = 4
A4 = [rng.normal(size=(d1, 2, d2)) for d1, d2 in ((1, 2), (2, 2), (2, 2), (2, 1))]
c = mps_full(A4)
E = np.ones((1, 1))
for a in A4:
    E = np.einsum('ab,asc,bsd->cd', E, a, a.conj())          # the transfer of the ket and the bra through one site
H4 = heis(L4)
check('third quiz, the open diagram has 2^4 = 16 entries, the closed one is the number <psi|psi>, H|psi> has 16 entries',
      c.size == 16 and E.shape == (1, 1) and abs(E[0, 0] - c @ c) < 1e-10 and (H4 @ c).size == 16, (c.size, E.shape))

# the problem
Mp, Dp = 10, 5
check('problem, M D = 50, and 200, 5000, 200 numbers per bulk tensor, D^2 = 25, then 2 x 250^2 = 1.25e5',
      Mp * Dp == 50 and 2 * Mp ** 2 == 200 and 2 * (Mp * Dp) ** 2 == 5000 and Dp ** 2 == 25
      and 2 * (Mp * Dp * Dp) ** 2 == 125000, (Mp * Dp, 2 * Mp ** 2, 2 * (Mp * Dp) ** 2, 2 * (Mp * Dp * Dp) ** 2))
print('all checks of page 09 passed')
