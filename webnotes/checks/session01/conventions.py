"""Checks of webnotes/conventions/session01.md, with numbers. Every bullet of the sheet is asserted here, in the order
of the sheet, by a calculation with numpy and, where pyqula has the model, by pyqula. It prints one line per bullet and
exits 0 when all hold.

Not asserted, since they are read and are not a number: what the release 0.0.96 of pyqula on PyPI does, which the
sheet says was read in its code and run only once apart from this script, that the widget of Section 1.10 draws the density from pyqula, that a
spinless loop with mf=None and no MF.pkl starts from a random guess, and that a figure script runs pyqula inside
style.run_script. Not asserted either, since the sheet gives them as not checked: that the exact chain (1.6) orders
only for V > 2t, that the s-wave state wins away from half filling, and the sign of the pairing of pyqula against
(5.3), which the sheet of Session 5 gives. Outcomes that depend on rounding or on a random guess are left out: the direction that a random guess picks,
and the loops that drift to another state or do not converge with mix=0.9.

Run it from anywhere:  python3 webnotes/checks/session01/conventions.py"""
import contextlib, io, json, os, tempfile, time
from math import comb
import numpy as np
from scipy import linalg, special, optimize

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
NOTEBOOK = os.path.join(REPO, 'jupyter-notebooks', 'session1.ipynb')
COUNT = [0]


def check(name, ok, detail):
    """Prints one line for a check and stops the script when it does not hold."""
    print(('ok    ' if ok else 'FAIL  ') + name + ': ' + detail, flush=True)
    assert ok, name
    COUNT[0] += 1


@contextlib.contextmanager
def quiet():
    """Keeps the iteration messages of pyqula out of the output."""
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        yield


def near(x, y, tol):
    return bool(np.all(np.abs(np.asarray(x, complex) - np.asarray(y, complex)) < tol))


# ----------------------------------------------------------------------------------------------- the Fock space
def fock(L, fermions=True):
    """Annihilation operators of L modes on the states |n_0 n_1 ...> = (c_0^+)^n_0 (c_1^+)^n_1 ... |0>, where the
    integer of a state has the bit j equal to n_j. For fermions c_j has the sign (-1)^(n_0 + ... + n_(j-1)), and
    without the sign these are hard-core bosons."""
    D = 2 ** L
    ops = []
    for j in range(L):
        c = np.zeros((D, D))
        for s in range(D):
            if s >> j & 1:
                c[s ^ (1 << j), s] = (-1) ** bin(s & ((1 << j) - 1)).count('1') if fermions else 1.0
        ops.append(c)
    return ops


def jordan_wigner(L):
    """The same operators from the Jordan-Wigner string, c_j = Z x ... x Z x a x 1 x ..., with mode 0 the last
    factor of the Kronecker product."""
    a, Z, one = np.array([[0., 1.], [0., 0.]]), np.diag([1., -1.]), np.eye(2)
    out = []
    for j in range(L):
        m = np.ones((1, 1))
        for l in reversed(range(L)):
            m = np.kron(m, a if l == j else (Z if l < j else one))
        out.append(m)
    return out


def number_blocks(H, N):
    """The eigenvalues of H in the sector of each particle number, with N the diagonal number operator."""
    n = np.round(np.diag(N)).astype(int)
    return {k: np.linalg.eigvalsh(H[np.ix_(n == k, n == k)]) for k in sorted(set(n))}


def chain_matrix(bonds):
    """The single-particle matrix of an open chain with the given list of bond matrix elements."""
    H = np.zeros((len(bonds) + 1, len(bonds) + 1))
    for i, b in enumerate(bonds):
        H[i, i + 1] = H[i + 1, i] = b
    return H


# ------------------------------------------------------------------------------- the Hubbard term, the chain loops
def site_ops():
    """c_up, c_dn and the derived operators on the four states of one site."""
    cu, cd = fock(2)
    nu, nd = cu.T @ cu, cd.T @ cd
    Sx = 0.5 * (cu.T @ cd + cd.T @ cu)
    Sy = -0.5j * (cu.T @ cd - cd.T @ cu)
    Sz = 0.5 * (nu - nd)
    return cu, cd, nu, nd, Sx, Sy, Sz


def stagger(delta, ks, f=lambda k: 1 + np.exp(-1j * k)):
    """<delta/E> of the lower band of [[-delta, f(k)], [f(k)*, delta]], averaged over the momenta ks. It is the
    difference n_A - n_B of one spin in a staggered potential, -delta on A and +delta on B."""
    E = np.sqrt(delta ** 2 + np.abs(f(ks)) ** 2)
    return np.mean(delta / E) if delta > 0 else 0.0


def kring(nk):
    return 2 * np.pi * np.arange(nk) / nk


def loop(U, ks, m0=0.1, mix=1.0, f=lambda k: 1 + np.exp(-1j * k), n=20000, tol=1e-13):
    """The Hartree loop of the half-filled antiferromagnet, m -> <Delta/E> with Delta = U m/2, on the momenta ks."""
    m = m0
    for i in range(n):
        new = stagger(U * m / 2, ks, f)
        if abs(new - m) < tol:
            return new
        m = mix * new + (1 - mix) * m
    return new


def chain_I(delta):
    """(1/pi) int_{-pi/2}^{pi/2} dk / sqrt(delta^2 + 4 cos^2 k), with the complete elliptic integral."""
    return 2 / np.pi * special.ellipk(4 / (delta ** 2 + 4)) / np.sqrt(delta ** 2 + 4)


def chain_m(U):
    """The moment of the half-filled Hubbard chain in Hartree, from the gap equation 1 = (U/2) I(Delta)."""
    delta = optimize.brentq(lambda d: U / 2 * chain_I(d) - 1, 1e-12, 50)
    return 2 * delta / U, delta


def uniform_map(m, U, n=1.0):
    """The uniform Hartree map m -> m' of the chain -2t cos k at n electrons per site, zero temperature, with the
    bands E - sigma U m/2 and the common chemical potential that holds n."""
    def counts(mu):
        up = np.arccos(np.clip(-(mu + U * m / 2) / 2, -1, 1)) / np.pi
        dn = np.arccos(np.clip(-(mu - U * m / 2) / 2, -1, 1)) / np.pi
        return up, dn
    mu = optimize.brentq(lambda x: sum(counts(x)) - n, -3 - U, 3 + U)
    up, dn = counts(mu)
    return up - dn


def uniform_energy(m, U, n=1.0):
    """The energy per site of the uniform state of the chain with the densities (n + m)/2 and (n - m)/2."""
    band = -(2 / np.pi) * (np.sin(np.pi * (n + m) / 2) + np.sin(np.pi * (n - m) / 2))
    return band + U * (n ** 2 - m ** 2) / 4


def ring_hartree_cdw(L, V, guess=0.3, n=3000):
    """Charges and levels of the spinless ring of L sites at half filling, hopping -1, in Hartree."""
    T = chain_matrix([-1.0] * (L - 1)); T[0, -1] = T[-1, 0] = -1.0
    dens = 0.5 + guess * (-1) ** np.arange(L) / 2
    for i in range(n):
        w, v = np.linalg.eigh(T + np.diag(V * (np.roll(dens, 1) + np.roll(dens, -1))))
        new = np.sum(np.abs(v[:, :L // 2]) ** 2, axis=1)
        if np.abs(new - dens).max() < 1e-13:
            break
        dens = 0.5 * new + 0.5 * dens
    return new, w


def ring_hf_cdw(L, V, n=4000):
    """The same ring in Hartree-Fock, with the hopping -1 - V <c_(i+1)^+ c_i> on each bond. Returns the charges and
    the hoppings."""
    dens = 0.5 + 0.2 * (-1) ** np.arange(L)
    chi = np.full(L, 0.3)
    j, jp = np.arange(L), (np.arange(L) + 1) % L
    for i in range(n):
        H = np.diag(V * (np.roll(dens, 1) + np.roll(dens, -1)))
        H[j, jp] = H[jp, j] = -1.0 - V * chi
        w, v = np.linalg.eigh(H)
        occ = v[:, :L // 2]
        rho = occ @ occ.T
        new_d, new_c = np.diag(rho).copy(), rho[jp, j]
        if max(np.abs(new_d - dens).max(), np.abs(new_c - chi).max()) < 1e-12:
            break
        dens, chi = 0.7 * new_d + 0.3 * dens, 0.7 * new_c + 0.3 * chi
    return dens, -1.0 - V * chi


def dimer_hartree(U, m0, b=0.0, n=20000, mix=0.5):
    """The Hubbard dimer in Hartree, hopping -1, a staggered field b that stays, from the guess m0 on site 0. Returns
    the moment of site 0, the occupied orbitals of the two spins, the energy with the double counting and the gap."""
    m = np.array([m0, -m0])
    for i in range(n):
        orb, lev = {}, {}
        for s in (1, -1):
            # spin s feels U <n_(-s)> = (U/2)(1 - s m) on each site, and the field -s b on site 0 and +s b on site 1
            H = np.array([[U / 2 * (1 - s * m[0]) - s * b, -1.0], [-1.0, U / 2 * (1 - s * m[1]) + s * b]])
            w, v = np.linalg.eigh(H)
            orb[s], lev[s] = v[:, 0], w
        new = np.abs(orb[1]) ** 2 - np.abs(orb[-1]) ** 2
        if np.abs(new - m).max() < 1e-14:
            break
        m = mix * new + (1 - mix) * m
    nu, nd = np.abs(orb[1]) ** 2, np.abs(orb[-1]) ** 2
    energy = lev[1][0] + lev[-1][0] - U * np.sum(nu * nd)
    gap = min(lev[1][1], lev[-1][1]) - max(lev[1][0], lev[-1][0])
    return new[0], orb, energy, gap


def dimer_exact():
    """Modes (0 up, 0 dn, 1 up, 1 dn) of the Hubbard dimer with hopping -1."""
    c = fock(4)
    n = [x.T @ x for x in c]
    hop = -(c[0].T @ c[2] + c[2].T @ c[0] + c[1].T @ c[3] + c[3].T @ c[1])
    return c, n, hop


def ising_free_fermion_gap(L, g, J=1.0):
    """The splitting of the two lowest states of the open quantum Ising chain from its free fermions, twice the
    smallest singular value of the bidiagonal matrix with g on the diagonal and -J next to it."""
    M = np.diag(np.full(L, g)) + np.diag(np.full(L - 1, -J), 1)
    return 2 * np.linalg.svd(M, compute_uv=False).min()


def ising_ed(L, g, J=1.0):
    """The two lowest levels and the flip parity of the ground state of the open quantum Ising chain, exactly."""
    sx, sz, one = np.array([[0., 1.], [1., 0.]]), np.diag([1., -1.]), np.eye(2)

    def op(o, i):
        m = np.ones((1, 1))
        for l in range(L):
            m = np.kron(m, o if l == i else one)
        return m
    H = -J * sum(op(sz, i) @ op(sz, i + 1) for i in range(L - 1)) - g * sum(op(sx, i) for i in range(L))
    w, v = np.linalg.eigh(H)
    P = np.ones((1, 1))
    for l in range(L):
        P = np.kron(P, sx)
    return w[:2], v[:, 0] @ P @ v[:, 0]


# ---------------------------------------------------------------------------------------------------- the checks
def main():
    from pyqula import geometry, islands, meanfield
    t0 = time.time()
    rng = np.random.default_rng(7)
    nb = json.load(open(NOTEBOOK, encoding='utf-8'))
    cells = [''.join(c['source']) for c in nb['cells']]

    def cell_after(title):
        """The source of the first code cell after the markdown cell whose first line has the title."""
        i = next(i for i, c in enumerate(nb['cells']) if c['cell_type'] == 'markdown' and title in cells[i].split('\n')[0])
        return next(cells[j] for j in range(i + 1, len(cells)) if nb['cells'][j]['cell_type'] == 'code'), cells[i]

    # ======================================================================= operators and the Fock space
    c3, jw3 = fock(3), jordan_wigner(3)
    vac = np.zeros(8); vac[0] = 1
    c4 = fock(4)
    alg = max(np.abs(c4[i] @ c4[j].T + c4[j].T @ c4[i] - (i == j) * np.eye(16)).max() for i in range(4) for j in range(4))
    alg = max(alg, max(np.abs(c4[i] @ c4[j] + c4[j] @ c4[i]).max() for i in range(4) for j in range(4)))
    vacuum = max(np.abs(c @ np.eye(16)[0]).max() for c in c4)
    s1 = (c3[0].T @ c3[1].T @ vac)[0b011]
    s2 = (c3[1].T @ c3[0].T @ vac)[0b011]
    s3 = (c3[2].T @ c3[0].T @ vac)[0b101]
    ok = all(np.array_equal(a, b) for a, b in zip(c3, jw3)) and alg == 0 and vacuum == 0 and (s1, s2, s3) == (1, -1, -1)
    check('the order of a Fock state', ok,
          'c0^+ c1^+|0> = %+.0f|110>, c1^+ c0^+|0> = %+.0f|110>, c2^+ c0^+|0> = %+.0f|101>, the matrices are the '
          'Jordan-Wigner ones, and (1.1) and (1.3) hold on four modes to %.0e' % (s1, s2, s3, alg))

    hop02 = c3[0].T @ c3[2]
    across = hop02[0b011, 0b110], hop02[0b001, 0b100]          # site 1 occupied, site 1 empty
    b3 = fock(3, fermions=False)
    tri = lambda ops: -sum(ops[i].T @ ops[j] + ops[j].T @ ops[i] for i, j in ((0, 1), (1, 2), (2, 0)))
    N3 = sum(x.T @ x for x in c3)
    ef, eb = number_blocks(tri(c3), N3)[2], number_blocks(tri(b3), N3)[2]
    e1 = np.linalg.eigvalsh(-(np.ones((3, 3)) - np.eye(3)))
    pairs = np.sort([e1[i] + e1[j] for i in range(3) for j in range(i + 1, 3)])
    check('the sign of a hop across an occupied site', across == (-1.0, 1.0) and near(ef, pairs, 1e-12) and near(eb, [-2, 1, 1], 1e-12),
          'c0^+ c2 has the element %+.0f across an occupied site 1 and %+.0f across an empty one, on the triangle with -t two '
          'fermions have %s, the sums of two of %s, and two hard-core bosons %s'
          % (across[0], across[1], np.round(ef, 6), np.round(e1, 6), np.round(eb, 6)))

    T4 = rng.normal(size=(4, 4)); T4 = T4 + T4.T
    V4 = rng.normal(size=(4, 4, 4, 4))
    H4 = sum(T4[i, j] * c4[i].T @ c4[j] for i in range(4) for j in range(4))
    Q = sum(V4[i, j, k, l] * c4[i].T @ c4[j].T @ c4[k] @ c4[l] for i in range(4) for j in range(4) for k in range(4) for l in range(4))
    H4 = H4 + Q + Q.T
    N4 = sum(x.T @ x for x in c4)
    comm = np.abs(H4 @ N4 - N4 @ H4).max()
    sizes = [int(np.sum(np.round(np.diag(N3)) == k)) for k in range(4)]
    spinful = sum(comb(6, k) for k in range(7))
    check('the size of the Fock space', comm < 1e-10 and sizes == [1, 3, 3, 1] and 4 ** 3 == spinful == 64 and 2 ** 20 == 1048576,
          '(1.5) with random t_ij and V_ijkl commutes with N to %.0e, three spinless sites have %d states, %s by particle '
          'number, three spinful sites have 4^3 = %d = sum_N C(6,N) states for a 6 x 6 single-particle matrix, and 2^20 = %d'
          % (comm, 2 ** 3, sizes, spinful, 2 ** 20))

    c2 = fock(2)
    N2 = sum(x.T @ x for x in c2)
    Hd = 1.0 * (c2[0].T @ c2[1] + c2[1].T @ c2[0])            # (1.2) with t = 1
    blocks = number_blocks(Hd, N2)
    one = np.linalg.eigh(np.array([[0., 1.], [1., 0.]]))
    anti = one[1][:, 0] * np.sign(one[1][0, 0])
    bos = np.diag(np.sqrt([1., 2.]), 1)                         # a boson with up to two per site
    I3 = np.eye(3)
    B0, B1 = np.kron(bos, I3), np.kron(I3, bos)
    NB = B0.T @ B0 + B1.T @ B1
    eB = number_blocks(B0.T @ B1 + B1.T @ B0, NB)[2]
    ok = near(blocks[1], [-1, 1], 1e-12) and near(anti, [1 / np.sqrt(2), -1 / np.sqrt(2)], 1e-12) and near(blocks[2], [0], 1e-12)
    check('the two sites of (1.2)', ok and near(eB, [-2, 0, 2], 1e-12),
          'with +t one electron has %s, the lower one on the antisymmetric state %s, two fermions have %s and two bosons %s'
          % (np.round(blocks[1], 6), np.round(anti, 3), np.round(blocks[2], 6), np.round(eB, 6)))

    # ======================================================================= the sign of the hopping
    L = 30
    Hm, Hp = chain_matrix([-1.0] * (L - 1)), chain_matrix([1.0] * (L - 1))
    (wm, vm), (wp, vp) = np.linalg.eigh(Hm), np.linalg.eigh(Hp)
    stag = (-1) ** np.arange(L)
    same = near(wm, wp, 1e-12) and near(np.abs(vm) ** 2, np.abs(vp) ** 2, 1e-12)
    same = same and all(abs(abs(np.dot(vp[:, n], stag * vm[:, n])) - 1) < 1e-12 for n in range(L))
    tri_m = np.linalg.eigvalsh(-(np.ones((3, 3)) - np.eye(3)))
    tri_p = np.linalg.eigvalsh(np.ones((3, 3)) - np.eye(3))
    gc = geometry.chain()
    pq = gc.get_hamiltonian(has_spin=False).get_hk_gen()([0.3, 0, 0])[0, 0]
    pqm = gc.get_hamiltonian(has_spin=False, tij=[-1.]).get_hk_gen()([0.3, 0, 0])[0, 0]
    note = r'E_n = 2t\cos(k_n)' in cells[5]
    ok = same and near(pq, 2 * np.cos(0.6 * np.pi), 1e-12) and near(pqm, -2 * np.cos(0.6 * np.pi), 1e-12) and note
    check('the sign of the hopping', ok and near(tri_m, [-2, 1, 1], 1e-12) and near(tri_p, [-1, -1, 2], 1e-12),
          'pyqula has the band %+.4f = 2 cos k at k = 0.3 x 2 pi, and %+.4f with tij=[-1.], the notebook writes E_n = 2t cos k_n, '
          'on the chain of 30 sites level n of -t and of +t have the same energy and density and differ by (-1)^j, and the '
          'triangle has %s with -t and %s with +t' % (pq.real, pqm.real, np.round(tri_m, 6), np.round(tri_p, 6)))

    N = 10
    g10 = geometry.chain().get_supercell(N); g10.dimensionality = 0
    out = []
    for tij in (None, [-1.]):
        h = g10.get_hamiltonian(has_spin=False) if tij is None else g10.get_hamiltonian(has_spin=False, tij=tij)
        w, v = np.linalg.eigh(np.asarray(h.intra.todense() if hasattr(h.intra, 'todense') else h.intra).real)
        psi = v[:, 0]
        box = np.sin(np.pi * np.arange(1, N + 1) / (N + 1)) ** 2 * 2 / (N + 1)
        out.append((int(np.sum(psi[:-1] * psi[1:] < 0)), np.abs(psi ** 2 - box).max()))
    check('the lowest state of an open chain', out[0][0] == 9 and out[1][0] == 0 and max(out[0][1], out[1][1]) < 1e-12,
          'N=10: the lowest state changes sign on %d of the 9 bonds with the +1 of pyqula and on %d with tij=[-1.], and its '
          'weight is 2 sin^2(pi j/(N+1))/(N+1) in both cases, to %.0e' % (out[0][0], out[1][0], max(out[0][1], out[1][1])))

    res = []
    for N in (10, 100):
        exact = -2 * np.cos(np.arange(1, N + 1) * np.pi / (N + 1))
        g = geometry.chain().get_supercell(N); g.dimensionality = 0
        lev = np.sort(np.real(g.get_hamiltonian(has_spin=False).get_bands()[1]))
        res.append((N, lev[N // 2] - lev[N // 2 - 1], 4 * np.sin(np.pi / (2 * (N + 1))), 2 * np.pi / (N + 1),
                    np.abs(lev - np.sort(exact)).max()))
    ok = near([r[1] for r in res], [r[2] for r in res], 1e-12) and max(r[4] for r in res) < 1e-12
    ok = ok and abs(res[0][1] - 0.5693) < 1e-4 and abs(res[1][1] - 0.0622) < 1e-4
    check('the levels of an open chain', ok,
          ', '.join('N=%d spacing at the center %.4f = 4t sin(pi/2(N+1)), 2 pi t/(N+1) = %.4f' % (r[0], r[1], r[3]) for r in res)
          + ', pyqula with get_supercell(N) and dimensionality=0 agrees with -2t cos(n pi/(N+1)) to %.0e' % max(r[4] for r in res))

    # ======================================================================= the finite systems of the pages
    a1, a2 = np.array([1.5, np.sqrt(3) / 2]), np.array([0.0, np.sqrt(3)])
    pts = []
    for i in range(-4, 5):
        for j in range(-4, 5):
            if max(abs(i), abs(j), abs(i + j)) <= 3:
                for th in np.arange(6) * np.pi / 3:
                    pts.append(i * a1 + j * a2 + [np.cos(th), np.sin(th)])
    pts = np.unique(np.round(pts, 8), axis=0)
    A = np.isclose(np.linalg.norm(pts[:, None] - pts[None], axis=-1), 1.0).astype(float)
    E, Vv = np.linalg.eigh(-A)
    gi = islands.get_geometry(name="honeycomb", n=4, nedges=6, rot=0)
    hi = gi.get_hamiltonian(has_spin=False)
    Ei = np.linalg.eigvalsh(np.asarray(hi.intra.todense() if hasattr(hi.intra, 'todense') else hi.intra).real)
    r = np.linalg.norm(pts, axis=1)
    groups, i = [], 0
    while i < len(E):
        j = i
        while j + 1 < len(E) and E[j + 1] - E[i] < 1e-8:
            j += 1
        groups.append(list(range(i, j + 1)))
        i = j + 1
    dist = [np.sum(np.mean(np.abs(Vv[:, gr]) ** 2, axis=1) * r) for gr in groups[:6]]
    low = Vv[:, 0] * np.sign(Vv[0, 0])
    ok = len(pts) == 96 and len(gi.r) == 96 and near(np.sort(E), Ei, 1e-9) and len(groups[0]) == 1 and np.all(low > 0)
    ok = ok and abs(r[np.argmax(low)] - 1) < 1e-9 and near([dist[0], dist[1], dist[5]], [2.87, 3.74, 4.43], 5e-3)
    check('the hexagonal island of Section 1.10', ok,
          '%d sites, the same spectrum as islands.get_geometry(name="honeycomb", n=4, nedges=6, rot=0), the lowest level of '
          '-t is single, of one sign on every site and largest at distance %.2f from the center, and the mean distance of '
          'the density of the levels 1, 2 and 6 is %.2f, %.2f and %.2f' % (len(pts), r[np.argmax(low)], dist[0], dist[1], dist[5]))

    weak = np.sort(np.abs(np.linalg.eigvalsh(chain_matrix([1.0 if b % 2 == 0 else 2.0 for b in range(19)]))))
    strong = np.sort(np.abs(np.linalg.eigvalsh(chain_matrix([2.0 if b % 2 == 0 else 1.0 for b in range(19)]))))
    ks = np.linspace(-np.pi, np.pi, 2001)
    bulk = 2 * np.min(np.abs(1 + 2 * np.exp(1j * ks)))
    ok = abs(bulk - 2) < 1e-6 and abs(weak[0] - 1.5e-3) < 1e-4 and abs(weak[1] - weak[0]) < 1e-12 and abs(weak[2] - 1.11) < 5e-3
    check('the two chains of the quiz of Section 1.2', ok and abs(strong[0] - 1.07) < 5e-3,
          'the bulk gap is 2|t1-t2| = %.3f, the 20 sites with the weak bond at the ends have two levels at |E| = %.1e and the '
          'next at %.2f, and with the strong bond at the ends the lowest |E| is %.2f' % (bulk, weak[0], weak[2], strong[0]))

    gb = geometry.bichain()
    hb = gb.get_hamiltonian(has_spin=False)
    hb.add_sublattice_imbalance(0.6)
    gen = hb.get_hk_gen()
    kr = np.linspace(0, 1, 201)
    bands = np.array([np.linalg.eigvalsh(gen([k, 0, 0])) for k in kr])
    q = np.pi * kr - np.pi / 2                                   # the momentum per site, measured from the zone edge
    form = np.sqrt(0.36 + (2 * np.sin(q)) ** 2)
    check('the chain with the onsite energies +-m', near(bands[:, 1], form, 1e-12) and near(bands[:, 0], -form, 1e-12)
          and abs(bands[100, 1] - bands[100, 0] - 1.2) < 1e-12,
          'bichain with add_sublattice_imbalance(0.6) has the bands +-sqrt(m^2 + (2t sin q)^2), q from the zone edge in units of '
          'the inverse site spacing, to 1e-12, and the gap %.3f = 2m at the edge' % (bands[100, 1] - bands[100, 0]))

    # ======================================================================= the Hubbard term and its mean field
    cu, cd, nu, nd, Sx, Sy, Sz = site_ops()
    n, mz = nu + nd, nu - nd
    S2 = (Sx @ Sx + Sy @ Sy + Sz @ Sz).real
    hub = nu @ nd
    ok = near(hub, cu.T @ cu @ cd.T @ cd, 1e-14) and near(hub, cu.T @ cd.T @ cd @ cu, 1e-14)
    ok = ok and near(hub, (n @ n - mz @ mz) / 4, 1e-14) and near(hub, n / 2 - 2 / 3 * S2, 1e-14) and near(S2, 0.75 * (n - 2 * hub), 1e-14)
    check('the Hubbard term', ok,
          'U c_up^+ c_up c_dn^+ c_dn of (1.7) and U c_up^+ c_dn^+ c_dn c_up of (5.2) are U n_up n_dn, which is (U/4)(n^2 - m^2) '
          'and (U/2) n - (2U/3) S^2, with S^2 = (3/4)(n - 2 n_up n_dn) = %s, as operators on the four states of a site'
          % np.round(np.diag(S2), 3))

    a, b, U = 0.83, 0.17, 3.7
    hart = U * (a * nd + nu * b - a * b * np.eye(4))
    ident = U / 2 * (a + b) * n - U / 2 * (a - b) * mz - U / 4 * ((a + b) ** 2 - (a - b) ** 2) * np.eye(4)
    lev_up, lev_dn = U * b, U * a                                 # the onsite energy that each spin feels
    m_ = a - b
    gd = geometry.bichain(); gd.dimensionality = 0
    with quiet():
        hz = gd.get_hamiltonian().get_mean_field_hamiltonian(U=4.0, mf="antiferro", mix=0.5)
    transverse = max(np.abs(np.real(hz.get_vev(o))).max() for o in ("mx", "my"))
    ok = near(hart, ident, 1e-13) and near([lev_up, lev_dn], [U / 2 * (a + b) - U / 2 * m_, U / 2 * (a + b) + U / 2 * m_], 1e-13)
    check('the Hartree decoupling', ok and abs((lev_dn - lev_up) - U * m_) < 1e-13 and transverse < 1e-9,
          'U(<n_up> n_dn + n_up <n_dn> - <n_up><n_dn>) = (U/2)<n> n - (U/2) m (n_up - n_dn) - (U/4)(<n>^2 - m^2) as operators, '
          'so the spin sigma level is E + (U/2)<n> - sigma (U/2) m, and the up level is lower by U m = %.3f for <n_up> = %.2f '
          'and <n_dn> = %.2f at U = %.1f, and the dimer of pyqula along z has m_x and m_y below %.0e, so no Fock term'
          % (lev_dn - lev_up, a, b, U, max(transverse, 1e-16)))

    c, nn, hop = dimer_exact()
    rows = []
    for U in (1.0, 4.0):
        m0, orb, e_mf, gp = dimer_hartree(U, 0.3)
        H = hop + U * (nn[0] @ nn[1] + nn[2] @ nn[3])
        vac = np.zeros(16); vac[0] = 1
        psi = (orb[1][0] * c[0].T + orb[1][1] * c[2].T) @ (orb[-1][0] * c[1].T + orb[-1][1] * c[3].T) @ vac
        slater = psi @ H @ psi / (psi @ psi)
        nu_, nd_ = np.abs(orb[1]) ** 2, np.abs(orb[-1]) ** 2
        levels = e_mf + U * np.sum(nu_ * nd_)
        with quiet():
            hm, Eq = gd.get_hamiltonian().get_mean_field_hamiltonian(U=U, mf="antiferro", mix=0.5, return_total_energy=True)
        rows.append((U, slater, e_mf, levels, Eq))
    exact4 = 2.0 - np.sqrt(4.0 + 4.0)
    ok = all(abs(r[1] - r[2]) < 1e-10 and abs(r[4] - r[2]) < 1e-4 for r in rows)
    ok = ok and near([rows[0][2], rows[1][2]], [-1.5, -0.5], 1e-9) and near([rows[0][3], rows[1][3]], [-1.0, 0.0], 1e-9)
    check('the double counting', ok and abs(exact4 + 0.8284) < 1e-4,
          ', '.join('U=%.0f: <H> of the Slater determinant %.4f, levels minus U sum <n_up><n_dn> %.4f, levels alone %.4f, '
                    'pyqula %.4f' % r for r in rows) + ', and the exact %.4f at U=4' % exact4)

    gch = geometry.chain()
    dirs = {}
    for mode in ("ferroZ", "ferroX"):
        with quiet():
            hm = gch.get_hamiltonian().get_mean_field_hamiltonian(U=4.0, mf=mode, filling=0.1, nk=50, mix=0.5)
        vals = [float(np.real(hm.get_vev(op, nk=50)[0])) for op in (None, "mx", "my", "mz")]
        e0 = np.linalg.eigvalsh(hm.get_hk_gen()([0.0, 0, 0]))
        dirs[mode] = (vals, e0[1] - e0[0])
    # the Hartree decoupling of -(2U/3) S^2 as 2<S>.S - <S>^2 with <S> = (0, 0, m/2)
    m_, U = 0.2, 4.0
    op = -2 * U / 3 * (2 * (m_ / 2) * Sz)
    split_s2 = (op[0b10, 0b10] - op[0b01, 0b01]).real              # the dn state minus the up state
    ratio_s2 = split_s2 / (U * m_)
    ok = all(abs(d[1] - 0.8) < 1e-6 for d in dirs.values()) and abs(dirs["ferroZ"][0][0] - 0.2) < 1e-9
    ok = ok and abs(abs(dirs["ferroZ"][0][3]) - 0.2) < 1e-6 and abs(abs(dirs["ferroX"][0][1]) - 0.2) < 1e-6 and abs(dirs["ferroX"][0][3]) < 1e-6
    ok = ok and abs(0.1 * 2 * 8 - 1.6) < 1e-12                      # the electrons of filling=0.1 on the default mesh
    check('the direction of the moment', ok and abs(split_s2 - 2 * U * m_ / 3) < 1e-12,
          'the chain at U=4t with filling=0.1 and nk=50 has n = %.3f per site, ferroZ ends at m_z = %+.3f and ferroX at '
          'm_x = %+.3f, both with the splitting %.3f = U|m|, while the Hartree decoupling of -(2U/3) S^2 gives only '
          '%.3f = (2U/3) m, and nk=8 would hold 1.6 electrons'
          % (dirs["ferroZ"][0][0], dirs["ferroZ"][0][3], dirs["ferroX"][0][1], dirs["ferroZ"][1], split_s2))

    rows = []
    for nfill, U in ((1.0, 1.0), (0.2, 1.0)):
        ns = nfill / 2
        D = 1 / (2 * np.pi * np.sin(np.pi * ns))
        slope = uniform_map(1e-5, U, nfill) / 1e-5
        rows.append((nfill, D, slope, U * D))
    sq = []
    for nk in (240, 480):
        k = 2 * np.pi * np.arange(nk) / nk
        e = -2 * (np.cos(k)[:, None] + np.cos(k)[None, :])
        f = 1 / (np.exp(e / 0.1) + 1)
        sq.append(np.mean(f * (1 - f)) / 0.1)
    with quiet():
        (ee, dd) = geometry.chain().get_hamiltonian().get_dos(energies=np.array([-0.05, 0.0, 0.05]), nk=4000, delta=0.02, write=False)
    ok = all(abs(r[2] / r[3] - 1) < 1e-3 for r in rows) and abs(rows[0][1] - 1 / (2 * np.pi)) < 1e-12 and abs(rows[1][1] - 0.5150) < 1e-4
    ok = ok and abs(sq[0] - sq[1]) < 1e-6 and abs(sq[0] - 0.264) < 5e-4 and abs(dd[1] / 2 - 1 / (2 * np.pi)) < 2e-3
    check('the Stoner criterion', ok,
          ', '.join('n=%.1f: D(E_F) = %.4f per spin and per site, slope of m -> m\' at m=0 %.4f = U D(E_F) %.4f at U=t' % r for r in rows)
          + ', the half-filled square lattice at T=0.1t has -int f\' D = %.4f/t on 240^2 and %.4f/t on 480^2, and pyqula\'s '
          'get_dos of the spinful chain at E=0 is %.4f, twice D' % (sq[0], sq[1], dd[1]))

    # the uniform states of the chain at half filling and at n = 0.2
    km = 2 * np.pi * (np.arange(20000) + 0.5) / 20000
    eps = np.sort(-2 * np.cos(km))
    mesh_e = lambda m: (eps[:int(round(20000 * (1 + m) / 2))].sum() + eps[:int(round(20000 * (1 - m) / 2))].sum()) / 20000
    form_e = -(4 / np.pi) * np.cos(np.pi * 0.3 / 2)
    exists = [uniform_map(1.0, U, 1.0) > 1 - 1e-12 for U in (3.99, 4.01)]
    cross = optimize.brentq(lambda U: uniform_energy(1.0, U) - uniform_energy(0.0, U), 4, 6)
    curv = [(uniform_energy(1e-3, U) + uniform_energy(-1e-3, U) - 2 * uniform_energy(0, U)) / 1e-6 for U in (6.2, 6.36, 5.5)]
    above = uniform_energy(0.0, 5.5) - uniform_energy(1.0, 5.5)
    quartic = uniform_energy(0.2, 2 * np.pi) - uniform_energy(0, 2 * np.pi)
    ex2 = [uniform_map(0.2, U, 0.2) > 0.2 - 1e-9 for U in (1.905, 1.915)]
    cross2 = optimize.brentq(lambda U: uniform_energy(0.2, U, 0.2) - uniform_energy(0.0, U, 0.2), 1.5, 2.5)
    # the semicircular density of states of the widget of Section 6.6, D(0) = 1/(pi t)
    F = lambda x: 0.5 + (np.clip(x, -2, 2) * np.sqrt(4 - np.clip(x, -2, 2) ** 2) / 2 + 2 * np.arcsin(np.clip(x, -2, 2) / 2)) / (2 * np.pi)
    semi = [optimize.brentq(lambda m: F(x * np.pi * m / 2) - F(-x * np.pi * m / 2) - m, 1e-4, 1.0) for x in (1.0001, 1.05)]
    ok = abs(mesh_e(0.3) - form_e) < 1e-6 and exists == [False, True] and abs(cross - 16 / np.pi) < 1e-9
    ok = ok and curv[0] > 0 > curv[1] and curv[2] > 0 and abs(above - 0.102) < 1e-3 and quartic < 0
    ok = ok and ex2 == [False, True] and abs(cross2 - 1.926) < 1e-3 and abs(1 / rows[1][1] - 1.9416) < 1e-4 and semi[0] < 0.05
    check('the uniform states of the chain', ok,
          'E(m) = -(4t/pi) cos(pi m/2) + U(1-m^2)/4 per site, the same as a mesh to 1e-6, with E(0.2) - E(0) = %.4f < 0 at '
          'U = 2 pi t, so the quartic term is negative, the full polarization is a solution from U=4t and lower than the '
          'paramagnet from %.4f = 16t/pi, the curvature at m=0 changes sign at 2 pi t, at 5.5t the paramagnet is locally '
          'stable and %.3f above, at n=0.2 the full polarization is a solution from 1.91t and lower from %.3f, with 1/D = %.4f, '
          'and the semicircle of half width 2t of the widget of Section 6.6 has m = %.3f at U = 1.0001 pi t and %.3f at 1.05 pi t'
          % (quartic, cross, above, cross2, 1 / rows[1][1], semi[0], semi[1]))

    # ======================================================================= the repulsion between neighbors
    T4r = chain_matrix([-1.0] * 3); T4r[0, 3] = T4r[3, 0] = -1.0
    guess = np.array([0.6, 0.4, 0.6, 0.4])
    onsite = 3.0 * (np.roll(guess, 1) + np.roll(guess, -1))
    w, v = np.linalg.eigh(T4r + np.diag(onsite))
    charges = np.sum(np.abs(v[:, :2]) ** 2, axis=1)
    closed = 0.75 + 0.6 / (4 * np.sqrt(4 + 0.36))
    check('the Hartree term of (1.6)', near(onsite, [2.4, 3.6, 2.4, 3.6], 1e-12) and near(charges[:2], [0.8218, 0.1782], 1e-4)
          and abs(charges[0] - closed) < 1e-12,
          'V=3t and the guess 0.6, 0.4 on the ring of four sites give the onsite energies %.1f and %.1f, the levels %s, and '
          'filling the two lowest gives %.4f and %.4f, also 3/4 + Delta/(4 sqrt(4t^2+Delta^2)) with Delta = V(0.6-0.4)'
          % (onsite[0], onsite[1], np.round(w, 3), charges[0], charges[1]))

    ks4 = kring(4000)
    rows = []
    for V in (1.0, 2.0, 3.0):
        d = 0.3
        for i in range(5000):
            # spinless chain, A sees V(n_B + n_B) = V(1 - d), B sees V(1 + d), so the staggered half difference is V d
            new = stagger(V * d, ks4)
            if abs(new - d) < 1e-13:
                break
            d = new
        with quiet():
            hm = geometry.bichain().get_hamiltonian(has_spin=False).get_mean_field_hamiltonian(
                V1=V, mf="CDW", mix=0.5, filling=0.5, nk=100, compute_cross=False, write=False)
        den = np.real(hm.get_vev(operator=None, nk=200))
        rows.append((V, d, chain_m(2 * V)[0], abs(den[0] - den[1]), hm.get_gap(), 2 * V * abs(den[0] - den[1])))
    ok = all(abs(r[1] - r[2]) < 1e-6 and abs(r[3] - r[2]) < 2e-3 and abs(r[4] - r[5]) < 2e-3 for r in rows)
    ok = ok and near([r[1] for r in rows], [0.3404, 0.7690, 0.8923], 1e-4) and abs(rows[2][4] - 5.354) < 5e-3
    check('the charge density wave in Hartree is the antiferromagnet with U = 2V', ok,
          ', '.join('V=%.0f: dn %.4f, m(U=2V) %.4f, pyqula with compute_cross=False %.4f, gap %.3f = 2V dn' % (r[0], r[1], r[2], r[3], r[4]) for r in rows))

    d0, w0 = ring_hartree_cdw(8, 0.0, guess=0.0)
    d3, w3 = ring_hartree_cdw(8, 3.0)
    ok = near(w0[:6], [-2, -np.sqrt(2), -np.sqrt(2), 0, 0, np.sqrt(2)], 1e-12) and near(np.sort(d3)[[0, -1]], [0.0538, 0.9462], 1e-4)
    check('the rings of Figure 1.5', ok and abs(w3[4] - w3[3] - 5.354) < 5e-3,
          'at V=0 the four electrons of eight sites fill %s and one of the pair at 0, and at V=3t the charges are %.4f and %.4f '
          'with the gap %.3f' % (np.round(w0[:3], 3), np.max(d3), np.min(d3), w3[4] - w3[3]))

    rows = []
    for V in (1.0, 2.0, 3.0, 10.0):
        dn, tb = ring_hf_cdw(100, V)
        with quiet():
            hm = geometry.bichain().get_hamiltonian(has_spin=False).get_mean_field_hamiltonian(
                V1=V, mf="CDW", mix=0.5, filling=0.5, nk=100, write=False)
        den = np.real(hm.get_vev(operator=None, nk=200))
        inter = [np.asarray(t.m) for t in hm.get_multicell().hopping if any(t.dir)]
        rows.append((V, np.ptp(dn), np.abs(tb).mean(), np.ptp(tb), abs(den[0] - den[1]), abs(np.asarray(hm.intra)[0, 1]),
                     max(np.abs(x).max() for x in inter), hm.get_gap()))
    ok = all(abs(r[1] - r[4]) < 2e-3 and abs(r[2] - r[5]) < 2e-3 and abs(r[5] - r[6]) < 1e-6 and r[3] < 1e-8 and abs(r[7] - 2 * r[0] * r[4]) < 3e-3 for r in rows)
    ok = ok and near([r[4] for r in rows], [0.168, 0.513, 0.704, 0.962], 1e-3) and near([r[5] for r in rows[:3]], [1.316, 1.570, 1.725], 1e-3)
    try:
        with quiet():
            geometry.bichain().get_hamiltonian().get_mean_field_hamiltonian(V1=1.5, mf="CDW", compute_cross=False, nk=8)
        refused = False
    except TypeError:
        refused = True
    check('the Fock term of (1.6)', ok and refused,
          ', '.join('V=%.0f: dn %.4f and hopping %.4f in pyqula, %.4f and %.4f in a real-space ring of 100 sites' % (r[0], r[4], r[5], r[1], r[2]) for r in rows)
          + ', the same on both bonds and the gap 2V dn, and the spinful call refuses compute_cross with a TypeError')

    L = 8
    c8 = fock(L)
    nf = [x.T @ x for x in c8]
    V, t = 1.3, 1.0
    Hf = -t * sum(c8[i].T @ c8[i + 1] + c8[i + 1].T @ c8[i] for i in range(L - 1)) + V * sum(nf[i] @ nf[i + 1] for i in range(L - 1))
    sx, sy, sz, one = np.array([[0, 1], [1, 0]]) / 2, np.array([[0, -1j], [1j, 0]]) / 2, np.diag([-0.5, 0.5]), np.eye(2)

    def sop(o, i):
        m = np.ones((1, 1))
        for l in reversed(range(L)):
            m = np.kron(m, o if l == i else one)
        return m
    S = [[sop(o, i) for i in range(L)] for o in (sx, sy, sz)]

    def xxz(Jxy, Jz, ends):
        H = sum(Jxy * (S[0][i] @ S[0][i + 1] + S[1][i] @ S[1][i + 1]) + Jz * S[2][i] @ S[2][i + 1] for i in range(L - 1))
        return H + ends * (S[2][0] + S[2][L - 1]) if ends else H
    # n = S_z + 1/2 on every site, the bulk terms V/2 (S_z^i + S_z^(i+1)) give V S_z^tot minus a field V/2 at each end
    Hs = xxz(-2 * t, V, -V / 2) + V * sum(S[2]) + V * (L - 1) / 4 * np.eye(2 ** L)
    spec = np.abs(np.sort(np.linalg.eigvalsh(Hf)) - np.sort(np.linalg.eigvalsh(Hs))).max()
    Stot = [sum(S[a]) for a in range(3)]
    S2t = sum(x @ x for x in Stot)
    rot = np.ones((1, 1))
    for l in reversed(range(L)):
        rot = np.kron(rot, np.diag([1, -1]) if l % 2 else one)
    comm = [np.abs((rot @ xxz(-2 * t, Vz, 0) @ rot) @ S2t - S2t @ (rot @ xxz(-2 * t, Vz, 0) @ rot)).max() for Vz in (2.0, 1.3)]
    check('the exact chain (1.6) is the XXZ chain', spec < 1e-10 and comm[0] < 1e-10 and comm[1] > 0.1,
          'the open chain of 8 sites at V=1.3t has the spectrum of J_xy = 2t, J_z = V with a field at the two ends to %.0e, and '
          'the total S^2 commutes with the XXZ part to %.0e at V=2t and not at 1.3t (%.2f)' % (spec, comm[0], comm[1]))

    # ======================================================================= the order parameters
    gd = geometry.bichain(); gd.dimensionality = 0
    with quiet():
        hm = gd.get_hamiltonian().get_mean_field_hamiltonian(U=9.8, mf="antiferro", mix=0.5)
    m98 = np.real(hm.get_vev("mz"))
    check('m and get_vev("mz")', near(np.abs(m98), np.sqrt(1 - (2 / 9.8) ** 2), 1e-4) and m98[0] < 0 < m98[1],
          'on the dimer at U=9.8t get_vev("mz") is %+.4f and %+.4f, so it is n_up - n_dn = sqrt(1-(2t/U)^2) = %.4f, where '
          '<S_z> would be %.4f, and with the guess "antiferro" it is negative on the first site'
          % (m98[0], m98[1], np.sqrt(1 - (2 / 9.8) ** 2), np.sqrt(1 - (2 / 9.8) ** 2) / 2))

    with quiet():
        haf3 = geometry.bichain().get_hamiltonian().get_mean_field_hamiltonian(U=3.0, mf="antiferro", mix=0.5, nk=100)
        hs4 = haf3.get_supercell(4)
    mom_c, fld_c = np.real(hs4.get_vev("mz", nk=50)), np.real(hs4.extract("mz"))
    check('extract("mz")', near(fld_c, -3.0 * mom_c / 2, 2e-3) and np.all(mom_c[0::2] < -0.62) and abs(fld_c[0] - 0.931) < 2e-3,
          'on get_supercell(4) of the chain at U=3t extract("mz") is %+.4f where get_vev("mz") is %+.4f on the even sites, '
          'so it is (H_upup - H_dndn)/2 = -U m/2, the field and not the moment' % (fld_c[0], mom_c[0]))

    c6 = fock(6)                                                  # a ring of three sites, modes (i up, i dn)
    n6 = [x.T @ x for x in c6]
    ring = [(0, 1), (1, 2), (2, 0)]
    hop6 = -sum(c6[2 * i + s].T @ c6[2 * j + s] + c6[2 * j + s].T @ c6[2 * i + s] for i, j in ring for s in (0, 1))
    Sy6 = sum(-0.5j * (c6[2 * i].T @ c6[2 * i + 1] - c6[2 * i + 1].T @ c6[2 * i]) for i in range(3))
    Sz6 = sum(0.5 * (n6[2 * i] - n6[2 * i + 1]) for i in range(3))
    P = linalg.expm(-1j * np.pi * Sy6)                            # the spin rotation of the time reversal P K
    sy2 = np.array([[0, -1j], [1j, 0]])
    flips = [np.abs((1j * sy2) @ np.conj(s) @ (1j * sy2).conj().T + s).max() for s in (np.array([[0, 1], [1, 0]]), sy2, np.diag([1, -1]))]
    m0op = n6[0] - n6[1]
    ok = max(flips) < 1e-14 and np.abs(P @ np.conj(m0op) @ P.conj().T + m0op).max() < 1e-12
    for U in (4.0, -4.0):
        H6 = hop6 + U * sum(n6[2 * i] @ n6[2 * i + 1] for i in range(3))
        ok = ok and np.abs(np.imag(H6)).max() == 0 and np.abs(H6 @ Sz6 - Sz6 @ H6).max() < 1e-12
        ok = ok and np.abs(P @ np.conj(H6) @ P.conj().T - H6).max() < 1e-10
    check('time reversal', ok,
          'i sigma_y K sends sigma_x, sigma_y and sigma_z to minus themselves, so it exchanges n_up and n_dn and changes the sign '
          'of m, and (1.7) on a ring of three sites is real, commutes with S_z and with the time reversal for U = +4t and -4t')

    Ua = 3.0
    dBCS = optimize.brentq(lambda d: Ua * np.mean(d / (2 * np.sqrt((2 * np.cos(ks4)) ** 2 + d ** 2))) - d, 1e-6, 10)
    pair = np.mean(dBCS / (2 * np.sqrt((2 * np.cos(ks4)) ** 2 + dBCS ** 2)))
    u_, v_ = 0.6, 0.8                                             # u|0> + v c_up^+ c_dn^+|0> on one site
    st = u_ * np.eye(4)[0] + v_ * (cu.T @ cd.T @ np.eye(4)[0])
    dnup, updn = st @ cd @ cu @ st, st @ cu @ cd @ st
    hn = geometry.chain().get_hamiltonian(); hn.setup_nambu_spinor()
    with quiet():
        hsw = hn.get_mean_field_hamiltonian(U=-Ua, mf="swave", mix=0.5, nk=100)
    sw = np.abs(np.asarray(hsw.extract("swave"))).max()
    gsw = hsw.get_hk_gen()
    gap_sw = 2 * min(np.abs(np.linalg.eigvalsh(gsw([k, 0, 0]))).min() for k in np.linspace(0, 1, 401))
    ok = abs(dnup + updn) < 1e-14 and abs(dnup) > 0.4 and abs(dBCS - 0.9309) < 1e-3 and abs(pair - 0.3103) < 1e-3
    check('the pairing amplitude', ok and abs(sw - dBCS) < 2e-3 and abs(gap_sw - 2 * dBCS) < 3e-3 and abs(dBCS - Ua * chain_m(Ua)[0] / 2) < 1e-6,
          '<c_dn c_up> = %+.2f = -<c_up c_dn> on one site, and on the chain at U=-3t the gap equation gives |Delta| = |U| '
          '|<c_dn c_up>| = %.4f with |<c_dn c_up>| = %.4f, pyqula\'s extract("swave") has the modulus %.4f, and the gap of the '
          'BdG bands is %.4f = 2|Delta|' % (dnup, dBCS, pair, sw, gap_sw))

    phi = 0.37
    Nn = sum(x.T @ x for x in c2)
    Ug = linalg.expm(-1j * phi * Nn)
    tr = lambda o: Ug @ o @ Ug.conj().T
    ok = near(tr(c2[0]), np.exp(1j * phi) * c2[0], 1e-13) and near(tr(c2[0].T @ c2[1]), c2[0].T @ c2[1], 1e-13)
    ok = ok and near(tr(c2[0] @ c2[1]), np.exp(2j * phi) * c2[0] @ c2[1], 1e-13) and near(tr(c2[0].T @ c2[1].T), np.exp(-2j * phi) * c2[0].T @ c2[1].T, 1e-13)
    check('the gauge transformation (1.10)', ok and abs(np.exp(2j * np.pi / 2) + 1) < 1e-15,
          'e^{-i phi N} c e^{i phi N} = e^{i phi} c, c^+ c does not change, c_i c_j gets e^{2 i phi}, c_i^+ c_j^+ gets '
          'e^{-2 i phi} as in (5.5), and phi = pi/2 gives -1')

    Hp = -0.3 * n + 0.8 * (cu.T @ cd.T + cd @ cu)
    w, v = np.linalg.eigh(Hp)
    par = np.diag((-1.0) ** np.round(np.diag(n)))
    var = v[:, 0] @ n @ n @ v[:, 0] - (v[:, 0] @ n @ v[:, 0]) ** 2
    ok = np.abs(Hp @ par - par @ Hp).max() < 1e-14 and np.abs(Hp @ n - n @ Hp).max() > 0.5 and v[:, 0] @ par @ v[:, 0] > 1 - 1e-12
    check('a pairing term keeps the parity', ok and abs(var - 0.877) < 1e-3,
          '-0.3 n + 0.8 (c_up^+ c_dn^+ + h.c.) commutes with (-1)^N and not with N, its ground state is even, and N has the variance %.3f' % var)

    # ======================================================================= the models of the pages
    rows, ok = [], True
    for U in (0.0, 1.0, 1.5, 2.1, 3.0, 4.0, 8.0, 9.8):
        m0, orb, e_mf, gp = dimer_hartree(U, 0.3)
        mf = np.sqrt(max(0, 1 - 4 / U ** 2)) if U > 0 else 0.0
        ef = -2 + U / 2 if U <= 2 else -2 / U
        gf = max(2.0, U)
        with quiet():
            hm, Eq = gd.get_hamiltonian().get_mean_field_hamiltonian(U=U, mf="antiferro", mix=0.5, return_total_energy=True)
        mq = abs(np.real(hm.get_vev("mz"))[0])
        ok = ok and abs(abs(m0) - mf) < 1e-6 and abs(e_mf - ef) < 1e-9 and abs(gp - gf) < 1e-6
        ok = ok and abs(mq - mf) < 1e-3 and abs(Eq - ef) < 1e-4 and abs(hm.get_gap() - gf) < 1e-3
        rows.append((U, abs(m0)))
    check('the Hubbard dimer in mean field', ok and near([r[1] for r in rows[3:7]], [0.3049, 0.7454, 0.8660, 0.9682], 1e-4),
          'm = 0 up to U=2t and sqrt(1-4t^2/U^2) above, ' + ', '.join('%.4f at %.1f' % (r[1], r[0]) for r in rows[3:7])
          + ', the energy -2t+U/2 and then exactly -2t^2/U, the gap max(2t, U), from a numpy loop to 1e-12, and from pyqula '
          'to 1e-4 in the energy and to 1e-3 in m and the gap, the tolerance of its loop next to U=2t, for U from 0 to 9.8t')

    rows = []
    for U in (4.0, 40.0):
        H = hop + U * (nn[0] @ nn[1] + nn[2] @ nn[3])
        Nd = sum(nn)
        sel = np.round(np.diag(Nd)) == 2
        w, v = np.linalg.eigh(H[np.ix_(sel, sel)])
        gs = v[:, 0]
        mom = gs @ (nn[0] - nn[1])[np.ix_(sel, sel)] @ gs
        rows.append((U, w[0], U / 2 - np.sqrt(U ** 2 / 4 + 4), mom))
    hf = 1e-5
    H = hop + 4.0 * (nn[0] @ nn[1] + nn[2] @ nn[3]) - hf * (nn[0] - nn[1]) + hf * (nn[2] - nn[3])
    sel = np.round(np.diag(sum(nn))) == 2
    w, v = np.linalg.eigh(H[np.ix_(sel, sel)])
    chi = v[:, 0] @ (nn[0] - nn[1])[np.ix_(sel, sel)] @ v[:, 0] / hf
    ok = all(abs(r[1] - r[2]) < 1e-12 and abs(r[3]) < 1e-12 for r in rows) and abs(rows[0][1] + 0.8284) < 1e-4
    check('the exact dimer', ok and abs(rows[1][1] / (-0.1) - 0.998) < 1e-3 and abs(chi - 4.12) < 0.01,
          'E0 = U/2 - sqrt(U^2/4+4t^2) is %.4f at U=4t and %.4f = %.3f (-4t^2/U) at U=40t, the singlet has m = 0, and a staggered '
          'field h at U=4t gives m = %.2f h, which goes to zero with h' % (rows[0][1], rows[1][1], rows[1][1] / -0.1, chi))

    rows = []
    for U in (1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 16.0):
        m, delta = chain_m(U)
        rows.append((U, m, delta))
    mesh_ok = all(abs(loop(U, kring(20000)) - chain_m(U)[0]) < 1e-5 for U in (2.0, 4.0, 6.0))
    small = 16 * np.exp(-2 * np.pi)
    L = 120
    T120 = chain_matrix([-1.0] * (L - 1)); T120[0, -1] = T120[-1, 0] = -1.0
    ms = 0.3 * (-1) ** np.arange(L)
    for i in range(3000):
        dens = {}
        for s in (1, -1):
            w, v = np.linalg.eigh(T120 + np.diag(3.0 / 2 * (1 - s * ms)))
            dens[s] = np.sum(np.abs(v[:, :L // 2]) ** 2, axis=1)
        new = dens[1] - dens[-1]
        if np.abs(new - ms).max() < 1e-12:
            break
        ms = 0.5 * new + 0.5 * ms
    with quiet():
        h3 = geometry.bichain().get_hamiltonian().get_mean_field_hamiltonian(U=3.0, mf="antiferro", mix=0.5, nk=100)
    m3q = abs(np.real(h3.get_vev("mz", nk=200))[0])
    vals = [r[1] for r in rows]
    ok = near(vals, [0.0299, 0.3404, 0.6206, 0.7690, 0.8923, 0.9385, 0.9844], 1e-4) and mesh_ok and abs(small / vals[0] - 1) < 3e-3
    ok = ok and abs(np.abs(ms).mean() - 0.6206) < 1e-4 and abs(m3q - 0.6206) < 2e-4 and abs(h3.get_gap() - 3 * vals[2]) < 2e-3
    check('the half-filled Hubbard chain', ok,
          'no threshold, m = %s at U = 1, 2, 3, 4, 6, 8, 16 from the gap equation with the elliptic integral and from a mesh, '
          '(16t/U) exp(-2 pi t/U) = %.4f at U=t, the ring of 120 sites has |m| = %.4f at 3t, and pyqula %.4f with the gap %.4f = U m'
          % (' '.join('%.4f' % x for x in vals), small, np.abs(ms).mean(), m3q, h3.get_gap()))

    fhc = lambda k1, k2: np.abs(1 + np.exp(1j * k1) + np.exp(1j * k2))
    inv = []
    for nk in (600, 1200):
        k = 2 * np.pi * (np.arange(nk) + 0.5) / nk
        inv.append(np.mean(1 / fhc(k[:, None], k[None, :])))
    Uc = [2 / x for x in inv]
    Uc_lim = 2 * Uc[1] - Uc[0]                                     # the error of a midpoint mesh falls as 1/nk here
    hh = geometry.honeycomb_lattice().get_hamiltonian()
    with quiet():
        hh3 = hh.get_mean_field_hamiltonian(U=3.0, mf="antiferro", mix=0.9, nk=20)
    mh = abs(np.real(hh3.get_vev("mz", nk=20))[0])
    k20 = 2 * np.pi * np.arange(20) / 20
    K1, K2 = np.meshgrid(k20, k20, indexing='ij')
    m = 0.3
    for i in range(5000):
        new = np.mean((3.0 * m / 2) / np.sqrt((3.0 * m / 2) ** 2 + fhc(K1, K2) ** 2))
        if abs(new - m) < 1e-13:
            break
        m = new
    genh = hh3.get_hk_gen()
    eK = np.linalg.eigvalsh(genh([1 / 3, 1 / 3, 0]))
    ok = 2.229 < Uc_lim < 2.234 and abs(mh - m) < 1e-4 and abs(mh - 0.444) < 1e-3 and abs(hh3.get_gap() - 3 * mh) < 1e-3
    check('the honeycomb lattice', ok and abs(np.min(np.abs(eK)) * 2 - 3 * mh) < 1e-3,
          'U_c = 2/<1/|f_k|> is %.4f and %.4f on midpoint meshes of 600^2 and 1200^2, so %.3f t, and at U=3t pyqula with nk=20 '
          'gives m = %.4f, a numpy loop on the same mesh %.4f, and the gap %.4f = U m, at K' % (Uc[0], Uc[1], Uc_lim, mh, m, hh3.get_gap()))

    rows = []
    for U in (1.0, 3.0, 6.0, 10.0):
        m, delta = chain_m(U)
        E_af = -2 * np.mean(np.sqrt(delta ** 2 + (2 * np.cos(ks4 / 2)) ** 2)) + U / 2 + U * m ** 2 / 2
        E_pm, E_fm = 2 * uniform_energy(0.0, U), (2 * uniform_energy(1.0, U) if U >= 4 else np.nan)
        rows.append((U, E_af, E_pm, E_fm))
    with quiet():
        _, Eq6 = geometry.bichain().get_hamiltonian().get_mean_field_hamiltonian(U=6.0, mf="antiferro", mix=0.5, return_total_energy=True)
    ok = all(r[1] < r[2] and (np.isnan(r[3]) or r[1] < r[3]) for r in rows) and abs(rows[2][1] + 0.648) < 1e-3 and abs(Eq6 - rows[2][1]) < 1e-3
    check('the antiferromagnet is the lowest state of the half-filled chain', ok and abs(rows[2][2] - 0.454) < 1e-3 and abs(rows[2][3]) < 1e-12,
          ', '.join('U=%.0f: %.3f against the paramagnet %.3f and the full ferromagnet %.3f' % r for r in rows)
          + ' per cell of two sites, and pyqula %.3f at U=6t' % Eq6)

    d_neg = chain_m(3.0)[0]
    grid = np.linspace(-1, 1, 201)
    mapped = np.array([-np.sign(x) * stagger(3.0 * abs(x) / 2, ks4) for x in grid])  # m -> F(U m/2) with U = -3t
    only0 = np.all(mapped[grid != 0] * grid[grid != 0] < 0)
    with quiet():
        hc = geometry.bichain().get_hamiltonian().get_mean_field_hamiltonian(U=-3.0, mf="CDW", mix=0.5, nk=50)
    dq = np.sort(np.real(hc.get_vev(operator=None, nk=50)))
    ok = only0 and near(dq, [1 - d_neg, 1 + d_neg], 2e-3) and abs(hc.get_gap() - 3 * d_neg) < 2e-3 and abs(2 * dBCS - 3 * d_neg) < 1e-6
    check('the attractive chain at half filling', ok,
          'at U=-3t the Hartree map of m has the opposite sign of m everywhere, so m = 0 is its only fixed point, the charge '
          'density wave has the charges %.3f and %.3f in pyqula with the gap %.4f, and the s-wave state has 2|Delta| = %.4f, '
          'the gap U m = %.4f of the antiferromagnet at U = +3t' % (dq[0], dq[1], hc.get_gap(), 2 * dBCS, 3 * d_neg))

    Fd = lambda d: np.mean(d / (2 * np.sqrt((2 * np.cos(ks4)) ** 2 + d ** 2)))
    dgrid = np.linspace(-1, 1, 201)
    rhs = np.array([-3.0 * Fd(x) for x in dgrid])
    check('no pairing for a repulsive U', np.all(rhs[dgrid != 0] * dgrid[dgrid != 0] < 0),
          'the gap equation is Delta = -U F(Delta), F = <Delta/2E> has the sign of Delta, so at U=3t the right side has the '
          'opposite sign of Delta for every Delta from -1 to 1 and Delta = 0 is the only solution')

    zero = dimer_hartree(4.0, 0.0)
    plus, minus = dimer_hartree(4.0, 1e-3), dimer_hartree(4.0, -1e-3)
    dies, attr = dimer_hartree(1.0, 0.1), dimer_hartree(-4.0, 0.5)
    fld1, fld4 = dimer_hartree(1.0, 0.0, b=1e-3), dimer_hartree(4.0, 0.0, b=1e-3)
    out = []
    for U in (1.0, 4.0):
        h = gd.get_hamiltonian(); h.add_antiferromagnetism(1e-3)
        with quiet():
            hm = h.get_mean_field_hamiltonian(U=U, mf="antiferro", mix=0.5)
        out.append(abs(np.real(hm.get_vev("mz"))[0]))
    ok = zero[0] == 0 and abs(plus[0] - np.sqrt(0.75)) < 1e-9 and abs(minus[0] + np.sqrt(0.75)) < 1e-9 and abs(plus[2] - minus[2]) < 1e-12
    ok = ok and abs(dies[0]) < 1e-9 and abs(attr[0]) < 1e-9 and abs(abs(fld1[0]) - 0.002) < 2e-6 and abs(abs(fld4[0]) - 0.866) < 1e-3
    check('a seed picks the state', ok and abs(out[0] - 0.002) < 1e-4 and abs(out[1] - 0.866) < 1e-3,
          'on the dimer a loop from m = 0 stays at %.0f, the seeds +1e-3 and -1e-3 at U=4t end at %+.4f and %+.4f with the '
          'energy %.4f and %.4f, at U=t the seed dies (%.0e), at U=-4t the seed 0.5 ends at %.0e, and a field b = 1e-3 that '
          'stays gives |m| = %.5f = b/(1-U/2t) at U=t and %.4f at U=4t, and %.4f and %.4f in pyqula with add_antiferromagnetism'
          % (zero[0], plus[0], minus[0], plus[2], minus[2], abs(dies[0]), abs(attr[0]), abs(fld1[0]), abs(fld4[0]), out[0], out[1]))

    rows = []
    for gg in (0.3, 0.5):
        for L in (8, 12):
            dff = ising_free_fermion_gap(L, gg)
            rows.append((gg, L, dff / (2 * (1 - gg ** 2) * gg ** L)))
    ed = [ising_ed(L, gg) for L in (8, 10) for gg in (0.3, 0.5)]
    ff = [ising_free_fermion_gap(L, gg) for L in (8, 10) for gg in (0.3, 0.5)]
    ok = all(abs(r[2] - 1) < 3e-4 for r in rows) and all(abs((e[0][1] - e[0][0]) / f - 1) < 1e-6 and e[1] > 1 - 1e-9 for e, f in zip(ed, ff))
    check('the quantum Ising chain', ok,
          'exact diagonalization and the free fermions agree on the splitting for L=8 and 10, the ground state is even under '
          'the flip of all spins, and Delta/(2J(1-(g/J)^2)(g/J)^L) is ' + ', '.join('%.4f at g=%.1fJ, L=%d' % (r[2], r[0], r[1]) for r in rows))

    sp = []
    for npts in (1200, 2400):
        x = np.linspace(-3, 3, npts + 2)[1:-1]
        dx = x[1] - x[0]
        w = linalg.eigh_tridiagonal(2 / dx ** 2 + 8 * (x ** 2 - 1) ** 2, np.full(npts - 1, -1 / dx ** 2), select='i', select_range=(0, 1))[0]
        sp.append(w[1] - w[0])
    check('the double well', abs(sp[0] - sp[1]) < 1e-4 and abs(sp[1] - 0.925) < 1e-3,
          '-psi\'\' + 8(x^2-1)^2 psi has 2 Delta = %.4f with 1200 points and %.4f with 2400' % (sp[0], sp[1]))

    # ======================================================================= pyqula
    hd = gd.get_hamiltonian()
    lev = np.sort(np.real(hd.get_bands()[1]))
    lev0 = np.sort(np.real(gd.get_hamiltonian(has_spin=False).get_bands()[1]))
    check('bichain and the dimer', near(lev, [-1, -1, 1, 1], 1e-12) and near(lev0, [-1, 1], 1e-12) and abs(hd.get_gap() - 2) < 1e-9
          and abs(np.asarray(geometry.bichain().get_hamiltonian(has_spin=False).intra)[0, 1] - 1) < 1e-12,
          'bichain has two sites and the hopping +1, the dimer of the notebook with dimensionality=0 has the levels %s, %s with '
          'has_spin=False, and get_gap() is %.3f at U=0' % (np.round(lev, 3), np.round(lev0, 3), hd.get_gap()))

    with quiet():
        hm4 = gd.get_hamiltonian().get_mean_field_hamiltonian(U=4.0, mf="antiferro", mix=0.5)
    m4 = np.real(hm4.get_vev("mz"))
    diag = np.real(np.diag(np.asarray(hm4.intra)))
    expect = np.array([-s * 4.0 * m4[i] / 2 for i in range(2) for s in (1, -1)])
    den3 = np.real(h3.get_vev(operator=None, nk=200))
    try:
        with quiet():
            geometry.bichain().get_hamiltonian().get_mean_field_hamiltonian(U=3.0, mf="antiferro", maxite=2, nk=8)
        raised = None
    except Exception as err:
        raised = type(err).__name__
    with quiet():
        hl = geometry.bichain().get_hamiltonian(has_spin=False).get_mean_field_hamiltonian(V1=1.0, mf="CDW", mix=0.5, nk=8, write=False)
    cell = np.sum(np.real(hl.get_vev(operator=None, nk=8)))
    dense = lambda m: np.asarray(m.todense() if hasattr(m, 'todense') else m)
    on_c = np.real(np.diag(dense(hc.intra)))                 # the charge density wave of the attractive chain above
    n_c = np.real(hc.get_vev(operator=None, nk=50))
    step_c = on_c[0] - on_c[2]
    xs = np.arange(60)                                       # the Kohn-Sham toy of the sheet of Session 10
    vext = -2 * np.exp(-((xs - 29.5) / 7) ** 2)
    htoy = geometry.chain().get_hamiltonian(tij=[-1.]).set_finite_system(n=60)
    htoy.add_onsite(vext)
    with quiet():
        hmt = htoy.get_mean_field_hamiltonian(U=4., filling=40 / 120, mix=0.3, maxerror=1e-8, constrains=['no_magnetism'])
    n_t = np.real(hmt.get_vev(operator=None))
    c_t = np.real(np.diag(dense(hmt.intra)))[0::2] - vext - 2 * n_t
    lev_t = np.linalg.eigvalsh(dense(geometry.chain().get_hamiltonian(tij=[-1.], has_spin=False).set_finite_system(n=60).intra)
                               + np.diag(vext + 2 * n_t))
    ok = near(diag, expect, 1e-4) and near(den3, 1.0, 1e-6) and abs(cell - 1) < 1e-9 and abs(dirs["ferroZ"][0][0] - 0.2) < 1e-9
    ok = ok and near(on_c[[0, 2]], on_c[[1, 3]], 1e-9) and abs(step_c - (-3.0) * (n_c[0] - n_c[1]) / 2) < 1e-3
    ok = ok and abs(abs(step_c) - 1.862) < 1e-3 and np.ptp(c_t) < 1e-9 and abs(c_t.mean() - 0.0477) < 5e-4
    ok = ok and abs(c_t.mean() + (lev_t[19] + lev_t[20]) / 2) < 1e-6
    check('the mean-field call', ok and raised == 'MeanFieldConvergenceError',
          'the onsite energies of the dimer at U=4t are %s = -sigma U m_i/2 with no uniform part, on the attractive chain at '
          'U=-3t the two sites differ by %.4f = U(n0-n1)/2, the toy of Session 10 has v_ext + 2 n_i + %.4f, minus the middle '
          'of the gap of its levels, the default filling=0.5 holds '
          '%.4f electrons on each site of the spinful chain and %.4f in a cell of two sites of the spinless one, filling=0.1 '
          'holds %.3f per site, and maxite=2 raises %s' % (np.round(diag, 4), abs(step_c), c_t.mean(), den3[0], cell,
                                                           dirs["ferroZ"][0][0], raised))

    rows = []
    for U in (1.0, 2.0, 3.0):
        mloop = loop(U, kring(8), mix=0.9)
        with quiet():
            hm = geometry.bichain().get_hamiltonian().get_mean_field_hamiltonian(U=U, mf="antiferro", mix=0.9)
        rows.append((U, mloop, abs(np.real(hm.get_vev("mz", nk=8))[0]), abs(np.real(hm.get_vev("mz"))[0]),
                     stagger(U * mloop / 2, kring(30)), chain_m(U)[0]))
    cdw = []
    for cc in (False, True):
        with quiet():
            hm = geometry.bichain().get_hamiltonian(has_spin=False).get_mean_field_hamiltonian(
                V1=1.0, mf="CDW", mix=0.5, filling=0.5, compute_cross=cc, write=False)
        d8, d30 = np.real(hm.get_vev(operator=None, nk=8)), np.real(hm.get_vev(operator=None))
        cdw.append((abs(d8[0] - d8[1]), abs(d30[0] - d30[1])))
    ok = all(abs(r[1] - r[2]) < 2e-4 and abs(r[3] - r[4]) < 2e-4 for r in rows)
    ok = ok and near([r[1] for r in rows], [0.192, 0.367, 0.621], 1e-3) and near([r[3] for r in rows], [0.138, 0.358, 0.621], 1e-3)
    ok = ok and abs(cdw[0][0] - rows[1][1]) < 2e-4 and abs(cdw[0][1] - rows[1][3]) < 2e-4 and near(cdw[1], [0.263, 0.235], 1e-3)
    check('the mesh of the loop and the mesh of get_vev', ok,
          ', '.join('U=%.0f: the loop on 8 cells %.4f (pyqula %.4f), get_vev() on 30 cells %.4f (numpy %.4f), converged %.4f' % r for r in rows)
          + ', and the Hartree charge density wave at V=t is %.4f and %.4f, with the Fock term %.4f and %.4f' % (cdw[0] + cdw[1]))

    h0 = geometry.bichain().get_hamiltonian(has_spin=False)
    h0.add_sublattice_imbalance(0.1)
    with quiet():
        hm = h0.get_mean_field_hamiltonian(V1=0.0, mf="CDW", mix=0.5, filling=0.5, write=False)
    dd = np.real(hm.get_vev(operator=None))
    seeds = [stagger(s, kring(4000)) for s in (0.1, 0.01, 0.001)]
    cell_src, _ = cell_after('## Symmetry breaking in the spinless fermionic chain')
    ok = abs(abs(dd[0] - dd[1]) - stagger(0.1, kring(30))) < 1e-4 and abs(stagger(0.1, kring(8)) - 0.1948) < 1e-4
    ok = ok and near(seeds, [0.1394, 0.0213, 0.0029], 1e-4) and 'get_vev(operator=None)' in cell_src and 'cdw = 0.' in cell_src
    check('the cell of the notebook with cdw=0.1', ok,
          'at V=0 the cell prints %.4f, the sum on 30 cells of get_vev, where 8 cells give %.4f and the converged value is %.4f, '
          'and the imbalance goes to zero with the seed, %.4f and %.4f for 0.01 and 0.001'
          % (abs(dd[0] - dd[1]), stagger(0.1, kring(8)), seeds[0], seeds[1], seeds[2]))

    hs = geometry.bichain().get_hamiltonian(has_spin=False)
    hsp = geometry.bichain().get_hamiltonian()
    gC = np.real(np.diag(np.asarray(meanfield.guess(hs, "CDW"))))
    gF = np.real(np.diag(np.asarray(meanfield.guess(hsp, "ferro"))))
    gA = np.real(np.diag(np.asarray(meanfield.guess(hsp, "antiferro"))))
    ha = geometry.bichain().get_hamiltonian(); ha.add_antiferromagnetism(0.1)
    sub = os.path.join(os.getcwd(), 'mfpkl'); os.makedirs(sub)
    here = os.getcwd(); os.chdir(sub)
    try:
        with quiet():
            first = hs.get_mean_field_hamiltonian(V1=3.0, mf="CDW", mix=0.5, filling=0.5, nk=20)
        pkl = os.path.exists('MF.pkl')
        try:
            with quiet():
                again = hs.get_mean_field_hamiltonian(V1=3.0, mf=None, mix=0.5, filling=0.5, nk=20, maxite=3)
            restart = abs(np.ptp(np.real(again.get_vev(operator=None, nk=20))) - np.ptp(np.real(first.get_vev(operator=None, nk=20)))) < 1e-4
        except Exception:
            restart = False
    finally:
        os.chdir(here)
    ok = near(gC, [1, -1], 1e-12) and near(gF, [0.1, -0.1, 0.1, -0.1], 1e-12) and near(gA, [0.1, -0.1, -0.1, 0.1], 1e-12)
    check('the guesses', ok and near(np.real(np.diag(np.asarray(ha.intra))), gA, 1e-12) and restart and pkl,
          '"ferro" is the onsite %s on (1 up, 1 dn, 2 up, 2 dn), "antiferro" is %s, the same as add_antiferromagnetism(0.1), '
          '"CDW" is %s, the sublattice index, and with mf=None the spinless loop starts from the MF.pkl that the last call left, '
          'converging in 3 steps' % (gF, gA, gC))

    with quiet():
        hf6, Ef6 = geometry.bichain().get_hamiltonian().get_mean_field_hamiltonian(U=6.0, mf="ferro", mix=0.9, return_total_energy=True)
        hs6 = hf6.get_supercell(4)
    fld6 = np.real(hs6.extract("mz"))
    arrows = fld6 / np.max(np.abs(fld6))
    # the same loop in numpy: a uniform field on the 8 cells of the mesh, 16 band states per spin at half filling
    eb = np.concatenate([np.linalg.eigvalsh(np.array([[0, 1 + np.exp(-1j * k)], [1 + np.exp(1j * k), 0]])) for k in kring(8)])
    field = 0.1
    for i in range(200):
        occ = np.argsort(np.concatenate([eb - field, eb + field]), kind='stable')[:16]
        m8 = (2 * np.sum(occ < 16) - 16) / 16
        if abs(6.0 * m8 / 2 - field) < 1e-14:
            break
        field = 6.0 * m8 / 2
    allE = np.sort(np.concatenate([eb - field, eb + field]))
    E8 = allE[:16].sum() / 8 + 6.0 / 2 + 6.0 * m8 ** 2 / 2
    e30 = np.concatenate([np.linalg.eigvalsh(np.array([[0, 1 + np.exp(-1j * k)], [1 + np.exp(1j * k), 0]])) for k in kring(30)])
    o30 = np.argsort(np.concatenate([e30 - field, e30 + field]), kind='stable')[:60]
    m30 = (2 * np.sum(o30 < 60) - 60) / 60
    src18, _ = cell_after('## Gap opening of the Hubbard model in a chain')
    gaps = []
    for U in np.linspace(0., 4.0, 40):
        with quiet():
            gaps.append(geometry.bichain().get_hamiltonian().get_mean_field_hamiltonian(U=U, mf="ferro", mix=0.9).get_gap())
    strong = []
    for U in (6.0, 3.0):
        hh_ = geometry.bichain().get_hamiltonian()
        with quiet():
            hF, EF = hh_.get_mean_field_hamiltonian(U=U, mf=meanfield.guess(hh_, "ferro", fun=3.0), mix=0.9, nk=40, return_total_energy=True)
        strong.append((np.abs(np.real(hF.get_vev("mz", nk=40))).min(), hF.get_gap(), EF))
    ok = abs(m8 - 0.125) < 1e-12 and abs(fld6[0] - 6.0 / 16) < 1e-6 and np.allclose(arrows, 1) and hf6.get_gap() < 1e-6
    ok = ok and abs(Ef6 - E8) < 1e-4 and abs(abs(np.real(hf6.get_vev("mz"))[0]) - m30) < 1e-6 and abs(m30 - 0.1) < 1e-12
    ok = ok and max(gaps) < 1e-9 and '#    h = h0.get_mean_field_hamiltonian(U=U,mf="ferro",mix=0.9)' in src18
    ok = ok and abs(strong[0][0] - 1) < 1e-6 and abs(strong[0][1] - 2) < 1e-6 and abs(strong[0][2]) < 1e-6 and strong[1][0] < 0.5
    check('the ferromagnetic guess of the notebook', ok,
          'at U=6t with nk=8 it ends at m = %.4f, one k-point of eight, with the field %.4f = U/16, no gap and the energy %.4f per '
          'cell (numpy %.4f), get_vev("mz") reads %.4f on its 30 cells, and the arrows of cell 12 are all %.0f, the commented '
          'line of cell 18 gives the largest gap %.0e for its 40 values of U, and a strong seed gives m = %.3f, the gap %.3f = U - 4t '
          'and the energy %.3f at U=6t and falls back to |m| = %.3f at U=3t'
          % (m8, fld6[0], Ef6, E8, abs(np.real(hf6.get_vev("mz"))[0]), arrows[0], max(gaps), strong[0][0], strong[0][1], strong[0][2], strong[1][0]))

    Ucm = {}
    for nk in (10, 20):
        k = 2 * np.pi * np.arange(nk) / nk
        Ucm[nk] = 2 / np.mean(1 / fhc(k[:, None], k[None, :]))
    k30 = 2 * np.pi * np.arange(30) / 30
    F30 = fhc(k30[:, None], k30[None, :])
    m30h = optimize.brentq(lambda d: 2.0 / 2 * np.mean(1 / np.sqrt(d ** 2 + F30 ** 2)) - 1, 1e-8, 5) * 2 / 2.0
    k10 = 2 * np.pi * np.arange(10) / 10
    F10 = fhc(k10[:, None], k10[None, :])
    m10 = optimize.brentq(lambda d: 2.4 / 2 * np.mean(1 / np.sqrt(d ** 2 + F10 ** 2)) - 1, 1e-8, 5) * 2 / 2.4
    q = []
    for U in (2.3, 2.4):
        with quiet():
            q.append(abs(np.real(hh.get_mean_field_hamiltonian(U=U, mf="antiferro", mix=0.9, nk=10).get_vev("mz", nk=10))[0]))
    src21, _ = cell_after('## Gap opening in the Hubbard model on the honeycomb lattice')
    ok = abs(Ucm[10] - 2.375) < 1e-3 and abs(Ucm[20] - 2.290) < 1e-3 and abs(m30h - 0.0150) < 2e-4 and q[0] < 3e-3 and abs(q[1] - m10) < 3e-3
    check('the honeycomb lattice in pyqula', ok and 'nk=10' in src21 and 'honeycomb_lattice()' in src21,
          'the 10 x 10 mesh of the notebook, which does not hold K, moves the threshold to %.3f and the 20 x 20 mesh to %.3f, '
          'pyqula with nk=10 and mix=0.9 gives |m| = %.0e at U=2.3t and %.4f at 2.4t, where the converged loop on the same mesh '
          'gives %.4f, so the default tolerance stops it early next to the threshold, and a 30 x 30 '
          'mesh holds K and gives m = %.4f already at U=2t' % (Ucm[10], Ucm[20], q[0], q[1], m10, m30h))

    sub = os.path.join(os.getcwd(), 'files'); os.makedirs(sub)
    os.chdir(sub)
    try:
        with quiet():
            hs.get_mean_field_hamiltonian(V1=1.0, mf="CDW", mix=0.5, filling=0.5, nk=8)
            hs.get_bands()
            hs.get_dos(energies=np.linspace(-1, 1, 5), nk=10)
        written = sorted(os.listdir('.'))
        for f in written:
            os.remove(f)
        with quiet():
            hs.get_mean_field_hamiltonian(V1=1.0, mf="CDW", mix=0.5, filling=0.5, nk=8, write=False)
            hs.get_dos(energies=np.linspace(-1, 1, 5), nk=10, write=False)
            geometry.bichain().get_hamiltonian().get_mean_field_hamiltonian(U=3.0, mf="antiferro", nk=8)
        clean = sorted(os.listdir('.'))
    finally:
        os.chdir(here)
    check('the files that pyqula writes', {'MF.pkl', 'BANDS.OUT', 'DOS.OUT'} <= set(written) and clean == [],
          'the spinless mean field, get_bands and get_dos write %s, and with write=False and the spinful mean field nothing' % written)

    src15, md14 = cell_after('## The interacting Hubbard dimer')
    Us = np.linspace(0., 10., 50)
    mzs = []
    for U in Us[:12]:
        with quiet():
            hm = gd.get_hamiltonian().get_mean_field_hamiltonian(U=U, mf="antiferro", mix=0.9)
        mzs.append(abs(np.real(hm.get_vev("mz"))[1]))
    with quiet():
        r19 = abs(np.real(gd.get_hamiltonian().get_mean_field_hamiltonian(U=1.9, mf="antiferro", mix=0.9).get_vev("mz"))[1])
    first = Us[next(i for i, x in enumerate(mzs) if x > 0.01)]
    ok = 'np.linspace(0.,10.,50)' in src15 and abs(first - 2.0408) < 1e-3 and abs(mzs[10] - np.sqrt(1 - 4 / Us[10] ** 2)) < 3e-3
    check('the dimer cell of the notebook', ok and max(mzs[:10]) < 1e-3 and r19 < 1.5e-3,
          'with U = linspace(0,10,50) the magnetization leaves zero at the point U=%.3f with |m| = %.4f, after %.0e at U=%.3f, '
          'and U=1.9t leaves %.0e, the tolerance of the loop next to the threshold' % (first, mzs[10], mzs[9], Us[9], r19))

    # ======================================================================= the open points of the old text
    md15 = dimer_hartree(1.5, 0.3)[0]
    check('a finite m for U>0', chain_m(1.0)[0] > 0.02 and abs(md15) < 1e-9 and Uc_lim > 2.2,
          'the half-filled chain has m = %.4f at U=t, while the dimer has m = %.0e at U=1.5t and the honeycomb lattice has no '
          'moment below %.2ft' % (chain_m(1.0)[0], abs(md15), Uc_lim))

    check('an attractive U at half filling', abs(2 * dBCS - 3 * d_neg) < 1e-6 and abs(hc.get_gap() - 2 * dBCS) < 2e-3,
          'at U=-3t the charge density wave and the s-wave state have the same gap %.4f' % (3 * d_neg))

    check('the honeycomb challenge', 'islands' not in src21 and 'honeycomb_lattice()' in src21 and 'nk=10' in src21,
          'the cell takes geometry.honeycomb_lattice() with nk=10, and no island')

    src24, _ = cell_after('## Symmetry breaking in the spinless fermionic chain')
    check('the unbiased guess', 'mf="CDW"' in src24 and near(gC, [1, -1], 1e-12),
          'the cell passes mf="CDW", the onsite energies %s' % gC)

    with quiet():
        hn24 = geometry.bichain().get_hamiltonian(has_spin=False).get_mean_field_hamiltonian(V1=3.0, mf="CDW", mix=0.5, filling=0.5, write=False)
    d24 = np.real(hn24.get_vev(operator=None))
    ok = 'compute_cross' not in src24 and abs(abs(d24[0] - d24[1]) - 0.70) < 0.01 and r'\langle n_i\rangle n_{i+1}' in cells[23]
    check('the decoupling of the notebook', ok,
          'the cell writes the Hartree decoupling and calls the default, which keeps the Fock term, so at V=3t it gives %.3f '
          'where Hartree gives %.3f' % (abs(d24[0] - d24[1]), 0.8923))

    src12, md11 = cell_after('## Magnetic order driven by interactions in a chain')
    check('the arrows of cell 12', 'extract("mz")' in src12 and near(fld_c, -3.0 * mom_c / 2, 2e-3),
          'the arrows are drawn from extract("mz"), the field -U m/2, so each arrow points against the moment of its site')

    ok = r'\langle S_z\rangle = \tfrac12' in md11 and r'\\langle S_z \\rangle' in src15 and 'get_vev("mz")' in src15
    check('the label of the dimer', ok and near(np.abs(m98), np.sqrt(1 - (2 / 9.8) ** 2), 1e-4),
          'cell 11 defines <S_z> as half of n_up - n_dn, and cell 15 plots get_vev("mz"), which is n_up - n_dn = %.4f at U=9.8t, '
          'with the label <S_z>' % abs(m98[0]))

    md17 = cells[17]
    check('the sign on the even sites', 'even sites have positive magnetization' in md17 and np.all(mom_c[0::2] < 0),
          'the cell says that the even sites have a positive magnetization, and get_vev("mz") with the guess "antiferro" is '
          '%+.4f there' % mom_c[0])

    check('Delta as a number and as an energy', abs(dBCS / pair - Ua) < 1e-6,
          '|Delta| of (5.3) is |U| = %.0f times |<c_dn c_up>| of (1.9), %.4f against %.4f' % (Ua, dBCS, pair))

    check('a continuous onset in Section 6.6', abs(cross - 16 / np.pi) < 1e-9 and chain_m(1.0)[0] > 0,
          'the half-filled chain has no threshold for the antiferromagnet, and its lowest uniform state jumps from m=0 to m=1 at '
          '%.3f, between the existence of the full polarization at 4t and U D(E_F) = 1 at %.3f' % (cross, 2 * np.pi))

    spinor = np.array([1.0, 1.0]) / np.sqrt(2)
    sx_spinor = spinor @ (np.array([[0, 1], [1, 0]]) / 2) @ spinor
    check('m in Section 6.3', abs(ratio_s2 - 2 / 3) < 1e-12 and abs(sx_spinor - 0.5) < 1e-12,
          'the S^2 form gives %.3f of the splitting U m, and the spinor (1,1)/sqrt2 has <S_x> = %.2f, half of the m_x = 1 that '
          'the m of (6.2) gives along x' % (ratio_s2, sx_spinor))

    print('%d checks hold, %.1f s' % (COUNT[0], time.time() - t0))


if __name__ == '__main__':
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            main()
        finally:
            os.chdir(cwd)
