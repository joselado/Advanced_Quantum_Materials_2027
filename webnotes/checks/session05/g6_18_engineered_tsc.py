"""Session 5, the numbers and the statements of page 18 (Section 5.18) that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a box is an assert, here
or in the figure script that draws it. The ticks and the levels of helical_edge_gap are asserted in
figures/session05/helical_edge_gap.py, the numbers of the picture quiz also in figures/session05/_g6_edge.py, and the curve
of the notebook model (0.3 at J=0, the level at Gamma from J=0.225 of the grid on, the dip at J=0.42, C=0 at J=0.3 and C=1
at J=0.6) in figures/session05/g6_artificial_tsc.py. This script holds the rest. It uses the edge Hamiltonian of the page,

    H(k) = tau_z (v k sigma_z - mu) + h sigma_x + Delta tau_x,

in the Nambu basis (5.6) with tau first in the Kronecker product, a lattice version of it for the zero modes, and pyqula for
the model of the notebook, with the Chern numbers also from the link variables of webnotes/figures/physcheck.py. The part
on the notebook model takes about 30 s. pyqula runs in a temporary folder, so the script writes no file.

Run it from anywhere:  python3 webnotes/checks/session05/g6_18_engineered_tsc.py"""
import os, sys, tempfile
import numpy as np
from scipy.optimize import minimize, minimize_scalar, brentq


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


S0, SX, SY, SZ = np.eye(2), np.array([[0., 1.], [1., 0.]]), np.array([[0., -1j], [1j, 0.]]), np.diag([1., -1.])
T = lambda a, b: np.kron(a, b)                                   # tau first, sigma second


def edge(k, h, D, mu, v=1.0):
    return T(SZ, v * k * SZ - mu * S0) + h * T(S0, SX) + D * T(SX, S0)


def emin_k(h, D, mu, ks):
    return min(np.abs(np.linalg.eigvalsh(edge(k, h, D, mu))).min() for k in ks)


# ---- the text before the key box: the kinetic term and mu change sign in the hole block, the exchange keeps it. This is the
# rule of the conventions sheet, -sigma_y h(-k)^* sigma_y for the hole block, applied to each term of the edge
hole = lambda hk, k: -SY @ hk(-k).conj() @ SY
k0 = 0.7
check('text: v k sigma_z (even under time reversal) and -mu change sign in the hole block, h sigma_x keeps it',
      np.allclose(hole(lambda k: k * SZ, k0), -k0 * SZ) and np.allclose(hole(lambda k: -0.4 * S0, k0), 0.4 * S0)
      and np.allclose(hole(lambda k: 0.3 * SX, k0), 0.3 * SX), 'ok')
check('text: the same rule gives the edge H(k) of the page', np.allclose(
    np.block([[k0 * SZ - 0.4 * S0 + 0.3 * SX, 0.5 * S0], [0.5 * S0, hole(lambda k: k * SZ - 0.4 * S0 + 0.3 * SX, k0)]]),
    edge(k0, 0.3, 0.5, 0.4)), 'ok')

# ---- the key box and its steps: at k=0 and mu=0 the levels are +-h +- Delta
ok = all(np.allclose(np.linalg.eigvalsh(edge(0, h, D, 0)), np.sort([h + D, h - D, -h + D, -h - D]))
         for h, D in ((0.3, 0.5), (0.7, 1.0), (1.4, 1.0), (0.2, 0.2)))
check('key: E(k=0) = +-h +- Delta at mu=0, four pairs of h and Delta', ok, 'ok')
check('steps: [sigma_x, tau_x] = 0', np.allclose(T(S0, SX) @ T(SX, S0) - T(SX, S0) @ T(S0, SX), 0), 0)
check('steps: with Delta=0 the levels are +-h, each twice', np.allclose(np.linalg.eigvalsh(edge(0, 0.7, 0, 0)), [-0.7, -0.7, 0.7, 0.7]), 'ok')
check('steps: with h=0 the levels are +-Delta, each twice', np.allclose(np.linalg.eigvalsh(edge(0, 0, 0.5, 0)), [-0.5, -0.5, 0.5, 0.5]), 'ok')
check('steps: eps tau_z and Delta tau_x anticommute', np.allclose(T(SZ, S0) @ T(SX, S0) + T(SX, S0) @ T(SZ, S0), 0), 0)
ks = np.linspace(-3, 3, 1201)
hs = np.linspace(0, 2, 81)
g = np.array([emin_k(h, 1.0, 0.0, ks) for h in hs])
check('key: at mu=0 the gap over all k closes at h=Delta and only there', g[40] < 1e-9 and np.all(g[np.abs(hs - 1) > 0.04] > 0.03),
      (round(g[40], 12), round(g[np.abs(hs - 1) > 0.04].min(), 4)))

# ---- the key box: the two sides of h=Delta are two phases, and a zero mode sits at their boundary. A lattice edge
# v sin k sigma_z + W (1 - cos k) sigma_x, whose second term gaps the doubler at k=pi, with a segment of pairing Delta=0.3
# between two magnets h=0.6, as in the conventions sheet
N, v, W = 200, 1.0, 1.0
def bdg_lattice(hn, Dn, mu=0.0):
    he = np.zeros((2 * N, 2 * N), dtype=complex)
    for n in range(N):
        he[2 * n:2 * n + 2, 2 * n:2 * n + 2] = W * SX - mu * S0 + hn[n] * SX
        if n + 1 < N:
            t = v / 2j * SZ - W / 2 * SX                         # v sin k sigma_z + W (1 - cos k) sigma_x
            he[2 * n:2 * n + 2, 2 * n + 2:2 * n + 4] = t
            he[2 * n + 2:2 * n + 4, 2 * n:2 * n + 2] = t.conj().T
    Y = np.kron(np.eye(N), SY)
    hh = -Y @ he.conj() @ Y                                      # the hole block of (5.6)
    P = np.kron(np.diag(Dn), S0)
    return np.block([[he, P], [P.conj().T, hh]])
inside = (np.arange(N) >= 60) & (np.arange(N) < 140)
e, vec = np.linalg.eigh(bdg_lattice(np.where(inside, 0.0, 0.6), np.where(inside, 0.3, 0.0)))
order = np.argsort(np.abs(e))
w = (np.abs(vec[:, order[:2]])**2).sum(axis=1).reshape(2, N, 2).sum(axis=(0, 2)) / 2
near = (np.abs(np.arange(N) - 60) <= 15) | (np.abs(np.arange(N) - 139) <= 15)
check('key: a segment Delta=0.3 between magnets h=0.6 has two levels at zero, at its two ends, and the next level at 0.3',
      np.abs(e[order[:2]]).max() < 1e-9 and w[near].sum() > 0.999 and abs(np.abs(e[order[2]]) - 0.3) < 0.01,
      (np.abs(e[order[:2]]).max(), round(w[near].sum(), 5), round(abs(e[order[2]]), 4)))

# ---- the quiz with equations as options
lv = np.linalg.eigvalsh(edge(0, 0.3, 0.5, 0))
check('quiz: h=0.3, Delta=0.5 give the levels +-0.2 and +-0.8', np.allclose(lv, [-0.8, -0.2, 0.2, 0.8]), np.round(lv, 4))
check('quiz: sqrt(h^2 + Delta^2) = 0.58 is not a level', abs(np.sqrt(0.34) - 0.58) < 5e-3 and np.min(np.abs(lv - np.sqrt(0.34))) > 0.2,
      round(np.sqrt(0.34), 4))
check('quiz: +-(h - Delta) = +-0.2 is the pair that crosses zero at h=Delta', np.allclose(np.linalg.eigvalsh(edge(0, 0.5, 0.5, 0))[1:3], 0),
      'ok')

# ---- the picture quiz, with v=1 and mu=0.2
kq = np.linspace(-0.65, 0.65, 651)
lev = lambda h, D: np.array([np.linalg.eigvalsh(edge(k, h, D, 0.2)) for k in kq])
eb, em, ep = lev(0, 0), lev(0.5, 0), lev(0, 0.3)
i0 = int(np.argmin(np.abs(kq)))
check('picture quiz: with h=Delta=0 the lines cross zero at k=+-0.2', np.min(np.abs(np.linalg.eigvalsh(edge(0.2, 0, 0, 0.2)))) < 1e-12
      and np.min(np.abs(np.linalg.eigvalsh(edge(-0.2, 0, 0, 0.2)))) < 1e-12, 'ok')
m = np.min(np.abs(em), axis=1)
check('picture quiz: the magnet h=0.5 gives the smallest energy h - mu = 0.3, at k=0', abs(m.min() - 0.3) < 1e-12 and int(np.argmin(m)) == i0,
      round(m.min(), 6))
p = np.min(np.abs(ep), axis=1)
check('picture quiz: the pairing gives 0.3 at k=+-0.2 and +-sqrt(mu^2+Delta^2) = +-0.36 at k=0',
      abs(p.min() - 0.3) < 1e-9 and np.allclose(np.abs(kq[p < 0.3 + 1e-9]), 0.2) and np.allclose(np.abs(ep[i0]), np.sqrt(0.13))
      and abs(np.sqrt(0.13) - 0.36) < 1e-2, (round(p.min(), 6), round(np.sqrt(0.13), 4)))

# ---- the problem, Delta=0.3 and mu=0.4
D, mu = 0.3, 0.4
A = -mu * SZ + D * SX
check('problem: (-mu tau_z + Delta tau_x)^2 = (mu^2 + Delta^2) 1 = 0.25', np.allclose(A @ A, 0.25 * S0), 0.25)
ok = all(np.allclose(np.linalg.eigvalsh(edge(0, h, D, mu)), np.sort([h + 0.5, h - 0.5, -h + 0.5, -h - 0.5])) for h in (0.1, 0.5, 0.9))
check('problem: E(k=0) = +-h +- sqrt(Delta^2 + mu^2) = +-h +- 0.5', ok and abs(np.sqrt(0.09 + 0.16) - 0.5) < 1e-12, 'ok')
hs = np.linspace(0, 1, 101)
g = np.array([emin_k(h, D, mu, ks) for h in hs])
check('problem: the smallest energy over all k vanishes only at h=0.5', g[50] < 1e-9 and np.all(g[np.abs(hs - 0.5) > 0.02] > 0.015),
      (g[50], round(g[np.abs(hs - 0.5) > 0.02].min(), 4)))

# ---- the model of the notebook, with pyqula in a temporary folder
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'figures'))
import physcheck


def bloch(h):
    """The Bloch matrix of a pyqula Hamiltonian at the reduced momenta k1, k2 (arrays of any shape), from its intra-cell
    matrix and its hoppings, so that a whole mesh is diagonalized at once. It is compared with h.get_hk_gen() below."""
    dense = lambda m: np.array(m.todense() if hasattr(m, 'todense') else m)
    intra = dense(h.intra)
    hops = [(np.array(t.dir[:2], float), dense(t.m)) for t in h.hopping]

    def H(k1, k2):
        k1, k2 = np.asarray(k1, float)[..., None, None], np.asarray(k2, float)[..., None, None]
        out = intra + 0j * k1
        for d, m in hops:
            out = out + m * np.exp(2j * np.pi * (d[0] * k1 + d[1] * k2))
        return out
    return H


cwd = os.getcwd()
with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    try:
        from pyqula import geometry
        gt = geometry.triangular_lattice()

        def model(J, rashba=1.0, pairing=0.3):
            h = gt.get_hamiltonian(); h.add_onsite(-5.7)
            if rashba:
                h.add_rashba(rashba)
            if pairing:
                h.add_zeeman([0., 0., J]); h.add_swave(pairing)
            return h

        # the hopping of pyqula: +1 on the triangular lattice, which is eps(k) = -2t sum cos(k.a) with t=-1
        hb = gt.get_hamiltonian(has_spin=False)
        hkb, B = physcheck.from_pyqula(hb)
        a1, a2 = np.array(gt.a1[:2]), np.array(gt.a2[:2])
        eps_notes = lambda k, t: -2 * t * (np.cos(k @ a1) + np.cos(k @ a2) + np.cos(k @ (a1 + a2)))
        rng = np.random.default_rng(3)
        ok = all(abs(np.linalg.eigvalsh(hkb(k))[0] - eps_notes(k, -1.0)) < 1e-12 for k in rng.uniform(-4, 4, (20, 2)))
        K = (B[0] + B[1]) / 3
        eb = np.array([np.linalg.eigvalsh(hkb(k))[0] for k in physcheck.kmesh(B, 60, points=(K,))])
        check('caption: in pyqula the hopping is +1, which is t=-1 of the notes, so the band runs from -3 at K to 6 at Gamma',
              ok and abs(eb.min() + 3) < 1e-12 and abs(eb.max() - 6) < 1e-12 and abs(np.linalg.eigvalsh(hkb(K))[0] + 3) < 1e-12
              and abs(np.linalg.eigvalsh(hkb(np.zeros(2)))[0] - 6) < 1e-12, (round(eb.min(), 12), round(eb.max(), 12)))

        # add_onsite(-5.7) puts the band at Gamma at 0.3, which is the top of the band before the Rashba term
        h0 = model(0, rashba=0, pairing=0)
        hk0, _ = physcheck.from_pyqula(h0)
        e0 = np.array([np.linalg.eigvalsh(hk0(k)) for k in physcheck.kmesh(B, 60)])
        check('caption: add_onsite(-5.7) puts the band at Gamma at eps_Gamma = 0.3, the top of the band without the Rashba term',
              np.allclose(np.linalg.eigvalsh(hk0(np.zeros(2))), 0.3) and abs(e0.max() - 0.3) < 1e-12, round(e0.max(), 12))

        # with add_rashba(1.0) Gamma is the crossing of the two Rashba bands at 0.3, and the top of the band moves away
        hr = model(0, pairing=0)
        hkr, _ = physcheck.from_pyqula(hr)
        er = np.array([np.linalg.eigvalsh(hkr(k)) for k in physcheck.kmesh(B, 60)])
        lg = np.linalg.eigvalsh(hkr(np.zeros(2)))
        split = np.diff(np.linalg.eigvalsh(hkr(np.array([0.01, 0.]))))[0]
        check('caption: with add_rashba(1.0) Gamma is the crossing of the two Rashba bands at 0.3, and not the top of the band',
              np.allclose(lg, 0.3) and split > 0.05 and er.max() > 1.5, (np.round(lg, 12), round(split, 4), round(er.max(), 4)))

        # the Fermi level cuts the two Rashba bands on two closed lines around Gamma, one very close to Gamma: on 12 rays
        # inside the zone, whose edge is at 3.63 toward M and 4.19 toward K (the rays stop at 3.6), each band changes sign once, the lower one at |k| = 0.096
        rs = np.linspace(1e-4, 3.6, 3601)
        inner, outer = [], []
        for ang in np.radians(np.arange(0, 360, 30)):
            u = np.array([np.cos(ang), np.sin(ang)])
            E = np.array([np.linalg.eigvalsh(hkr(r * u)) for r in rs])
            cuts = [np.where(np.diff(np.sign(E[:, j])) != 0)[0] for j in range(2)]
            assert len(cuts[0]) == 1 and len(cuts[1]) == 1, (np.degrees(ang), cuts)
            inner.append(rs[cuts[0][0]]); outer.append(rs[cuts[1][0]])
        GM = np.linalg.norm(B[0]) / 2
        check('caption: the Fermi level cuts the two Rashba bands on two closed lines around Gamma, one very close to Gamma',
              abs(GM - 3.6276) < 1e-4 and max(inner) < 0.1 and 1.7 < min(outer) and max(outer) < 1.8,
              (round(min(inner), 4), round(max(inner), 4), round(min(outer), 4), round(max(outer), 4)))

        # the levels at Gamma of the BdG Hamiltonian
        Jc = np.sqrt(0.3**2 + 0.3**2)
        ok = all(np.allclose(np.linalg.eigvalsh(model(J).get_hk_gen()([0., 0., 0.])), np.sort([J + Jc, J - Jc, -J + Jc, -J - Jc]))
                 for J in (0, 0.2, 0.5))
        check('text: the levels at Gamma are +-J +- sqrt(eps_Gamma^2 + Delta^2), closing at J = 0.42', ok and abs(round(Jc, 2) - 0.42) < 1e-12,
              round(Jc, 4))

        # the caption: the smallest energy on the line M, Gamma, M is the smallest one over the whole zone, at all 41 values
        # of J of the figure. The zone minimum comes from a mesh of 241 x 241 reduced momenta, whose step 0.004 resolves the
        # inner Fermi line at the reduced radius 0.013, refined with Nelder-Mead from its 12 lowest points and from the
        # minimum on the line. The line minimum is refined between the points of the line of the script, 1001 of them,
        # and the dots of the figure, which are those 1001 points, lie within 2e-4 of the zone minimum.
        Js = np.linspace(0., 0.6, 41)
        line = np.linspace(-0.5, 0.5, 1001)
        a = np.arange(241) / 241 - 0.5
        A1, A2 = np.meshgrid(a, a, indexing='ij')
        refined, dots = [], []
        for J in Js:
            h = model(J)
            hk, H = h.get_hk_gen(), bloch(h)
            if J in (Js[0], Js[20], Js[40]):
                assert max(np.abs(H(x, y) - hk([x, y, 0.])).max() for x, y in rng.uniform(-0.5, 0.5, (10, 2))) < 1e-12
            f = lambda r: np.abs(np.linalg.eigvalsh(hk([r[0], r[1], 0.]))).min()
            em = np.abs(np.linalg.eigvalsh(H(A1, A2))).min(axis=-1).ravel()
            el = np.abs(np.linalg.eigvalsh(H(line, 0 * line))).min(axis=-1)
            i0 = int(np.argmin(el))
            starts = [(A1.ravel()[j], A2.ravel()[j]) for j in np.argsort(em)[:12]] + [(line[i0], 0.)]
            zone = min([minimize(f, s0, method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-12)).fun for s0 in starts]
                       + [em.min(), el.min()])
            lo, hi = line[max(i0 - 1, 0)], line[min(i0 + 1, len(line) - 1)]
            ref = minimize_scalar(lambda x: f([x, 0.]), bounds=(lo, hi), method='bounded', options=dict(xatol=1e-12)).fun
            refined.append(ref - zone); dots.append(el.min() - zone)
        refined, dots = np.array(refined), np.array(dots)
        check('caption: at all 41 J the smallest energy on the line M, Gamma, M is the smallest one over the zone, to 1e-6',
              np.abs(refined).max() < 1e-6, float(np.abs(refined).max()))
        check('figure: at all 41 J the dots, 1001 points of the line, lie within 2e-4 of the zone minimum',
              dots.min() > -1e-9 and dots.max() < 2e-4, (round(float(dots.max()), 6), float(Js[int(np.argmax(dots))])))

        hk0 = model(0.0).get_hk_gen()
        e0 = min(np.abs(np.linalg.eigvalsh(hk0([k, 0., 0.]))).min() for k in line)
        check('caption: at J=0 the smallest energy is Delta = 0.3, on the Fermi surface, and the level at Gamma is 0.42',
              abs(e0 - 0.3) < 1e-3 and abs(np.abs(np.linalg.eigvalsh(hk0([0., 0., 0.]))).min() - Jc) < 1e-12, round(e0, 5))
        def excess(J):
            hk = model(J).get_hk_gen()
            return min(np.abs(np.linalg.eigvalsh(hk([k, 0., 0.]))).min() for k in line) - abs(J - Jc) + 1e-7
        Js_on = brentq(excess, 0.15, 0.3, xtol=1e-4)
        check('caption: from about J=0.22 on, the smallest energy is the level at Gamma', 0.21 < Js_on < 0.225, round(Js_on, 4))

        # the caption: C=0 at J=0.3 and C=1 at J=0.6, from the link variables of the two BdG bands below zero, a second
        # route next to h.get_chern(nk=40) of the figure script
        C = []
        for J in (0.3, 0.6):
            hk, Bz = physcheck.from_pyqula(model(J))
            C.append([physcheck.chern_links(hk, Bz, bands=range(2), nk=nk) for nk in (24, 48)])
        C = np.array(C)
        check('caption: the links give C = 0 at J=0.3 and C = 1 at J=0.6, for nk = 24 and 48',
              np.allclose(C[0], 0, atol=1e-6) and np.allclose(C[1], 1, atol=1e-6), np.round(C, 6).tolist())
    finally:
        os.chdir(cwd)
