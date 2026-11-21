"""Session 2, the numbers that page 03 (Section 2.3) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The dimer and the two rings of the schematic dimer_ring_symmetry are asserted in
its figure script, the block matrix in block_diagonal.py and the three states of the picture quiz in _g1_ring.py, all
in figures/session02/. This script holds the rest, and it also runs check() of _g1_ring.py, so that --verify sees the
asserts of the picture quiz. It needs numpy, and matplotlib for that import, and writes no file.

The rotation R of the page moves every amplitude to the next site, (R psi)_j = psi_{j-1}, which is the direction that
the page uses today. The direction is an open point of the plan, so every new statement of the page is checked here
for both senses, R and its transpose, and only the old text and the quiz that defines R use R alone."""
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


R4 = np.roll(np.eye(4), 1, axis=0)                       # (R psi)_j = psi_{j-1}, the direction of the page
SENSES = (R4, R4.T)
H4 = -(R4 + R4.T)                                        # the ring of four sites with the hopping -t, t = 1


def factor(R, v):
    lam = (v.conj() @ R @ v) / (v.conj() @ v)
    return lam if np.allclose(R @ v, lam * v) else None


# the two examples of the text, with the rotation of the page
s1 = np.array([1, -1, 1, -1], complex)
s2 = np.array([1, -1j, -1, 1j])
check('(1,-1,1,-1) goes to (-1,1,-1,1), the eigenvalue -1, phi = pi', np.allclose(R4 @ s1, [-1, 1, -1, 1])
      and np.isclose(factor(R4, s1), -1) and np.isclose(np.angle(-1), np.pi), factor(R4, s1))
check('(1,-i,-1,i) has the eigenvalue i, phi = pi/2', np.isclose(factor(R4, s2), 1j) and np.isclose(np.angle(1j), np.pi / 2),
      factor(R4, s2))

# the first quiz, which defines R as the page does
q = np.array([1, 1j, -1, -1j])
check('(1,i,-1,-i) goes to (-i,1,i,-1), which is -i times it', np.allclose(R4 @ q, [-1j, 1, 1j, -1])
      and np.isclose(factor(R4, q), -1j) and np.isclose(np.angle(-1j), -np.pi / 2), R4 @ q)
check('the eigenvalue i would give (i,-1,-i,1), and (1,1,1,1) is the state of the eigenvalue 1',
      np.allclose(1j * q, [1j, -1, -1j, 1]) and np.isclose(factor(R4, np.ones(4)), 1), True)

# the steps: |lambda| = 1 from (2.1), for a random unitary matrix
rng = np.random.default_rng(3)
Q, _ = np.linalg.qr(rng.normal(size=(6, 6)) + 1j * rng.normal(size=(6, 6)))
check('the eigenvalues of a unitary matrix have modulus 1', np.allclose(np.abs(np.linalg.eigvals(Q)), 1),
      np.round(np.abs(np.linalg.eigvals(Q)), 12))

# the steps: the level E = 0 of the ring of four sites, for both senses of the rotation
a = np.array([1, 0, -1, 0]) / np.sqrt(2)
b = np.array([0, 1, 0, -1]) / np.sqrt(2)
e4 = np.linalg.eigvalsh(H4)
ok = np.allclose(H4 @ a, 0) and np.allclose(H4 @ b, 0) and np.allclose(e4, [-2, 0, 0, 2])
ok = ok and np.allclose(R4 @ a, b) and np.allclose(R4 @ b, -a) and np.allclose(R4.T @ a, -b) and np.allclose(R4.T @ b, a)
for R in SENSES:
    ok = ok and factor(R, a) is None and factor(R, b) is None
    m = np.array([[x @ R @ y for y in (a, b)] for x in (a, b)])
    ok = ok and np.allclose(np.sort_complex(np.linalg.eigvals(m)), np.sort_complex(np.array([-1j, 1j])))
    for sign in (1, -1):
        v = a - sign * 1j * b
        target = np.array([1, -sign * 1j, -1, sign * 1j])
        ok = ok and np.allclose(v, target / np.sqrt(2)) and np.isclose(np.linalg.norm(v), np.sqrt(2))
        ok = ok and np.allclose(v / np.sqrt(2), target / 2) and np.isclose(np.linalg.norm(v / np.sqrt(2)), 1)
        ok = ok and factor(R, v) is not None and np.isclose(abs(factor(R, v)), 1)
ok = ok and np.isclose(factor(R4, a - 1j * b), 1j) and np.isclose(factor(R4, a + 1j * b), -1j)
check('the level 0 of the ring with -t holds a and b, the rotation maps a to +-b and b to -+a, a -+ ib = '
      '(1,-+i,-1,+-i)/sqrt2 with the norm sqrt2, the normalized (a -+ ib)/sqrt2 = (1,-+i,-1,+-i)/2, and with the R of '
      'the page a - ib has i and a + ib has -i', ok, np.round(e4, 6))

# the steps, last line: H has no element between two eigenvalues of S that differ
Hr = sum(c * np.linalg.matrix_power(R4, n) for n, c in enumerate(rng.normal(size=4) + 1j * rng.normal(size=4)))
Hr = Hr + Hr.conj().T
F = np.array([np.exp(-1j * np.pi / 2 * n * np.arange(4)) / 2 for n in range(4)]).T     # eigenvectors of R4
lam = np.array([factor(R4, F[:, n]) for n in range(4)])
Hf = F.conj().T @ Hr @ F
off = max(abs(Hf[m, n]) for m in range(4) for n in range(4) if not np.isclose(lam[m], lam[n]))
check('a Hamiltonian that commutes with R has no element between two different eigenvalues of R',
      np.allclose(Hr @ R4, R4 @ Hr) and off < 1e-12, off)

# the quiz on [H,S] = 0: the ground state (1,1,1,1)/2 of the ring with -t
g = np.ones(4) / 2
w, V = np.linalg.eigh(H4)
check('(1,1,1,1)/2 is the single ground state at -2t, S psi = psi and the overlap is 1',
      np.allclose(H4 @ g, -2 * g) and w[1] - w[0] > 1 and np.isclose(abs(V[:, 0] @ g), 1)
      and all(np.allclose(R @ g, g) for R in SENSES) and np.isclose(g @ R4 @ g, 1), w)
check('H S psi = -2t psi, not +2t psi', np.allclose(H4 @ R4 @ g, -2 * g) and not np.allclose(H4 @ R4 @ g, 2 * g), True)
# the question says that S is unitary: S = H also commutes with H, and it gives S psi = -2 psi, which is not a phase
check('a non-unitary S = H commutes with H and gives S psi = -2 psi, of modulus 2, so the quiz needs a unitary S',
      np.allclose(H4 @ H4, H4 @ H4) and np.allclose(H4 @ g, -2 * g) and not np.allclose(H4.conj().T @ H4, np.eye(4)),
      np.round((H4 @ g) / g, 6))

# the picture quiz: the state e^{i pi j/3} turns by 60, 60, 60 and 180 degrees, and 4 x 60 = 240 is not 360 n.
# The asserts of the three pictures live in figures/session02/_g1_ring.py, and its check() writes no figure.
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'figures', 'session02'))
import _g1_ring
_g1_ring.check()
w = _g1_ring.STATES['turn60']
steps = np.degrees(np.angle(np.r_[w[1:], w[:1]] / w)) % 360
check('the state turning by 60 degrees: the same length, the steps 60, 60, 60, 180, and 4 x 60 = 240 is no multiple of 360',
      np.allclose(np.abs(w), 1) and np.allclose(steps, [60, 60, 60, 180]) and 4 * 60 == 240 and 240 % 360 != 0,
      np.round(steps, 6))

# the problem: the open chain of three sites and the mirror that exchanges the sites 1 and 3
M = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
ok = True
for t in (1.0, -1.0, 0.7):
    H3 = t * np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    ok = ok and np.allclose(H3 @ M, M @ H3) and np.allclose(M @ H3 @ M, H3) and np.allclose(M @ M, np.eye(3))
    up, zero, dn = np.array([1, np.sqrt(2), 1]) / 2, np.array([1, 0, -1]) / np.sqrt(2), np.array([1, -np.sqrt(2), 1]) / 2
    ok = ok and np.allclose(H3 @ up, np.sqrt(2) * t * up) and np.allclose(H3 @ dn, -np.sqrt(2) * t * dn)
    ok = ok and np.allclose(H3 @ zero, 0) and np.allclose(M @ up, up) and np.allclose(M @ dn, dn) and np.allclose(M @ zero, -zero)
    u, v = np.array([1, 0, 1]) / np.sqrt(2), np.array([0, 1, 0])
    sector = np.array([[x @ H3 @ y for y in (u, v)] for x in (u, v)])
    ok = ok and np.allclose(sector, [[0, np.sqrt(2) * t], [np.sqrt(2) * t, 0]])
    e, vecs = np.linalg.eigh(H3)
    mirror = [vecs[:, n] @ M @ vecs[:, n] for n in range(3)]
    ok = ok and np.allclose(e, np.sort([-np.sqrt(2) * abs(t), 0, np.sqrt(2) * abs(t)])) and np.allclose(mirror, [1, -1, 1])
check('the chain of three sites: [H,M] = 0, the energies -sqrt2 t, 0, sqrt2 t with the mirror +1, -1, +1, for t = 1, -1, 0.7',
      ok, np.round(np.linalg.eigvalsh(np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])), 4))
print('all checks of page 03 hold')
