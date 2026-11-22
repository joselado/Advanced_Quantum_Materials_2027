"""Session 5, the statements and numbers of page 19 (Section 5.19), checked with the matrices of two fermion modes.

One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a box is an assert. The
four Majoranas are built from two modes c1 = (g1 + i g2)/2 and c2 = (g3 + i g4)/2 with a Jordan-Wigner string, which is
(5.18) for each mode, so that i g1 g2 = 2 n1 - 1 as on the conventions sheet. The figures four_majoranas and braid_order
assert their own statements. The numbers 1% and 2 T of the lab box are read with python3 webnotes/labsource.py --check 5,
which does not know the unit ms, so the sentence with 1 ms is asserted here in the tracked stored source. This script uses
numpy and scipy only, reads that one file and writes no file.

Run it from anywhere:  python3 webnotes/checks/session05/g6_19_braiding.py"""
import os
import numpy as np
from scipy.linalg import expm


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


I2, Z, X, Y = np.eye(2), np.diag([1.0, -1.0]), np.array([[0, 1.0], [1, 0]]), np.array([[0, -1j], [1j, 0]])
I = np.eye(4)
g = [None, np.kron(X, I2), np.kron(Y, I2), np.kron(Z, X), np.kron(Z, Y)]          # g[1] .. g[4]
c1, c2 = (g[1] + 1j * g[2]) / 2, (g[3] + 1j * g[4]) / 2
n1, n2 = c1.conj().T @ c1, c2.conj().T @ c2
dag = lambda m: m.conj().T
U = lambda a, b: expm(np.pi / 4 * g[a] @ g[b])

# ---- the recall box and the algebra of the Majoranas
ok = all(np.allclose(g[a] @ g[b] + g[b] @ g[a], 2 * I * (a == b)) for a in range(1, 5) for b in range(1, 5))
ok = ok and all(np.allclose(dag(g[a]), g[a]) for a in range(1, 5))
check('recall: the Majoranas are Hermitian, square to one and anticommute', ok, 'ok')
check('recall: c = (gA + i gB)/2 is a fermion, {c, c^dag} = 1 and c^2 = 0',
      np.allclose(c1 @ dag(c1) + dag(c1) @ c1, I) and np.allclose(c1 @ c1, 0) and np.allclose(c1 @ dag(c2) + dag(c2) @ c1, 0), 'ok')
check('i g1 g2 = 2 n1 - 1', np.allclose(1j * g[1] @ g[2], 2 * n1 - I), 'ok')

# ---- the first quiz and the figure of four Majoranas: four states, two of each parity
P = (I - 2 * n1) @ (I - 2 * n2)
check('quiz 1: two modes give 4 states, 2 of even and 2 of odd parity', sorted(np.round(np.diag(P).real)) == [-1, -1, 1, 1],
      np.diag(P).real)

# ---- the key box and its steps
G = g[1] @ g[2]
check('steps: (g1 g2)^2 = -1', np.allclose(G @ G, -I), 'ok')
th = 0.37
check('steps: exp(theta g1 g2) = cos theta + g1 g2 sin theta', np.allclose(expm(th * G), np.cos(th) * I + np.sin(th) * G), th)
U12, U23, U34 = U(1, 2), U(2, 3), U(3, 4)
check('steps: U12 = (1 + g1 g2)/sqrt 2 and U12^dag = (1 - g1 g2)/sqrt 2',
      np.allclose(U12, (I + G) / np.sqrt(2)) and np.allclose(dag(U12), (I - G) / np.sqrt(2)) and np.allclose(dag(G), -G), 'ok')
check('steps: g1 g2 g1 = -g2 and g1 g1 g2 = g2', np.allclose(g[1] @ g[2] @ g[1], -g[2]) and np.allclose(g[1] @ g[1] @ g[2], g[2]), 'ok')
check('steps: (g1 - g2)(1 - g1 g2)/2 = -g2', np.allclose((g[1] - g[2]) @ (I - G) / 2, -g[2]), 'ok')
check('steps: U12 g1 U12^dag = -g2 and U12 g2 U12^dag = g1',
      np.allclose(U12 @ g[1] @ dag(U12), -g[2]) and np.allclose(U12 @ g[2] @ dag(U12), g[1]), 'ok')
comm = U12 @ U23 - U23 @ U12
check('key and steps: U12 U23 - U23 U12 = g1 g3, which is not zero, with entries up to 1.00',
      np.allclose(comm, g[1] @ g[3]) and abs(np.abs(comm).max() - 1) < 1e-12, round(np.abs(comm).max(), 4))
check('key and steps: g1 g2 and g3 g4 commute, so U12 U34 = U34 U12',
      np.allclose(G @ g[3] @ g[4], g[3] @ g[4] @ G) and np.allclose(U12 @ U34, U34 @ U12), 'ok')
check('text: g1 g2 and g2 g3 anticommute', np.allclose(G @ g[2] @ g[3] + g[2] @ g[3] @ G, 0), 'ok')
check('a braid keeps the parity', np.allclose(U12 @ P, P @ U12), 'ok')

# ---- the second quiz, kept: in the even sector i g3 g4 acts like sigma_z and i g2 g3 like sigma_x
even = [0, 3]                                                   # |00> and |11>
A, B = (1j * g[3] @ g[4])[np.ix_(even, even)], (1j * g[2] @ g[3])[np.ix_(even, even)]
check('quiz 2: in the even sector i g3 g4 is diagonal with +-1 and i g2 g3 is off-diagonal with modulus 1',
      np.allclose(np.abs(np.diag(A)), 1) and np.allclose(A, np.diag(np.diag(A))) and np.allclose(np.diag(B), 0)
      and np.allclose(np.abs(B[0, 1]), 1) and np.allclose(A @ B + B @ A, 0), (np.diag(A).real, B[0, 1]))

# ---- the new quiz: (g1 g2)^2 = -1, and g1 g2 = -i (2 n1 - 1) is i on the empty state and -i on the filled one
check('quiz 3: g1 g2 = -i (2 c^dag c - 1)', np.allclose(G, -1j * (2 * n1 - I)), 'ok')
vac = np.zeros(4); vac[0] = 1                                    # both modes empty
filled = dag(c1) @ vac
check('quiz 3: g1 g2 is i on the empty state and -i on the filled one',
      np.allclose(G @ vac, 1j * vac) and np.allclose(G @ filled, -1j * filled), 'ok')
S1, S2 = np.kron(Z, I2), np.kron(I2, Z)
check('quiz 3: sigma_z on two different sites commute, and their product squares to +1',
      np.allclose(S1 @ S2, S2 @ S1) and np.allclose((S1 @ S2) @ (S1 @ S2), I), 'ok')

# ---- the problem
check('problem: U12^4 = -1', np.allclose(np.linalg.matrix_power(U12, 4), -I), 'ok')
U2 = U12 @ U12
check('problem: U12^2 = g1 g2, and it sends g1 to -g1', np.allclose(U2, G) and np.allclose(U2 @ g[1] @ dag(U2), -g[1]), 'ok')
check('problem: one braid twice, g1 -> -g2 -> -g1', np.allclose(U12 @ (-g[2]) @ dag(U12), -g[1]), 'ok')
val = 1j * G
ok = True
for s, phase in ((-1, np.exp(1j * np.pi / 4)), (1, np.exp(-1j * np.pi / 4))):
    w, v = np.linalg.eigh(val)
    for j in np.where(np.isclose(w, s))[0]:
        ok = ok and np.allclose(U12 @ v[:, j], phase * v[:, j])
check('problem: U12 gives e^{i pi/4} to i g1 g2 = -1 and e^{-i pi/4} to i g1 g2 = +1', ok, 'ok')

# ---- the end of the solution: in the even sector, |00> and |11>, one braid is a phase gate and two braids are i sigma_z
s00 = vac
s11 = dag(c1) @ dag(c2) @ vac
check('problem: |00> has i g1 g2 = -1 and |11> has i g1 g2 = +1',
      np.allclose(1j * G @ s00, -s00) and np.allclose(1j * G @ s11, s11) and np.isclose(np.linalg.norm(s11), 1), 'ok')
ev = np.array([s00, s11]).T                                      # the columns are |00> and |11>
U1e, U2e = dag(ev) @ U12 @ ev, dag(ev) @ U2 @ ev
check('problem: one braid is diag(e^{i pi/4}, e^{-i pi/4}) on |00>, |11>, a phase gate with the relative phase e^{-i pi/2}',
      np.allclose(U1e, np.diag([np.exp(1j * np.pi / 4), np.exp(-1j * np.pi / 4)])) and np.isclose(U1e[1, 1] / U1e[0, 0], -1j), 'ok')
check('problem: two braids, U12^2 = g1 g2, are i on |00> and -i on |11>, so i sigma_z in the even sector, not a multiple of 1',
      np.allclose(U2e, 1j * Z) and not np.allclose(U2e, U2e[0, 0] * np.eye(2)), np.round(np.diag(U2e), 6))
check('problem: four braids are -1 on both states, which does nothing to a qubit',
      np.allclose(dag(ev) @ np.linalg.matrix_power(U12, 4) @ ev, -np.eye(2)), 'ok')

# ---- the lab box: the sentence of the dwell time, with 1 ms, is in the tracked stored source of the article
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'sources', 'session05', 'aghaee2025_arxiv2401.09549.txt')
text = open(src, encoding='utf-8').read()
check('lab box: the stored source states the dwell time longer than 1 ms at approximately 2 T, and the error probability of 1%',
      'a dwell time in the two associated states that is longer than 1 ms at in-plane magnetic fields of approximately 2 T' in text
      and 'parity measurement with an assignment error probability of 1%' in text
      and 'url: https://www.nature.com/articles/s41586-024-08445-2' in text, os.path.relpath(src, os.path.dirname(src) + '/../..'))
