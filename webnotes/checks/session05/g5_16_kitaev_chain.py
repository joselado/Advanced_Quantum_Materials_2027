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
# the third feedback, corrected on 2026-11-22: "No Delta gives a band flat at t, since at k=0 the pairing vanishes and E=2t for
# any Delta". First route, the formula at mu=0, E(0) = |2t cos 0| = 2t. Second route, the levels of the BdG matrix of a ring of
# 16 sites, which hold the level 2t of k=0 for every Delta, while the band is flat only at Delta=t, where it is at 2t
for D_ in (0.2, 0.5, 1.0, 1.5):
    E = np.sqrt((2 * np.cos(k))**2 + (2 * D_ * np.sin(k))**2)
    Nr = 16
    hr, dr = np.zeros((Nr, Nr)), np.zeros((Nr, Nr))
    for n in range(Nr):
        m = (n + 1) % Nr
        hr[n, m] = hr[m, n] = -1.0
        dr[m, n], dr[n, m] = D_, -D_
    er = np.abs(np.linalg.eigvalsh(np.block([[hr, dr], [dr.T, -hr]])))
    flat = E.max() - E.min() < 1e-12
    check(f'quiz: at Delta={D_}t and mu=0, E(k=0) = 2t by the formula and on a ring, and the band is flat only at Delta=t',
          abs(E[np.argmin(np.abs(k))] - 2) < 1e-12 and np.min(np.abs(er - 2)) < 1e-12 and flat == (D_ == 1.0),
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

# ---- the sentence after (5.20), the lecturer's pick of 2026-11-22: "The sign of i is a gauge choice, Delta -> -Delta, and the
# spectrum depends only on 2|Delta sin k|". First route, a ring of 24 sites at mu=0.7 and Delta=0.35: the levels for +Delta and
# -Delta are the same, and they are +-sqrt(eps^2 + 4 Delta^2 sin^2 k). Second route, the 2x2 block at three momenta with
# +2i Delta sin k, -2i Delta sin k and the real 2 Delta |sin k|, which have the same modulus. Third route, the gauge c_n -> i c_n
# is the unitary diag(i, -i) of the Nambu basis, and it turns the BdG matrix of Delta into the one of -Delta.
def ring(Nr, t, mu, D):
    hr, dr = np.zeros((Nr, Nr)), np.zeros((Nr, Nr))
    for n in range(Nr):
        m = (n + 1) % Nr
        hr[n, m] = hr[m, n] = -t
        dr[m, n], dr[n, m] = D, -D
    hr -= mu * np.eye(Nr)
    return np.block([[hr, dr], [dr.T, -hr]])


Nr, mu_, D_ = 24, 0.7, 0.35
ep, em = np.linalg.eigvalsh(ring(Nr, 1.0, mu_, D_)), np.linalg.eigvalsh(ring(Nr, 1.0, mu_, -D_))
kr = 2 * np.pi * np.arange(Nr) / Nr
Ek = np.sqrt((2 * np.cos(kr) + mu_)**2 + 4 * D_**2 * np.sin(kr)**2)
check('after (5.20): on a ring of 24 sites, mu=0.7, Delta=+-0.35 give the same levels, +-sqrt((2t cos k + mu)^2 + 4 Delta^2 sin^2 k)',
      np.abs(ep - em).max() < 1e-12 and np.abs(np.sort(np.r_[Ek, -Ek]) - ep).max() < 1e-12, round(np.abs(ep - em).max(), 15))
ok = True
for kk in (0.3, 1.1, 2.5):
    eps_ = -2 * np.cos(kk) - mu_
    lev = [np.linalg.eigvalsh(np.array([[eps_, dk], [np.conj(dk), -eps_]])) for dk in
           (2j * D_ * np.sin(kk), -2j * D_ * np.sin(kk), 2 * D_ * abs(np.sin(kk)))]
    ok = ok and all(np.allclose(l, lev[0], atol=1e-12) for l in lev) and np.allclose(lev[0][1], np.hypot(eps_, 2 * D_ * np.sin(kk)))
check('after (5.20): the block with +2i Delta sin k, -2i Delta sin k or 2 Delta |sin k| has the same two levels at k = 0.3, 1.1, 2.5',
      ok, 3)
Ug = np.diag(np.r_[1j * np.ones(8), -1j * np.ones(8)])
check('after (5.20): the gauge c_n -> i c_n turns the open chain of Delta=0.3 into the one of Delta=-0.3, mu=0.4, 8 sites',
      np.abs(Ug @ kc.bdg(8, 1.0, 0.4, 0.3) @ Ug.conj().T - kc.bdg(8, 1.0, 0.4, -0.3)).max() < 1e-15, 0)

# ---- the notebook box, rewritten on 2026-11-22 to match its cell. The cell "Emergence of Majorana modes as a function of the
# size of the superconductor" builds the chain of L sites with add_onsite(mu) and add_pairing(mode="pwave", delta=Delta,
# d=[1,1,0]), at Delta = 0.1 and mu = 0.3, for L from 4 to 40. With the conventions sheet this is (5.19) with t=1,
# mu = -0.3 and Delta = 0.1 |1 + i| = 0.14. First route, the text of the cell. Second route, its pyqula chain against the exact
# chain of _g5_kitaev, for every L of the cell. At Delta=t, mu=0 the two lowest levels are zero for every L of the cell, and at
# the values of the cell they come down from 0.29 at L=4 to below 0.002 at L=40, with oscillations.
import json
nb = json.load(open(os.path.join(HERE, '..', '..', '..', 'jupyter-notebooks', 'session5.ipynb'), encoding='utf-8'))
cells = [''.join(x['source']) for x in nb['cells']]
head = [i for i, s in enumerate(cells) if s.startswith('## Emergence of Majorana modes as a function of the size of the superconductor')]
code = cells[head[0] + 1]
check('notebook box: the cell has Delta = 0.1, mu = 0.3, add_onsite(mu), d=[1.,1.,0.] and the lengths range(4,42,2)',
      len(head) == 1 and 'Delta = 0.1 ' in code and 'mu = 0.3 ' in code and 'h.add_onsite(mu)' in code
      and 'd=[1.,1.,0.]' in code and 'Ls = range(4,42,2)' in code, head)


def cell_levels(L, mu, Delta):
    g = geometry.chain().get_supercell(L)  # the open chain of the cell
    g.dimensionality = 0
    h = g.get_hamiltonian()
    h.add_onsite(4.0); h.add_exchange([0., 0., 4.])
    h.add_onsite(mu)
    h.add_pairing(mode="pwave", delta=Delta, d=[1., 1., 0.])
    m = h.intra.todense() if hasattr(h.intra, 'todense') else h.intra
    return np.sort(np.abs(np.linalg.eigvalsh(np.array(m))))


gs = geometry.chain().get_supercell(4); gs.dimensionality = 0
hs = gs.get_hamiltonian(); hs.add_onsite(4.0); hs.add_exchange([0., 0., 4.]); hs.add_onsite(0.3)
ms = np.array(hs.intra.todense() if hasattr(hs.intra, 'todense') else hs.intra)
check('notebook box: mu = 0.3 of the cell puts the spin-down onsite energy at +0.3, which is -mu c^dag c of (5.19) with mu=-0.3',
      abs(ms[1, 1] - 0.3) < 1e-12 and abs(ms[0, 0] - 8.3) < 1e-12, (ms[1, 1].real, ms[0, 0].real))
Dcell = 0.1 * abs(1 + 1j)
ok, first, last, low = True, None, None, {}
for L in range(4, 42, 2):
    a = cell_levels(L, 0.3, 0.1)[:L]
    b = np.sort(np.abs(kc.levels(L, 1.0, -0.3, Dcell)))[:L]
    z = np.sort(np.abs(kc.levels(L, 1.0, 0.0, 1.0)))[:2]
    ok = ok and np.abs(a - b).max() < 1e-10 and z.max() < 1e-12
    first = a[0] if first is None else first
    last = a[0]
    low[L] = a[0]
check('notebook box: the cell is (5.19) with mu=-0.3 and Delta=0.14 for every L from 4 to 40, and Delta=t, mu=0 has two zero levels '
      'for every L', ok and abs(Dcell - 0.14) < 5e-3, round(Dcell, 4))
check('notebook box: at the values of the cell the lowest level goes from 0.29 at L=4 to below 0.002 at L=40',
      abs(first - 0.285) < 5e-3 and last < 2e-3, (round(first, 4), round(last, 5)))
# corrected after the independent check of 2026-11-22: "There the two states approach zero only as the chain grows, with
# oscillations, since the overlap of the two end modes oscillates with the length of the chain." First route, the levels of the
# cell: the lowest one is not monotonic in L, 0.0126 at L=10 and 0.0449 at L=14, 2.0e-5 at L=30 and 1.65e-3 at L=40. Second route,
# the end mode: at E=0 its Majorana amplitude a_n obeys (t+Delta) a_{n+1} + mu a_n + (t-Delta) a_{n-1} = 0, whose two roots are
# complex for mu^2 < 4(t^2 - Delta^2), with the modulus sqrt((t-Delta)/(t+Delta)) = 0.867, so a_n decays as 0.867^n and oscillates.
# The u+v part of the lowest state of a chain of 60 sites obeys this recursion at the left end, and |a_n| is not monotonic there
nonmono = low[14] > 2 * low[10] and low[40] > 10 * low[30] and low[30] < 1e-4
lam = np.roots([1.0 + Dcell, -0.3, 1.0 - Dcell])
ev60, vv60 = np.linalg.eigh(kc.bdg(60, 1.0, -0.3, Dcell))
j60 = int(np.argmin(np.where(ev60 > 0, ev60, np.inf)))
amp = vv60[:60, j60] + vv60[60:, j60]
amp = amp / amp[np.argmax(np.abs(amp))]
res = np.abs((1 + Dcell) * amp[2:30] - 0.3 * amp[1:29] + (1 - Dcell) * amp[0:28]).max()
check('notebook box: the lowest level of the cell oscillates in L, and the end mode decays as 0.867^n with complex roots',
      nonmono and np.all(np.abs(lam.imag) > 0.5) and np.allclose(np.abs(lam), np.sqrt((1 - Dcell) / (1 + Dcell)), atol=1e-12)
      and abs(np.abs(lam[0]) - 0.867) < 5e-4 and (-0.3) ** 2 < 4 * (1 - Dcell ** 2) and res < 1e-5 and abs(amp[1]) < abs(amp[2]),
      (round(low[10], 4), round(low[14], 4), '%.1e' % low[30], '%.2e' % low[40], round(abs(lam[0]), 4), '%.0e' % res))
print('all checks of page 16 hold')
