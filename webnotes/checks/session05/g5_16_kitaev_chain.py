"""Session 5, the numbers and the algebra that page 16 (Section 5.16, the Kitaev chain) states and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or in the
figure script that draws it. The levels of the open chain of 20 sites (two at zero, 19 at each of +-2t, half of the zero weight
on site 1 and half on site 20) are asserted in figures/session05/g5_kitaev_sweet_spot.py, and those of the three quiz pictures of
10 sites in figures/session05/g5_quiz_levels_*.py. This script checks the steps fold, the quizzes and the problem with the
operators of a few sites, built with the Jordan-Wigner matrices, and the levels again by a second route, the pyqula chain of
the recipe "The open Kitaev chain and its end modes". pyqula is called with no file written, since only h.intra is read.

Run it from anywhere:  python3 webnotes/checks/session05/g5_16_kitaev_chain.py"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures', 'session05'))
import _g5_kitaev as kc


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def fermions(N):
    """Annihilation operators c_1..c_N on the 2^N states, with the Jordan-Wigner string."""
    a = np.array([[0., 1.], [0., 0.]])
    z, one = np.diag([1., -1.]), np.eye(2)
    ops = []
    for n in range(N):
        m = np.array([[1.]])
        for j in range(N):
            m = np.kron(m, z if j < n else (a if j == n else one))
        ops.append(m)
    return ops


def majoranas(c):
    """gamma_{2n-1} = c_n + c_n^dag and gamma_{2n} = -i(c_n - c_n^dag), as (5.17), in the list g[1..2N] (g[0] unused)."""
    g = [None]
    for cn in c:
        g += [cn + cn.conj().T, -1j * (cn - cn.conj().T)]
    return g


def kitaev(c, t, mu, D):
    """The Hamiltonian (5.19) on an open chain, as a matrix on the Fock space."""
    N = len(c)
    d = lambda o: o.conj().T
    H = sum(-mu * d(cn) @ cn for cn in c)
    for n in range(N - 1):
        H = H - t * (d(c[n]) @ c[n + 1] + d(c[n + 1]) @ c[n]) + D * (c[n] @ c[n + 1] + d(c[n + 1]) @ d(c[n]))
    return H


def close(A, B):
    return np.abs(A - B).max() < 1e-12


# ---- the Majorana operators and (5.18) on two sites
c = fermions(2)
g = majoranas(c)
I = np.eye(4)
ok = all(close(g[i] @ g[i], I) for i in range(1, 5)) and all(close(g[i] @ g[j] + g[j] @ g[i], 0 * I)
                                                              for i in range(1, 5) for j in range(1, 5) if i != j)
check('recall: gamma^2 = 1 and {gamma_i, gamma_j} = 0 for i != j, on two sites', ok, 4)
check('recall: c_n = (gamma_{2n-1} + i gamma_{2n})/2, (5.18)', all(close(c[n], (g[2 * n + 1] + 1j * g[2 * n + 2]) / 2) for n in range(2)), 2)

# ---- the steps fold, one bond first
t, D, mu = 0.83, 0.37, 0.29
hop = -t * (c[0].T @ c[1] + c[1].T @ c[0])
pair = D * (c[0] @ c[1] + c[1].T @ c[0].T)
check('steps: the hopping of one bond is (it/2)(gamma_2 gamma_3 - gamma_1 gamma_4)', close(hop, 0.5j * t * (g[2] @ g[3] - g[1] @ g[4])), t)
check('steps: the pairing of one bond is (i Delta/2)(gamma_2 gamma_3 + gamma_1 gamma_4)', close(pair, 0.5j * D * (g[2] @ g[3] + g[1] @ g[4])), D)
check('steps: one bond is (i/2)(t+Delta) gamma_2 gamma_3 + (i/2)(Delta-t) gamma_1 gamma_4',
      close(hop + pair, 0.5j * (t + D) * g[2] @ g[3] + 0.5j * (D - t) * g[1] @ g[4]), (t, D))
check('steps: -mu c^dag c = -(mu/2)(1 + i gamma_1 gamma_2), which binds the two halves of one site',
      close(-mu * c[0].T @ c[0], -0.5 * mu * (I + 1j * g[1] @ g[2])), mu)
check('steps: c^dag c = (1 + i gamma_{2n-1} gamma_{2n})/2, so i gamma_{2n-1} gamma_{2n} = 2 c^dag c - 1',
      close(1j * g[1] @ g[2], 2 * c[0].T @ c[0] - I), 0)

# ---- the key box (5.21) on a chain of 4 sites, and the case Delta = -t of the quiz
N = 4
c4 = fermions(N)
g4 = majoranas(c4)
for tt in (1.0, 0.6):
    H = kitaev(c4, tt, 0.0, tt)
    H21 = sum(1j * tt * g4[2 * n] @ g4[2 * n + 1] for n in range(1, N))
    free = all(close(H @ g4[i] - g4[i] @ H, 0 * H) for i in (1, 2 * N))
    bound = not any(close(H @ g4[i] - g4[i] @ H, 0 * H) for i in range(2, 2 * N))
    check(f'key: (5.19) at Delta=t={tt}, mu=0 is i t sum gamma_2n gamma_2n+1, and only gamma_1 and gamma_8 commute with it',
          close(H, H21) and free and bound, tt)
H = kitaev(c4, 1.0, 0.0, -1.0)
Hm = sum(-1j * g4[2 * n - 1] @ g4[2 * n + 2] for n in range(1, N))
free = all(close(H @ g4[i] - g4[i] @ H, 0 * H) for i in (2, 2 * N - 1))
check('quiz: at Delta=-t, mu=0 the chain is -i t sum gamma_{2n-1} gamma_{2n+2}, with gamma_2 and gamma_7 free', close(H, Hm) and free, -1)
Hs = sum(1j * g4[2 * n - 1] @ g4[2 * n] for n in range(1, N + 1))
check('quiz: i t sum gamma_{2n-1} gamma_{2n} = 2t sum c^dag c - Nt, the term -mu sum c^dag c with mu=-2t',
      close(Hs, kitaev(c4, 0.0, -2.0, 0.0) - N * np.eye(2**N)), -2)

# ---- the problem: the bond fermion d = (gamma_2n + i gamma_2n+1)/2
dn = (g4[2] + 1j * g4[3]) / 2
Id = np.eye(2**N)
check('problem: d is a fermion, {d, d^dag} = 1 and d^2 = 0', close(dn @ dn.conj().T + dn.conj().T @ dn, Id) and close(dn @ dn, 0 * Id), 1)
check('problem: i t gamma_2n gamma_2n+1 = t (2 d^dag d - 1), levels -t and +t, so filling a bond costs 2t',
      close(1j * g4[2] @ g4[3], 2 * dn.conj().T @ dn - Id), 2)
E = np.linalg.eigvalsh(kitaev(c4, 1.0, 0.0, 1.0))
check('problem: at Delta=t, mu=0 on 4 sites the ground state is -(N-1)t, twice, and the next states are 2t above',
      abs(E[0] + 3) < 1e-12 and abs(E[1] + 3) < 1e-12 and abs(E[2] + 1) < 1e-12, np.round(E[:3], 6))
f = (g4[1] + 1j * g4[2 * N]) / 2
P = np.diag([(-1)**bin(s).count('1') for s in range(2**N)])
check('problem: the end fermion f = (gamma_1 + i gamma_2N)/2 costs no energy, and the two ground states have opposite parity',
      close(kitaev(c4, 1.0, 0.0, 1.0) @ f - f @ kitaev(c4, 1.0, 0.0, 1.0), 0 * Id), 0)
w, v = np.linalg.eigh(kitaev(c4, 1.0, 0.0, 1.0) + 1e-3 * P)
check('problem: the two ground states are one even and one odd', abs(w[1] - w[0] - 2e-3) < 1e-9, round(w[1] - w[0], 6))
# the BdG counting of the solution, on the 20 sites of the figure: N-1 bond fermions give the levels at +2t and -2t, and the single
# mode f gives the two levels at zero, whose eigenvectors are the Nambu vectors of gamma_1 and gamma_2N, the two halves of f
N20 = 20
e20, v20 = np.linalg.eigh(kc.bdg(N20, 1.0, 0.0, 1.0))
zero = v20[:, np.abs(e20) < 1e-12]
g1 = np.r_[np.eye(N20)[0], np.eye(N20)[0]] / np.sqrt(2)
g2N = np.r_[np.eye(N20)[-1], -np.eye(N20)[-1]] / np.sqrt(2)
proj = zero @ zero.conj().T
check('problem: on 20 sites N-1=19 levels at +2t, 19 at -2t, and the two levels at zero span the vectors of gamma_1 and gamma_2N',
      np.sum(np.abs(e20 - 2) < 1e-12) == N20 - 1 and np.sum(np.abs(e20 + 2) < 1e-12) == N20 - 1 and zero.shape[1] == 2
      and np.abs(proj @ g1 - g1).max() < 1e-12 and np.abs(proj @ g2N - g2N).max() < 1e-12, zero.shape[1])

# ---- the BdG matrix of the figures against the many-body levels, on 4 sites
for (mu_, D_) in ((0.0, 1.0), (0.4, 0.7), (2.5, 1.0)):
    e = kc.levels(N, 1.0, mu_, D_)
    pos = np.sort(e)[N:]                                   # the upper half, which holds the zero levels once
    E0 = 0.5 * np.trace(-mu_ * np.eye(N)) - 0.5 * pos.sum()
    combos = np.sort([E0 + sum(pos[j] for j in range(N) if (s >> j) & 1) for s in range(2**N)])
    Emb = np.linalg.eigvalsh(kitaev(c4, 1.0, mu_, D_))
    check(f'figures: the BdG levels of _g5_kitaev give the 16 many-body levels of 4 sites, mu={mu_}, Delta={D_}',
          np.abs(combos - Emb).max() < 1e-12, round(np.abs(combos - Emb).max(), 15))

# ---- the quiz on the flat band, E = 2t for every k at Delta=t, mu=0, with |Delta(k)| = 2 Delta |sin k|
k = np.linspace(-np.pi, np.pi, 1001)
for tt in (1.0, 0.7):
    E = np.sqrt((-2 * tt * np.cos(k))**2 + (2 * tt * np.sin(k))**2)
    check(f'quiz: the bulk band is flat at Delta=t={tt}, mu=0, E = 2t', np.allclose(E, 2 * tt), tt)
check('quiz: at k=0, eps=-2t and Delta(0)=0, at k=pi/2, eps=0 and |Delta|=2t', abs(-2 * np.cos(0) + 2) < 1e-15 and abs(2 * np.sin(np.pi / 2) - 2) < 1e-15, 2)
E = np.sqrt((2 * np.cos(k))**2 + (2 * 0.5 * np.sin(k))**2)
check('quiz: the flat value t would need Delta=t/2, which is not flat, E from t to 2t', abs(E.min() - 1) < 1e-6 and abs(E.max() - 2) < 1e-12,
      (round(E.min(), 4), round(E.max(), 4)))

# ---- a second route for the levels of the figures, the pyqula chain with d=[1,0,0], whose lowest levels are those of (5.19)
from pyqula import geometry


def pyqula_levels(L, mu, delta):
    g = geometry.chain().get_supercell(L)  # L sites
    g.dimensionality = 0  # open chain
    h = g.get_hamiltonian()  # two spins
    h.add_onsite(4.0)  # every energy up by 4
    h.add_exchange([0., 0., 4.])  # spin up 8 above, spin down back to 2 cos k
    h.add_onsite(-mu)  # mu of the spin-down band
    h.add_pairing(mode="pwave", delta=delta, d=[1., 0., 0.])  # the Kitaev pairing Delta = delta
    m = h.intra.todense() if hasattr(h.intra, 'todense') else h.intra
    return np.sort(np.abs(np.linalg.eigvalsh(np.array(m))))


for (L, mu_, D_, n, expect) in ((20, 0.0, 1.0, 4, [0, 0, 2, 2]), (10, 0.0, 1.0, 4, [0, 0, 2, 2]), (10, 2.5, 1.0, 2, [0.7068, 0.7068])):
    a = pyqula_levels(L, mu_, D_)[:n]
    b = np.sort(np.abs(kc.levels(L, 1.0, mu_, D_)))[:n]
    check(f'second route: pyqula and numpy give the lowest levels {expect} for L={L}, mu={mu_}, Delta={D_}',
          np.abs(a - b).max() < 1e-12 and np.abs(a - np.array(expect)).max() < 1e-4, np.round(a, 4))
j = np.arange(1, 11)
e = kc.levels(10, 1.0, 0.0, 0.0)
check('second route: the metal of 10 sites has the levels +-2t cos(pi j/11), the smallest 0.28t, the largest 1.92t',
      np.allclose(np.sort(e), np.sort(np.r_[2 * np.cos(np.pi * j / 11), -2 * np.cos(np.pi * j / 11)])) and
      abs(2 * np.cos(5 * np.pi / 11) - 0.2846) < 1e-4 and abs(2 * np.cos(np.pi / 11) - 1.919) < 1e-3, round(2 * np.cos(5 * np.pi / 11), 4))
print('all checks of page 16 hold')
