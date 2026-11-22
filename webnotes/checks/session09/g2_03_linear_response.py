"""Session 9, the numbers that page 03 (Section 9.3) states and that no figure script asserts.

The coefficients of the figure mixing (-0.286 for the level at 0.35t, the signs, the exact eigenvector) are asserted in
webnotes/figures/session09/mixing.py. This script holds the rest, the steps fold, the three quizzes and the problem, with
numpy only, and it writes no file.

Run it from anywhere:  python3 webnotes/checks/session09/g2_03_linear_response.py"""
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


sx = np.array([[0., 1.], [1., 0.]])


def ground(H):
    """Ground state of H with the coefficient of the first basis state set to one, and its energy."""
    w, U = np.linalg.eigh(H)
    return U[:, 0] / U[0, 0], w[0]


# ---- the steps fold, two levels: c = -lambda v/Delta, and chi_A = -2v/Delta for A = sigma_x
D, v, lam = 1.0, 0.1, 1e-4
psi, E = ground(np.diag([0., D]) + lam * v * sx)
check('steps: two levels, c/lambda -> -v/Delta at small lambda', abs(psi[1] / lam - (-v / D)) < 1e-6, psi[1] / lam)
check('steps: E_1(lambda) starts at order lambda^2', abs(E) < 2 * (lam * v)**2 / D, E)
sxexp = lambda l: (lambda p: p @ sx @ p / (p @ p))(ground(np.diag([0., D]) + l * v * sx)[0])
slope = (sxexp(lam) - sxexp(-lam)) / (2 * lam)
check('steps: chi_A = -2v/Delta for A = sigma_x, the slope of <sigma_x> in the exact ground state', abs(slope + 2 * v / D) < 1e-6, slope)
for vs, text in ((0.1, '-0.0990'), (-0.1, '0.0990')):
    cs = ground(np.diag([0., D]) + vs * sx)[0][1]
    check(f'steps: for v = {vs} Delta the exact coefficient is {text}, the sign of -v/Delta, negative only for v > 0',
          f'{cs:.4f}' == text and np.sign(cs) == np.sign(-vs / D), cs)

# ---- the steps fold, general case: c_m, E^(1) = <n|V|n> and chi_A = 2 Re sum <n|A|m><m|V|n>/(E_n - E_m) on random levels
rng = np.random.default_rng(3)
N = 6
H0 = np.diag([-2.0, -1.1, -0.3, 0.4, 1.2, 2.1])                   # levels at least 0.7 apart
herm = lambda: (lambda M: (M + M.conj().T) / 2)(rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N)))
Vm, A = herm(), herm()
E0 = np.diag(H0).real
lam = 1e-6
for n in (0, 2):
    others = [m for m in range(N) if m != n]
    c = np.array([Vm[m, n] / (E0[n] - E0[m]) for m in others])
    w, U = np.linalg.eigh(H0 + lam * Vm)
    u = U[:, n] / U[n, n]
    check(f'steps: c_m of (9.3) against the exact eigenvector, level {n} of {N} random levels',
          np.allclose(u[others] / lam, c, rtol=1e-3, atol=1e-6), np.round(np.abs(u[others] / lam - c).max(), 8))
    check(f'steps: E_n^(1) = <n|V|n>, level {n}', abs((w[n] - E0[n]) / lam - Vm[n, n].real) < 1e-3, (w[n] - E0[n]) / lam)
    chiA = 2 * np.real(sum(A[n, m] * Vm[m, n] / (E0[n] - E0[m]) for m in others))
    expA = lambda l: (lambda W: np.real(W[1][:, n].conj() @ A @ W[1][:, n]))(np.linalg.eigh(H0 + l * Vm))
    fd = (expA(lam) - expA(-lam)) / (2 * lam)
    check(f'steps: chi_A = 2 Re sum <n|A|m><m|V|n>/(E_n-E_m), level {n}', abs(fd - chiA) < 1e-5, (fd, chiA))

# ---- the first quiz: the sizes 0.1 and 0.01 for a matrix element 0.01t at 0.1t and 1.0t
c1, c2 = 0.01 / 0.1, 0.01 / 1.0
check('quiz 1: |c| = 0.1 at 0.1t and 0.01 at 1.0t, a factor ten', np.isclose(c1, 0.1) and np.isclose(c2, 0.01) and np.isclose(c1 / c2, 10),
      (c1, c2))

# ---- the second quiz: H_0 = 0 and a coupling v give (|1> +- |2>)/sqrt2 at +-v, and v/delta = 100 for v = 0.01t, delta = 1e-4 t
w, U = np.linalg.eigh(0.01 * sx)
check('quiz 2: degenerate levels coupled by v split into -v and +v', np.allclose(w, [-0.01, 0.01]), w)
check('quiz 2: the state at +v is (|1>+|2>)/sqrt2 and the one at -v is (|1>-|2>)/sqrt2',
      np.isclose(abs(U[:, 1] @ np.array([1, 1]) / np.sqrt(2)), 1) and np.isclose(abs(U[:, 0] @ np.array([1, -1]) / np.sqrt(2)), 1), U)
check('quiz 2: v/delta = 100 for v = 0.01t and delta = 1e-4 t', np.isclose(0.01 / 1e-4, 100), 0.01 / 1e-4)
w, U = np.linalg.eigh(np.diag([0., 1e-4]) + 1e-6 * sx)
check('quiz 2: a split delta = 1e-4 gives the first-order coefficient v/delta at small v', abs(U[1, 0] / U[0, 0] / 1e-6 + 1e4) < 1e2,
      U[1, 0] / U[0, 0] / 1e-6)

# ---- the third quiz and the problem: v = 0.1 Delta
D, v = 1.0, 0.1
psi, Em = ground(np.diag([0., D]) + v * sx)
Eexact = D / 2 - np.sqrt(D**2 / 4 + v**2)
check('problem: first order coefficient v/(0 - Delta) = -0.1', np.isclose(v / (0 - D), -0.1), v / (0 - D))
check('problem: exact E_- = -0.0099 Delta', np.isclose(Em, Eexact) and f'{Em:.4f}' == '-0.0099', Em)
check('problem and quiz 3: exact c = E_-/v = -0.0990', np.isclose(psi[1], Em / v) and f'{psi[1]:.4f}' == '-0.0990', psi[1])
cn = psi[1] / np.sqrt(1 + psi[1]**2)
check('problem: normalized coefficient -0.0985', f'{cn:.4f}' == '-0.0985', cn)
check('problem: E_1 = v c exactly, from the first row', np.isclose(Em, v * psi[1]), (Em, v * psi[1]))
check('problem and quiz 3: second order shift -v^2/Delta = -0.01 Delta', np.isclose(v * (-v / D), -0.01), v * (-v / D))
err_c, err_E = abs(psi[1] / -0.1 - 1), abs(Em / -0.01 - 1)
check('problem: both errors are one percent, (v/Delta)^2 = 0.01', round(100 * err_c) == 1 and round(100 * err_E) == 1, (err_c, err_E))
check('quiz 3: +v/Delta is the coefficient of |1> in the excited state', abs(np.linalg.eigh(np.diag([0., D]) + 1e-4 * sx)[1][:, 1][0]
      / np.linalg.eigh(np.diag([0., D]) + 1e-4 * sx)[1][:, 1][1] / 1e-4 - 1 / D) < 1e-3, 'v/(Delta - 0)')
print('all checks of page 03 hold')
