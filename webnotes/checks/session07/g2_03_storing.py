"""Session 7, the numbers that page 03 (Section 7.3) quotes, checked in the order of the page.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or
in the figure script that draws it. The crossings of the line of one gigabyte at L=13 and L=26, the count
(L+1) 2^(L-1) of the red dots and the bytes at L=30 are asserted in figures/session07/matrix_vs_vector.py and
memory_scaling.py, and again here, so that build.py --verify runs them. Here the
Heisenberg chain is built as a dense matrix with np.kron, site 0 as the first factor, so the count of the fold is
checked on a second route, independent of the bit strings of the figure. The lab box is checked against the stored
source. The script finds the repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session07/g2_03_storing.py"""
import os, sys
sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
assert os.path.exists(os.path.join(REPO, 'webnotes', 'pages', 'session07'))

import numpy as np
from functools import reduce
from math import comb, log2, pi, sqrt


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


sx = np.array([[0, 1], [1, 0]]) / 2
sy = np.array([[0, -1j], [1j, 0]]) / 2
sz = np.diag([1.0, -1.0]) / 2
sp = np.array([[0, 1.0], [0, 0]])          # S^+ = |up><down|, with up the first basis state
sm = sp.T


def op(o, i, L):
    return reduce(np.kron, [o if j == i else np.eye(2) for j in range(L)])


def heisenberg(L):
    return sum(op(s, i, L) @ op(s, i + 1, L) for i in range(L - 1) for s in (sx, sy, sz)).real


# the singlet (7.3) of the dimer: unique ground state at -3/4, and every single-site spin has zero expectation value
H2 = heisenberg(2)
e, v = np.linalg.eigh(H2)
up, dn = np.array([1.0, 0]), np.array([0, 1.0])
singlet = (np.kron(up, dn) - np.kron(dn, up)) / np.sqrt(2)
check('text, the dimer has the singlet (7.3) as its unique ground state at -3/4',
      abs(e[0] + 0.75) < 1e-12 and e[1] - e[0] > 0.5 and abs(abs(v[:, 0] @ singlet) - 1) < 1e-12, np.round(e, 4))
m = [np.vdot(singlet, op(s, i, 2) @ singlet).real for s in (sx, sy, sz) for i in (0, 1)]
check('text, every single-site spin of the singlet has zero expectation value', np.allclose(m, 0, atol=1e-14), m)
# for the report, finding c9: the cause is the total spin zero, the same under every rotation, and the zero moments
# follow from it
S2 = sum((op(s, 0, 2) + op(s, 1, 2)) @ (op(s, 0, 2) + op(s, 1, 2)) for s in (sx, sy, sz))
check('text, the singlet has total spin zero, S_tot^2 = 0', abs(np.vdot(singlet, S2 @ singlet)) < 1e-14, 0)

# the key box and the text: 2^L coefficients, 4, 8, 16 for L = 2, 3, 4
check('key box and text, 2^L is 4, 8 and 16 for L = 2, 3, 4', [2 ** L for L in (2, 3, 4)] == [4, 8, 16],
      [2 ** L for L in (2, 3, 4)])

# the caption of memory_scaling: L=26 is the first size above one gigabyte (1e9 bytes) of 16-byte numbers
gb = 1e9 / 16
check('caption, 2^25 numbers are below one gigabyte and 2^26 above it, so the exact state crosses at about L=26',
      2 ** 25 < gb < 2 ** 26, (2 ** 25 * 16, 2 ** 26 * 16))
check('caption, the MPS curves are drawn for M = 16 and M = 64, as in figures/session07/memory_scaling.py',
      "for M in (16, 64)" in open(os.path.join(REPO, 'webnotes', 'figures', 'session07', 'memory_scaling.py')).read(),
      (16, 64))
# the same numbers as the asserts of the two figure scripts, here so that build.py --verify runs them too.
# The MPS curves are L M^2 without the factor 2 of the two spin values, as the caption says, and with or without it
# they stay 100 times below the line up to L=50
Lm = np.arange(1, 51)
check('caption, the MPS curves L M^2 and 2 L M^2 for M=64 stay 100 times below the line up to L=50',
      (Lm * 64 ** 2).max() < gb / 100 and (2 * Lm * 64 ** 2).max() < gb / 100, (2 * Lm * 64 ** 2).max())
check('caption, 2^30 numbers of 16 bytes are 1.72e10 bytes, 17.2 in units of 1e9 bytes and 16 in units of 2^30 bytes',
      round(2 ** 30 * 16 / 1e9, 1) == 17.2 and 2 ** 30 * 16 / 2 ** 30 == 16 and round(2 ** 30 * 16 / 1e10, 2) == 1.72,
      2 ** 30 * 16)
check('caption, corrected on 2026-11-22, the exact state has about seventeen gigabytes at L=30 in the unit of the dashed line',
      round(2 ** 30 * 16 / 1e9) == 17 and round(2 ** 30 / gb) == 17, 2 ** 30 / gb)
check('caption of matrix_vs_vector, the dense matrix 4^L crosses the line at L=13 and the vector 2^L at L=26',
      4 ** 12 < gb < 4 ** 13 and min(L for L in range(1, 40) if 4 ** L > gb) == 13
      and min(L for L in range(1, 40) if 2 ** L > gb) == 26, (4 ** 12 * 16, 4 ** 13 * 16))


def nonzeros_bits(L):
    """Nonzero elements of the open Heisenberg chain on the bit strings, site i as bit i, as the figure counts them."""
    s = np.arange(2 ** L, dtype=np.int64)
    diag = np.zeros(2 ** L)
    off = 0
    for i in range(L - 1):
        anti = ((s >> i) & 1) != ((s >> (i + 1)) & 1)
        diag += np.where(anti, -0.25, 0.25)
        off += int(anti.sum())
    return int(np.count_nonzero(np.abs(diag) > 1e-12)) + off


bits = {L: nonzeros_bits(L) for L in range(12, 23, 2)}
check('caption of matrix_vs_vector, the bit strings give (L+1) 2^(L-1) for even L = 12 to 22, below the line',
      all(n == (L + 1) * 2 ** (L - 1) and n < gb for L, n in bits.items()), bits)

# the fold: the nonzero elements of the open Heisenberg chain, from the dense np.kron matrix
H2nz = np.count_nonzero(np.abs(H2) > 1e-12)
check('fold, L=2 has 6 nonzero elements of 16, diagonal 1/4, -1/4, -1/4, 1/4 and two off-diagonal 1/2',
      H2nz == 6 and np.allclose(np.diag(H2), [0.25, -0.25, -0.25, 0.25]) and abs(H2[1, 2] - 0.5) < 1e-12, H2nz)
counts = {}
for L in range(2, 11):
    H = heisenberg(L)
    counts[L] = int(np.count_nonzero(np.abs(H) > 1e-12))
even = {L: counts[L] for L in counts if L % 2 == 0}
check('fold, for even L the count is (L+1) 2^(L-1), L = 2 to 10',
      all(n == (L + 1) * 2 ** (L - 1) for L, n in even.items()), even)
check('fold, (L+1) 2^(L-1) = 2^L + (L-1) 2^(L-1), which is (L+1)/2 times the vector',
      all((L + 1) * 2 ** (L - 1) == 2 ** L + (L - 1) * 2 ** (L - 1) for L in range(2, 30)), True)
check('fold, for odd L some diagonal elements vanish, 84 instead of 96 for L=5 (and 472 instead of 512 for L=7)',
      counts[5] == 84 and (5 + 1) * 2 ** 4 == 96 and counts[7] == 472, (counts[5], counts[7]))
H6 = heisenberg(6)
offd = int(np.count_nonzero(np.abs(H6 - np.diag(np.diag(H6))) > 1e-12))
check('fold, the off-diagonal elements are (L-1) 2^(L-1), one per antiparallel bond, for L=6',
      offd == 5 * 2 ** 5 and np.count_nonzero(np.abs(np.diag(H6)) > 1e-12) == 2 ** 6, offd)

# the lab box: J = 226 meV is 2600 K, and room temperature (300 K) is 0.11 J
kB = 8.617333262e-2          # meV per K
check('lab box, J/k_B = 226 meV / k_B is about 2600 K', abs(226 / kB - 2600) < 50, round(226 / kB, 1))
check('lab box, k_B T at 300 K is about 0.11 J', round(kB * 300 / 226, 2) == 0.11, round(kB * 300 / 226, 4))
src = open(os.path.join(REPO, 'webnotes', 'sources', 'session07', 'zaliznyak2004_arxivcond-mat-0312724.txt'),
           encoding='utf-8').read()
check('lab box, the source states J = 226(12) meV, inelastic neutron scattering and the two-spinon continuum',
      'J = 226(12) meV' in src and 'inelastic neutron scattering' in src and 'two-spinon continuum' in src
      and 'S=1/2 antiferromagnetic Heisenberg spin chain' in src, 'zaliznyak2004')
check('lab box, the source gets J from the lower boundary of the continuum, which extends up to about 360 meV',
      'The lower boundary of the continuum extends up to ≈ 360 meV, which corresponds to an exchange constant '
      'J = 226(12) meV.' in src, 360)
# second route for 360 meV and J: the lower boundary of the two-spinon continuum of the Heisenberg chain is
# (pi/2) J |sin q|, with its top pi J / 2, and J = 226(12) meV gives 336 to 374 meV, which holds 360
lo, hi = np.pi / 2 * (226 - 12), np.pi / 2 * (226 + 12)
check('lab box, pi J / 2 for J = 226(12) meV holds 360 meV', lo < 360 < hi, (round(lo, 1), round(hi, 1)))

# the first quiz: L=40 is 2^40 = 1.1e12 numbers, 1.76e13 bytes (about 17 TB, 16 TiB), L=30 is 1.7e10 bytes,
# ten more sites multiply by 1024, and 40 numbers of 16 bytes are 640 bytes
b40, b30 = 2 ** 40 * 16, 2 ** 30 * 16
check('quiz 1, 2^40 is about 1.1e12', round(2 ** 40 / 1e12, 1) == 1.1, 2 ** 40)
check('quiz 1, 2^40 numbers of 16 bytes are 1.76e13 bytes, 17.6 in units of 1e12 bytes and 16 in units of 2^40 bytes',
      round(b40 / 1e13, 2) == 1.76 and round(b40 / 1e12, 1) == 17.6 and b40 / 2 ** 40 == 16, b40)
check('quiz 1, 2^30 numbers of 16 bytes are 1.7e10 bytes', round(b30 / 1e10, 1) == 1.7, b30)
check('quiz 1, ten more sites multiply the memory by about one thousand', 2 ** 10 == 1024, 1024)
check('quiz 1, 40 numbers of 16 bytes are 640 bytes', 40 * 16 == 640, 640)
# the third option counts one complex number per site. A spin 1/2 state (a, b) has four real numbers, and its norm and
# its phase leave two, the angles of cos(t/2), e^(i p) sin(t/2), which is one complex number of 16 bytes. The MPS with
# M=1 keeps both amplitudes, two complex numbers per site, so 80 numbers and 1280 bytes for 40 sites
rng = np.random.default_rng(3)
fits = []
for _ in range(200):
    a = rng.normal(size=2) + 1j * rng.normal(size=2)
    a /= np.linalg.norm(a)
    t, p = 2 * np.arccos(abs(a[0])), np.angle(a[1]) - np.angle(a[0])
    fits.append(abs(abs(np.vdot(np.array([np.cos(t / 2), np.exp(1j * p) * np.sin(t / 2)]), a)) - 1) < 1e-12)
check('quiz 1, a spin state fixed up to norm and phase is two real numbers, one complex number of 16 bytes',
      all(fits) and 4 - 2 == 2 and np.dtype(np.complex128).itemsize == 16, 16)
check('quiz 1, the MPS with M=1 stores two numbers per site, 80 numbers and 1280 bytes for 40 sites',
      2 * 40 == 80 and 80 * 16 == 1280, 1280)

# the second quiz: 2^L+4 and L 2^L hold from L=2 to 3 only, 2^(L+1) always, and 10 to 11 adds 1024
check('quiz 2, 2^L+4 gives 8 for L=2 and 12 for L=3, while 2^4=16', 2 ** 2 + 4 == 8 == 2 ** 3 and 2 ** 3 + 4 == 12, 12)
check('quiz 2, L 2^L gives 8 for L=2 and 24 for L=3, while 2^4=16', 2 * 4 == 8 and 3 * 8 == 24 and 2 ** 4 == 16, 24)
check('quiz 2, from L=10 to L=11 the count grows by 1024', 2 ** 11 - 2 ** 10 == 1024, 1024)

# the problem: H conserves S^z_tot, the sector S^z_tot = 0 has binom(L, L/2) states, 6 of 16 for L=4 and
# 1.55e8 of 1.07e9 for L=30, a factor 6.9, Stirling 2^L sqrt(2/(pi L)), and 6.9 = 2^2.8, two or three sites
for L in (4, 6):
    Sz = sum(op(sz, i, L) for i in range(L))
    H = heisenberg(L)
    check(f'problem, [H, S^z_tot] = 0 for L={L}', np.abs(H @ Sz - Sz @ H).max() < 1e-12, 0)
sector4 = [s for s in range(16) if bin(s).count('1') == 2]
check('problem, the sector S^z_tot = 0 of L=4 has 6 states', len(sector4) == 6 == comb(4, 2), len(sector4))
c30 = comb(30, 15)
check('problem, binom(30,15) = 1.55e8 and 2^30 = 1.07e9', round(c30 / 1e8, 2) == 1.55 and round(2 ** 30 / 1e9, 2) == 1.07,
      c30)
ratio = 2 ** 30 / c30
stir = 1 / sqrt(2 / (pi * 30))
check('problem, the factor 2^30 / binom(30,15) is 6.9, and Stirling gives 6.9 too',
      round(ratio, 1) == 6.9 and round(stir, 1) == 6.9, (round(ratio, 4), round(stir, 4)))
check('problem, 6.9 is about 2^2.8', round(log2(ratio), 1) == 2.8, round(log2(ratio), 3))
# the sector grows exponentially, as 2^L / sqrt(L), with the prefactor sqrt(2/pi) = 0.798 that Stirling gives
pref = [comb(L, L // 2) / (2 ** L / sqrt(L)) for L in range(10, 61, 2)]
check('problem, binom(L, L/2) / (2^L / sqrt L) grows from 0.778 to 0.795 for even L = 10 to 60, toward sqrt(2/pi) = 0.798',
      all(0.77 < x < sqrt(2 / pi) for x in pref) and all(np.diff(pref) > 0) and pref[-1] > 0.99 * sqrt(2 / pi),
      (round(pref[0], 4), round(pref[-1], 4)))


# the largest L that fits in a memory of m bytes, with 16 bytes per number, for the full space 2^L and for the sector
# S^z_tot = 0, whose size is binom(L, L // 2) for even and odd L (for odd L the sectors S^z_tot = +-1/2)
def lmax(m, size):
    L = 1
    while size(L + 1) * 16 <= m:
        L += 1
    return L


def shift(m):
    return lmax(m, lambda L: comb(L, L // 2)) - lmax(m, lambda L: 2 ** L)


named = {m: shift(m) for m in (1e9, 2 ** 30, 16e9, 2 ** 34, 1e12)}
sweep = sorted({shift(m) for m in np.logspace(9, 12, 601)})
check('problem, the sector moves the largest chain by 3 sites for 1e9, 16e9 and 1e12 bytes, and by 2 for 2^30 and 2^34',
      named == {1e9: 3, 2 ** 30: 2, 16e9: 3, 2 ** 34: 2, 1e12: 3}, named)
check('problem, for every memory from one gigabyte to one terabyte the shift is two or three sites',
      sweep == [2, 3], sweep)
check('problem, beyond one terabyte the shift can reach four sites, so the range of the memory is needed',
      4 in {shift(m) for m in np.logspace(12, 15, 301)}, 4)

# the try-it box: the energy per site of the infinite chain is 1/4 - ln 2 = -0.443
check('try-it, 1/4 - ln 2 = -0.443', round(0.25 - np.log(2), 3) == -0.443, 0.25 - np.log(2))
# the notebook box and the try-it, rewritten on 2026-11-22 to match the cell: its code calls gs_energy(mode="DMRG"), so it
# runs DMRG and not exact diagonalization, and it imports dmrgpy only, not pyqula
import json
nb = json.load(open(os.path.join(REPO, 'jupyter-notebooks', 'session7.ipynb'), encoding='utf-8'))
src = [''.join(c['source']) for c in nb['cells']]
k = next(i for i, t in enumerate(src) if t.startswith('## Energy of the Heisenberg model as a function of the system size'))
code, quiz = src[k + 1], src[k + 2]
check('notebook box and try-it, the cell calls sc.gs_energy(mode="DMRG") and imports dmrgpy and not pyqula',
      'sc.gs_energy(mode="DMRG")' in code and 'from dmrgpy import spinchain' in code and 'pyqula' not in code, 'DMRG')
check('notebook box, the quiz of the cell asks for the biggest system of exact diagonalization',
      'biggest system that you could compute with exact diagonalization' in quiz, 'quiz')
print('all checks of page 03 hold')
