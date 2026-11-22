"""Session 2, the numbers that page 04 (Section 2.4) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The ring of five sites of the schematic ring_long_range is asserted in its figure
script, on the matrices of the pyqula script g1_ring_five_sites.py, and the phases of the ring of six sites in
ring_six_phases.py. This script holds the rest. It needs numpy only and writes no file.

The rotation R of the page moves every amplitude to the previous site, (R psi)_j = psi_{j+1}, as in Section 2.3, the
direction that the lecturer picked on 2026-11-22. The statements that do not depend on the direction are still checked
for both senses. With the plus sign of the ring of five sites the lowest level is degenerate, and the weight 1/5 holds
for the Fourier modes of the level and not for every combination of them, which the page says since 2026-11-22. The
same holds for the twofold level of the ring of three sites, which is why the page says "can be chosen as"."""
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def shift(L):
    return np.roll(np.eye(L), -1, axis=0)                  # (R psi)_j = psi_{j+1}, its transpose is the other sense


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
        ok = ok and np.allclose(v[1:], mu * v[:-1]) and np.isclose(mu ** L, 1)             # alpha_{j+1} = mu alpha_j
        ok = ok and np.isclose(mu, np.exp(2j * np.pi * n / L))                               # e^{i phi_n} under R
        ok = ok and np.isclose(factor(R.T, v), np.exp(-2j * np.pi * n / L))                  # e^{-i phi_n} in the other sense
        lams.append(mu)
    ok = ok and len(set(np.round(lams, 9))) == L
check('Fourier modes on 3 to 6 sites: eigenstates of random H with the rotation, weight 1/L, alpha_(j+1) = mu alpha_j, '
      'the eigenvalue e^(i phi_n) under the R of the page and e^(-i phi_n) in the other sense, L different eigenvalues of R',
      ok, True)
# the text of the three sites: (R psi)_j = psi_(j+1) with psi_4 = psi_1 moves the amplitude of the site 2 to the site 1
R3 = shift(3)
check('three sites: the R of the page takes the amplitude of the site 2 to the site 1 and of the site 1 to the site 3',
      np.allclose(R3 @ np.eye(3)[1], np.eye(3)[0]) and np.allclose(R3 @ np.eye(3)[0], np.eye(3)[2]), True)
# "can be chosen as", the decision of 2026-11-22, in the text and since the recheck d1 also in the caption of Figure 2.1:
# with a real hopping the modes n = 1 and 2 of three sites have the same energy, so the real state (2,-1,-1)/sqrt6 is
# also an eigenstate, and it is not an eigenstate of R and has the weight 2/3 on one site, not 1/3. Here ring(3, [t])
# has the matrix element t, so the twofold level is -t, and for the hopping -t of (2.5) with t = 1, which is t = -1
# below, the levels are -2, 1, 1 and the twofold level is +t.
e3n = np.linalg.eigvalsh(ring(3, [-1.0]))
check('three sites with the hopping -t of (2.5), t = 1: the levels are -2t, t, t, so the twofold level is +t',
      np.allclose(e3n, [-2, 1, 1]) and np.allclose(ring(3, [-1.0]) @ (np.array([2, -1, -1]) / np.sqrt(6)),
                                                   np.array([2, -1, -1]) / np.sqrt(6)), np.round(e3n, 6))
ok = True
for t in (1.0, -1.0, 0.4):
    H3 = ring(3, [t])
    w = np.array([2, -1, -1]) / np.sqrt(6)
    ok = ok and np.allclose(H3 @ w, -t * w) and factor(R3, w) is None and np.isclose(w[0] ** 2, 2 / 3)
    e3 = np.linalg.eigvalsh(H3)
    ok = ok and np.isclose(np.sort(e3)[1], -t) and np.sum(np.isclose(e3, -t)) == 2           # the level -t holds two
check('three sites with a real hopping: (2,-1,-1)/sqrt6 is an eigenstate of the twofold level, not of R, with the weight '
      '2/3 on site 1, so the eigenstates can be chosen as the Fourier modes and are not all of them', ok, True)
# the ring of six sites with long-range couplings, which the text keeps: real hoppings to the neighbors at distance 1, 2
# and 3, and every Fourier mode is an eigenstate with the weight 1/6
H6l = ring(6, [-1.0, -0.4, 0.3])
check('six sites with long-range couplings: every Fourier mode is an eigenstate, with the weight 1/6',
      all(factor(H6l, mode(6, 2 * np.pi * n / 6)) is not None for n in range(6)), np.round(np.linalg.eigvalsh(H6l), 3))
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
# the old text, corrected on 2026-11-22 with "once we choose the eigenstates as these Fourier modes": with the plus sign
# the lowest level of five sites, 2cos(4 pi/5), holds two modes, and their real combination cos(4 pi j/5) is also an
# eigenstate of that level, whose weight on site 1 is not 1/5. So the weight 1/5 holds for the Fourier modes.
ep = np.linalg.eigvalsh(Hp)
cr = np.cos(4 * np.pi * np.arange(5) / 5); cr = cr / np.linalg.norm(cr)
check('five sites with the plus sign: the lowest level is 2cos(4pi/5) twice, and its real eigenstate cos(4 pi j/5) has '
      'the weight of site 1 different from 1/5', np.allclose(ep[:2], 2 * np.cos(4 * np.pi / 5)) and ep[2] - ep[1] > 0.1
      and np.allclose(Hp @ cr, ep[0] * cr) and not np.isclose(cr[1] ** 2, 0.2), np.round(cr ** 2, 3))
# the quiz on the weight, corrected on 2026-11-22 with "can be chosen as": six sites with eta = 0.3 have the levels
# -0.7 and 1.3 twice, and cos(2 pi j/6) is an eigenstate at -0.7 with the weights 1/3 and 1/12, not 1/6
e6w = np.linalg.eigvalsh(H6)
c6 = np.cos(2 * np.pi * np.arange(6) / 6); c6 = c6 / np.linalg.norm(c6)
check('six sites with eta = 0.3: two levels hold two states, and the real eigenstate cos(2 pi j/6) at -0.7 has the '
      'weights 1/3 and 1/12, so the weight 1/6 holds for the Fourier modes', np.allclose(e6w, [-2.6, -0.7, -0.7, 1.3, 1.3, 1.4])
      and np.allclose(H6 @ c6, -0.7 * c6) and np.allclose(c6 ** 2, [1 / 3, 1 / 12, 1 / 12, 1 / 3, 1 / 12, 1 / 12]),
      np.round(c6 ** 2, 4))

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

# the sentence on STM, decided on 2026-11-22: it says only what the stored nilius2002 says, that STM places single atoms
# and builds gold chains, which are then measured. The tracked file keeps the title, the full copy, which git ignores,
# the whole abstract.
import os
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'sources')
tracked = ' '.join(open(os.path.join(src, 'session02', 'nilius2002_science.1075242.txt'), encoding='utf-8').read().split())
check('STM sentence, the tracked file of nilius2002 has the title on artificial gold chains and the URL of the page',
      'Artificial Gold Chains' in tracked and 'https://www.science.org/doi/10.1126/science.1075242' in tracked, 'found')
full = os.path.join(src, '.full', 'session02', 'nilius2002_science.1075242.txt')
if os.path.exists(full):
    text = ' '.join(open(full, encoding='utf-8').read().split())
    for phrase in ('to manipulate single atoms is used to build well-defined gold chains',
                   'Spatially resolved conductance measurements along a 20-atom chain'):
        check('STM sentence, the full copy of nilius2002 says "%s"' % phrase, phrase in text, 'found')
else:
    print('NOT CHECKED the abstract of nilius2002, no full copy of the source on this machine', flush=True)
print('all checks of page 04 hold')
