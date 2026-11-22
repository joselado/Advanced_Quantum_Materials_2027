"""Session 1, the numbers that page 12 (Section 1.12, the general interacting Hamiltonian and mean field) quotes and
that no figure script asserts. One check script per page is the rule: every number of a caption, a feedback, a fold
or a solution is an assert, here or in the figure script that draws it. The figure dimer_meanfield.py asserts that
mean field stays above the exact energy, that the moment appears at U = 2t and the energy -2t + U/2 below it, and the
closed form of the exact energy. This script checks the problem on the exact Hubbard dimer, the caption of the dimer
figure, the fold on the mean-field decoupling and the feedback of the two quizzes, with numpy in the Fock space and
with pyqula for the mean-field dimer. The Hamiltonian of the dimer is (1.7) on two sites, with the hopping -t. It
finds the repository from its own path and writes no file, since pyqula runs in a temporary folder."""
import contextlib
import io
import os
import tempfile

import numpy as np
from scipy import special, optimize

HERE = os.path.dirname(os.path.abspath(__file__))
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


# the dimer, modes 1up, 1dn, 2up, 2dn
c1u, c1d, c2u, c2d = modes(4)
vac = np.zeros(16); vac[0] = 1.0
n = lambda c: c.T @ c
hop = -t * sum(x.T @ y + y.T @ x for x, y in ((c1u, c2u), (c1d, c2d)))
H = lambda U: hop + U * (n(c1u) @ n(c1d) + n(c2u) @ n(c2d))
for x in (c1u, c1d, c2u, c2d):
    assert np.allclose(x @ x.T + x.T @ x, np.eye(16))

# ------------------------------------------------------------------ the problem, the exact dimer with S_z = 0
a = c1u.T @ c2d.T @ vac          # one electron on each site
b = c1d.T @ c2u.T @ vac
c = c1u.T @ c1d.T @ vac          # both on site 1
dd = c2u.T @ c2d.T @ vac         # both on site 2
four = np.array([a, b, c, dd])
check('the four states are orthonormal', np.allclose(four @ four.T, np.eye(4)), 4)
Ntot = sum(n(x) for x in (c1u, c1d, c2u, c2d))
Sz = 0.5 * (n(c1u) - n(c1d) + n(c2u) - n(c2d))
two0 = [s for s in range(16) if np.isclose(Ntot[s, s], 2) and np.isclose(Sz[s, s], 0)]
check('two electrons with S_z = 0 have four states', len(two0) == 4, len(two0))
U = 4.0
h4 = four @ H(U) @ four.T
check('hopping matrix elements of the solution, <c|H|a> = <d|H|a> = -t, <c|H|b> = <d|H|b> = +t',
      np.allclose(h4[2:, :2], [[-t, t], [-t, t]]), h4[2:, :2].tolist())
check('diagonal 0, 0, U, U', np.allclose(np.diag(h4), [0, 0, U, U]), np.diag(h4).tolist())
S = (a - b) / np.sqrt(2); T0 = (a + b) / np.sqrt(2); Dp = (c + dd) / np.sqrt(2); Dm = (c - dd) / np.sqrt(2)
check('<D+|H|S> = -2t, the only coupling of the singlet', np.isclose(Dp @ H(U) @ S, -2 * t) and np.isclose(Dm @ H(U) @ S, 0),
      Dp @ H(U) @ S)
check('(a+b)/sqrt2 is an eigenstate at 0 and (c-d)/sqrt2 at U', np.allclose(H(U) @ T0, 0) and np.allclose(H(U) @ Dm, U * Dm), U)
# total spin of the two combinations of one electron per site, S^2 = S_z^2 + (S+S- + S-S+)/2
Sp = c1u.T @ c1d + c2u.T @ c2d
S2 = Sz @ Sz + 0.5 * (Sp @ Sp.T + Sp.T @ Sp)
check('(a-b)/sqrt2 is the singlet and (a+b)/sqrt2 the triplet', np.isclose(S @ S2 @ S, 0) and np.isclose(T0 @ S2 @ T0, 2),
      (S @ S2 @ S, T0 @ S2 @ T0))
E0 = lambda U: U / 2 - np.sqrt(U ** 2 / 4 + 4 * t ** 2)
for U in (0.0, 1.0, 4.0, 10.0):
    block = np.array([[0, -2 * t], [-2 * t, U]])
    Hn2 = H(U)[np.ix_(two0, two0)]
    ok = np.isclose(np.linalg.eigvalsh(block)[0], E0(U)) and np.isclose(np.linalg.eigvalsh(Hn2)[0], E0(U))
    N2 = [s for s in range(16) if np.isclose(Ntot[s, s], 2)]
    ok &= np.isclose(np.linalg.eigvalsh(H(U)[np.ix_(N2, N2)])[0], E0(U))
    check('E0 = U/2 - sqrt(U^2/4 + 4t^2) at U = %g, also the lowest of all six states with two electrons' % U, ok, E0(U))
check('E0 = -0.83t at U = 4t', abs(E0(4.0) + 0.83) < 0.005 and np.isclose(E0(4.0), 2 - 2 * np.sqrt(2)), E0(4.0))
check('at large U, E0 goes as -4t^2/U, 0.998 of it at U = 40t', abs(E0(40.0) / (-4 / 40.0) - 0.998) < 5e-4, E0(40.0) / (-0.1))
check('the expansion sqrt(U^2/4 + 4t^2) = U/2 + 4t^2/U + O(t^4/U^3)',
      abs(np.sqrt(100 ** 2 / 4 + 4) - 50 - 4 / 100) < 2e-5, np.sqrt(100 ** 2 / 4 + 4) - 50 - 4 / 100)


# ------------------------------------------------------------------ the mean-field dimer of the caption and the quiz
def meanfield(U, m=0.9, it=20000):
    """Antiferromagnetic mean field of the dimer, n_1up = (1+m)/2, n_1dn = (1-m)/2 and the opposite on site 2."""
    for _ in range(it):
        nu = np.array([(1 + m) / 2, (1 - m) / 2]); nd = 1 - nu
        eu, vu = np.linalg.eigh(np.array([[U * nd[0], -t], [-t, U * nd[1]]]))
        ed, vd = np.linalg.eigh(np.array([[U * nu[0], -t], [-t, U * nu[1]]]))
        mn = vu[0, 0] ** 2 - vu[1, 0] ** 2
        if abs(mn - m) < 1e-14:
            break
        m = 0.5 * m + 0.5 * mn
    nu = np.array([(1 + m) / 2, (1 - m) / 2]); nd = 1 - nu
    return abs(m), eu[0] + ed[0], U * np.sum(nu * nd), vu[:, 0], vd[:, 0]


for U in (2.5, 3.0, 4.0, 8.0):
    m, levels, dc, _, _ = meanfield(U)
    check('mean-field energy -2t^2/U at U = %g, for every U > 2t' % U, abs(levels - dc + 2 * t ** 2 / U) < 1e-9, levels - dc)
m40, l40, dc40, _, _ = meanfield(40.0)
check('at large U mean field gains half of the exact energy', abs((l40 - dc40) / E0(40.0) - 0.5) < 2e-3, (l40 - dc40) / E0(40.0))
check('the moment is zero up to U = 2t', meanfield(1.9)[0] < 1e-6 and meanfield(2.2)[0] > 0.3, (meanfield(1.9)[0], meanfield(2.2)[0]))
# the quiz with equations as options, at U = 4t
m, levels, dc, vu, vd = meanfield(4.0)
check('m = 0.866 on the dimer at U = 4t, 0.87 as the quiz quotes it', abs(m - np.sqrt(0.75)) < 1e-9 and abs(m - 0.87) < 0.005, m)
check('the filled levels sum to 0 at U = 4t', abs(levels) < 1e-9, levels)
check('U sum_i <n_i up><n_i dn> = 0.5t at U = 4t', abs(dc - 0.5) < 1e-9, dc)
slater = (vu[0] * c1u.T + vu[1] * c2u.T) @ (vd[0] * c1d.T + vd[1] * c2d.T) @ vac
check('<H> of the Slater determinant in the Fock space is -0.5t, the levels minus the double counting',
      abs(slater @ H(4.0) @ slater + 0.5) < 1e-9 and abs(levels - dc - slater @ H(4.0) @ slater) < 1e-9, slater @ H(4.0) @ slater)
check('the mean-field energy -0.5t lies above the exact -0.83t at U = 4t', slater @ H(4.0) @ slater > E0(4.0) + 0.3,
      (slater @ H(4.0) @ slater, E0(4.0)))
# the quiz names the antiferromagnetic solution, since m = 0 is also self-consistent at U = 4t, with other numbers
pm, pl, pdc, _, _ = meanfield(4.0, m=0.0)
check('U = 4t: m = 0 is also a fixed point, with the filled levels 2t, the constant -2t and <H> = 0, above the AF -0.5t',
      pm < 1e-12 and abs(pl - 2) < 1e-9 and abs(pdc - 2) < 1e-9 and abs(pl - pdc) < 1e-9, (pm, pl, pdc))
# a number in place of the operator, U <n_up><n_dn>: the spectrum is the one of U = 0, +-t on the dimer
check('without the interaction the levels of the dimer are -t and +t for each spin',
      np.allclose(np.linalg.eigvalsh(np.array([[0, -t], [-t, 0]])), [-t, t]), [-t, t])
# the identity of the fold, for operators that do not commute and numbers <A> and <B>
rng = np.random.default_rng(3)
A, B = rng.normal(size=(2, 5, 5)); ea, eb = 0.3, -0.7
check('AB = <A>B + A<B> - <A><B> + (A-<A>)(B-<B>)',
      np.allclose(A @ B, ea * B + eb * A - ea * eb * np.eye(5) + (A - ea * np.eye(5)) @ (B - eb * np.eye(5))), 'exact')
check('n_up n_dn = c_up^+ c_dn^+ c_dn c_up on a site, the pairing channel of the same term',
      np.allclose(n(c1u) @ n(c1d), c1u.T @ c1d.T @ c1d @ c1u), 'exact')
check('n_i n_j = c_i^+ c_j^+ c_j c_i for two sites, a term of (1.5)',
      np.allclose(n(c1u) @ n(c2u), c1u.T @ c2u.T @ c2u @ c1u), 'exact')


# the pairing channel of the fold: zero for U > 0, nonzero for U < 0. The decoupling gives the term
# Delta c_up^+ c_dn^+ + h.c. with Delta = U <c_dn c_up>, solved on a half-filled ring in the Nambu basis (c_i up, c_i dn^+)
def pairing_map(U, Delta, N=400):
    """One pass of the loop of the pairing channel, the new Delta = U <c_dn c_up> for the input Delta."""
    h = np.zeros((N, N))
    for i in range(N):
        h[i, (i + 1) % N] = h[(i + 1) % N, i] = -t
    Hb = np.block([[h, Delta * np.eye(N)], [np.conj(Delta) * np.eye(N), -h.T]])
    w, v = np.linalg.eigh(Hb)
    occ = v[:, w < 0]
    G = occ.conj() @ occ.T                                  # G[a, b] = <psi_a^+ psi_b>
    return U * np.conj(np.mean([G[i, N + i] for i in range(N)]))    # U <c_dn c_up> = U conj <c_up^+ c_dn^+>


Ds = (-1.0, -0.3, -0.05, 0.05, 0.3, 1.0)
check('pairing, U = +3t: the new Delta has the sign opposite to Delta, so the self-consistent value is zero',
      all(pairing_map(3.0, D).real * D < 0 for D in Ds), [round(pairing_map(3.0, D).real, 3) for D in Ds])
Dfix = optimize.brentq(lambda D: pairing_map(-3.0, D).real - D, 0.1, 2.0)
check('pairing, U = -3t: a nonzero self-consistent |Delta| = 0.931, the U m/2 of the antiferromagnet at U = +3t',
      abs(Dfix - 0.931) < 1e-3 and all(pairing_map(-3.0, D).real * D > 0 for D in Ds), Dfix)

# the dimer of pyqula at U = 4t, the same moment and energy (it writes no file)
from pyqula import geometry
with tempfile.TemporaryDirectory() as tmp:
    cwd = os.getcwd(); os.chdir(tmp)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            g = geometry.bichain(); g.dimensionality = 0
            hmf, e = g.get_hamiltonian().get_mean_field_hamiltonian(U=4.0, mf="antiferro", mix=0.9, return_total_energy=True)
            mz = hmf.get_vev("mz")
        left = os.listdir(tmp)
    finally:
        os.chdir(cwd)
check('pyqula dimer at U = 4t, |m| = 0.866 and the energy -0.5t', abs(abs(mz[0]) - 0.866) < 2e-3 and abs(e + 0.5) < 1e-3,
      (mz, e))
check('the spinful mean field of pyqula writes no file', left == [], left)


# ------------------------------------------------------------------ quiz 1, the charges of the chain (1.6) at V = 3t
def imbalance(V):
    """Hartree imbalance of the half-filled chain (1.6), 1 = (V/pi) int dk / sqrt(D^2 + 4t^2 cos^2 k), D = V dn,
    written with the complete elliptic integral K(m) of parameter m = 4t^2/(D^2 + 4t^2)."""
    f = lambda D: V * (2 / np.pi) * special.ellipk(4 * t ** 2 / (D ** 2 + 4 * t ** 2)) / np.sqrt(D ** 2 + 4 * t ** 2) - 1
    return optimize.brentq(f, 1e-12, 2 * V) / V


dn = imbalance(3.0)
check('in the Hartree mean field the half-filled chain at V = 3t ends with the charges 0.95 and 0.05', abs((1 + dn) / 2 - 0.946) < 1e-3 and
      abs((1 - dn) / 2 - 0.054) < 1e-3, ((1 + dn) / 2, (1 - dn) / 2))
print('all checks of page 12 hold')
