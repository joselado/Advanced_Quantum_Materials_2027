"""Session 9, the numbers and the algebra that page 05 (Section 9.5a, the RPA and the plasmon) states.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or
in the figure script that draws it. The page has no plot of its own, so everything is here: the iteration of the
self-consistent equation of the steps fold, the numbers of the three quizzes and of the problem, and the reading of
the lab box, that a two-dimensional plasmon goes to zero as q -> 0, with omega_pl^2 proportional to q. That one is
computed from the sum over the Fermi sea of (9.5), on a polar grid, for the 2D electron gas and for the Dirac cone of
graphene, and compared with the closed forms, omega^2 = 2 pi n e^2 q/m + (3/4) v_F^2 q^2 for the gas and
omega^2 = 2 e^2 E_F q/hbar^2 for the cone with its four flavors. The 3D gas of (9.7) is computed in the same way as
a contrast, and it goes to omega_p. Since the pick of the lecturer of 2026-11-22 the page says after (9.6) that chi_0
counts one spin, and that for an interaction that couples to the total density the denominator is 1 + 2 v(q) chi_0. The
sums below hold the two spins, so the root of 1 + v(q) chi_gas, with chi_gas the sum over the two spins, is the root of
1 + 2 v(q) chi_0 with the chi_0 of one spin, and chi_0 is negative above the continuum, which is what the sheet
webnotes/conventions/session09.md states. The caption of Figure 9.2 writes 1 + 2 v(q) chi_0 since the same day, in place
of the old 1 - v(q) chi_0. The new sentence is checked on a ring with a self-consistent Hartree loop, and the steps fold of
the plasma frequency by its algebra and by the sum over the Fermi sphere. The lab box numbers are checked against the
stored source. Nothing here writes a file.

Run it from anywhere:  python3 webnotes/checks/session09/g3_05_rpa_plasmons.py"""
import os, sys
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq

WEBNOTES = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(WEBNOTES, 'figures', 'session09'))
import _g3_chi0path as cp                                  # the elliptic density of states of the square lattice


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# ---- the steps fold: iterating chi = chi_0 - chi_0 U chi gives the partial sums of the geometric series
def iterate(x, n):
    """chi/chi_0 after n iterations of the self-consistent equation from chi = chi_0, with x = U chi_0."""
    c = 1.0
    out = [c]
    for _ in range(n):
        c = 1.0 - x * c
        out.append(c)
    return out


for x in (0.2, 0.5, -0.7):
    it = iterate(x, 6)
    partial = [sum((-x) ** j for j in range(k + 1)) for k in range(7)]
    check('the iteration adds one bubble and one line, with the factor -U chi_0, x = %.1f' % x,
          np.allclose(it, partial, atol=1e-14), np.round(it[:4], 4).tolist())
x = 0.5
check('the series converges to 1/(1+U chi_0) for |U chi_0| < 1', abs(iterate(x, 80)[-1] - 1 / (1 + x)) < 1e-12,
      iterate(x, 80)[-1])
x = 2.0
check('for U chi_0 = 2 the series does not converge, while chi_0/(1+U chi_0) solves the equation',
      abs(iterate(x, 30)[-1]) > 1e6 and abs((1 / (1 + x)) - (1 - x / (1 + x))) < 1e-15, (iterate(x, 4), 1 / (1 + x)))
part = [sum((-x) ** j for j in range(k + 1)) for k in range(50) for x in (-1.0,)]
check('each truncation is a polynomial, finite at U chi_0 = -1, while (9.6) has the pole there',
      part[:4] == [1.0, 2.0, 3.0, 4.0] and all(np.isfinite(part)), 'partial sums at U chi_0 = -1 are 1, 2, 3, ...')
x = 1.0
p1 = [sum((-x) ** j for j in range(k + 1)) for k in range(6)]
check('the fold: at U chi_0 = 1 the partial sums are 1, 0, 1, 0, while chi_0/2 solves chi (1 + U chi_0) = chi_0',
      p1 == [1.0, 0.0, 1.0, 0.0, 1.0, 0.0] and abs(0.5 * (1 + x) - 1) < 1e-15, p1)
x = -1.0
check('the fold: at U chi_0 = -1 the equation chi (1 + U chi_0) = chi_0 reads 0 = chi_0, with no solution',
      all(abs(c * (1 + x) - 1.0) == 1.0 for c in (-1e9, -1.0, 0.0, 1.0, 1e9)) and 1 / (1 + -0.999) > 999,
      'chi (1 + U chi_0) = 0 for every chi, and chi/chi_0 = 1000 at U chi_0 = -0.999')

# ---- the recall box: (9.5) sums over the pairs of one filled and one empty state, in both orders
nk = 20000
kc = 2 * np.pi * (np.arange(nk) + 0.5) / nk
qc, wc, Tc = 0.3, 6.0, 0.01
f1c = 0.5 * (1 - np.tanh(-2 * np.cos(kc) / (2 * Tc)))
f2c = 0.5 * (1 - np.tanh(-2 * np.cos(kc + qc) / (2 * Tc)))
Dc = -2 * np.cos(kc + qc) + 2 * np.cos(kc)
order1 = np.mean(f1c * (1 - f2c) / (Dc - wc))            # k filled, k+q empty
order2 = np.mean(-f2c * (1 - f1c) / (Dc - wc))           # k empty, k+q filled
full = np.mean((f1c - f2c) / (Dc - wc))
check('recall: both orders of the pair enter (9.5), half-filled chain at q = 0.3, omega = 6t, and they add to (9.5)',
      abs(order1) > 1e-3 and abs(order2) > 1e-3 and abs(order1 + order2 - full) < 1e-12 and full < 0,
      (round(order1, 5), round(order2, 5), round(full, 5)))

# ---- the quiz on screening: U = t and chi_0 = 0.68/t
check('quiz 1: chi = 0.68/1.68 = 0.40/t, the denominator 1.68 is larger than one',
      round(0.68 / 1.68, 2) == 0.40 and abs(1 + 0.68 - 1.68) < 1e-12 and 0.68 / 1.68 < 0.68, 0.68 / 1.68)
gM = cp.elliptic(0.1)[1]
ks = 2 * np.pi * (np.arange(240) + 0.5) / 240
KX, KY = np.meshgrid(ks, ks, indexing='ij')
es = -2 * (np.cos(KX) + np.cos(KY))
small = np.abs(es) < 1e-9                                   # eps(k+Q) = -eps(k) at half filling, T = 0.1t
mesh = float(np.mean(np.where(small, 1 / (4 * 0.1), np.tanh(es / 0.2) / (2 * np.where(small, 1.0, es)))))
check('quiz 1: chi_0(pi,pi) = 0.68/t on the half-filled square lattice at T = 0.1t, by two routes',
      round(gM, 2) == 0.68 and abs(mesh - gM) < 2e-3, (gM, mesh))

# ---- the quiz on the plasmon: at q = 0.1 k_F the pairs end at hbar omega_+ = 0.21 E_F
hbar = m = kF = 1.0
EF, vF, q = hbar ** 2 * kF ** 2 / (2 * m), hbar * kF / m, 0.1 * kF
wplus = (hbar * vF * q + hbar ** 2 * q ** 2 / (2 * m)) / EF
check('quiz 2: hbar omega_+ = hbar v_F q + hbar^2 q^2/2m = 0.21 E_F at q = 0.1 k_F', abs(wplus - 0.21) < 1e-12, wplus)
qs = np.array([0.1, 0.03, 0.01])
check('quiz 2: omega_+ goes to zero with q', np.all(np.diff((vF * qs + qs ** 2 / 2)) < 0), (vF * qs + qs ** 2 / 2).tolist())
rs = 4.0                                                    # atomic units, hbar = m = e = a_0 = 1
n_rs = 3 / (4 * np.pi * rs ** 3)
EF_rs = (3 * np.pi ** 2 * n_rs) ** (2 / 3) / 2
wp_rs = np.sqrt(4 * np.pi * n_rs)
closed = 2 * np.sqrt(3) * np.sqrt(rs) / (9 * np.pi / 4) ** (2 / 3)
check('quiz 2: hbar omega_p = 1.9 E_F for one electron per sphere of radius 4 a_0, far above 0.21 E_F',
      round(wp_rs / EF_rs, 1) == 1.9 and abs(wp_rs / EF_rs - closed) < 1e-12 and wp_rs / EF_rs > 0.21,
      (wp_rs / EF_rs, closed))

# ---- the quiz on the series, U chi_0 = 0.2
x = 0.2
three, rpa, plus, first = 1 - x + x * x, 1 / (1 + x), 1 / (1 - x), 1 - x
check('quiz 3: the three terms give 0.84 chi_0 and (9.6) gives 0.833 chi_0',
      abs(three - 0.84) < 1e-12 and round(rpa, 3) == 0.833, (three, rpa))
check('quiz 3: the series with all signs + sums to chi_0/(1-U chi_0) = 1.25 chi_0',
      abs(plus - 1.25) < 1e-12 and abs(sum(x ** j for j in range(200)) - plus) < 1e-12, plus)
check('quiz 3: the first order chi_0 - U chi_0^2 gives 0.8 chi_0', abs(first - 0.8) < 1e-12, first)

# ---- the problem
x = 0.5
check('problem: U chi_0 = 0.5, three terms 0.75, (9.6) 0.667, with the fourth term 0.625',
      abs(1 - x + x * x - 0.75) < 1e-12 and round(1 / (1 + x), 3) == 0.667 and abs(1 - x + x * x - x ** 3 - 0.625) < 1e-12
      and abs(-x ** 3 + 0.125) < 1e-12 and 0.625 < 1 / (1 + x) < 0.75, (0.75, 1 / (1 + x), 0.625))
x = 2.0
ps = [sum((-x) ** j for j in range(k + 1)) for k in range(4)]
check('problem: U chi_0 = 2, three terms 3, partial sums 1, -1, 3, -5, and (9.6) gives 0.333',
      ps == [1.0, -1.0, 3.0, -5.0] and round(1 / (1 + x), 3) == 0.333 and abs(1 / 3 - (1 - 2 / 3)) < 1e-15, ps)


# ---- the lab box: the plasmon in two dimensions goes to zero as sqrt(q)
def polar(nr=1000, nt=1000):
    r = (np.arange(nr) + 0.5) / nr
    th = 2 * np.pi * (np.arange(nt) + 0.5) / nt
    R, TH = np.meshgrid(r, th, indexing='ij')
    return R, TH, R / (nr * nt) * 2 * np.pi / (2 * np.pi) ** 2        # the weight of d^2k/(2 pi)^2 inside k_F = 1


R, TH, W = polar()


def chi_gas2d(q, w):
    """(9.5) summed over the filled disk, two spins, hbar = m = k_F = 1, written as sum_k f_k 2D/(D^2 - w^2)."""
    D = R * q * np.cos(TH) + q * q / 2
    return 2 * np.sum(W * 2 * D / (D * D - w * w))


def chi_dirac(q, w):
    """The intraband part of (9.5) for the doped Dirac cone eps = v|k| with v = k_F = 1, with the overlap of the two
    spinors, for 4 flavors (spin and valley). The interband part is of order q^2 and not q^2/w^2, so it does not
    change the limit q -> 0."""
    kx, ky = R * np.cos(TH), R * np.sin(TH)
    kq = np.sqrt((kx + q) ** 2 + ky ** 2)
    D = kq - R
    F = (1 + (kx * (kx + q) + ky * ky) / (R * kq)) / 2
    return 4 * np.sum(W * F * 2 * D / (D * D - w * w))


n2 = 2 * np.sum(W)
check('the polar grid holds the density of the 2D gas, k_F^2/2pi for two spins', abs(n2 - 1 / (2 * np.pi)) < 1e-12, n2)
e2 = 1.0
rows = []
for q in (0.001, 0.002, 0.004):
    wg = brentq(lambda w: 1 + 2 * np.pi * e2 / q * chi_gas2d(q, w), 1.5 * (q + q * q / 2), 2.0)
    wd = brentq(lambda w: 1 + 2 * np.pi * e2 / q * chi_dirac(q, w), 1.5 * q, 2.0)
    rows.append((q, wg, wd, chi_gas2d(q, wg), -n2 * q * q / wg ** 2))
ok = all(abs(wg ** 2 - (2 * np.pi * n2 * e2 * q + 0.75 * q * q)) < 2e-3 * wg ** 2 for q, wg, wd, c, lead in rows)
ok = ok and all(c < 0 and abs(c / lead - 1) < 0.01 for q, wg, wd, c, lead in rows)
check('2D gas: the zero of 1 + v(q) chi_0 with v = 2 pi e^2/q gives omega^2 = 2 pi n e^2 q/m + (3/4) v_F^2 q^2', ok,
      ['q=%.3f omega=%.4f omega^2/q=%.4f' % (q, wg, wg * wg / q) for q, wg, wd, c, lead in rows])
ok = all(abs(wd ** 2 / q - 2.0) < 0.01 for q, wg, wd, c, lead in rows)
ok = ok and abs(rows[0][2] ** 2 / rows[0][0] - rows[1][2] ** 2 / rows[1][0]) < 0.005
check('Dirac cone: omega^2/q goes to 2 e^2 E_F/hbar^2, so the plasmon of graphene goes to zero as sqrt(q)', ok,
      ['q=%.3f omega=%.4f omega^2/q=%.4f' % (q, wd, wd * wd / q) for q, wg, wd, c, lead in rows])
check('both 2D plasmons go to zero with q', all(rows[i][1] < rows[i + 1][1] and rows[i][2] < rows[i + 1][2]
                                                 for i in range(2)) and rows[0][1] < 0.04 and rows[0][2] < 0.05,
      [(r[0], round(r[1], 4), round(r[2], 4)) for r in rows])


def chi_gas3d(q, w, nk=800, nc=800):
    """(9.5) of the 3D gas over the filled sphere, two spins, in the same form, hbar = m = k_F = 1."""
    k = (np.arange(nk) + 0.5) / nk
    c = -1 + 2 * (np.arange(nc) + 0.5) / nc
    K, C = np.meshgrid(k, c, indexing='ij')
    D = K * q * C + q * q / 2
    return 2 * np.sum(K ** 2 * 2 * D / (D * D - w * w)) * (1 / nk) * (2 / nc) * 2 * np.pi / (2 * np.pi) ** 3


n3, wp = 1 / (3 * np.pi ** 2), 1.0
e2_3 = wp ** 2 / (4 * np.pi * n3)
w3 = [brentq(lambda w: 1 + 4 * np.pi * e2_3 / q ** 2 * chi_gas3d(q, w), 1.5 * (q + q * q / 2), 5.0) for q in (0.02, 0.04)]
check('3D gas, as a contrast: the zero of 1 + v(q) chi_0 with v = 4 pi e^2/q^2 stays at omega_p = 1 as q -> 0',
      all(abs(w - wp) < 0.01 for w in w3), w3)
# The plasma fold, picked factor 2 of 2026-11-22: v(q) couples to the total density, so with the chi_0 of one spin, the
# half of chi_gas3d, the zero of 1 + 2 v(q) chi_0 is at omega_p and the zero of 1 + v(q) chi_0 at omega_p/sqrt(2).
chi1 = lambda q, w: chi_gas3d(q, w) / 2                    # the chi_0 of one spin
w3a = [brentq(lambda w: 1 + 2 * 4 * np.pi * e2_3 / q ** 2 * chi1(q, w), 1.5 * (q + q * q / 2), 5.0) for q in (0.02, 0.04)]
w3s = brentq(lambda w: 1 + 4 * np.pi * e2_3 / 0.02 ** 2 * chi1(0.02, w), 1.5 * (0.02 + 0.0002), 5.0)
check('plasma fold: with chi_0 of one spin, 1 + 2 v(q) chi_0 = 0 gives omega_p, and 1 + v(q) chi_0 = 0 gives omega_p/sqrt(2)',
      all(abs(w - wp) < 0.01 for w in w3a) and abs(w3s - wp / np.sqrt(2)) < 0.01, (np.round(w3a, 4).tolist(), round(w3s, 4), round(wp / np.sqrt(2), 4)))
# The algebra of the fold. The first term of the expansion vanishes, the shift k -> k - q gives the bracket
# eps(k+q) + eps(k-q) - 2 eps(k), which is hbar^2 q^2/m for free electrons, and the result is -n_sigma q^2/(m omega^2).
kg = 2 * np.pi * (np.arange(4000) + 0.5) / 4000
ec = lambda kk: -2 * np.cos(kk)                               # a periodic band, where the shift k -> k - q is exact
qf, wf, Tf, muf = 2 * np.pi * 40 / 4000, 9.0, 0.05, -1.0
fq = lambda e: 0.5 * (1 - np.tanh((e - muf) / (2 * Tf)))
num = fq(ec(kg)) - fq(ec(kg + qf))
dk = ec(kg + qf) - ec(kg)
second = -np.mean(num * dk) / wf ** 2
shifted = -np.mean(fq(ec(kg)) * (ec(kg + qf) + ec(kg - qf) - 2 * ec(kg))) / wf ** 2
full = np.mean(num / (dk - wf))
check('plasma fold: the first term sums to zero, the shift k -> k-q gives the bracket, and at omega >> the pair energies '
      'the second term is (9.5), chain q = 0.063, omega = 9t',
      abs(np.mean(num)) < 1e-15 and abs(second - shifted) < 1e-15 and abs(full / second - 1) < 1e-3 and second < 0,
      (np.mean(num), second, shifted, full))
rng_ = np.random.default_rng(5)
kv_ = rng_.normal(size=(5, 3)); qv_ = rng_.normal(size=3)
free = lambda kk: 0.5 * np.sum(kk ** 2, axis=-1)            # hbar = m = 1
check('plasma fold: for free electrons the bracket is hbar^2 q^2/m for every k',
      np.allclose(free(kv_ + qv_) + free(kv_ - qv_) - 2 * free(kv_), qv_ @ qv_), round(float(qv_ @ qv_), 6))
c1, c1_exp = chi1(0.1, 1.2), -(n3 / 2) * 0.1 ** 2 / 1.2 ** 2
check('plasma fold: the chi_0 of one spin of the 3D gas at q = 0.1 k_F, omega = 1.2 is -n_sigma q^2/(m omega^2) within '
      '2 percent, with n_sigma = n/2, and negative', c1 < 0 and abs(c1 / c1_exp - 1) < 0.02, (round(c1, 7), round(c1_exp, 7)))
wpg = np.sqrt(4 * np.pi * n3 * e2_3)
check('plasma fold: 2 v(q) n_sigma q^2/m = 4 pi n e^2/m = omega_p^2, independent of q', abs(wpg - wp) < 1e-12
      and all(abs(2 * 4 * np.pi * e2_3 / q ** 2 * (n3 / 2) * q ** 2 - wp ** 2) < 1e-12 for q in (0.01, 0.1, 1.0)), wpg)

# ---- the sentence after (9.6): "Here chi_0 counts one spin. For an interaction that couples to the total density, the
# denominator is 1 + 2 v(q) chi_0." A ring of 200 sites, spinful, mu = -t, T = 0.1t, a weak external v_ext cos(qx) on both
# spins, and a self-consistent Hartree loop with the pair interaction v(r) = 0.4 e^{-|r|} on the total density, measured
# from the unperturbed density. The response delta n_q / v_ext of the total density is -2 chi_0/(1 + 2 v_q chi_0), with
# chi_0 of (9.4) per spin on the same ring and v_q the Fourier sum of v(r). With the Hubbard U the field of one spin comes
# from the other spin only, and the same loop gives -2 chi_0/(1 + U chi_0).
Nh, muh, Th, vext = 200, -1.0, 0.1, 1e-5
xh = np.arange(Nh)
H0h = -np.eye(Nh, k=1) - np.eye(Nh, k=-1); H0h[0, -1] = H0h[-1, 0] = -1
rr = np.minimum(xh, Nh - xh)
vr = 0.4 * np.exp(-rr.astype(float))
Vmat = np.array([np.roll(vr, i) for i in range(Nh)])          # v(i - j) on the ring
fh = lambda e: 0.5 * (1 - np.tanh((e - muh) / (2 * Th)))
def spin_density(pot):
    w_, u_ = np.linalg.eigh(H0h + np.diag(pot))
    return (np.abs(u_) ** 2 * fh(w_)).sum(axis=1)
n0s = spin_density(np.zeros(Nh))
def hartree(mh, kind, U=1.0):
    q = 2 * np.pi * mh / Nh
    ext = vext * np.cos(q * xh)
    dns = np.zeros(Nh)                                       # the change of the density of one spin, the same for both
    for _ in range(400):
        field = Vmat @ (2 * dns) if kind == 'total' else U * dns
        new = spin_density(ext + field) - n0s
        if np.abs(new - dns).max() < 1e-16:
            break
        dns = 0.5 * dns + 0.5 * new
    kq = 2 * np.pi * np.arange(Nh) / Nh
    ek, ekq = -2 * np.cos(kq), -2 * np.cos(kq + q)
    de = ekq - ek
    sm = np.abs(de) < 1e-12
    c0 = float(np.mean(np.where(sm, fh(ek) * (1 - fh(ek)) / Th, (fh(ek) - fh(ekq)) / np.where(sm, 1.0, de))))
    vq_ = float(np.sum(vr * np.cos(q * xh)))
    resp = 2 * np.mean(2 * dns * np.cos(q * xh)) / vext       # delta n_q / v_ext of the total density
    return resp, c0, vq_
rows_h = [(mh,) + hartree(mh, 'total') for mh in (10, 30, 60)]
check('after (9.6): with v(r) on the total density the Hartree loop gives -2 chi_0/(1 + 2 v_q chi_0), chi_0 of one spin',
      all(abs(r_ / (-2 * c0 / (1 + 2 * vq_ * c0)) - 1) < 2e-3 and abs(r_ / (-2 * c0 / (1 + vq_ * c0)) - 1) > 0.05
          for mh, r_, c0, vq_ in rows_h),
      [(mh, round(r_, 5), round(-2 * c0 / (1 + 2 * vq_ * c0), 5), round(vq_, 4)) for mh, r_, c0, vq_ in rows_h])
r_, c0, vq_ = hartree(30, 'hubbard', U=1.0)
check('after (9.6): with the Hubbard U = t the same loop gives -2 chi_0/(1 + U chi_0), the denominator of (9.6)',
      abs(r_ / (-2 * c0 / (1 + c0)) - 1) < 2e-3, (round(r_, 5), round(-2 * c0 / (1 + c0), 5)))

# ---- the caption of Figure 9.2: above the continuum chi_0 of (9.5) is negative, so the plasmon is a zero of
# 1 + 2 v(q) chi_0 with the chi_0 of one spin, and 1 - 2 v(q) chi_0 is larger than one there and has no zero.
# Route 1 is the sum over the filled sphere of both spins, route 2 the expansion -n q^2/(m omega^2), with n = k_F^3/(3 pi^2)
# the density of both spins, which is 2 v(q) times the -n_sigma q^2/(m omega^2) of one spin.
c_sum = chi_gas3d(0.1, 1.2)
c_exp = -n3 * 0.1 ** 2 / 1.2 ** 2
ws_ = np.linspace(1.5 * (0.1 + 0.005), 5.0, 60)
minus = [1 - 4 * np.pi * e2_3 / 0.1 ** 2 * chi_gas3d(0.1, w) for w in ws_]
check('caption of Figure 9.2: chi_0 < 0 above the continuum by two routes, so 1 - 2 v chi_0 > 1 has no zero there',
      c_sum < 0 and abs(c_sum / c_exp - 1) < 0.02 and min(minus) > 1, (round(c_sum, 6), round(c_exp, 6), round(min(minus), 3)))

# ---- the text after the steps: a pole at omega = 0 is a phase transition, a pole at a finite omega a collective mode.
# The static density response of the half-filled square lattice at T = 0.1t has chi_0(q,0) > 0 at every q of a mesh,
# so 1 + U chi_0 > 1 for U > 0 and the density channel has no pole at omega = 0, while the spin channel has one at
# U = 1/chi_0(pi,pi), the transition of Section 9.5b, and the plasmon is a pole at the finite omega_p.
kk_ = 2 * np.pi * (np.arange(120) + 0.5) / 120
KX_, KY_ = np.meshgrid(kk_, kk_, indexing='ij')
E_ = -2 * (np.cos(KX_) + np.cos(KY_))
f_ = 1 / (np.exp(E_ / 0.1) + 1)
stat = []
for iq in range(0, 61, 6):
    for jq in range(0, iq + 1, 6):
        Eq_ = np.roll(np.roll(E_, -iq, 0), -jq, 1); fq_ = np.roll(np.roll(f_, -iq, 0), -jq, 1)
        de_ = Eq_ - E_; sm_ = np.abs(de_) < 1e-9
        stat.append(float(np.mean(np.where(sm_, f_ * (1 - f_) / 0.1, (f_ - fq_) / np.where(sm_, 1.0, de_)))))
check('text: the static chi_0(q,0) > 0 at every q, so 1 + U chi_0 > 1 for U > 0, while 1 - U chi_0 vanishes at U = 1/0.68t '
      'and the plasmon pole sits at the finite omega_p', min(stat) > 0 and abs(1 / max(stat) - 1 / 0.677) < 0.02 and abs(w3[0] - wp) < 0.01,
      (round(min(stat), 4), round(max(stat), 4), round(w3[0], 4)))

# ---- the solution of the problem: the series converges for every |U chi_0| < 1, also when it is not small, and it
# does not converge for |U chi_0| >= 1, while (9.6) stays finite except at its pole U chi_0 = -1
conv = iterate(0.9, 400)[-1]
diverge = {x: iterate(x, 60) for x in (1.0, 2.0, -1.0, -2.0)}
check('solution: at U chi_0 = 0.9 the partial sums go to 1/1.9 = 0.526, and at U chi_0 = 1, 2, -1 and -2 they do not converge',
      abs(conv - 1 / 1.9) < 1e-12 and round(1 / 1.9, 3) == 0.526
      and all(abs(v_[-1] - v_[-2]) >= 1.0 for v_ in diverge.values()), (conv, {x: v_[-2:] for x, v_ in diverge.items() if abs(x) == 1}))
check('solution: the closed form chi_0/(1 + U chi_0) is finite at U chi_0 = 1, 2 and -2, and has its pole only at -1',
      all(np.isfinite(1 / (1 + x)) for x in (1.0, 2.0, -2.0)) and abs(1 / (1 + 2.0) - 1 / 3) < 1e-15, [1 / (1 + x) for x in (1.0, 2.0, -2.0)])

# ---- the lab box against its stored source
src = open(os.path.join(WEBNOTES, 'sources', 'session09', 'fei2012_arxiv1202.4993.txt'), encoding='utf-8').read()
quotes = ['The wavelength of graphene plasmons is of the order of 200 nm at technologically relevant infrared frequencies, '
          'and they can propagate several times this distance.',
          'We have succeeded in altering both the amplitude and wavelength of these plasmons by gate voltage.',
          'Through infrared nano-imaging we explicitly show that common graphene/SiO2/Si back-gated structures support '
          'propagating surface plasmons.',
          'by exploring real space profiles of plasmon standing waves formed between the tip of our nano-probe and edges of '
          'the samples.']
check('the lab box: the three sentences are in the stored abstract', all(s in src for s in quotes), '200 nm')
print('all checks of page 05 of Session 9 hold')
