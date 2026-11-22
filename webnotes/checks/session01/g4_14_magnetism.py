"""Session 1, the numbers that page 14 (Sections 1.14 and 1.15, magnetism and superconductivity in mean field) quotes and
that no figure script asserts. One check script per page is the rule: every number of a caption, a feedback, a fold or
a solution is an assert, here or in the figure script that draws it. The figure afm_gap.py asserts the moment and the
gap of the half-filled chain from pyqula against the gap equation and a ring of 120 sites (0.03 at U = t, 0.62 and
1.86t at U = 3t, 0.94 at U = 8t), gauge_phase.py the factor -1 at phi = pi/2, and _g4_gauge.py the gauge
transformation in the Fock space for the picture quiz. This script checks the fold, the key box, the problem on the
mean-field dimer, the feedback of the quizzes and the try-it box, with numpy and by a second route where one exists.
The chain is (1.7) with the hopping -t. It writes no file."""
import numpy as np
from scipy import special, optimize

t = 1.0


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def modes(L):
    """Annihilation operators of L fermionic modes with the Jordan-Wigner signs, mode 0 the last Kronecker factor."""
    a, Z, I = np.array([[0., 1.], [0., 0.]]), np.diag([1., -1.]), np.eye(2)
    out = []
    for j in range(L):
        m = [I] * (L - 1 - j) + [a] + [Z] * j
        op = m[0]
        for x in m[1:]:
            op = np.kron(op, x)
        out.append(op)
    return out


def moment(U):
    """The moment of the half-filled chain in Hartree, 1 = (U/2)(1/pi) int dk / sqrt(D^2 + 4t^2 cos^2 k) with D = U m/2,
    with the complete elliptic integral K(p) of parameter p = 4t^2/(D^2 + 4t^2)."""
    f = lambda D: (U / 2) * (2 / np.pi) * special.ellipk(4 * t ** 2 / (D ** 2 + 4 * t ** 2)) / np.sqrt(D ** 2 + 4 * t ** 2) - 1
    return 2 * optimize.brentq(f, 1e-14, U) / U


def chain_map(U, m, nk=20001):
    """One pass of the Hartree loop of the half-filled chain, the new moment for the moment m."""
    k = np.linspace(-np.pi / 2, np.pi / 2, nk)
    D = U * m / 2
    return np.trapezoid(D / np.sqrt(D ** 2 + 4 * t ** 2 * np.cos(k) ** 2), k) / np.pi


# ------------------------------------------------------------------ the fold, from U n_up n_dn to the gap U m
for m in (0.3, 0.621):
    nu_A, nd_A = (1 + m) / 2, (1 - m) / 2
    up_A, dn_A = 1.0 * nd_A, 1.0 * nu_A                         # spin up feels U <n_dn>, spin down U <n_up>, at U = 1
    ok = np.isclose(up_A, 0.5 - m / 2) and np.isclose(dn_A, 0.5 + m / 2)
    check('m = %g: on sublattice A spin up feels U/2 - Um/2 and spin down U/2 + Um/2' % m, ok, (up_A, dn_A))
    # the decoupling on the four states of a site, U n_up n_dn -> U(<nu> n_dn + n_up <nd> - <nu><nd>), against its form
    nu_op = np.diag([0, 1, 0, 1.]); nd_op = np.diag([0, 0, 1, 1.])
    hf = nu_A * nd_op + nu_op * nd_A - nu_A * nd_A * np.eye(4)
    other = 0.5 * (nu_A + nd_A) * (nu_op + nd_op) - 0.5 * m * (nu_op - nd_op) - 0.25 * ((nu_A + nd_A) ** 2 - m ** 2) * np.eye(4)
    check('m = %g: the decoupling is (U/2)<n> n - (U/2) m (n_up - n_dn) - (U/4)(<n>^2 - m^2)' % m, np.allclose(hf, other), 'exact')
for U in (1.0, 3.0, 8.0):
    m = moment(U)
    k = np.linspace(-np.pi / 2, np.pi / 2, 4001)
    e = np.sqrt((U * m / 2) ** 2 + 4 * t ** 2 * np.cos(k) ** 2)
    check('U = %g: each spin has the bands U/2 -+ sqrt((Um/2)^2 + 4t^2 cos^2 k) and the gap U m' % U, np.isclose(2 * e.min(), U * m),
          (2 * e.min(), U * m))
    check('U = %g: the moment is a fixed point of the loop of the chain' % U, abs(chain_map(U, m) - m) < 1e-6, (m, chain_map(U, m)))
check('the gap is U m: 0.03t at U = t, 1.86t with m = 0.62 at U = 3t', abs(moment(1.0) - 0.0299) < 1e-4 and
      abs(1.0 * moment(1.0) - 0.03) < 1e-3 and abs(moment(3.0) - 0.621) < 1e-3 and abs(3 * moment(3.0) - 1.86) < 0.005,
      (moment(1.0), moment(3.0), 3 * moment(3.0)))
check('the gap approaches U at large U, m = 0.94 at U = 8t and 0.98 at 16t', abs(moment(8.0) - 0.939) < 1e-3 and
      abs(moment(16.0) - 0.984) < 1e-3, (moment(8.0), moment(16.0)))
check('at small U the moment is (16t/U) exp(-2 pi t/U)', abs(moment(1.0) - 16 * np.exp(-2 * np.pi)) < 2e-4,
      (moment(1.0), 16 * np.exp(-2 * np.pi)))
k = np.linspace(-np.pi, np.pi, 4001)
check('at U = 0 the chain has no gap, the band -2t cos k crosses zero at k = pi/2', np.min(np.abs(-2 * t * np.cos(k))) < 2e-3 and
      np.isclose(-2 * t * np.cos(np.pi / 2), 0), np.min(np.abs(-2 * t * np.cos(k))))


# ------------------------------------------------------------------ the problem, the mean-field dimer
def dimer_map(U, m):
    D = U * m / 2
    return D / np.sqrt(D ** 2 + t ** 2)


for U in (2.5, 4.0, 8.0):
    m = np.sqrt(1 - (2 * t / U) ** 2)
    check('U = %g: m = sqrt(1 - (2t/U)^2) is a fixed point of m -> (Um/2)/sqrt((Um/2)^2 + t^2)' % U,
          np.isclose(dimer_map(U, m), m), (m, dimer_map(U, m)))
    E = 2 * (U / 2 - np.sqrt((U * m / 2) ** 2 + t ** 2)) - U * 2 * (1 - m ** 2) / 4
    check('U = %g: the energy, two filled levels minus U sum <n_up><n_dn>, is -2t^2/U' % U, np.isclose(E, -2 * t ** 2 / U), E)
    lev = U / 2 + np.array([-1, 1]) * np.sqrt((U * m / 2) ** 2 + t ** 2)
    check('U = %g: the levels of each spin are 0 and U, so the gap is U' % U, np.allclose(lev, [0, U]), lev)
check('the slope of the map at m = 0 is U/2t, so a moment needs U > 2t', np.isclose(dimer_map(2.0, 1e-7) / 1e-7, 1.0, atol=1e-6)
      and dimer_map(1.9, 0.5) < 0.5 and dimer_map(2.1, 0.01) > 0.01, dimer_map(2.0, 1e-7) / 1e-7)
for U, mexp in ((1.5, 0.0), (4.0, 0.866)):
    m = 0.9
    for _ in range(5000):
        m = 0.5 * m + 0.5 * dimer_map(U, m)
    check('U = %g: the loop from m = 0.9 ends at %g' % (U, mexp), abs(m - mexp) < 1e-3, m)
check('the threshold belongs to the dimer: the half-filled chain has a moment for every U > 0, 0.03 at U = t',
      abs(moment(1.0) - 0.03) < 5e-4 and moment(0.8) > 0 and abs(chain_map(1.0, moment(1.0)) - moment(1.0)) < 1e-6
      and dimer_map(1.0, 0.03) < 0.03, (moment(1.0), moment(0.8)))
# the problem says one bond: (1.7) on a ring of two sites counts the bond twice, the hopping 2t, and the threshold
# moves to U = 4t, so the dimer of the problem is the open one, with -t in H_up
c1x, c2x = modes(2)
ring2 = -t * sum(c1x.T @ c2x + c2x.T @ c1x for _ in range(2))
dimer_2bonds = lambda U, m: (U * m / 2) / np.sqrt((U * m / 2) ** 2 + 4 * t ** 2)
check('a ring of two sites has the hopping 2t, levels -2t and 2t, and its threshold at U = 4t, not 2t',
      np.allclose(np.linalg.eigvalsh(ring2)[[0, 3]], [-2 * t, 2 * t]) and dimer_2bonds(3.9, 0.01) < 0.01
      and dimer_2bonds(4.1, 0.01) > 0.01 and dimer_map(2.1, 0.01) > 0.01, np.linalg.eigvalsh(ring2))
check('at U = 4t: m = 0.87, the mean-field energy -0.50t against the exact -0.83t',
      abs(np.sqrt(0.75) - 0.866) < 1e-3 and np.isclose(-2 / 4.0, -0.5) and abs(2 - np.sqrt(8) + 0.828) < 1e-3,
      (np.sqrt(0.75), -0.5, 2 - np.sqrt(8)))
# the try-it box: the dimer at U = 0 has the levels -t and +t, so the gap 2t
check('the dimer at U = 0 has the levels -t and t, the gap 2t', np.allclose(np.linalg.eigvalsh([[0, -t], [-t, 0]]), [-t, t]), 2 * t)

# ------------------------------------------------------------------ the quiz on U < 0
ms = np.linspace(-0.95, 0.95, 39)
ms = ms[np.abs(ms) > 1e-9]
check('U = -3t: the Hartree map of the chain has the opposite sign of m for every m, so m = 0 is the only fixed point',
      all(chain_map(-3.0, m) * m < 0 for m in ms), chain_map(-3.0, 0.5))
m = 0.5
for _ in range(2000):
    m = 0.5 * m + 0.5 * dimer_map(-4.0, m)
check('U = -4t: the loop of the dimer from m = 0.5 ends at m = 0', abs(m) < 1e-9, m)
# (1.7) on a ring of three sites: real, unchanged under c_up -> c_dn, c_dn -> -c_up, and S_z commutes
cs = modes(6)
up, dn = cs[0::2], cs[1::2]


def hubbard(U, up, dn):
    H = 0
    for i in range(3):
        j = (i + 1) % 3
        for c in (up, dn):
            H = H - t * (c[i].T @ c[j] + c[j].T @ c[i])
        H = H + U * (up[i].T @ up[i]) @ (dn[i].T @ dn[i])
    return H


Sz = 0.5 * sum(up[i].T @ up[i] - dn[i].T @ dn[i] for i in range(3))
for U in (4.0, -4.0):
    H = hubbard(U, up, dn)
    flipped = hubbard(U, dn, [-c for c in up])
    ok = np.allclose(H, H.conj()) and np.allclose(H, flipped) and np.allclose(H @ Sz, Sz @ H)
    check('U = %g: (1.7) on three sites is real, does not change when up and down are exchanged, and keeps S_z' % U, ok, 'exact')
    check('U = %g: the exchange of up and down changes the sign of the magnetization of a site' % U,
          np.allclose(dn[0].T @ dn[0] - up[0].T @ up[0], -(up[0].T @ up[0] - dn[0].T @ dn[0])), 'exact')

# ------------------------------------------------------------------ the gauge quizzes and the parity of a pairing term
check('each operator gets e^{i pi/2} = i at phi = pi/2, and the pair i^2 = -1', np.isclose(np.exp(1j * np.pi / 2), 1j) and
      np.isclose(np.exp(2j * np.pi / 2), -1), np.exp(2j * np.pi / 2))
check('the pair gets 1 only at multiples of pi, and i at phi = pi/4', np.isclose(np.exp(2j * 0), 1) and np.isclose(np.exp(2j * np.pi), 1)
      and np.isclose(np.exp(2j * np.pi / 4), 1j), np.exp(2j * np.pi / 4))
c1, c2 = modes(2)
N = c1.T @ c1 + c2.T @ c2
P = np.diag((-1.0) ** np.diag(N))
pair = -0.3 * N + 0.8 * (c1.T @ c2.T + c2 @ c1)
check('a pairing term keeps the parity (-1)^N and not N', np.allclose(pair @ P, P @ pair) and not np.allclose(pair @ N, N @ pair),
      'exact')
print('all checks of page 14 hold')
