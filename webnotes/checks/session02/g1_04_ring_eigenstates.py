"""Session 2, the numbers that page 04 (Section 2.4) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The ring of five sites of the schematic ring_long_range is asserted in its figure
script, on the matrices of the pyqula script g1_ring_five_sites.py, and the phases of the ring of six sites in
ring_six_phases.py. This script holds the rest. It needs numpy only and writes no file.

The direction of the rotation is an open point of the plan, so every statement here is checked for the rotation in
both senses. The text says that the weight 1/5 holds for every state of the ring of five sites with the plus sign. With
that sign the lowest level is degenerate, and the weight holds for the Fourier modes of the level and not for every
combination of them, which is the third open point of the plan. This script asserts the weight of the modes only."""
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def shift(L):
    return np.roll(np.eye(L), 1, axis=0)                   # (R psi)_j = psi_{j-1}, its transpose is the other sense


def factor(R, v):
    lam = (v.conj() @ R @ v) / (v.conj() @ v)
    return lam if np.allclose(R @ v, lam * v) else None


def ring(L, hops):
    """The ring of L sites, hops[n-1] the matrix element to the neighbor at distance n."""
    S = shift(L)
    H = np.zeros((L, L))
    for n, t in enumerate(hops, 1):
        P = np.linalg.matrix_power(S, n)
        H = H + t * (P + P.T)
    return H


def mode(L, phi):
    return np.exp(1j * phi * np.arange(L)) / np.sqrt(L)


rng = np.random.default_rng(5)


def random_symmetric(L):
    """A random Hamiltonian that commutes with the rotation of a ring of L sites, complex hoppings included."""
    c = rng.normal(size=L) + 1j * rng.normal(size=L)
    H = sum(c[n] * np.linalg.matrix_power(shift(L), n) for n in range(L))
    return H + H.conj().T


# (2.4) and the key box: R^L = 1 and the phases 2 pi n / L, for L = 3 and the L = 3, 5 of Figure 2.1
for L in (3, 5, 6):
    R = shift(L)
    ev = np.linalg.eigvals(R)
    ph = np.sort(np.mod(np.angle(ev), 2 * np.pi))
    check('ring of %d sites: R^L = 1 and the phases 2 pi n / L' % L,
          np.allclose(np.linalg.matrix_power(R, L), np.eye(L)) and np.allclose(ph, 2 * np.pi * np.arange(L) / L, atol=1e-9),
          np.round(ph / np.pi, 4))

# the key box: modulo 2 pi the phases 2 pi n / L, n = 0..L-1, are the same set as the L phases in (-pi, pi] of (2.2),
# and 4 pi/3 of (2.4) is the phase -2 pi/3
ok = True
for L in (3, 4, 5, 6):
    full = 2 * np.pi * np.arange(L) / L
    folded = np.angle(np.exp(1j * full))
    folded = np.where(np.isclose(folded, -np.pi), np.pi, folded)                # numpy may give -pi for pi
    ok = ok and np.all(folded > -np.pi) and np.all(folded <= np.pi + 1e-12)
    ok = ok and np.allclose(np.sort(np.mod(folded, 2 * np.pi)), np.sort(np.mod(full, 2 * np.pi)))
    ok = ok and len(set(np.round(folded, 9))) == L and np.allclose(np.exp(1j * L * folded), 1)
ok = ok and np.isclose(np.exp(4j * np.pi / 3), np.exp(-2j * np.pi / 3)) and 4 * np.pi / 3 > np.pi
ok = ok and np.isclose(np.angle(np.exp(4j * np.pi / 3)), -2 * np.pi / 3)
check('L = 3 to 6: 2 pi n/L, n = 0..L-1, equal modulo 2 pi the L phases in (-pi, pi], and 4 pi/3 is -2 pi/3', ok,
      np.round(np.angle(np.exp(2j * np.pi * np.arange(3) / 3)) / np.pi, 4))

# the key box and the steps: every Fourier mode is an eigenstate of every H that keeps the rotation, in both senses,
# with the weight 1/L, and the L modes have L different eigenvalues of R
ok = True
for L in (3, 4, 5, 6):
    H = random_symmetric(L)
    R = shift(L)
    ok = ok and np.allclose(H @ R, R @ H)
    lams = []
    for n in range(L):
        v = mode(L, 2 * np.pi * n / L)
        ok = ok and factor(H, v) is not None and np.allclose(np.abs(v) ** 2, 1 / L)
        for Rs in (R, R.T):
            mu = factor(Rs, v)
            ok = ok and mu is not None and np.isclose(abs(mu), 1)
        mu = factor(R, v)
        lam = v[1] / v[0]
        ok = ok and (np.isclose(lam, mu) or np.isclose(lam, 1 / mu)) and np.isclose(lam ** L, 1)
        lams.append(mu)
    ok = ok and len(set(np.round(lams, 9))) == L
check('Fourier modes on 3 to 6 sites: eigenstates of random H with the rotation, weight 1/L, the neighbor ratio is mu or 1/mu, '
      'L different eigenvalues of R', ok, True)
check('the weight on five sites is 1/5', np.allclose(np.abs(mode(5, 2 * np.pi * 2 / 5)) ** 2, 0.2), 0.2)

# the quiz on six sites: (1,-1,1,-1,1,-1) has -1, phi = pi, and pi/6 gives lambda^6 = -1
alt = np.array([1, -1, 1, -1, 1, -1], complex)
check('(1,-1,1,-1,1,-1) has the eigenvalue -1 in both senses, and exp(i pi/6)^6 = -1',
      all(np.isclose(factor(Rs, alt), -1) for Rs in (shift(6), shift(6).T)) and np.isclose(np.exp(1j * np.pi / 6) ** 6, -1),
      True)

# the quiz on the weight: six sites with t = 1 and eta = 0.3, and the mode (1,i,-1,-i)/2 of four sites
H6 = ring(6, [-1.0, -0.3])
ok = all(factor(H6, mode(6, 2 * np.pi * n / 6)) is not None for n in range(6))
check('six sites with eta = 0.3: the Fourier modes are eigenstates with the weight 1/6', ok
      and np.allclose(np.abs(mode(6, 1.0)) ** 2, 1 / 6), True)
q = np.array([1, 1j, -1, -1j]) / 2
check('(1,i,-1,-i)/2 has the weight 1/4 on every site', np.allclose(np.abs(q) ** 2, 0.25), np.abs(q) ** 2)

# the text on five sites with H = sum c^+ c: the Fourier modes are eigenstates with the weight 1/5
Hp = ring(5, [1.0])
ok = all(factor(Hp, mode(5, 2 * np.pi * n / 5)) is not None for n in range(5))
check('five sites with the plus sign: every Fourier mode is an eigenstate with the weight 1/5', ok, True)

# the new quiz on five sites
H5 = ring(5, [-1.0])
good = np.exp(2j * np.pi * np.arange(5) / 5)
bad = np.exp(1j * np.pi * np.arange(5) / 5)
delta = np.eye(5)[0]
ok = all(factor(random_symmetric(5), good) is not None for _ in range(5))
ok = ok and all(factor(Rs, good) is not None for Rs in (shift(5), shift(5).T))
check('exp(2 pi i j/5) is an eigenstate of 5 random H with the rotation and of R in both senses', ok, True)
ratio = (H5 @ bad) / bad
ok = all(factor(Rs, bad) is None for Rs in (shift(5), shift(5).T)) and np.isclose(np.exp(1j * np.pi * 5 / 5), -1)
ok = ok and np.isclose(ratio[1], -1.618, atol=5e-4) and np.isclose(ratio[0], -1.176j, atol=5e-4)
ok = ok and round(ratio[1].real, 2) == -1.62 and round(ratio[0].imag, 2) == -1.18
check('exp(i pi j/5) is not an eigenstate: five steps give -1, and (H a)_j/a_j is -1.62 t on site 1 and -1.18i t on site 0',
      ok, np.round(ratio[:2], 4))
ok = all(factor(Rs, delta) is None for Rs in (shift(5), shift(5).T)) and np.allclose(H5 @ delta, [0, -1, 0, 0, -1])
check('delta_j0 is not an eigenstate, H puts -t on the sites 1 and 4', ok, H5 @ delta)

# the problem: the ring of six sites with -t
e6 = np.sort(np.linalg.eigvalsh(ring(6, [-1.0])))
en = -2 * np.cos(np.pi * np.arange(6) / 3)
ok = np.allclose(e6, [-2, -1, -1, 1, 1, 2]) and np.allclose(en, [-2, -1, 1, 2, 1, -1])
ok = ok and len(np.unique(np.round(e6, 9))) == 4 and np.isclose(e6[:3].sum(), -4) and np.isclose(2 * e6[:3].sum(), -8)
ok = ok and all(factor(ring(6, [-1.0]), mode(6, 2 * np.pi * n / 6)) is not None for n in range(6))
check('six sites: -2t, -t, -t, t, t, 2t, four levels, three spinless electrons -4t, six with spin -8t', ok, e6)
print('all checks of page 04 hold')
