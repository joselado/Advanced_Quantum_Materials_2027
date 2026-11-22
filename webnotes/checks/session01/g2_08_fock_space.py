"""Session 1, the numbers that page 08 (Sections 1.8, 1.9 and 1.10) quotes.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The island of the figure island_states and of the three pictures of the quiz on
the lowest level is checked by check() of figures/session01/_g2_island.py, which this script runs again on the pyqula
script scripts/session01/g2_honeycomb_island.py. The levels of the open chain are also asserted in levels_vs_size.py.
This script holds the numbers in the order of the page. It finds the repository from its own path and writes no file
in it, since pyqula runs in a temporary folder.

Run it from anywhere:  python3 webnotes/checks/session01/g2_08_fock_space.py"""
import os
import sys
import tempfile
from itertools import product
from math import comb

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.dirname(os.path.dirname(HERE))


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# Section 1.9 and Figure 1.1: three spinless sites give 1+3+3+1 = 8 = 2^3 states, and L = 20 about a million
states = list(product((0, 1), repeat=3))
byN = [sum(1 for s in states if sum(s) == N) for N in range(4)]
check('1.9: three sites, 1, 3, 3, 1 states with N = 0..3, 8 in total', byN == [1, 3, 3, 1] and len(states) == 8 == 2 ** 3,
      byN)
check('Figure 1.1: 2^20 = 1 048 576, about a million', 2 ** 20 == 1048576 and 0.9e6 < 2 ** 20 < 1.1e6, 2 ** 20)

# the opener: at fixed N an interacting wave function of N electrons on L orbitals lives in the antisymmetric part of
# the N-fold product space, whose dimension is binom(L, N), the block of the Fock space with N electrons
from itertools import permutations  # noqa: E402


def antisym_dim(L, N):
    """The rank of the antisymmetrizer on the N-fold product of an L-dimensional space."""
    dim = L ** N
    A = np.zeros((dim, dim))
    idx = list(product(range(L), repeat=N))
    pos = {s: k for k, s in enumerate(idx)}
    for perm in permutations(range(N)):
        sign = np.linalg.det(np.eye(N)[list(perm)])
        for k, s in enumerate(idx):
            A[pos[tuple(s[p] for p in perm)], k] += sign
    return int(np.linalg.matrix_rank(A))


dims = {(L, N): antisym_dim(L, N) for (L, N) in ((4, 2), (5, 2), (4, 3), (5, 3), (6, 3))}
check('opener: N electrons on L orbitals in first quantization span binom(L, N) states, the block of fixed N',
      all(v == comb(L, N) for (L, N), v in dims.items()), dims)

# the key box: L x L, or 2L x 2L with spin, against 2^L x 2^L and 4^L x 4^L, a new site doubles it, or multiplies it
# by four with spin
ok_key = all(2 ** (L + 1) == 2 * 2 ** L and 4 ** (L + 1) == 4 * 4 ** L and 4 ** L == 2 ** (2 * L) for L in range(1, 31))
check('key box: 2^(L+1) = 2 * 2^L and 4^(L+1) = 4 * 4^L = 2^(2(L+1)) for L = 1..30', ok_key, ok_key)
ok_fock = all(len(list(product((0, 1), repeat=L))) == 2 ** L and len(list(product(range(4), repeat=L))) == 4 ** L
              for L in range(1, 7))
check('key box: the lists of occupations give 2^L spinless and 4^L spinful states for L = 1..6', ok_fock, ok_fock)
# the single-particle matrix with spin is 2L x 2L, by the spin as one more orbital index, and with pyqula below

# the fold: sum_N binom(L, N) = 2^L, a number-conserving Hamiltonian is block diagonal, the largest block of L = 20
check('fold: sum_N binom(3, N) = 1+3+3+1 = 8', [comb(3, N) for N in range(4)] == [1, 3, 3, 1], 8)
check('fold: sum_N binom(L, N) = 2^L = (1+1)^L for L = 1..30', all(sum(comb(L, N) for N in range(L + 1)) == 2 ** L
                                                                  for L in range(1, 31)), 2 ** 30)
check('fold: binom(20, 10) = 184 756 out of 2^20 = 1 048 576', comb(20, 10) == 184756 and 2 ** 20 == 1048576,
      comb(20, 10) / 2 ** 20)
check('fold: the largest block binom(L, L/2) still grows exponentially, by more than 1.8 per site from L=10 to 20',
      all(comb(L + 2, L // 2 + 1) / comb(L, L // 2) > 1.8 ** 2 for L in range(10, 20, 2)), comb(22, 11) / comb(20, 10))
# a random Hamiltonian with hoppings and a quartic term on three spinless sites commutes with N
a, Z, I = np.array([[0., 1.], [0., 0.]]), np.diag([1., -1.]), np.eye(2)
c = [np.kron(np.kron(*([Z] * j + [a] + [I] * (2 - j))[:2]), ([Z] * j + [a] + [I] * (2 - j))[2]) for j in range(3)]
rng = np.random.default_rng(1)
tij = rng.normal(size=(3, 3)); tij = tij + tij.T
H = sum(tij[i, j] * c[i].T @ c[j] for i in range(3) for j in range(3))
for i, j, k, l in product(range(3), repeat=4):
    H = H + rng.normal() * c[i].T @ c[j].T @ c[k] @ c[l]
H = H + H.T
N = sum(x.T @ x for x in c)
check('fold: a Hamiltonian with t_ij and a quartic term commutes with N, so it has blocks of fixed N',
      np.allclose(H @ N, N @ H), np.abs(H @ N - N @ H).max())
check('fold: three spinful sites, 4^3 = 2^6 = 64 states and a 6 x 6 single-particle matrix',
      4 ** 3 == 2 ** 6 == 64 == len(list(product(range(4), repeat=3))), 64)

# the quiz on three spinful sites
check('quiz: 4+4+4 = 12 is not the count, two sites already give 4 x 4 = 16 pairs',
      4 + 4 + 4 == 12 and len(list(product(range(4), repeat=2))) == 16, 16)
check('quiz: 4^3 = 64 and sum_N binom(6, N) = 2^6 = 64', 4 ** 3 == 64 == sum(comb(6, N) for N in range(7)) == 2 ** 6, 64)

# the problem: one state of 20 spinful sites with 8 bytes per coefficient
full = 4 ** 20
check('problem: 4^20 = 1.1e12 states', np.isclose(full, 1.1e12, rtol=0.01), f'{full:.4e}')
check('problem: 8 bytes each is 8.8e12 bytes = 8.8 TB', round(8 * full / 1e12, 1) == 8.8, 8 * full / 1e12)
up = comb(20, 10)
check('problem: binom(20, 10) = 184 756 ways for 10 up electrons on 20 sites', up == 184756, up)
check('problem: binom(20, 10)^2 = 3.4e10 states', round(up ** 2 / 1e10, 1) == 3.4, f'{up ** 2:.4e}')
check('problem: 8 bytes each is 273 GB', round(8 * up ** 2 / 1e9) == 273, 8 * up ** 2 / 1e9)
# N = 20 and S_z = 0 are 10 up and 10 down electrons, and the count is the number of such Fock states
check('problem: the N = 20, S_z = 0 sector of 20 sites is binom(20,10)^2, as the sum over the sectors gives 4^20',
      sum(comb(20, nu) * comb(20, nd) for nu in range(21) for nd in range(21)) == 4 ** 20, up ** 2)
ratio = full / up ** 2
check('problem: the two conserved quantities gain a factor of about 32, less than 4^3 = 64', 31 < ratio < 33 and ratio < 64,
      ratio)
check('problem: 2^20 = 1 048 576 spinless coefficients take 8.4 MB', 2 ** 20 == 1048576 and round(8 * 2 ** 20 / 1e6, 1) == 8.4,
      8 * 2 ** 20 / 1e6)
dense = (2 ** 20) ** 2
check('problem: the full 2^20 x 2^20 matrix has 2^40 entries, 8.8 TB, as much as one state of 20 spinful sites',
      dense == 2 ** 40 == 4 ** 20 and round(8 * dense / 1e12, 1) == 8.8, 8 * dense / 1e12)
check('problem: one state of 20 spinless sites is 2^20 times smaller than the full matrix', dense // 2 ** 20 == 2 ** 20,
      2 ** 20)

# the lab box: the band of the honeycomb lattice with the hopping -t has its bottom at -3t
k = np.linspace(-np.pi, np.pi, 301)
k1, k2 = np.meshgrid(k, k)
f = np.abs(1 + np.exp(1j * k1) + np.exp(1j * k2))
check('lab: the bottom of the band of the honeycomb lattice with the hopping -t is -3t', np.isclose(-f.max(), -3.0), -f.max())

# the island: the pyqula script, checked by _g2_island.check, which asserts the 96 sites, the zigzag edges, the levels
# -2.91, -2.76 and -2.34, the absence of a node in the lowest state, the odd states of the second level, the density of
# the sixth level on the central hexagon below 1% of its maximum, and the mean distances 2.87, 3.74 and 4.43
sys.dont_write_bytecode = True                  # no __pycache__ next to the figure helpers
sys.path.insert(0, os.path.join(WEB, 'figures'))
sys.path.insert(0, os.path.join(WEB, 'figures', 'session01'))
import style  # noqa: E402
import _g2_island  # noqa: E402

d = style.run_script('session01/g2_honeycomb_island.py')
mean_r = _g2_island.check(d)
lev = d['levels']
check('island: 96 sites', len(d['x']) == 96, len(d['x']))
check('island: the lowest, the second and the sixth level are -2.91t, -2.76t and -2.34t',
      [round(float(lev[n]), 2) for n in (0, 1, 5)] == [-2.91, -2.76, -2.34], np.round(lev[[0, 1, 5]], 4))
check('island: the lowest level lies close to the bottom -3t of the band, above it', -3.0 < lev[0] < -2.9, lev[0])
check('island: mean distances 2.87, 3.74 and 4.43 bond lengths', np.allclose(mean_r, [2.87, 3.74, 4.43], atol=0.005),
      np.round(mean_r, 3))
dens = d['density']
r = np.hypot(d['x'], d['y'])
check('island: the key disc 0.03 lies between the densities that are drawn', dens[0].max() > 0.03 and dens[5].max() > 0.03,
      (round(dens[0].max(), 4), round(dens[5].max(), 4)))
check('quiz island: the sixth level has less than a hundredth of its maximum on the central hexagon',
      dens[5][r < 1.01].mean() < 0.01 * dens[5].max(), dens[5][r < 1.01].mean() / dens[5].max())

# the island by a second route: my own construction, the hexagons whose centers are at most three steps from the
# central one on the triangular lattice of the centers, with the hopping -t of the caption, diagonalized here
a1, a2 = np.array([1.5, np.sqrt(3) / 2]), np.array([0.0, np.sqrt(3)])
pts = set()
for i in range(-4, 5):
    for j in range(-4, 5):
        if max(abs(i), abs(j), abs(i + j)) <= 3:
            cen = i * a1 + j * a2
            for m in range(6):
                p = cen + np.array([np.cos(m * np.pi / 3), np.sin(m * np.pi / 3)])
                pts.add((round(p[0], 6), round(p[1], 6)))
X = np.array(sorted(pts))
xo, yo = X[:, 0], X[:, 1]
Do = np.hypot(xo[:, None] - xo[None], yo[:, None] - yo[None])
Ao = (np.abs(Do - 1) < 1e-4).astype(float)
Eo, Vo = np.linalg.eigh(-Ao)
ro = np.hypot(xo, yo)
key5 = lambda a, b: np.array(sorted(zip(np.round(a, 5), np.round(b, 5))))
check('island, second route: the same 96 positions as the pyqula script', len(xo) == 96
      and np.abs(key5(xo, yo) - key5(d['x'], d['y'])).max() < 1e-4, len(xo))
check('island, second route: the same 96 levels as the pyqula script', np.allclose(Eo, d['energies'], atol=1e-10),
      np.abs(Eo - d['energies']).max())
levo, start, groups = [], 0, []
while start < 96:
    stop = start + int(np.sum(np.abs(Eo - Eo[start]) < 1e-6))
    levo.append(Eo[start]); groups.append(list(range(start, stop))); start = stop
dego = [len(g_) for g_ in groups]
check('island, second route: the first ten levels have the degeneracies 1, 2, 2, 1, 1, 1, 2, 2, 2, 1',
      dego[:10] == [1, 2, 2, 1, 1, 1, 2, 2, 2, 1], dego[:10])
check('caption: a degenerate level counted once, the sixth level is the eighth state, the second level the states 2 and 3',
      groups[5] == [7] and groups[1] == [1, 2], (groups[1], groups[5]))
check('island, second route: the levels -2.91t, -2.76t, -2.52t and -2.34t of the first, second, fourth and sixth level',
      [round(float(levo[n]), 2) for n in (0, 1, 3, 5)] == [-2.91, -2.76, -2.52, -2.34], np.round([levo[n] for n in (0, 1, 3, 5)], 4))
denso = [np.mean(Vo[:, g_] ** 2, axis=1) for g_ in groups[:10]]
mro = [float((dn * ro).sum()) for dn in denso]
check('quiz closing line: the mean distances of the levels 2 to 10 are all larger than 2.87 of the lowest level',
      np.isclose(mro[0], 2.87, atol=0.005) and min(mro[1:10]) > 2.87 + 0.4, np.round(mro, 3))
check('island, second route: mean distances 2.87, 3.74 and 4.43 of the first, second and sixth level',
      np.allclose([mro[0], mro[1], mro[5]], [2.87, 3.74, 4.43], atol=0.005), np.round([mro[0], mro[1], mro[5]], 3))
v0 = Vo[:, 0] * np.sign(Vo[0, 0])
check('quiz closing line: the lowest state has one sign on all sites, and every other state changes sign',
      np.all(v0 > 1e-6) and all((Vo[:, k] > 1e-9).any() and (Vo[:, k] < -1e-9).any() for k in range(1, 96)), v0.min())
# the inversion r -> -r and the rotation by 60 degrees, as permutations of the sites
Po = np.array([[1.0 if np.hypot(xo[i] + xo[j], yo[i] + yo[j]) < 1e-4 else 0.0 for j in range(96)] for i in range(96)])
xr, yr = np.cos(np.pi / 3) * xo - np.sin(np.pi / 3) * yo, np.sin(np.pi / 3) * xo + np.cos(np.pi / 3) * yo
Ro = np.array([[1.0 if np.hypot(xr[j] - xo[i], yr[j] - yo[i]) < 1e-4 else 0.0 for j in range(96)] for i in range(96)])
check('island, second route: the inversion is the rotation by 180 degrees, and both commute with H',
      np.allclose(np.linalg.matrix_power(Ro, 3), Po) and np.allclose(Po @ Ao, Ao @ Po) and np.allclose(Ro @ Ao, Ao @ Ro), 0)
V2 = Vo[:, groups[1]]
chi6, chi2 = np.trace(V2.T @ Ro @ V2), np.trace(V2.T @ Po @ V2)
check('quiz: the second level has the character +1 under the rotation by 60 degrees, so -2 under the inversion, odd',
      np.isclose(chi6, 1.0) and np.isclose(chi6 ** 3 - 3 * chi6, chi2) and np.isclose(chi2, -2.0), (round(chi6, 6), round(chi2, 6)))
v6 = Vo[:, groups[5][0]]
check('island, second route: the sixth level, the eighth state, is odd under r -> -r', np.allclose(Po @ v6, -v6), 0)
v4 = Vo[:, groups[3][0]]
v4 = v4 * np.sign(v4[np.argmin(ro)])
check('quiz closing line: the fourth level is single and changes sign on a ring, + for r < 3 and - for r > 3.5',
      dego[3] == 1 and np.all(v4[ro < 3] > 1e-6) and np.all(v4[ro > 3.5] < -1e-6) and not ((ro > 3) & (ro < 3.5)).any(),
      (round(v4[ro < 3].min(), 3), round(v4[ro > 3.5].max(), 3)))
d4 = denso[3]
check('quiz closing line: the largest density of the fourth level is on the central hexagon, 1.7 times that of the lowest',
      np.isclose(d4[ro < 1.01].min(), d4.max()) and 1.6 < d4.max() / denso[0].max() < 1.8, round(d4.max() / denso[0].max(), 3))

# the quiz on the spacing: the open chain, -2t cos(n pi/(N+1)), 0.57t for N = 10 and 0.062t for N = 100, close to
# 2 pi t/(N+1), in a window of width 4t, with pyqula as in the recipe "The levels of an open chain"
os.chdir(tempfile.mkdtemp())
from pyqula import geometry  # noqa: E402

# the key box: the single-particle matrix of L sites is L x L without spin and 2L x 2L with spin, in pyqula
shapes = {}
for Ls in (3, 5):
    gs = geometry.chain().get_supercell(Ls)
    gs.dimensionality = 0
    shapes[Ls] = (gs.get_hamiltonian(has_spin=False).intra.shape, gs.get_hamiltonian(has_spin=True).intra.shape)
check('key box: pyqula gives an L x L matrix without spin and 2L x 2L with spin, 6 x 6 for three sites',
      all(s == ((L_, L_), (2 * L_, 2 * L_)) for L_, s in shapes.items()), shapes)

for Nc, val in ((10, 0.57), (100, 0.062)):
    g = geometry.chain().get_supercell(Nc)
    g.dimensionality = 0
    e = np.linalg.eigvalsh(g.get_hamiltonian(has_spin=False, tij=[-1.]).intra)
    ref = np.sort(-2 * np.cos(np.arange(1, Nc + 1) * np.pi / (Nc + 1)))
    gap = e[Nc // 2] - e[Nc // 2 - 1]
    check(f'quiz spacing: N={Nc}, pyqula gives -2t cos(n pi/(N+1)), center spacing {val}t',
          np.allclose(e, ref) and abs(gap - val) < (0.005 if Nc == 10 else 0.0005), round(gap, 4))
    check(f'quiz spacing: N={Nc}, the levels fill the window from -2t to 2t, of width 4t',
          -2 < e.min() < -1.9 and 1.9 < e.max() < 2, (round(e.min(), 3), round(e.max(), 3)))
check('quiz spacing: 2 pi t/(N+1) = 0.0622t for N = 100, close to the spacing 4t sin(pi/(2(N+1)))',
      abs(2 * np.pi / 101 - 0.0622) < 5e-5 and abs(4 * np.sin(np.pi / 202) - 2 * np.pi / 101) < 1e-5, 2 * np.pi / 101)
# the tryit: the distance of the two levels closest to zero falls as 1/L
Ls = np.array([20, 40, 80, 160])
gaps = [np.diff(np.sort(-2 * np.cos(np.arange(1, L + 1) * np.pi / (L + 1))))[L // 2 - 1] for L in Ls]
prod = np.array(gaps) * (Ls + 1)
check('tryit: the spacing at the center falls as 1/L, (L+1) times the spacing is 2 pi to 0.2%',
      np.allclose(prod, 2 * np.pi, rtol=2e-3), np.round(prod, 4))
