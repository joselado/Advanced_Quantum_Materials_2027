"""Session 5, the numbers and the algebra that page 15 (Section 5.15) states, checked with matrices.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert. Page
15 has no figure with numbers, so everything is here: the relations of (5.17) and (5.18) and of the steps fold, the
three quizzes, and the problem with the two Majoranas H = (i eps/2) gamma_A gamma_B, whose closing sentence ties eps to
the lowest BdG level of an open Kitaev chain (5.19). The last part builds the chain of 8 sites in the many-body space,
2^8 states, and compares the splitting of its two lowest states of opposite parity with the lowest positive BdG level.
It finds the repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session05/g4_15_majorana_operators.py"""
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def dag(m):
    return m.conj().T


def close(a, b, tol=1e-12):
    return np.abs(np.asarray(a) - np.asarray(b)).max() < tol


# one fermion mode in the basis (|0>, |1>)
c = np.array([[0, 1], [0, 0]], dtype=complex)
cd = dag(c)
one = np.eye(2)
n = cd @ c
gA = c + cd
gB = -1j * (c - cd)
vac, full = np.array([1, 0], complex), np.array([0, 1], complex)

check('{c, c^dag} = 1 and c^2 = 0', close(c @ cd + cd @ c, one) and close(c @ c, 0 * one), True)
check('(5.16) and (5.17): gamma_A and gamma_B are Hermitian', close(gA, dag(gA)) and close(gB, dag(gB)), True)
check('gamma_A^2 = gamma_B^2 = 1', close(gA @ gA, one) and close(gB @ gB, one), True)
check('{gamma_A, gamma_B} = 0', close(gA @ gB + gB @ gA, 0 * one), True)
check('(5.18): c = (gamma_A + i gamma_B)/2 and c^dag = (gamma_A - i gamma_B)/2',
      close(c, (gA + 1j * gB) / 2) and close(cd, (gA - 1j * gB) / 2), True)
check('the fold: gamma_A gamma_B = -i (c^dag c - c c^dag) = -i (2 c^dag c - 1)',
      close(gA @ gB, -1j * (cd @ c - c @ cd)) and close(gA @ gB, -1j * (2 * n - one)), True)
check('i gamma_A gamma_B = 2 c^dag c - 1, which is -1 on the empty mode and +1 on the filled one',
      close(1j * gA @ gB, 2 * n - one) and close(1j * gA @ gB @ vac, -vac) and close(1j * gA @ gB @ full, full), True)
check('the kept quiz: gamma_A gamma_B |0> = i|0> and gamma_B gamma_A |0> = -i|0>',
      close(gA @ gB @ vac, 1j * vac) and close(gB @ gA @ vac, -1j * vac), True)
check('the kept quiz: gamma_A |0> = |1> and gamma_A |1> = |0>', close(gA @ vac, full) and close(gA @ full, vac), True)
check('the kept quiz: (i gamma_A gamma_B)^2 = 1, so its eigenvalues are +-1 and never 0',
      close((1j * gA @ gB) @ (1j * gA @ gB), one) and close(np.sort(np.linalg.eigvalsh(1j * gA @ gB)), [-1, 1]), True)

# the new quiz: which operator is Hermitian and squares to one
m1, m2, m3 = c + cd, c - cd, cd @ c
check('quiz, c + c^dag is Hermitian and squares to one', close(m1, dag(m1)) and close(m1 @ m1, one), True)
check('quiz, (c - c^dag)^dag = -(c - c^dag) and (c - c^dag)^2 = -1', close(dag(m2), -m2) and close(m2 @ m2, -one), True)
check('quiz, -i(c - c^dag) is Hermitian, gamma_B', close(-1j * m2, gB) and close(-1j * m2, dag(-1j * m2)), True)
check('quiz, multiplied by i or by -i, c - c^dag becomes Hermitian and squares to one, and i(c - c^dag) = -gamma_B',
      all(close(z * m2, dag(z * m2)) and close((z * m2) @ (z * m2), one) for z in (1j, -1j)) and close(1j * m2, -gB), True)
check('quiz, c^dag c is Hermitian, (c^dag c)^2 = c^dag c, which is 0 on the empty mode',
      close(m3, dag(m3)) and close(m3 @ m3, m3) and close(m3 @ m3 @ vac, 0 * vac)
      and close(np.sort(np.linalg.eigvalsh(m3)), [0, 1]), True)

# the problem: H = (i eps/2) gamma_A gamma_B = eps c^dag c - eps/2, levels -eps/2 (empty) and +eps/2 (filled)
eps = 0.2
H = 0.5j * eps * gA @ gB
check('the problem, H = eps c^dag c - eps/2', close(H, eps * n - eps / 2 * one), True)
lev = np.linalg.eigvalsh(H)
check('the problem, eps = 0.2: levels -0.1 on the empty mode and +0.1 on the filled mode, splitting 0.2',
      close(lev, [-0.1, 0.1]) and close(vac.conj() @ H @ vac, -0.1) and close(full.conj() @ H @ full, 0.1)
      and abs(lev[1] - lev[0] - eps) < 1e-12, np.round(lev, 12))


# the closing sentence of the solution: in an open Kitaev chain (5.19) the two lowest many-body states have opposite
# parity, and their splitting is the lowest positive BdG level, 0.0111 t for N = 8, Delta = 0.5 t and mu = t
def fermions(N):
    Z, I, low = np.diag([1.0, -1.0]), np.eye(2), np.array([[0.0, 1.0], [0.0, 0.0]])
    out = []
    for j in range(N):
        m = np.array([[1.0]])
        for l in range(N):
            m = np.kron(m, Z if l < j else (low if l == j else I))
        out.append(m)
    return out


N, t, mu, D = 8, 1.0, 1.0, 0.5
f = fermions(N)
Hmb = sum(-t * (f[j].T @ f[j + 1] + f[j + 1].T @ f[j]) + D * (f[j] @ f[j + 1] + f[j + 1].T @ f[j].T) for j in range(N - 1))
Hmb = Hmb - mu * sum(x.T @ x for x in f)
P = np.diag([(-1) ** bin(s).count('1') for s in range(2 ** N)])
check('the Kitaev chain conserves the parity', close(Hmb @ P, P @ Hmb), True)
w, v = np.linalg.eigh(Hmb)
par = [float(np.real(v[:, i] @ P @ v[:, i])) for i in range(2)]
split = w[1] - w[0]
hop = -t * (np.eye(N, k=1) + np.eye(N, k=-1)) - mu * np.eye(N)
pair = D * (np.eye(N, k=-1) - np.eye(N, k=1))            # the matrix of the sheet, d_{n+1,n} = Delta = -d_{n,n+1}
bdg = np.block([[hop, pair], [dag(pair), -hop]])
e = np.linalg.eigvalsh(bdg)
lowest = e[e > -1e-12].min()
check('N=8, Delta=0.5t, mu=t: the two lowest states have opposite parity', abs(par[0] + par[1]) < 1e-9,
      np.round(par, 9))
check('their splitting equals the lowest positive BdG level, the page says 0.011t', abs(split - lowest) < 1e-10
      and abs(lowest - 0.0111) < 5e-5, (round(split, 6), round(lowest, 6)))
print('all checks of page 15 hold')
