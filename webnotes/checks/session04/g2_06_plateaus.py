"""Session 4, the numbers that page 06 (Sections 4.6 and 4.7) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a box is an
assert, here or in the figure script that draws it. The crossings of the plateaus with the classical line at
B/B_1 = 1/N, the narrowing of the plateaus and the curves of the picture quiz are asserted in
figures/session04/_g2_hall.py, which plateaus.py and the three options run, and since build.py --verify runs only this
folder, its check runs here again. This script holds, in the order of the page: the resistances of the key box and of
the first quiz, the caption and the alt texts of plateaus and of the classical option, the problem on the density
3e11 cm^-2, the fold from the Peierls phases to minimal coupling with its condition phi << 1, the loop sums of the quiz
on the bond phase, and the sentence of the lab box in the stored source. The phases are written
in units of phi, the sum of the phases around one plaquette, so no factor of (4.4) enters. It finds the repository
from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session04/g2_06_plateaus.py"""
import os
import sys
sys.dont_write_bytecode = True

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(HERE, '..', '..')
FIG = os.path.join(WEB, 'figures', 'session04')
sys.path.insert(0, FIG)
sys.path.insert(0, os.path.join(FIG, '..'))
import _g2_hall as hall  # noqa: E402


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


h_planck, e_charge = 6.62607015e-34, 1.602176634e-19
rk = h_planck / e_charge ** 2

# the key box and the first quiz: h/(N e^2) is 25.8, 12.9 and 6.45 kOhm for N = 1, 2 and 4
plateau = {N: rk / N / 1e3 for N in (1, 2, 4)}
check('key box and quiz, h/(N e^2) in kOhm for N = 1, 2, 4, the page says 25.8, 12.9, 6.45',
      abs(plateau[1] - 25.8) < 0.05 and abs(plateau[2] - 12.9) < 0.05 and abs(plateau[4] - 6.45) < 0.005,
      {N: round(v, 4) for N, v in plateau.items()})

# the problem: n = 3e11 cm^-2, nu = n h/(e B), and the classical B/(n e) is h/(nu e^2)
n = 3e11 * 1e4                                       # in m^-2
B = np.linspace(0.5, 20, 400)
nu = n * h_planck / (e_charge * B)
check('problem, B/(n e) = h/(nu e^2) at every field', np.allclose(B / (n * e_charge), rk / nu, rtol=1e-12), True)
B2 = n * h_planck / (2 * e_charge)
B1 = n * h_planck / e_charge
check('problem, the field where N = 2 levels are just filled, the page says 6.20 T', abs(B2 - 6.20) < 0.005, round(B2, 4))
check('problem, B_1 of this density, where one level is filled, the page says 12.4 T', abs(B1 - 12.4) < 0.05, round(B1, 3))
# the figure plateaus and its options. _g2_hall.check asserts the flat parts, their narrowing, the rise of R_xy and the
# wrong staircase when a figure is drawn, and build.py --verify runs only this folder, so it runs here again.
flat, widths = hall.check()
check('figure, the classical line meets the plateaus N = 1 to 4 at B/B_1 = 1/N, inside their flat parts',
      all(flat[N][0] < 1 / N < flat[N][1] for N in (1, 2, 3, 4)), {N: tuple(round(float(v), 3) for v in flat[N]) for N in flat})
# the caption: every plateau crosses the classical line at 1/N. The blue curve starts at B/B_1 = 0.1, so N = 1 to 10.
psrc = open(os.path.join(FIG, 'plateaus.py')).read()
assert 'x = np.linspace(0.1, hall.XMAX, 3000)' in psrc
check('caption, every drawn plateau N = 1 to 10 is at 1/N where the classical line is, at B/B_1 = 1/N',
      all(abs(hall.quantum(1 / N) - 1 / N) < 1e-9 for N in range(1, 11)),
      max(abs(hall.quantum(1 / N) - 1 / N) for N in range(1, 11)))
# the alt text: four dots, at 1, 1/2, 1/3 and 1/4
check('alt text, plateaus.py draws the dots at 1/N for N = 1, 2, 3, 4 only',
      "for N in (1, 2, 3, 4):\n    style.guide(ax, y=1 / N, ls=':')\n    ax.plot([1 / N], [1 / N], 'o'" in psrc, True)
# the alt text of the classical option: a straight line from zero up to about 1.5
hsrc = open(os.path.join(FIG, '_g2_hall.py')).read()
check('alt text of the classical option, the line R_xy e^2/h = B/B_1 runs from 0 to XMAX, about 1.5',
      "np.linspace(0.1 if curve == 'quantum' else 0.0, XMAX, 3000)" in hsrc and hall.classical(0.0) == 0.0
      and abs(float(hall.classical(hall.XMAX)) - 1.5) < 0.1, hall.XMAX)

check('problem, B/(n e) at 6.20 T is h/2e^2, the page says 12.9 kOhm', abs(B2 / (n * e_charge) / 1e3 - 12.9) < 0.05
      and abs(B2 / (n * e_charge) - rk / 2) < 1e-6 * rk, round(B2 / (n * e_charge) / 1e3, 4))

# the fold, the chain: the hopping -t with the phase theta on every bond, as (4.4) gives for a uniform A along the chain.
# A ring of L sites has the levels -2t cos(k a - theta) with k a = 2 pi m / L, so the band is shifted by theta/a.
t, L = 1.0, 60
for theta in (0.0, 0.3, -0.7):
    Hm = np.zeros((L, L), complex)
    for j in range(L):
        Hm[(j + 1) % L, j] = -t * np.exp(1j * theta)        # the amplitude of the hop from j to j+1
        Hm[j, (j + 1) % L] = np.conj(Hm[(j + 1) % L, j])
    ka = 2 * np.pi * np.arange(L) / L
    exact = np.sort(-2 * t * np.cos(ka - theta))
    check(f'fold, ring of {L} sites with the bond phase {theta}: the levels are -2t cos(ka - theta)',
          np.allclose(np.linalg.eigvalsh(Hm), exact, atol=1e-12), True)
kk = np.linspace(-np.pi, np.pi, 200001)
theta = 0.3
band = -2 * t * np.cos(kk - theta)
check('fold, the minimum of the band moves from k a = 0 to k a = theta', abs(kk[np.argmin(band)] - theta) < 1e-4,
      kk[np.argmin(band)])
near = np.abs(kk - theta) < 0.05
check('fold, near the minimum -2t cos(ka - theta) = -2t + t (ka - theta)^2 to fourth order',
      np.max(np.abs(band[near] - (-2 * t + t * (kk[near] - theta) ** 2))) < (0.05 ** 4) / 12 * 2 * t * 1.01, True)
# a uniform phase on an open chain is removed by c_j -> exp(i j theta) c_j, while on a ring only L theta mod 2 pi matters
lev = {th: np.linalg.eigvalsh(np.array([[-t * np.exp(1j * th) if r == (c + 1) % L else (-t * np.exp(-1j * th) if c == (r + 1) % L else 0)
                                         for c in range(L)] for r in range(L)])) for th in (0.1, 0.1 + 2 * np.pi / L)}
check('fold, on a ring the phase theta and theta + 2 pi / L give the same levels', np.allclose(*lev.values(), atol=1e-12), True)

# the fold, the square lattice: the vertical bond of column x has the phase x phi, the horizontal bonds none. For one
# k_y the columns are the chain -2t cos(k_y a - x phi) with the hopping -t between them, a parabola in x around
# x0 = k_y a / phi near the bottom of the band.
phi = 2 * np.pi / 100
cols = np.arange(-45, 46)                                # less than one period 100 of the phase, so one minimum
for kya in (0.0, 0.2, -0.3):
    Hx = np.diag(-2 * t * np.cos(kya - cols * phi)) - t * (np.eye(len(cols), k=1) + np.eye(len(cols), k=-1))
    e, v = np.linalg.eigh(Hx)
    x_mean = np.sum(cols * np.abs(v[:, 0]) ** 2)
    check(f'fold, phi = 2 pi/100, k_y a = {kya}: the lowest state sits at x0 = k_y a / phi = {kya / phi:.2f}',
          abs(x_mean - kya / phi) < 0.05, round(x_mean, 3))
x0 = 0.2 / phi
xs = x0 + np.linspace(-3, 3, 601)
expand = np.max(np.abs(-2 * t * np.cos(0.2 - xs * phi) - (-2 * t + t * phi ** 2 * (xs - x0) ** 2)))
check('fold, -2t cos(k_y a - x phi) is -2t + t phi^2 (x - x0)^2 within 3 columns of x0, up to the quartic term t (3 phi)^4/12',
      expand <= t * (3 * phi) ** 4 / 12 * 1.001, expand)
# the condition of the fold: the expansion needs phi << 1, and the oscillator state has the width 1/sqrt(2 phi) columns.
# The parabola t phi^2 x^2 with the kinetic energy t k_x^2 has the lowest level t phi above -4t and the rms width
# 1/sqrt(2 phi). On the chain H(k_y = 0) the width is that, and the level is below t phi by about phi/8 of it, so the
# parabola holds when phi is small.
rel = {}
for q in (25, 50, 100, 200):
    ph = 2 * np.pi / q
    cq = np.arange(-q // 2 + 1, q // 2)
    Hq = np.diag(-2 * t * np.cos(-cq * ph)) - t * (np.eye(len(cq), k=1) + np.eye(len(cq), k=-1))
    eq_, vq = np.linalg.eigh(Hq)
    pq = np.abs(vq[:, 0]) ** 2
    wq = np.sqrt(np.sum((cq - np.sum(cq * pq)) ** 2 * pq))
    rel[q] = ((eq_[0] + 4 * t) / (t * ph) - 1, wq * np.sqrt(2 * ph))
check('fold, the width of the lowest state is 1/sqrt(2 phi) columns to 1 percent, for phi = 2 pi/q, q = 25 to 200',
      all(abs(w - 1) < 0.01 for _, w in rel.values()), {q: round(w, 4) for q, (_, w) in rel.items()})
check('fold, the lowest level is below t phi by about phi/8 of it, so the parabola needs phi << 1',
      all(abs(r / (-2 * np.pi / q / 8) - 1) < 0.1 for q, (r, _) in rel.items())
      and abs(rel[25][0]) > abs(rel[50][0]) > abs(rel[100][0]) > abs(rel[200][0]), {q: round(r, 4) for q, (r, _) in rel.items()})

# the quiz on the bond phase: the phases of the bonds of one plaquette with the lower left corner (x, y), counterclockwise,
# in units of phi. The option x phi gives the sum 1, the options y phi and 0 give 0, so only x phi has the flux phi.
def loop(vertical, x, y):
    """bottom, right, top, left, with no phase on the horizontal bonds, and the left bond gone down."""
    return 0.0 + vertical(x + 1, y) + 0.0 - vertical(x, y)


sums = {name: [loop(f, x, y) for x in range(-3, 4) for y in range(-3, 4)]
        for name, f in (('x phi', lambda x, y: x), ('y phi', lambda x, y: y), ('0', lambda x, y: 0))}
check('quiz, the loop sum in units of phi for the vertical phases x phi, y phi and 0, the page says 1, 0 and 0',
      set(sums['x phi']) == {1} and set(sums['y phi']) == {0} and set(sums['0']) == {0},
      {k: sorted(set(v)) for k, v in sums.items()})
vy = {name: (f(2, 1), f(2, 5)) for name, f in (('x phi', lambda x, y: x), ('y phi', lambda x, y: y))}
check('quiz, the bonds from (2,1) and from (2,5) upward have the phases 2 and 2 for x phi, and 1 and 5 for y phi',
      vy == {'x phi': (2, 2), 'y phi': (1, 5)}, vy)

# the lab box: the relative uncertainty 8.2e-11 has no unit, so labsource --check does not find it. The stored abstract
# of arXiv 1504.06511 has the sentence, and the box quotes the number.
sentence = ('We also measured an agreement of the quantized Hall resistance in graphene and GaAs/AlGaAs with an ultimate '
            'relative uncertainty of 8.2× 10^-11.')
stored = open(os.path.join(WEB, 'sources', 'session04', 'ribeiro-palau2015_arxiv1504.06511.txt'), encoding='utf-8').read()
page = open(os.path.join(WEB, 'pages', 'session04', '06-quantized-hall-plateaus-in-experiment.md'), encoding='utf-8').read()
box = page.split('::: lab', 1)[1].split('\n:::', 1)[0]
check('lab box, the stored abstract says 8.2x10^-11 and the box quotes 8.2x10^-11 with the link to the article',
      sentence in stored and r'$8.2\times10^{-11}$' in box and 'https://arxiv.org/abs/1504.06511' in box, True)
print('all checks of page 06 hold')
