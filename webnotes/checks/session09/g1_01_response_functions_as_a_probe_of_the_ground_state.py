"""Session 9, the numbers and the statements that page 01 (Section 9.1) quotes, in the steps fold, the two quizzes and
the problem. The page has no lab box and no figure that states a number in its caption.

The picture quiz shows the static density response chi(x, x') of three rings of 40 sites, drawn by
webnotes/figures/session09/_g1_ringchi.py from the sum over pairs of eigenstates. Here the same matrix is computed
by a second route, a finite difference of the density of the ring when one onsite energy changes, so the sign of the
sheet, delta n = -chi v, is checked again, and the numbers of the feedback (0.25/t on the diagonal, 0.09/t on the
impurity) are asserted. The quiz states it as an onsite energy lowered by delta mu, which raises the density at x' by
chi(x, x') delta mu, the sign of delta A = chi f of the key box, and this is asserted too. What the maps show is checked
on the matrix clipped to the color scale of the figure, +-0.1/t, which the script reads from the figure helper without
running it. The problem is checked by the closed form and by the direct sum. The condition of the key box, a response
at q + G in a crystal, is checked on a ring with two sites per cell.

It needs numpy and scipy, and writes no file.

Run it from anywhere:  python3 webnotes/checks/session09/g1_01_response_functions_as_a_probe_of_the_ground_state.py"""
import ast, os, sys
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# ---------------------------------------------------------------------------------------------------------------
# the steps fold and the first quiz: on a ring a response that depends only on n' - n keeps the wavevector
N = 60
m = np.arange(N)
d = np.minimum(m, N - m)
chim = np.exp(-d / 3.0) * np.cos(1.1 * d)                         # any response that depends only on the distance
M = np.array([[chim[(n1 - n0) % N] for n0 in range(N)] for n1 in range(N)])   # M[n', n] = chi(n' - n)
q = 2 * np.pi * 7 / N
f = np.exp(1j * q * m)
dA = M @ f
chiq = np.sum(chim * np.exp(-1j * q * m))
check('steps, a perturbation e^{iqn} gives chi(q) e^{iqn\'}', np.allclose(dA, chiq * np.exp(1j * q * m), atol=1e-12),
      'largest difference %.1e' % np.abs(dA - chiq * np.exp(1j * q * m)).max())
check('quiz 1, the pairs (0,5) and (10,15) have the same response', np.isclose(M[5, 0], M[15, 10]), (round(float(M[5, 0]), 6), round(float(M[15, 10]), 6)))
Mimp = M.copy()
Mimp[:3, :3] += 0.3                                                # a response that depends on n and n' near one site
spec = np.abs(np.fft.fft(Mimp @ f)) / N
other = np.delete(spec, 7)
check('steps, near an impurity a perturbation at q gives other wavevectors', other.max() > 1e-3,
      'largest weight at another q %.3f, at q %.3f' % (other.max(), spec[7]))


# the key box: in a crystal with two sites per cell a perturbation at q also gives a response at q + G, G = pi
def ring_chi(onsite, hop, mu, T=0.05):
    """chi(x, x') = -d n(x') / d v(x) of a ring, from the sum over the pairs of eigenstates."""
    n = len(onsite)
    i = np.arange(n)
    H = np.diag(np.asarray(onsite, dtype=float))
    H[i, (i + 1) % n] = H[(i + 1) % n, i] = -np.asarray(hop, dtype=float)
    e, w = np.linalg.eigh(H)
    fe = 0.5 * (1 - np.tanh((e - mu) / (2 * T)))
    de, df = e[None, :] - e[:, None], fe[:, None] - fe[None, :]
    same = np.abs(de) < 1e-10
    F = np.where(same, (fe * (1 - fe) / T)[:, None] * np.ones(n), df / np.where(same, 1.0, de))
    A = np.einsum('xa,xb->xab', w, w)
    return np.einsum('xab,ab,yab->xy', A, F, A)


NR, KQ = 40, 6
iq = np.arange(NR)
fq = np.exp(1j * 2 * np.pi * KQ / NR * iq)
weights = {}
for name, hop in (('one site per cell', np.ones(NR)), ('two sites per cell', np.where(iq % 2 == 0, 1.0, 0.6))):
    w_q = np.abs(np.fft.fft(ring_chi(np.zeros(NR), hop, 0.3).T @ fq)) / NR
    weights[name] = (w_q[KQ], w_q[KQ + NR // 2], np.delete(w_q, [KQ, KQ + NR // 2]).max())
one, two = weights['one site per cell'], weights['two sites per cell']
check('key box, a ring with hoppings 1 and 0.6 answers a perturbation at q at q and at q + pi only, the clean ring at q only',
      two[1] > 0.1 and two[2] < 1e-12 and one[1] < 1e-12 and one[2] < 1e-12,
      'two sites per cell: q %.4f, q + pi %.4f, elsewhere %.0e; one site per cell: q + pi %.0e' % (two[0], two[1], two[2], one[1]))

# ---------------------------------------------------------------------------------------------------------------
# the problem: chi(n) = e^{-|n|/xi}
def chi_sum(q, xi, nmax=4000):
    n = np.arange(-nmax, nmax + 1)
    return float(np.sum(np.exp(-np.abs(n) / xi) * np.cos(q * n)))


def chi_closed(q, xi):
    a = np.exp(-1 / xi)
    return (1 - a * a) / (1 - 2 * a * np.cos(q) + a * a)


c0, cpi = chi_sum(0, 1), chi_sum(np.pi, 1)
check('problem, chi(0) = coth(1/2) = 2.16 by the sum and by the closed form',
      abs(c0 - 1 / np.tanh(0.5)) < 1e-10 and abs(chi_closed(0, 1) - c0) < 1e-10 and round(c0, 2) == 2.16, round(c0, 4))
check('problem, chi(pi) = tanh(1/2) = 0.46 by the sum and by the closed form',
      abs(cpi - np.tanh(0.5)) < 1e-10 and abs(chi_closed(np.pi, 1) - cpi) < 1e-10 and round(cpi, 2) == 0.46, round(cpi, 4))
qs = np.linspace(0, np.pi, 7)
check('problem, the closed form against the sum at seven q and xi = 1, 3', all(abs(chi_sum(x, xi) - chi_closed(x, xi)) < 1e-9
      for x in qs for xi in (1, 3)), 'ok')
half = {xi: brentq(lambda x: chi_closed(x, xi) / chi_closed(0, xi) - 0.5, 1e-6, np.pi) for xi in (10, 20, 50)}
check('problem, for a long xi chi(q) falls to half of chi(0) at about q = 1/xi',
      all(abs(half[xi] * xi - 1) < 0.01 for xi in half), {xi: round(half[xi] * xi, 4) for xi in half})

# ---------------------------------------------------------------------------------------------------------------
# the picture quiz: three rings of 40 sites, hopping -t, mu = 0, T = 0.05 t
L, MU, T = 40, 0.0, 0.05


def density(onsite):
    H = np.diag(onsite)
    i = np.arange(L)
    H[i, (i + 1) % L] = H[(i + 1) % L, i] = -1.0
    e, w = np.linalg.eigh(H)
    return (w ** 2) @ (0.5 * (1 - np.tanh((e - MU) / (2 * T))))


def response(onsite, dv=1e-5):
    """chi(x, x') = -d n(x') / d v(x), by a finite difference, column x of the transpose."""
    out = np.zeros((L, L))
    for x in range(L):
        up, dn = onsite.copy(), onsite.copy()
        up[x] += dv; dn[x] -= dv
        out[x] = -(density(up) - density(dn)) / (2 * dv)
    return out


def spread(chi):
    return max(np.ptp([chi[x, (x + s) % L] for x in range(L)]) for s in range(L))


clean = np.zeros(L)
imp = np.zeros(L); imp[20] = 2.0
rnd = np.random.default_rng(3).uniform(-1.5, 1.5, L)              # the seed and the width of _g1_ringchi.py
cc, ci, cr = response(clean), response(imp), response(rnd)
dmu = 1e-4
low = clean.copy(); low[5] -= dmu                                # the onsite energy of site 5 lowered by delta mu
check('quiz 2, lowering the onsite energy of x by delta mu raises the density at x\' by chi(x,x\') delta mu',
      np.allclose((density(low) - density(clean)) / dmu, cc[5], atol=1e-4) and cc[5, 5] > 0,
      'largest difference %.1e' % np.abs((density(low) - density(clean)) / dmu - cc[5]).max())
check('quiz 2, the clean ring at mu = 0 is half filled', abs(density(clean).mean() - 0.5) < 1e-12, round(float(density(clean).mean()), 12))
check('quiz 2, clean ring, one value on each line parallel to the diagonal, 0.25/t on the diagonal',
      spread(cc) < 1e-8 and round(cc[0, 0], 2) == 0.25, ('%.1e' % spread(cc), round(float(cc[0, 0]), 4)))
row = cc[0, 1:11]
check('quiz 2, clean ring, the stripes alternate in sign and fade away from the diagonal',
      all(np.sign(row[k]) == (-1) ** (k + 1) for k in range(10)) and abs(row[9]) < abs(row[0]) / 3, np.round(row, 4))
check('quiz 2, impurity 2t at x = 20, chi(20,20) = 0.09/t and chi(0,0) = 0.25/t',
      round(ci[20, 20], 2) == 0.09 and round(ci[0, 0], 2) == 0.25, (round(float(ci[20, 20]), 4), round(float(ci[0, 0]), 4)))
far = max(abs(ci[x, (x + s) % L] - cc[0, s]) for x in (0, 1, 2, 38, 39) for s in (0, 1, 2, 38, 39))
near = max(abs(ci[x, (x + s) % L] - cc[0, s]) for x in (19, 20, 21) for s in (0, 1, 39))
check('quiz 2, impurity, the stripes break around x = 20 and stay close to the clean ones far from it',
      near > 0.15 and far < 0.01, 'difference to the clean ring near x = 20 %.3f, far from it %.4f' % (near, far))
check('quiz 2, random ring with w in [-1.5t, 1.5t], the color changes along the lines parallel to the diagonal',
      spread(cr) > 0.2 and np.ptp(np.diag(cr)) > 0.1, (round(float(spread(cr)), 3), round(float(np.ptp(np.diag(cr))), 3)))

# what the maps show: the parameters and the color scale of the figure helper, read without running it
helper = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                      'figures', 'session09', '_g1_ringchi.py')
par = {}
for node in ast.parse(open(helper, encoding='utf-8').read()).body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Tuple):
        par.update(zip([t.id for t in node.targets[0].elts], ast.literal_eval(node.value)))
check('quiz 2, the figure helper draws the same rings, and its color scale ends at +-0.1/t',
      (par['N'], par['MU'], par['T'], par['VMAX'], par['V_IMPURITY'], par['SITE_IMPURITY'], par['W_RANDOM'], par['SEED'])
      == (L, MU, T, 0.1, 2.0, 20, 1.5, 3), par)
VMAX = par['VMAX']
clip = {name: np.clip(c, -VMAX, VMAX) for name, c in (('clean', cc), ('impurity', ci), ('random', cr))}
dark = min(float(np.diag(c).min()) for c in clip.values()) / VMAX
check('quiz 2, the diagonal is dark red in all three maps, at least 0.85 of the end of the scale',
      dark > 0.85 and min(np.diag(c).min() for c in (cc, ci, cr)) > 0.085, round(dark, 3))
check('quiz 2, impurity, the stripes break on the row and the column of x = 20, nearly white next to the diagonal',
      abs(clip['impurity'][20, 21]) < 0.01 and abs(clip['impurity'][19, 20]) < 0.01 and abs(clip['clean'][0, 1]) > 0.06,
      (round(float(ci[20, 21]), 4), round(float(ci[19, 20]), 4), round(float(cc[0, 1]), 4)))
by_d = [np.ptp([clip['random'][x, (x + s) % L] for x in range(L)]) for s in range(L // 2 + 1)]
check('quiz 2, random ring, on the drawn scale the color changes along the lines next to the diagonal and not far from it',
      min(by_d[1:10]) > 0.02 and max(by_d[10:]) < 0.015, np.round(by_d, 3))
# ---------------------------------------------------------------------------------------------------------------
# the third bullet: a local change of temperature, measured as a change of temperature at another place, gives the
# thermal diffusivity D = kappa/C, with C the heat capacity per unit volume. Route 1, the heat equation C dT/dt = kappa d^2T/dx^2 on a chain by finite differences,
# for (kappa, C) = (1, 1), (2, 2) and (2, 1). Route 2, its Green's function, a Gaussian of variance 2 D t. The ratio of
# the change at x' to the change at x depends on kappa and C only through D, so a thermal conductance, which needs
# kappa alone, is not what this response gives.
def heat_profile(kappa, C, steps=4000, n=401, dt=0.05):
    T_ = np.zeros(n); T_[n // 2] = 1.0
    for _ in range(steps):
        T_ = T_ + dt * kappa / C * (np.roll(T_, 1) + np.roll(T_, -1) - 2 * T_)
    return T_


prof = {kc: heat_profile(*kc) for kc in ((1.0, 1.0), (2.0, 2.0), (2.0, 1.0))}
xs = np.arange(401) - 200
gauss = lambda D_, t_: np.exp(-xs ** 2 / (4 * D_ * t_)) / np.sqrt(4 * np.pi * D_ * t_)
ratio = lambda p_: p_[200 + 10] / p_[200]
check('third bullet: the same D = kappa/C gives the same response at x\' = x + 10, and another D does not',
      abs(ratio(prof[(1.0, 1.0)]) / ratio(prof[(2.0, 2.0)]) - 1) < 1e-12 and abs(ratio(prof[(2.0, 1.0)]) / ratio(prof[(1.0, 1.0)]) - 1) > 0.05,
      (round(ratio(prof[(1.0, 1.0)]), 4), round(ratio(prof[(2.0, 2.0)]), 4), round(ratio(prof[(2.0, 1.0)]), 4)))
check('third bullet: the response is the Gaussian of the diffusion with D = kappa/C, at t = 200 and for D = 1 and 2',
      np.abs(prof[(1.0, 1.0)] - gauss(1.0, 200.0)).max() < 1e-4 and np.abs(prof[(2.0, 1.0)] - gauss(2.0, 200.0)).max() < 1e-4,
      (float(np.abs(prof[(1.0, 1.0)] - gauss(1.0, 200.0)).max()), float(np.abs(prof[(2.0, 1.0)] - gauss(2.0, 200.0)).max())))
# the unit of D: kappa in W/(m K) over a heat capacity per unit volume, J/(m^3 K), is m^2/s, the unit of a diffusion
# constant, while over a heat capacity in J/K it is not. Exponents of (kg, m, s, K).
W_, J_ = np.array([1, 2, -3, 0]), np.array([1, 2, -2, 0])
m_, K_ = np.array([0, 1, 0, 0]), np.array([0, 0, 0, 1])
kappa_u, Cvol_u, Ctot_u = W_ - m_ - K_, J_ - 3 * m_ - K_, J_ - K_
check('third bullet: kappa over the heat capacity per unit volume has the unit m^2/s, and over the heat capacity in J/K not',
      np.array_equal(kappa_u - Cvol_u, [0, 2, -1, 0]) and not np.array_equal(kappa_u - Ctot_u, [0, 2, -1, 0]),
      ((kappa_u - Cvol_u).tolist(), (kappa_u - Ctot_u).tolist()))
print('all checks of page 01 hold')
