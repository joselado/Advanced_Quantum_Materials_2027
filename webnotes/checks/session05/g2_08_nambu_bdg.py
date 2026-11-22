"""Session 5, the numbers and the signs that page 08 (Section 5.8) states and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a box is an assert, here
or in the figure script that draws it. The numbers of the chain figure nambu_bands (t=1, mu=-1, Delta=0.45, k_F = pi/3, the
gap 0.9 and the weight 1/2 at k_F) are asserted in figures/session05/nambu_bands.py, those of the square lattice (mu=-1.90, the
two crossings, the smallest energy 0.8, and the distance 1.6 between the two drawn branches at both crossings) in
figures/session05/g2_nambu_square.py, and those of the three pictures of the quiz (the smallest energy Delta and the distance
2 Delta between the drawn branches, 0.4, 0.8 and 1.6) in figures/session05/_g2_bdg.py. This script holds the rest, in the order
of the page. The fold is checked as an identity between
operators on rings of 3 and 4 sites, with the matrices of the fermion operators. pyqula runs in a temporary folder, so the
script writes no file in the repository.

Run it from anywhere:  python3 webnotes/checks/session05/g2_08_nambu_bdg.py"""
import os
import tempfile

import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def fermions(n):
    """Annihilation operators of n fermion modes, with the Jordan-Wigner string, as 2^n x 2^n matrices."""
    a = np.array([[0., 1.], [0., 0.]])
    z = np.diag([1., -1.])
    out = []
    for j in range(n):
        m = np.array([[1.]])
        for i in range(n):
            m = np.kron(m, z if i < j else (a if i == j else np.eye(2)))
        out.append(m)
    return out


def dag(m):
    return m.conj().T


# ---- the fold, on rings of L sites: (5.4) without its constant against one block, the full spinor and the factor 1/2
t, mu, D = 1.0, 0.37, 0.3 + 0.2j
for L in (3, 4):
    c = fermions(2 * L)
    up, dn = c[0::2], c[1::2]
    I = np.eye(2 ** (2 * L))
    H = sum(-t * (dag(s[n]) @ s[(n + 1) % L] + dag(s[(n + 1) % L]) @ s[n]) for s in (up, dn) for n in range(L))
    H = H - mu * sum(dag(x) @ x for x in c)
    H = H + sum(D * dag(up[n]) @ dag(dn[n]) + np.conj(D) * dn[n] @ up[n] for n in range(L))
    ks = 2 * np.pi * np.arange(L) / L
    eps = -2 * t * np.cos(ks) - mu
    for sgn in (1, -1):                              # c_n = sum_k e^{sgn i k n} c_k / sqrt(L), both signs of the transform
        ck = {s: [sum(np.exp(-sgn * 1j * k * n) * x[n] for n in range(L)) / np.sqrt(L) for k in ks] for s, x in (('u', up), ('d', dn))}
        mk = lambda i: (-i) % L                                                     # noqa: E731, the index of -k
        pair_n = sum(dag(up[n]) @ dag(dn[n]) for n in range(L))
        pair_k = sum(dag(ck['u'][i]) @ dag(ck['d'][mk(i)]) for i in range(L))
        check(f'fold, first step: sum_n c+_nup c+_ndn = sum_k c+_kup c+_-kdn, L={L}, sign {sgn:+d}', np.abs(pair_n - pair_k).max() < 1e-12,
              np.abs(pair_n - pair_k).max())
        kin = sum(eps[i] * (dag(ck[s][i]) @ ck[s][i]) for s in 'ud' for i in range(L))
        Hk = kin + D * pair_k + np.conj(D) * dag(pair_k)
        check(f'fold, first step: the hopping and mu give sum eps(k) c+c, L={L}, sign {sgn:+d}', np.abs(H - Hk).max() < 1e-12,
              np.abs(H - Hk).max())
        h = lambda e: np.array([[e, D], [np.conj(D), -e]])                                       # noqa: E731, (5.8)
        block1 = 0
        for i in range(L):
            row = [dag(ck['u'][i]), ck['d'][mk(i)]]
            col = [ck['u'][i], dag(ck['d'][mk(i)])]
            block1 = block1 + sum(h(eps[i])[a, b] * row[a] @ col[b] for a in range(2) for b in range(2))
        check(f'fold, second step: H = sum_k (c+_kup, c_-kdn) h_BdG (c_kup, c+_-kdn) + sum_k eps(k), L={L}, sign {sgn:+d}',
              np.abs(H - block1 - eps.sum() * I).max() < 1e-12, np.abs(H - block1 - eps.sum() * I).max())
        block2 = 0
        for i in range(L):
            row = [dag(ck['d'][i]), -ck['u'][mk(i)]]
            col = [ck['d'][i], -dag(ck['u'][mk(i)])]
            block2 = block2 + sum(h(eps[i])[a, b] * row[a] @ col[b] for a in range(2) for b in range(2))
        check(f'fold, third step: the second block gives the same terms, L={L}, sign {sgn:+d}',
              np.abs(block2 - block1).max() < 1e-12, np.abs(block2 - block1).max())
        full = 0
        HB = lambda e: np.array([[e, 0, D, 0], [0, e, 0, D], [np.conj(D), 0, -e, 0], [0, np.conj(D), 0, -e]])   # noqa: E731, (5.7)
        for i in range(L):
            psi = [ck['u'][i], ck['d'][i], dag(ck['d'][mk(i)]), -dag(ck['u'][mk(i)])]
            full = full + sum(HB(eps[i])[a, b] * dag(psi[a]) @ psi[b] for a in range(4) for b in range(4))
        check(f'fold, third step: H = (1/2) sum_k Psi+ H_BdG Psi + sum_k eps(k), L={L}, sign {sgn:+d}',
              np.abs(H - 0.5 * full - eps.sum() * I).max() < 1e-12, np.abs(H - 0.5 * full - eps.sum() * I).max())
        # decided on 2026-11-22, the text after (5.6): "Without it, the two blocks would still be decoupled, but with +Delta in
        # one and -Delta in the other, so they would not be identical copies." The spinor without the minus sign,
        # (c_kup, c_kdn, c+_-kdn, c+_-kup), gives H with the pairing block diag(D, -D), which couples (e up, h dn) and
        # (e dn, h up) only inside each block, and not with diag(D, D), the identical copies
        nosign = {}
        for s2 in (1, -1):
            HBn = lambda e: np.array([[e, 0, D, 0], [0, e, 0, s2 * D], [np.conj(D), 0, -e, 0], [0, s2 * np.conj(D), 0, -e]])  # noqa: E731
            alt = 0
            for i in range(L):
                psi = [ck['u'][i], ck['d'][i], dag(ck['d'][mk(i)]), dag(ck['u'][mk(i)])]
                alt = alt + sum(HBn(eps[i])[a, b] * dag(psi[a]) @ psi[b] for a in range(4) for b in range(4))
            nosign[s2] = np.abs(H - 0.5 * alt - eps.sum() * I).max()
        check(f'text after (5.6): without the minus sign the blocks are decoupled with +Delta and -Delta, not identical, L={L}, '
              f'sign {sgn:+d}', nosign[-1] < 1e-12 and nosign[1] > 0.1, (nosign[-1], round(nosign[1], 3)))
    # corrected on 2026-11-22, the text before the key box: "The 4x4 problem in (5.7) splits into two 2x2 blocks, and it would
    # split also without the extra minus sign of the spinor (5.6)", "and the minus sign is what makes the second one identical to
    # the first". In the order of (5.6) the matrix (5.7) has Delta at (0,2) and (1,3), so it is not block-diagonal as written, and
    # the order (0,2,1,3) gives two blocks h_BdG(D) with nothing between them. The matrix of the spinor without the sign, checked
    # as operators above, gives in the same order h_BdG(D) and h_BdG(-D), also with nothing between them
    perm = [0, 2, 1, 3]
    Ms, Mn = HB(0.7)[np.ix_(perm, perm)], HBn(0.7)[np.ix_(perm, perm)]
    hD, hmD = np.array([[0.7, D], [np.conj(D), -0.7]]), np.array([[0.7, -D], [-np.conj(D), -0.7]])
    check(f'text before the key box: (5.7) is interleaved in the order of (5.6), and splits into h(D), h(D) with the sign and into '
          f'h(D), h(-D) without it, L={L}', abs(HB(0.7)[0, 2]) > 0.1 and abs(HB(0.7)[1, 3]) > 0.1 and np.allclose(Ms[:2, 2:], 0)
          and np.allclose(Ms[:2, :2], hD) and np.allclose(Ms[2:, 2:], hD) and np.allclose(Mn[:2, 2:], 0) and np.allclose(Mn[:2, :2], hD)
          and np.allclose(Mn[2:, 2:], hmD) and s2 == -1, 'ok')
    i = 1
    x, y = ck['d'][i], ck['u'][mk(i)]
    check(f'fold, third step: -D c+_kdn c+_-kup = D c+_-kup c+_kdn, L={L}', np.allclose(-D * dag(x) @ dag(y), D * dag(y) @ dag(x)), 0)
    lhs = eps[i] * dag(ck['d'][mk(i)]) @ ck['d'][mk(i)]
    rhs = -eps[i] * ck['d'][mk(i)] @ dag(ck['d'][mk(i)]) + eps[i] * I
    check(f'fold, second step: eps c+c = -eps c c+ + eps, L={L}', np.abs(lhs - rhs).max() < 1e-12, 0)

# ---- the fold, last step, and the new quiz with equations as options
for e_, D_ in ((0.3, 0.4), (-0.7, 0.2 - 0.5j), (1.3, 0.05j)):
    m = np.array([[e_, D_], [np.conj(D_), -e_]])
    ev = np.linalg.eigvalsh(m)
    check(f'fold, (5.9): eigenvalues +-sqrt(eps^2+|D|^2), trace 0, det -eps^2-|D|^2, eps={e_} D={D_}',
          np.allclose(ev, [-np.hypot(e_, abs(D_)), np.hypot(e_, abs(D_))]) and np.isclose(np.trace(m), 0)
          and np.isclose(np.linalg.det(m).real, -e_**2 - abs(D_)**2), np.round(ev, 4))
ev = np.linalg.eigvalsh(np.array([[0.3, 0.4], [0.4, -0.3]]))
check('fold and quiz: eps=0.3, Delta=0.4 give E = +-0.5', np.allclose(ev, [-0.5, 0.5]), ev)
check('quiz: eps +- |D| gives 0.7 and -0.1, which add up to 0.6', np.isclose(0.3 + 0.4, 0.7) and np.isclose(0.3 - 0.4, -0.1)
      and np.isclose(0.7 - 0.1, 0.6), 0.6)
check('quiz: the determinant is -0.25, while +-(|eps|+|D|) gives -0.49', np.isclose(np.linalg.det([[0.3, 0.4], [0.4, -0.3]]), -0.25)
      and np.isclose(-(0.3 + 0.4)**2, -0.49), -0.25)

# ---- the key box of (5.9): |Delta| for a band that crosses the Fermi level, larger outside the band
k = np.linspace(-np.pi, np.pi, 200001)
for mu_ in (-1.0, 0.0, 1.5):
    E = np.sqrt((-2 * np.cos(k) - mu_)**2 + 0.45**2)
    check(f'key (5.9): chain with mu={mu_} inside the band, the smallest |E| is |Delta|=0.45 at eps=0', abs(E.min() - 0.45) < 1e-6,
          round(E.min(), 6))
E = np.sqrt((-2 * np.cos(k) - 2.5)**2 + 0.3**2)
check('key (5.9), the condition: mu=2.5 outside the band gives 0.5831 > |Delta|=0.3', abs(E.min() - 0.5831) < 1e-4, round(E.min(), 4))

# ---- the first quiz: t=1, mu=0, Delta=0.2 on the square lattice
kk = np.linspace(-np.pi, np.pi, 401)
KX, KY = np.meshgrid(kk, kk)
eps2 = -2 * (np.cos(KX) + np.cos(KY))
E2 = np.sqrt(eps2**2 + 0.2**2)
check('quiz 1: at the band bottom eps=-4, E = sqrt(16.04) = 4.0, the largest |E|', np.isclose(eps2.min(), -4)
      and abs(np.sqrt(16.04) - 4.005) < 1e-3 and np.isclose(E2.max(), np.sqrt(16.04)), round(np.sqrt(16.04), 4))
check('quiz 1: at eps=0, E = +-0.2, and the branches are 0.4 apart', np.isclose(np.sqrt(0 + 0.2**2), 0.2), 0.4)
# the picture quiz: the pictures (asserted in _g2_bdg.square_option) give the branches 0.8, 1.6 and 0.4 apart for 0.4, 0.8, 0.2
for D_, apart_ in ((0.4, 0.8), (0.8, 1.6), (0.2, 0.4)):
    ev = np.linalg.eigvalsh(np.array([[0., D_], [D_, 0.]]))
    check(f'picture quiz: at eps=0 the block with Delta={D_} has E = +-{D_}, so the branches are {apart_} apart', np.allclose(ev, [-D_, D_])
          and np.isclose(ev[1] - ev[0], apart_), round(ev[1] - ev[0], 4))
check('picture quiz: for Delta=0.2 the gap 0.4 is half of the 0.8 of the question', np.isclose(0.4, 0.8 / 2), 0.4)

# ---- the problem: |u|^2 = (1 + eps/E)/2, 0.854 at eps=|Delta|, and the lower branch (-v*, u*) with the weight |v|^2 = 0.146
for e_, D_ in ((0.5, 0.5), (0.3, 0.2 + 0.4j), (-1.1, 0.3j)):
    m = np.array([[e_, D_], [np.conj(D_), -e_]])
    ev, vec = np.linalg.eigh(m)
    E = np.hypot(e_, abs(D_))
    u, v = vec[:, 1]
    lower = vec[:, 0]
    ok = np.isclose(abs(u)**2, 0.5 * (1 + e_ / E)) and np.isclose(abs(v)**2, 0.5 * (1 - e_ / E))
    ok = ok and np.isclose(v, (E - e_) * u / D_) and np.isclose(abs(abs(np.vdot(lower, [-np.conj(v), np.conj(u)]))), 1)
    ok = ok and np.isclose(abs(lower[0])**2, abs(v)**2)
    check(f'problem: |u|^2 = (1+eps/E)/2, v = (E-eps) u/D, lower branch (-v*, u*) with weight |v|^2, eps={e_} D={D_}', ok,
          round(abs(u)**2, 4))
E = np.sqrt(2) * 0.5
check('problem: at eps=|Delta|, E = sqrt2 |Delta|, |u|^2 = 0.854 and |v|^2 = 0.146', abs(0.5 * (1 + 0.5 / E) - 0.854) < 5e-4
      and abs(0.5 * (1 - 0.5 / E) - 0.146) < 5e-4 and np.isclose(0.5 * (1 + 1 / np.sqrt(2)), 0.5 * (1 + 0.5 / E)),
      round(0.5 * (1 + 0.5 / E), 4))

# ---- the caption of the square lattice: set_filling(0.2) is mu=-1.90, a pocket of filled states around M
cwd = os.getcwd()
os.chdir(tempfile.mkdtemp())
from pyqula import geometry  # noqa: E402

g = geometry.square_lattice()
hq = g.get_hamiltonian()
hq.set_filling(0.2, nk=20)
x0 = hq.intra[0, 0].real
shifts = {}
for kw in ({}, {'nk': 10}):                         # the call without nk, and the default nk=10 of filling.set_average_filling
    hd = geometry.square_lattice().get_hamiltonian()
    hd.set_filling(0.2, **kw)
    shifts[str(kw)] = hd.intra[0, 0].real
# decided on 2026-11-22, the notebook box: "check that you get two copies of the band structure", without "same", since the
# second copy is the mirror -eps(k). The cell "Nambu electronic structure without superconductivity" is this lattice with
# set_filling(0.2, nk=20) and setup_nambu_spinor(). At Gamma and at M its four levels are eps twice and -eps twice, and the
# range of -eps, from -5.90 to 2.10, is not the range of eps, from -2.10 to 5.90
hn = geometry.square_lattice().get_hamiltonian()
hn.set_filling(0.2, nk=20)
hn.setup_nambu_spinor()
hkn = hn.get_hk_gen()
lev = {kn: np.sort(np.linalg.eigvalsh(np.array(hkn(np.array(kv))))) for kn, kv in (('G', [0., 0., 0.]), ('M', [0.5, 0.5, 0.]))}
os.chdir(cwd)
eG, eM = 4 + x0, -4 + x0
check('notebook box: without pairing the Nambu levels are eps and -eps, twice each, at Gamma and M, and the two copies are mirrors',
      np.allclose(lev['G'], np.sort([eG, eG, -eG, -eG])) and np.allclose(lev['M'], np.sort([eM, eM, -eM, -eM]))
      and abs(eG - (-eM)) > 1, (round(eM, 3), round(eG, 3)))      # top of eps 5.90, top of -eps 2.10
import json  # noqa: E402
nbk = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'jupyter-notebooks', 'session5.ipynb'),
                     encoding='utf-8'))
cl = [''.join(x['source']) for x in nbk['cells']]
hi = [i for i, s in enumerate(cl) if s.startswith('## Nambu electronic structure without superconductivity')]
check('notebook box: the cell is the square lattice with set_filling(0.2,nk=20), setup_nambu_spinor() and the electron weight',
      len(hi) == 1 and 'geometry.square_lattice()' in cl[hi[0] + 1] and 'h.set_filling(0.2,nk=20)' in cl[hi[0] + 1]
      and 'h.setup_nambu_spinor()' in cl[hi[0] + 1] and 'operator="electron"' in cl[hi[0] + 1], hi)
check('caption: with the default nk=10 the same call adds 2.236, which is mu=-2.24', abs(shifts['{}'] - shifts["{'nk': 10}"]) < 1e-12
      and abs(shifts['{}'] - 2.236) < 1e-3 and round(-shifts['{}'], 2) == -2.24, round(shifts['{}'], 5))
q = np.linspace(0, 2 * np.pi, 600, endpoint=False)
QX, QY = np.meshgrid(q, q)
band = 2 * (np.cos(QX) + np.cos(QY)) + x0
check('caption: set_filling(0.2) adds 1.902, which is mu=-1.90', abs(x0 - 1.902) < 1e-3, round(x0, 4))
check('caption: about a fraction 0.2 of the electron states is filled, 0.196 on a fine mesh', abs(np.mean(band < 0) - 0.2) < 0.01,
      round(np.mean(band < 0), 4))
check('caption: the pocket of filled states is around M, empty at Gamma and X', 2 * (-2) + x0 < 0 and 2 * (2) + x0 > 0 and 2 * (0) + x0 > 0,
      (round(-4 + x0, 3), round(4 + x0, 3), round(x0, 3)))
print('all checks of page 08 hold')
