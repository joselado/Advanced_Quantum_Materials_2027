"""Session 2, the numbers that page 06 (Section 2.6) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a box is an
assert, here or in the figure script that draws it. The numbers of the figure aliasing are asserted in
figures/session02/aliasing.py, and those of the three wave pictures of the quiz in _g2_wave.py. This script holds the
rest, in the order of the page. It uses numpy only and writes no file.

Run it from anywhere:  python3 webnotes/checks/session02/g2_06_quasi_momentum.py"""
from math import factorial

import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# the steps fold: the Taylor series of a plane wave is e^{ika} e^{ikx}, so the translation by a has the eigenvalue
# e^{ika}, and a sum of plane waves with k a = phi + 2 pi m has the same eigenvalue e^{i phi}
a, k = 1.3, 0.7
x = np.linspace(-2, 2, 9)
series = sum((1j * k * a) ** n / factorial(n) for n in range(40)) * np.exp(1j * k * x)
check('fold: the Taylor series of e^{ikx} is e^{ika} e^{ikx}', np.allclose(series, np.exp(1j * k * (x + a))),
      np.round(series[0], 6))
phi = 0.9
rng = np.random.default_rng(1)
c = rng.normal(size=5) + 1j * rng.normal(size=5)
psi = lambda x: sum(c[m] * np.exp(1j * (phi + 2 * np.pi * (m - 2)) / a * x) for m in range(5))
check('fold: a sum of plane waves with ka = phi + 2 pi m has psi(x+a) = e^{i phi} psi(x)',
      np.allclose(psi(x + a), np.exp(1j * phi) * psi(x)), np.round(psi(x + a)[0] / psi(x)[0], 6))

# the key box: k and k + 2 pi/a give the same phase, so the same state on the sites x = n a
n = np.arange(-6, 7)
check('key box: e^{i k n a} = e^{i (k + 2 pi/a) n a} on every site',
      np.allclose(np.exp(1j * k * n * a), np.exp(1j * (k + 2 * np.pi / a) * n * a)), len(n))

# the first quiz: a = 1, k = 0.5, e^{i 0.5} = e^{i (0.5 + 2 pi)}, a shift by pi/a gives a sign on every second site
check('quiz 1: e^{i0.5} and e^{i(0.5+2pi)} are the same number', np.isclose(np.exp(0.5j), np.exp(1j * (0.5 + 2 * np.pi))),
      np.round(np.exp(0.5j), 6))
check('quiz 1: a shift of k by pi/a multiplies the site n by (-1)^n',
      np.allclose(np.exp(1j * (0.5 + np.pi) * n), (-1.0) ** n * np.exp(0.5j * n)), 'ok')
check('quiz 1: e^{2 pi i n} = 1', np.allclose(np.exp(2j * np.pi * n), 1), 'ok')

# the picture quiz, the alt texts of the two wrong options, on the dots cos(0.5 n), n = 0 to 6, of _g2_wave.py.
# The slow wave cos(1.0 x) passes through the first dot, misses the dots at x = 1, 2, 3, 5, 6 by more than 0.3 and
# the dot at x = 2 by more than 0.9, and comes within 0.25 at x = 4 only, so it misses most of the others. The fast
# wave cos[(0.5 + pi) x] passes through the dots at even x and gives the opposite values at odd x, and at x = 3 both
# values are below 0.1 in size, so there it is close to the dot.
nd = np.arange(7)
dots = np.cos(0.5 * nd)
slow, fast = np.cos(1.0 * nd), np.cos((0.5 + np.pi) * nd)
miss = np.abs(slow - dots)
check('picture quiz alt: the slow wave meets the first dot and misses x=1,2,3,5,6 by more than 0.3, x=2 by more than 0.9',
      miss[0] < 1e-12 and np.all(miss[[1, 2, 3, 5, 6]] > 0.3) and miss[2] > 0.9 and miss[4] < 0.25, np.round(miss, 3))
check('picture quiz alt: the fast wave meets the dots at even x and the opposite values at odd x',
      np.allclose(fast[0::2], dots[0::2]) and np.allclose(fast[1::2], -dots[1::2]), np.round(fast, 3))
check('picture quiz alt: at x=3 the dot and the fast wave are both below 0.1 in size, so close to each other',
      abs(dots[3]) < 0.1 and abs(fast[3]) < 0.1 and abs(fast[3] - dots[3]) < 0.15, (round(dots[3], 4), round(fast[3], 4)))

# the second quiz: the zone (-pi/a, pi/a] has the width 2 pi for a = 1 and pi for a' = 2, a ring of 100 sites has 100
# values of k in the zone of a and 50 in the zone of 2a, and with two sites per cell the single band folds into two
check('quiz 2: the zone has the width 2 pi for a=1 and pi for a=2', np.isclose(2 * np.pi / 1, 2 * np.pi)
      and np.isclose(2 * np.pi / 2, np.pi), (2 * np.pi, np.pi))
L = 100
k1 = 2 * np.pi * np.arange(L) / L                      # the allowed phases with the cell a = 1
k2 = 2 * np.pi * np.arange(L // 2) / (L // 2)          # the allowed phases per cell with the cell 2a
check('quiz 2: a ring of 100 sites has 100 values of k with a and 50 with 2a', len(np.unique(np.round(k1, 9))) == 100
      and len(np.unique(np.round(k2, 9))) == 50, (len(k1), len(k2)))
H = -(np.roll(np.eye(L), 1, axis=1) + np.roll(np.eye(L), -1, axis=1))
folded = np.sort(np.concatenate([[-2 * np.cos((p + 2 * np.pi * m) / 2) for m in range(2)] for p in k2]))
check('quiz 2: with two sites per cell the band folds into two bands, the same 100 states', len(folded) == 100
      and np.allclose(folded, np.sort(np.linalg.eigvalsh(H))), folded[:2])

# the problem: a = 0.3 nm, pi/a = 10.5 nm^-1, 2 pi/a = 20.94 nm^-1, 25 - 20.94 = 4.06 nm^-1, inside the zone, the
# same values on the sites, and the same band energy, here for the chain band -2t cos(k a)
a = 0.3
check('problem: pi/a = 10.5 nm^-1', round(np.pi / a, 1) == 10.5, np.pi / a)
check('problem: 2 pi/a = 20.94 nm^-1', round(2 * np.pi / a, 2) == 20.94, 2 * np.pi / a)
kp = 25 - 2 * np.pi / a
check('problem: 25 - 2 pi/a = 4.06 nm^-1, inside the zone and 25 outside', round(kp, 2) == 4.06
      and -np.pi / a < kp <= np.pi / a and 25 > np.pi / a, kp)
xs = a * np.arange(-5, 6)
check('problem: e^{i 25 x} = e^{i 4.06 x} on the sites x = n a', np.allclose(np.exp(25j * xs), np.exp(1j * kp * xs)), 'ok')
check('problem: the band energy is the same at 25 and at 4.06 nm^-1', np.isclose(-2 * np.cos(25 * a), -2 * np.cos(kp * a)),
      -2 * np.cos(kp * a))
