"""Session 9, the numbers and the algebra that page 06b (Section 9.6b, Friedel oscillations in a chain and the contrast
with an insulator) quotes, checked by a second route. One check script per page is the rule: every number of a
caption, a feedback, a fold or a solution is an assert, here or in the figure script that draws it. The figure script
friedel.py asserts its own numbers (k_F = 0.64 and 1.05, the periods 4.9 and 3.0 sites, also from the zero crossings,
and the power 1.00 of the envelope beyond 10 sites).

This script checks the key box and the fold on chains with a gap, by exact diagonalization: the chain with the onsite
energies +m and -m and the hopping t, at half filling with the Fermi level in the middle of the gap 2m, and the
dimerized chain with the hoppings t and 0.6 t. The density change around one impurity decays as e^{-x/xi}, with
1/xi = 2 asinh(m/2t) close to m/t = E_g/(hbar v_F), up to a slower factor in front. It also checks the transform of
1/(q^2 + kappa^2), the numbers of the quizzes and the problem. The density, and not the LDOS at one energy, is what
the new blocks of the page state. The sentences of the old text on the LDOS were corrected on 2026-11-22, and their
checks are at the end of this script. It finds the repository from its own path and writes no file.
"""
import numpy as np
from scipy.integrate import quad
from scipy.linalg import eigh_tridiagonal


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


N = 2001
c = N // 2


def density(onsite, hop, v0, mu=0.0):
    """The density of the open chain with the onsite energies onsite, the hoppings -hop and the impurity v0 on the
    middle site, with the states below mu filled."""
    d = np.array(onsite, float).copy()
    d[c] += v0
    e, w = eigh_tridiagonal(d, -np.asarray(hop, float))
    return (np.abs(w[:, e < mu]) ** 2).sum(axis=1)


def response(onsite, hop, v0):
    return density(onsite, hop, v0) - density(onsite, hop, 0.0)


# --------------------------------------------------------------------------- the chain with onsite energies +m and -m
m = 0.3
stag = np.array([m if i % 2 == 0 else -m for i in range(N)])
ones = np.ones(N - 1)
xi = 1 / (2 * np.arcsinh(m / 2))
check('key and fold: 1/xi = 2 asinh(m/2t) is close to m/t = E_g/(hbar v_F), E_g = 2m and v_F = 2t, at m = 0.3t',
      abs(xi - 1 / m) / xi < 0.01, (round(xi, 3), round(1 / m, 3)))
# the fold: v_F = 2ta/hbar is the group velocity of the band -2t cos k at k_F = pi/2, the half-filled chain without the
# gap, so E_g/(hbar v_F) = 2m/2t = m/t
kk = np.linspace(0, np.pi, 200001)
vg = np.gradient(-2 * np.cos(kk), kk)
check('fold: v_F = 2t (a = hbar = 1) at k_F = pi/2 of the chain without the gap, and E_g/v_F = 2m/2t = m/t',
      abs(vg[100000] - 2) < 1e-8 and abs(2 * m / vg[100000] - m) < 1e-8, round(vg[100000], 8))
check('key and fold: xi = 3.3 sites for the gap 0.6t, and xi grows as the gap closes, 10.0 sites for m = 0.1t',
      round(xi, 1) == 3.3 and round(1 / (2 * np.arcsinh(0.05)), 1) == 10.0, (xi, 1 / (2 * np.arcsinh(0.05))))
ratios = {}
for v0 in (0.1, 1.0):
    y = response(stag, ones, v0)[c:c + 61]
    ev = np.arange(10, 41, 2)
    slope = -np.polyfit(ev, np.log(np.abs(y[ev])), 1)[0]
    ratios[v0] = abs(y[10] / y[20])
    print(f'   v0 = {v0}: |dn| at 10, 20, 30, 40 = {np.abs(y[[10, 20, 30, 40]])}, fitted 1/xi = {slope:.3f}')
    check(f'key and fold: the density change at v0 = {v0}t decays at the rate 1/xi = {1 / xi:.3f}, a fit from 10 to 40 sites',
          abs(slope * xi - 1) < 0.06, round(slope, 4))
    check(f'key: no slow tail, |dn| falls by more than 15 from x = 10 to 20 at v0 = {v0}t', ratios[v0] > 15, round(ratios[v0], 2))
# the fold and quiz 2: an impurity 0.1t on a site with +m or with -m, from x = 10 to 20 and from 11 to 21, on both sides
fac = []
for sgn in (1, -1):
    y = response(sgn * stag, ones, 0.1)
    fac += [abs(y[c + s * x] / y[c + s * (x + 10)]) for x in (10, 11) for s in (1, -1)]
check('fold: the factor from x = 10 to 20 and from 11 to 21 is between 21 and 29, on either sublattice, at v0 = 0.1t',
      21 <= min(fac) and max(fac) <= 29.5, (round(min(fac), 2), round(max(fac), 2)))
check('fold: a little more than e^{10/xi} = 20, from the slower factor in front', min(fac) > np.exp(10 / xi), min(fac))
check('quiz 2: more than a factor 20 from x = 10 to x = 20 for an impurity 0.1t, with the gap 0.6t', min(fac) > 20, min(fac))
# a second route to 1/xi = 2 asinh(m/2t): the Green's function of the clean chain at E = 0, the middle of the gap,
# decays per site as asinh(m/2t), and the density change is built from two of them
H = np.diag(stag) - np.diag(ones, 1) - np.diag(ones, -1)
G = np.linalg.inv(-H)
gr = -np.diff(np.log(np.abs(G[c, c + 10:c + 51:2]))) / 2
check('fold: G(x, E = 0) of the clean chain decays per site as asinh(m/2t)', np.abs(gr - np.arcsinh(m / 2)).max() < 1e-6,
      round(gr.mean(), 6))
# and the local rate of the density change from 40 to 60 sites, with the factor x^-1/2 of the integral over the
# imaginary frequency taken out, is 2 asinh(m/2t) within 2 percent, for both sublattices and v0 = 0.1t and t
for sgn in (1, -1):
    for v0 in (0.1, 1.0):
        y = response(sgn * stag, ones, v0)
        ev = np.arange(40, 61, 2)
        rate = -np.polyfit(ev, np.log(np.abs(y[c + ev]) * np.sqrt(ev)), 1)[0]
        check(f'fold: the density change decays at the rate 2 asinh(m/2t) = {1 / xi:.4f}, impurity on {sgn * m:+.1f}, '
              f'v0 = {v0}t, from 40 to 60 sites', abs(rate * xi - 1) < 0.02, round(rate, 4))
check('quiz 2: e^{10/xi} = 20 for xi = 3.35 sites', round(np.exp(10 / xi)) == 20, np.exp(10 / xi))
check('quiz 2: 1/x gives 2 and 1/x^2 gives 4 from x = 10 to x = 20', (20 / 10) == 2 and (20 / 10) ** 2 == 4, (2, 4))
# the gap of this chain is 2m: the levels closest to zero of the clean ring of 400 sites are at +-m
k = 2 * np.pi * np.arange(200) / 200
band = np.sqrt(m ** 2 + (2 * np.cos(k / 2)) ** 2)
check('quiz 2: the chain with onsite energies +-0.3t has the gap 0.6t', abs(2 * band.min() - 0.6) < 1e-3, 2 * band.min())

# --------------------------------------------------------------------------- the dimerized chain of quiz 1
hop = np.array([1.0 if i % 2 == 0 else 0.6 for i in range(N - 1)])
zero = np.zeros(N)
y = response(zero, hop, 0.1)
fall = min(min(abs(y[c + x] / y[c + x + 10]), abs(y[c - x] / y[c - x - 10])) for x in range(10, 31))
check('quiz 1: in the dimerized chain t, 0.6t, v0 = 0.1t, beyond ten sites the density change falls by more than 100 every ten sites',
      fall > 100, round(fall, 1))
check('quiz 1: the dimerized chain t, 0.6t has the gap 2|t1 - t2| = 0.8t', abs(2 * abs(1 - 0.6) - 0.8) < 1e-12, 0.8)
check('quiz 1: e^{-4} = 0.02, the response at ten sites for xi = 2.5', round(np.exp(-10 / 2.5), 2) == 0.02, np.exp(-4))

# ------------------------------------------------------------------------------------ the fold, the simplest case
for kappa in (0.4, 1.3):
    for x in (0.0, 2.0, 7.5):
        val = quad(lambda q: 1 / (q ** 2 + kappa ** 2), 0, np.inf, weight='cos', wvar=x)[0] / np.pi if x > 0 else \
            quad(lambda q: 1 / (q ** 2 + kappa ** 2), -np.inf, np.inf)[0] / (2 * np.pi)
        check(f'fold: int dq/2pi e^(iqx)/(q^2 + kappa^2) = e^(-kappa|x|)/(2 kappa), kappa = {kappa}, x = {x}',
              abs(val - np.exp(-kappa * x) / (2 * kappa)) < 1e-8, round(val, 8))
# the residue at q = i kappa of e^{iqx}/(q^2 + kappa^2) is e^{-kappa x}/(2 i kappa), and 2 pi i / 2 pi times it is the result
kappa, x = 0.7, 3.0
res = np.exp(1j * (1j * kappa) * x) / (2j * kappa)
check('fold: 2 pi i times the residue at i kappa, over 2 pi, is e^(-kappa x)/(2 kappa)', abs(1j * res - np.exp(-kappa * x) / (2 * kappa)) < 1e-14,
      (1j * res).real)

# ----------------------------------------------------------------------------------------------- the problem
x_gap = 1 + 2.5 * np.log(100)
check('problem: e^{-(x-1)/xi} = 0.01 at x = 1 + xi ln 100 = 12.5 sites for xi = 2.5', round(x_gap, 1) == 12.5, x_gap)
check('problem: ln 100 = 4.61', round(np.log(100), 2) == 4.61, np.log(100))
check('problem: xi ln 100 = 11.5 sites beyond x = 1', round(2.5 * np.log(100), 1) == 11.5, 2.5 * np.log(100))
check('problem: 1/x = 0.01 at x = 100', abs(1 / 100 - 0.01) < 1e-15, 100)
check('problem: at x = 15 the exponential is at 0.4 percent of its value at x = 1, and 1/x at 7 percent',
      round(100 * np.exp(-14 / 2.5), 1) == 0.4 and round(100 / 15) == 7, (np.exp(-14 / 2.5), 1 / 15))
check('problem: at x = 30 the two laws differ by orders of magnitude, 1/x over e^{-(x-1)/xi} above 1000',
      (1 / 30) / np.exp(-29 / 2.5) > 1000, (1 / 30) / np.exp(-29 / 2.5))
# ---- the second paragraph and the notebook box. In a gapped chain the LDOS change at the middle of the gap decays
# exponentially. The cell "Impurity in an electronic insulator" of session9.ipynb, its own pyqula call, run in a temporary
# folder for the gaps 0.2 and 0.6, gives the decay lengths 10 and 3.3 sites of the box, which the closed form
# 1/(2 asinh(m/2t)) gives too. In a metallic chain the LDOS at one energy keeps oscillating with pi/k_F far from the
# impurity, with no power law: at the Fermi level of mu = -t and with an impurity t, the closed form of the T-matrix has
# the same amplitude at x = 10, 40 and 160, and the sum over momenta with a broadening 0.001t only the damping
# e^{-2 delta x/v_F} of the broadening.
import json, os, tempfile
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
nb = json.load(open(os.path.join(REPO, 'jupyter-notebooks', 'session9.ipynb'), encoding='utf-8'))
cell = ''.join(next(c['source'] for c in nb['cells'] if c['cell_type'] == 'code' and 'gaps = [0.1,0.3]' in ''.join(c['source'])))
check('notebook box: the cell has gaps = [0.1,0.3] in add_sublattice_imbalance, W = 0.2 and the LDOS at energy 0',
      'h.add_sublattice_imbalance(gap)' in cell and 'W = 0.2' in cell and 'energy=0.,delta=1e-2,nk=400' in cell, 'read from the cell')
cwd = os.getcwd()
lengths = []
with tempfile.TemporaryDirectory() as d:
    os.chdir(d)
    try:
        from pyqula import geometry, embedding
        for gap in (0.1, 0.3):
            g = geometry.bichain()
            h = g.get_hamiltonian(has_spin=False, tij=[1])
            h.add_sublattice_imbalance(gap)
            hv = h.copy(); hv.add_onsite(lambda r: (np.sum((r - g.r[0]) ** 2) < 1e-2) * 0.2)
            x_, y_, d1 = embedding.Embedding(h, m=hv).get_ldos(nsuper=51, energy=0., delta=1e-2, nk=400)
            x0_, y0_, d0 = embedding.Embedding(h, m=h.copy()).get_ldos(nsuper=51, energy=0., delta=1e-2, nk=400)
            x_ = np.array(x_); r_ = np.abs(x_ - g.r[0][0]); dd = np.abs(np.array(d1) - np.array(d0))
            sel = (r_ >= 4) & (r_ <= 40)
            lengths.append(-1 / np.polyfit(r_[sel], np.log(dd[sel]), 1)[0])
    finally:
        os.chdir(cwd)
closed = [1 / (2 * np.arcsinh(m_ / 2)) for m_ in (0.1, 0.3)]
check('notebook box: the change of the LDOS decays over about 10 sites for the gap 0.2 and 3.3 sites for 0.6, by the cell and '
      'by 1/(2 asinh(m/2t))', round(lengths[0]) == 10 and round(lengths[1], 1) == 3.3 and round(closed[0]) == 10
      and round(closed[1], 1) == 3.3 and all(abs(a / b - 1) < 0.01 for a, b in zip(lengths, closed)),
      (np.round(lengths, 3).tolist(), np.round(closed, 3).tolist()))
kF_ = np.arccos(0.5)
vF_ = 2 * np.sin(kF_)
xs_ = np.array([10, 40, 160])
amp = lambda gx, T_: np.abs(gx ** 2 * T_) / np.pi
g0_cf = -1j / (2 * np.sin(kF_))
amps_cf = amp(g0_cf * np.exp(1j * kF_ * xs_), 1.0 / (1 - g0_cf))
kq_ = 2 * np.pi * (np.arange(400000) + 0.5) / 400000
gk = lambda x_: np.mean(np.exp(1j * kq_ * x_) / (-1.0 + 0.001j + 2 * np.cos(kq_)))
amps_ks = amp(np.array([gk(x_) for x_ in xs_]), 1.0 / (1 - gk(0)))
damp = np.exp(-2 * 0.001 * (xs_ - xs_[0]) / vF_)
check('paragraph 2: in a metallic chain the LDOS change at the Fermi energy keeps its amplitude far from the impurity, by the '
      'closed form, and by the sum over momenta up to the damping of the broadening', np.ptp(amps_cf) < 1e-12
      and np.allclose(amps_ks / amps_ks[0], damp, rtol=0.03), (np.round(amps_cf, 5).tolist(), np.round(amps_ks / amps_ks[0], 4).tolist(), np.round(damp, 4).tolist()))
sg_ = np.sign(-np.imag(np.array([gk(x_) for x_ in range(20, 61)]) ** 2 * (1.0 / (1 - gk(0)))))
zc_ = np.where(sg_[1:] != sg_[:-1])[0]
check('paragraph 2: the LDOS change of the metal at the Fermi energy oscillates with the period pi/k_F = 3 sites for mu = -t',
      abs(2 * np.diff(zc_).mean() - np.pi / kF_) < 0.1, (round(2 * np.diff(zc_).mean(), 3), round(np.pi / kF_, 3)))
# paragraph 2, the gapped chain: the change decays exponentially at the energies inside the gap, such as E = 0 of the cell.
# The T-matrix of the infinite chain with the onsite energies +-m, m = 0.1t, the hopping t, the impurity 0.2t of the cell on
# an A site and the broadening 0.001t, by a sum over 400000 cells. At E = 0 the change falls at the rate 2 asinh(m/2t) per
# site. At E = 0.5t, inside the band of the same chain, its envelope falls only by the factor e^{-2 delta n/v} of the
# broadening, with n the number of cells and v the group velocity in cells, so it keeps oscillating as in a metal.
mg, Vg, dg = 0.1, 0.2, 1e-3
kc = 2 * np.pi * (np.arange(400000) + 0.5) / 400000
habk = -(1 + np.exp(-1j * kc))


def gAA(E, n):
    z = E + 1j * dg
    return np.mean(np.exp(1j * kc * n) * (z + mg) / ((z - mg) * (z + mg) - np.abs(habk) ** 2))


def drho(E, ns):
    Tg = Vg / (1 - Vg * gAA(E, 0))
    return np.array([-np.imag(gAA(E, n) ** 2 * Tg) / np.pi for n in ns])


in_gap = np.abs(drho(0.0, [10, 100]))
rate = np.log(in_gap[0] / in_gap[1]) / (2 * 90)
check('paragraph 2: E = 0 is inside the gap of the cell, and there the LDOS change falls from 20 to 200 sites at the rate '
      '2 asinh(m/2t) per site', abs(0.0) < mg and abs(rate / (2 * np.arcsinh(mg / 2)) - 1) < 0.02,
      ('%.2e %.2e' % tuple(in_gap), round(rate, 4), round(2 * np.arcsinh(mg / 2), 4)))
env = [np.abs(drho(0.5, range(c - 5, c + 6))).max() for c in (200, 400)]
kE = 2 * np.arccos(np.sqrt((0.5 ** 2 - mg ** 2) / 4))                    # E^2 = m^2 + 4 cos^2(k/2) in the band
vE = np.sin(kE) / 0.5                                                    # |dE/dk| = sin k / E, in cells
check('paragraph 2: at E = 0.5t, inside the band of the gapped chain, the envelope from 400 to 800 sites falls only by the '
      'factor of the broadening', np.sqrt((0.5 ** 2 - mg ** 2)) > mg and abs(env[1] / env[0] / np.exp(-2 * dg * 200 / vE) - 1) < 0.03,
      (np.round(env, 4).tolist(), round(env[1] / env[0], 4), round(np.exp(-2 * dg * 200 / vE), 4)))

# ---- the caption of friedel: the numbers are those of a spinless chain, one state per site, as friedel.py computes
src = open(os.path.join(REPO, 'webnotes', 'figures', 'session09', 'friedel.py'), encoding='utf-8').read()
check('caption of friedel: the script diagonalizes one tridiagonal matrix of N = 4001 sites, a spinless chain',
      'N, v0, HOP, MUS = 4001, 1.0, -1.0, (-1.6, -1.0)' in src and 'eigh_tridiagonal(d, HOP * np.ones(N - 1))' in src, 'read from the script')
print('all checks of page 06b hold')
