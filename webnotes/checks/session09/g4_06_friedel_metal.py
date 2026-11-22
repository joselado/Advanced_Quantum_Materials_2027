"""Session 9, the numbers and the algebra that page 06 (Section 9.6a, Friedel oscillations in a metal) quotes, checked
by a second route. One check script per page is the rule: every number of a caption, a feedback, a fold or a solution
is an assert, here or in the figure script that draws it. The figure scripts assert their own numbers. These are
_g4_ripples.check, which friedel2d.py and the three pictures of the quiz call (the band -2 (cos kx + cos ky) of the
pyqula Hamiltonian, k_F = 0.45, 0.80 and 1.05, the periods 6.97, 3.95 and 3.00 sites, the wavevector of the ripples
fitted on the maps within 5 percent of 2 k_F), and period.py (the pattern 1, 0, -1, 0 and its period of 4 sites).

This script checks the recall of (9.4), the fold from the closed form of chi_0 to the 1/x tail with its prefactor,
the envelopes 1/|x|^2 and 1/|x|^3 of the free-electron gas, the condition of the key box (a Fermi surface with no flat
parts) on the square lattice at mu = -t and at half filling, the quizzes, the picture quiz by the shape of the three
Fermi contours, the problem by exact diagonalization, the clean reference and the unit of the pyqula script, the 1/r
decay and the damping length of the LDOS of the caption of friedel2d, the numbers of the widget, and the reading of
the lab box. The fold is written about the Fourier transform
F(x) of chi_0 and says only that the density is proportional to v0 F(x). The text before the key box writes the minus
sign of delta n(x) since 2026-11-22, which is checked at the end of this script. It finds the repository from its own path and writes no file,
since the pyqula call runs in the temporary folder of style.run_script, and only nsuper = 2 and 5 are computed here.
"""
import os
import sys

import numpy as np
from scipy.integrate import quad
from scipy.linalg import eigh_tridiagonal
from scipy.special import sici

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, '..', '..', 'figures')
sys.path.insert(0, FIG)


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# ---------------------------------------------------------------------------------------------- the recall of (9.4)
# chi_0(q) of (9.4) on a chain with the band -2 cos k, at mu = -t and T = 0.05 t, is positive at every q, and its
# limit q -> 0 is the density of states D(E_F) averaged over -n_F', as Section 9.4a says
def chi0_chain(q, mu, T, nk=4000):
    k = 2 * np.pi * np.arange(nk) / nk
    e1, e2 = -2 * np.cos(k), -2 * np.cos(k + q)
    f = lambda e: 0.5 * (1 - np.tanh((e - mu) / (2 * T)))
    with np.errstate(invalid='ignore', divide='ignore'):
        r = (f(e1) - f(e2)) / (e2 - e1)
    deg = np.abs(e2 - e1) < 1e-10
    r[deg] = (f(e1[deg]) * (1 - f(e1[deg])) / T)
    return r.mean()


qs = np.linspace(0.01, np.pi, 40)
vals = [chi0_chain(q, -1.0, 0.05) for q in qs]
k = 2 * np.pi * np.arange(4000) / 4000
ek = -2 * np.cos(k)
dos = (0.5 / 0.05 / np.cosh((ek + 1.0) / 0.1) ** 2 / 2).mean()     # -n_F' = 1/(4T cosh^2((e-mu)/2T))
check('recall: chi_0(q) of (9.4) is positive on a chain at mu = -t, T = 0.05 t', min(vals) > 0, round(min(vals), 4))
check('recall: chi_0(q -> 0) is the density of states averaged over -n_F\'', abs(chi0_chain(1e-4, -1.0, 0.05) - dos) < 1e-3,
      (round(chi0_chain(1e-4, -1.0, 0.05), 4), round(dos, 4)))

# ------------------------------------------------------------------------- the fold, in units m = hbar = 1, k_F = 1
# chi_0(q) = (m / pi hbar^2 q) ln|(2 k_F + q)/(2 k_F - q)|, and F(x) = int dq/2pi e^{iqx} chi_0(q)
kF = 1.0
a = 2 * kF
chi0 = lambda q: np.log(abs((a + q) / (a - q))) / (np.pi * q)


def F_direct(x):
    """(1/pi) int_0^inf cos(qx) chi_0(q) dq, split at the logarithm at q = 2 k_F."""
    if x == 0:
        return (quad(chi0, 0, a, limit=400)[0] + quad(chi0, a, 2 * a, limit=400)[0] + quad(chi0, 2 * a, np.inf)[0]) / np.pi
    I = quad(lambda q: chi0(q) * np.cos(q * x), 0, a, limit=800)[0]
    I += quad(lambda q: chi0(q) * np.cos(q * x), a, 2 * a, limit=800)[0]
    I += quad(chi0, 2 * a, np.inf, weight='cos', wvar=x, limit=800)[0]
    return I / np.pi


F_closed = lambda x: (np.pi / 2 - sici(a * abs(x))[0]) / np.pi          # (m / pi hbar^2) [pi/2 - Si(2 k_F |x|)]
errs = [abs(F_direct(x) - F_closed(x)) for x in (0.0, 0.7, 3.0, 10.0, 25.0)]
check('fold: F(x) = (m/pi hbar^2) [pi/2 - Si(2 k_F |x|)], against the direct integral at five x', max(errs) < 1e-7,
      max(errs))
check('fold: F(0) = m/(2 hbar^2), the value on the impurity', abs(F_direct(0.0) - 0.5) < 1e-9, F_direct(0.0))
# the tail: pi/2 - Si(z) = cos z/z + O(1/z^2), so F(x) - (m/pi hbar^2) cos(2 k_F x)/(2 k_F x) falls as 1/x^2
xs = np.linspace(20, 200, 400)
tail = np.cos(a * xs) / (a * xs) / np.pi
rem = np.abs(np.array([F_closed(x) for x in xs]) - tail) * xs ** 2
check('fold: the tail of F(x) is (m/pi hbar^2) cos(2 k_F x)/(2 k_F x), with a remainder of order 1/x^2',
      rem.max() < 0.1, round(rem.max(), 4))
# near q = 2 k_F, chi_0 = -(m / 2 pi hbar^2 k_F) ln|q - 2 k_F| + smooth, so (q - 2 k_F) chi_0'(q) -> -m/(2 pi hbar^2 k_F)
for eps in (1e-4, -1e-4):
    q, h = a + eps, 1e-8
    slope = (chi0(q + h) - chi0(q - h)) / (2 * h)
    check(f'fold: the pole of chi_0\' at 2 k_F, (q - 2k_F) chi_0\'(q) at q - 2k_F = {eps}',
          abs(eps * slope + 1 / (2 * np.pi * kF)) < 1e-3, round(eps * slope, 5))
# the principal value int sin(qx)/(q - q0) dq = pi cos(q0 x) for x > 0, by the weight 'cauchy' of quad
for x in (1.3, 4.0):
    q0, L = a, 400.0
    pv = quad(lambda q: np.sin(q * x), q0 - L, q0 + L, weight='cauchy', wvar=q0, limit=4000)[0]
    tails = 2 * np.cos(q0 * x) * (np.pi / 2 - sici(L * x)[0])
    check(f'fold: PV int sin(qx)/(q - 2k_F) dq = pi cos(2 k_F x) at x = {x}', abs(pv + tails - np.pi * np.cos(q0 * x)) < 1e-6,
          round(pv + tails, 6))
# the integration by parts: (1/pi) int cos(qx) chi_0 dq = -(1/(pi x)) int sin(qx) chi_0'(q) dq, here at x = 3
x = 3.0
dchi = lambda q: (chi0(q + 1e-6) - chi0(q - 1e-6)) / 2e-6
inner = quad(lambda q: np.sin(q * x) * dchi(q) * (q - a), 1e-5, 3 * a, weight='cauchy', wvar=a, limit=2000)[0]
inner += quad(lambda q: np.sin(q * x) * dchi(q), 3 * a, 60, limit=4000)[0] + quad(dchi, 60, np.inf, weight='sin', wvar=x)[0]
check('fold: one integration by parts, -(1/(pi x)) PV int sin(qx) chi_0\'(q) dq = F(x) at x = 3',
      abs(-inner / (np.pi * x) - F_closed(x)) < 1e-4, (round(-inner / (np.pi * x), 6), round(F_closed(x), 6)))
# in d = 2 and d = 3 the envelopes 1/|x|^2 and 1/|x|^3, for the free-electron gas, where chi_0 is non-analytic on the
# circle or sphere |q| = 2 k_F. The density is Im int_0^kF dk k^(d-1) G(r, E_k)^2 up to a constant, with
# G ~ H_0^(1)(kr) in d = 2 and G ~ e^{ikr}/r in d = 3. In d = 2 the Lommel integral gives k_F^2 (J0 Y0 + J1 Y1)(k_F r),
# in d = 3 the integral gives (sin 2k_F r - 2k_F r cos 2k_F r)/(4 r^4). Both closed forms are checked against the
# integral by quad, and then the power of their envelope is fitted, as on the conventions sheet (1.98 and 2.97).
from scipy.special import hankel1, j0, j1, y0, y1


def power(y, r, q, damp=None, ps=np.arange(0.0, 4.005, 0.01)):
    """The power p of the best fit of y(r) by r^-p (A cos qr + B sin qr), times damp(r) when it is given."""
    best = (None, np.inf)
    for p in ps:
        A = np.stack([np.cos(q * r), np.sin(q * r)], 1) * (r ** (-p) * (1 if damp is None else damp))[:, None]
        cc = np.linalg.lstsq(A, y, rcond=None)[0]
        err = np.sum((A @ cc - y) ** 2) / np.sum(y ** 2)
        if err < best[1]:
            best = (round(float(p), 2), err)
    return best[0]


kc = 1.0
d2 = lambda r: kc ** 2 * (j0(kc * r) * y0(kc * r) + j1(kc * r) * y1(kc * r))
d3 = lambda r: (np.sin(2 * kc * r) - 2 * kc * r * np.cos(2 * kc * r)) / (4 * r ** 4)
e2 = max(abs(quad(lambda k: k * np.imag(hankel1(0, k * r) ** 2), 0, kc, limit=400)[0] - d2(r)) for r in (2.0, 7.0, 15.0))
e3 = max(abs(quad(lambda k: k * np.sin(2 * k * r), 0, kc)[0] / r ** 2 - d3(r)) for r in (2.0, 7.0, 15.0))
check('fold: the closed forms of the density in d = 2 (Lommel) and d = 3 against the integral over the Fermi sea',
      e2 < 1e-8 and e3 < 1e-12, (e2, e3))
rr = np.arange(5, 31).astype(float)
p2, p3 = power(d2(rr), rr, 2 * kc), power(d3(rr), rr, 2 * kc)
check('fold: the envelopes 1/|x|^2 and 1/|x|^3 of the free-electron gas in d = 2 and d = 3, fitted from r = 5 to 30',
      abs(p2 - 2) < 0.03 and abs(p3 - 3) < 0.05, (p2, p3))

# the square lattice, the condition of the key box and of the fold. chi_0(r) of (9.4) in real space is
# -T sum_n G(r, i w_n)^2, from an FFT on an L x L mesh at the temperature T, and the density change is -v0 chi_0(r).
# At mu = -t the Fermi surface has no flat parts, and the envelope is 1/r^2 along the axis and along the diagonal,
# with the thermal factor (r/L_T)/sinh(r/L_T) divided out. At half filling the Fermi surface is the flat, nested
# square, and on the diagonal r^2 |chi_0| grows from x = 4 to 16, so the envelope falls more slowly than 1/r^2.
# The temperature only makes the decay faster, since r^2 |chi_0| grows more at the lower T.
def chi_square(mu, T, L=512, wmax=20.0):
    k = 2 * np.pi * np.arange(L) / L
    e = -2 * (np.cos(k)[:, None] + np.cos(k)[None, :]) - mu
    out, n = np.zeros((L, L)), 0
    while (2 * n + 1) * np.pi * T < wmax:
        out += -2 * T * np.real(np.fft.ifft2(1 / (1j * (2 * n + 1) * np.pi * T - e)) ** 2)
        n += 1
    return out


T = 0.02
xs_ = np.arange(6, 40).astype(float)
cm = chi_square(-1.0, T)
kx = np.arccos(-1.0 / 2)                       # -2 cos kx - 2 = -1 on the axis
kd = np.arccos(1.0 / 4)                        # -4 cos kd = -1 at k = (kd, kd) on the diagonal
LT, LTd = 2 * np.sin(kx) / (2 * np.pi * T), 2 * np.sqrt(2) * np.sin(kd) / (2 * np.pi * T)
pa = power(np.array([cm[int(x), 0] for x in xs_]), xs_, 2 * kx, (xs_ / LT) / np.sinh(xs_ / LT))
rd = np.sqrt(2) * xs_
pd = power(np.array([cm[int(x), int(x)] for x in xs_]), xs_, 4 * kd, (rd / LTd) / np.sinh(rd / LTd))
check('key and fold: the square lattice at mu = -t has the envelope 1/r^2 along the axis and along the diagonal',
      abs(pa - 2) < 0.05 and abs(pd - 2) < 0.05, (pa, pd))
grow = []
for Tn in (0.04, 0.02):
    ch = chi_square(0.0, Tn)
    grow.append((2 * 16 ** 2 * abs(ch[16, 16])) / (2 * 4 ** 2 * abs(ch[4, 4])))
check('fold: at half filling r^2 |chi_0| on the diagonal grows from x = 4 to 16, more at the lower T, so the envelope is '
      'slower than 1/r^2', 1.5 < grow[1] and grow[0] < grow[1], [round(g_, 3) for g_ in grow])

# ----------------------------------------------------------------------------------------------- the quizzes
check('quiz 1: k_F = pi/4 gives the period pi/k_F = 4 of cos(2 k_F x)', abs(np.pi / (np.pi / 4) - 4) < 1e-12, 4)
check('quiz 1: the Fermi wavelength 2 pi/k_F = 8', abs(2 * np.pi / (np.pi / 4) - 8) < 1e-12, 8)
check('quiz 1: a period 2 means 2 k_F = pi, k_F = pi/2, half filling of the spinless chain', abs(np.pi / (np.pi / 2) - 2) < 1e-12, 2)
for d, f in ((1, 2), (2, 4), (3, 8)):
    check(f'quiz 2: doubling x divides 1/|x|^{d} by {f}', 2 ** d == f, 2 ** d)
# the picture quiz: the Fermi contour at E of -2 (cos kx + cos ky) is a circle, k_F along the axis and along the
# diagonal differ by less than 3 percent, and the largest circle has the shortest period pi/k_F
rows = []
for E in (-3.8, -3.4, -3.0):
    k_ax = np.arccos(-E / 2 - 1)
    k_dg = np.sqrt(2) * np.arccos(-E / 4)
    rows.append((E, k_ax, k_dg, np.pi / k_ax))
    check(f'picture quiz: at E = {E} the contour is a circle, k_F = {k_ax:.3f} on the axis and {k_dg:.3f} on the diagonal',
          abs(k_dg / k_ax - 1) < 0.03, round(k_dg / k_ax, 4))
check('picture quiz: k_F = 0.45, 0.80 and 1.05, periods 7.0, 3.95 and 3.0 sites',
      [round(r[1], 2) for r in rows] == [0.45, 0.80, 1.05] and [round(r[3], 2) for r in rows] == [6.97, 3.95, 3.0],
      [(round(r[1], 3), round(r[3], 2)) for r in rows])
check('picture quiz: k_F = pi/3 at E = -3t', abs(rows[2][1] - np.pi / 3) < 1e-12, rows[2][1])

# ----------------------------------------------------------------------------------------------- the problem
# a spinless chain with 0.2 electrons per site: k_F = 0.2 pi, period 5, factors 4 and 16 from x = 10 to 40
n = 0.2
kFp = np.pi * n
check('problem: k_F = pi n = 0.2 pi for the spinless chain', abs(kFp - 0.2 * np.pi) < 1e-12, kFp)
check('problem: the period pi/k_F = 5 sites', abs(np.pi / kFp - 5) < 1e-12, np.pi / kFp)
check('problem: from x = 10 to 40 the envelope falls by 4 in d = 1 and by 16 in d = 2', (40 / 10) == 4 and (40 / 10) ** 2 == 16,
      (4, 16))
# the same by exact diagonalization: a chain of 4001 sites with the band -2 cos k filled up to the Fermi level of 0.2
# electrons per site, -2 cos(0.2 pi), and an impurity 0.1 t in the middle
N = 4001
c = N // 2
def dens(v, mu=-2 * np.cos(0.2 * np.pi)):
    dd = np.zeros(N); dd[c] = v
    e, w = eigh_tridiagonal(dd, -np.ones(N - 1))
    return (np.abs(w[:, e < mu]) ** 2).sum(axis=1)
n0 = dens(0.0)
check('problem: the chain at this Fermi level has 0.2 electrons per site', abs(n0[c - 500:c + 500].mean() - 0.2) < 1e-3,
      round(n0[c - 500:c + 500].mean(), 4))
dn = dens(0.1) - n0
y = dn[c + 10:c + 300]
s = np.sign(y); z = np.where(s[1:] != s[:-1])[0]
per = 2 * np.diff(z).mean()
check('problem: the density change oscillates with the period 5.0 sites', abs(per - 5) < 0.05, round(per, 3))
far = np.arange(10, 101)
ps = np.linspace(0.5, 1.5, 1001)
res = []
for p in ps:
    M = (far ** -p)[:, None] * np.array([np.cos(2 * kFp * far), np.sin(2 * kFp * far)]).T
    cc = np.linalg.lstsq(M, dn[c + far], rcond=None)[0]
    res.append(np.sum((M @ cc - dn[c + far]) ** 2))
pfit = ps[int(np.argmin(res))]
check('problem: the envelope of the same chain falls as 1/x, a fit from 10 to 100 sites gives the power', abs(pfit - 1) < 0.02,
      round(pfit, 3))

# ------------------------------------------------------------------------- the clean reference of the pyqula script
# the script subtracts the LDOS of the clean lattice from Embedding(h, m=h) with nsuper = 2, on the same k-mesh as the
# map with nsuper = 25. The clean map has the same value on every site, for any nsuper, so the two agree.
from pyqula import geometry, embedding
g = geometry.square_lattice()
h = g.get_hamiltonian(has_spin=False, tij=[-1.])
import tempfile
cwd = os.getcwd()
with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    try:
        l2 = embedding.Embedding(h, m=h).get_ldos(nsuper=2, energy=-3.4, delta=0.05, nk=150)[2]
        l5 = embedding.Embedding(h, m=h).get_ldos(nsuper=5, energy=-3.4, delta=0.05, nk=150)[2]
    finally:
        os.chdir(cwd)
check('script: the clean LDOS is the same on every site with nsuper = 2 and 5', np.ptp(np.concatenate([l2, l5])) < 1e-10,
      (round(float(l2[0]), 6), float(np.ptp(np.concatenate([l2, l5])))))
# the unit of the caption, 10^-3/t: the clean LDOS of pyqula is the density of states per site and per unit of energy,
# (1/N) sum_k (delta/pi)/((E - e_k)^2 + delta^2) on the same 150 x 150 mesh, so the map is in units of 1/t
k150 = 2 * np.pi * np.arange(150) / 150
e150 = -2 * (np.cos(k150)[:, None] + np.cos(k150)[None, :])
lor = ((0.05 / np.pi) / ((-3.4 - e150) ** 2 + 0.05 ** 2)).mean()
check('caption of friedel2d: the LDOS of pyqula is per site and per t, the Lorentzian density of states on the same mesh',
      abs(l2[0] - lor) < 1e-10, (round(float(l2[0]), 6), round(lor, 6)))

# the caption of friedel2d: the change of the LDOS at one energy falls as 1/r in two dimensions, one power slower than
# the density, and the broadening damps it as e^{-2 delta r/v_F}, over v_F/(2 delta) = 14 sites. The T-matrix of the
# impurity v0 = 3t of the figure, -(1/pi) Im[G(r)^2 v0/(1 - v0 G(0))] with G at E = -3.4t + 0.05i on a 1024 mesh,
# is fitted along the axis from r = 7 to 60 with the damping divided out
E2, dl, v2 = -3.4, 0.05, 3.0
kF2 = np.arccos(-E2 / 2 - 1)
vF2 = 2 * np.sin(kF2)
k1024 = 2 * np.pi * np.arange(1024) / 1024
G2 = np.fft.ifft2(1 / (E2 + 1j * dl + 2 * (np.cos(k1024)[:, None] + np.cos(k1024)[None, :])))[:, 0]
ldos_r = -np.imag(G2 ** 2 * v2 / (1 - v2 * G2[0])) / np.pi
rl = np.arange(7, 61).astype(float)
pl = power(ldos_r[7:61], rl, 2 * kF2, np.exp(-2 * dl * rl / vF2))
check('caption of friedel2d: the LDOS change of the impurity 3t at E = -3.4t falls as 1/r, damping divided out', abs(pl - 1) < 0.05, pl)
check('caption of friedel2d: the broadening 0.05t damps it over v_F/(2 delta) = 14 sites, v_F = 2t sin k_F',
      round(vF2 / (2 * dl)) == 14, (round(vF2, 4), round(vF2 / (2 * dl), 2)))

# ------------------------------------------------------------------------------------------------- the widget
# the widget text quotes a ring of 201 sites and an impurity of 1.5t at site 0. Its compute() is run and its density
# change is compared with a ring of our own with these numbers, and the period is pi/k_F with k_F = pi N_e/N
import importlib.util
spec = importlib.util.spec_from_file_location('g4_friedel_widget', os.path.join(HERE, '..', '..', 'widgets', 'defs', 'friedel.py'))
wid = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wid)
Ne = 41
yw = np.asarray(wid.compute({'Ne': Ne})['panels'][0]['series'][2]['y'])
Hr = np.zeros((201, 201))
for j in range(201):
    Hr[j, (j + 1) % 201] = Hr[(j + 1) % 201, j] = -1.0
Hr[0, 0] = 1.5
er, wr = np.linalg.eigh(Hr)
dn_ring = (wr[:, :Ne] ** 2).sum(axis=1) - Ne / 201
check('widget: a ring of 201 sites with the hopping -t and an impurity 1.5t at site 0, the same density change',
      len(yw) == 100 and np.allclose(yw, dn_ring[1:101], atol=1e-12), float(np.abs(yw - dn_ring[1:101]).max()))
sw = np.sign(yw[9:]); zw = np.where(sw[1:] != sw[:-1])[0]
check('widget: the density change oscillates with the period pi/k_F = N/N_e, here 4.9 sites',
      abs(2 * np.diff(zw).mean() / (201 / Ne) - 1) < 0.05, (round(2 * np.diff(zw).mean(), 3), round(201 / Ne, 3)))

# the widget text: an STM map at low bias, which measures the LDOS at the Fermi level, shows the same period pi/k_F around the
# impurity. The infinite chain with the filling of the widget, k_F = pi 41/201, and the impurity 1.5t, by the T-matrix
# delta rho(x) = -(1/pi) Im[g(x)^2 T], T = v0/(1 - v0 g(0)). Route 1, the closed form g(x) = -i e^{i k_F |x|}/(2 sin k_F)
# at the Fermi level. Route 2, the sum over 20000 momenta with the broadening 0.01t. Both oscillate with pi/k_F.
kFw = np.pi * Ne / 201
EFw = -2 * np.cos(kFw)
xw = np.arange(0, 101)
g_cf = -1j * np.exp(1j * kFw * xw) / (2 * np.sin(kFw))
kq = 2 * np.pi * (np.arange(20000) + 0.5) / 20000
g_ks = np.array([np.mean(np.exp(1j * kq * x_) / (EFw + 0.01j + 2 * np.cos(kq))) for x_ in xw])
periods = []
for gx in (g_cf, g_ks):
    Tm = 1.5 / (1 - 1.5 * gx[0])
    drho = -np.imag(gx ** 2 * Tm) / np.pi
    sg = np.sign(drho[10:]); zc = np.where(sg[1:] != sg[:-1])[0]
    periods.append(2 * np.diff(zc).mean())
check('widget: the LDOS at the Fermi level around the impurity oscillates with the same period pi/k_F = 4.9 sites, by two routes',
      all(abs(p_ / (201 / Ne) - 1) < 0.05 for p_ in periods) and np.allclose(g_cf[:3], g_ks[:3], atol=0.02),
      (np.round(periods, 3).tolist(), round(201 / Ne, 3)))
# "at low bias": an STM map at the bias V measures the LDOS at E_F + eV, whose period is pi/k(E_F + eV). At the bias
# 0.5t the same closed form oscillates with pi/k(E) and not with pi/k_F, so the period of the widget needs a low bias.
Eb = EFw + 0.5
kb = np.arccos(-Eb / 2)
gb = -1j * np.exp(1j * kb * xw) / (2 * np.sin(kb))
drb = -np.imag(gb ** 2 * (1.5 / (1 - 1.5 * gb[0]))) / np.pi
sb = np.sign(drb[10:]); zb = np.where(sb[1:] != sb[:-1])[0]
pb = 2 * np.diff(zb).mean()
check('widget: at the bias 0.5t the LDOS has the period pi/k(E_F + 0.5t) and not pi/k_F, so the same period needs a low bias',
      abs(pb / (np.pi / kb) - 1) < 0.05 and abs(pb / (201 / Ne) - 1) > 0.1, (round(pb, 3), round(np.pi / kb, 3), round(201 / Ne, 3)))

# the text before the key box: delta n(x) = -int dq/2pi e^{iqx} chi_0(q) v0, with the minus sign. A ring of 400 sites at
# mu = -t and T = 0.05t, an onsite energy v0 = 1e-4 on site 0. Route 1, the exact density by diagonalization. Route 2,
# the Fourier sum of (9.4) with the minus sign. A repulsive impurity lowers the density on its site.
Nr = 400
Hr0 = np.zeros((Nr, Nr))
for j in range(Nr):
    Hr0[j, (j + 1) % Nr] = Hr0[(j + 1) % Nr, j] = -1.0
nF = lambda e: 0.5 * (1 - np.tanh((e + 1.0) / (2 * 0.05)))
def dens_ring(v0):
    H_ = Hr0.copy(); H_[0, 0] += v0
    e_, w_ = np.linalg.eigh(H_)
    return (w_ ** 2 * nF(e_)).sum(axis=1)
v0 = 1e-4
dn_exact = (dens_ring(v0) - dens_ring(-v0)) / 2
qr = 2 * np.pi * np.arange(Nr) / Nr
chq = np.array([chi0_chain(q_, -1.0, 0.05, nk=Nr) for q_ in qr])
dn_four = -v0 * np.array([np.mean(np.exp(1j * qr * x_) * chq).real for x_ in range(Nr)])
check('text: delta n(x) = -int dq/2pi e^{iqx} chi_0(q) v0, the exact density of a ring and the Fourier sum agree, and '
      'delta n(0)/v0 = -0.25 < 0', np.abs(dn_exact - dn_four).max() < 1e-4 * v0 and abs(dn_exact[0] / v0 + 0.25) < 0.005,
      (round(dn_exact[0] / v0, 4), float(np.abs(dn_exact - dn_four).max() / v0)))

# ------------------------------------------------------------------------------------------------- the lab box
# our reading: the Fermi wavelength is 2 pi/k_F, so lambda_F/2 = pi/k_F, the period of (9.9)
check('lab: lambda_F/2 = pi/k_F for any k_F', all(abs((2 * np.pi / q) / 2 - np.pi / q) < 1e-12 for q in (0.3, 1.0, 2.2)),
      'identity')
print('all checks of page 06 hold')
