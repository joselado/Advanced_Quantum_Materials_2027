"""Checks of webnotes/conventions/session05.md, with numbers. Every bullet of the sheet has one check here, in the order
of the sheet, and each check asserts the numbers that its bullet states. It prints one line per check and exits 0 when
all hold. Two drafts of the sheet were written apart, and a third calculation settled the lines where they differed
or where only one of them had a line that a page needs. Those lines are checked here by that third calculation.

Not asserted, since they are not a short calculation or not a number: the reading of the prime of (5.10) as a sum
over half of the zone (only the sum over the whole zone is computed), the curve (9.10) of Session 9 (only its limit
of one site), the sign of C of the interaction-driven triplet for a given random start (only |C| = 1 is asserted, and
the signs are printed), the notebook cell "Topological modes in interaction-driven spin triplet superconductors"
(not run), what the figures draw, and the lab facts of the pages.

Run it from anywhere:  python3 webnotes/checks/session05/conventions.py"""
import importlib.util, itertools, os, sys, tempfile, time
from functools import partial
import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq, minimize, minimize_scalar

WEBNOTES = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(WEBNOTES, 'figures'))
import physcheck as pc

COUNT = [0]
KEEP = {}                                    # numbers of earlier checks that the open points quote again
S0 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]])
SZ = np.diag([1.0, -1.0]).astype(complex)
ISY = 1j * SY


def check(name, ok, detail):
    """Prints one line for a check and stops the script when it does not hold."""
    print(('ok    ' if ok else 'FAIL  ') + name + ': ' + detail, flush=True)
    assert ok, name
    COUNT[0] += 1


def dense(m):
    """A pyqula matrix as a dense numpy array."""
    return np.asarray(m.todense() if hasattr(m, 'todense') else m)


def dag(m):
    return m.conj().T


def fermions(n):
    """Jordan-Wigner annihilation operators of n fermion modes, as dense matrices of size 2^n."""
    Z, I, low = np.diag([1.0, -1.0]), np.eye(2), np.array([[0.0, 1.0], [0.0, 0.0]])
    out = []
    for j in range(n):
        m = np.array([[1.0]])
        for l in range(n):
            m = np.kron(m, Z if l < j else (low if l == j else I))
        out.append(m.astype(complex))
    return out


def bdg_realspace(he, D):
    """The BdG matrix in the per-site order (e_up, e_dn, h_dn, -h_up) of (5.6), from the electron matrix he (site by
    site, up then down) and the electron-hole block D. The hole block is -sigma_y he^* sigma_y."""
    N = he.shape[0] // 2
    S = np.kron(np.eye(N), SY)
    B = np.block([[he, D], [dag(D), -S @ he.conj() @ S]])
    p = [i for n in range(N) for i in (2 * n, 2 * n + 1, 2 * N + 2 * n, 2 * N + 2 * n + 1)]
    return B[np.ix_(p, p)]


def kitaev(N, t, mu, D, ring=False):
    """The BdG matrix of (5.19) in the basis (c_1..c_N, c_1^dag..c_N^dag), with d[n+1,n] = D = -d[n,n+1], which is
    D c_{n+1}^dag c_n^dag + h.c., the matrix of the figure scripts and of the widget kitaevbdg."""
    h = -mu * np.eye(N) - t * (np.eye(N, k=1) + np.eye(N, k=-1))
    d = D * (np.eye(N, k=-1) - np.eye(N, k=1))
    if ring:
        h[0, N - 1] = h[N - 1, 0] = -t
        d[0, N - 1], d[N - 1, 0] = D, -D
    return np.block([[h, d], [dag(d), -h.T]])


def kitaev_op(c, t, mu, D):
    """The many-body operator (5.19) on an open chain, from the annihilation operators c."""
    N = len(c)
    H = -mu * sum(dag(x) @ x for x in c)
    for n in range(N - 1):
        H = H - t * (dag(c[n]) @ c[n + 1] + dag(c[n + 1]) @ c[n]) + D * (c[n] @ c[n + 1] + dag(c[n + 1]) @ dag(c[n]))
    return H


def majorana(N, t, mu, D):
    """The real antisymmetric A of (5.19) on an open chain, H = (i/4) gamma^T A gamma + const, in the order
    (a_1, b_1, a_2, ...) with c_n = (a_n + i b_n)/2. The term -mu c^dag c gives A[a_n, b_n] = -mu, and a bond gives
    (i/2)[(D - t) a_n b_n+1 + (t + D) b_n a_n+1]. The quasiparticle energies are the moduli of the eigenvalues of iA."""
    A = np.zeros((2 * N, 2 * N))
    for n in range(N):
        A[2 * n, 2 * n + 1] = -mu
        if n < N - 1:
            A[2 * n, 2 * n + 3] = D - t
            A[2 * n + 1, 2 * n + 2] = t + D
    return A - A.T


def qp(A):
    """The quasiparticle energies of a Majorana form, sorted, each once per pair."""
    return np.sort(np.abs(np.linalg.eigvalsh(1j * A)))[::2]


def lowest(m, n=1):
    """The n smallest |E| of a BdG matrix, one per +E, -E pair."""
    return np.sort(np.abs(np.linalg.eigvalsh(m)))[:2 * n:2]


def refined_min(hk, B, band, nk=60):
    """The smallest value of the eigenvalue number band of hk over the zone, from the best point of a mesh and a local
    minimization, so that it does not depend on the mesh."""
    best = min(pc.kmesh(B, nk), key=lambda k: np.linalg.eigvalsh(hk(k))[band])
    r = minimize(lambda x: np.linalg.eigvalsh(hk(x))[band], best, method='Nelder-Mead',
                 options=dict(xatol=1e-10, fatol=1e-13, maxiter=4000))
    return r.fun


def crossings(E, Y, E0):
    """For bands E[k, n] sorted at each k of a closed loop of momenta, with positions Y, the counts of the crossings of
    the level E0, as (sign of y, sign of the slope)."""
    out = {(1, 1): 0, (1, -1): 0, (-1, 1): 0, (-1, -1): 0}
    for i in range(E.shape[0]):
        j = (i + 1) % E.shape[0]
        for n in range(E.shape[1]):
            a, b = E[i, n] - E0, E[j, n] - E0
            if a * b < 0:
                out[(int(np.sign(Y[i, n] + Y[j, n])), int(np.sign(b - a)))] += 1
    return out


def ci(x):
    """A Chern number for printing, with no minus sign on zero."""
    return '%+d' % int(round(x))


def pf4(A):
    return A[0, 1] * A[2, 3] - A[0, 2] * A[1, 3] + A[0, 3] * A[1, 2]


def main():
    """Runs every check. The pyqula calls write files, so the caller runs this in a temporary folder."""
    from pyqula import geometry, ribbon, topology
    from pyqula import superconductivity as sc
    from pyqula.sctk.pairing import get_triplet
    from pyqula.utilities import get_callable
    pmi = partial(get_triplet, df=get_callable([0.0, 0.0, 1.0]), L=-1)     # p_x - i p_y, no function defined
    t0 = time.time()
    rng = np.random.default_rng(5)
    gch, gsq, gtr = geometry.chain(), geometry.square_lattice(), geometry.triangular_lattice()

    # The Nambu spinor and the BdG Hamiltonian
    g3 = geometry.chain().get_supercell(3); g3.dimensionality = 0
    D3 = 0.3 + 0.2j
    he3 = np.kron(-0.4 * np.eye(3) - (np.eye(3, k=1) + np.eye(3, k=-1)), S0)
    h = g3.get_hamiltonian(tij=[-1.0]); h.add_onsite(-0.4); h.add_swave(D3)
    err = np.abs(dense(h.intra) - bdg_realspace(he3, D3 * np.eye(6))).max()
    h1 = gch.get_hamiltonian(); h1.add_swave(0.2); m1 = dense(h1.intra)
    order = np.allclose(m1[[0, 1], [2, 3]], 0.2) and np.allclose(m1[[0, 1], [3, 2]], 0)
    hs = gch.get_hamiltonian(has_spin=False); s1 = dense(hs.intra).shape; hs.add_swave(0.2)
    hn = gch.get_hamiltonian(has_spin=False); hn.setup_nambu_spinor()
    check('the Nambu spinor of pyqula', err < 1e-14 and order and s1 == (1, 1) and dense(hs.intra).shape == (4, 4)
          and hs.has_spin and dense(hn.intra).shape == (4, 4),
          'add_swave(0.2) on one site puts 0.2 at (0,2) and (1,3) and 0 at (0,3) and (1,2); the open chain of 3 sites with '
          'tij=[-1.], add_onsite(-0.4), add_swave(0.3+0.2j) is (5.7) in real space to %.0e; a chain with has_spin=False goes '
          'from %s to (4, 4) with add_swave or setup_nambu_spinor' % (err, s1))

    gq = geometry.square_lattice().get_supercell(2); gq.dimensionality = 0
    hq = gq.get_hamiltonian(); hq.add_onsite(0.3); hq.add_rashba(0.4); hq.add_exchange([0.2, -0.5, 0.7])
    he = dense(hq.intra).copy()
    Dc = 0.3 * np.exp(0.7j)
    hq.add_swave(Dc)
    M = dense(hq.intra)
    ns = len(gq.r)
    c = fermions(2 * ns); cd = [dag(x) for x in c]
    psi = []
    for i in range(ns):
        psi += [c[2 * i], c[2 * i + 1], cd[2 * i + 1], -cd[2 * i]]
    O = sum(0.5 * dag(psi[a]) @ psi[b] * M[a, b] for a in range(4 * ns) for b in range(4 * ns) if abs(M[a, b]) > 0)
    Hop = sum(cd[i] @ c[j] * he[i, j] for i in range(2 * ns) for j in range(2 * ns) if abs(he[i, j]) > 0)
    Hop = Hop + sum(Dc * cd[2 * i] @ cd[2 * i + 1] + np.conj(Dc) * c[2 * i + 1] @ c[2 * i] for i in range(ns))
    const = 0.5 * np.trace(he).real
    err4 = np.abs(Hop - O - const * np.eye(len(Hop))).max()
    cluster = np.sort(np.linalg.eigvalsh(M))
    KEEP['cluster'] = cluster
    # the chain of 3 sites with an exchange in a general direction, all 64 levels
    J3 = np.array([0.3, 0.2, 0.1])
    c6 = fermions(6)
    Js = J3[0] * SX + J3[1] * SY + J3[2] * SZ
    H6 = 0
    for n in range(3):
        for s in range(2):
            if n < 2:
                H6 = H6 - (dag(c6[2 * n + s]) @ c6[2 * n + 2 + s] + dag(c6[2 * n + 2 + s]) @ c6[2 * n + s])
            H6 = H6 - 0.4 * dag(c6[2 * n + s]) @ c6[2 * n + s]
            for s2 in range(2):
                H6 = H6 + Js[s, s2] * dag(c6[2 * n + s]) @ c6[2 * n + s2]
        P = D3 * dag(c6[2 * n]) @ dag(c6[2 * n + 1])
        H6 = H6 + P + dag(P)
    h = g3.get_hamiltonian(tij=[-1.0]); h.add_onsite(-0.4); h.add_exchange(list(J3)); h.add_swave(D3)
    E3, V3 = np.linalg.eigh(dense(h.intra))
    Ep = E3[6:]
    E0 = 0.5 * np.trace(dense(h.intra)[np.ix_(*[[i for n in range(3) for i in (4 * n, 4 * n + 1)]] * 2)]).real - 0.5 * Ep.sum()
    mb = np.sort([E0 + sum(x) for x in itertools.product(*[(0.0, e) for e in Ep])])
    e6, v6 = np.linalg.eigh(H6)
    err64 = np.abs(np.sort(e6) - mb).max()
    check('the factor one half', err4 < 1e-12 and err64 < 1e-12 and abs(E0 + 4.6646) < 1e-4,
          'H = (1/2) Psi^dag H_BdG Psi + (1/2) Tr h on four sites with hopping, onsite, Rashba, exchange and Delta=0.3 '
          'exp(0.7i), to %.0e in 256 states; the 64 levels of the chain of 3 sites with mu=0.4, Delta=0.3+0.2i and an '
          'exchange (0.3,0.2,0.1) are E0 plus sums of the positive BdG levels to %.0e, E0 = %.4f' % (err4, err64, E0))

    c2 = fermions(2); cd2 = [dag(x) for x in c2]
    vac = np.zeros(4); vac[0] = 1.0
    two = cd2[0] @ cd2[1] @ vac
    one = []
    for Dv in (0.5, -0.5):
        H1 = Dv * cd2[0] @ cd2[1] + Dv * c2[1] @ c2[0]
        w, v = np.linalg.eigh(H1)
        g0 = v[:, 0] * np.sign(np.vdot(vac, v[:, 0]).real)
        one.append((w[0], w[1], np.vdot(two, g0).real / np.vdot(vac, g0).real, np.vdot(g0, c2[1] @ c2[0] @ g0).real))
    exact = np.array([v6[:, 0].conj() @ (c6[2 * n + 1] @ c6[2 * n]) @ v6[:, 0] for n in range(3)])
    neg = E3 < 0
    b31 = np.array([np.sum(V3[4 * n + 2, neg].conj() * V3[4 * n, neg]) for n in range(3)])
    b42 = np.array([np.sum(V3[4 * n + 3, neg].conj() * V3[4 * n + 1, neg]) for n in range(3)])
    hp = g3.get_hamiltonian(tij=[-1.0]); hp.add_onsite(-0.4); hp.add_exchange(list(J3)); hp.add_pairing(mode="swave", delta=D3)
    ok = abs(one[0][0] + 0.5) < 1e-12 and abs(one[0][2] + 1) < 1e-12 and abs(one[0][3] + 0.5) < 1e-12 and abs(one[0][1]) < 1e-12
    ok = ok and abs(one[1][2] - 1) < 1e-12 and abs(one[1][3] - 0.5) < 1e-12 and np.abs(dense(hp.intra) - dense(h.intra)).max() < 1e-14
    ok = ok and np.abs(exact - b31).max() < 1e-12 and np.abs(exact - b42).max() < 1e-12 and abs(np.angle(exact[1] / -D3)) < 1e-9
    check('add_swave and the sign of <c_dn c_up>', ok,
          'one site at mu=0 with Delta=0.5 has the ground state (|0> - c_up^dag c_dn^dag|0>)/sqrt2 at %.2f, the odd states at '
          '%.2f, <c_dn c_up> = %.2f, and Delta=-0.5 gives the plus sign and %+.2f; on the chain the exact <c_dn c_up> of the '
          'middle site is %s, equal to sum over E<0 of phi(3)^* phi(1) and phi(4)^* phi(2), with the phase of -Delta; '
          'add_pairing(mode="swave") is the same matrix' % (one[0][0], one[0][1], one[0][3], one[1][3], np.round(exact[1], 4)))

    k = np.array([0.13, 0.37, 0.0])
    ok = True
    for f in (lambda q: None, lambda q: q.add_onsite(0.4), lambda q: q.add_rashba(0.5)):
        hn = gtr.get_hamiltonian(); f(hn)
        hb = gtr.get_hamiltonian(); f(hb); hb.setup_nambu_spinor()
        ok = ok and np.allclose(hb.get_hk_gen()(k), np.kron(SZ, hn.get_hk_gen()(k)))
    B3 = [0.2, -0.5, 0.7]
    h0 = gtr.get_hamiltonian(); h0.setup_nambu_spinor()
    hb = gtr.get_hamiltonian(); hb.add_exchange(B3); hb.setup_nambu_spinor()
    ok = ok and np.allclose(hb.get_hk_gen()(k) - h0.get_hk_gen()(k), np.kron(S0, B3[0] * SX + B3[1] * SY + B3[2] * SZ))
    hb = gtr.get_hamiltonian(); hb.add_swave(Dc)
    ok = ok and np.allclose(hb.get_hk_gen()(k) - h0.get_hk_gen()(k), np.kron(Dc.real * SX - Dc.imag * SY, S0))
    full = gtr.get_hamiltonian(); full.add_rashba(0.5); full.add_exchange(B3); full.add_onsite(0.4); full.add_swave(Dc)
    norm = gtr.get_hamiltonian(); norm.add_rashba(0.5); norm.add_exchange(B3); norm.add_onsite(0.4)
    ok = ok and np.allclose(full.get_hk_gen()(k)[2:, 2:], -SY @ norm.get_hk_gen()(-k).conj() @ SY)
    hc = gch.get_hamiltonian(); hc.add_onsite(0.7); hc.add_exchange([0.3, 0.2, 0.1]); hc.add_swave(0.25 + 0.1j)
    m = dense(hc.intra)
    Js1 = 0.3 * SX + 0.2 * SY + 0.1 * SZ
    ok = ok and np.allclose(m[:2, :2], 0.7 * S0 + Js1) and np.allclose(m[2:, 2:], -0.7 * S0 + Js1)
    # the order of the notebook of Session 9: onsite, pairing, then a local exchange and a local potential
    hi = g3.get_hamiltonian(); hi.add_onsite(1.8); hi.add_swave(0.2)
    base = dense(hi.intra).copy()
    r0 = g3.r[0]
    hi.add_exchange(lambda r: [0.0, 0.0, 1.1 * (np.sum((r - r0) ** 2) < 1e-2)])
    hi.add_onsite(lambda r: 0.6 * (np.sum((r - r0) ** 2) < 1e-2))
    diff = dense(hi.intra) - base
    loc = np.abs(diff[:4, :4] - (np.kron(S0, 1.1 * SZ) + np.kron(SZ, 0.6 * S0))).max()
    rest = np.abs(diff[4:, :]).max() + np.abs(diff[:4, 4:]).max()
    check('the hole block and the impurities of Session 9', ok and loc < 1e-12 and rest < 1e-14,
          'hopping, onsite and Rashba enter as tau_z h(k), an exchange B.sigma as tau_0 B.sigma, Delta as Re Delta tau_x '
          '- Im Delta tau_y, the hole block is -sigma_y h(-k)^* sigma_y, an onsite 0.7 is -0.7 in the hole block and an '
          'exchange keeps its sign; after add_onsite(1.8) and add_swave(0.2) a local exchange 1.1 and potential 0.6 are '
          'tau_0 1.1 sigma_z and tau_z 0.6 on their site to %.0e, and nothing elsewhere' % loc)

    cu, cdn = c2
    N2 = dag(cu) @ cu + dag(cdn) @ cdn
    pair = dag(cu) @ dag(cdn)
    parity = np.diag((-1.0) ** np.round(np.diag(N2).real))
    rows, ok = [], True
    for mu, D in ((0.0, 0.3), (0.2, 0.3)):
        jc = np.hypot(mu, D)
        for J in (jc - 0.1, jc - 0.01, jc + 0.01, jc + 0.1):
            Hm = -mu * N2 + J * (dag(cu) @ cu - dag(cdn) @ cdn) + D * (pair + dag(pair))
            wm, vm = np.linalg.eigh(Hm)
            par = np.real(vm[:, 0].conj() @ parity @ vm[:, 0])
            one = geometry.chain().get_supercell(1); one.dimensionality = 0
            hp = one.get_hamiltonian(); hp.add_onsite(-mu); hp.add_exchange([0.0, 0.0, J]); hp.add_swave(D)
            lv = np.sort(np.linalg.eigvalsh(dense(hp.intra)))
            ok = ok and np.allclose(lv, np.sort([J + jc, J - jc, -J + jc, -J - jc])) and abs(abs(par) - 1) < 1e-12
            ok = ok and (par > 0) == (J < jc) and abs(wm[0] - (-mu - (jc if J < jc else J))) < 1e-12
            rows.append((mu, J, par, wm[0]))
    check('one site, the limit of the bound state of Section 9.7', ok and abs(rows[0][3] + 0.3) < 1e-12 and abs(rows[3][3] + 0.4) < 1e-12,
          'the BdG levels are +-J +- sqrt(mu^2+Delta^2), and the exact ground state is even below J = sqrt(mu^2+Delta^2) '
          'and odd above it; Delta=0.3 and mu=0 give an even state at %.2f for J=0.2 and an odd one at %.2f for J=0.4, and '
          'mu=0.2 moves the crossing to %.3f' % (rows[0][3], rows[3][3], np.hypot(0.2, 0.3)))

    hph = gsq.get_hamiltonian(); hph.add_rashba(0.3); hph.add_exchange([0.1, 0.2, 0.3]); hph.add_onsite(0.5)
    hph.add_swave(0.2); hph.add_pairing(mode="dx2y2", delta=0.1)
    P4 = np.kron(SY, SY)
    err = 0.0
    for _ in range(5):
        kr = rng.uniform(-0.5, 0.5, 2)
        err = max(err, np.abs(P4 @ hph.get_hk_gen()([kr[0], kr[1], 0]).conj() @ P4 + hph.get_hk_gen()([-kr[0], -kr[1], 0])).max())
    gen = full.get_hk_gen()
    ks3 = [k, np.array([0.41, -0.2, 0.0]), np.array([0.05, 0.77, 0.0])]
    ph = all(np.allclose(P4 @ gen(q).conj() @ P4, -gen(-q)) for q in ks3)
    single = any(not np.allclose(np.sort(np.linalg.eigvalsh(gen(q))), np.sort(-np.linalg.eigvalsh(gen(q)))) for q in ks3)
    check('particle-hole symmetry', err < 1e-13 and ph and single and np.allclose(cluster, -cluster[::-1]),
          'tau_y sigma_y H(k)^* tau_y sigma_y = -H(-k) to %.0e at 5 random k of the square lattice with Rashba, exchange, '
          'onsite, s-wave and d-wave pairing, and at 3 k of the triangular lattice with a complex Delta, where the spectrum '
          'at one k alone is not symmetric; the 16 levels of the cluster of four sites come in pairs +-E' % err)

    flip = np.diag([1, 1, 1, -1]).astype(complex)
    hs1 = gch.get_hamiltonian(); hs1.add_onsite(-1.0); hs1.add_swave(0.3)
    m = hs1.get_hk_gen()([0.11, 0, 0]); m2 = flip @ m @ flip
    hx = gch.get_hamiltonian(); hx.add_exchange([0.4, 0.0, 0.0]); hx.setup_nambu_spinor()
    hz = gch.get_hamiltonian(); hz.add_exchange([0.0, 0.0, 0.4]); hz.setup_nambu_spinor()
    mx, mz = flip @ dense(hx.intra) @ flip, flip @ dense(hz.intra) @ flip
    mix = np.abs(m2[np.ix_([0, 2], [1, 3])]).max()
    ok = np.allclose(m2[:2, 2:], 0.3 * SZ) and np.allclose(m[:2, 2:], 0.3 * S0) and mix < 1e-15
    ok = ok and np.allclose(np.linalg.eigvalsh(m), np.linalg.eigvalsh(m2)) and np.allclose(dense(hx.intra)[2:, 2:], 0.4 * SX)
    ok = ok and np.allclose(mx[2:, 2:], -0.4 * SX) and np.allclose(mz[2:, 2:], 0.4 * SZ)
    KEEP['sign'] = mix
    check('the minus sign of (5.6)', ok,
          'with the sign the pairing block is 0.3 sigma_0, without it 0.3 sigma_z, and the blocks (e_up, h_dn) and '
          '(e_dn, h_up) stay decoupled, coupling %.0f, with Delta and -Delta and the same spectrum; an exchange 0.4 sigma_x '
          'has the hole block +0.4 sigma_x with the sign and -0.4 sigma_x without it, and 0.4 sigma_z keeps its sign' % mix)

    kp = [[x, 0, 0] for x in np.linspace(0, 0.5, 11)]
    ik, e, w = hs1.get_bands(operator='electron', kpath=kp)
    e, w = np.array(e).reshape(11, -1), np.array(w).reshape(11, -1)
    ep = 2 * np.cos(2 * np.pi * np.linspace(0, 0.5, 11)) - 1
    Eq = np.sqrt(ep ** 2 + 0.09)
    werr = max(np.abs(e[:, -1] - Eq).max(), np.abs(w[:, -1] - (1 + ep / Eq) / 2).max())
    h0 = gch.get_hamiltonian(); h0.setup_nambu_spinor()
    kk, eb, cb = h0.get_bands(operator="electron", nk=200)
    cb = np.array(cb)
    zero_one = np.all((np.abs(cb - 1) < 1e-9) | (np.abs(cb) < 1e-9))
    hd = gch.get_hamiltonian(); hd.set_filling(0.2, nk=20); hd.add_swave(0.8)
    es = np.linspace(-5, 5, 1001); de = es[1] - es[0]
    d1 = np.array(hd.get_dos(energies=es, delta=1e-2, nk=1000)[1])
    d2 = np.array(hd.get_dos(energies=es, operator="electron", delta=1e-2, nk=1000)[1])
    d3 = np.array(hd.get_dos(energies=es, operator="hole", delta=1e-2, nk=1000)[1])
    on = dense(hd.intra)[0, 0].real
    kn = 2 * np.pi * (np.arange(4000) + 0.5) / 4000
    eps = 2 * np.cos(kn) + on
    E = np.sqrt(eps ** 2 + 0.64)
    u2 = (1 + eps / E) / 2
    lor = lambda x: 1e-2 / np.pi / (x ** 2 + 1e-4)
    nfull = 2 * (lor(es[:, None] - E[None, :]) + lor(es[:, None] + E[None, :])).mean(1)
    nelec = 2 * (u2 * lor(es[:, None] - E[None, :]) + (1 - u2) * lor(es[:, None] + E[None, :])).mean(1)
    peak = es[np.argmax(d1 * (es > 0))]
    ok = werr < 1e-12 and zero_one and abs(d1.sum() * de - 3.993) < 1e-3 and abs(d2.sum() * de - 1.996) < 1e-3
    ok = ok and np.abs(d1 - d1[::-1]).max() < 1e-10 * d1.max() and np.abs(d2 + d3 - d1).max() < 1e-10 * d1.max()
    ok = ok and abs(peak - 0.81) < 1e-9 and np.abs(nfull - d1).max() < 1e-3 * d1.max() and np.abs(nelec - d2).max() < 1e-3 * d1.max()
    ok = ok and np.abs(d2 - d2[::-1]).max() > 0.5 * d2.max()
    check('the electron weight and the density of states', ok,
          'the electron weight of the upper branch of an s-wave chain is (1 + eps/E)/2 to %.0e, and 0 or 1 with Delta=0; '
          'the cell with set_filling(0.2) and add_swave(0.8), delta=0.01 and nk=1000 gives on (-5,5) the integrals %.3f '
          'for all the states and %.3f for the electron part, electron plus hole is the full one, the full one is '
          'symmetric, its peak is at %.2f, and a numpy sum of Lorentzians gives the same curves' % (werr, d1.sum() * de, d2.sum() * de, peak))

    hk, B = pc.from_pyqula(hs1)
    gg1 = hs1.get_gap()
    ht = gtr.get_supercell((2, 2)).get_hamiltonian(); ht.add_onsite(-4.0); ht.add_pairing(mode="chiral_pwave", delta=0.1)
    hkt, Bt = pc.from_pyqula(ht)
    nb = dense(ht.intra).shape[0]
    gg2, ref2 = ht.get_gap(), 2 * refined_min(hkt, Bt, nb // 2, nk=40)
    check('h.get_gap() of a BdG Hamiltonian', abs(gg1 - 0.6) < 1e-6 and abs(pc.gap(hk, B, 2, nk=300) - 0.6) < 1e-6 and abs(gg2 - ref2) < 2e-3
          and abs(gg2 - 0.5992) < 1e-4 and abs(gg2 / 2 - 0.2996) < 1e-4,
          'the s-wave chain with Delta=0.3 gives %.4f, the distance between the branches, as physcheck.gap with half the '
          'bands filled; the 2x2 triangular cell of Session 9 with add_onsite(-4) and chiral_pwave 0.1 gives %.5f against '
          '%.5f from a minimization, so h.get_gap()/2 = %.4f is the smallest energy' % (gg1, gg2, ref2, gg2 / 2))

    # pyqula, the normal state
    def band(gg, **kw):
        hh = gg.get_hamiltonian(**kw)
        hk, Bq = pc.from_pyqula(hh)
        e = np.linalg.eigvalsh(np.array([hk(q) for q in pc.kmesh(Bq, 60)]))
        return e.min(), e.max(), hk
    lo, hi_, hk = band(gsq)
    eG, eM = np.linalg.eigvalsh(hk(np.zeros(2)))[0], np.linalg.eigvalsh(hk(np.array([np.pi, np.pi])))[0]
    tlo, thi, hkt = band(gtr)
    mlo, mhi, _ = band(gtr, tij=[-1.0])
    e0 = np.linalg.eigvalsh(gch.get_hamiltonian().get_hk_gen()([0.0, 0, 0]))[0]
    cs = []
    for x in (2.0, 1.0, -1.0, -3.0):
        for tij in ([1.0], [-1.0]):
            hh = gsq.get_hamiltonian(tij=tij); hh.add_onsite(x); hh.add_pairing(mode="chiral_pwave", delta=0.25)
            hk2, B2 = pc.from_pyqula(hh)
            cs.append(pc.chern_links(hk2, B2, range(2), nk=24))
    ok = abs(e0 - 2) < 1e-12 and abs(eG - 4) < 1e-12 and abs(eM + 4) < 1e-12 and abs(tlo + 3) < 1e-9 and abs(thi - 6) < 1e-9
    ok = ok and abs(np.linalg.eigvalsh(hkt(np.zeros(2)))[0] - 6) < 1e-9 and abs(mlo + 6) < 1e-9 and abs(mhi - 3) < 1e-9
    ok = ok and np.allclose(cs, [2, 2, 2, 2, -2, -2, -2, -2], atol=1e-9)
    check('the sign of the hopping', ok,
          'the chain has %.0f at k=0, the square lattice %.0f at Gamma and %.0f at M, the triangular lattice runs from %.0f '
          'to %.0f with the top at Gamma, and from %.0f to %.0f with tij=[-1.]; chiral_pwave 0.25 on the square lattice '
          'gives the same C for tij=[1.] and [-1.], %s for add_onsite 2, 1, -1, -3'
          % (e0, eG, eM, tlo, thi, mlo, mhi, ' '.join(ci(x) for x in cs[::2])))

    h1 = gch.get_hamiltonian(); h1.set_filling(0.2, nk=200)
    x = dense(h1.intra)[0, 0].real
    frac = np.mean(2 * np.cos(np.linspace(-np.pi, np.pi, 200001)) + x < 0)
    h2 = gch.get_hamiltonian(); h2.setup_nambu_spinor(); h2.set_filling(0.2, nk=200)
    hb = gtr.get_hamiltonian(); hb.setup_nambu_spinor(); hb.add_onsite(0.4); hb.add_exchange(B3)
    hc2 = gtr.get_hamiltonian(); hc2.add_onsite(0.4); hc2.add_exchange(B3); hc2.setup_nambu_spinor()
    h3 = gch.get_hamiltonian(); h3.add_onsite(0.3)
    h9 = gch.get_hamiltonian(has_spin=False); h9.add_onsite(1.0)                     # the mu = 1. of Session 9
    d9 = float(np.real(h9.get_dos(energies=[0.0], delta=0.005, nk=20000, write=False)[1][0]))
    d9ref = 1 / (np.pi * np.sqrt(4 - 1.0))                                          # mu = -t of the notes, band -2 cos k
    check('add_onsite and set_filling', abs(dense(h3.intra)[0, 0] - 0.3) < 1e-12 and abs(frac - 0.2) < 1e-4 and abs(x - 1.618) < 1e-3
          and np.allclose(np.diag(dense(h2.intra)).real, [x, x, -x, -x]) and np.allclose(hb.get_hk_gen()(k), hc2.get_hk_gen()(k))
          and abs(d9 - 0.1838) < 3e-4 and abs(d9ref - 0.1838) < 1e-4,
          'add_onsite(0.3) adds +0.3 to every electron energy, set_filling(0.2) on the chain adds %.4f and leaves a fraction '
          '%.4f of the band 2 cos k + %.3f below zero, both give the same matrix before or after setup_nambu_spinor, and '
          'add_onsite(1.0) gives D(E_F) = %.4f, the %.4f of mu = -t' % (x, frac, x, d9, d9ref))

    out = []
    for J in (1.0, 2.0):
        hx = gch.get_hamiltonian(); hx.add_exchange([0.0, 0.0, J])
        kk, e, sz = hx.get_bands(operator='sz', kpath=[[0.1, 0, 0]])
        out.append((e[1] - e[0], sz[np.argmax(e)]))
    hz = gtr.get_hamiltonian(); hz.add_zeeman([0.0, 0.0, 0.3])
    hx = gtr.get_hamiltonian(); hx.add_exchange([0.0, 0.0, 0.3])
    KEEP['exchange'] = out[0][1]
    check('add_exchange and add_zeeman', abs(out[0][0] - 2) < 1e-12 and abs(out[1][0] - 4) < 1e-12 and out[0][1] > 0.99
          and np.allclose(hz.get_hk_gen()(k), hx.get_hk_gen()(k)),
          'add_exchange([0,0,J]) is +J (n_up - n_dn), it splits the chain bands by %.0f and %.0f for J=1 and 2, the upper '
          'band has sz=%+.0f, and add_zeeman is the same term' % (out[0][0], out[1][0], out[0][1]))

    # pyqula, the pairing
    ok, vals = True, []
    for mode, sgn in (('dx2y2', -1), ('extended_swave', 1)):
        hp = gsq.get_hamiltonian(); hp.add_pairing(mode=mode, delta=0.1)
        gen = hp.get_hk_gen()
        for kr in ([0.1, 0.3], [0.5, 0.0], [0.27, 0.27], [0.0, 0.0]):
            kc = 2 * np.pi * np.array(kr)
            want = 0.2 * (np.cos(kc[0]) + sgn * np.cos(kc[1]))
            got = gen([kr[0], kr[1], 0.0])
            ok = ok and abs(got[0, 2] - want) < 1e-12 and abs(got[1, 3] - want) < 1e-12
        vals.append(gen([0.5, 0.0, 0.0])[0, 2].real)
    hw = gsq.get_hamiltonian(); hw.add_pairing(mode='swave', delta=0.1)
    check('dx2y2, extended_swave and swave', ok and abs(hw.get_hk_gen()([0.1, 0.3, 0])[0, 2] - 0.1) < 1e-12,
          'delta=0.1 gives 0.2 (cos kx - cos ky) and 0.2 (cos kx + cos ky) at four momenta, so Delta_0 of (5.13) is 2 delta, '
          '%.1f at X for dx2y2, and swave gives delta' % vals[0])

    hp = gsq.get_hamiltonian(); hp.add_pairing(mode='chiral_pwave', delta=0.2)
    hm = gsq.get_hamiltonian(); hm.add_pairing(mode=pmi, delta=0.2)
    ok = True
    for kr in ([0.1, 0.3], [0.25, 0.0], [0.4, -0.15]):
        kc = 2 * np.pi * np.array(kr)
        zp, zm = np.sin(kc[0]) + 1j * np.sin(kc[1]), np.sin(kc[0]) - 1j * np.sin(kc[1])
        a, b = hp.get_hk_gen()([kr[0], kr[1], 0.0]), hm.get_hk_gen()([kr[0], kr[1], 0.0])
        ok = ok and abs(a[0, 2] + 0.4j * zp) < 1e-12 and abs(a[1, 3] - 0.4j * zp) < 1e-12 and abs(a[0, 3]) < 1e-12
        ok = ok and abs(b[0, 2] + 0.4j * zm) < 1e-12 and abs(b[1, 3] - 0.4j * zm) < 1e-12
    cs = []
    for mode in ('chiral_pwave', pmi):
        for d in (0.4, -0.4):
            hh = gtr.get_hamiltonian(); hh.add_onsite(-3.0); hh.add_pairing(mode=mode, delta=d)
            hk2, B2 = pc.from_pyqula(hh)
            cs.append((hh.get_chern(), pc.chern_kubo(hk2, B2, range(2), nk=30)))
    try:
        hr = gtr.get_hamiltonian(); hr.add_pairing(mode='chiral_pwave', delta=0.4, L=-1)
        raised = 'nothing'
    except TypeError:
        raised = 'TypeError'
    ok = ok and raised == 'TypeError' and np.allclose([x[0] for x in cs], [-2, -2, 2, 2], atol=1e-6)
    ok = ok and np.allclose([x[1] for x in cs], [-2, -2, 2, 2], atol=0.01)
    KEEP['pmi'] = cs
    check('chiral_pwave and the other chirality', ok,
          'chiral_pwave 0.2 puts -0.4i (sin kx + i sin ky) at (0,2) and +0.4i (sin kx + i sin ky) at (1,3), L=-1 as a '
          'keyword raises %s, and partial(get_triplet, df=get_callable([0,0,1]), L=-1) puts -0.4i (sin kx - i sin ky) at '
          '(0,2); on the triangular model with add_onsite(-3.0) they give C %s for delta 0.4 and -0.4, with the Kubo form %s'
          % (raised, ' '.join(ci(x[0]) for x in cs), ' '.join('%+.3f' % x[1] for x in cs)))

    ok = True
    for d, amp in (([1.0, 0.0, 0.0], SX), ([0.0, 0.0, 1.0], SZ), ([1.0, 1.0, 0.0], SX + SY)):
        hp = gch.get_hamiltonian(); hp.add_pairing(mode='pwave', delta=0.2, d=d)
        for kr in (0.25, 0.1):
            ok = ok and np.allclose(hp.get_hk_gen()([kr, 0, 0])[:2, 2:], -0.4j * np.sin(2 * np.pi * kr) * amp)
    check('pwave on a chain', ok,
          'the pairing block is -2i delta sin k (d.sigma) for d along x, along z and [1,1,0], so d is not normalized, '
          'd=[1,0,0] pairs up-up and down-down, and the down-down amplitude is delta |d_x + i d_y|, sqrt2 delta for [1,1,0]')

    res = {}
    for mode, dl in (("swave", 0.4), ("nodal_fwave", 0.2)):
        hp = gtr.get_hamiltonian(); hp.add_pairing(mode=mode, delta=dl)
        kd, ed, cd_ = hp.get_bands(operator="electron", kpath=["G", "K", "M", "G"])
        k2, e2, c2_ = hp.get_bands(operator="electron", kpath=["G", "K", "M", "G"], nk=2000)
        hk, Bq = pc.from_pyqula(hp)
        res[mode] = (len(set(np.round(kd, 9))), np.min(np.abs(ed)), np.min(np.abs(e2)), hk, Bq)
    hk, Bq = res["nodal_fwave"][3:]
    hkn, _ = pc.from_pyqula(gtr.get_hamiltonian(has_spin=False))
    third = Bq[0] + Bq[1] if abs(np.linalg.norm(Bq[0] + Bq[1]) - np.linalg.norm(Bq[0])) < 1e-9 else Bq[0] - Bq[1]
    Ms = [Bq[0] / 2, Bq[1] / 2, third / 2]
    alongM = max(abs(hk(s * Mp)[0, 2]) for Mp in Ms for s in np.linspace(0.05, 1, 9))
    Kp = (Bq[0] + third) / 3
    alongK = max(abs(hk(s * Kp)[0, 2]) for s in np.linspace(0.2, 0.7, 6))
    s0 = brentq(lambda s: np.linalg.eigvalsh(hkn(s * Ms[0]))[0], 0.05, 1.0)
    efs = min(np.min(np.abs(np.linalg.eigvalsh(hk(s0 * Mp)))) for Mp in Ms)
    hks = res["swave"][3]
    efs_s = np.min(np.abs(np.linalg.eigvalsh(hks(s0 * Ms[0]))))
    odd = np.allclose(hk(-np.array([0.31, -0.77]))[:2, 2:], -hk(np.array([0.31, -0.77]))[:2, 2:])
    ok = alongM < 1e-12 and alongK > 1.4 and abs(s0 - 2 / 3) < 1e-9 and efs < 1e-12 and odd and abs(efs_s - 0.4) < 1e-12
    ok = ok and res["nodal_fwave"][0] == 546 and abs(res["nodal_fwave"][1] - 0.0182) < 1e-4 and abs(res["nodal_fwave"][2] - 0.0036) < 1e-4
    ok = ok and abs(res["swave"][1] - 0.4004) < 1e-4 and abs(res["swave"][2] - 0.4) < 1e-4
    check('nodal_fwave', ok,
          'odd in k, zero on the three lines Gamma-M (largest entry %.0e) and up to %.2f on Gamma-K; at mu=0 the Fermi '
          'surface crosses Gamma-M at %.4f of the way to M, where |E| is %.0e; on the path G K M G the smallest |E| is '
          '%.4f with the default %d steps and %.4f with nk=2000, and swave 0.4 gives %.4f and %.4f there, 0.4 on the '
          'Fermi surface' % (alongM, alongK, s0, efs, res["nodal_fwave"][1], res["nodal_fwave"][0], res["nodal_fwave"][2],
                             res["swave"][1], res["swave"][2]))

    # The gap
    out, ok = [], True
    for Dv in (0.8, 0.4, 0.2):
        hh = gsq.get_hamiltonian(); hh.set_filling(0.2, nk=20); hh.setup_nambu_spinor(); hh.add_swave(Dv)
        kk, e, w = hh.get_bands(operator='electron', nk=800)
        out.append(np.abs(e).min())
        ok = ok and abs(out[-1] - Dv) < 1e-4
    mus = []
    for mu in (-1.2, 0.0, 1.2):
        hm = gch.get_hamiltonian(); hm.add_onsite(-mu); hm.add_swave(0.3)
        hk, Bc = pc.from_pyqula(hm)
        mus.append(refined_min(hk, Bc, 2, nk=200))
    tri, hon = [], []
    for x in (-4.0, 0.0, 2.0):
        hh = gtr.get_hamiltonian(); hh.add_onsite(x); hh.add_swave(0.3)
        hk, Bq = pc.from_pyqula(hh)
        tri.append(refined_min(hk, Bq, 2, nk=40))
    for x in np.linspace(-1.0, 2.5, 6):
        hh = geometry.honeycomb_lattice().get_hamiltonian(); hh.add_onsite(x); hh.add_swave(0.5)
        hk, Bq = pc.from_pyqula(hh)
        hon.append(refined_min(hk, Bq, 4, nk=40))
    hm = gch.get_hamiltonian(); hm.add_onsite(-2.5); hm.add_swave(0.3)
    hk, Bc = pc.from_pyqula(hm)
    outside = refined_min(hk, Bc, 2, nk=200)
    hk, Bc = pc.from_pyqula(hs1)
    twice = pc.gap(hk, Bc, 2, nk=3000)
    ok = ok and np.allclose(mus, 0.3, atol=1e-7) and np.allclose(tri, 0.3, atol=1e-7) and np.allclose(hon, 0.5, atol=1e-7)
    ok = ok and abs(outside - np.hypot(0.5, 0.3)) < 1e-7 and abs(twice - 0.6) < 1e-5
    KEEP['gap'] = (out, twice)
    check('the smallest energy is |Delta| for s-wave pairing', ok,
          'set_filling(0.2) on the square lattice with add_swave 0.8, 0.4, 0.2 gives %.4f, %.4f, %.4f on the path of '
          'the notebook; the chain with Delta=0.3 gives %.4f for mu = -1.2, 0, 1.2, the triangular lattice with Delta=0.3 '
          '%.4f for add_onsite -4, 0, 2, the honeycomb lattice with Delta=0.5 %.4f for add_onsite -1 to 2.5, all from a '
          'minimization; outside the band, mu=2.5 on the chain, %.4f = sqrt(0.5^2+0.3^2); physcheck.gap with half the '
          'bands filled gives %.4f = 2|Delta|' % (out[0], out[1], out[2], mus[0], tri[0], hon[0], outside, twice))

    # The mean field
    kb = 2 * np.pi * (np.arange(4000) + 0.5) / 4000

    def bcs(U):
        def number(Dv):
            f = lambda mu: np.mean(1 - (2 * np.cos(kb) - mu) / np.sqrt((2 * np.cos(kb) - mu) ** 2 + Dv ** 2)) - 0.2
            return brentq(f, -12, 12)

        def gap_eq(Dv):
            mu = number(Dv)
            return abs(U) * np.mean(1 / (2 * np.sqrt((2 * np.cos(kb) - mu) ** 2 + Dv ** 2))) - 1
        return brentq(gap_eq, 1e-4, 5)
    out = []
    for U in (-1.0, -1.5, -2.0):
        hu = gch.get_hamiltonian(); hu.setup_nambu_spinor()
        hsc = hu.get_mean_field_hamiltonian(U=U, filling=0.1, nk=100, mix=0.5, mf='swave')
        Dv = dense(hsc.intra)[0, 2]
        gen = hsc.get_hk_gen()
        anom, dens, emin = 0, 0, 1e9
        for xk in np.arange(400) / 400:
            e, v = np.linalg.eigh(gen([xk, 0, 0]))
            occ = v[:, e < 0]
            anom += np.sum(np.conj(occ[2]) * occ[0]) / 400
            dens += np.sum(np.abs(occ[0]) ** 2 + np.abs(occ[1]) ** 2) / 400
            emin = min(emin, np.abs(e).min())
        out.append((U, Dv, U * anom, bcs(U), dens, emin))
    np.random.seed(7)
    hu = gch.get_hamiltonian(); hu.setup_nambu_spinor()
    again = dense(hu.get_mean_field_hamiltonian(U=-1.0, filling=0.1, nk=100, mix=0.5, mf='swave').intra)[0, 2]
    ok = all(abs(o[1] - o[2]) < 1e-4 and abs(abs(o[1]) - o[3]) < 2e-4 and abs(o[4] - 0.2) < 2e-3 and abs(o[5] - abs(o[1])) < 1e-4
             and abs(o[1].imag) < 1e-9 for o in out) and abs(again - out[0][1]) < 1e-6
    ok = ok and np.allclose([o[1].real for o in out], [0.1031, 0.2226, 0.3606], atol=1e-4)
    KEEP['mf'] = [o[1].real for o in out]
    check('the s-wave mean field', ok,
          'mf="swave" at filling 0.1, which is %.4f electrons per site, gives the real Delta %s for U = -1, -1.5, -2, '
          'equal to U<c_dn c_up> (%s) and to the BCS gap equation solved with numpy (%s), the smallest |E| is |Delta|, '
          'and a run with another random seed gives the same' % (out[0][4], ' '.join('%.4f' % o[1].real for o in out),
                                                                 ' '.join('%.4f' % o[2].real for o in out), ' '.join('%.4f' % o[3] for o in out)))

    out = []
    for seed in range(4):
        np.random.seed(seed)
        hv = gtr.get_hamiltonian(); hv.add_exchange([0.0, 0.0, -2.0]); hv.setup_nambu_spinor()
        hsc = hv.get_mean_field_hamiltonian(V1=-1.0, filling=0.3, mix=0.3, mf='random')
        hk, Bt = pc.from_pyqula(hsc)
        kinds = sc.identify_superconductivity(hsc)
        upup = 'up-up pairing' in kinds and 'down-down pairing' not in kinds and 'up-down pairing' not in kinds
        out.append((hsc.get_chern(nk=40), pc.chern_links(hk, Bt, range(2), nk=24), pc.gap(hk, Bt, 2, nk=48),
                    pc.gap(hk, Bt, 2, nk=60), 2 * refined_min(hk, Bt, 2, nk=60), upup))
    ok = all(abs(abs(o[0]) - 1) < 1e-6 and abs(o[1] - o[0]) < 1e-6 and o[5] and abs(o[4] - 0.3728) < 5e-4
             and abs(o[2] - 0.3761) < 5e-4 and abs(o[3] - 0.3748) < 5e-4 for o in out)
    check('the interaction-driven triplet of the notebook', ok,
          'V1=-1, the exchange [0,0,-2], filling 0.3, mix 0.3 and mf="random" give only up-up triplet pairing and |C|=1 on '
          'four random starts, with the signs %s; the branches are %.4f apart from a minimization, while a mesh of 48 and of '
          '60 gives %.4f and %.4f' % (' '.join(ci(o[0]) for o in out), np.mean([o[4] for o in out]),
                                       np.mean([o[2] for o in out]), np.mean([o[3] for o in out])))

    # The Chern number of the BdG bands
    hcp = gtr.get_hamiltonian(); hcp.add_onsite(-3.0); hcp.add_pairing(mode='chiral_pwave', delta=0.4)
    hk, Bt = pc.from_pyqula(hcp)
    c1, c2_ = hcp.get_chern(), pc.chern_links(hk, Bt, range(2), nk=30)
    check('h.get_chern() of a BdG Hamiltonian', abs(c1 + 2) < 1e-6 and abs(c2_ + 2) < 1e-9,
          'the chiral p-wave of the notebook gives %+.4f, and physcheck.chern_links on the two BdG bands below zero %+.4f, '
          'with no factor one half' % (c1, c2_))

    B2 = 2 * np.pi * np.eye(2)
    out = {}
    for mu in (-3.5, -2.0, -1.0, 1.0, 3.0, 5.0):
        for chir in (1, -1):
            blk = lambda kk, mu=mu, chir=chir: np.array(
                [[-2 * (np.cos(kk[0]) + np.cos(kk[1])) - mu, 0.5 * (np.sin(kk[0]) + 1j * chir * np.sin(kk[1]))],
                 [0.5 * (np.sin(kk[0]) - 1j * chir * np.sin(kk[1])), 2 * (np.cos(kk[0]) + np.cos(kk[1])) + mu]])
            out[(mu, chir)] = (pc.chern_links(blk, B2, 0, nk=36), pc.chern_kubo(blk, B2, 0, nk=36))
    want = {-3.5: 1, -2.0: 1, -1.0: 1, 1.0: -1, 3.0: -1, 5.0: 0}
    ok = all(abs(out[(mu, ch)][0] - ch * want[mu]) < 1e-9 and abs(out[(mu, ch)][1] - ch * want[mu]) < 0.02 for mu in want for ch in (1, -1))
    check('the Chern number of one block with p+ip', ok,
          'the block (5.8) with Delta_0 = 0.5 (sin kx + i sin ky) and t=1 has C %s for mu = -3.5, -2, -1, 1, 3, 5, by '
          'the links and by the Kubo form, and the opposite for sin kx - i sin ky' % ' '.join(ci(out[(mu, 1)][0]) for mu in want))

    out = []
    for mu in (-2.0, -1.0, 1.0, -5.0):
        hh = gsq.get_hamiltonian(tij=[-1.0]); hh.add_onsite(-mu); hh.add_pairing(mode="chiral_pwave", delta=0.25)
        hk, Bq = pc.from_pyqula(hh)
        out.append((hh.get_chern(), pc.chern_links(hk, Bq, range(2), nk=36)))
    tri = []
    for name, dl in (("swave", 1.0), ("chiral_pwave", 0.4), ("chiral_pwave", 0.8)):
        hh = gtr.get_hamiltonian(); hh.add_onsite(-3.0); hh.add_pairing(mode=name, delta=dl)
        hk, Bq = pc.from_pyqula(hh)
        tri.append((hh.get_chern(), pc.chern_links(hk, Bq, range(2), nk=36)))
    eGt = np.linalg.eigvalsh(gtr.get_hamiltonian(has_spin=False).get_hk_gen()([0, 0, 0]))[0] - 3.0
    hh = gtr.get_hamiltonian(tij=[-1.0]); hh.add_onsite(3.0); hh.add_pairing(mode="chiral_pwave", delta=0.4)
    hk, Bq = pc.from_pyqula(hh)
    fl = (hh.get_chern(), pc.chern_links(hk, Bq, range(2), nk=36))
    ok = np.allclose([o[0] for o in out], [2, 2, -2, 0], atol=1e-6) and np.allclose([o[1] for o in out], [2, 2, -2, 0], atol=1e-9)
    ok = ok and np.allclose([o[0] for o in tri], [0, -2, -2], atol=1e-6) and np.allclose([o[1] for o in tri], [0, -2, -2], atol=1e-9)
    ok = ok and abs(eGt - 3) < 1e-9 and abs(fl[0] - 2) < 1e-6 and abs(fl[1] - 2) < 1e-9
    KEEP['side'] = (out, tri, fl)
    check('chiral_pwave of pyqula and the side of the Fermi surface', ok,
          'chiral_pwave 0.25 on the square lattice with tij=[-1.] and add_onsite(-mu) gives C %s for mu = -2, -1, 1, -5; '
          'the triangular model with add_onsite(-3.0) has eps(Gamma) = %+.0f, a pocket of empty states, and gives %s for '
          'swave 1.0 and chiral_pwave 0.4 and 0.8; tij=[-1.] with add_onsite(3.0) gives %+.0f with chiral_pwave 0.4, '
          'get_chern and the links agree' % (' '.join(ci(o[0]) for o in out), eGt, ' '.join(ci(o[0]) for o in tri), fl[0]))

    gr = ribbon.bulk2ribbon(gtr, n=20)
    nk = 200
    kpath = [[x, 0.0, 0.0] for x in np.linspace(-0.5, 0.5, nk, endpoint=False)]
    found = {}
    for name, mode in (("p+ip", "chiral_pwave"), ("p-ip", pmi)):
        hr = gr.get_hamiltonian(); hr.add_onsite(-3.0); hr.add_pairing(mode=mode, delta=0.4)
        ik, e, y = hr.get_bands(operator='yposition', kpath=kpath)
        Er, Yr = np.array(e).reshape(nk, -1), np.array(y).reshape(nk, -1)
        found[name] = [crossings(Er, Yr, E0) for E0 in (0.1, 0.3, 0.5, -0.5)]
    hs2 = gr.get_hamiltonian(); hs2.add_onsite(-3.0); hs2.add_swave(1.0)
    smin = np.abs(hs2.get_bands(operator='yposition', kpath=kpath)[1]).min()
    bulk = refined_min(*pc.from_pyqula(hcp), 2, nk=60)
    down = {(1, 1): 0, (1, -1): 2, (-1, 1): 2, (-1, -1): 0}
    up = {(1, 1): 2, (1, -1): 0, (-1, 1): 0, (-1, -1): 2}
    ok = all(f == down for f in found["p+ip"]) and all(f == up for f in found["p-ip"]) and abs(smin - 1.0) < 1e-3
    ok = ok and abs(bulk - 1.336) < 2e-3
    check('the edge branches of the ribbon', ok,
          'bulk2ribbon(n=20) of the notebook model, whose bulk has the smallest energy %.3f, has at E = 0.1, 0.3, 0.5 and '
          '-0.5 two branches going down with k at the edge of positive y and two going up at the other edge, p_x - i p_y '
          'reverses all of them, and the s-wave ribbon keeps the smallest |E| %.4f' % (bulk, smin))

    r = np.hypot(0.3, 0.3)
    rows, ok = [], True
    for J in np.linspace(0.0, 0.6, 9):
        hJ = gtr.get_hamiltonian(); hJ.add_onsite(-5.7); hJ.add_rashba(1.0); hJ.add_zeeman([0.0, 0.0, J]); hJ.add_swave(0.3)
        kk, e, w = hJ.get_bands(nk=1000, operator='sx', kpath=['M1', 'G', 'M1'])
        eG = np.sort(np.linalg.eigvalsh(hJ.get_hk_gen()([0.0, 0.0, 0.0])))
        ok = ok and np.allclose(eG, np.sort([J + r, J - r, -J + r, -J - r]), atol=1e-9)
        cJ = np.nan
        if round(J, 3) in (0.3, 0.375, 0.525, 0.6):
            hk, Bt = pc.from_pyqula(hJ)
            cJ = pc.chern_links(hk, Bt, range(2), nk=40)
        rows.append((J, np.abs(e).min(), cJ, np.abs(eG).min()))
    hn = gtr.get_hamiltonian(has_spin=False); hn.add_onsite(-5.7)
    epsG = np.linalg.eigvalsh(hn.get_hk_gen()([0, 0, 0]))[0]
    mins = [x[1] for x in rows]
    ok = ok and abs(epsG - 0.3) < 1e-12 and abs(mins[0] - 0.3) < 1e-3 and all(np.diff(mins[:7]) < 0) and all(np.diff(mins[6:]) > 0)
    ok = ok and np.allclose([rows[i][2] for i in (4, 5, 7, 8)], [0, 0, 1, 1], atol=1e-9)
    ok = ok and all(x[1] < x[3] - 0.01 for x in rows[:3]) and all(abs(x[1] - x[3]) < 1e-3 for x in rows[3:])
    check('the exchange-driven transition of Section 5.18', ok,
          'with add_onsite(-5.7), add_rashba(1.0) and add_swave(0.3) the band is at %.1f at Gamma, the levels at Gamma are '
          '+-J +- %.4f and close at J=%.4f; on the 9 values of J of the cell the smallest |E| on M1 G M1 is %s, and C is '
          '0 at J=0.3 and 0.375 and +1 at J=0.525 and 0.6; it sits on the Fermi pocket up to J=0.15 and at Gamma from '
          'J=0.225 on, where the level at Gamma starts at %.3f for J=0' % (epsG, r, r, ' '.join('%.3f' % x for x in mins), rows[0][3]))

    out = []
    for Z in (-0.6, 0.6):
        hz = gtr.get_hamiltonian(); hz.add_rashba(1.0); hz.add_onsite(2.0); hz.add_zeeman([0.0, 0.0, Z]); hz.add_swave(0.3)
        hk, Bt = pc.from_pyqula(hz)
        out.append((hz.get_chern(nk=60), pc.chern_kubo(hk, Bt, range(2), nk=72), refined_min(hk, Bt, 2, nk=60)))
    check('the artificial topological superconductor of the notebook', abs(out[0][0] - 3) < 1e-6 and abs(out[1][0] + 3) < 1e-6
          and abs(out[0][1] - 3) < 0.01 and abs(out[1][1] + 3) < 0.01 and abs(out[0][2] - out[1][2]) < 1e-4 and abs(out[0][2] - 0.2101) < 1e-4,
          'Rashba 1, add_onsite(2.0), the Zeeman field -0.6 and +0.6 and Delta=0.3 give C %+.0f and %+.0f, with the Kubo '
          'form %+.3f and %+.3f, and the smallest energy %.4f from a minimization' % (out[0][0], out[1][0], out[0][1], out[1][1], out[0][2]))

    # The Kitaev chain
    c1m = fermions(1)[0]
    gA, gB = c1m + dag(c1m), -1j * (c1m - dag(c1m))
    empty = np.array([1.0, 0.0])
    ok = np.allclose(gA, dag(gA)) and np.allclose(gB, dag(gB)) and np.allclose(gA @ gA, np.eye(2)) and np.allclose(gB @ gB, np.eye(2))
    ok = ok and np.allclose(gA @ gB + gB @ gA, 0) and np.allclose(1j * gA @ gB, 2 * dag(c1m) @ c1m - np.eye(2))
    ok = ok and np.allclose((gA + 1j * gB) / 2, c1m) and np.allclose(gA @ gB @ empty, 1j * empty) and np.allclose(gB @ gA @ empty, -1j * empty)
    val = (empty @ (1j * gA @ gB) @ empty).real
    check('the Majorana operators (5.17)', ok and abs(val + 1) < 1e-12,
          'gamma^2 = 1, {gamma_A, gamma_B} = 0, i gamma_A gamma_B = 2 c^dag c - 1, which is %+.0f on the empty mode, '
          'gamma_A gamma_B |0> = i|0>, gamma_B gamma_A |0> = -i|0>, and c = (gamma_A + i gamma_B)/2' % val)

    c4 = fermions(4)
    gam = []
    for n in range(4):
        gam += [c4[n] + dag(c4[n]), -1j * (c4[n] - dag(c4[n]))]
    Hs = kitaev_op(c4, 1.0, 0.0, 1.0)
    maj = 1j * sum(gam[2 * n + 1] @ gam[2 * n + 2] for n in range(3))
    free = all(np.allclose(Hs @ gam[j], gam[j] @ Hs) for j in (0, 7))
    Hm = kitaev_op(c4, 1.0, 0.0, -1.0)
    majm = -1j * sum(gam[2 * n] @ gam[2 * n + 3] for n in range(3))
    freem = all(np.allclose(Hm @ gam[j], gam[j] @ Hm) for j in (1, 6))
    Hn = kitaev_op(c4, -1.0, 0.0, -1.0)
    check('(5.21)', np.allclose(Hs, maj) and free and np.allclose(Hm, majm) and freem and np.allclose(Hn, -maj),
          'at Delta=t=1 and mu=0 the operator (5.19) on four sites is i t sum gamma_2n gamma_2n+1 exactly, with c_n = '
          '(gamma_2n-1 + i gamma_2n)/2, and gamma_1 and gamma_8 commute with it; t=Delta=-1 gives (5.21) with t=-1, and '
          'Delta=-t gives -i t sum gamma_2n-1 gamma_2n+2 with gamma_2 and gamma_7 free')

    worst = 0.0
    for mu, Dv in ((0.0, 1.0), (0.7, 0.5), (2.5, 0.5), (-1.3, 0.8)):
        Hk = kitaev_op(c4, 1.0, mu, Dv)
        Mk = kitaev(4, 1.0, mu, Dv)
        Ep = np.sort(np.linalg.eigvalsh(Mk))[4:]
        mb = np.sort([-4 * mu / 2 - 0.5 * Ep.sum() + sum(x) for x in itertools.product(*[(0.0, e) for e in Ep])])
        worst = max(worst, np.abs(np.sort(np.linalg.eigvalsh(Hk)) - mb).max())
    Nr = 8
    F = np.exp(1j * np.outer(np.arange(Nr), 2 * np.pi * np.arange(Nr) / Nr)) / np.sqrt(Nr)
    W = np.block([[F, np.zeros((Nr, Nr))], [np.zeros((Nr, Nr)), F]])
    Mk = dag(W) @ kitaev(Nr, 1.0, 0.3, 0.7, ring=True) @ W
    ks8 = 2 * np.pi * np.arange(Nr) / Nr
    entry = np.array([Mk[j, Nr + j] for j in range(Nr)])
    kr = np.linspace(-np.pi, np.pi, 4001)
    wind, zak = [], []
    for sgn in (-1, 1):
        for mu in (1.0, 3.0):
            eps = -2 * np.cos(kr) - mu
            dk = sgn * 2j * 0.5 * np.sin(kr)
            wind.append(np.sum(np.diff(np.unwrap(np.angle(eps - 1j * dk.imag)))) / (2 * np.pi))
            hk = lambda q, sgn=sgn, mu=mu: np.array([[-2 * np.cos(q) - mu, sgn * 1j * np.sin(q)], [-sgn * 1j * np.sin(q), 2 * np.cos(q) + mu]])
            zak.append(abs(pc.zak_phase(hk, 2 * np.pi, 0, nk=200)))
    ok = worst < 1e-12 and np.allclose(entry, -2j * 0.7 * np.sin(ks8)) and np.allclose([Mk[j, j] for j in range(Nr)], -2 * np.cos(ks8) - 0.3)
    ok = ok and np.allclose(wind, [-1, 0, 1, 0], atol=1e-6) and np.allclose(zak, [np.pi, 0, np.pi, 0], atol=1e-9)
    KEEP['520'] = (entry[2], wind)
    check('the BdG matrix of (5.19) and the sign of (5.20)', ok,
          'the matrix with d[n+1,n] = Delta gives the 16 many-body levels of four sites to %.0e at four (mu, Delta); with '
          'the Fourier transform (2.7) the entry above the diagonal is -2i Delta sin k, %.4fi at k=pi/2 for Delta=0.7, '
          'with -2t cos k - mu on the diagonal; with -2i Delta sin k and with the +2i Delta sin k of (5.20) the Zak phase '
          'is %.4f and %.4f at mu=t, 0 at mu=3t, and the signed winding of (eps, Im Delta(k)) is %+.0f and %+.0f'
          % (worst, entry[2].imag, zak[0], zak[2], wind[0], wind[2]))

    flat = [np.linalg.eigvalsh(np.array([[-2 * np.cos(q), -2j * np.sin(q)], [2j * np.sin(q), 2 * np.cos(q)]]))[1] for q in np.linspace(-np.pi, np.pi, 13)]
    out = []
    for L in (5, 12, 31):
        gg = geometry.chain().get_supercell(L); gg.dimensionality = 0
        hh = gg.get_hamiltonian(); hh.add_onsite(4.0); hh.add_exchange([0.0, 0.0, 4.0])
        hh.add_pairing(mode='pwave', delta=1.0, d=[1.0, 0.0, 0.0])
        lv = np.sort(np.abs(hh.get_bands()[1]))
        out.append((lv[1], lv[2]))
    check('the flat band and the sweet spot in pyqula', np.allclose(flat, 2.0) and all(o[0] < 2e-15 and abs(o[1] - 2) < 1e-12 for o in out),
          'at Delta=t=1 and mu=0 the bulk energy is %.4f at 13 momenta; in pyqula add_onsite(4.0), add_exchange([0,0,4]) '
          'and pwave delta=1 with d=[1,0,0] give the two lowest |E| below %.0e for 5, 12 and 31 sites and the next at 2t'
          % (flat[0], max(o[0] for o in out)))

    out = []
    for (mu, Dv) in ((1.0, 0.5), (0.5, 0.3), (1.9, 0.5), (1.0, 1.0)):
        rmin = minimize_scalar(lambda q: np.sqrt((-2 * np.cos(q) - mu) ** 2 + 4 * Dv ** 2 * np.sin(q) ** 2), bounds=(0, np.pi),
                               method='bounded', options=dict(xatol=1e-12)).fun
        num = min(rmin, abs(2 - mu), abs(2 + mu))
        form = Dv * np.sqrt(4 - mu ** 2 / (1 - Dv ** 2)) if Dv < 1 and abs(mu) <= 2 * (1 - Dv ** 2) else abs(2 - abs(mu))
        out.append((num, form))
    big = qp(majorana(200, 1.0, 1.0, 0.5))[1]
    ok = all(abs(a - b) < 1e-8 for a, b in out) and np.allclose([o[0] for o in out], [0.8165, 0.5790, 0.1, 1.0], atol=1e-4)
    ok = ok and abs(big - 0.8167) < 1e-4
    KEEP['bulk'] = out[0][0]
    check('the bulk minimum of the Kitaev chain', ok,
          'Delta sqrt(4 - mu^2/(t^2-Delta^2)) when Delta<t and |mu| t <= 2(t^2-Delta^2), and |2t - |mu|| otherwise, is '
          '%.4f, %.4f, %.4f, %.4f for (mu, Delta) = (t, 0.5t), (0.5t, 0.3t), (1.9t, 0.5t), (t, t), as a minimization over k '
          'gives; the branches are %.3f apart for (t, 0.5t), and the open chain of 200 sites has its first bulk level at %.4f'
          % (out[0][0], out[1][0], out[2][0], out[3][0], 2 * out[0][0], big))

    out, signs = [], []
    for mu in (0.0, 1.0, 1.5, 2.5, 3.0):
        hb = gch.get_hamiltonian(); hb.add_onsite(4.0); hb.add_exchange([0.0, 0.0, 4.0]); hb.add_onsite(-mu)
        hb.add_pairing(mode='pwave', delta=0.3, d=[1.0, 0.0, 0.0])
        hk, G = pc.from_pyqula(hb)
        z2 = np.sign((-2 - mu) * (2 - mu))
        out.append((mu, z2, topology.berry_phase(hb, nk=200), pc.zak_phase(hk, G, range(2), nk=200), lowest(kitaev(60, 1.0, mu, 0.7))[0]))
        if mu < 2:
            for nkk in (50, 100, 201):
                signs.append(np.sign(topology.berry_phase(hb, nk=nkk)))
    e19 = [refined_min(lambda q, m=m: np.array([[-2 * np.cos(q[0]) - m, -1j * np.sin(q[0])], [1j * np.sin(q[0]), 2 * np.cos(q[0]) + m]]),
                       2 * np.pi * np.eye(2), 1, nk=50) for m in (1.9, 2.1)]
    ok = all((abs(abs(o[2]) - np.pi) < 1e-6 and abs(o[3] - np.pi) < 1e-6 and o[1] < 0 and o[4] < 1e-3) if o[0] < 2 else
             (abs(o[2]) < 1e-6 and abs(o[3]) < 1e-6 and o[1] > 0 and o[4] > 0.05) for o in out)
    ok = ok and abs(out[3][4] - 0.507) < 1e-3 and abs(out[4][4] - 1.005) < 1e-3 and np.allclose(e19, 0.1, atol=1e-6)
    check('the topological range (5.22)', ok,
          'for mu = 0, t, 1.5t the sign of eps(0) eps(pi) is -1, the Zak phase of the BdG bands is pi with physcheck and '
          'with topology.berry_phase, which returns +pi in %d and -pi in %d of %d runs, and the open chain of 60 sites with '
          'Delta=0.7t has a level below 1e-3; mu = 2.5t and 3t give +1, 0 and the lowest levels %.3f and %.3f; with '
          'Delta=0.5t the smallest energy is %.4f at mu=1.9t and %.4f at 2.1t'
          % (sum(s > 0 for s in signs), sum(s < 0 for s in signs), len(signs), out[3][4], out[4][4], e19[0], e19[1]))

    A = majorana(300, 1.0, 1.9, 0.5)
    w, v = np.linalg.eigh(1j * A)
    a = v[0::2, np.argmin(np.abs(w))]
    ratio = (a[41] / a[40]).real
    roots = np.roots([1.5, 1.9, 0.5])
    lam = roots[np.argmax(np.abs(roots))].real
    Ns = np.arange(8, 61)
    E0s = np.array([qp(majorana(N, 1.0, 1.0, 0.5))[0] for N in Ns])
    slope = np.polyfit(Ns, np.log(E0s), 1)[0]
    r09 = qp(majorana(21, 1.0, 1.0, 0.9))[0] / qp(majorana(20, 1.0, 1.0, 0.9))[0]
    root09 = np.max(np.abs(np.roots([1.9, 1.0, 0.1])))
    s19 = (qp(majorana(100, 1.0, 1.9, 0.5))[0] / qp(majorana(60, 1.0, 1.9, 0.5))[0]) ** (1 / 40)
    l8, l20, l40 = (qp(majorana(N, 1.0, 1.0, 0.5)) for N in (8, 20, 40))
    triv = qp(majorana(40, 1.0, 2.5, 0.5))[0]
    ok = abs(ratio - lam) < 1e-4 and abs(lam + 0.8937) < 1e-4 and abs(slope - np.log(np.sqrt(0.5 / 1.5))) < 0.01
    ok = ok and abs(r09 - root09) < 1e-3 and abs(root09 - 0.3921) < 1e-4 and abs(s19 - 0.8937) < 1e-4
    ok = ok and abs(l8[0] - 0.0111) < 5e-5 and abs(l20[0] - 1.94e-5) < 1e-7 and abs(l40[0] - 3.49e-10) < 1e-12
    ok = ok and abs(l8[1] - 0.8933) < 1e-4 and abs(l20[1] - 0.8347) < 1e-4 and abs(triv - 0.511) < 1e-3
    check('the splitting of the end modes', ok,
          'the zero mode at the left end has a_n+1/a_n = %.4f for mu=1.9t and Delta=0.5t, the root of larger modulus of '
          '(t+Delta) l^2 + mu l + (t-Delta) = 0; for Delta=0.5t and mu=t the roots are complex, the splitting is %.4f, '
          '%.2e and %.2e for N = 8, 20, 40, its envelope goes as exp(%.3f N) against log sqrt((t-Delta)/(t+Delta)) = %.3f, '
          'and the first bulk level is %.4f and %.4f at N = 8 and 20; Delta=0.9t gives the ratio %.4f per site and mu=1.9t '
          '%.4f, the larger real roots; the trivial chain of 40 sites at mu=2.5t has its lowest level at %.4f'
          % (ratio, l8[0], l20[0], l40[0], slope, np.log(np.sqrt(0.5 / 1.5)), l8[1], l20[1], r09, s19, triv))

    worst, nb = 0.0, {}
    for (L, m, Dv, d) in ((8, -1.0, 0.5, [1, 0, 0]), (20, -1.0, 0.5, [1, 0, 0]), (30, 0.7, 0.3, [1, 0, 0]),
                          (40, 0.3, 0.1, [1, 1, 0]), (40, 1.0, 0.1, [1, 1, 0]), (40, 2.5, 0.1, [1, 1, 0]), (30, 0.3, 0.1, [1, 1, 0])):
        gg = geometry.chain().get_supercell(L); gg.dimensionality = 0
        hh = gg.get_hamiltonian(); hh.add_onsite(4.0); hh.add_exchange([0.0, 0.0, 4.0]); hh.add_onsite(m)
        hh.add_pairing(mode='pwave', delta=Dv, d=d)
        e = np.array(hh.get_bands()[1])
        De = Dv * abs(d[0] + 1j * d[1])
        low = np.sort(np.abs(e))[:2 * L:2]
        worst = max(worst, np.abs(low - qp(majorana(L, 1.0, -m, De))).max())
        nb[(L, m)] = low[0]
    hf = gch.get_hamiltonian(); hf.add_onsite(4.0); hf.add_exchange([0.0, 0.0, 4.0]); hf.add_onsite(-1.0)
    hf.add_pairing(mode='pwave', delta=0.5, d=[1.0, 0.0, 0.0])
    fin = np.sort(np.abs(hf.set_finite_system(n=8).get_bands()[1]))[0]
    ok = worst < 1e-10 and abs(fin - nb[(8, -1.0)]) < 1e-10 and abs(nb[(40, 0.3)] - 1.65e-3) < 1e-5 and abs(nb[(40, 1.0)] - 1.39e-3) < 1e-5
    ok = ok and abs(nb[(40, 2.5)] - 0.506) < 1e-3 and abs(nb[(30, 0.3)] - 2.04e-5) < 1e-7
    KEEP['cell517'] = nb
    check('the Kitaev chain of the notebook in pyqula', ok,
          'add_onsite(4.0), add_exchange([0,0,4]), add_onsite(m) and pwave with delta and d have the L lowest levels of '
          '(5.19) with t=1, mu=-m and Delta = delta |d_x + i d_y| to %.0e, from the Majorana form; set_finite_system(n=8) '
          'of the bulk gives the same %.4f; the cell of Section 5.17 with delta=0.1, d=[1,1,0] and L=40 gives %.2e, %.2e '
          'and %.3f for mu = 0.3, 1.0, 2.5, and L=30 gives %.1e for mu=0.3'
          % (worst, fin, nb[(40, 0.3)], nb[(40, 1.0)], nb[(40, 2.5)], nb[(30, 0.3)]))

    L = 100
    gg = geometry.chain().get_supercell(L); gg.dimensionality = 0
    hh = gg.get_hamiltonian(); hh.add_onsite(4.0); hh.add_exchange([0.0, 0.0, 4.0]); hh.add_pairing(mode='pwave', delta=0.2, d=[1.0, 0.0, 0.0])
    es = np.linspace(-1, 1, 201)
    vals = []
    for site in (0, L // 10, L // 2):
        P = hh.get_operator('site', index=site) * hh.get_operator('electron')
        vals.append(np.array(hh.get_dos(operator=P, energies=es, delta=2e-2)[1])[100])
    parts = []
    for mu8 in (0.0, -8.0):                       # the spin-down chain, and the spin-up band 8 higher with its up-up pairing
        w, v = np.linalg.eigh(1j * majorana(L, 1.0, mu8, 0.2))
        u = (v[0::2, :] + 1j * v[1::2, :]) / np.sqrt(2)
        parts.append(np.array([np.sum(np.abs(u[i, :]) ** 2 * 0.02 / np.pi / (w ** 2 + 4e-4)) for i in (0, 10, 50)]))
    ok = np.allclose(vals, parts[0] + parts[1], rtol=1e-6) and np.allclose(vals, [4.427, 0.0843, 0.0081], atol=[1e-3, 1e-4, 1e-4])
    ok = ok and abs(parts[0][2] - 0.0079) < 1e-4 and parts[1].max() < 2e-4
    check('the local density of states of the end mode', ok,
          'the cell with 100 sites, delta=0.2 and the broadening 0.02 gives at E=0 the electron LDOS %.3f, %.4f and %.4f '
          'on the sites 0, 10, 50; the spinless chain alone gives %.3f, %.4f, %.4f, and the spin-up band, 6 above, adds '
          'its tails, %.0e at most' % (vals[0], vals[1], vals[2], parts[0][0], parts[0][1], parts[0][2], parts[1].max()))

    spec = importlib.util.spec_from_file_location('kitaevbdg', os.path.join(WEBNOTES, 'widgets', 'defs', 'kitaevbdg.py'))
    widget = importlib.util.module_from_spec(spec); spec.loader.exec_module(widget)
    wid, ok = {}, True
    for mu in (1.0, 1.5, 1.9, 2.5):
        levels = np.sort(np.abs(widget.compute(dict(mu=mu))['panels'][0]['series'][0]['y']))
        mine = qp(majorana(30, 1.0, mu, 1.0))
        ok = ok and np.allclose(levels[::2], mine, atol=1e-12)
        wid[mu] = mine[0]
    r31 = qp(majorana(31, 1.0, 1.5, 1.0))[0] / wid[1.5]
    ok = ok and wid[1.0] < 2e-9 and abs(wid[1.5] - 1.56e-4) < 1e-6 and abs(wid[1.9] - 0.0475) < 1e-4 and abs(r31 - 0.75) < 1e-3
    KEEP['widget'] = wid
    check('the widget kitaevbdg', ok,
          'its 60 levels for 30 sites and t=Delta=1 are those of the Majorana form, with the lowest at %.1e for mu=1, '
          '%.2e for mu=1.5 and %.4f for mu=1.9, where the bulk value |2t-|mu|| is 0.1; at Delta=t the decay root is -mu/2t, '
          'and one more site multiplies the splitting at mu=1.5 by %.4f' % (wid[1.0], wid[1.5], wid[1.9], r31))

    # The helical edge
    ok = True
    for (mu, Dv) in ((0.0, 1.0), (0.5, 1.0), (0.4, 0.3), (0.0, 0.5)):
        hcr = np.hypot(mu, Dv)
        edge = lambda kk, hh: np.kron(SZ, kk * SZ - mu * S0) + hh * np.kron(S0, SX) + Dv * np.kron(SX, S0)
        ok = ok and np.allclose(np.linalg.eigvalsh(edge(0.0, 0.3)), np.sort([0.3 + hcr, 0.3 - hcr, -0.3 + hcr, -0.3 - hcr]))
        kk = np.linspace(-3, 3, 601)
        gmin = lambda hh: min(np.abs(np.linalg.eigvalsh(edge(x, hh))).min() for x in kk)
        ok = ok and gmin(hcr) < 1e-9 and gmin(hcr - 0.1) > 0.02 and gmin(hcr + 0.1) > 0.02
    lv = np.linalg.eigvalsh(np.kron(SZ, 0 * SZ) + 0.3 * np.kron(S0, SX) + 0.5 * np.kron(SX, S0))
    check('the helical edge at k=0', ok and np.allclose(lv, [-0.8, -0.2, 0.2, 0.8]),
          'tau_z (v k sigma_z - mu) + h sigma_x + Delta tau_x has at k=0 the levels +-h +- sqrt(Delta^2+mu^2), %s for '
          'h=0.3, Delta=0.5 and mu=0, and its gap over all k closes only at h = sqrt(Delta^2+mu^2), checked for '
          '(mu, Delta) = (0, 1), (0.5, 1), (0.4, 0.3), (0, 0.5)' % np.round(lv, 2))

    Om = 0.5 * np.array([[1, 1j, 0, 0], [0, 0, 1, 1j], [0, 0, 1, -1j], [-1, 1j, 0, 0]])
    v_, W_ = 0.8, 0.7

    def lattice_edge(q, hh, Dv, mu=0.0):
        he = v_ * np.sin(q) * SZ + (W_ * (1 - np.cos(q)) + hh) * SX - mu * S0
        hm = v_ * np.sin(-q) * SZ + (W_ * (1 - np.cos(q)) + hh) * SX - mu * S0
        return np.block([[he, Dv * S0], [Dv * S0, -SY @ hm.conj() @ SY]])

    def z2(hh, Dv, mu=0.0):
        s = 1
        for q in (0.0, np.pi):
            A = -2j * dag(Om) @ lattice_edge(q, hh, Dv, mu) @ Om
            assert np.abs(A.imag).max() < 1e-12 and np.abs(A + A.T).max() < 1e-12
            s *= np.sign(pf4(A.real))
        return int(s)

    def junction(inner, outer, N=240, seg=(80, 160)):
        H = np.zeros((4 * N, 4 * N), complex)
        T = (v_ / 2j) * SZ - (W_ / 2) * SX
        bond = np.block([[T, 0 * S0], [0 * S0, -SY @ T.conj() @ SY]])
        for i in range(N):
            hh, Dv = inner if seg[0] <= i < seg[1] else outer
            H[4 * i:4 * i + 4, 4 * i:4 * i + 4] = np.block([[(W_ + hh) * SX, Dv * S0], [Dv * S0, (W_ + hh) * SX]])
            if i < N - 1:
                H[4 * i:4 * i + 4, 4 * i + 4:4 * i + 8] = bond
                H[4 * i + 4:4 * i + 8, 4 * i:4 * i + 4] = dag(bond)
        w, vv = np.linalg.eigh(H)
        idx = np.argsort(np.abs(w))
        wt = [(np.abs(vv[:, j]) ** 2).reshape(N, 4).sum(1) for j in idx[:2]]
        at_if = min(x[seg[0] - 15:seg[0] + 15].sum() + x[seg[1] - 15:seg[1] + 15].sum() for x in wt)
        at_end = min(x[:15].sum() + x[-15:].sum() for x in wt)
        return np.abs(w[idx[:3]]), at_if, at_end
    zs = [z2(hh, 0.3) for hh in (0.0, 0.2, 0.29, 0.31, 0.6)] + [z2(hh, 0.3, 0.4) for hh in (0.45, 0.55)]
    j1, j2, j3 = junction((0.0, 0.3), (0.6, 0.0)), junction((0.1, 0.3), (0.5, 0.3)), junction((0.1, 0.3), (0.2, 0.3))
    ok = zs == [-1, -1, -1, 1, 1, -1, 1] and j1[0][1] < 1e-12 and j1[1] > 0.99 and abs(j1[0][2] - 0.301) < 1e-3
    ok = ok and j2[0][1] < 1e-9 and j2[1] > 0.99 and j3[0][1] < 1e-12 and j3[1] < 1e-3 and j3[2] > 0.97
    check('two phases on the helical edge', ok,
          'on the lattice edge v sin k sigma_z + W(1 - cos k) sigma_x, v=0.8 and W=0.7, the index sign(Pf(0) Pf(pi)) is '
          '%s for h = 0, 0.2, 0.29, 0.31, 0.6 with Delta=0.3, and %s for h = 0.45, 0.55 with mu=0.4; a segment with '
          'Delta=0.3 between magnets h=0.6 has two levels at %.0e with a weight %.3f within 15 sites of the interfaces and '
          'the next at %.3f; with Delta=0.3 everywhere, h=0.1 inside and 0.5 outside give two levels at %.0e at the '
          'interfaces, and h=0.1 inside and 0.2 outside put them at the open ends, weight %.3f'
          % (' '.join('%+d' % z for z in zs[:5]), ' '.join('%+d' % z for z in zs[5:]), j1[0][1], j1[1], j1[0][2], j2[0][1], j3[2]))

    # Four Majoranas
    g4 = [c2[0] + dag(c2[0]), -1j * (c2[0] - dag(c2[0])), c2[1] + dag(c2[1]), -1j * (c2[1] - dag(c2[1]))]
    U12, U23, U34 = (expm(np.pi / 4 * g4[a] @ g4[a + 1]) for a in (0, 1, 2))
    A12, A23, A34 = (1j * g4[a] @ g4[a + 1] for a in (0, 1, 2))
    par2 = np.diag([1, -1, -1, 1])
    ok = np.allclose(U12, (np.eye(4) + g4[0] @ g4[1]) / np.sqrt(2)) and np.allclose(U12 @ g4[0] @ dag(U12), -g4[1])
    ok = ok and np.allclose(U12 @ g4[1] @ dag(U12), g4[0]) and np.allclose(U12 @ par2, par2 @ U12)
    ok = ok and np.allclose(A12 @ A23, -A23 @ A12) and np.allclose(A12 @ A34, A34 @ A12)
    pv = np.real(np.diag(A12))
    ok = ok and np.allclose(A12, np.diag(np.diag(A12))) and np.allclose(np.diag(U12)[pv < 0], np.exp(1j * np.pi / 4))
    ok = ok and np.allclose(np.diag(U12)[pv > 0], np.exp(-1j * np.pi / 4))
    dist = np.abs(U12 @ U23 - U23 @ U12).max()
    ok = ok and dist > 0.5 and np.allclose(U12 @ U34, U34 @ U12)
    check('the braid (5.23)', ok,
          'U_12 = exp(pi gamma_1 gamma_2/4) = (1 + gamma_1 gamma_2)/sqrt2 sends gamma_1 to -gamma_2 and gamma_2 to gamma_1, '
          'keeps the parity, and multiplies the states with i gamma_1 gamma_2 = -1 and +1 by exp(i pi/4) and exp(-i pi/4); '
          'i gamma_1 gamma_2 and i gamma_2 gamma_3 anticommute, i gamma_1 gamma_2 and i gamma_3 gamma_4 commute, '
          'U_12 U_23 - U_23 U_12 has entries up to %.2f and U_12 U_34 = U_34 U_12' % dist)

    phi = 0.3
    U = np.diag(np.exp(1j * phi * np.diag(N2).real))
    lhs = dag(U) @ cu @ U
    fit = np.vdot(pair.ravel(), (dag(U) @ pair @ U).ravel()) / np.vdot(pair.ravel(), pair.ravel())
    gs = lambda Dv: np.linalg.eigh(Dv * pair + np.conj(Dv) * dag(pair))[1][:, 0]
    pa = lambda Dv: np.vdot(gs(Dv), cdn @ cu @ gs(Dv))
    ang = np.angle(pa(0.5 * np.exp(2j * phi)) / pa(0.5))
    check('the gauge phase of (5.5)', np.allclose(lhs, np.exp(1j * phi) * cu) and abs(np.angle(fit) + 2 * phi) < 1e-12
          and abs(abs(fit) - 1) < 1e-12 and abs(ang - 2 * phi) < 1e-12,
          'with c -> c e^{i phi} the term c_up^dag c_dn^dag gets e^{%.3fi} for phi=0.3, which is (5.5), and the ground state '
          'with Delta e^{2i phi} has <c_dn c_up> multiplied by e^{%.3fi}, the Delta -> Delta e^{2i phi} of Section 5.7 and '
          'of the index page' % (np.angle(fit), ang))

    # Pairing symmetry
    worst, parity_ok = 0.0, True
    for mode in ("dx2y2", "extended_swave", "chiral_pwave", "swave"):
        hh = gsq.get_hamiltonian(); hh.add_pairing(mode=mode, delta=0.2)
        gen = hh.get_hk_gen()
        for _ in range(3):
            kr = rng.uniform(-0.5, 0.5, 2)
            Dp, Dm = gen([kr[0], kr[1], 0])[:2, 2:], gen([-kr[0], -kr[1], 0])[:2, 2:]
            worst = max(worst, np.abs(Dp - SY @ Dm.T @ SY).max())
            G, Gm = Dp @ ISY, Dm @ ISY
            worst = max(worst, np.abs(G + Gm.T).max())
            parity_ok = parity_ok and np.allclose((G - G.T) / 2, (Gm - Gm.T) / 2) and np.allclose((G + G.T) / 2, -(Gm + Gm.T) / 2)
            if mode == 'chiral_pwave':
                parity_ok = parity_ok and abs(np.trace(Dp)) < 1e-12
            else:
                parity_ok = parity_ok and np.allclose(Dp, Dp[0, 0] * S0)
    hh = gch.get_hamiltonian(); hh.add_pairing(mode="pwave", delta=0.2, d=[1.0, 1.0, 0.0])
    Dp, Dm = hh.get_hk_gen()([0.13, 0, 0])[:2, 2:], hh.get_hk_gen()([-0.13, 0, 0])[:2, 2:]
    worst = max(worst, np.abs(Dp - SY @ Dm.T @ SY).max())
    check('Fermi antisymmetry (5.11) in the basis of pyqula', worst < 1e-13 and parity_ok,
          'the electron-hole block P(k) = psi sigma_0 + d.sigma gives the pair matrix G = P i sigma_y, and G(k) = -G(-k)^T, '
          'which is P(k) = sigma_y P(-k)^T sigma_y, holds to %.0e for dx2y2, extended_swave, chiral_pwave, swave and pwave '
          'with d=[1,1,0]; the singlet part is psi sigma_0 and even in k, the triplet part odd' % worst)

    Nr = 4
    c8 = fermions(2 * Nr)
    ck = {}
    for mm in range(Nr):
        kk = 2 * np.pi * mm / Nr
        for s in range(2):
            ck[(mm, s)] = sum(np.exp(-1j * kk * n) * c8[2 * n + s] for n in range(Nr)) / np.sqrt(Nr)
    odd = 0.5 * sum(np.sin(2 * np.pi * mm / Nr) * (dag(ck[(mm, 0)]) @ dag(ck[((-mm) % Nr, 1)]) - dag(ck[(mm, 1)]) @ dag(ck[((-mm) % Nr, 0)]))
                    for mm in range(Nr))
    eps = lambda kk: -2 * (np.cos(kk[0]) + np.cos(kk[1])) + 2.0
    dk = lambda kk: 0.5 * (np.sin(kk[0]) + 1j * np.sin(kk[1]))
    H57 = lambda kk: np.block([[eps(kk) * S0, dk(kk) * S0], [np.conj(dk(kk)) * S0, -eps(kk) * S0]])
    kq = np.array([0.7, -1.1])
    broken = not np.allclose(P4 @ H57(kq).conj() @ P4, -H57(-kq))
    fake = min(np.min(np.abs(np.linalg.eigvalsh(H57(q)))) for q in pc.kmesh(2 * np.pi * np.eye(2), 40))
    Hz = lambda kk: np.block([[eps(kk) * S0, dk(kk) * SZ], [np.conj(dk(kk)) * SZ, -eps(kk) * S0]])
    trip = np.allclose(P4 @ Hz(kq).conj() @ P4, -Hz(-kq)) and abs(pc.chern_links(Hz, 2 * np.pi * np.eye(2), range(2), nk=36) - 2) < 1e-9
    check('one Delta(k) on both blocks of (5.7)', np.abs(odd).max() < 1e-12 and broken and abs(fake - 0.5) < 1e-9 and trip,
          'the operator of an odd Delta(k) on the identity, (1/2) sum_k sin k [c_k,up^dag c_-k,dn^dag - c_k,dn^dag c_-k,up^dag], '
          'is %.0e on a ring of 4 sites, and the BdG matrix with Delta_0 (sin kx + i sin ky) times the identity breaks '
          'particle-hole symmetry while its smallest energy is %.2f at mu=-2; the triplet with d along z, Delta(k) sigma_z, '
          'keeps it and has C=+2' % (np.abs(odd).max(), fake))

    Dv = 0.3 + 0.1j
    P54 = sum(Dv * dag(c8[2 * n]) @ dag(c8[2 * n + 1]) for n in range(Nr))
    P510 = -0.5 * sum(-Dv * dag(ck[(mm, 0)]) @ dag(ck[((-mm) % Nr, 1)]) + Dv * dag(ck[(mm, 1)]) @ dag(ck[((-mm) % Nr, 0)]) for mm in range(Nr))
    c6b = fermions(6)
    ck3 = lambda kk, s: sum(np.exp(-1j * kk * n) * c6b[2 * n + s] for n in range(3)) / np.sqrt(3)
    A3 = sum(dag(c6b[2 * n]) @ dag(c6b[2 * n + 1]) for n in range(3)); A3 = A3 + dag(A3)
    B3op = -0.5 * sum(dag(ck3(kk, 0)) @ dag(ck3(-kk, 1)) - dag(ck3(kk, 1)) @ dag(ck3(-kk, 0)) for kk in 2 * np.pi * np.arange(3) / 3)
    B3op = B3op + dag(B3op)
    xfit = np.vdot(B3op.ravel(), A3.ravel()).real / np.vdot(B3op.ravel(), B3op.ravel()).real
    KEEP['510'] = xfit
    check('(5.10)', np.abs(P54 - P510).max() < 1e-12 and abs(xfit + 1) < 1e-12 and np.abs(A3 - xfit * B3op).max() < 1e-12,
          'with the primed sum over the whole zone, the term Delta c_up^dag c_dn^dag of (5.4) is (5.10) with Delta_updn = '
          '-Delta and Delta_dnup = +Delta, to %.0e on a ring of 4 sites, and the fit on a ring of 3 sites gives %.3f Delta'
          % (np.abs(P54 - P510).max(), xfit))

    th = np.linspace(0, 2 * np.pi, 3601)
    vals = []
    for rad in (0.3, 0.5):
        kx, ky = np.pi + rad * np.cos(th), rad * np.sin(th)
        vals.append(np.abs(np.cos(kx) - np.cos(ky)))
    diag = abs(np.cos(1.1) - np.cos(-1.1)) == 0
    KEEP['X'] = (vals[0].min(), vals[1].min())
    check('the d-wave nodes and a pocket at X', diag and abs(-2 * (np.cos(np.pi / 2) * 2)) < 1e-15 and abs(vals[0].min() - 1.9552) < 1e-4
          and vals[0].max() < 2 and abs(vals[1].min() - 1.876) < 1e-3,
          'Delta_d vanishes on kx = +-ky, the Fermi surface at mu=0 passes through (pi/2, pi/2), and on a circle of radius '
          '0.3 around X the factor |cos kx - cos ky| goes from %.4f to %.4f, and down to %.3f on a radius 0.5'
          % (vals[0].min(), vals[0].max(), vals[1].min()))

    out = []
    for mu in (-2.0, -3.5):
        a = np.arccos(-mu / 2 - 1)
        kx = np.linspace(-a, a, 200001)
        ky = np.arccos(np.clip(-mu / 2 - np.cos(kx), -1, 1))
        mod = 0.2 * np.sqrt(np.sin(kx) ** 2 + np.sin(ky) ** 2)
        f = lambda q, mu=mu: np.sqrt((-2 * (np.cos(q[0]) + np.cos(q[1])) - mu) ** 2 + 0.04 * (np.sin(q[0]) ** 2 + np.sin(q[1]) ** 2))
        g = lambda q, mu=mu: np.sqrt((-2 * (np.cos(q[0]) + np.cos(q[1])) - mu) ** 2 + 0.04)
        ep = min(minimize(f, x0, method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-13)).fun for x0 in ([0.3, 0.2], [0.1, 1.2], [1.0, 0.9], [0.05, 0.6]))
        es_ = min(minimize(g, x0, method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-13)).fun for x0 in ([0.3, 0.2], [0.1, 1.2], [1.0, 0.9]))
        out.append((mod.min(), mod.max(), es_, ep))
    ok = abs(out[0][0] - 0.2) < 1e-4 and abs(out[0][1] - 0.2449) < 1e-4 and abs(out[0][2] - 0.2) < 1e-6 and abs(out[0][3] - 0.2) < 1e-6
    ok = ok and abs(out[1][2] - 0.2) < 1e-6 and abs(out[1][3] - 0.1314) < 1e-4
    KEEP['pip'] = out
    check('p+ip along the Fermi surface', ok,
          'with Delta_0=0.2t and mu=-2t the factor |Delta_p+ip| goes from %.4f t to %.4f t along the Fermi surface, and the '
          'smallest energy is %.4f t for s-wave and %.4f t for p+ip; at mu=-3.5t they are %.4f t and %.4f t'
          % (out[0][0], out[0][1], out[0][2], out[0][3], out[1][2], out[1][3]))

    # Constants
    hP, e = 6.62607015e-34, 1.602176634e-19
    x1, x2 = np.linspace(0, 0.999, 2000), np.linspace(1.001, 6, 2000)
    veff = lambda Vc, x: Vc - 1 / (1 - x ** 2)
    ok = abs(hP / (2 * e) - 2.0678e-15) < 1e-19 and abs(hP / e - 4.1357e-15) < 1e-19 and abs(2 * e / hP * 1e-12 - 483.6) < 0.05
    ok = ok and veff(0.5, x1).max() < 0 and abs(veff(0.5, x1).max() + 0.5) < 1e-12 and veff(0.5, x2).min() > 0 and veff(1.5, 0.0) > 0
    check('the flux quantum, the Josephson frequency and the phonon interaction', ok,
          'h/2e = %.4e Wb, h/e = %.4e Wb, 2e/h = %.1f MHz per microvolt; V_eff in units of 2g^2/w0 with V_c = 0.5 is at '
          'most %.2f below w0 and positive above, while V_c = 1.5 is %+.1f at w = 0'
          % (hP / (2 * e), hP / e, 2 * e / hP * 1e-12, veff(0.5, x1).max(), veff(1.5, 0.0)))

    # Open points of the old text
    check('Section 5.8, the minus sign', KEEP['sign'] == 0,
          'without the sign of (5.6) the pairing block is Delta sigma_z and the coupling between the two blocks is %.0f'
          % KEEP['sign'])
    check('the quiz of Section 5.10', KEEP['X'][0] < 2,
          'on a pocket of radius 0.3 around X the gap is %.3f Delta_0, below 2 Delta_0, and %.3f Delta_0 for a radius 0.5' % KEEP['X'])
    check('(5.10) of Section 5.11', abs(KEEP['510'] + 1) < 1e-12,
          'Delta_updn of (5.10) is %.0f times the Delta of (5.4) with the sum over the whole zone' % KEEP['510'])
    out_s, tri_s, fl_s = KEEP['side']
    check('Section 5.14, the sign of C', abs(tri_s[1][0] + 2) < 1e-6 and abs(out_s[0][0] - 2) < 1e-6 and abs(KEEP['pmi'][2][0] - 2) < 1e-6,
          'the same p_x + i p_y gives %+.0f with the pocket of empty states of the notebook and %+.0f with a pocket of '
          'filled states, and p_x - i p_y gives %+.0f on the notebook model' % (tri_s[1][0], out_s[0][0], KEEP['pmi'][2][0]))
    pip = KEEP['pip']
    check('the quiz of Section 5.14', pip[0][1] > pip[0][0] + 0.04 and abs(pip[0][3] - 0.2) < 1e-6 and pip[1][3] < 0.14,
          'on the Fermi surface of mu=-2t the p+ip gap goes from %.3f t to %.3f t while the s-wave one is 0.2 t, the '
          'smallest energies are both 0.2 t, and at mu=-3.5t they differ, 0.2 t against %.4f t' % (pip[0][0], pip[0][1], pip[1][3]))
    ent, wnd = KEEP['520']
    check('(5.20) of Section 5.16', abs(ent + 1.4j) < 1e-12 and wnd[0] == -wnd[2],
          'with (2.7) the entry of (5.8) at k=pi/2 is %.1fi for Delta=0.7, so -2i Delta sin k, and the sign changes only '
          'the signed winding' % ent.imag)
    mf = KEEP['mf']
    check('the try-it of Section 5.5', np.allclose(np.round(mf, 1), [0.1, 0.2, 0.4]) and np.allclose(np.round(mf, 2), [0.10, 0.22, 0.36]),
          'the loop gives %.3f, %.3f and %.3f, which is 0.1, 0.2 and 0.4 to one digit and 0.10, 0.22 and 0.36 to two' % tuple(mf))
    wid = KEEP['widget']
    check('the widget text of Section 5.17', wid[1.9] > 0.04 and wid[1.5] > 1e-4,
          'with 30 sites the two levels are at %.1e for mu=1.5t and at %.3f t for mu=1.9t, half of the bulk value 0.1 t'
          % (wid[1.5], wid[1.9]))
    sq, twice = KEEP['gap']
    check('the word gap', abs(twice - 2 * 0.3) < 1e-5 and abs(KEEP['bulk'] - 0.8165) < 1e-4,
          'the distance between the branches is %.4f for Delta=0.3, twice the smallest energy, and the 0.82t of the quiz '
          'of Section 5.17 is the smallest energy %.4f t, while the branches are %.3f t apart' % (twice, KEEP['bulk'], 2 * KEEP['bulk']))
    nb = KEEP['cell517']
    g40 = geometry.chain().get_supercell(40); g40.dimensionality = 0
    hh = g40.get_hamiltonian(); hh.add_onsite(4.0); hh.add_exchange([0.0, 0.0, 4.0]); hh.add_onsite(-0.3)
    hh.add_pairing(mode='pwave', delta=0.1, d=[1.0, 1.0, 0.0])
    same = abs(np.sort(np.abs(hh.get_bands()[1]))[0] - nb[(40, 0.3)]) < 1e-12
    check('the try-it of Section 5.17', same and nb[(40, 2.5)] > 0.5,
          'mu=0.3 in the cell is add_onsite(0.3), which is mu=-0.3 of (5.22), and add_onsite(-0.3), which is mu=+0.3, '
          'gives the same %.2e; mu=2.5 gives %.3f'
          % (nb[(40, 0.3)], nb[(40, 2.5)]))
    hR = gsq.get_hamiltonian(); hR.add_rashba(0.3)
    hRn = gsq.get_hamiltonian(); hRn.add_rashba(0.3); hRn.setup_nambu_spinor()
    kq3 = [0.1, 0.2, 0.0]
    off = np.abs(hRn.get_hk_gen()(kq3)[2:, 2:] + hR.get_hk_gen()(kq3).conj()).max()
    check('the notebook text', KEEP['exchange'] > 0.99 and abs(off - 0.71) < 0.01,
          'add_exchange([0,0,J]) moves the spin-up band up, sz=%+.0f for the upper band, against the -J s_z of the '
          'notebook, and the hole block -(H0-mu)^* of the notebook is off by %.2f for a Rashba coupling 0.3 at k=(0.1,0.2)'
          % (KEEP['exchange'], off))
    print('%d checks hold, %.1f s' % (COUNT[0], time.time() - t0))


if __name__ == '__main__':
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            main()
        finally:
            os.chdir(cwd)
