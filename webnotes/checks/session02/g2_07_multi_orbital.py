"""Session 2, the numbers that page 07 (Section 2.7) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a box is an
assert, here or in the figure script that draws it. The numbers of the figure ssh_recipe are asserted in
figures/session02/ssh_recipe.py, and those of fold_three in fold_three.py. This script holds the rest, in the order
of the page. It finds the repository from its own path and writes no file in it, since pyqula runs in a temporary
folder.

Run it from anywhere:  python3 webnotes/checks/session02/g2_07_multi_orbital.py"""
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
import physcheck  # noqa: E402


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def bloch(t, g, f):
    """(2.12), H(phi) = t + gamma e^{i phi} + gamma^dagger e^{-i phi}."""
    return t + g * np.exp(1j * f) + g.conj().T * np.exp(-1j * f)


def ssh(eta, f):
    """(2.13), the chain with the hopping 1 inside the cell and eta from B to A of the next cell, A first."""
    return bloch(np.array([[0, 1.], [1., 0]]), np.array([[0, 0], [eta, 0.]]), f)


# the fold, simplest case: one orbital, t = 0 and gamma = -t give -2t cos(phi), which is (2.8)
f = np.linspace(-np.pi, np.pi, 13)
check('fold: one orbital with gamma=-t gives -2t cos(phi)', np.allclose(
    [bloch(np.zeros((1, 1)), np.array([[-0.8]]), x)[0, 0] for x in f], -2 * 0.8 * np.cos(f)), 'ok')

# the fold, general case: the spectrum of (2.11) on a ring of L cells is the set of eigenvalues of (2.12) at the
# phases 2 pi j / L, for a random Hermitian t and a random gamma of three orbitals
rng = np.random.default_rng(2)
no, L = 3, 7
t = rng.normal(size=(no, no)) + 1j * rng.normal(size=(no, no)); t = t + t.conj().T
g = rng.normal(size=(no, no)) + 1j * rng.normal(size=(no, no))
H = np.zeros((no * L, no * L), complex)
for n in range(L):
    H[no * n:no * n + no, no * n:no * n + no] += t
    m = (n + 1) % L
    H[no * n:no * n + no, no * m:no * m + no] += g          # gamma_ab c^dagger_{n,a} c_{n+1,b}
    H[no * m:no * m + no, no * n:no * n + no] += g.conj().T  # its Hermitian conjugate
ek = np.sort(np.concatenate([np.linalg.eigvalsh(bloch(t, g, 2 * np.pi * j / L)) for j in range(L)]))
check('fold: (2.11) on a ring of 7 cells has the eigenvalues of (2.12) at phi = 2 pi j/7', np.allclose(
    ek, np.linalg.eigvalsh(H)), np.round(ek[:3], 4))

# the fold: the operators c^dagger_{phi,a} = sum_n e^{i n phi} c^dagger_{n,a} do not mix the orbitals, and the
# eigenstates are these operators rotated by U(phi), the eigenvectors of H(phi). On the ring, the vector with the
# amplitude e^{i n phi} u on the cell n is an eigenvector of (2.11) when H(phi) u = eps u, for every band.
ok = True
for j in range(L):
    fj = 2 * np.pi * j / L
    w, U = np.linalg.eigh(bloch(t, g, fj))
    for b in range(no):
        v = np.concatenate([np.exp(1j * n * fj) * U[:, b] for n in range(L)])
        ok = ok and np.allclose(H @ v, w[b] * v)
check('fold: e^{i n phi} u is an eigenvector of (2.11) on the ring for each eigenvector u of H(phi)', ok, 'ok')

# the key box: a hopping gamma_m to the cell at the distance m adds gamma_m e^{i m phi} and its Hermitian conjugate.
# Ring of 9 cells of two orbitals with a random t, gamma_1 and gamma_2.
no2, L2 = 2, 9
t2 = rng.normal(size=(no2, no2)) + 1j * rng.normal(size=(no2, no2)); t2 = t2 + t2.conj().T
g1 = rng.normal(size=(no2, no2)) + 1j * rng.normal(size=(no2, no2))
g2 = rng.normal(size=(no2, no2)) + 1j * rng.normal(size=(no2, no2))
H2 = np.zeros((no2 * L2, no2 * L2), complex)
for n in range(L2):
    H2[no2 * n:no2 * n + no2, no2 * n:no2 * n + no2] += t2
    for m_, gm in ((1, g1), (2, g2)):
        q = (n + m_) % L2
        H2[no2 * n:no2 * n + no2, no2 * q:no2 * q + no2] += gm
        H2[no2 * q:no2 * q + no2, no2 * n:no2 * n + no2] += gm.conj().T
bm = lambda x: bloch(t2, g1, x) + g2 * np.exp(2j * x) + g2.conj().T * np.exp(-2j * x)
ek2 = np.sort(np.concatenate([np.linalg.eigvalsh(bm(2 * np.pi * j / L2)) for j in range(L2)]))
check('key box: a hopping gamma_2 to the cell at distance 2 adds gamma_2 e^{2i phi} + h.c., ring of 9 cells',
      np.allclose(ek2, np.linalg.eigvalsh(H2)) and not np.allclose(ek2, np.sort(np.concatenate(
          [np.linalg.eigvalsh(bloch(t2, g1, 2 * np.pi * j / L2)) for j in range(L2)]))), np.round(ek2[:2], 4))

# the fold, the chain of (2.13): the entries 1 + eta e^{-i phi} and 1 + eta e^{i phi}, zero trace, the determinant
# -|1 + eta e^{-i phi}|^2 and the bands +-|1 + eta e^{-i phi}|
for eta in (0.6, 1.0, 1.4):
    ok = True
    for x in f:
        m = ssh(eta, x)
        z = 1 + eta * np.exp(-1j * x)
        ok = ok and np.isclose(m[0, 1], z) and np.isclose(m[1, 0], np.conj(z)) and np.isclose(np.trace(m), 0) \
            and np.isclose(np.linalg.det(m), -abs(z) ** 2) and np.allclose(np.linalg.eigvalsh(m), [-abs(z), abs(z)])
    check(f'fold: (2.13) entry by entry, trace, determinant and bands, eta={eta}', ok, 'ok')

# the fold: in pyqula h.intra is t and h.inter is gamma, so bichain with h.inter = eta*h.inter gives (2.13)
os.chdir(tempfile.mkdtemp())
from pyqula import geometry  # noqa: E402

hb = geometry.bichain().get_hamiltonian(has_spin=False)
hb.inter = 0.6 * hb.inter
hk = hb.get_hk_gen()
check('fold: pyqula bichain intra is t and inter is gamma of (2.13)', np.allclose(hb.intra, [[0, 1], [1, 0]])
      and np.allclose(hb.inter, [[0, 0], [0.6, 0]]), 'ok')
check('fold: pyqula bichain H(k) is (2.13) with phi = 2 pi k', all(np.allclose(np.asarray(hk([x / (2 * np.pi), 0, 0])),
      ssh(0.6, x)) for x in f), 'ok')

# the caption of Figure 2.3: for eta = 0.6 a gap at the zone edge, closed exactly at eta = 1
gap = lambda eta: np.diff(np.linalg.eigvalsh(ssh(eta, np.pi)))[0]
check('Figure 2.3: a gap for eta=0.6, none for eta=1', gap(0.6) > 0.1 and abs(gap(1.0)) < 1e-12, (gap(0.6), gap(1.0)))

# the quiz with three matrices
m1 = lambda eta, x: np.array([[2 * eta * np.cos(x), 1], [1, 2 * eta * np.cos(x)]])
m2 = lambda eta, x: np.array([[0, eta + np.exp(-1j * x)], [eta + np.exp(1j * x), 0]])
check('matrix quiz, option 1: eta between equal sites of neighboring cells gives 2 eta cos(phi) on the diagonal',
      np.allclose(m1(0.6, 0.4), bloch(np.array([[0, 1.], [1, 0]]), 0.6 * np.eye(2), 0.4)), 'ok')
check('matrix quiz, option 1: for eta=1, phi=pi it gives -3 and -1, while (2.13) gives 0 and 0',
      np.allclose(np.linalg.eigvalsh(m1(1.0, np.pi)), [-3, -1]) and np.allclose(np.linalg.eigvalsh(ssh(1.0, np.pi)), 0),
      np.linalg.eigvalsh(m1(1.0, np.pi)))
check('matrix quiz, option 2: it is the chain with eta inside the cell and 1 between cells',
      all(np.allclose(m2(0.6, x), bloch(np.array([[0, 0.6], [0.6, 0]]), np.array([[0, 0], [1., 0]]), x)) for x in f), 'ok')
check('matrix quiz, option 2: at eta=0 it still depends on phi, while (2.13) does not',
      not np.allclose(m2(0, 0.3), m2(0, 1.3)) and np.allclose(ssh(0, 0.3), ssh(0, 1.3)), 'ok')
check('matrix quiz, option 2: the same bands, |eta + e^{-i phi}| = |1 + eta e^{-i phi}|',
      all(np.allclose(np.linalg.eigvalsh(m2(eta, x)), np.linalg.eigvalsh(ssh(eta, x))) for eta in (0.3, 0.6, 1.5)
          for x in f), 'ok')
# option 2 is the form (3.5) of Session 3, d(k) = t + e^{ik} with the variable hopping t inside the cell, for t = eta
# and the phase of the opposite sign, k = -phi. The key box of Session 3.9c gives its Zak phase pi for t<1 and 0 for t>1.
d35 = lambda tt, k: np.array([[0, tt + np.exp(1j * k)], [tt + np.exp(-1j * k), 0]])
check('matrix quiz, option 2: it is (3.5) with t=eta and k=-phi', all(np.allclose(m2(eta, x), d35(eta, -x))
      for eta in (0.3, 1.5) for x in f), 'ok')
z35 = [physcheck.zak_phase(lambda k: d35(tt, k), 2 * np.pi, bands=0, nk=200) for tt in (0.3, 1.5)]
check('matrix quiz, option 2: (3.5) has the Zak phase pi for t=0.3 and 0 for t=1.5, as Section 3.9c says',
      abs(abs(z35[0]) - np.pi) < 1e-6 and abs(z35[1]) < 1e-6, np.round(z35, 6))
for eta in (0.3, 0.6):
    z_right = physcheck.zak_phase(lambda k: ssh(eta, k), 2 * np.pi, bands=0, nk=200)
    z_opt2 = physcheck.zak_phase(lambda k: m2(eta, k), 2 * np.pi, bands=0, nk=200)
    check(f'matrix quiz, option 2: for eta={eta}<1 the Zak phase is 0 for (2.13) and pi for option 2',
          abs(z_right) < 1e-6 and abs(abs(z_opt2) - np.pi) < 1e-6, (round(z_right, 6), round(z_opt2, 6)))

# the quiz on eta = 1 and phi = pi: 1 + eta e^{-i pi} = 1 - eta = 0, +-2 = +-|1 + eta| at phi = 0, the gap 2|1 - eta|
# is 1 for eta = 0.5 and 0 for eta = 1
check('quiz eta=1: both bands 0 at phi=pi', np.allclose(np.linalg.eigvalsh(ssh(1.0, np.pi)), 0), 0)
check('quiz eta=1: +-2 at phi=0', np.allclose(np.linalg.eigvalsh(ssh(1.0, 0.0)), [-2, 2]), np.linalg.eigvalsh(ssh(1.0, 0.0)))
check('quiz eta=1: the gap 2|1-eta| at pi is 1 for eta=0.5 and 0 for eta=1', np.isclose(gap(0.5), 1.0)
      and np.isclose(gap(0.5), 2 * abs(1 - 0.5)) and abs(gap(1.0)) < 1e-12, gap(0.5))

# the quiz on three sites: three bands, -2t, t, t at phi = 0, the zone 2 pi/3a, the uniform chain with t = 1
t1 = 1.0
h3 = lambda x: bloch(np.array([[0, -t1, 0], [-t1, 0, -t1], [0, -t1, 0]]),
                     np.array([[0, 0, 0], [0, 0, 0], [-t1, 0, 0]]), x)
check('quiz three sites: -2t, t, t at phi=0, three bands', np.allclose(np.linalg.eigvalsh(h3(0.0)), [-2, 1, 1]), 'ok')
check('quiz three sites: the branches -2t cos[(phi + 2 pi m)/3]', all(np.allclose(np.linalg.eigvalsh(h3(x)), np.sort(
    [-2 * np.cos((x + 2 * np.pi * m) / 3) for m in range(3)])) for x in f), 'ok')

# the problem: H(phi), the bands +-sqrt(Delta^2 + 2 t^2 (1 + cos phi)), the gap 2|Delta| at pi, +-sqrt(Delta^2 + 4t^2)
# at 0, +-2t|cos(phi/2)| for Delta = 0, from numpy and from pyqula (bichain, hoppings -1, add_sublattice_imbalance).
# A negative Delta is included, since the page writes |Delta|: t = 0.7, Delta = -0.4 gives the gap 0.8.
for t_, D in ((1.0, 0.3), (0.7, 0.5), (0.7, -0.4)):
    Hp = lambda x: np.array([[D, -t_ * (1 + np.exp(-1j * x))], [-t_ * (1 + np.exp(1j * x)), -D]])
    ok = all(np.isclose(Hp(x)[0, 1], bloch(np.array([[D, -t_], [-t_, -D]]), np.array([[0, 0], [-t_, 0]]), x)[0, 1])
             and np.allclose(np.linalg.eigvalsh(Hp(x)), np.array([-1, 1]) * np.sqrt(D ** 2 + 2 * t_ ** 2 * (1 + np.cos(x))))
             for x in f)
    ok = ok and np.isclose(np.diff(np.linalg.eigvalsh(Hp(np.pi)))[0], 2 * abs(D)) \
        and np.allclose(np.linalg.eigvalsh(Hp(np.pi)), [-abs(D), abs(D)]) \
        and np.allclose(np.linalg.eigvalsh(Hp(0.0)), [-np.sqrt(D ** 2 + 4 * t_ ** 2), np.sqrt(D ** 2 + 4 * t_ ** 2)])
    check(f'problem, t={t_} Delta={D}: H(phi), the bands, +-|Delta| and the gap 2|Delta| at pi, '
          f'+-sqrt(Delta^2+4t^2) at 0', ok, np.diff(np.linalg.eigvalsh(Hp(np.pi)))[0])
Hq = lambda t_, D, x: np.array([[D, -t_ * (1 + np.exp(-1j * x))], [-t_ * (1 + np.exp(1j * x)), -D]])
gq = lambda t_, D: np.diff(np.linalg.eigvalsh(Hq(t_, D, np.pi)))[0]
check('problem: t=0.7, Delta=-0.4 gives the gap 0.8 = 2|Delta| at pi', np.isclose(gq(0.7, -0.4), 0.8), gq(0.7, -0.4))
check('problem: for Delta=0 the gap at pi is zero, so the insulator needs Delta not zero',
      np.isclose(gq(1.0, 0.0), 0, atol=1e-12), gq(1.0, 0.0))
check('problem: |1 + e^{-i phi}|^2 = 2 + 2 cos(phi)', np.allclose(abs(1 + np.exp(-1j * f)) ** 2, 2 + 2 * np.cos(f)), 'ok')
check('problem: Delta = 0 gives +-2t|cos(phi/2)|, touching at pi', np.allclose(np.sqrt(2 * (1 + np.cos(f))),
      2 * abs(np.cos(f / 2))) and np.isclose(np.sqrt(2 * (1 + np.cos(np.pi))), 0, atol=1e-7), 'ok')
hp = geometry.bichain().get_hamiltonian(has_spin=False)
hp.intra = -hp.intra; hp.inter = -hp.inter
hp.add_sublattice_imbalance(0.3)
hkp = hp.get_hk_gen()
check('problem: pyqula bichain with -1 hoppings and the imbalance 0.3 gives the gap 0.6 at pi and the bands',
      np.isclose(np.diff(np.linalg.eigvalsh(hkp([0.5, 0, 0])))[0], 0.6) and all(np.allclose(
          np.linalg.eigvalsh(hkp([x / (2 * np.pi), 0, 0])), np.array([-1, 1]) * np.sqrt(0.09 + 2 * (1 + np.cos(x))))
          for x in f), 'ok')
# the closing sentence: in Session 3 a staggered potential opens the gap of the honeycomb lattice at its Dirac points
hh = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False)
hh.add_sublattice_imbalance(0.5)
hkh, B = physcheck.from_pyqula(hh)
K = (B[0] + B[1]) / 3
check('problem: a staggered potential 0.5 opens the gap 1.0 of the honeycomb lattice at K',
      np.isclose(np.diff(np.linalg.eigvalsh(hkh(K)))[0], 1.0) and np.isclose(physcheck.gap(hkh, B, 1, nk=60), 1.0, atol=1e-6),
      np.diff(np.linalg.eigvalsh(hkh(K)))[0])
