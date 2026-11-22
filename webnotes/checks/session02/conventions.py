"""Checks of webnotes/conventions/session02.md, with numbers. Every bullet of the sheet is asserted here, in the order
of the sheet, by a formula with numpy and, where pyqula has the model, by pyqula. It prints one line per bullet and
exits 0 when all hold.

Not asserted, since they are read in code and are not a number: what the release 0.0.96 of pyqula on PyPI does (its
label "M" and its get_dos), which the sheet says was read and not run, and the sign that each figure script of the
session takes, which the opening paragraph of the sheet gives as read on 2026-11-21, and the name K that the recipe
test of Session 3 gives to the corner (b1+b2)/3. The bullet on the labels of pyqula asserts the side of the
development tree that this script imports.

Run it from anywhere:  python3 webnotes/checks/session02/conventions.py"""
import json, os, re, tempfile, time
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
NOTEBOOK = os.path.join(REPO, 'jupyter-notebooks', 'session2.ipynb')
S3 = np.sqrt(3.0)
COUNT = [0]


def check(name, ok, detail):
    """Prints one line for a check and stops the script when it does not hold."""
    print(('ok    ' if ok else 'FAIL  ') + name + ': ' + detail, flush=True)
    assert ok, name
    COUNT[0] += 1


def near(x, y, tol=1e-9):
    return bool(np.all(np.abs(np.asarray(x, complex) - np.asarray(y, complex)) < tol))


def cart(h):
    """(hk, A, B) of a pyqula Hamiltonian, hk takes the Cartesian momentum, A holds the lattice vectors as rows and B
    the reciprocal vectors as rows, a_i.b_j = 2 pi delta_ij. pyqula takes the reduced momentum k.a_i/2 pi."""
    d = h.dimensionality
    g = h.geometry
    A = np.array([g.a1, g.a2, g.a3], float)[:d, :d]
    gen = h.get_hk_gen()

    def hk(k):
        kr = np.zeros(3)
        kr[:d] = A @ np.atleast_1d(np.asarray(k, float)) / (2 * np.pi)
        m = gen(kr)
        return np.asarray(m.todense() if hasattr(m, 'todense') else m)
    return hk, A, 2 * np.pi * np.linalg.inv(A).T


def ev(hk, k):
    return np.linalg.eigvalsh(hk(k))


def ring(L, hops):
    """The Hamiltonian of a ring of L sites, hops[n-1] the matrix element to the neighbor at distance n."""
    S = np.roll(np.eye(L), 1, axis=1)
    H = np.zeros((L, L))
    for n, t in enumerate(hops, 1):
        P = np.linalg.matrix_power(S, n)
        H += t * (P + P.T)
    return H


def honey_f(k, delta):
    return np.exp(1j * np.asarray(k) @ delta.T).sum(-1)


DELTA = np.array([[1.0, 0.0], [-0.5, S3 / 2], [-0.5, -S3 / 2]])     # graphene_path.py, bond length 1
KN = np.array([2 * np.pi / 3, 2 * np.pi / (3 * S3)])                   # K of the notes in that frame
MN = np.array([2 * np.pi / 3, 0.0])


def lieb_bands(k):
    """The Lieb lattice with -t, t=1, bond length 1, k in units of the inverse bond length."""
    a, b = -2 * np.cos(k[0]), -2 * np.cos(k[1])
    return np.linalg.eigvalsh(np.array([[0, a, b], [a, 0, 0], [b, 0, 0]]))


def kagome_bands(k):
    """The kagome lattice with -t, t=1, bond length 1, the sites at 0, a1/2, a2/2 with a1=(2,0), a2=(1,sqrt3)."""
    a1, a2 = np.array([2.0, 0.0]), np.array([1.0, S3])
    c = [np.cos(k @ v / 2) for v in (a1, a2, a2 - a1)]
    return np.linalg.eigvalsh(-2 * np.array([[0, c[0], c[1]], [c[0], 0, c[2]], [c[1], c[2], 0]]))


def main():
    from pyqula import geometry
    from pyqula.kpointstk.labels import label2k
    t0 = time.time()
    rng = np.random.default_rng(2)
    G = {n: getattr(geometry, n)() for n in ('chain', 'square_lattice', 'cubic_lattice', 'triangular_lattice',
                                            'honeycomb_lattice', 'lieb_lattice', 'kagome_lattice', 'ladder', 'bichain')}
    H = {n: g.get_hamiltonian(has_spin=False) for n, g in G.items()}
    Hm = {n: g.get_hamiltonian(has_spin=False, tij=[-1.0]) for n, g in G.items() if n not in ('ladder', 'bichain')}

    # The sign of the hopping
    e12 = np.sort(np.linalg.eigvalsh(ring(12, [-1.0])))
    ref = np.sort(-2 * np.cos(2 * np.pi * np.arange(12) / 12))
    e9 = np.sort(np.linalg.eigvalsh(ring(12, [-1.0, -0.3])))
    ref9 = np.sort(-2 * np.cos(2 * np.pi * np.arange(12) / 12) - 0.6 * np.cos(4 * np.pi * np.arange(12) / 12))
    hk, A, B = cart(Hm['chain'])
    pq = [ev(hk, p)[0] for p in (0.0, np.pi)]
    hs, _, _ = cart(Hm['square_lattice'])
    hc, _, _ = cart(Hm['cubic_lattice'])
    sq = [ev(hs, [0, 0])[0], ev(hs, [np.pi, np.pi])[0]]
    cu = [ev(hc, [0, 0, 0])[0], ev(hc, [np.pi] * 3)[0]]
    check('the sign of the notes', near(e12, ref, 1e-12) and near(e9, ref9, 1e-12) and near(pq, [-2, 2]) and near(sq, [-4, 4])
          and near(cu, [-6, 6]),
          'a ring of 12 sites with -1 has -2 cos(phi) and with -0.3 more the levels of (2.9), pyqula with tij=[-1.] gives '
          '%+.0f, %+.0f for the chain, %+.0f, %+.0f for the square and %+.0f, %+.0f for the cubic lattice at Gamma and the corner'
          % (*pq, *sq, *cu))

    Hd = np.array([[0, 1.0], [1.0, 0]])                               # (1.2) with t=1 on the sites 0 and 1
    sym, anti = np.array([1, 1]) / np.sqrt(2), np.array([1, -1]) / np.sqrt(2)
    Mir = np.array([[0, 1], [1, 0]])
    esy, ean = sym @ Hd @ sym, anti @ Hd @ anti
    ms, ma = sym @ Mir @ sym, anti @ Mir @ anti
    low = np.linalg.eigh(-Hd)[1][:, 0]
    check('the dimer (1.2)', near([esy, ean, ms, ma], [1, -1, 1, -1]) and near(np.abs(low @ sym), 1) and near(esy + ean, 0),
          'for t=1 the symmetric state has %+.0f and the mirror %+.0f, the antisymmetric one %+.0f and %+.0f, two electrons '
          'have %+.0f, and with the element -1 the lowest state is the symmetric one' % (esy, ms, ean, ma, esy + ean))

    ks = rng.uniform(-4, 4, size=(20, 2))
    fp, fm = np.abs(honey_f(ks, DELTA)), np.abs(-honey_f(ks, DELTA))
    hh, Ah, Bh = cart(H['honeycomb_lattice'])
    pyq = [ev(hh, k)[1] for k in ks]
    check('the sign of (2.19)', near(fp, fm, 1e-12) and near(pyq, fp, 1e-12),
          'the bands +-|f| are the same for +t and -t at 20 momenta, and the default of honeycomb_lattice gives them to %.0e'
          % np.max(np.abs(np.array(pyq) - fp)))

    worst, neg = 0.0, 0
    for n, h in H.items():
        hk1, A1, _ = cart(h)
        d = h.dimensionality
        k0 = np.zeros(d)
        neg += int(np.sum(hk1(k0).real < -1e-12))
        if n in Hm:
            hk2, _, _ = cart(Hm[n])
            for k in rng.uniform(-3, 3, size=(3, d)):
                worst = max(worst, np.abs(hk1(k) + hk2(k)).max())
    check('pyqula puts +1 on every first-neighbor bond', neg == 0 and worst < 1e-12,
          'H(Gamma) has no negative entry on the 9 lattices, and the default H(k) is minus the one of tij=[-1.] to %.0e' % worst)

    out = {}
    for n in ('chain', 'square_lattice', 'cubic_lattice', 'honeycomb_lattice', 'lieb_lattice', 'triangular_lattice', 'kagome_lattice'):
        hp, A1, B1 = cart(H[n])
        hm, _, _ = cart(Hm[n])
        d = H[n].dimensionality
        Q = B1.sum(0) / 2
        sh = same = 0.0
        for k in rng.uniform(-3, 3, size=(4, d)):
            sh = max(sh, np.abs(ev(hm, k) - ev(hp, k + Q)).max())
            same = max(same, np.abs(ev(hm, k) - ev(hp, k)).max())
        mesh = [np.array([i, j]) / 30 @ B1 for i in range(30) for j in range(30)] if d == 2 else rng.uniform(-4, 4, size=(400, d))
        ep = np.array([ev(hp, k) for k in mesh])
        out[n] = (sh, same, ep.min(), ep.max())
    hb = G['bichain'].get_hamiltonian(has_spin=False)
    hbm = G['bichain'].get_hamiltonian(has_spin=False)
    hbm.intra, hbm.inter = -hbm.intra, -hbm.inter
    hbp, _, _ = cart(hb)
    hbn, _, _ = cart(hbm)
    bsame = max(np.abs(ev(hbp, k) - ev(hbn, k)).max() for k in (0.3, 1.1, 2.0))
    he, _, _ = cart(G['chain'].get_hamiltonian(has_spin=False, tij=[1.0, 0.5]))
    hen, _, _ = cart(G['chain'].get_hamiltonian(has_spin=False, tij=[-1.0, -0.5]))
    eta_e = np.array([ev(he, p)[0] for p in np.linspace(-np.pi, np.pi, 801)])
    eta_n = np.array([ev(hen, p)[0] for p in np.linspace(-np.pi, np.pi, 801)])
    ok = all(out[n][0] < 1e-12 for n in ('chain', 'square_lattice', 'cubic_lattice'))
    tops = [ev(cart(H[n])[0], np.zeros(H[n].dimensionality))[-1] for n in ('chain', 'square_lattice', 'cubic_lattice')]
    ok = ok and near(tops, [2, 4, 6], 1e-12)
    ok = ok and all(out[n][1] < 1e-12 for n in ('honeycomb_lattice', 'lieb_lattice')) and bsame < 1e-12
    tri, kag = out['triangular_lattice'], out['kagome_lattice']
    ok = ok and near([tri[2], tri[3]], [-3, 6], 1e-9) and near([kag[2], kag[3]], [-2, 4], 1e-9)
    ok = ok and near([eta_e.min(), eta_e.max(), eta_n.min(), eta_n.max()], [-1.5, 3, -3, 1.5], 1e-4)
    check('the notebook sign against the sign of the notes', ok,
          'with +1 the chain, square and cubic lattices have the energies of -1 moved by pi (to %.0e), with the tops %s at Gamma, the honeycomb, Lieb '
          'and bichain the same energies at each k (to %.0e), and the triangular (%.2f to %.2f), kagome (%.2f to %.2f) and '
          'the chain with eta=0.5 (%.2f to %.2f against %.2f to %.2f) turn upside down'
          % (max(out[n][0] for n in ('chain', 'square_lattice', 'cubic_lattice')), np.round(tops, 3).tolist(),
             max(out['honeycomb_lattice'][1], out['lieb_lattice'][1], bsame), tri[2], tri[3], kag[2], kag[3],
             eta_e.min(), eta_e.max(), eta_n.min(), eta_n.max()))

    phis = np.linspace(-np.pi, np.pi, 41)
    def chain_band(tij):
        hq, _, _ = cart(G['chain'].get_hamiltonian(has_spin=False, tij=tij))
        return np.array([ev(hq, p)[0] for p in phis])
    b3 = chain_band([1.0, 0.3, -0.2])
    f3 = 2 * np.cos(phis) + 0.6 * np.cos(2 * phis) - 0.4 * np.cos(3 * phis)
    e29 = -2 * np.cos(phis) - 0.6 * np.cos(2 * phis)
    miss = np.abs(chain_band([-1.0, 0.3]) - e29).max()
    check('tij on the chain', near(b3, f3, 1e-12)
          and near(chain_band([-1.0, -0.3]), e29, 1e-12) and near(chain_band([1.0, 0.3]), -e29, 1e-12) and abs(miss - 1.2) < 1e-9,
          'tij=[1,0.3,-0.2] gives 2 cos(phi) + 0.6 cos(2 phi) - 0.4 cos(3 phi), tij=[-1,-0.3] gives (2.9), tij=[1,0.3] gives '
          'minus (2.9), and tij=[-1,0.3] misses (2.9) by %.2f' % miss)

    nb = json.load(open(NOTEBOOK, encoding='utf-8'))
    calls, head, chain_cell = [], '', None
    for c in nb['cells']:
        s = ''.join(c['source'])
        if c['cell_type'] == 'markdown' and s.lstrip().startswith('#') and 'Exercise' not in s.split('\n')[0]:
            head = s.split('\n')[0].strip('# ').split(' (')[0]
        if c['cell_type'] == 'code':
            for m in re.finditer(r'get_hamiltonian\(([^)]*)\)', s):
                calls.append((head, m.group(1).replace(' ', '')))
                if head == 'One dimensional chain':
                    chain_cell = m.group(1).replace(' ', '')
    tijs = [re.search(r'tij=\[([^\]]*)\]', a).group(1) for h, a in calls if 'tij=' in a]
    spinful = sorted(set(h for h, a in calls if 'has_spin=False' not in a))
    ok = all(t.split(',')[0] == '1.0' for t in tijs) and chain_cell == 'tij=[1.0,0.]'
    ok = ok and 'Fermi surface of the honeycomb lattice' in spinful and 'Density of states of the honeycomb lattice' not in spinful
    check('the notebook', ok, '%d calls of get_hamiltonian, every tij starts with 1.0 (%s), "One dimensional chain" has %s, '
          'and %d sections call it spinful, among them "Fermi surface of the honeycomb lattice"'
          % (len(calls), ' '.join(sorted(set(tijs))), chain_cell, len(spinful)))

    # The Bloch phase and the momentum of pyqula
    def shift(L, s):
        return np.roll(np.eye(L), s, axis=0)                          # (P psi)_n = psi_{n-s}
    L = 8
    T, R = shift(L, -1), shift(L, -1)                                  # (T psi)_n = psi_{n+1}, and R since 2026-11-22
    phi = 2 * np.pi * 3 / L
    v = np.exp(1j * phi * np.arange(L))
    okT = near(T @ v, np.exp(1j * phi) * v) and near(R @ v, np.exp(1j * phi) * v)
    okT = okT and near(shift(L, 1) @ v, np.exp(-1j * phi) * v)        # the other sense gives e^{-i phi}
    s4 = np.array([1, -1j, -1, 1j])
    q4 = np.array([1, 1j, -1, -1j])
    R4, T4 = shift(4, -1), shift(4, -1)
    v3 = np.exp(2j * np.pi * np.arange(3) / 3)
    check('the direction of the shift', okT and near(R4 @ s4, -1j * s4) and near(T4 @ s4, -1j * s4) and near(R4 @ q4, 1j * q4)
          and near(shift(3, -1) @ v3, np.exp(2j * np.pi / 3) * v3) and near(R4 @ np.eye(4)[1], np.eye(4)[0]),
          'R and T move every amplitude to the previous site, e^{i n phi} has e^{i phi} under both on 8 sites and e^{-i phi} '
          'in the other sense, (1,-i,-1,i) has -i, (1,i,-1,-i) has i, and on 3 sites R gives e^{2 pi i j/3} the '
          'eigenvalue e^{2 pi i/3}')

    ph = 2 * np.pi * np.arange(L) / L
    F = np.exp(1j * np.outer(np.arange(L), ph))                       # column phi is e^{in phi}, (2.7) with no factor
    orth = F.conj().T @ F
    back = F @ F.conj().T                                              # sum over phi of e^{-in phi} e^{im phi}
    U = F / np.sqrt(L)                                                 # (2.7) as printed since 2026-11-22
    Hdiag = U.conj().T @ ring(L, [-1.0]) @ U
    check('the normalization of (2.7)', near(orth, L * np.eye(L), 1e-12) and near(back, L * np.eye(L), 1e-12)
          and near(U.conj().T @ U, np.eye(L), 1e-12) and near(U @ U.conj().T, np.eye(L), 1e-12)
          and near(Hdiag, np.diag(-2 * np.cos(ph)), 1e-12),
          'on 8 sites sum_n e^{in(phi-phi\')} is 8 delta, with 1/sqrt(8) the transform (2.7) is unitary, its inverse gives '
          'c_n^+, and H is diagonal with -2 cos(phi), (2.8)')

    hb = G['bichain'].get_hamiltonian(has_spin=False)
    inter = np.asarray(hb.inter).real
    gen = hb.get_hk_gen()
    eta = 0.6
    hb.inter = eta * hb.inter
    gen6 = hb.get_hk_gen()
    err = 0.0
    for k in (0.1, 0.37, -0.2):
        p = 2 * np.pi * k
        want = np.array([[0, 1 + eta * np.exp(-1j * p)], [1 + eta * np.exp(1j * p), 0]])
        g12 = np.asarray(gen6([k, 0, 0]))
        intra = np.asarray(hb.intra)
        err = max(err, np.abs(g12 - want).max(),
                  np.abs(g12 - (intra + np.asarray(hb.inter) * np.exp(1j * p) + np.asarray(hb.inter).conj().T * np.exp(-1j * p))).max())
    check('(2.12) in pyqula', near(inter, [[0, 0], [1, 0]]) and err < 1e-12,
          'bichain has h.inter[1,0]=1, the bond from B of a cell to A of the next one, which is gamma_BA of (2.11), and '
          'h.get_hk_gen()([k,0,0]) is h.intra + h.inter e^{2 pi i k} + h.c., the matrix (2.13) for h.inter = 0.6*h.inter, to %.0e' % err)

    k, e = H['chain'].get_bands()
    check('the momentum of pyqula', len(k) == 400 and near(k, np.arange(400)) and near([e[0], e[-1]], [2, 2], 1e-12)
          and near(e[199], 2 * np.cos(2 * np.pi * 199 / 399), 1e-12),
          'the chain of get_bands() returns the step 0 to 399 in place of k, on 400 momenta from k=0 to k=1 with both ends, '
          'the band 2 cos(2 pi k) is +2 at both ends and %.5f at step 199' % e[199])

    # Lattices, zones and points
    lc = {n: np.linalg.norm(np.asarray(G[n].a1, float)) for n in G}
    bond = {n: min(np.linalg.norm(G[n].r[i] - G[n].r[j] - m * np.asarray(G[n].a1) - l * np.asarray(G[n].a2))
                   for i in range(len(G[n].r)) for j in range(len(G[n].r)) for m in (-1, 0, 1) for l in (-1, 0, 1)
                   if (i, j, m, l) != (i, i, 0, 0))
            for n in ('square_lattice', 'triangular_lattice', 'honeycomb_lattice', 'lieb_lattice', 'kagome_lattice')}
    gh = G['honeycomb_lattice']
    ok = near([lc['chain'], lc['square_lattice'], lc['cubic_lattice'], lc['triangular_lattice'], lc['honeycomb_lattice'],
               lc['lieb_lattice'], lc['kagome_lattice'], lc['bichain']], [1, 1, 1, 1, S3, 2, 2, 2], 1e-12)
    ok = ok and all(abs(b - 1) < 1e-12 for b in bond.values())
    ok = ok and near(np.asarray(gh.a1)[:2], [1.5, S3 / 2]) and near(np.asarray(gh.a2)[:2], [-1.5, S3 / 2])
    ok = ok and near(np.asarray(gh.r)[:, :2], [[-0.5, 0], [0.5, 0]]) and near(np.asarray(G['bichain'].r)[:, 0], [-0.5, 0.5])
    ok = ok and near(np.asarray(G['triangular_lattice'].a2)[:2], [-0.5, S3 / 2]) and near(np.asarray(G['kagome_lattice'].a2)[:2], [1, S3])
    ok = ok and near(np.asarray(G['lieb_lattice'].a2)[:2], [0, 2])
    check('the lengths of pyqula', ok,
          'bond length 1 everywhere, lattice constants %s, honeycomb sites at (-1/2,0) and (1/2,0)'
          % ' '.join('%.3f' % lc[n] for n in ('chain', 'square_lattice', 'cubic_lattice', 'triangular_lattice',
                                             'honeycomb_lattice', 'lieb_lattice', 'kagome_lattice', 'bichain')))

    lab = {n: {l: np.round(np.array(label2k(G[n], l), float)[:2], 6).tolist() for l in (['X', 'M'] if n in ('square_lattice', 'lieb_lattice') else ['K', "K'", 'M'])}
           for n in ('square_lattice', 'lieb_lattice', 'honeycomb_lattice', 'triangular_lattice', 'kagome_lattice')}
    t = 1 / 3
    ok = lab['square_lattice'] == {'X': [0.5, 0.0], 'M': [0.5, 0.5]} and lab['lieb_lattice'] == lab['square_lattice']
    for n, s in (('honeycomb_lattice', [-1, -1]), ('triangular_lattice', [-1, -1]), ('kagome_lattice', [-1, 1])):
        ok = ok and near(lab[n]['K'], np.array(s) * t, 1e-6) and near(lab[n]["K'"], -np.array(s) * t, 1e-6) and lab[n]['M'] == [0.5, 0.0]
    nk = 100
    nodes = np.array([[0, 0, 0], [0.5, 0, 0], [0.5, 0.5, 0], [0, 0, 0]])
    path = [nodes[i] + (nodes[i + 1] - nodes[i]) * j / nk for i in range(3) for j in range(nk)] + [nodes[-1]]
    kk, ee = Hm['square_lattice'].get_bands(kpath=path)
    check('the labels of pyqula', ok and near(ee[[0, nk, 2 * nk, 3 * nk]], [-4, 0, 4, -4], 1e-12),
          'label2k gives X %s and M %s on the square and Lieb lattices, K %s and K\' %s on the honeycomb and triangular '
          'lattices, K %s on the kagome lattice, M (1/2,0) on all three, and a path of reduced momenta given by hand has '
          '-4, 0, 4 at Gamma, X, M with tij=[-1.]'
          % (lab['square_lattice']['X'], lab['square_lattice']['M'], np.round(lab['honeycomb_lattice']['K'], 4).tolist(),
             np.round(lab['honeycomb_lattice']["K'"], 4).tolist(), np.round(lab['kagome_lattice']['K'], 4).tolist()))

    kp = np.array(gh.get_kpath(['G', 'K', 'M', 'G'], nk=60, write=True))
    marks = open('BANDLINES.OUT').read().split()
    iK = int(float(marks[2]))
    kK = kp[iK][:2] @ Bh
    kd = np.array(gh.get_kpath(None, nk=400, write=True))
    dmarks = open('BANDLINES.OUT').read().split()
    s3c = (Bh[0] + Bh[1]) / 3
    lblK = np.array(label2k(gh, 'K'), float)[:2] @ Bh
    diff = np.linalg.solve(Bh.T, kK - lblK)
    ok = near(np.abs(honey_f(kK, DELTA)), 0, 1e-12) and near(diff, np.round(diff), 1e-9) and near(kK, [-2 * np.pi / 3, 2 * np.pi / (3 * S3)], 1e-9)
    ok = ok and near(kd[132][:2], [133 / 400] * 2, 1e-12) and dmarks[3] == 'K' and abs(float(dmarks[2]) - 400 / 3) < 1e-9
    ok = ok and near(s3c, [0, 4 * np.pi / (3 * S3)], 1e-12) and near(lblK, -s3c, 1e-12)
    nK = np.linalg.solve(Bh.T, KN - lblK)
    check('K and K\' of pyqula', ok and near(nK, np.round(nK), 1e-9),
          'get_bands(kpath=["G","K","M","G"]) walks to the corner (%.4f, %.4f), the same valley as label2k K at (0, %.4f), '
          'which is the K of the notes minus b1, while the default path writes "K" in BANDLINES.OUT at the step of (1/3,1/3), '
          'the corner (0, %.4f) that label2k calls K\'' % (kK[0], kK[1], lblK[1], s3c[1]))

    kc = np.array(geometry.cubic_lattice().get_kpath(None, nk=400, write=False))
    hk_, ehk = H['honeycomb_lattice'].get_bands()
    Ehk = ehk.reshape(-1, 2)
    kdsq = np.array(G['square_lattice'].get_kpath(None, nk=400, write=False))
    kdkg = np.array(G['kagome_lattice'].get_kpath(None, nk=400, write=False))
    ok = near(kd[0][:2], [1 / 400, 1 / 400], 1e-12) and near(kd[-1][:2], [1, 1], 1e-12) and len(kd) == 400
    ok = ok and near(kdsq[-1][:2], [1, -1], 1e-12) and near(kdkg[-1][:2], [1, -1], 1e-12)
    ok = ok and near(np.abs(Ehk[[132, 266]]).min(), 0.00908, 1e-4) and near(Ehk[199], [-1, 1], 1e-12) and near(Ehk[399], [-3, 3], 1e-12)
    corners = [kc[0], kc[np.argmin(np.linalg.norm(kc - [0.5, 0, 0], axis=1))], kc[-1]]
    ok = ok and near(corners[1], [0.5, 0, 0], 1e-12) and near(corners[2], [0.5, 0.5, 0.5], 1e-12)
    check('the default path of get_bands()', ok,
          'in 2D 400 steps s(1,1) for the honeycomb and triangular lattices and s(1,-1) for the square, Lieb and kagome '
          'lattices, s from 1/400 to 1, the honeycomb bands are %.4f at steps 132 and 266, +-1 at 199 and +-3 at 399, and in '
          '3D the path goes from Gamma to X, M, Gamma and R' % np.abs(Ehk[[132, 266]]).min())

    hk, _, Bt = cart(Hm['triangular_lattice'])
    Kt = np.array(label2k(G['triangular_lattice'], 'K'), float)[:2] @ Bt
    Mt = np.array([0.5, 0]) @ Bt
    tri = [ev(hk, [0, 0])[0], ev(hk, Kt)[0], ev(hk, Mt)[0]]
    hx = 1e-4
    curv = [(ev(hk, Mt + hx * u)[0] - 2 * tri[2] + ev(hk, Mt - hx * u)[0]) / hx ** 2
            for u in (Mt / np.linalg.norm(Mt), np.array([-Mt[1], Mt[0]]) / np.linalg.norm(Mt))]
    pts = {'chain': [ev(cart(Hm['chain'])[0], p)[0] for p in (0, np.pi)],
           'square': [ev(hs, p)[0] for p in ([0, 0], [np.pi, 0], [np.pi, np.pi])],
           'cubic': [ev(hc, p)[0] for p in ([0, 0, 0], [np.pi, 0, 0], [np.pi, np.pi, 0], [np.pi] * 3)]}
    ok = near(pts['chain'], [-2, 2]) and near(pts['square'], [-4, 0, 4]) and near(pts['cubic'], [-6, -2, 2, 6])
    ok = ok and near(tri, [-6, 3, 2]) and curv[0] * curv[1] < 0 and near(np.linalg.norm(Kt), 4 * np.pi / 3) and near(np.linalg.norm(Mt), 2 * np.pi / S3)
    check('the chain, square, cubic and triangular points', ok,
          'with tij=[-1.] the chain has -2, 2, the square -4, 0, 4, the cubic -6, -2, 2, 6 and the triangular lattice '
          '%.0f, %.0f, %.0f at Gamma, K, M with a saddle at M (curvatures %.1f and %.1f), widths 4, 8, 12 and 9'
          % (*tri, *curv))

    fG, fM, fK = (abs(honey_f(k, DELTA)) for k in ([0, 0], MN, KN))
    D2 = np.array([[0.0, 1.0], [S3 / 2, -0.5], [-S3 / 2, -0.5]])       # s02f04_dirac.py, the bonds along y
    K2 = np.array([4 * np.pi / (3 * S3), 0.0])
    nb1 = np.linalg.solve(Bh.T, KN - lblK)
    check('the honeycomb lattice of the notes', near([fG, fM, fK], [3, 1, 0], 1e-12) and near(np.linalg.norm(KN), 2.4184, 1e-4)
          and near(np.linalg.norm(MN), 2.0944, 1e-4) and near(abs(honey_f(K2, D2)), 0, 1e-12) and near(nb1, [1, 0], 1e-9),
          '|f| is %.0f, %.0f, %.0f at Gamma, M, K, |K| = %.4f and |M| = %.4f, the K of graphene_path.py is label2k K plus b1, '
          'and f vanishes at (4 pi/3 sqrt3, 0) in the frame of s02f04_dirac.py' % (fG, fM, fK, np.linalg.norm(KN), np.linalg.norm(MN)))

    r = np.asarray(gh.r)[:, :2]
    err = max(abs(hh(k)[0, 1] - honey_f(k, DELTA) * np.exp(-1j * k @ (r[1] - r[0]))) for k in rng.uniform(-4, 4, size=(6, 2)))
    per = np.abs(hh(KN + Bh[0]) - hh(KN)).max()
    fper = abs(honey_f(KN + Bh[0] + [0.1, 0], DELTA) - honey_f(KN + [0.1, 0], DELTA))
    check('the gauge of h.get_hk_gen()', err < 1e-12 and per < 1e-12 and fper > 0.1,
          'the entry [0,1] is f(k) e^{-i k.(r1-r0)} with r1-r0 = delta_1 = (1,0), to %.0e, it is periodic over the zone '
          'while f of (2.19) changes by %.2f' % (err, fper))

    hl, _, Bl = cart(Hm['lieb_lattice'])
    hlp, _, _ = cart(H['lieb_lattice'])
    P = {'G': [0, 0], 'X': [np.pi / 2, 0], 'M': [np.pi / 2, np.pi / 2]}
    lv = {p: ev(hl, k) for p, k in P.items()}
    lw = max(np.abs(ev(hl, k) - lieb_bands(k)).max() + np.abs(ev(hlp, k) - lieb_bands(k)).max() for k in rng.uniform(-3, 3, (5, 2)))
    slope = ev(hl, np.array(P['M']) + [1e-6, 0])[2] / 1e-6
    # the Blender figure takes the lattice constant 1, so its band at k is the band here at k/2
    Mb1 = np.array([np.pi, np.pi])
    slope1 = (lieb_bands((Mb1 + [1e-6, 0]) / 2)[2]) / 1e-6
    check('the Lieb lattice', near(lv['G'], [-2 * np.sqrt(2), 0, 2 * np.sqrt(2)]) and near(lv['X'], [-2, 0, 2]) and near(lv['M'], 0)
          and lw < 1e-12 and near(slope, 2, 1e-5) and near(lieb_bands(Mb1 / 2), 0, 1e-12) and near(slope1, 1, 1e-5),
          'the bands 0 and +-2 sqrt(cos^2 kx + cos^2 ky) for both signs, %s at Gamma, X, M, and the cone at M has the slope '
          '%.4f, t times the lattice constant 2, and with the lattice constant 1 the point M is (pi,pi) and the slope %.4f'
          % ([np.round(lv[p], 3).tolist() for p in 'GXM'], slope, slope1))

    hkg, _, Bk = cart(Hm['kagome_lattice'])
    hkp, _, _ = cart(H['kagome_lattice'])
    Kk = np.array(label2k(G['kagome_lattice'], 'K'), float)[:2] @ Bk
    Mk = np.array([0.5, 0]) @ Bk
    kv = [ev(hkg, k) for k in ([0, 0], Kk, Mk)]
    kpv = [ev(hkp, k) for k in ([0, 0], Kk, Mk)]
    kwr = max(np.abs(ev(hkg, k) - kagome_bands(k)).max() for k in rng.uniform(-3, 3, (5, 2)))
    # the Blender figure of Section 2.11b takes the lattice constant 1, so the same points are at half the lengths
    Kb, Mb = np.array([4 * np.pi / 3, 0]), np.array([np.pi, np.pi / S3])
    blend = [kagome_bands(k / 2) for k in (Kb, Mb)]
    check('the kagome lattice', near(kv, [[-4, 2, 2], [-1, -1, 2], [-2, 0, 2]]) and near(kpv, [[-2, -2, 4], [-2, 1, 1], [-2, 0, 2]])
          and kwr < 1e-12 and near(blend, [[-1, -1, 2], [-2, 0, 2]]),
          'with -t %s at Gamma, K, M, with the default %s, the K of the lattice constant 1 at (4 pi/3, 0) and M at '
          '(pi, pi/sqrt3)' % ([np.round(x, 3).tolist() for x in kv], [np.round(x, 3).tolist() for x in kpv]))

    def sublattice(g, T):
        """True when the sites of g differ by vectors of the lattice T of spacing 1, and its lattice vectors are twice
        those of T, so its cell is a 2 x 2 cell of T that keeps len(g.r) of the 4 sites."""
        r = np.asarray(g.r)[:, :2]
        A = np.array([g.a1, g.a2])[:, :2]
        cs = [np.linalg.solve(T.T, r[i] - r[0]) for i in range(len(r))]
        return all(near(c, np.round(c), 1e-9) for c in cs) and near(A, 2 * T, 1e-12) and len(set(tuple(np.round(c) % 2) for c in cs)) == len(r)
    Tt, Ts = np.array([[1, 0], [0.5, S3 / 2]]), np.eye(2)
    ok = sublattice(G['kagome_lattice'], Tt) and sublattice(G['lieb_lattice'], Ts) and len(G['kagome_lattice'].r) == len(G['lieb_lattice'].r) == 3
    Ak, Al = 2 * Tt, 2 * Ts
    check('one site in four removed', ok and near([3 / abs(np.linalg.det(Ak)) / (2 / S3), 3 / abs(np.linalg.det(Al))], [0.75, 0.75], 1e-12),
          'the 3 sites of kagome_lattice() are 3 of the 4 sites of a 2 x 2 cell of the triangular lattice of spacing 1, and '
          'those of lieb_lattice() 3 of the 4 of a 2 x 2 cell of the square lattice')

    # the state on one hexagon of the kagome lattice
    Lc = 6
    a1, a2 = np.array([2.0, 0.0]), np.array([1.0, S3])
    basis = [np.zeros(2), a1 / 2, a2 / 2]
    pos = np.array([i * a1 + j * a2 + b for i in range(Lc) for j in range(Lc) for b in basis])
    N = len(pos)
    Ht = np.zeros((N, N))
    big = np.array([Lc * a1, Lc * a2])
    for i in range(N):
        for j in range(N):
            dd = pos[j] - pos[i]
            c = np.linalg.solve(big.T, dd)
            dd = dd - (np.round(c) @ big)
            if abs(np.linalg.norm(dd) - 1) < 1e-9:
                Ht[i, j] = -1.0
    # a hexagon center has six sites at distance 1, a site has four, so the search finds a center
    centers = (pos[:, None, :] + np.array([[0.5, S3 / 2], [-0.5, S3 / 2], [1.0, 0.0]])[None]).reshape(-1, 2)
    psi = None
    for c in centers:
        dd = pos - c
        cc = np.linalg.solve(big.T, dd.T).T
        dd = dd - np.round(cc) @ big
        ring6 = np.nonzero(np.abs(np.linalg.norm(dd, axis=1) - 1) < 1e-9)[0]
        if len(ring6) == 6:
            ang = np.arctan2(dd[ring6, 1], dd[ring6, 0])
            order = ring6[np.argsort(ang)]
            psi = np.zeros(N)
            psi[order] = [1, -1, 1, -1, 1, -1]
            break
    hexok = psi is not None and near(Ht @ psi, 2 * psi, 1e-12) and near((2 * Ht) @ psi, 4 * psi, 1e-12)
    outside = [i for i in range(N) if psi[i] == 0 and np.any(Ht[i, psi != 0] != 0)]
    check('the state on one kagome hexagon', hexok and len(outside) == 6 and all(abs(Ht[i] @ psi) < 1e-12 for i in outside),
          'alternating +1 and -1 on the 6 sites of a hexagon of a torus of %d sites gives H psi = 2t psi for t=1 and t=2, '
          'and each of the %d sites that touch it gets -t(1-1) = 0' % (N, len(outside)))


    # The Dirac cone
    sl_n = [abs(honey_f(KN + 1e-6 * np.array([np.cos(a), np.sin(a)]), DELTA)) / 1e-6 for a in np.linspace(0, 2 * np.pi, 8, endpoint=False)]
    sl_2 = [abs(honey_f(K2 + 1e-6 * np.array([np.cos(a), np.sin(a)]), D2)) / 1e-6 for a in np.linspace(0, 2 * np.pi, 8, endpoint=False)]
    sl_p = [ev(hh, lblK + 1e-6 * np.array([np.cos(a), np.sin(a)]))[1] / 1e-6 for a in np.linspace(0, 2 * np.pi, 8, endpoint=False)]
    # the chain v = 2t sin(phi): the signed velocity is +2 at pi/2 and -2 at -pi/2, so only its size is largest at
    # both, and that size 2 is larger than the 1.5 of the cone
    phv = np.linspace(-np.pi, np.pi, 200001)
    vch = 2 * np.sin(phv)
    vok = (near(phv[np.argmax(vch)], np.pi / 2, 1e-4) and near(phv[np.argmin(vch)], -np.pi / 2, 1e-4)
           and near(np.abs(vch).max(), 2, 1e-9) and np.abs(vch).max() > 1.5)
    check('the Dirac velocity', near(sl_n, 1.5, 1e-5) and near(sl_2, 1.5, 1e-5) and near(sl_p, 1.5, 1e-5)
          and abs(1.5 / S3 - 0.866) < 1e-3 and vok,
          'the slope at K is %.5f to %.5f in 8 directions in each frame of the scripts and in pyqula, 3t/2 in units of the '
          'bond length, %.3f in units of the lattice constant, and the largest size of the velocity of the chain is %.4f at '
          '+-pi/2' % (min(sl_n + sl_2 + sl_p), max(sl_n + sl_2 + sl_p), 1.5 / S3, np.abs(vch).max()))

    errK = errKp = 0.0
    for a in np.linspace(0, 2 * np.pi, 7, endpoint=False):
        q = 1e-6 * np.array([np.cos(a), np.sin(a)])
        errK = max(errK, abs(honey_f(KN + q, DELTA) / (1.5 * np.exp(-5j * np.pi / 6) * (q[0] - 1j * q[1])) - 1))
        errKp = max(errKp, abs(honey_f(-KN + q, DELTA) / (1.5 * np.exp(-1j * np.pi / 6) * (q[0] + 1j * q[1])) - 1))
    check('the Dirac form at K and K\'', errK < 1e-5 and errKp < 1e-5,
          'f(K+q) = (3t/2) e^{-5 i pi/6} (qx - i qy) and f(K\'+q) = (3t/2) e^{-i pi/6} (qx + i qy) with K\' = -K, to %.0e'
          % max(errK, errKp))

    qq, hd = 0.01, 1e-4
    rad, tra = [], []
    for a in np.linspace(0, 2 * np.pi, 24, endpoint=False):
        u, w = np.array([np.cos(a), np.sin(a)]), np.array([-np.sin(a), np.cos(a)])
        p0 = KN + qq * u
        E = lambda k: abs(honey_f(k, DELTA))
        rad.append((E(p0 + hd * u) - 2 * E(p0) + E(p0 - hd * u)) / hd ** 2)
        tra.append((E(p0 + hd * w) - 2 * E(p0) + E(p0 - hd * w)) / hd ** 2)
    check('the effective mass of the cone', -0.8 < min(rad) < -0.7 and 0.7 < max(rad) < 0.8 and 145 < min(tra) and max(tra) < 155,
          'the band |f| at |q| = 0.01 from K has the radial curvature %.2f to %.2f and the curvature across q %.0f to %.0f, '
          'where v_F/|q| = 150' % (min(rad), max(rad), min(tra), max(tra)))

    # The density of states
    w = np.array([0.0, 1.0, 1.5])
    form = 1 / (np.pi * np.sqrt(4 - w ** 2))
    _, dg = H['chain'].get_dos(energies=w, mode='Green', delta=1e-4, write=False)
    pc = np.linspace(-np.pi, np.pi, 2000001)[:-1]
    Ec = -2 * np.cos(pc)
    cnt = [np.mean(np.abs(Ec - x) < 5e-3) / 1e-2 for x in w]
    check('the density of states of the chain', near(form, [1 / (2 * np.pi), 0.1838, 0.2406], 1e-4) and near(cnt, form, 1e-3)
          and near(dg, form, 1e-3),
          '1/(pi sqrt(4-w^2)) is %.4f %.4f %.4f at w = 0, 1, 1.5, a count on 2e6 momenta gives %.4f %.4f %.4f, and '
          'mode="Green" %.4f %.4f %.4f' % (*form, *cnt, *dg))

    from scipy.special import ellipk
    n = 2000
    s = (np.arange(n) + 0.5) / n * 2 * np.pi
    Es = (-2 * (np.cos(s)[:, None] + np.cos(s)[None, :])).ravel()
    ws = np.array([-3.95, -3.0, -1.0, -0.1])
    fsq = ellipk(1 - ws ** 2 / 16) / (2 * np.pi ** 2)
    csq = [np.mean(np.abs(Es - x) < 0.01) / 0.02 for x in ws]
    edge = ellipk(0.0) / (2 * np.pi ** 2)
    logs = (ellipk(1 - 1e-3 ** 2 / 16) - ellipk(1 - 1e-2 ** 2 / 16)) / (2 * np.pi ** 2)
    check('the density of states of the square lattice', np.max(np.abs(np.array(csq) / fsq - 1)) < 0.02 and near(edge, 1 / (4 * np.pi), 1e-12)
          and near(logs, np.log(10) / (2 * np.pi ** 2), 1e-5),
          'K(1-w^2/16)/(2 pi^2) is %s at w = %s, a count on 2000^2 momenta gives %s, %.1f percent at most, the edge value '
          'is 1/(4 pi) = %.4f, and from w=0.01 to 0.001 it grows by ln(10)/(2 pi^2)'
          % (np.round(fsq, 4).tolist(), ws.tolist(), np.round(csq, 4).tolist(), 100 * np.max(np.abs(np.array(csq) / fsq - 1)), edge))

    n = 1500
    s = (np.arange(n) + 0.5) / n
    fmesh = np.concatenate([np.abs(honey_f(s[i] * Bh[0] + s[:, None] * Bh[1], DELTA)) for i in range(n)])
    states = 2 * np.mean(fmesh < 0.2)                                   # both bands, per cell, |E| < 0.2
    slopeV = 2 / (S3 * np.pi)
    area = 3 * S3 / 2
    check('the V of the honeycomb lattice', near(states, slopeV * 0.2 ** 2, 2e-4) and near(slopeV, area / (np.pi * 2.25), 1e-12),
          'per cell, for one spin and summed over the two bands, g(E) = 2|E|/(sqrt3 pi) = %.4f |E|, so %.5f states with '
          '|E| < 0.2, and a count on 1500^2 momenta gives %.5f' % (slopeV, slopeV * 0.04, states))

    es = np.linspace(-5.0, 5.0, 1001)
    areas = []
    for nme in ('chain', 'honeycomb_lattice', 'kagome_lattice'):
        _, d = H[nme].get_dos(energies=es, delta=0.04, nk=100 if nme != 'chain' else 2000, write=False)
        areas.append(np.trapezoid(d, es))
    _, d1 = H['chain'].get_dos(energies=[0.0], delta=0.02, nk=4000, write=False)
    _, d2 = G['chain'].get_hamiltonian().get_dos(energies=[0.0], delta=0.02, nk=4000, write=False)
    # the call of webnotes/scripts/session02/g4_kagome_bands.py, which the figure kagome_dos runs, with write=False
    ek, dk = Hm['kagome_lattice'].get_dos(energies=np.linspace(-5., 3., 801), delta=4e-2, nk=200, write=False)
    ek, dk = np.asarray(ek), np.asarray(dk)
    kag_area = np.trapezoid(dk, ek)
    kag_peaks = [dk[np.abs(ek - x) < 0.4].max() for x in (-2.0, 0.0)]
    kag_v = dk[np.abs(ek + 1) < 0.4].min()
    _, dk1 = Hm['kagome_lattice'].get_dos(energies=[-2.0, -1.0, 2.0], delta=4e-2, nk=40, write=False)
    _, dk2 = G['kagome_lattice'].get_hamiltonian(tij=[-1.0]).get_dos(energies=[-2.0, -1.0, 2.0], delta=4e-2, nk=40, write=False)
    ok = near(areas, [1, 2, 3], 0.03) and near(d1, 1 / (2 * np.pi), 2e-3) and near(d2, 2 * d1, 1e-9)
    ok = ok and abs(kag_area - 2.969) < 1e-3 and ek[np.argmax(dk)] == 2.0 and abs(dk.max() - 8.10) < 5e-3
    ok = ok and near(kag_peaks, [0.70, 0.70], 6e-3) and abs(kag_v - 0.042) < 1e-3 and near(dk2, 2 * np.asarray(dk1), 1e-9)
    check('the density of states of pyqula', ok,
          'the area of h.get_dos is %.3f %.3f %.3f for the chain, honeycomb and kagome lattices, the chain gives %.4f at 0 '
          'and %.4f spinful, and the call of kagome_dos (tij=[-1.], has_spin=False, delta=0.04, nk=200) has the area %.3f '
          'on (-5, 3), its largest value %.2f at %.1f against 1/(pi delta) = %.2f, the peaks %.2f and %.2f at -2 and 0, the '
          'V %.3f at -1, and twice these with spin' % (*areas, d1[0], d2[0], kag_area, dk.max(), ek[np.argmax(dk)],
                                                      1 / (np.pi * 0.04), *kag_peaks, kag_v))

    energies = np.linspace(-3.5, 3.5, 400)
    e, d = H['honeycomb_lattice'].get_dos(delta=4e-2, energies=energies, nk=200, write=False)
    e, d = np.asarray(e), np.asarray(d)
    z = np.abs(e) < 0.3
    dmin, emin = d[z].min(), e[z][np.argmin(d[z])]
    pk = [e[e > 0][np.argmax(d[e > 0])], e[e < 0][np.argmax(d[e < 0])]]
    et, dt = H['triangular_lattice'].get_dos(delta=4e-2, energies=energies, nk=200, write=False)
    et, dt = np.asarray(et), np.asarray(dt)
    near0 = dt[np.abs(et) < 0.1]
    m = 1500
    s = (np.arange(m) + 0.5) / m * 2 * np.pi
    Etri = (2 * (np.cos(s)[:, None] + np.cos(s)[None, :] + np.cos(s[:, None] + s[None, :]))).ravel()    # the default sign
    exact = np.mean(np.abs(Etri) < 0.01) / 0.02
    check('the call of the notebook', near(np.trapezoid(d, e), 1.979, 0.002) and near(dmin, 0.041, 0.001) and abs(emin) < 0.01
          and near(pk, [1.009, -1.009], 0.001) and near(exact, 0.107, 0.002) and 0.100 < near0.min() and near0.max() < 0.115
          and near(et[np.argmax(dt)], -2.009, 0.001),
          'the honeycomb call has the area %.3f, the minimum %.3f at %.3f and the peaks at %.3f and %.3f on its grid, and '
          'the triangular one gives %.3f to %.3f within 0.1 of zero, where a count gives %.4f, and its peak at %.3f'
          % (np.trapezoid(d, e), dmin, emin, pk[0], pk[1], near0.min(), near0.max(), exact, et[np.argmax(dt)]))

    def saddles(f, ks):
        out = []
        for k in ks:
            hx = 1e-4
            Hs = np.array([[(f(k + hx * (a + b)) - f(k + hx * (a - b)) - f(k - hx * (a - b)) + f(k - hx * (a + b))) / (4 * hx ** 2)
                            for b in np.eye(2)] for a in np.eye(2)])
            out.append(np.linalg.eigvalsh(Hs))
        return out
    sqs = saddles(lambda k: -2 * (np.cos(k[0]) + np.cos(k[1])), [np.array([np.pi, 0])])
    hos = saddles(lambda k: abs(honey_f(k, DELTA)), [MN])
    trs = saddles(lambda k: ev(hk, k)[0], [Mt])
    kgs = saddles(lambda k: kagome_bands(k)[0], [Mk]) + saddles(lambda k: kagome_bands(k)[1], [Mk])
    vals = [-2 * (np.cos(np.pi) + 1), abs(honey_f(MN, DELTA)), ev(hk, Mt)[0], kagome_bands(Mk)[0], kagome_bands(Mk)[1]]
    _, dtp = H['triangular_lattice'].get_dos(energies=np.linspace(-2.3, -1.7, 61), delta=0.02, nk=300, write=False)
    _, dkp = H['kagome_lattice'].get_dos(energies=np.linspace(-0.3, 2.3, 131), delta=0.02, nk=200, write=False)
    ekp = np.linspace(-0.3, 2.3, 131)
    lowk = ekp < 1.0
    ok = all(x[0] * x[1] < 0 for x in sqs + hos + trs + kgs) and near(vals, [0, 1, 2, -2, 0], 1e-9)
    ok = ok and near(np.linspace(-2.3, -1.7, 61)[np.argmax(dtp)], -2, 0.011) and near(ekp[lowk][np.argmax(np.asarray(dkp)[lowk])], 0, 0.021)
    ok = ok and near(ekp[~lowk][np.argmax(np.asarray(dkp)[~lowk])], 2, 0.021)
    e198 = 1.98
    g198 = np.mean(np.abs(Ec - e198) < 5e-3) / 1e-2
    g_ex, g_edge = 1 / (np.pi * np.sqrt(4 - e198 ** 2)), 1 / (np.pi * np.sqrt(4 * (2 - e198)))
    check('the van Hove energies', ok and abs(g198 / g_ex - 1) < 0.01 and abs(g_ex / g_edge - 1) < 0.01,
          'with -t the saddles are at %s for the square (X), honeycomb (M), triangular (M) and kagome (M, two bands), '
          'pyqula with +1 peaks at -2 on the triangular and at 0 and 2 on the kagome lattice, and the chain has %.3f at 1.98 '
          'on a mesh, %.3f from the formula and %.3f from the form at the edge' % (np.round(vals, 3).tolist(), g198, g_ex, g_edge))

    kmesh = [np.array([i, j]) / 30 @ Bk for i in range(30) for j in range(30)]
    ek = np.array([kagome_bands(k) for k in kmesh])
    lmesh = [np.array([i, j]) / 30 @ Bl for i in range(30) for j in range(30)]
    el = np.array([ev(hl, k) for k in lmesh])
    elp = np.array([ev(hlp, k) for k in lmesh])
    ok = near(ek[:, 2], 2, 1e-9) and ek[:, :2].min() > -4 - 1e-9 and ek[:, :2].max() < 2 + 1e-9 and near(ek[:, :2].min(), -4, 1e-9)
    ok = ok and near(el[:, 1], 0, 1e-9) and near(elp[:, 1], 0, 1e-9)
    check('the flat bands', ok, 'the kagome flat band is at 2t at every momentum of a 30 x 30 mesh, one band of three, so one third '
          'of the states, the two others lie in %.3f to %.3f, and the middle Lieb band is 0 for both signs' % (ek[:, :2].min(), ek[:, :2].max()))

    h3, _, _ = cart(G['chain'].get_hamiltonian(has_spin=False, tij=[1.0, 0.0, 1 / 3]))
    E3 = lambda p: ev(h3, p)[0]
    x0 = np.pi / 2
    der = [(E3(x0 + 1e-3) - E3(x0 - 1e-3)) / 2e-3, (E3(x0 + 1e-3) - 2 * E3(x0) + E3(x0 - 1e-3)) / 1e-6,
           (E3(x0 + 2e-3) - 2 * E3(x0 + 1e-3) + 2 * E3(x0 - 1e-3) - E3(x0 - 2e-3)) / (2 * 1e-9)]
    Ep = 2 * np.cos(pc) + (2 / 3) * np.cos(3 * pc)
    expo = np.log10(np.mean(np.abs(Ep) < 1e-3) / np.mean(np.abs(Ep) < 1e-4)) - 1
    check('the third-neighbor hopping of the notebook', abs(E3(x0)) < 1e-12 and abs(der[0]) < 1e-5 and abs(der[1]) < 1e-4
          and abs(der[2] + 16) < 1e-2 and abs(expo + 2 / 3) < 0.01,
          'tij=[1,0,1/3] gives 2 cos k + (2/3) cos 3k, with energy, slope and curvature 0 at k = pi/2 and the third derivative '
          '%.2f, so the density of states grows as |E|^%.3f toward zero energy' % (der[2], expo))

    # Velocity, mass and the Fermi surface
    hk1, _, _ = cart(Hm['chain'])
    E1 = lambda p: ev(hk1, p)[0]
    vel = [(E1(p + 1e-5) - E1(p - 1e-5)) / 2e-5 for p in (0, np.pi / 2, np.pi)]
    cur = [(E1(p + 1e-4) - 2 * E1(p) + E1(p - 1e-4)) / 1e-8 for p in (0, np.pi / 2, np.pi)]
    ends = [E1(0.01) - (-2 + 0.01 ** 2), E1(np.pi + 0.01) - (2 - 0.01 ** 2)]
    check('velocity and mass of the chain', near(vel, [0, 2, 0], 1e-6) and near(cur, [2, 0, -2], 1e-3) and near(ends, 0, 1e-8),
          'with tij=[-1.] the slope is %.3f %.3f %.3f and the curvature %.3f %.3f %.3f at phi = 0, pi/2, pi, and the band is '
          '-2 + phi^2 and 2 - delta^2 at the ends to fourth order' % (*vel, *cur))

    sqc = []
    for p in ([0, 0], [np.pi, 0], [np.pi, np.pi]):
        p = np.array(p, float)
        sqc.append([(ev(hs, p + 1e-4 * u)[0] - 2 * ev(hs, p)[0] + ev(hs, p - 1e-4 * u)[0]) / 1e-8 for u in np.eye(2)])
    check('the masses of the square lattice', near(sqc, [[2, 2], [-2, 2], [-2, -2]], 1e-3),
          'the curvatures along x and y are %s at Gamma, X and M, so X is a saddle point' % np.round(sqc, 3).tolist())

    fine = np.linspace(-np.pi, np.pi, 400001)
    info = {}
    for et in (0.2, 0.3, 0.5):
        b = -2 * np.cos(fine) - 2 * et * np.cos(2 * fine)
        top = b.max()
        info[et] = (top - b[-1], b[len(b) // 2], b[-1], top, np.sum((b[1:-1] > b[:-2]) & (b[1:-1] > b[2:])) + np.sum((b[1:-1] < b[:-2]) & (b[1:-1] < b[2:])))
    c_pi = lambda et: (-2 * np.cos(np.pi + 1e-4) - 2 * et * np.cos(2 * (np.pi + 1e-4)) - 2 * (2 - 2 * et) + (-2 * np.cos(np.pi - 1e-4) - 2 * et * np.cos(2 * (np.pi - 1e-4)))) / 1e-8
    ok = near([c_pi(0.2), c_pi(0.3), c_pi(0.5)], [8 * 0.2 - 2, 8 * 0.3 - 2, 8 * 0.5 - 2], 1e-3)
    ok = ok and all(near(-2 * np.cos(np.pi / 2) - 2 * et * np.cos(np.pi), 2 * et, 1e-12) for et in (0.2, 0.3, 0.5))
    ok = ok and near([info[0.3][0], info[0.5][0]], [(4 * 0.3 - 1) ** 2 / 1.2, 0.5], 1e-6) and info[0.2][0] < 1e-12
    ok = ok and near(info[0.5][1:4], [-3, 1, 1.5], 1e-6) and info[0.2][4] == 1 and info[0.3][4] == 3 and info[0.5][4] == 3
    hq5, _, _ = cart(G['chain'].get_hamiltonian(has_spin=False, tij=[1.0, 0.5]))
    ext = sorted([ev(hq5, 0)[0], ev(hq5, np.pi)[0], ev(hq5, np.arccos(-0.25 / 0.5))[0]])
    check('the chain with a second-neighbor hopping (2.9)', ok and near(ext, [-1.5, -1, 3], 1e-12),
          'eps(pi/2) = 2 eta, the curvature at pi is 8 eta - 2t, the dip at pi is %.4f for eta=0.3, %.4f for 0.5 and none for 0.2, eta=0.5 has '
          '%.0f at 0, %.0f at pi and the maxima %.1f, a width of 4.5, and pyqula with tij=[1,0.5] has %s'
          % (info[0.3][0], info[0.5][0], *info[0.5][1:4], np.round(ext, 3).tolist()))

    ns = 400
    s = np.linspace(-np.pi, np.pi, ns, endpoint=False)
    Esq = -2 * (np.cos(s)[:, None] + np.cos(s)[None, :])
    Q = np.roll(np.roll(Esq, ns // 2, 0), ns // 2, 1)
    below = np.mean(Esq < -1e-12) + 0.5 * np.mean(np.abs(Esq) < 1e-12)
    line = np.abs(np.abs(s[:, None]) + np.abs(s[None, :]) - np.pi) < 1e-9
    Ech = -2 * np.cos(s)
    check('half filling', near(Q, -Esq, 1e-12) and near(below, 0.5, 1e-12) and near(Esq[line], 0, 1e-12) and near(np.mean(Ech < 0), 0.5, 0.01),
          'eps(k+Q) = -eps(k) with Q=(pi,pi), half of the states below zero, eps vanishes on |phi_x|+|phi_y|=pi, and the '
          'chain is below zero for |phi| < pi/2, so k_F = pi/2 and 2k_F = pi')

    from scipy import ndimage
    n = 240
    s = np.arange(n) / n
    fm = np.array([np.abs(honey_f(s[i] * Bh[0] + s[:, None] * Bh[1], DELTA)) for i in range(n)])
    def pieces(mask):
        """The number of connected regions of the mask on the torus of the zone."""
        lab, num = ndimage.label(mask)
        root = list(range(num + 1))
        def find(a):
            while root[a] != a:
                a = root[a]
            return a
        for a, b in list(zip(lab[:, 0], lab[:, -1])) + list(zip(lab[0, :], lab[-1, :])):
            if a and b:
                root[find(a)] = find(b)
        return len(set(find(a) for a in range(1, num + 1)))
    cnts = [pieces(fm < x) for x in (0.5, 0.999)] + [pieces(fm > 1.5)]
    cM = saddles(lambda k: abs(honey_f(k, DELTA)), [MN])[0]
    check('the Fermi surface of the honeycomb lattice', cnts == [2, 2, 1] and near(sorted(cM), [-1.5, 4.5], 1e-4),
          'on a 240^2 mesh the states with |E| below 0.5 and 0.999 form %d and %d pockets, above 1.5 %d region around '
          'Gamma, and the upper band has the curvatures %.2f and %.2f at M, where the pockets meet at |E| = t'
          % (cnts[0], cnts[1], cnts[2], *sorted(cM)))

    nk = 31                                                            # x=0 and y=2/3 are points of the mesh
    x, y, wfs = H['honeycomb_lattice'].get_fermi_surface(e=0.0, delta=0.05, nk=nk, write=False)
    x, y, wfs = np.asarray(x), np.asarray(y), np.asarray(wfs)
    unit = 2 * np.pi / lc['honeycomb_lattice']
    wref = np.array([sum(0.05 / ((0 - E) ** 2 + 0.05 ** 2) for E in (-abs(honey_f(unit * np.array([a, b]), DELTA)), abs(honey_f(unit * np.array([a, b]), DELTA))))
                     for a, b in zip(x, y)])
    _, _, wsp = G['honeycomb_lattice'].get_hamiltonian().get_fermi_surface(e=0.0, delta=0.05, nk=nk, write=False)
    iK = np.argmin(np.abs(x) + np.abs(y - 2 / 3))
    kb, eb = H['honeycomb_lattice'].get_bands_map(n=0, nk=20, write=False)
    kb, eb = np.asarray(kb), np.asarray(eb)
    eref = np.array([-abs(honey_f(unit * kq[:2], DELTA)) for kq in kb])
    zones = (4 * np.pi / lc['honeycomb_lattice']) ** 2 / abs(np.linalg.det(Bh))
    ok = near([x[0], x[-1], y[0], y[-1]], [-1, 1, -1, 1], 1e-12) and x[0] == x[1] and y[1] > y[0] and len(x) == nk * nk
    ok = ok and near(wfs, wref, 1e-8) and near(wsp, 2 * wfs, 1e-8) and near(wfs[iK], 40, 1e-6) and near(y[iK], 2 / 3, 1e-12)
    ok = ok and near(np.unique(kb[:, 0]), np.linspace(-1, 1, 20, endpoint=False), 1e-12) and kb[0, 0] == kb[1, 0] and near(eb, eref, 1e-9)
    check('the maps of pyqula', ok and near(zones, 2 * S3, 1e-12),
          'get_fermi_surface gives nk^2 points from -1 to 1 with both ends, x the slow index, in units of 2 pi over |a1|, '
          'the weight sum delta/((e-E)^2+delta^2), %.1f = 2/delta at K and twice when spinful, and get_bands_map runs from '
          '-1 to 1-2/nk with band 0 the lowest, a window of %.2f zones of the honeycomb lattice' % (wfs[iK], zones))

    # Chains with more sites per cell
    hb2 = G['bichain'].get_hamiltonian(has_spin=False)
    hb2.inter = 0.6 * hb2.inter
    h13, _, _ = cart(hb2)
    b0, bpi = ev(h13, 0.0), ev(h13, np.pi / 2)                          # the cell has a=2, so phi = 2k
    hb1, _, _ = cart(G['bichain'].get_hamiltonian(has_spin=False))
    pp = np.linspace(-np.pi, np.pi, 9)
    one = np.array([ev(hb1, p / 2)[1] for p in pp])
    check('the chain of (2.13)', near(b0, [-1.6, 1.6], 1e-12) and near(bpi, [-0.4, 0.4], 1e-12)
          and near(one, 2 * np.abs(np.cos(pp / 2)), 1e-12),
          'bichain with h.inter = 0.6*h.inter has +-1.6 at phi=0 and the gap %.2f at phi=pi, and with eta=1 the bands '
          '+-2|cos(phi/2)|, the chain folded into the zone of two sites' % (bpi[1] - bpi[0]))

    E60 = np.sort(np.linalg.eigvalsh(ring(60, [-1.0])))
    fold = {}
    for nn in (3, 4):
        br = [np.sort(-2 * np.cos((p + 2 * np.pi * np.arange(nn)) / nn)) for p in 2 * np.pi * np.arange(60 // nn) / (60 // nn)]
        fold[nn] = (np.sort(np.concatenate(br)), br[0])
    hs3 = geometry.chain().get_supercell(3)
    e3d = np.linalg.eigvalsh(hs3.get_hamiltonian(has_spin=False).get_hk_gen()([0, 0, 0]))
    e3m = np.linalg.eigvalsh(hs3.get_hamiltonian(has_spin=False, tij=[-1.0]).get_hk_gen()([0, 0, 0]))
    hs5 = geometry.chain().get_supercell(5).get_hamiltonian(has_spin=False, tij=[-1.0, -0.8])
    e5 = np.linalg.eigvalsh(hs5.get_hk_gen()([0, 0, 0]))
    r5 = np.linalg.eigvalsh(ring(5, [-1.0, -0.8]))
    check('band folding', near(fold[3][0], E60, 1e-12) and near(fold[4][0], E60, 1e-12) and near(fold[3][1], [-2, 1, 1], 1e-12)
          and near(fold[4][1], [-2, 0, 0, 2], 1e-12) and near(e3d, [-1, -1, 2], 1e-12) and near(e3m, [-2, 1, 1], 1e-12)
          and near(hs3.a1, [3, 0, 0]) and near(e5, r5, 1e-12),
          'the branches of cells of 3 and 4 sites are the levels of a ring of 60, -2t, t, t and -2t, 0, 0, 2t at phi=0, '
          'chain().get_supercell(3) has a=3 and %s at k=0, %s with tij=[-1.], and get_supercell(5) with tij=[-1,-0.8] '
          'has the levels %s of the ring of five sites' % (np.round(e3d, 3).tolist(), np.round(e3m, 3).tolist(), np.round(e5, 3).tolist()))

    hlad = H['ladder']
    lad_intra, lad_inter = np.asarray(hlad.intra).real, np.asarray(hlad.inter).real
    hlk, _, _ = cart(hlad)
    l0, lpi = ev(hlk, 0.0), ev(hlk, np.pi)
    lw = max(np.abs(ev(hlk, p) - np.sort([2 * np.cos(p) - 1, 2 * np.cos(p) + 1])).max() for p in (0.3, 1.2, 2.5))
    check('the ladder of the notebook', near(lad_intra, [[0, 1], [1, 0]]) and near(lad_inter, np.eye(2)) and near(l0, [1, 3], 1e-12)
          and near(lpi, [-3, -1], 1e-12) and lw < 1e-12,
          'geometry.ladder() has the rung 1 in h.intra and the two legs 1 in h.inter, so the bands 2 cos(phi) -+ 1, %s at 0 '
          'and %s at pi, where (2.13) with eta=1 has -2, 2 and 0, 0' % (np.round(l0, 3).tolist(), np.round(lpi, 3).tolist()))

    # Rings and ARPES
    Hp = ring(5, [1.0])
    ep, vp = np.linalg.eigh(Hp)
    a = np.linspace(0, np.pi, 181)
    modes = [np.exp(1j * 4 * np.pi / 5 * np.arange(5)) / np.sqrt(5), np.exp(-1j * 4 * np.pi / 5 * np.arange(5)) / np.sqrt(5)]
    wts = np.array([np.abs(np.cos(x) * modes[0] + np.sin(x) * modes[1]) ** 2 for x in a])
    em = np.linalg.eigvalsh(ring(5, [-1.0]))
    six = ring(6, [-1.0, -0.3])
    four6 = [np.exp(2j * np.pi * nq * np.arange(6) / 6) for nq in range(6)]
    ok6 = all(np.allclose(six @ f6, (f6.conj() @ six @ f6 / 6) * f6) for f6 in four6)
    check('rings', near(ep[:2], 2 * np.cos(4 * np.pi / 5), 1e-12) and near([wts.min(), wts.max()], [0, 0.4], 1e-6)
          and near(em[0], -2) and em[1] - em[0] > 1 and near(np.sort(r5), [-3.6, 0.6764, 0.6764, 1.1236, 1.1236], 1e-4) and ok6,
          'with +1 the lowest level of 5 sites is %.3f twice and a site has the weight %.2f to %.2f in its states, with -1 '
          'the ground state is single, and t2=0.8t gives %s' % (ep[0], wts.min(), wts.max(), np.round(r5, 3).tolist()))

    hbar, me, eV = 1.054571817e-34, 9.1093837015e-31, 1.602176634e-19
    c = hbar ** 2 / (2 * me) / eV * 1e20
    kk = np.sqrt(20.0 / c) * 10
    kpar = [kk * np.sin(np.radians(x)) for x in (10, 20)]
    check('ARPES', near(c, 3.810, 5e-4) and near(kk, 22.91, 0.01) and near(kpar, [3.98, 7.84], 0.01),
          'hbar^2/2m = %.4f eV A^2, an electron of 20 eV has k = %.2f nm^-1, and 10 and 20 degrees give %.2f and %.2f nm^-1'
          % (c, kk, *kpar))

    # Points of the old text, all decided or corrected on 2026-11-22
    check('corrected, the dimer of Section 2.3', near(esy, 1) and near(ms, 1),
          'c1+ + c2+ has the mirror +1 and the energy +t, the upper level for t > 0, so the page calls it symmetric')
    check('decided, the direction of the ring', near(R4 @ s4, -1j * s4) and near(T4 @ s4, -1j * s4)
          and near(shift(3, -1) @ v3, np.exp(2j * np.pi / 3) * v3),
          '(1,-i,-1,i) has R=T=-i, and R gives e^{i phi j} the eigenvalue e^{i phi}, as T does')
    check('decided, (2.7)', near(orth, L * np.eye(L), 1e-12) and near(Hdiag, np.diag(-2 * np.cos(ph)), 1e-12),
          'the sum is L delta, and with 1/sqrt(L) in (2.7) the band is (2.8) with no factor')
    check('corrected, the ring of five sites', near(ep[1] - ep[0], 0, 1e-12) and wts.max() > 0.39,
          'with +1 the lowest level is degenerate, and a state of it has a weight up to %.2f on one site' % wts.max())
    v3r = np.array([2, -1, -1]) / np.sqrt(6)
    e3 = np.linalg.eigvalsh(ring(3, [-1.0]))
    check('decided, the ring of three sites', near(e3, [-2, 1, 1], 1e-12) and near(ring(3, [-1.0]) @ v3r, v3r)
          and not near(shift(3, -1) @ v3r, v3r) and near(v3r[0] ** 2, 2 / 3),
          'with the hopping -t of (2.5) the levels are %s, so the twofold level is +t, and (2,-1,-1)/sqrt6 is an '
          'eigenstate of it that is no Fourier mode, so the page and the caption of Figure 2.1 say that the eigenstates '
          'can be chosen as the Fourier modes' % np.round(e3, 6).tolist())
    check('corrected, the try-it of Section 2.5', info[0.3][4] == 3 and near(info[0.3][0], 0.0333, 1e-4),
          'eta=0.3 already has the extremum at pi, %.4f deep, so the try-it starts at 0.2' % info[0.3][0])
    check('corrected, the notebook box of Section 2.5', chain_cell == 'tij=[1.0,0.]' and near(chain_band([1.0, 0.0]), 2 * np.cos(phis), 1e-12),
          'the cell has tij=[1.0,0.], which gives +2 cos(phi)')
    check('corrected, the notebook box of Section 2.7', near(l0, [1, 3], 1e-12),
          'the ladder has 2 cos(phi) -+ 1, not +-|1 + eta e^{-i phi}|')
    print('%d checks hold, %.1f s' % (COUNT[0], time.time() - t0))


if __name__ == '__main__':
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            main()
        finally:
            os.chdir(cwd)
