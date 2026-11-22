"""Session 5, the numbers that page 09 (Sections 5.9 and 5.10) states and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a box is an assert, here
or in the figure script that draws it. The numbers of the chain figure gap_any_mu (k_F = 0.93, 1.57 and 2.21, the minimum 0.3)
are asserted in figures/session05/gap_any_mu.py, those of the triangular lattice (the band from -3 to 6, the crossings, 0.4) in
figures/session05/g2_swave_triangular_mu.py, the 1.88 of the pocket at X in figures/session05/pockets_nodes.py, and the four
nodes and the 1.5 of the picture quiz in figures/session05/_g2_fsgap.py. This script holds the rest, with numpy only, and it
writes no file. From the repository, found from the path of this script, it reads only the tracked source of the lab box,
webnotes/sources/session05/kim2022_s41586-022-04715-z.txt.

Run it from anywhere:  python3 webnotes/checks/session05/g2_09_gap_dispersion.py"""
import os

import numpy as np
from scipy.optimize import minimize_scalar

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


t = 1.0
k = np.linspace(-np.pi, np.pi, 801)
KX, KY = np.meshgrid(k, k, indexing='ij')
C = np.cos(KX) + np.cos(KY)


def eps(mu):
    return -2 * t * C - mu


# ---- the caption of gap_any_mu, again from the formula
kF = np.arccos(np.array([1.2, 0.0, -1.2]) / (2 * t))
check('gap_any_mu: k_F = arccos(-mu/2t) = 0.93, 1.57, 2.21 for mu = -1.2, 0, 1.2', np.allclose(kF, [0.93, 1.57, 2.21], atol=5e-3),
      np.round(kF, 3))

# ---- the key box of 5.10: min E against the smallest |Delta| on the Fermi surface. In s = cos kx + cos ky the band is
# -2t s - mu, and a pairing that depends on k only through s, the uniform one and the extended s-wave, has E^2 = eps^2 + |D(s)|^2
for mu in (-3.0, -1.0, 0.0, 1.5):
    E = np.sqrt(eps(mu)**2 + 0.3**2)
    check(f'key: a uniform Delta=0.3 on the square lattice at mu={mu}, min E = 0.3 = |Delta| on the Fermi surface',
          abs(E.min() - 0.3) < 2e-3 and E.min() >= 0.3 - 1e-12, round(E.min(), 4))
E = np.sqrt(eps(-1.0)**2 + (np.cos(KX) - np.cos(KY))**2 * 0.2**2)
check('key: a node on the Fermi surface, d-wave at mu=-t, min E = 0', E.min() < 2e-2, round(E.min(), 4))
for D0, close in ((0.1, True), (1.0, False)):
    res = minimize_scalar(lambda s: (-2 * t * s + t)**2 + (D0 * s)**2, bounds=(-2, 2), method='bounded')
    Emin, onFS = np.sqrt(res.fun), D0 * 0.5
    check(f'key: extended s-wave D0 (cos kx + cos ky) at mu=-t, D0={D0}: min E {Emin:.4f} against {onFS:.4f} on the Fermi surface',
          (abs(Emin - onFS) / onFS < 2e-3) == close and Emin <= onFS + 1e-12, (round(Emin, 5), onFS))

# ---- the paragraph after the key box: the extended s-wave at mu=-t, by the closed form and by the minimizer. With
# s = cos kx + cos ky the band is eps = -2t s + t, so Delta = D0 s = D0 (t - eps)/2t, a straight line in eps with the slope
# -D0/2t. For a line Delta_F + a eps the smallest E is Delta_F / sqrt(1 + a^2), at s = 2/(4 + D0^2) for t=1
for D0, Eprint, Fprint in ((1.0, '0.447', '0.5'), (0.1, '0.0499', '0.05')):
    s_star = 2 / (4 + D0**2)
    closed = np.sqrt((1 - 2 * s_star)**2 + (D0 * s_star)**2)
    line = (D0 / 2) / np.sqrt(1 + (D0 / 2)**2)
    res = minimize_scalar(lambda s: (-2 * t * s + t)**2 + (D0 * s)**2, bounds=(-2, 2), method='bounded', options={'xatol': 1e-12})
    grid = np.sqrt((-2 * t * C + t)**2 + (D0 * C)**2).min()
    ok = np.isclose(closed, line) and abs(np.sqrt(res.fun) - closed) < 1e-9 and closed <= grid <= closed + 2e-3
    ok = ok and f'{closed:.{len(Eprint) - 2}f}' == Eprint and np.isclose(D0 * 0.5, float(Fprint))
    check(f'after the key box: extended s-wave D0={D0}t at mu=-t, min E = {Eprint}t against {Fprint}t on the Fermi surface, '
          'closed form, line formula, minimizer and the 801x801 mesh', ok, (round(closed, 5), round(np.sqrt(res.fun), 5), round(grid, 5)))
check('after the key box: the slope dDelta/deps = -D0/2t of the extended s-wave', np.isclose(np.polyfit(eps(-1.0).ravel(), 0.7 * C.ravel(), 1)[0],
      -0.7 / 2), round(np.polyfit(eps(-1.0).ravel(), 0.7 * C.ravel(), 1)[0], 6))
check('after the key box: the line Delta=0.5 at s=1/2 gives 0.4472 = sqrt(0.2) for D0=t', np.isclose(0.5 / np.sqrt(1.25), np.sqrt(0.2))
      and abs(np.sqrt(0.2) - 0.4472) < 1e-4, round(np.sqrt(0.2), 5))
# the left side is never larger than the right side: min over the zone of E <= min over the Fermi surface of |Delta|
sgrid = np.linspace(-2, 2, 400001)
worst = -1.0
for mu in (-3.5, -2.0, -1.0, 0.5, 2.0, 3.0):
    for D0 in (0.1, 0.5, 1.0, 2.0):
        for f in (lambda s: np.ones_like(s), lambda s: s, lambda s: s**2 - 0.3):     # uniform, extended s, and a curved one
            onFS = abs(D0 * f(np.array([-mu / (2 * t)]))[0])
            Emin = np.sqrt((-2 * t * sgrid - mu)**2 + (D0 * f(sgrid))**2).min()
            worst = max(worst, Emin - onFS)
check('key: min E is never above |Delta| on the Fermi surface, 72 cases of mu, D0 and Delta(s)', worst <= 1e-9, worst)

# ---- the quiz on the pocket at X
check('quiz on X: cos kx - cos ky = -2 at X = (pi, 0)', np.isclose(np.cos(np.pi) - np.cos(0), -2), -2)
# the first option, old text: "|Delta_d| approx 2 Delta_0" holds, and "E >= 2 Delta_0" does not (open for the lecturer)
ang = np.linspace(0, 2 * np.pi, 10000, endpoint=False)
rng = {}
for rad in (0.1, 0.3, 0.5):
    g = np.abs(np.cos(np.pi + rad * np.cos(ang)) - np.cos(rad * np.sin(ang)))
    rng[rad] = (round(g.min(), 4), round(g.max(), 4))
    check(f'quiz on X: on a pocket of radius {rad} around X, 1.876 <= |Delta_d|/Delta_0 < 2, so close to 2 and below it',
          g.min() >= 1.876 - 1e-4 and g.max() < 2, rng[rad])
check('quiz on X: the 1.88 of the caption is the pocket of radius 0.5', rng[0.5][0] >= 1.876 and round(rng[0.5][1], 2) == 1.88, rng[0.5])

# ---- the lab box: the filling of the stored source, in words
src = open(os.path.join(REPO, 'webnotes', 'sources', 'session05', 'kim2022_s41586-022-04715-z.txt')).read()
check('lab: the tracked source says "two to three holes per moire unit cell", the probe and "consistent with"',
      'in a density window spanning two to three holes per moire unit cell' in src and 'scanning tunneling microscopy' in src
      and 'consistent with a gate-tunable transition from a gapped to a nodal superconductor' in src, 'found')

# ---- the quiz with equations as options
E = np.sqrt(eps(-1.0)**2 + 0.2**2)
check('quiz: a uniform Delta_0 = 0.2t at mu=-t has the smallest energy 0.2t', abs(E.min() - 0.2) < 2e-3, round(E.min(), 4))
for mu in (-3.5, -1.0, 0.0, 2.0, 3.9):
    k0 = np.arccos(-mu / (4 * t))
    check(f'quiz: the Fermi surface at mu={mu} crosses the diagonal at cos k = -mu/4t', abs(-2 * t * 2 * np.cos(k0) - mu) < 1e-12,
          round(k0, 4))
check('quiz: at mu=0 the Fermi surface passes through (pi/2, pi/2), where cos kx - cos ky = 0',
      abs(-2 * t * 2 * np.cos(np.pi / 2)) < 1e-12 and abs(np.cos(np.pi / 2) - np.cos(np.pi / 2)) < 1e-15, 0)
fs0 = np.abs(eps(0.0)) < 1e-2
check('quiz: at mu=0 the extended s-wave cos kx + cos ky vanishes on the whole Fermi surface', np.abs(C[fs0]).max() < 1e-2,
      round(np.abs(C[fs0]).max(), 4))

# ---- the problem: mu=-t and the d-wave gap
k0 = np.arccos(0.25)
check('problem: cos k0 = 1/4, k0 = 1.318, about 0.42 pi', abs(k0 - 1.318) < 5e-4 and abs(k0 / np.pi - 0.42) < 5e-3,
      (round(k0, 4), round(k0 / np.pi, 4)))
pts = [(sx * k0, sy * k0) for sx in (1, -1) for sy in (1, -1)]
ok = all(abs(-2 * t * (np.cos(a) + np.cos(b)) + t) < 1e-12 and abs(np.cos(a) - np.cos(b)) < 1e-12 for a, b in pts)
check('problem: E = 0 at the four points (+-k0, +-k0) of the Fermi surface', ok, len(pts))
th = np.linspace(0, 2 * np.pi, 3600, endpoint=False) + 1e-4
r = np.array([minimize_scalar(lambda r: (np.cos(r * np.cos(a)) + np.cos(r * np.sin(a)) - 0.5)**2,
                              bounds=(0, np.pi / max(abs(np.cos(a)), abs(np.sin(a)))), method='bounded').x for a in th])
fx, fy = r * np.cos(th), r * np.sin(th)
d = np.cos(fx) - np.cos(fy)
check('problem: four zeros on the Fermi surface and nowhere else', np.sum(np.diff(np.sign(d)) != 0) + (np.sign(d[0]) != np.sign(d[-1])) == 4,
      int(np.sum(np.diff(np.sign(d)) != 0)))
check('problem: |Delta_d| is largest on the axes, cos kx = -1/2 and ky = 0, with 1.5 Delta_0 there',
      abs(np.abs(d).max() - 1.5) < 1e-6 and abs(np.cos(2 * np.pi / 3) - np.cos(0) + 1.5) < 1e-12, round(np.abs(d).max(), 5))
print('all checks of page 09 hold')
