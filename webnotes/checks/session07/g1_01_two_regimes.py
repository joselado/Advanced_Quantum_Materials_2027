"""Session 7, the statements of page 01 (Sections 7.1 and 7.2a).

It checks the reordering of the fold, from the order c^dag c^dag c c of (1.5) to the order c^dag c c^dag c of (7.1),
by two routes: the identity of four operators on random modes, and a random V of (7.1) written in the form (1.5) with
the relabeled and sign-changed V and the extra hopping. It checks the problem on two spins in a product state, the
numbers -1/4 and -3/4 of the first quiz, the rules of the second quiz as matrices, and the ratio of the lab box. Since
2026-11-22 the first quiz, the index page and the first bullet of 7.12 say that mean field converges to a magnetic order
and not to zero, and the Weiss decoupling below checks it on the dimer and on the triangular lattice.
It needs numpy only and writes no file."""
import itertools
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def modes(n):
    """Annihilation operators of n spinless fermionic modes, with the Jordan-Wigner order."""
    a = np.array([[0., 1.], [0., 0.]])
    Z = np.diag([1., -1.])
    ops = []
    for i in range(n):
        m = np.eye(1)
        for j in range(n):
            m = np.kron(m, Z if j < i else (a if j == i else np.eye(2)))
        ops.append(m)
    return ops


d = lambda m: m.conj().T
c = modes(4)
I = np.eye(16)

# route 1, the identity of the fold for every choice of four indices out of four modes
ok = True
for i, j, k, l in itertools.product(range(4), repeat=4):
    lhs = d(c[i]) @ c[j] @ d(c[k]) @ c[l]
    rhs = (j == k) * d(c[i]) @ c[l] - d(c[i]) @ d(c[k]) @ c[j] @ c[l]
    ok = ok and np.allclose(lhs, rhs)
check('c_i^dag c_j c_k^dag c_l = delta_jk c_i^dag c_l - c_i^dag c_k^dag c_j c_l, all 256 index choices', ok, 'ok')

# route 2, a random V of (7.1) on 4 modes is the form (1.5) with V'_abcd = -V_acbd and the hopping sum_j V_ijjl
rng = np.random.default_rng(7)
V = rng.normal(size=(4, 4, 4, 4)) + 1j * rng.normal(size=(4, 4, 4, 4))
H71 = sum(V[i, j, k, l] * d(c[i]) @ c[j] @ d(c[k]) @ c[l] for i, j, k, l in itertools.product(range(4), repeat=4))
Vp = -np.transpose(V, (0, 2, 1, 3))
tp = np.einsum('ijjl->il', V)
H15 = sum(Vp[a, b, e, f] * d(c[a]) @ d(c[b]) @ c[e] @ c[f] for a, b, e, f in itertools.product(range(4), repeat=4))
H15 = H15 + sum(tp[i, l] * d(c[i]) @ c[l] for i in range(4) for l in range(4))
check('the sentence after (7.1): the quartic term is (1.5) with the two middle indices of V exchanged and a minus sign, plus a hopping', np.allclose(H71, H15),
      np.abs(H71 - H15).max())
# without the minus sign the two forms differ, so the sign is needed
H15wrong = -sum(Vp[a, b, e, f] * d(c[a]) @ d(c[b]) @ c[e] @ c[f] for a, b, e, f in itertools.product(range(4), repeat=4))
H15wrong = H15wrong + sum(tp[i, l] * d(c[i]) @ c[l] for i in range(4) for l in range(4))
check('with the opposite sign the two forms differ', not np.allclose(H71, H15wrong), np.abs(H71 - H15wrong).max())

# two spins 1/2, S = sigma/2
sx = np.array([[0, 1], [1, 0]]) / 2
sy = np.array([[0, -1j], [1j, 0]]) / 2
sz = np.diag([.5, -.5])
SS = sum(np.kron(s, s) for s in (sx, sy, sz))


def spinor(n):
    """The spin 1/2 state that points along the unit vector n."""
    th, ph = np.arccos(n[2]), np.arctan2(n[1], n[0])
    return np.array([np.cos(th / 2), np.exp(1j * ph) * np.sin(th / 2)])


# the problem, <S_1.S_2> = n_1.n_2/4 for a product state, and <S> = n/2 on one site
ok = True
for _ in range(20):
    n1, n2 = rng.normal(size=3), rng.normal(size=3)
    n1, n2 = n1 / np.linalg.norm(n1), n2 / np.linalg.norm(n2)
    u1, u2 = spinor(n1), spinor(n2)
    psi = np.kron(u1, u2)
    ok = ok and abs(np.vdot(psi, SS @ psi) - n1 @ n2 / 4) < 1e-12
    ok = ok and np.allclose([np.vdot(u1, s @ u1).real for s in (sx, sy, sz)], n1 / 2)
check('<S_1.S_2> = n_1.n_2/4 for 20 random product states, and <S> = n/2', ok, 'ok')
up, dn = np.array([1., 0]), np.array([0., 1])
check('antiparallel spins give -1/4', abs(np.kron(up, dn) @ SS @ np.kron(up, dn) + 0.25) < 1e-12, -0.25)
sing = (np.kron(up, dn) - np.kron(dn, up)) / np.sqrt(2)
check('the singlet gives -3/4', abs(sing @ SS @ sing + 0.75) < 1e-12, -0.75)
check('the singlet is an eigenstate of S_1.S_2', np.allclose(SS @ sing, -0.75 * sing), 'ok')
# the identity of the solution, S_1.S_2 = (S_tot^2 - 3/2)/2, gives -3/4 for S_tot = 0 and 1/4 for S_tot = 1
Stot2 = sum((np.kron(s, np.eye(2)) + np.kron(np.eye(2), s)) @ (np.kron(s, np.eye(2)) + np.kron(np.eye(2), s))
            for s in (sx, sy, sz))
check('S_1.S_2 = (S_tot^2 - 3/2)/2', np.allclose(SS, (Stot2 - 1.5 * np.eye(4)) / 2), 'ok')
check('the levels of S_1.S_2 are -3/4 once and 1/4 three times', np.allclose(np.linalg.eigvalsh(SS), [-.75, .25, .25, .25]),
      np.round(np.linalg.eigvalsh(SS), 6))
check('<S^z_1> = 0 in the singlet', abs(sing @ np.kron(sz, np.eye(2)) @ sing) < 1e-12, 0)
# the solution of the problem, each spin has S_i^2 = 3/4
check('S_i^2 = 3/4 for a spin 1/2', np.allclose(sum(s @ s for s in (sx, sy, sz)), 0.75 * np.eye(2)), 0.75)


def heisenberg_open(L):
    """The open Heisenberg chain J sum_i S_i.S_{i+1} with J = 1, and the spin operators S[a][i], a = x, y, z."""
    def site(op, i):
        out = np.eye(1)
        for j in range(L):
            out = np.kron(out, op if j == i else np.eye(2))
        return out
    S = [[site(s, i) for i in range(L)] for s in (sx, sy, sz)]
    H = sum(S[a][i] @ S[a][i + 1] for a in range(3) for i in range(L - 1))
    return H, S


# first quiz, second feedback, <S^z_i> = 0 on both sites of the singlet, and also on every site of the singlet ground
# state of open chains of 4 to 8 sites
ok, vals = True, []
for Lc in (2, 4, 6, 8):
    Hc, Sc = heisenberg_open(Lc)
    e, v = np.linalg.eigh(Hc)
    g0 = v[:, 0]
    Stot2 = sum(sum(Sc[a]) @ sum(Sc[a]) for a in range(3))
    ok = ok and e[1] - e[0] > 1e-6 and abs(g0.conj() @ Stot2 @ g0) < 1e-10          # a unique ground state, a singlet
    ok = ok and max(abs(g0.conj() @ z @ g0) for z in Sc[2]) < 1e-12
    vals.append(round(e[0], 6))
check('<S^z_i> = 0 on every site of the singlet ground state of open chains of 2, 4, 6 and 8 sites', ok, vals)

# the opener, the lab box, the first quiz and the index page, mean field orders. The Weiss decoupling of J S_i.S_j at zero temperature puts each <S_i>
# antiparallel to the field of its neighbors, with |<S_i>| = 1/2. Started from random <S_i> of size 1e-3 it does not
# stay at zero: the dimer goes to antiparallel spins at -J/4, and the three sublattices of the triangular lattice, each
# site with 3 neighbors on each of the two other sublattices, go to the 120 degree state at -3J/8 per site.
unit = lambda v: v / np.linalg.norm(v)
ok, Es = True, []
for seed in range(5):
    r = np.random.default_rng(seed)
    m = [1e-3 * r.normal(size=3) for _ in range(2)]
    for _ in range(20):
        m[0] = -0.5 * unit(m[1])
        m[1] = -0.5 * unit(m[0])
    ok = ok and np.allclose([np.linalg.norm(x) for x in m], 0.5) and abs(m[0] @ m[1] + 0.25) < 1e-12
    Es.append(round(m[0] @ m[1], 12))
check('first quiz and opener: Weiss mean field of the dimer, 5 random starts of size 1e-3, |<S_i>| = 1/2, antiparallel, E = -J/4', ok, Es)
ok, Es = True, []
for seed in range(5):
    r = np.random.default_rng(seed)
    m = [1e-3 * r.normal(size=3) for _ in range(3)]
    for _ in range(500):
        for a in range(3):
            m[a] = -0.5 * unit(3 * sum(m[b] for b in range(3) if b != a))
    E = m[0] @ m[1] + m[1] @ m[2] + m[0] @ m[2]               # 3 bonds per site, one of each pair of sublattices
    cosines = [unit(m[a]) @ unit(m[b]) for a, b in ((0, 1), (1, 2), (0, 2))]
    ok = ok and np.allclose([np.linalg.norm(x) for x in m], 0.5) and np.allclose(cosines, -0.5) and abs(E + 0.375) < 1e-10
    Es.append(round(E, 10))
check('first quiz and index: Weiss mean field of the triangular lattice, 5 random starts of size 1e-3, |<S_i>| = 1/2, the 120 degree state, E = -3J/8 per site', ok, Es)

# first quiz, option 1: zero solves the self-consistent equations, but the loop leaves it. The Weiss equation of the dimer
# at a temperature T, <S_a> = -(1/2) tanh(|h_a|/2T) h_a/|h_a| with h_a = J <S_b>, keeps <S> = 0 exactly, while a start of
# size 1e-3 ends at |<S>| = (1/2) tanh(|<S>|/2T), close to 1/2 at T = 0.05 J, below the mean-field T_N = J/4 of the dimer
def weiss_dimer(m, T, steps=400):
    m = [x.copy() for x in m]
    for _ in range(steps):
        for a in range(2):
            h = m[1 - a]
            nh = np.linalg.norm(h)
            m[a] = np.zeros(3) if nh == 0 else -0.5 * np.tanh(nh / (2 * T)) * h / nh
    return m
zero = weiss_dimer([np.zeros(3), np.zeros(3)], 0.05)
small = weiss_dimer([1e-3 * np.random.default_rng(3).normal(size=3) for _ in range(2)], 0.05)
mag = [np.linalg.norm(x) for x in small]
check('first quiz, option 1: at T = 0.05 J zero stays zero, and a start of size 1e-3 goes to the antiparallel solution of '
      '|<S>| = (1/2) tanh(|<S>|/2T), close to 1/2',
      all(np.linalg.norm(x) == 0 for x in zero) and all(abs(x - 0.5 * np.tanh(x / 0.1)) < 1e-12 for x in mag)
      and min(mag) > 0.499 and small[0] @ small[1] < 0, [round(x, 6) for x in mag])

# the index page, which names herbertsmithite: on a kagome torus of 4 x 4 cells, 48 sites with 4 neighbors each, the same
# loop from random starts of size 1e-3 also ends with |<S_i>| = 1/2, at the classical energy -J/4 per site, where every
# triangle has the total spin zero
nk = 4
kidx = lambda x, y, s: 3 * ((x % nk) * nk + (y % nk)) + s
kb = set()
for x in range(nk):
    for y in range(nk):
        for tri in ((kidx(x, y, 0), kidx(x, y, 1), kidx(x, y, 2)), (kidx(x, y, 0), kidx(x - 1, y, 1), kidx(x, y - 1, 2))):
            for i_, j_ in ((0, 1), (1, 2), (0, 2)):
                kb.add(tuple(sorted((tri[i_], tri[j_]))))
Nk = 3 * nk * nk
knb = [[] for _ in range(Nk)]
for i_, j_ in kb:
    knb[i_].append(j_); knb[j_].append(i_)
ok, Es = all(len(v) == 4 for v in knb) and len(kb) == 2 * Nk, []
for seed in range(3):
    mk = 1e-3 * np.random.default_rng(seed).normal(size=(Nk, 3))
    for _ in range(3000):
        for i_ in range(Nk):
            mk[i_] = -0.5 * unit(mk[knb[i_]].sum(0))
    Ek = sum(mk[i_] @ mk[j_] for i_, j_ in kb) / Nk
    ok = ok and np.allclose(np.linalg.norm(mk, axis=1), 0.5) and abs(Ek + 0.25) < 1e-6
    Es.append(round(Ek, 8))
check('index: Weiss mean field of a kagome torus of 48 sites, 3 random starts of size 1e-3, |<S_i>| = 1/2, E = -J/4 per site',
      ok, Es)

# second quiz, the rules of two different sites
c2 = modes(2)
sp = np.array([[0., 1.], [0., 0.]])                   # S^+ in the basis (up, down), up is the occupied site
S1p, S2p = np.kron(sp, np.eye(2)), np.kron(np.eye(2), sp)
check('c_1^dag c_2^dag = -c_2^dag c_1^dag', np.allclose(d(c2[0]) @ d(c2[1]), -d(c2[1]) @ d(c2[0])), 'ok')
check('c_1^dag c_2^dag is not zero', np.abs(d(c2[0]) @ d(c2[1])).max() > 0.5, 1)
check('S_1^+ S_2^+ = S_2^+ S_1^+', np.allclose(S1p @ S2p, S2p @ S1p), 'ok')
check('(S^+)^2 = 0 and (c^dag)^2 = 0 on one site', np.allclose(sp @ sp, 0) and np.allclose(d(c2[0]) @ d(c2[0]), 0), 'ok')
check('S^z = n - 1/2 on one site, with up the occupied state', np.allclose(sz, sp @ sp.T - 0.5 * np.eye(2)), 'ok')

# the lab box quotes J ~ 250 K and 32 mK, and the source says four orders of magnitude
check('250 K / 32 mK is about 10^4', 3.5 < np.log10(250 / 0.032) < 4.5, 250 / 0.032)
check('four orders of magnitude, log10(250 K / 32 mK) rounds to 4', round(np.log10(250 / 0.032)) == 4,
      round(np.log10(250 / 0.032), 3))

# our reading in the lab box: the Weiss mean field of the triangular Heisenberg antiferromagnet orders at a temperature of
# the order of J, k T_N = S(S+1)|J(Q)|/3 with J(Q) = J sum_delta cos(Q.delta) = -3J at the 120 degree wave vector K
a1, a2 = np.array([1., 0.]), np.array([0.5, np.sqrt(3) / 2])
deltas = [a1, a2, a2 - a1, -a1, -a2, a1 - a2]
Q = np.array([4 * np.pi / 3, 0.])
JQ = sum(np.cos(Q @ dl) for dl in deltas)
TN = 0.5 * 1.5 * abs(JQ) / 3
check('the 120 degree order has J(Q) = -3J, and the mean-field T_N = S(S+1)J = 0.75 J', abs(JQ + 3) < 1e-12 and abs(TN - 0.75) < 1e-12, TN)
# the solution of the problem, mean field misses J/2 of the energy of the Heisenberg dimer J S_1.S_2
check('the best product state misses (-1/4) - (-3/4) = 1/2 in units of J', abs((-0.25) - (sing @ SS @ sing) - 0.5) < 1e-12, 0.5)
