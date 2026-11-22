"""Session 2, the numbers that page 11 (Section 2.11a, the Dirac cone of graphene) quotes and that no figure script
asserts. One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a lab box
is an assert, here or in the figure script that draws it. The figure scripts of the page assert their own numbers:
graphene_path.py (the energies at Gamma, K and M, the range -3t to 3t, the slope 3/2 at K), g4_graphene_dos.py (the
peaks at +-t, the value 0.04 at zero energy, the area), dirac_mass.py (the gap 2m) and _g4_bands.py (the gap 1.0 of the
sublattice imbalance 0.5 and the band of the triangular lattice). This script checks the fold, the solution of the
problem and the feedback of the quizzes, each by a second route where the conventions sheet does not have the number.
The frame is the one of the sheet, with the bond length a = 1 and delta_1 along x. It finds the repository from its own
path and writes no file, since pyqula runs in a temporary folder."""
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
import physcheck  # noqa: E402

S3 = np.sqrt(3.0)


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# the frame of the fold and of the figure graphene_path, a = t = 1
delta = np.array([[1.0, 0.0], [-0.5, S3 / 2], [-0.5, -S3 / 2]])
K = np.array([2 * np.pi / 3, 2 * np.pi / (3 * S3)])
M = np.array([2 * np.pi / 3, 0.0])


def f(k, t=1.0):
    return t * np.exp(1j * (np.asarray(k) @ delta.T)).sum(-1)


# the fold: the three phases at K and their sum
phases = K @ delta.T
check('phases K.delta_j, the fold says 2 pi/3, 0, -2 pi/3', np.allclose(phases, [2 * np.pi / 3, 0, -2 * np.pi / 3]),
      np.round(phases / np.pi, 6))
check('f(K) = t (1 + 2 cos 2 pi/3) = 0', abs(f(K)) < 1e-12 and abs(1 + 2 * np.cos(2 * np.pi / 3)) < 1e-12, abs(f(K)))
check('|K| = 4 pi/3 sqrt3 is a corner, the same distance as the other corners', abs(np.linalg.norm(K) - 4 * np.pi / (3 * S3)) < 1e-12,
      round(np.linalg.norm(K), 4))


def linear(q, k0):
    """The linear term of the fold, i t sum_j (q.delta_j) exp(i k0.delta_j), with t = 1."""
    return 1j * ((delta @ q) * np.exp(1j * (delta @ k0))).sum()


# the simplest case, q along x: i t q a (e^{2 pi i/3} - 1/2 - e^{-2 pi i/3}/2) = i t q a (-3/4 + 3 sqrt3 i/4)
c = np.exp(2j * np.pi / 3) - 0.5 - 0.5 * np.exp(-2j * np.pi / 3)
check('q along x, the bracket is -3/4 + 3 sqrt3 i/4', abs(c - (-0.75 + 0.75j * S3)) < 1e-12, np.round(c, 6))
check('q along x, the linear term is i q times the bracket', abs(linear(np.array([1.0, 0.0]), K) - 1j * c) < 1e-12,
      np.round(linear(np.array([1.0, 0.0]), K), 6))
check('q along x, the modulus is 3/2 times q', abs(abs(1j * c) - 1.5) < 1e-12, abs(1j * c))

# a general direction: f(K+q) = (3/2) e^{-5 pi i/6} (q_x - i q_y), and at K' = -K (3/2) e^{-i pi/6} (q_x + i q_y)
rng = np.random.default_rng(1)
for q in rng.normal(size=(5, 2)):
    lk = linear(q, K)
    lkp = linear(q, -K)
    ok = abs(lk - 1.5 * np.exp(-5j * np.pi / 6) * (q[0] - 1j * q[1])) < 1e-12
    ok &= abs(lkp - 1.5 * np.exp(-1j * np.pi / 6) * (q[0] + 1j * q[1])) < 1e-12
    # second route: the expansion against f itself, for a small q the error is of order q^2
    s = 1e-5 * q
    ok &= abs(f(K + s) - 1.5 * np.exp(-5j * np.pi / 6) * (s[0] - 1j * s[1])) < 1e-9
    ok &= abs(f(-K + s) - 1.5 * np.exp(-1j * np.pi / 6) * (s[0] + 1j * s[1])) < 1e-9
    check('f(K+q) and f(K\'+q) of the fold at q = (%.2f, %.2f)' % tuple(q), ok, np.round([lk, lkp], 4))

# the phase of the B orbital: |B'> = e^{5 pi i/6} |B> turns the linear H at K into (3/2)(q_x sigma_x + q_y sigma_y),
# and at K' the same phase choice of that valley, e^{i pi/6}, gives (3/2)(q_x sigma_x - q_y sigma_y)
sx = np.array([[0, 1], [1, 0]], complex); sy = np.array([[0, -1j], [1j, 0]])
for kk, beta, lam in ((K, 5 * np.pi / 6, 1), (-K, np.pi / 6, -1)):
    q = np.array([0.3, -0.7])
    fl = linear(q, kk)
    H = np.array([[0, fl], [np.conj(fl), 0]])
    U = np.diag([1, np.exp(1j * beta)])
    Hn = U.conj().T @ H @ U
    target = 1.5 * (q[0] * sx + lam * q[1] * sy)
    check('Dirac form at %s with the phase %.0f degrees on B, sign of sigma_y %+d' % ('K' if lam > 0 else "K'", np.degrees(beta), lam),
          np.allclose(Hn, target), np.round(Hn[0, 1], 6))
    check('the energies are the same, +-(3/2)|q|', np.allclose(np.linalg.eigvalsh(H), [-1.5 * np.linalg.norm(q), 1.5 * np.linalg.norm(q)]),
          np.round(np.linalg.eigvalsh(H), 6))

# the problem: |f| at Gamma and at M, the phases at M, and the range of the bands
check('|f(Gamma)| = 3t', abs(abs(f([0.0, 0.0])) - 3) < 1e-12, abs(f([0.0, 0.0])))
check('phases M.delta_j, the solution says 2 pi/3, -pi/3, -pi/3', np.allclose(M @ delta.T, [2 * np.pi / 3, -np.pi / 3, -np.pi / 3]),
      np.round(M @ delta.T / np.pi, 6))
check('f(M) = t (1/2 - sqrt3 i/2), the solution', abs(f(M) - (0.5 - 0.5j * S3)) < 1e-12, np.round(f(M), 6))
check('|f(M)| = t', abs(abs(f(M)) - 1) < 1e-12, abs(f(M)))
mesh = np.array([i * 2 * np.pi * np.array([1 / 3, 1 / S3]) / 90 + j * 2 * np.pi * np.array([-1 / 3, 1 / S3]) / 90
                 for i in range(90) for j in range(90)])
check('max |f| over the zone is 3t, so the bands span -3t to 3t', abs(np.abs(f(mesh)).max() - 3) < 1e-12,
      np.abs(f(mesh)).max())
# M is a saddle point of |f|: zero gradient, curvatures of opposite sign
h = 1e-4
e = lambda k: abs(f(k))
grad = [(e(M + h * u) - e(M - h * u)) / (2 * h) for u in np.eye(2)]
curv = [(e(M + h * u) - 2 * e(M) + e(M - h * u)) / h ** 2 for u in np.eye(2)]
check('M is a saddle point of the upper band, gradient 0, curvatures 4.5 along x and -1.5 along y as on the sheet',
      np.allclose(grad, 0, atol=1e-6) and abs(curv[0] - 4.5) < 1e-3 and abs(curv[1] + 1.5) < 1e-3, np.round(curv, 4))

# second route for the density of states: the states with |E| < 0.2 on a fine mesh against the two cones,
# whose density per cell is 2|E|/(sqrt3 pi t^2), so that the integral from -0.2 to 0.2 is 0.0147
n = 1200
u = (np.arange(n) + 0.5) / n
B = 2 * np.pi * np.array([[1 / 3, 1 / S3], [-1 / 3, 1 / S3]])
ks = u[:, None, None] * B[0] + u[None, :, None] * B[1]
E = np.abs(f(ks.reshape(-1, 2)))
count = 2 * np.mean(E < 0.2)                    # two bands, +-|f|, each with weight one state per cell
cone = 2 / (S3 * np.pi) * 0.2 ** 2
check('states per cell with |E| < 0.2, count against the two cones 0.0147', abs(count - cone) / cone < 0.03,
      (round(count, 5), round(cone, 5)))
hist, edges = np.histogram(np.concatenate([E, -E]), bins=np.linspace(-3, 3, 241))
centers = (edges[1:] + edges[:-1]) / 2
peaks = sorted(centers[np.argsort(hist)[-2:]])
check('the histogram of the bands peaks at +-t, the saddle points', np.allclose(peaks, [-1, 1], atol=0.02), np.round(peaks, 3))

# pyqula writes files, so it runs in a temporary folder
os.chdir(tempfile.mkdtemp())
from pyqula import geometry  # noqa: E402

g = geometry.honeycomb_lattice()
A = np.array([g.a1[:2], g.a2[:2]])
Kp = K  # the K of the notes in the frame of pyqula, as the sheet says


def slope(h, k0):
    hk = h.get_hk_gen()
    out = []
    for th in np.linspace(0, 2 * np.pi, 5)[:-1]:
        q = 1e-5 * np.array([np.cos(th), np.sin(th)])
        kr = A @ (k0 + q) / (2 * np.pi)
        out.append(np.linalg.eigvalsh(hk([kr[0], kr[1], 0.]))[1] / 1e-5)
    return np.array(out)


s1 = slope(g.get_hamiltonian(has_spin=False), Kp)
s2 = slope(g.get_hamiltonian(has_spin=False, tij=[2.0]), Kp)
check('pyqula, the slope at K is 3/2 for t = 1', np.allclose(s1, 1.5, atol=1e-4), np.round(s1, 5))
check('pyqula, the slope at K is 3 for t = 2, the cone twice as steep', np.allclose(s2, 3.0, atol=1e-4), np.round(s2, 5))
hk2 = g.get_hamiltonian(has_spin=False, tij=[2.0]).get_hk_gen()
kr = A @ Kp / (2 * np.pi)
check('pyqula, for t = 2 the bands still touch at the same K', np.abs(np.linalg.eigvalsh(hk2([kr[0], kr[1], 0.]))).max() < 1e-9,
      np.linalg.eigvalsh(hk2([kr[0], kr[1], 0.])))
check('the same K for t = 2 from f, f(K) = 0', abs(f(K, t=2.0)) < 1e-12, abs(f(K, t=2.0)))
h = g.get_hamiltonian(has_spin=False)
h.add_sublattice_imbalance(0.5)
hk, Bq = physcheck.from_pyqula(h)
ek = np.linalg.eigvalsh(hk(Kp))
check('pyqula, the sublattice imbalance 0.5 gives +-0.5 at K, the gap 1.0, since f(K) = 0', np.allclose(ek, [-0.5, 0.5]), ek)
check('the gap of the imbalance 0.5 over the zone is 1.0, at K', abs(physcheck.gap(hk, Bq, 1, nk=60) - 1.0) < 1e-9,
      round(physcheck.gap(hk, Bq, 1, nk=60), 6))
# the old text, corrected on 2026-11-22 to "The massless cone is the low-energy physics of graphene, and of every
# honeycomb monolayer whose Fermi level sits at K and K'. This holds as long as no term, such as a sublattice
# imbalance, opens a gap there." First condition, no gap: without the imbalance both corners have zero energy and the
# cone, with it neither corner is gapless, so a honeycomb lattice alone does not give the cone
h0 = g.get_hamiltonian(has_spin=False)
hk0, _ = physcheck.from_pyqula(h0)
e_pair = [np.abs(np.linalg.eigvalsh(hk0(kk))).max() for kk in (Kp, -Kp)] + [np.abs(np.linalg.eigvalsh(hk(kk))).min() for kk in (Kp, -Kp)]
check('pyqula honeycomb: 0 at K and K\' without the imbalance, +-0.5 at both with the imbalance 0.5',
      max(e_pair[:2]) < 1e-9 and np.allclose(e_pair[2:], 0.5), np.round(e_pair, 9))
# Second condition, one layer: a Bernal (AB) stack of two layers, with the interlayer hopping 0.14 t from B of the
# first layer to A of the second, has zero energy at K and no gap, but its lowest band grows as q^2 and not as q.
# Route 1 is the ratio E(2q)/E(q), which is 2 for one layer. Route 2 is the two-band form E = (3q/2)^2/0.14.
def bilayer(k, g1=0.14):
    fk = f(k)
    hb = np.zeros((4, 4), complex)
    hb[0, 1], hb[2, 3], hb[1, 2] = fk, fk, g1
    return np.linalg.eigvalsh(hb + hb.conj().T)


qb = 0.005
eb1, eb2 = np.abs(bilayer(K + [qb, 0])).min(), np.abs(bilayer(K + [2 * qb, 0])).min()
em1, em2 = np.abs(np.linalg.eigvalsh(hk0(K + [qb, 0]))).min(), np.abs(np.linalg.eigvalsh(hk0(K + [2 * qb, 0]))).min()
check('the Bernal bilayer with 0.14 t: 0 at K, E(2q)/E(q) about 4 against 2 for one layer, and E = (1.5 q)^2/0.14',
      np.abs(bilayer(K)).min() < 1e-12 and 3.9 < eb2 / eb1 < 4.0 and abs(em2 / em1 - 2) < 1e-3
      and abs(eb1 / ((1.5 * qb) ** 2 / 0.14) - 1) < 0.01, (round(eb2 / eb1, 3), round(em2 / em1, 4)))
# Third condition, the Fermi level at K: one layer with a real second-neighbor hopping t2 keeps the touching at K, at
# the energy -3 t2, since the six second neighbors give t2 (|f|^2 - 3). Above t2 = t/3 the lower band at Gamma,
# -3t + 6 t2, rises above the touching, and the Fermi level of half filling leaves it. Route 1 is the sum over the six
# second neighbors, route 2 the closed form, and the Fermi level is the median of the levels on a 300 x 300 mesh.
bvec = np.array([delta[i] - delta[j] for i in range(3) for j in range(3) if i != j])
nm = 300
b1, b2 = 2 * np.pi * np.array([1 / 3, 1 / S3]), 2 * np.pi * np.array([1 / 3, -1 / S3])
km = (((np.arange(nm) + 0.5) / nm)[:, None, None] * b1 + ((np.arange(nm) + 0.5) / nm)[None, :, None] * b2).reshape(-1, 2)
fm = f(km)
s2n = np.exp(1j * km @ bvec.T).sum(-1).real
efs = {}
for t2 in (0.1, 0.25, 0.4):
    lev = np.sort(np.concatenate([t2 * s2n + np.abs(fm), t2 * s2n - np.abs(fm)]))
    efs[t2] = 0.5 * (lev[lev.size // 2 - 1] + lev[lev.size // 2])
check('second-neighbor t2: the six neighbors give |f|^2 - 3, the touching at K is at -3 t2, and the Fermi level of half '
      'filling sits there for t2 = 0.1 and 0.25 but is about -0.744 for t2 = 0.4, against the touching at -1.2',
      np.allclose(s2n, np.abs(fm) ** 2 - 3) and abs(np.exp(1j * bvec @ K).sum().real + 3) < 1e-12
      and abs(efs[0.1] + 0.3) < 0.01 and abs(efs[0.25] + 0.75) < 0.01 and abs(efs[0.4] + 0.744) < 0.01,
      {k_: round(v_, 4) for k_, v_ in efs.items()})

# the triangular lattice of the third picture, by the formula -2t sum cos(k.a), a1 = (1,0), a2 = (-1/2, sqrt3/2)
a_t = np.array([[1.0, 0.0], [-0.5, S3 / 2], [0.5, S3 / 2]])
band_t = lambda k: -2 * np.cos(np.asarray(k) @ a_t.T).sum(-1)
Kt, Mt = np.array([2 * np.pi / 3, 2 * np.pi / S3]), np.array([np.pi, np.pi / S3])
check('triangular, -6t at Gamma, 3t at K, 2t at M', np.allclose([band_t([0, 0]), band_t(Kt), band_t(Mt)], [-6, 3, 2]),
      np.round([band_t([0, 0]), band_t(Kt), band_t(Mt)], 6))
check('triangular, |K| = 4 pi/3 and |M| = 2 pi/sqrt3', np.isclose(np.linalg.norm(Kt), 4 * np.pi / 3) and np.isclose(np.linalg.norm(Mt), 2 * np.pi / S3),
      np.round([np.linalg.norm(Kt), np.linalg.norm(Mt)], 4))

# ---- added after the physics check of the group, findings c1, c4, c5, c6, c7 and the numbers with no assert ----

# the problem: the bands span -3t to 3t, a width of 6t
check('the width of the two bands, 2 max|f| = 6t', abs(2 * np.abs(f(mesh)).max() - 6) < 1e-12, 2 * np.abs(f(mesh)).max())

# c1, the quiz on the word massless: for the cone E = hbar v_F |q| the formula 1/m = d^2E/dq^2 gives 0 along q and
# v_F/|q| across q, so m = hbar |q|/v_F across q, which goes to zero at the tip. On the lattice band |f| at |q| = 0.01
# the curvature across q is close to v_F/|q| = 150 and the curvature along q is small, the trigonal warping, and the
# second difference through the tip grows as 2 v_F/s, so the formula is not defined at the tip.
vF, qq, hh = 1.5, 0.01, 1e-4
cross, along = [], []
for th in np.linspace(0, 2 * np.pi, 72, endpoint=False):
    u = np.array([np.cos(th), np.sin(th)]); w = np.array([-np.sin(th), np.cos(th)])
    p = K + qq * u
    along.append((abs(f(p + hh * u)) - 2 * abs(f(p)) + abs(f(p - hh * u))) / hh ** 2)
    cross.append((abs(f(p + hh * w)) - 2 * abs(f(p)) + abs(f(p - hh * w))) / hh ** 2)
check('curvature of |f| across q at |q| = 0.01, 147 to 153 around v_F/|q| = 150', min(cross) > 147 and max(cross) < 153,
      (round(min(cross), 2), round(max(cross), 2)))
check('curvature of |f| along q at |q| = 0.01 is small, -0.76 to 0.74', min(along) > -0.8 and max(along) < 0.8,
      (round(min(along), 3), round(max(along), 3)))
tip = [(abs(f(K + s * np.array([1.0, 0]))) - 2 * abs(f(K)) + abs(f(K - s * np.array([1.0, 0])))) / s ** 2 for s in (1e-2, 1e-3, 1e-4)]
check('second difference through the tip, 2 v_F/s = 300, 3000, 30000, so not defined at the tip',
      np.allclose(tip, [2 * vF / s for s in (1e-2, 1e-3, 1e-4)], rtol=0.01), np.round(tip, 1))
qv = np.array([0.02, 0.0])
cone = lambda q: vF * np.linalg.norm(q)
cross_cone = (cone(qv + [0, hh]) - 2 * cone(qv) + cone(qv - [0, hh])) / hh ** 2
check('the cone itself, mass across q is |q|/v_F (hbar = 1)', abs(1 / cross_cone - np.linalg.norm(qv) / vF) < 1e-6,
      round(1 / cross_cone, 6))

# c4, the phase on B at K': with e^{i pi/6} the form is q_x sigma_x - q_y sigma_y, with the phase e^{5 pi i/6} of K the
# entry is (3/2) e^{2 pi i/3} (q_x + i q_y), and no constant phase gives the form q_x sigma_x + q_y sigma_y of K
q = np.array([0.3, -0.7])
fl = linear(q, -K)
check("at K' with the phase e^{5 pi i/6} of K the entry is (3/2) e^{2 pi i/3} (q_x + i q_y)",
      abs(fl * np.exp(5j * np.pi / 6) - 1.5 * np.exp(2j * np.pi / 3) * (q[0] + 1j * q[1])) < 1e-12, np.round(fl * np.exp(5j * np.pi / 6), 6))
dirs = np.array([[np.cos(a), np.sin(a)] for a in np.linspace(0, np.pi, 37)])          # unit q in many directions
lin = np.array([linear(v, -K) for v in dirs])
worst = [np.abs(lin * np.exp(1j * b) - 1.5 * (dirs[:, 0] - 1j * dirs[:, 1])).max() for b in np.linspace(0, 2 * np.pi, 721)]
check("at K' no constant phase on B gives the form of K for every direction of q, the mismatch stays 3|q|",
      min(worst) > 2.99, round(min(worst), 4))

# c6, the frame of Figure 2.5, read from its Blender script: delta_1 along y, K on the k_x axis. A turn by 90 degrees
# takes the frame of the fold to it, with our delta_2 on its delta_3 and our delta_3 on its delta_2, and the bands agree.
import math  # noqa: E402
import re  # noqa: E402
src = open(os.path.join(HERE, '..', '..', '..', 'lecture_notes', 'src', 'figures', 'blender', 's02f04_dirac.py')).read()
ns = {'S3': S3, 'math': math, '__builtins__': {}}
fig_delta = np.array(eval(re.search(r'^DELTA = (.*)$', src, re.M).group(1), ns))
fig_a = np.array(eval(re.search(r'^A1, A2 = (.*)$', src, re.M).group(1), ns))
fig_K = np.array(eval(re.search(r'^\s*K = (\(4 \* math\.pi.*\))$', src, re.M).group(1), ns))
R90 = np.array([[0.0, -1.0], [1.0, 0.0]])
check('Figure 2.5 has delta_1 along +y and K = (4 pi/3 sqrt3, 0) on the k_x axis',
      np.allclose(fig_delta[0], [0, 1]) and np.allclose(fig_K, [4 * np.pi / (3 * S3), 0]), (fig_delta[0], np.round(fig_K, 4)))
check('the turn by 90 degrees takes our delta_1, delta_2, delta_3 to its delta_1, delta_3, delta_2',
      np.allclose(delta @ R90.T, fig_delta[[0, 2, 1]]), np.round(delta @ R90.T, 4))
f_fig = lambda k: np.exp(1j * (np.asarray(k) @ fig_delta.T)).sum(-1)
G = fig_K - R90 @ K
check('its K minus our turned K is a reciprocal vector of its lattice, so the same valley',
      np.allclose(np.exp(1j * (fig_a @ G)), 1), np.round(fig_a @ G / (2 * np.pi), 6))
check('f vanishes at the K of the figure', abs(f_fig(fig_K)) < 1e-12, abs(f_fig(fig_K)))
ks = rng.uniform(-4, 4, size=(20, 2))
check('the bands |f| are the same in the two frames at 20 momenta', np.allclose(np.abs(f(ks)), np.abs(f_fig(ks @ R90.T))), 20)

# c5 and the caption of g4_graphene_dos, run in --verify: the pyqula script of the figure gives 0.04 at zero energy,
# the V rounded by the broadening, the peaks at +-t, no states beyond +-3t but the tails, two states per cell
sys.dont_write_bytecode = True                                     # the check writes no file
os.environ.setdefault('MPLBACKEND', 'Agg')
import style  # noqa: E402
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures', 'session02'))
import _g4_bands  # noqa: E402
d = style.run_script('session02/g4_graphene_dos.py')
e, dos = np.array(d['e']), np.array(d['dos'])
i0 = np.argmin(np.abs(e))
check('graphene dos at zero energy, about 0.04 per cell and per t, the minimum of the V',
      abs(dos[i0] - 0.04) < 0.002 and dos[i0] == dos[np.abs(e) < 0.5].min(), round(dos[i0], 4))
ip, im = np.argmax(np.where(e > 0, dos, 0)), np.argmax(np.where(e < 0, dos, 0))
check('graphene dos, the peaks at +-t', abs(e[ip] - 1) < 0.015 and abs(e[im] + 1) < 0.015, (round(e[im], 3), round(e[ip], 3)))
check('graphene dos, only the tails beyond +-3t, and two states per cell less the tails',
      dos[np.abs(e) > 3.2].max() < 0.02 and abs(d['states'] - 1.98) < 0.01, round(d['states'], 4))
# second route for the 0.04: the Lorentzian sum of half width 0.04 over the bands +-|f| on 200 x 200 momenta
u = np.arange(200) / 200
kk = (u[:, None, None] * B[0] + u[None, :, None] * B[1]).reshape(-1, 2)
Eb = np.abs(f(kk))
lor = 2 * np.mean(0.04 / np.pi / (Eb ** 2 + 0.04 ** 2))
check('the Lorentzian sum by numpy at zero energy agrees with pyqula', abs(lor - dos[i0]) < 1e-3, round(lor, 4))

# the picture quiz on three band structures, run in --verify: the asserts of _g4_bands.check_graphene
d = style.run_script('session02/g4_graphene_bands.py')
iK, iM = _g4_bands.check_graphene(d)
b, bi, bt = d['bands'], d['bands_imbalance'], d['band_triangular']
check('quiz pictures, graphene +-3t at Gamma, 0 at K, +-t at M', np.allclose([b[0], b[iK], b[iM]], [[-3, 3], [0, 0], [-1, 1]], atol=1e-9),
      np.round([b[0], b[iK], b[iM]], 6).tolist())
check('quiz pictures, the imbalance 0.5 gives +-0.5 at K, the gap 1.0t', np.allclose(bi[iK], [-0.5, 0.5]), np.round(bi[iK], 6))
check('quiz pictures, the triangular band from -6t at Gamma to 3t at K', np.isclose(bt[0], -6) and np.isclose(bt[iK], 3), (bt[0], bt[iK]))

# c7 and the lab box: the words of the box are in the stored arXiv abstract of elias2011, which the tracked file keeps whole
text = ' '.join(open(os.path.join(HERE, '..', '..', 'sources', 'session02', 'elias2011_nphys2049.txt'), encoding='utf-8').read().split())
for phrase in ('carrier concentrations n varying over three orders of magnitude', 'measurements of the cyclotron mass',
               'upper limit of ~0.1 meV on the possible gap', 'In contrast to the single-particle picture, the real spectrum of graphene is profoundly nonlinear',
               'three times the value commonly used for graphene', 'attributed to electron-electron interaction',
               'in suspended graphene'):
    check('lab box elias2011, the source says "%s"' % phrase, phrase in text, 'found')

# the turned frame of Figure 2.5: our K = (2 pi/3a, 2 pi/3 sqrt3 a) turned by +90 degrees is (-2 pi/3 sqrt3 a, 2 pi/3a), and the
# corner (4 pi/3 sqrt3 a, 0) of the figure differs from it by a reciprocal vector of the turned lattice (a = 1)
Kt = np.array([-2 * np.pi / (3 * S3), 2 * np.pi / 3])
check('our K turned by 90 degrees', np.allclose(Kt, [[0, -1], [1, 0]] @ np.array([2 * np.pi / 3, 2 * np.pi / (3 * S3)])), Kt.round(4))
Bt = [[0, -1], [1, 0]] @ (2 * np.pi / 3 * np.array([[1, 1], [S3, -S3]]))      # the columns are b1 and b2 turned
d = np.linalg.solve(Bt, np.array([4 * np.pi / (3 * S3), 0]) - Kt)
check('the corner of the figure minus our turned K is a reciprocal vector', np.allclose(d, np.round(d)), d.round(6))
