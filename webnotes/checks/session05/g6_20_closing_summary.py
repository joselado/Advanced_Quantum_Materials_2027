"""Session 5, the statements of the quizzes of page 20 (Section 5.20, the closing summary).

One check script per page is the rule: every number of a feedback is an assert. The winding of the arrows of the picture quiz
is asserted in figures/session05/_g6_phase.py, on the pocket that it draws, and again here, with the arrows and dots that
its function marks() gives to the drawing and that the alt texts count. The Chern numbers come from
webnotes/figures/physcheck.py on the Bloch Hamiltonians of the square lattice with eps(k) = -2t (cos kx + cos ky) - mu at
mu=-t, t=1 and Delta_0=0.5, the pocket of the pictures. The s-wave and the d-wave pairings enter each spin block as (5.8),
and the chiral p-wave, a triplet with its d-vector along z, enters the two blocks with +Delta(k) and -Delta(k), as the
conventions sheet says. The script uses numpy only and writes no file.

Run it from anywhere:  python3 webnotes/checks/session05/g6_20_closing_summary.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'figures'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'figures', 'session05'))
import numpy as np
import physcheck
import _g6_phase


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


t, mu, D0 = 1.0, -1.0, 0.5
B = 2 * np.pi * np.eye(2)
eps = lambda k: -2 * t * (np.cos(k[0]) + np.cos(k[1])) - mu
pair = {'swave': lambda k: D0 + 0j, 'pwave': lambda k: D0 * (np.sin(k[0]) + 1j * np.sin(k[1])),
        'dwave': lambda k: D0 * (np.cos(k[0]) - np.cos(k[1])) + 0j}


def block(kind, sign=1):
    return lambda k: np.array([[eps(k), sign * pair[kind](k)], [sign * np.conj(pair[kind](k)), -eps(k)]])


# ---- the quiz with equations as options: the parity of the three pairings
rng = np.random.default_rng(1)
ks = rng.uniform(-np.pi, np.pi, size=(20, 2))
even = lambda f: all(np.isclose(f(k), f(-k)) for k in ks)
odd = lambda f: all(np.isclose(f(k), -f(-k)) for k in ks)
check('quiz: Delta_0 is even, a singlet', even(pair['swave']) and not odd(pair['swave']), 'ok')
check('quiz: Delta_0 (cos kx - cos ky) is even, a singlet', even(pair['dwave']) and not odd(pair['dwave']), 'ok')
k1 = np.array([np.pi / 2, 0.])
check('quiz: Delta_0 (cos kx - cos ky) is -Delta_0 at (pi/2, 0) and at -(pi/2, 0)',
      np.isclose(pair['dwave'](k1), -D0) and np.isclose(pair['dwave'](-k1), -D0), pair['dwave'](k1).real / D0)
check('quiz: Delta_0 (sin kx + i sin ky) is odd, a triplet', odd(pair['pwave']) and not even(pair['pwave']), 'ok')

# ---- the picture quiz: the winding of the arrows on the pocket of the pictures
w = {kind: _g6_phase.winding(kind) for kind in ('swave', 'pwave', 'dwave')}
check('picture quiz: the s-wave arrows do not wind, the p-wave arrows wind once, the d-wave arrows change sign four times',
      w == {'swave': (0, 0), 'pwave': (1, 0), 'dwave': (0, 4)}, w)
# the alt texts: sixteen arrows for s and p, the s arrows all of one length and to the right, the p arrows away from the
# center, and for d the arrows to the left on the kx axis, to the right on the ky axis and four dots on the diagonals
m = {kind: _g6_phase.marks(kind) for kind in ('swave', 'pwave', 'dwave')}
dot = {kind: np.abs(a) < 1e-9 for kind, (_, _, _, a) in m.items()}
_, _, _, a_s = m['swave']
_, px, py, a_p = m['pwave']
th, _, _, a_d = m['dwave']
deg = np.round(np.degrees(th)).astype(int)
check('picture quiz, alt texts: 16 arrows for s and p, 12 arrows and 4 dots for d',
      (~dot['swave']).sum() == 16 and (~dot['pwave']).sum() == 16 and (~dot['dwave']).sum() == 12 and dot['dwave'].sum() == 4,
      {kind: (int((~v).sum()), int(v.sum())) for kind, v in dot.items()})
check('picture quiz, alt texts: the s arrows have one length and point to the right, the p arrows point away from the center',
      np.allclose(a_s, a_s[0]) and a_s[0].real > 0 and np.allclose(a_s.imag, 0) and np.all(a_p.real * px + a_p.imag * py > 0), 'ok')
check('picture quiz, alt text: the d dots are on the diagonals, the arrows point left on the kx axis and right on the ky axis',
      sorted(deg[dot['dwave']].tolist()) == [45, 135, 225, 315] and all(a_d[deg == x][0].real < 0 for x in (0, 180))
      and all(a_d[deg == x][0].real > 0 for x in (90, 270)) and np.allclose(a_d.imag, 0), deg[dot['dwave']].tolist())
Cs = physcheck.chern_links(block('swave'), B, bands=0, nk=48)
check('picture quiz: the s-wave block has C = 0, so the two blocks give 0', abs(Cs) < 1e-6, round(Cs, 6))
C1 = physcheck.chern_links(block('pwave'), B, bands=0, nk=48)
C2 = physcheck.chern_links(block('pwave', -1), B, bands=0, nk=48)
Ck = physcheck.chern_kubo(block('pwave'), B, bands=0, nk=96)
check('picture quiz: the p-wave blocks with +Delta and -Delta have the same C = +1 each, so |C| = 2',
      abs(C1 - 1) < 1e-6 and abs(C2 - 1) < 1e-6 and abs(Ck - 1) < 0.05, (round(C1, 6), round(C2, 6), round(Ck, 4)))
full = lambda k: np.block([[block('pwave')(k), np.zeros((2, 2))], [np.zeros((2, 2)), block('pwave', -1)(k)]])
C4 = physcheck.chern_links(full, B, bands=range(2), nk=48)
check('picture quiz: the 4x4 BdG matrix of the two blocks gives C = 2 for the two bands below zero', abs(C4 - 2) < 1e-6, round(C4, 6))
gp = physcheck.gap(block('pwave'), B, nfilled=1, nk=60)
check('picture quiz: the p-wave spectrum has a gap on the pocket', gp > 0.3, round(gp, 4))
k0 = np.arccos(0.25)
node = np.array([k0, k0])
Enode = np.abs(np.linalg.eigvalsh(block('dwave')(node))).min()
check('picture quiz: the d-wave Delta vanishes where the pocket crosses the diagonal, so E = 0 there and there is no gap',
      abs(eps(node)) < 1e-12 and abs(pair['dwave'](node)) < 1e-12 and Enode < 1e-12, round(k0, 4))

# ---- the quiz on the bond pairing, kept: on a ring a pairing f(k) c_k c_-k with f even cancels, with f odd it does not
N = 4
I2, Z, S = np.eye(2), np.diag([1., -1.]), np.array([[0., 1.], [0., 0.]])
def op(n):
    m = np.eye(1)
    for j in range(N):
        m = np.kron(m, Z if j < n else (S if j == n else I2))
    return m
cn = [op(n) for n in range(N)]
kk = 2 * np.pi * np.arange(N) / N
ck = [sum(np.exp(-1j * q * n) * cn[n] for n in range(N)) / np.sqrt(N) for q in kk]
minus = lambda i: (-i) % N
even_sum = sum(np.cos(kk[i]) * ck[i] @ ck[minus(i)] for i in range(N))
odd_sum = sum(np.sin(kk[i]) * ck[i] @ ck[minus(i)] for i in range(N))
check('kept quiz: sum_k cos k c_k c_-k = 0 by antisymmetry, while sum_k sin k c_k c_-k is not zero',
      np.abs(even_sum).max() < 1e-12 and np.abs(odd_sum).max() > 0.1, round(np.abs(odd_sum).max(), 4))
check('kept quiz: the onsite term c_n c_n vanishes', all(np.abs(c @ c).max() == 0 for c in cn), 0)
