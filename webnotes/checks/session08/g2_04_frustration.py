"""Session 8, the numbers that page 04 (Section 8.4) quotes, checked in the order of the page.

One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a lab box is an
assert, here or in the figure script that draws it. The figure ising_degeneracy counts the ground states of the
periodic clusters and asserts them, this script counts the two clusters of 24 sites again with its own code, and
_g2_cluster.py asserts the energies of the picture quiz, which this script asserts again. The Ising spins are S^z = +-1/2 with H = J sum_<ij> S^z_i S^z_j and J = 1, as on the conventions sheet.
It finds the repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session08/g2_04_frustration.py"""
import os, sys, itertools
sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
assert os.path.exists(os.path.join(REPO, 'webnotes', 'pages', 'session08'))

import numpy as np
from scipy.integrate import quad
from math import comb


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def levels(N, bonds):
    """The energies of the 2^N Ising configurations and how many configurations have each."""
    out = {}
    for c in itertools.product((0.5, -0.5), repeat=N):
        e = round(sum(c[i] * c[j] for i, j in bonds), 9)
        out[e] = out.get(e, 0) + 1
    return dict(sorted(out.items()))


def all_pairs(N):
    return list(itertools.combinations(range(N), 2))


def lowest_count(N, bonds):
    """The number of the 2^N configurations with the lowest energy sum_<ij> s_i s_j, s = +-1, in chunks of 2^22."""
    emin, cnt = None, 0
    chunk = 1 << min(N, 22)
    for start in range(0, 1 << N, chunk):
        c = np.arange(start, start + chunk, dtype=np.int64)
        E = np.zeros(chunk, dtype=np.int8)
        for i, j in bonds:
            E += (1 - 2 * (((c >> i) ^ (c >> j)) & 1)).astype(np.int8)
        m = int(E.min())
        if emin is None or m < emin:
            emin, cnt = m, int((E == m).sum())
        elif m == emin:
            cnt += int((E == m).sum())
    return cnt


def torus(L1, L2, steps):
    idx = lambda x, y: (x % L1) + L1 * (y % L2)
    return L1 * L2, [(idx(x, y), idx(x + dx, y + dy)) for x in range(L1) for y in range(L2) for dx, dy in steps]


# the recall box: the Heisenberg dimer J S_0.S_1 has the singlet at -3/4 once and the triplet at +1/4 three times
SXYZ = [np.array([[0, 1], [1, 0]]) / 2, np.array([[0, -1j], [1j, 0]]) / 2, np.diag([0.5, -0.5])]
w = np.round(np.linalg.eigvalsh(sum(np.kron(s, s) for s in SXYZ).real), 9)
dimer_h = {float(v): int((w == v).sum()) for v in np.unique(w)}
check('recall, the Heisenberg dimer has -3/4 once and +1/4 three times', dimer_h == {-0.75: 1, 0.25: 3}, dimer_h)

# the fold: when every pair is a bond, sum S_i S_j = (M^2 - N/4)/2 with M the total S^z
for N, text in ((2, 'two spins'), (3, 'triangle'), (4, 'tetrahedron')):
    worst = max(abs(sum(c[i] * c[j] for i, j in all_pairs(N)) - 0.5 * (sum(c) ** 2 - N / 4))
                for c in itertools.product((0.5, -0.5), repeat=N))
    check('fold and problem, sum over the pairs = (M^2 - N/4)/2 for the ' + text, worst < 1e-12, worst)
check('fold, the dimer has -1/4 twice at M = 0 and +1/4 twice', levels(2, [(0, 1)]) == {-0.25: 2, 0.25: 2},
      levels(2, [(0, 1)]))
tri = levels(3, all_pairs(3))
check('fold, key box and first quiz, the triangle has -1/4 six times and +3/4 twice', tri == {-0.25: 6, 0.75: 2}, tri)
check('fold, M = +-1/2 has 3 + 3 configurations and M = +-3/2 one each', comb(3, 1) + comb(3, 2) == 6, comb(3, 1))
check('opener and quiz, a triangle with every bond satisfied would have -3/4, the lowest is -1/4',
      min(tri) == -0.25 and 3 * (-0.25) == -0.75, min(tri))

# the caption of Figure 8.2: free classical spins on the triangle go into the 120 degree state, which is unique up to a
# global rotation, since for unit vectors sum_<ij> S_i.S_j = (|S_0 + S_1 + S_2|^2 - 3)/2 is lowest, -3/2, at zero sum
rng = np.random.default_rng(8)
worst_e, worst_c, ranks = 0.0, 0.0, set()
for trial in range(20):
    v = rng.normal(size=(3, 3))
    v /= np.linalg.norm(v, axis=1)[:, None]
    for sweep in range(2000):
        for i in range(3):
            h = v[(i + 1) % 3] + v[(i + 2) % 3]
            if np.linalg.norm(h) > 1e-12:
                v[i] = -h / np.linalg.norm(h)
    e = sum(v[i] @ v[j] for i, j in all_pairs(3))
    worst_e = max(worst_e, abs(e + 1.5))
    worst_c = max(worst_c, max(abs(v[i] @ v[j] + 0.5) for i, j in all_pairs(3)))
    ranks.add(int(np.linalg.matrix_rank(v, tol=1e-6)))
check('caption of Figure 8.2, three classical unit spins relax to -3/2, every angle 120 degrees, coplanar, 20 starts',
      worst_e < 1e-9 and worst_c < 1e-6 and ranks == {2} and abs(np.cos(2 * np.pi / 3) + 0.5) < 1e-12,
      (worst_e, worst_c, ranks))

# the key box: the entropies per site of the infinite lattices, 0.32 and 0.50
s_tri = 2 / np.pi * quad(lambda w: np.log(2 * np.cos(w)), 0, np.pi / 3)[0]
check('key box, the triangular lattice has s = 0.32', abs(s_tri - 0.32) < 0.005, round(s_tri, 4))
s_kag = np.log(2) + 2 / 3 * np.log(3 / 4)                    # the Pauling count, the conventions sheet says about 0.50
check('key box, the kagome lattice has s = 0.50 (Pauling count)', abs(s_kag - 0.50) < 0.005, round(s_kag, 4))
def kagome(n1, n2):
    idx = lambda x, y, s: 3 * ((x % n1) + n1 * (y % n2)) + s
    b = []
    for x in range(n1):
        for y in range(n2):
            A, B, C = idx(x, y, 0), idx(x, y, 1), idx(x, y, 2)
            b += [(A, B), (B, C), (C, A), (B, idx(x + 1, y, 0)), (C, idx(x, y + 1, 0)), (B, idx(x + 1, y - 1, 2))]
    return 3 * n1 * n2, b


# the key box: the clusters of 24 sites of the conventions sheet, recounted here among all 2^24 configurations
n_kag = lowest_count(*kagome(2, 4))
n_tri = lowest_count(*torus(6, 4, ((1, 0), (0, 1), (1, -1))))
check('key box, the kagome cluster of 24 sites has 181122 ground states, ln W / N = 0.50',
      n_kag == 181122 and abs(np.log(n_kag) / 24 - 0.50) < 0.01, (n_kag, round(np.log(n_kag) / 24, 4)))
check('key box, the triangular cluster 6 x 4 has 1698 ground states, ln W / N = 0.31',
      n_tri == 1698 and abs(np.log(n_tri) / 24 - 0.31) < 0.005, (n_tri, round(np.log(n_tri) / 24, 4)))

# the lab box: the ratio of the Curie-Weiss temperature and of the lowest temperature, ours
check('lab box, 300 K over 50 mK is 6000', abs(300 / 0.050 - 6000) < 1e-9, 300 / 0.050)
# the lab box, "in mean field": two sublattices with m_A = (C/T)(h - zJ m_B) and the same for B, C = S(S+1)/3, J = 1.
# The uniform response 1/chi = (T + zJC)/C vanishes at theta_CW = -zJC, and the staggered one diverges at T_N = zJC.
from scipy.optimize import brentq
worst = 0.0
for z in (2, 3, 4, 6):                       # the chain, the honeycomb, the square and the simple cubic lattice
    C = 0.5 * 1.5 / 3
    M = lambda T: np.array([[1, z * C / T], [z * C / T, 1]])
    inv_chi = lambda T: 1 / np.linalg.solve(M(T), C / T * np.ones(2))[0]
    slope = (inv_chi(20.0) - inv_chi(10.0)) / 10.0
    theta = 10.0 - inv_chi(10.0) / slope
    TN = brentq(lambda T: np.linalg.det(M(T)), 1e-3, 1e3)
    worst = max(worst, abs(TN - abs(theta)), abs(theta + z * C))
check('lab box, in mean field a bipartite antiferromagnet orders at T_N = |theta_CW|, for z = 2, 3, 4, 6', worst < 1e-9,
      worst)

# the second quiz: the kagome lattice has four neighbors, like the square lattice
N, bonds = kagome(3, 3)
deg = np.bincount(np.array(bonds).ravel(), minlength=N)
check('second quiz, every site of the kagome lattice has 4 neighbors', set(deg) == {4}, set(deg))
N, bonds = torus(4, 4, ((1, 0), (0, 1)))
deg = np.bincount(np.array(bonds).ravel(), minlength=N)
check('second quiz, every site of the square lattice has 4 neighbors', set(deg) == {4}, set(deg))

# the third quiz and the problem: the square plaquette and the tetrahedron
square = levels(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
tetra = levels(4, all_pairs(4))
check('third quiz and problem, the square has its lowest energy -1, every bond satisfied, 2 times',
      min(square) == -1.0 and square[-1.0] == 2 and 4 * (-0.25) == -1.0, square)
check('third quiz and problem, the tetrahedron has -1/2 six times, against -3/2 with every bond satisfied',
      min(tetra) == -0.5 and tetra[-0.5] == 6 and 6 * (-0.25) == -1.5, tetra)
check('problem, M = 0 on four sites is C(4,2) = 6 configurations', comb(4, 2) == 6, comb(4, 2))
pairs4 = set(all_pairs(4))
triangles = [t for t in itertools.combinations(range(4), 3) if all(p in pairs4 for p in itertools.combinations(t, 2))]
check('third quiz, the tetrahedron is made of four triangles', len(triangles) == 4, len(triangles))
worst = 0
for c in itertools.product((0.5, -0.5), repeat=4):
    if sum(c) == 0:
        worst = max(worst, abs(sum(c[i] == c[j] for i, j in all_pairs(4)) - 2))
check('problem, each ground state of the tetrahedron has two parallel pairs among its six bonds', worst == 0, worst)

# corrected and decided on 2026-11-22, old text of the page
SXq, SYq, SZq = np.array([[0, 1], [1, 0]]) / 2, np.array([[0, -1j], [1j, 0]]) / 2, np.diag([0.5, -0.5])


def opq(o, i, n):
    out = np.eye(1)
    for j in range(n):
        out = np.kron(out, o if j == i else np.eye(2))
    return out


def heis(n, bonds):
    return sum(opq(s, i, n) @ opq(s, j, n) for i, j in bonds for s in (SXq, SYq, SZq)).real


def theta(n):
    """Time reversal theta K with theta = i sigma^y on each spin."""
    out = np.eye(1)
    for _ in range(n):
        out = np.kron(out, np.array([[0, 1], [-1, 0]]))
    return out


# caption of Figure 8.2: the Heisenberg triangle has its ground level -3/4 four times, two doublets with S = 1/2, and
# for three spins one half (theta K)^2 = -1, so no state maps to itself (Kramers), while two triangles that share an edge,
# four sites with five bonds, have one singlet at -7/4 that time reversal maps to itself and that has <S_i> = 0
et = np.round(np.linalg.eigvalsh(heis(3, [(0, 1), (1, 2), (2, 0)])), 9)
T3 = theta(3)
kramers = np.allclose(T3 @ T3.conj(), -np.eye(8))
Hr = heis(4, [(0, 1), (1, 2), (2, 0), (1, 3), (2, 3)])
er, vr = np.linalg.eigh(Hr)
g4 = vr[:, 0]
S2r = sum(sum(opq(s, i, 4) for i in range(4)) @ sum(opq(s, i, 4) for i in range(4)) for s in (SXq, SYq, SZq)).real
mags = [abs(np.vdot(g4, opq(s, i, 4) @ g4)) for s in (SXq, SYq, SZq) for i in range(4)]
check('corrected, caption of Figure 8.2: the triangle has -3/4 four times and (theta K)^2 = -1, and two triangles on an edge '
      'have one singlet at -7/4 with <S_i> = 0 that time reversal maps to itself',
      list(et).count(-0.75) == 4 and et[4] > -0.75 + 1 and kramers and abs(er[0] + 1.75) < 1e-12 and er[1] - er[0] > 0.5
      and abs(np.vdot(g4, S2r @ g4)) < 1e-12 and max(mags) < 1e-12 and abs(abs(np.vdot(g4, theta(4) @ g4.conj())) - 1) < 1e-12,
      (list(et).count(-0.75), round(er[0], 6), round(er[1] - er[0], 6)))
# second quiz: on the square plaquette the classical Neel configuration satisfies every bond, while for the quantum
# Heisenberg model of the question the Neel state is not an eigenstate, so the option says "classical"
Hsq = heis(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
neel = np.zeros(16); neel[int('0101', 2)] = 1.0
check('decided, second quiz: the Neel state of the plaquette has <H> = -1, every bond at -1/4, and it is not an eigenstate '
      'of the Heisenberg model, whose ground level is -2',
      abs(neel @ Hsq @ neel + 1) < 1e-12 and np.linalg.norm(Hsq @ neel - (neel @ Hsq @ neel) * neel) > 0.5
      and abs(np.linalg.eigvalsh(Hsq)[0] + 2) < 1e-12, round(np.linalg.norm(Hsq @ neel + neel), 4))
