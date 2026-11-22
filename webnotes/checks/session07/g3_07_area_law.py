"""Session 7, the numbers that page 07 (Section 7.7) quotes, checked in the order of the page.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or
in the figure script that draws it. The cut bonds are counted bond by bond on a lattice much larger than the region.
The fold and the problem use horizontal dimers on the sites (2m, y) and (2m+1, y), and the smallest square is also
checked on the real product of singlets of 8 sites. The figure random_vs_gapped is computed again, with the dimerized
chain in the sector S^z_tot = 0 and site i as bit i of the index, as in its own script, which asserts less. It finds the
repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session07/g3_07_area_law.py"""
import os, sys
sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
assert os.path.exists(os.path.join(REPO, 'webnotes', 'pages', 'session07'))

import itertools
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


def cut_bonds(region, dim):
    """Bonds of the simple cubic lattice in dim dimensions with one site in the region and one outside."""
    region = set(region)
    n = 0
    for site in region:
        for d in range(dim):
            for s in (1, -1):
                nb = list(site); nb[d] += s
                n += tuple(nb) not in region
    return n


def box(*sides, origin=None):
    origin = origin or (0,) * len(sides)
    return [tuple(o + x for o, x in zip(origin, p)) for p in itertools.product(*[range(a) for a in sides])]


def cut_singlets(region):
    """Horizontal dimers on (2m, y) and (2m+1, y): a dimer is cut when one of its two sites is in the region."""
    region = set(region)
    return sum(((x - x % 2, y) in region) != ((x - x % 2 + 1, y) in region) for x, y in
               {(x - x % 2, y) for x, y in region})


# the text and the caption of Figure 7.2: a square of side 2 cuts 8 bonds and one of side 4 cuts 16
check('text and Figure 7.2, the squares of side 2 and 4 cut 8 and 16 bonds', [cut_bonds(box(l, l), 2) for l in (2, 4)] == [8, 16],
      [cut_bonds(box(l, l), 2) for l in (2, 4)])

singlet = np.array([0, 1, -1, 0]) / np.sqrt(2)


def block_entropy(psi, sites):
    rest = [i for i in range(psi.ndim) if i not in sites]
    m = np.transpose(psi, list(sites) + rest).reshape(2 ** len(sites), -1)
    return entropy_of(np.linalg.svd(m, compute_uv=False) ** 2)


# the caption of Figure 7.2 (a): a block whose ends cut one dimer each, with two and with five interior dimers, has 2 log 2
chain = np.array([1.0])
for n in range(7):
    chain = np.kron(chain, singlet)
chain = chain.reshape((2,) * 14)
S25 = [block_entropy(chain, list(range(1, 2 * k + 3))) for k in (2, 5)]       # the sites 1 to 6 and 1 to 12
check('Figure 7.2 (a), two and five interior dimers, two cut singlets, S_A = 2 log 2 in both', np.allclose(S25, 2 * ln2), np.array(S25) / ln2)

# the caption of Figure 7.2 (b) and the text before it, corrected on 2026-11-22 (open point 5 of the plan): the tetramers
# are Heisenberg rings of four sites on the 2 x 2 blocks, and the squares are offset by one site, as on the conventions
# sheet. 8 to 16 cut bonds give 4 log 2 to 8.83 log 2, a factor 2.21 and not 2, so S_A grows "roughly in proportion", and
# each cut cluster gives one contribution, at most log 2 per cut bond, in both
sv = [np.array([[0, 1], [1, 0]]) / 2, np.array([[0, -1j], [1j, 0]]) / 2, np.diag([0.5, -0.5])]
op4 = lambda o, i: np.kron(np.kron(np.eye(2 ** i), o), np.eye(2 ** (3 - i)))
ring = sum(op4(s, i) @ op4(s, (i + 1) % 4) for s in sv for i in range(4)).real
er, vr = np.linalg.eigh(ring)
plaq = vr[:, 0].reshape(2, 2, 2, 2)                                              # ring order (0,0), (1,0), (1,1), (0,1)
check('Figure 7.2 (b), the tetramer ground state is a singlet at -2J', abs(er[0] + 2) < 1e-12 and er[1] - er[0] > 0.5, er[:2])
ring_pos = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 3}
check('Figure 7.2 (b), one site of a tetramer has log 2 and two sites of a side 1.2075 log 2',
      abs(block_entropy(plaq, [0]) - ln2) < 1e-12 and abs(block_entropy(plaq, [0, 1]) / ln2 - 1.2075) < 1e-4,
      (block_entropy(plaq, [0]) / ln2, block_entropy(plaq, [0, 1]) / ln2))


def tetramer_entropy(region):
    region, S = set(region), 0.0
    for a, b in {(x // 2, y // 2) for x, y in region}:
        keep = sorted(ring_pos[(x - 2 * a, y - 2 * b)] for x, y in region if (x // 2, y // 2) == (a, b))
        S += block_entropy(plaq, keep) if len(keep) < 4 else 0.0
    return S


small, large = box(2, 2, origin=(1, 1)), box(4, 4, origin=(1, 1))
Ss, Sl = tetramer_entropy(small), tetramer_entropy(large)
check('Figure 7.2 (b), the small square: 8 cut bonds and 4 log 2', cut_bonds(small, 2) == 8 and abs(Ss / ln2 - 4) < 1e-10, Ss / ln2)
check('Figure 7.2 (b), the large square: 16 cut bonds and 8.83 log 2, a factor 2.21 for twice the cut bonds, roughly in proportion',
      cut_bonds(large, 2) == 16 and round(Sl / ln2, 2) == 8.83 and round(Sl / Ss, 2) == 2.21 and abs(Sl / Ss - 2) < 0.25, (Sl / ln2, Sl / Ss))
check('Figure 7.2 (b) and the text, at most log 2 per cut bond', Ss <= 8 * ln2 and Sl <= 16 * ln2, (Ss / 8 / ln2, Sl / 16 / ln2))
# the text: one contribution from each cut cluster, at most log 2 per cut bond, for any state of a plaquette: a cut of one
# site crosses two bonds of the ring and holds at most log 2, a cut along a side crosses two bonds and holds at most 2 log 2
check('the text, a cut cluster holds at most log 2 per cut bond for the cuts of the figure, one site and one side',
      block_entropy(plaq, [0]) <= 2 * ln2 and block_entropy(plaq, [0, 1]) <= 2 * ln2 + 1e-12, 'ok')
check('Figure 7.2 (b), a square aligned with the tetramers has S = 0', tetramer_entropy(box(4, 4)) == 0.0, 0)

# the key box and the problem: in a product of singlets the area law is a bound, S_A <= log 2 times the cut bonds,
# for every square of side 1 to 8 at every shift
ok = all(cut_singlets(box(l, l, origin=(s, 0))) <= cut_bonds(box(l, l, origin=(s, 0)), 2) for l in range(1, 9) for s in range(4))
check('key box and problem, S_A = n_cut log 2 <= |dA| log 2 for every square and shift', ok, ok)

# the fold: the square of side l on the columns 1 to l cuts 2l singlets, its boundary has 4l bonds, alpha = log 2 / 2
for l in (2, 4, 6, 8):
    sq = box(l, l, origin=(1, 0))
    n, b = cut_singlets(sq), cut_bonds(sq, 2)
    check(f'fold, side {l}: 2l = {2 * l} cut singlets, 4l = {4 * l} cut bonds, alpha = log2/2', n == 2 * l and b == 4 * l
          and abs(n * ln2 / b - ln2 / 2) < 1e-15, (n, b))
# the fold and the problem: the same square on the columns 0 to l-1 cuts no dimer for any even l, alpha = 0
for l in (2, 4, 6, 8):
    sq = box(l, l)
    check(f'fold and problem, side {l} on the columns 0 to {l - 1}: 0 cut singlets with {4 * l} cut bonds',
          cut_singlets(sq) == 0 and cut_bonds(sq, 2) == 4 * l, (cut_singlets(sq), cut_bonds(sq, 2)))
check('problem, "for any even l": an odd side on the columns 0 to l-1 does cut singlets, one per row on its right side',
      cut_singlets(box(3, 3)) == 3, cut_singlets(box(3, 3)))

# the fold on the real state: 2 rows of 4 sites, singlets on (0,1) and (2,3) of each row, the square on the columns 1, 2
psi =np.kron(np.kron(singlet, singlet), np.kron(singlet, singlet)).reshape((2,) * 8)   # site index 4*y + x
sites = [4 * y + x for y in (0, 1) for x in (1, 2)]
rest = [i for i in range(8) if i not in sites]
S = entropy_of(np.linalg.svd(np.transpose(psi, sites + rest).reshape(16, -1), compute_uv=False) ** 2)
check('fold and problem, the real state: the square of side 2 on the columns 1 and 2 has 4 log 2', abs(S - 4 * ln2) < 1e-10, S / ln2)
sites = [4 * y + x for y in (0, 1) for x in (0, 1)]
rest = [i for i in range(8) if i not in sites]
S = entropy_of(np.linalg.svd(np.transpose(psi, sites + rest).reshape(16, -1), compute_uv=False) ** 2)
check('problem, the real state: a square that contains its dimers has S = 0', abs(S) < 1e-10, S)

# the problem: 4 log 2 and 8 log 2 against the volume law 4 log 2 and 16 log 2, the shifted square, the MPS cut
check('problem, 2l log 2 = 4 and 8 log 2 for l = 2 and 4', [cut_singlets(box(l, l, origin=(1, 0))) for l in (2, 4)] == [4, 8], True)
check('problem, the volume law |A| log 2 = 4 and 16 log 2', [l * l for l in (2, 4)] == [4, 16], True)
shifted = box(4, 4, origin=(0, 0))
check('problem, the square of side 4 on the columns 0 to 3 cuts no singlet and 16 bonds',
      cut_singlets(shifted) == 0 and cut_bonds(shifted, 2) == 16, (cut_singlets(shifted), cut_bonds(shifted, 2)))
for W in (2, 4, 10):
    strip = [(0, y) for y in range(W)]                       # the left part of the cut between the columns 0 and 1
    n = cut_singlets(strip)
    check(f'problem, a strip of W={W} rows: the cut between the columns 0 and 1 crosses W singlets, M >= 2^W',
          n == W and abs(n * ln2 - np.log(2 ** W)) < 1e-12, n)

# the problem, the order of the MPS: 4 rows and 4 columns of horizontal singlets, the real state of 16 spins. Column by
# column the largest cut holds W log 2 = 4 log 2, after the column 0, and row by row every cut holds at most log 2, M = 2
pairs = [((2 * m, y), (2 * m + 1, y)) for m in range(2) for y in range(4)]
labels = [s for pr in pairs for s in pr]
strip = np.array([1.0])
for _ in pairs:
    strip = np.kron(strip, singlet)
strip = strip.reshape((2,) * 16)
for name, order in (('column', [(x, y) for x in range(4) for y in range(4)]), ('row', [(x, y) for y in range(4) for x in range(4)])):
    v = np.transpose(strip, [labels.index(s) for s in order]).reshape(-1)
    Sc = np.array([entropy_of(np.linalg.svd(v.reshape(2 ** k, -1), compute_uv=False) ** 2) for k in range(1, 16)]) / ln2
    if name == 'column':
        check('problem, column by column the cut after the column 0 holds 4 log 2, the largest cut', abs(Sc[3] - 4) < 1e-10 and
              abs(Sc.max() - 4) < 1e-10, np.round(Sc, 6))
    else:
        check('problem, row by row every cut holds at most log 2, so M = 2 is enough', abs(Sc.max() - 1) < 1e-10, np.round(Sc, 6))
# the problem: on a strip of W rows and length at least W, every set of half of the sites has at least W bonds to the rest,
# so every order of the sites has a cut through at least W bonds, the cut after half of the sites
for W, Lx in ((2, 4), (3, 4), (4, 4), (3, 6)):
    sites = [(x, y) for x in range(Lx) for y in range(W)]
    ind = {s: i for i, s in enumerate(sites)}
    ends = np.array([(ind[(x, y)], ind[(x + dx, y + dy)]) for x, y in sites for dx, dy in ((1, 0), (0, 1))
                     if (x + dx, y + dy) in ind])
    least = min(int(np.sum(m[ends[:, 0]] != m[ends[:, 1]])) for m in
                (np.isin(np.arange(len(sites)), (0,) + c) for c in itertools.combinations(range(1, len(sites)), len(sites) // 2 - 1)))
    check(f'problem, a strip of {W} rows and {Lx} columns: half of the sites have at least W = {W} bonds to the rest', least == W, least)

# the first quiz: 16, 20 and 34 cut bonds, 32 along the long sides of the line, 2(a+b)
for (a, b), n in (((4, 4), 16), ((2, 8), 20), ((1, 16), 34)):
    check(f'first quiz, a region of {a} by {b} sites cuts {n} = 2(a+b) bonds', cut_bonds(box(a, b), 2) == n == 2 * (a + b),
          cut_bonds(box(a, b), 2))
check('first quiz, the line cuts 32 bonds along its long sides and 2 at its ends', 2 * 16 + 2 == 34, True)
# the feedback of the line: in a product of horizontal singlets on (2m, y), (2m+1, y) the square of 4 by 4 cuts 0 or 8
# singlets and the line of 16 sites 0 or 2, depending on where it sits, so the order of the regions can be reversed
shifts = {name: sorted({cut_singlets(box(a, b, origin=(s, t))) for s in range(4) for t in range(2)})
          for name, (a, b) in (('square', (4, 4)), ('rect', (8, 2)), ('line', (16, 1)))}
check('first quiz, horizontal singlets: the square cuts 0 or 8 singlets, the rectangle 0 or 4 and the line 0 or 2, so 8 > 4 > 2 '
      'reverses the order of the cut bonds', shifts['square'] == [0, 8] and shifts['rect'] == [0, 4] and shifts['line'] == [0, 2]
      and max(shifts['square']) > max(shifts['rect']) > max(shifts['line']), shifts)

# the second quiz: a cube of side l has 6 l^2 surface bonds, 24 and 96 for l = 2 and 4, 6e4 and 1e6 sites for l = 100
check('second quiz, the cubes of side 2 and 4 cut 24 and 96 bonds', [cut_bonds(box(l, l, l), 3) for l in (2, 4)] == [24, 96],
      [cut_bonds(box(l, l, l), 3) for l in (2, 4)])
check('second quiz, the cube of side 6 cuts 6 l^2 bonds, counted', cut_bonds(box(6, 6, 6), 3) == 6 * 36, True)
check('second quiz, l = 100: 10^6 sites and 6 x 10^4 cut bonds', 100 ** 3 == 10 ** 6 and 6 * 100 ** 2 == 6 * 10 ** 4, True)


# the caption of random_vs_gapped: L = 14, J1 = 1 on (0,1), (2,3), ..., J2 = 0.5, and a random state of seed 7
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


L = 14
H, states = heisenberg(L, [1.0 if i % 2 == 0 else 0.5 for i in range(L - 1)])
e, v = spl.eigsh(H, k=1, which='SA', tol=1e-13)
gs = np.zeros(2 ** L)
gs[states] = v[:, 0]
S_gs = np.array([entropy_of(np.linalg.svd(gs.reshape(-1, 2 ** l), compute_uv=False) ** 2) for l in range(1, L)]) / ln2
strong, weak = S_gs[0::2], S_gs[1::2]
check('random_vs_gapped caption, a cut through a strong bond is close to log 2', np.all(abs(strong - 1) < 0.005),
      (strong.min(), strong.max()))
check('random_vs_gapped caption and alt, a cut through a weak bond is about 0.14 log 2, computed 0.139 to 0.145',
      np.all(abs(weak - 0.14) < 0.0055) and np.all((weak > 0.1385) & (weak < 0.1455)), (weak.min(), weak.max()))
rng = np.random.default_rng(7)
rnd = rng.normal(size=2 ** L) + 1j * rng.normal(size=2 ** L)
rnd /= np.linalg.norm(rnd)
S_rnd = np.array([entropy_of(np.linalg.svd(rnd.reshape(-1, 2 ** l), compute_uv=False) ** 2) for l in range(1, L)]) / ln2
deficit = np.minimum(np.arange(1, L), L - np.arange(1, L)) - S_rnd
check('random_vs_gapped caption, the random state follows the maximum with its largest deficit at the middle, under 1 bit',
      np.argmax(deficit) == L // 2 - 1 and 0 < deficit.max() < 1 and deficit[0] < 0.01, np.round(deficit, 3))
check('random_vs_gapped caption, the random state stays far above the gapped one at the middle', S_rnd[6] > 5 and S_gs[6] < 1.1,
      (S_rnd[6], S_gs[6]))
check('random_vs_gapped alt, the red tent rises to about 6 at the middle, computed 6.2 to 6.35 in units of log 2',
      6.2 < S_rnd[6] < 6.35 and S_rnd[6] == S_rnd.max(), S_rnd[6])
print('all checks of page 07 hold')
