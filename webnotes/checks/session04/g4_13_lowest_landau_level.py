"""Session 4, the numbers and the steps that page 13 (Sections 4.13 to 4.15, the symmetric gauge, the lowest Landau level
and the filled level) quotes. One check script per page is the rule: every number of a key box, a fold, a feedback, a
caption, a solution is an assert here or in the figure script that draws it. lll_radius.py asserts the radii of its
figure. droplet_density.py draws its figure without an assert, so the numbers of its caption are asserted here, the
filled level from the orbitals and the Laughlin state from four runs of the Monte Carlo of _g4_laughlin_mc.py.

The charge is +e in the field B z, as webnotes/conventions/session04.md says, with pi = p - e A and the symmetric gauge
A = B/2 (-y, x). sympy checks the step of the fold, pi_x + i pi_y = -2 i hbar (d_zbar + z/4 l_B^2), the states z^m times the
Gaussian, and the three functions of the quiz, with the Hamiltonian written in x and y, which does not use the ladder
operators of the page. The script writes no file and takes about 40 s, most of it in the Monte Carlo.

The blocks marked "corrected on 2026-11-22" back the sentences of the old text that were corrected on that day, after
the lecturer chose to fix the errors of the old text. The block marked "decided on 2026-11-22" backs the sentence of
Section 4.14, |C_tot| = N and |sigma_xy| = nu e^2/h, which the lecturer picked that day."""
import os
import sys
from math import factorial

import numpy as np
import sympy as sp

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'figures', 'session04'))
import _g4_laughlin_mc as mc  # noqa: E402

HBAR, E, H = 1.054571817e-34, 1.602176634e-19, 6.62607015e-34


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# ---------------------------------------------------------------- the fold, from the ladder operator to (4.9)
x, y = sp.symbols('x y', real=True)
hb, e, B = sp.symbols('hbar e B', positive=True)
lB2 = hb / (e * B)
zz, zb = x + sp.I * y, x - sp.I * y
f = sp.Function('f')(x, y)
dzb = lambda g: (sp.diff(g, x) + sp.I * sp.diff(g, y)) / 2          # d/d zbar
pix = lambda g: -sp.I * hb * sp.diff(g, x) + e * B * y / 2 * g      # pi = p - e A, A = B/2 (-y, x)
piy = lambda g: -sp.I * hb * sp.diff(g, y) - e * B * x / 2 * g
lhs = pix(f) + sp.I * piy(f)
rhs = -2 * sp.I * hb * (dzb(f) + zz / (4 * lB2) * f)
check('pi_x + i pi_y = -2 i hbar (d_zbar + z/4 l_B^2) for the charge +e, with l_B^2 = hbar/eB', sp.simplify(sp.expand(lhs - rhs)) == 0, 'sympy')
comm = sp.simplify(pix(piy(f)) - piy(pix(f)))
check('[pi_x, pi_y] = i hbar e B = i hbar^2/l_B^2', sp.simplify(comm - sp.I * hb * e * B * f) == 0, comm)
a_op = lambda g: sp.sqrt(lB2) / (sp.sqrt(2) * hb) * (pix(g) + sp.I * piy(g))
a2 = lambda g: -sp.I * sp.sqrt(2) * sp.sqrt(lB2) * (dzb(g) + zz / (4 * lB2) * g)
check('a = l_B (pi_x + i pi_y)/(sqrt 2 hbar) of (4.8) is -i sqrt(2) l_B (d_zbar + z/4 l_B^2)', sp.simplify(sp.expand(a_op(f) - a2(f))) == 0, 'sympy')
gauss = sp.exp(-zz * zb / (4 * lB2))
check('the Gaussian solves (d_zbar + z/4 l_B^2) psi = 0, since d_zbar of it is -z/4 l_B^2 times it',
      sp.simplify(dzb(gauss) + zz / (4 * lB2) * gauss) == 0, 'sympy')
out = []
for g in (zz, zz ** 3, sp.exp(zz), sp.sin(zz)):
    out.append(sp.simplify(dzb(g * gauss) + zz / (4 * lB2) * g * gauss))
check('f(z) times the Gaussian solves it for f = z, z^3, exp(z), sin(z)', all(o == 0 for o in out), 'sympy')

# ---------------------------------------------------------------- the quiz with the three functions, in units hbar = e = B = m = 1
L = lambda g: sp.simplify(dzb(g) + zz / 4 * g)                       # the operator of the question, l_B = 1
Hm = lambda g: sp.simplify((pix(pix(g)) + piy(piy(g))).subs({hb: 1, e: 1, B: 1}) / 2)
Lz = lambda g: sp.simplify(-sp.I * (x * sp.diff(g, y) - y * sp.diff(g, x)))
g1 = (zz ** 2 * sp.exp(-zz * zb / 4))
g2 = (zb ** 2 * sp.exp(-zz * zb / 4))
g3 = (zz * zb * sp.exp(-zz * zb / 4))
check('z^2 exp(-|z|^2/4): the operator gives 0, the energy is hbar omega_c/2 and L_z = 2 hbar',
      L(g1) == 0 and sp.simplify(Hm(g1) - g1 / 2) == 0 and sp.simplify(Lz(g1) - 2 * g1) == 0, 'sympy')
check('zbar^2 exp(-|z|^2/4): the operator gives 2 zbar exp(-|z|^2/4), and the energy is 5/2 hbar omega_c',
      sp.simplify(L(g2) - 2 * zb * sp.exp(-zz * zb / 4)) == 0 and sp.simplify(Hm(g2) - sp.Rational(5, 2) * g2) == 0, 'sympy')
check('|z|^2 exp(-|z|^2/4): the operator gives z exp(-|z|^2/4), not zero', sp.simplify(L(g3) - zz * sp.exp(-zz * zb / 4)) == 0, 'sympy')
mm = 4
gm = zz ** mm * sp.exp(-zz * zb / 4)
check('z^m exp(-|z|^2/4) has L_z = m hbar, here m = 4', sp.simplify(Lz(gm) - mm * gm) == 0, 'sympy')

# ---------------------------------------------------------------- the radius of an orbital, the quiz on m = 8
r = np.linspace(1e-6, 12, 120001)
peaks = {m: r[np.argmax(2 * m * np.log(r) - r ** 2 / 2)] for m in (4, 8, 32)}
check('|psi_m|^2 has its maximum at sqrt(2m) l_B, 2 sqrt 2, 4 and 8 for m = 4, 8, 32',
      all(abs(peaks[m] - np.sqrt(2 * m)) < 1e-3 for m in peaks), {m: round(v, 3) for m, v in peaks.items()})
check('a ring of radius r holds r^2/2 l_B^2 flux quanta, 4 for 2 sqrt 2 l_B and 32 for 8 l_B',
      abs((2 * np.sqrt(2)) ** 2 / 2 - 4) < 1e-12 and abs(8 ** 2 / 2 - 32) < 1e-12, '4, 32')

# ---------------------------------------------------------------- the Slater determinant (4.11)
zr = np.random.default_rng(5).normal(size=6) + 1j * np.random.default_rng(6).normal(size=6)
vdm = np.linalg.det(np.vander(zr, increasing=True)) / np.prod([zr[j] - zr[i] for i in range(6) for j in range(i + 1, 6)])
check('det(z_i^(j-1)) = prod_(i<j) (z_j - z_i) at 6 random points', abs(vdm - 1) < 1e-12, '%.1e' % abs(vdm - 1))
z1, z2, z3 = sp.symbols('z1 z2 z3')
V = (z1 - z2) * (z1 - z3) * (z2 - z3)
check('the exchange z1 <-> z2 changes the sign of prod_(i<j) (z_i - z_j)', sp.expand(V.subs({z1: z2, z2: z1}, simultaneous=True) + V) == 0, 'sympy')

# ---------------------------------------------------------------- the problem, the density of the filled level
norms = []
for m in range(6):
    rr = np.linspace(0, 40, 400001)
    num = 2 * np.pi * np.trapezoid(rr ** (2 * m + 1) * np.exp(-rr ** 2 / 2), rr)
    norms.append(num / (2 * np.pi * 2 ** m * factorial(m)))
check('the norm of z^m exp(-|z|^2/4 l_B^2) is 2 pi 2^m m! l_B^(2m+2), m = 0 to 5', np.allclose(norms, 1, atol=1e-9), np.round(norms, 10))
dens = [sum(mc.orbital_density(m, np.array([rv]))[0] for m in range(400)) * 2 * np.pi for rv in (0.0, 0.5, 2.0, 5.0, 10.0)]
check('the sum of |psi_m|^2 over all m is 1/(2 pi l_B^2) at every r', np.allclose(dens, 1, atol=1e-12), np.round(dens, 12))
perum2 = E * 1.0 / H * 1e-12
check('eB/h at 1 T is 241.8 per square micrometre', abs(perum2 - 241.8) < 0.05, round(perum2, 2))
lb = np.sqrt(HBAR / (E * 1.0))
check('2 pi l_B^2 B is the flux quantum h/e', abs(2 * np.pi * lb ** 2 * 1.0 / (H / E) - 1) < 1e-8, '%.4e Wb' % (2 * np.pi * lb ** 2))

# ---------------------------------------------------------------- the quiz on the radius of the droplet
rad = {n: np.sqrt(2 * (n - 1)) for n in (26, 52, 100, 200)}
check('sqrt(2(N-1)) is 7.1, 10.1, 14.1, 19.9 for N = 26, 52, 100, 200, while the old quiz wrote 20.0 for N = 200',
      [round(rad[n], 1) for n in (26, 52, 100, 200)] == [7.1, 10.1, 14.1, 19.9], {n: round(v, 2) for n, v in rad.items()})
check('doubling N from 26 to 52 or from 100 to 200 multiplies the radius by 1.4, and 4 times N, 104, by 2.0',
      round(rad[52] / rad[26], 1) == 1.4 and round(rad[200] / rad[100], 1) == 1.4 and round(np.sqrt(2 * 103) / rad[26], 1) == 2.0, (round(rad[52] / rad[26], 3), round(np.sqrt(2 * 103) / rad[26], 3)))

# ---------------------------------------------------------------- the caption of droplet_density and of Figure 4.5
rd = np.linspace(0, 12.5, 2501)
full = mc.filled_filling(20, rd)
flat = np.abs(full[rd < np.sqrt(40) - 2] - 1).max()
half = rd[np.argmin(np.abs(full - 0.5))]
check('the filled level of 20 electrons is 1 within 0.002 up to sqrt(2N) - 2 l_B = 4.3 l_B and drops through 1/2 at 6.27 l_B, '
      'near sqrt(2N) = 6.32, the solution of the problem',
      flat < 0.002 and abs(half - np.sqrt(40)) < 0.1 and round(half, 2) == 6.27 and round(np.sqrt(40) - 2, 1) == 4.3,
      'flat to %.4f, half at %.2f against %.2f' % (flat, half, np.sqrt(40)))
# the solution for any N: one half at u = N, the radius sqrt(2N), and flat only up to about 2 l_B inside it, since at
# 1 l_B inside the density is already 8 percent below 1. The width of the edge does not grow with N.
edge_n = {}
for n in (20, 100, 200):
    rn = np.linspace(0, np.sqrt(2 * n) + 6, 20001)
    fn = mc.filled_filling(n, rn)
    edge_n[n] = (np.abs(fn[rn < np.sqrt(2 * n) - 2] - 1).max(), rn[np.argmin(np.abs(fn - 0.5))] - np.sqrt(2 * n),
                 mc.filled_filling(n, np.array([np.sqrt(2 * n) - 1]))[0])
check('for N = 20, 100, 200 the filled level is 1 within 0.003 up to 2 l_B inside sqrt(2N), 0.92 or less at 1 l_B inside, '
      'and one half within 0.06 l_B of sqrt(2N)',
      all(v[0] < 0.003 and abs(v[1]) < 0.06 and v[2] < 0.925 for v in edge_n.values()),
      {n: tuple(np.round(v, 4)) for n, v in edge_n.items()})
# the caption of droplet_density, corrected on 2026-11-22 from "flat at nu = 1 up to the radius sqrt(2N) l_B, where it drops
# to zero" to "flat up to about 2 l_B inside the radius, and around this radius it drops to zero": for N = 20 it is 1 within
# 0.002 at 2 l_B inside, 0.92 at 1 l_B inside, 0.47 at the radius and below 0.01 at 2 l_B outside, by the sum of the
# orbitals of _g4_laughlin_mc and by the regularized incomplete gamma function Q(N, r^2/2)
from scipy.special import gammaincc  # noqa: E402
rr = np.sqrt(40) + np.array([-2.0, -1.0, 0.0, 2.0])
by_sum, by_gamma = mc.filled_filling(20, rr), gammaincc(20, rr ** 2 / 2)
check('caption: the filled level of 20 electrons is 0.998, 0.92, 0.47 and below 0.01 at 2 and 1 l_B inside, at, and 2 l_B '
      'outside sqrt(2N) l_B, by two routes',
      np.allclose(by_sum, by_gamma, atol=1e-6) and by_sum[0] > 0.998 and round(by_sum[1], 2) == 0.92
      and round(by_sum[2], 2) == 0.47 and by_sum[3] < 0.01, np.round(by_sum, 4))
fill, bump, edge = [], [], []
for s in (1, 2, 3, 4):
    rc, nu, _ = mc.metropolis(20, 3, [], s)
    fill.append(nu[rc < 5].mean()); bump.append(3 * nu.max() - 1)
    edge.append(rc[(rc > 8) & (nu < 1 / 6)][0])
check('the Laughlin state of 20 electrons, four runs, is 1/3 within 0.01 for r < 5 l_B and rises 25 to 35 percent above 1/3 at the edge',
      all(abs(v - 1 / 3) < 0.01 for v in fill) and all(0.25 < b < 0.35 for b in bump),
      'filling %s, bump %s percent' % (np.round(fill, 3), np.round(100 * np.array(bump), 1)))
ratio = np.mean(edge) / half
check('its edge, where it drops to half of 1/3, is about sqrt 3 times further out than the edge of the filled level, three times the area',
      abs(ratio - np.sqrt(3)) < 0.1, 'edge at %s l_B, ratio %.2f against %.2f' % (np.round(edge, 2), ratio, np.sqrt(3)))
check('Figure 4.5: the orbitals up to 3(N-1) against N-1 give the radius sqrt(3) times larger and a third of the density',
      abs(np.sqrt(2 * 3 * 19) / np.sqrt(2 * 19) - np.sqrt(3)) < 1e-12, 'sqrt 3')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'figures'))
import physcheck as pcl  # noqa: E402

# ---------------------------------------------------------------- Section 4.14, |C_tot| = N, decided on 2026-11-22 by the lecturer
# Section 4.14 says that the filling nu = N equals |C_tot| = N of (4.2), so |sigma_xy| = nu e^2/h.
# A magnetic cell of the square lattice with the phase (4.4) of the charge +e, A = (0, s B x) and the flux 1/10: the
# hop from (x, y) to (x, y+1) is -exp(i s 2 pi x/10), s = +1 for the field along +z, and s = -1 is an electron there.
def landau_cell_q10(s, q=10):
    def hk_(k):
        m = np.diag(-2 * np.cos(k[1] - s * 2 * np.pi * np.arange(q) / q)).astype(complex)
        m += -np.eye(q, k=1) - np.eye(q, k=-1)
        m[q - 1, 0] += -np.exp(1j * k[0] * q)
        m[0, q - 1] += -np.exp(-1j * k[0] * q)
        return m
    return hk_, pcl.reciprocal([[q, 0], [0, 1]])


Cq10 = {s: [pcl.chern_links(*landau_cell_q10(s), bands=n, nk=10) for n in range(3)] for s in (1, -1)}
check('decided on 2026-11-22: each of the three lowest levels has |C| = 1 and N filled levels have |C_tot| = N, for both charges, C = -1 per level for the charge +e in B z and +1 for an electron, so |sigma_xy| = nu e^2/h at nu = N', all(np.allclose(np.abs(Cq10[s]), 1, atol=1e-9)
      and np.allclose(np.abs(np.cumsum(Cq10[s])), [1, 2, 3], atol=1e-9) for s in Cq10)
      and np.allclose(Cq10[1], -1, atol=1e-9) and np.allclose(Cq10[-1], 1, atol=1e-9), {s: np.round(Cq10[s], 6) for s in Cq10})

print('all checks of page 13 hold')
