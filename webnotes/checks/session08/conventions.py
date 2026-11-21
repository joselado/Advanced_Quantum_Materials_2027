"""Checks of webnotes/conventions/session08.md, with numbers. Every bullet of the sheet, the open points included, is
one check here, in the order of the sheet, and the script prints one line per bullet and exits 0 when all hold.

The many-body checks build the spin and fermion operators as matrices, with the Jordan-Wigner signs, and the second
route is exact diagonalization in a sector of S^z, dmrgpy, pyqula, a closed form or a count by another rule. The DMRG
numbers of the chains of 40 sites come from one run each and are asserted as ranges. Not asserted, since they are
not a number: what the notebook draws with imshow, and that a page says which coupling or which chi it means.

Run it from anywhere:  python3 webnotes/checks/session08/conventions.py
It runs in about three minutes, most of it in the Ising counts, the Lanczos rings and dmrgpy."""
import contextlib, io, itertools, os, sys, tempfile, time
sys.dont_write_bytecode = True
from math import comb
import numpy as np
import scipy.sparse as sp
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar
from scipy.sparse.linalg import eigsh
from scipy.special import ellipk, expit

PAULI = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], complex)]
SPIN = [p / 2 for p in PAULI]
COUNT = [0]
R = {}                                   # numbers that the open points at the end assert again


def check(name, ok, detail):
    """Prints one line for a check and stops the script when it does not hold."""
    print(('ok    ' if ok else 'FAIL  ') + name + ': ' + detail, flush=True)
    assert ok, name
    COUNT[0] += 1


def quiet(f, *a, **k):
    """Calls f with its printing to stdout swallowed, since dmrgpy prints a notice for short chains."""
    with contextlib.redirect_stdout(io.StringIO()):
        return f(*a, **k)


def dense(m):
    return np.asarray(m.todense() if hasattr(m, 'todense') else m)


# spins one half as matrices

def op(o, i, n):
    """The one-site operator o on site i of n spins one half."""
    out = np.eye(1)
    for j in range(n):
        out = np.kron(out, o if j == i else np.eye(2))
    return out


def sdot(i, j, n):
    return sum(op(s, i, n) @ op(s, j, n) for s in SPIN).real


def stot2(sites, n):
    """The square of the total spin of the given sites, out of n."""
    T = [sum(op(s, i, n) for i in sites) for s in SPIN]
    return sum(t @ t for t in T).real


# fermions as matrices

def modes(m):
    """Annihilation operators of m fermion modes with the Jordan-Wigner strings."""
    a, z = np.array([[0.0, 1.0], [0.0, 0.0]]), np.diag([1.0, -1.0])
    out = []
    for k in range(m):
        o = np.eye(1)
        for j in range(m):
            o = np.kron(o, z if j < k else (a if j == k else np.eye(2)))
        out.append(o.astype(complex))
    return out


def H_(m):
    return m.conj().T


def parton(fu, fd):
    """S = (1/2) f^dag sigma f of one site from its modes up and down."""
    f = (fu, fd)
    return [0.5 * sum(P[a, b] * (H_(f[a]) @ f[b]) for a in range(2) for b in range(2)) for P in PAULI]


# spin chains in a sector of S^z, for Lanczos

def heis_sector(N, bonds, nup, field=None):
    """sum_b J_b S_i.S_j + sum_i h_i S^z_i on the states with nup spins up, a sparse matrix, and the basis."""
    st = np.array(sorted(sum(1 << i for i in c) for c in itertools.combinations(range(N), nup)), dtype=np.int64)
    diag, R_, C_, V_ = np.zeros(len(st)), [], [], []
    for i, j, J in bonds:
        si, sj = (st >> i) & 1, (st >> j) & 1
        diag += 0.25 * J * (2 * si - 1) * (2 * sj - 1)
        fl = np.nonzero(si != sj)[0]
        R_.append(np.searchsorted(st, st[fl] ^ ((1 << i) | (1 << j)))); C_.append(fl); V_.append(np.full(len(fl), 0.5 * J))
    for i, hz in (field or {}).items():
        diag += hz * (((st >> i) & 1) - 0.5)
    R_.append(np.arange(len(st))); C_.append(np.arange(len(st))); V_.append(diag)
    M = sp.csr_matrix((np.concatenate(V_), (np.concatenate(R_), np.concatenate(C_))), shape=(len(st), len(st)))
    return M, st


def ring_gap(N, Js):
    """E0(S^z=1) - E0(S^z=0) of the ring with the bonds Js repeated."""
    b = [(i, (i + 1) % N, Js[i % len(Js)]) for i in range(N)]
    e = [eigsh(heis_sector(N, b, N // 2 + s)[0], k=1, which='SA', tol=1e-10)[0][0] for s in (0, 1)]
    return e[1] - e[0]


def dmrg_chain(n, d=0.0, local=None, uniform=None):
    """The dmrgpy chain of the notebook, bonds 1 + d (-1)^i, and a field on site 0 or on every site."""
    from dmrgpy import spinchain
    sc = spinchain.Spin_Chain(["S=1/2"] * n)
    h = 0
    for i in range(n - 1):
        J = 1.0 + d * (-1) ** i
        h = h + J * (sc.Sx[i] * sc.Sx[i + 1] + sc.Sy[i] * sc.Sy[i + 1] + sc.Sz[i] * sc.Sz[i + 1])
    if local is not None:
        h = h + local * sc.Sz[0]
    if uniform is not None:
        for i in range(n):
            h = h + uniform * sc.Sz[i]
    sc.set_hamiltonian(h)
    return sc


# Ising ground states

def count_configs(N, groups, rule):
    """Number of the 2^N configurations for which rule(bits of a group) holds for every group of sites."""
    total, chunk = 0, 1 << min(N, 22)
    for start in range(0, 1 << N, chunk):
        c = np.arange(start, start + chunk, dtype=np.int64)
        ok = np.ones(chunk, bool)
        for grp in groups:
            ok &= rule(*[(c >> s) & 1 for s in grp])
        total += int(ok.sum())
    return total


def count_lowest(N, bonds):
    """Number of the 2^N configurations with the lowest energy sum_<ij> s_i s_j, with s = +-1."""
    emin, total, chunk = None, 0, 1 << min(N, 22)
    for start in range(0, 1 << N, chunk):
        c = np.arange(start, start + chunk, dtype=np.int64)
        E = np.zeros(chunk, dtype=np.int16)
        for i, j in bonds:
            E += (1 - 2 * (((c >> i) ^ (c >> j)) & 1)).astype(np.int16)
        m = int(E.min())
        if emin is None or m < emin:
            emin, total = m, int((E == m).sum())
        elif m == emin:
            total += int((E == m).sum())
    return total


def edges(triangles):
    """The bonds of a list of triangles, each once."""
    return sorted({tuple(sorted(p)) for t in triangles for p in ((t[0], t[1]), (t[1], t[2]), (t[0], t[2]))})


def kagome_triangles(n1, n2):
    """The up and down triangles of a kagome torus of n1 x n2 cells, A at the cell, B at a1/2, C at a2/2."""
    i = lambda x, y, s: 3 * ((x % n1) + n1 * (y % n2)) + s
    return 3 * n1 * n2, ([(i(x, y, 0), i(x, y, 1), i(x, y, 2)) for x in range(n1) for y in range(n2)] +
                         [(i(x, y, 1), i(x + 1, y, 0), i(x + 1, y - 1, 2)) for x in range(n1) for y in range(n2)])


def triangular_triangles(l1, l2):
    i = lambda x, y: (x % l1) + l1 * (y % l2)
    return l1 * l2, ([(i(x, y), i(x + 1, y), i(x, y + 1)) for x in range(l1) for y in range(l2)] +
                     [(i(x, y), i(x + 1, y), i(x + 1, y - 1)) for x in range(l1) for y in range(l2)])


def square_bonds(l1, l2):
    i = lambda x, y: (x % l1) + l1 * (y % l2)
    return l1 * l2, [(i(x, y), i(x + d[0], y + d[1])) for x in range(l1) for y in range(l2) for d in ((1, 0), (0, 1))]


# spinons on an open square lattice

def open_square(L, links=None):
    """The hopping matrix of an open L x L square lattice, 1 on every bond, times links[(i, j)] where given."""
    links = links or {}
    idx = lambda x, y: x + L * y
    M = np.zeros((L * L, L * L), complex)
    for x in range(L):
        for y in range(L):
            for dx, dy in ((1, 0), (0, 1)):
                if x + dx < L and y + dy < L:
                    i, j = idx(x, y), idx(x + dx, y + dy)
                    M[i, j] = links.get((i, j), 1.0)
                    M[j, i] = np.conj(M[i, j])
    return M, idx


def plaquette_flux(M, idx, L):
    """The product of the hoppings around every plaquette, counterclockwise, over its modulus."""
    F = np.zeros((L - 1, L - 1), complex)
    for x in range(L - 1):
        for y in range(L - 1):
            a, b, c, d = idx(x, y), idx(x + 1, y), idx(x + 1, y + 1), idx(x, y + 1)
            p = M[a, b] * M[b, c] * M[c, d] * M[d, a]
            F[x, y] = p / abs(p)
    return F


def filled(M):
    """The energy of the half-filled levels of one spin of a hopping matrix with a spectrum symmetric around zero."""
    return np.sort(np.linalg.eigvalsh(M))[:len(M) // 2].sum()


def tri_band(k1, k2, t1=1.0, t2=0.0):
    """The band of geometry.triangular_lattice() with the hoppings t1 and t2, by hand, in reduced momenta."""
    c = lambda x: np.cos(2 * np.pi * x)
    return 2 * t1 * (c(k1) + c(k2) + c(k1 + k2)) + 2 * t2 * (c(2 * k1 + k2) + c(k1 + 2 * k2) + c(k1 - k2))


def mesh_levels(h, n, offset=0.0):
    """All the levels of a pyqula Hamiltonian on an n x n mesh of reduced momenta."""
    hk = h.get_hk_gen()
    ks = (np.arange(n) + offset) / n
    return np.array([np.linalg.eigvalsh(hk([a, b, 0.0])) for a in ks for b in ks])


def notebook_kondo(JK, onsite=-2.0, J=0.0, lattice='triangular_lattice'):
    """The Hamiltonian of the Kondo cells of the notebook, the onsite energy put in before H2HFH."""
    from pyqula import geometry
    from pyqula.specialhamiltonian import H2HFH
    h = getattr(geometry, lattice)().get_hamiltonian()
    if onsite:
        h.add_onsite(onsite)
    return H2HFH(h, JK=JK, J=J)


def kondo_weight(h, n):
    """The fermions on the Kondo sites of an H2HFH Hamiltonian in the states below zero, per site, on an n x n mesh."""
    hk = h.get_hk_gen()
    kondo = np.repeat(h.geometry.r[:, 2] > 0, 2)
    tot = 0.0
    for a in np.arange(n) / n:
        for b in np.arange(n) / n:
            e, v = np.linalg.eigh(hk([a, b, 0.0]))
            tot += np.sum(np.abs(v[kondo][:, e < 0]) ** 2)
    return tot / n ** 2 / (kondo.sum() / 2)


def main():
    from pyqula import geometry
    from pyqula.specialhamiltonian import H2HFH
    t0 = time.time()

    # Spins and the exchange
    e, v = np.linalg.eigh(sdot(0, 1, 2))
    check('the Heisenberg coupling', abs(e[0] + 0.75) < 1e-12 and abs(v[:, 0] @ stot2([0, 1], 2) @ v[:, 0]) < 1e-12,
          'with S = sigma/2 and J = 1 on one bond the ground state of J S_0.S_1 has %.2f and S_tot = 0, so J > 0 is '
          'antiferromagnetic' % e[0])
    c = modes(4)                                     # site 0 up and down, site 1 up and down
    n_ = [H_(x) @ x for x in c]
    U, t = 20.0, 1.0
    Hh = -t * sum(H_(c[a]) @ c[a + 2] + H_(c[a + 2]) @ c[a] for a in (0, 1)) + U * (n_[0] @ n_[1] + n_[2] @ n_[3])
    two = np.nonzero(np.abs(np.diag(sum(n_)).real - 2) < 1e-9)[0]
    S0, S1 = parton(c[0], c[1]), parton(c[2], c[3])
    S2 = sum((a + b) @ (a + b) for a, b in zip(S0, S1))
    w, vv = np.linalg.eigh(Hh[np.ix_(two, two)])
    s2 = np.real(np.diag(H_(vv) @ S2[np.ix_(two, two)] @ vv))
    gap_h = w[np.abs(s2 - 2) < 1e-6].min() - w[np.abs(s2) < 1e-6].min()
    check('the Hubbard dimer as a reference', abs(gap_h - 0.1980) < 1e-4 and abs(4 * t ** 2 / U - 0.2) < 1e-12,
          'at U = 20t the singlet lies %.4f t below the triplet, where 4t^2/U of (6.4) is %.4f t' % (gap_h, 4 * t ** 2 / U))
    from dmrgpy import spinchain
    sc = spinchain.Spin_Chain(["S=1/2"] * 2)
    sc.set_hamiltonian(sc.Sx[0] * sc.Sx[1] + sc.Sy[0] * sc.Sy[1] + sc.Sz[0] * sc.Sz[1])
    ed = np.sort(np.real(quiet(sc.get_excited, n=4, mode="ED")))
    ei = np.linalg.eigvalsh(op(SPIN[2], 0, 2) @ op(SPIN[2], 1, 2)).real
    ef = np.linalg.eigvalsh(-sdot(0, 1, 2))
    J109 = -0.25                                      # one bond of (10.9) of Session 10, -J sigma_0 sigma_1
    same109 = np.abs(op(SPIN[2], 0, 2) @ op(SPIN[2], 1, 2) - (-J109) * op(PAULI[2], 0, 2) @ op(PAULI[2], 1, 2)).max()
    check('the two dimers', np.allclose(e, [-0.75, 0.25, 0.25, 0.25]) and np.allclose(ed, e, atol=1e-8)
          and np.allclose(ei, [-0.25, -0.25, 0.25, 0.25]) and np.allclose(ef, [-0.25, -0.25, -0.25, 0.75]) and same109 < 1e-15,
          'Heisenberg %s, dmrgpy %s, Ising %s, which is -J sigma_0 sigma_1 of (10.9) with J = %.2f, and J=-1 gives %s'
          % (np.round(e, 2), np.round(ed, 2), np.round(ei, 2), J109, np.round(ef, 2)))
    psi = np.array([0, 1, -1, 0]) / np.sqrt(2)
    sv = np.linalg.svd(psi.reshape(2, 2), compute_uv=False)
    ent = -np.sum(sv ** 2 * np.log(sv ** 2))
    Tpsi = np.kron(1j * PAULI[1], 1j * PAULI[1]) @ psi.conj()
    mag = max(abs(psi @ op(s, i, 2) @ psi) for s in SPIN for i in (0, 1))
    check('the singlet (8.3)', np.allclose(sv ** 2, 0.5) and abs(ent - np.log(2)) < 1e-12 and np.allclose(Tpsi, psi) and mag < 1e-12,
          '<S_i> = 0, time reversal gives the same state, the Schmidt weights are %s and the entropy %.4f = ln 2'
          % (np.round(sv ** 2, 3), ent))
    ok = True
    for N in range(2, 8):
        x = np.round(np.linalg.eigvalsh(stot2(range(N), N)), 8)
        S = (np.sqrt(1 + 4 * x) - 1) / 2
        for s in np.unique(np.round(S, 6)):
            m = int(round(N / 2 - s))
            want = comb(N, m) - (comb(N, m - 1) if m > 0 else 0)
            ok = ok and abs(np.sum(np.abs(S - s) < 1e-6) - (2 * s + 1) * want) < 1e-9 and abs((2 * s) % 2 - N % 2) < 1e-9
    x4 = np.round(np.linalg.eigvalsh(stot2(range(4), 4)), 8)
    mult4 = [int(np.sum(x4 == s * (s + 1)) // (2 * s + 1)) for s in (0, 1, 2)]
    check('the total spin of N spins one half', ok and mult4 == [2, 3, 1],
          'from S^2 for N = 2 to 7, an integer for even N and a half-integer for odd N with the multiplicity '
          'C(N, N/2-S) - C(N, N/2-S-1), and four sites have S = 0, 1, 2 with %s' % mult4)
    pup = psi @ op(np.diag([1.0, 0.0]), 0, 2) @ psi
    nb = 0.5 - psi @ op(SPIN[2], 0, 2).real @ psi
    check('the Holstein-Primakoff boson in the singlet', abs(nb - 0.5) < 1e-12 and abs(pup - 0.5) < 1e-12,
          '<a^dag a> = S - <S^z> = %.2f = S, no boson with the probability %.2f and one with %.2f' % (nb, pup, 1 - pup))

    # Frustration
    Ez = [sum(a * b for a, b in ((s[0], s[1]), (s[1], s[2]), (s[2], s[0]))) for s in itertools.product((0.5, -0.5), repeat=3)]
    check('the Ising triangle', sorted(Ez).count(-0.25) == 6 and sorted(Ez).count(0.75) == 2,
          'six of the eight configurations at -1/4 and two at +3/4')
    H3 = sdot(0, 1, 3) + sdot(1, 2, 3) + sdot(2, 0, 3)
    w3, v3 = np.linalg.eigh(H3)
    g3 = v3[:, np.abs(w3 - w3[0]) < 1e-9]
    s3 = np.linalg.eigvalsh(H_(g3) @ stot2(range(3), 3) @ g3)
    ok = abs(w3[0] + 0.75) < 1e-12 and g3.shape[1] == 4 and np.allclose(s3, 0.75)
    ok = ok and np.allclose(H3, 0.5 * (stot2(range(3), 3) - 9 / 4 * np.eye(8)))
    R['triangle'] = (g3.shape[1], s3[0])
    check('the Heisenberg triangle', ok, 'the ground level %.2f four times, with S(S+1) = %.2f, two doublets of S = 1/2, '
          'and H = (J/2)(S_tot^2 - 9/4)' % (w3[0], s3[0]))
    not_aligned = lambda a, b, c: ~((a == b) & (b == c))
    antiparallel = lambda a, b: a != b
    sq = [count_configs(*square_bonds(4, l), antiparallel) for l in (2, 4, 6)]
    ntr, ttr = triangular_triangles(6, 4)
    tri = count_configs(ntr, ttr, not_aligned)
    kag = [count_configs(*kagome_triangles(2, l), not_aligned) for l in (3, 4)]
    low = [count_lowest(*square_bonds(4, l)) for l in (2, 4, 6)] + [count_lowest(ntr, edges(ttr))]
    low += [count_lowest(n_k, edges(t_k)) for n_k, t_k in (kagome_triangles(2, l) for l in (3, 4))]
    w_ = np.linspace(0, np.pi / 3, 200001)
    s_tri = 2 / np.pi * np.trapezoid(np.log(2 * np.cos(w_)), w_)
    pauling = np.log(2) + 2 / 3 * np.log(3 / 4)
    ok = sq == [2, 2, 2] and tri == 1698 and kag == [8882, 181122] and abs(s_tri - 0.3231) < 1e-4 and abs(pauling - 0.501) < 1e-3
    ok = ok and low == sq + [tri] + kag
    ok = ok and abs(np.log(tri) / 24 - 0.310) < 1e-3 and abs(np.log(kag[0]) / 18 - 0.505) < 1e-3 and abs(np.log(kag[1]) / 24 - 0.504) < 1e-3
    check('the Ising ground states of the clusters', ok,
          'square 8, 16, 24 sites %s, triangular 6x4 %d (%.3f per site), kagome 18 and 24 sites %d and %d (%.3f and %.3f '
          'per site), the same as the lowest energy over all 2^N configurations, %s, and as the configurations with no '
          'triangle of three equal spins, Wannier %.4f, Pauling %.3f'
          % (sq, tri, np.log(tri) / 24, kag[0], kag[1], np.log(kag[0]) / 18, np.log(kag[1]) / 24, low, s_tri, pauling))
    zs = {}
    for name in ('square_lattice', 'triangular_lattice', 'kagome_lattice'):
        gg = getattr(geometry, name)()
        a1, a2 = np.array(gg.a1)[:2], np.array(gg.a2)[:2]
        r = np.array(gg.r)[:, :2]
        img = np.array([r[j] + n1 * a1 + n2 * a2 for j in range(len(r)) for n1 in range(-2, 3) for n2 in range(-2, 3)])
        d = np.linalg.norm(img[None, :, :] - r[:, None, :], axis=2)
        d[d < 1e-9] = np.inf
        zs[name] = sorted(set(int(np.sum(np.abs(row - row.min()) < 1e-9)) for row in d))
        zs[name + '_bond'] = d.min()
    gk = geometry.kagome_lattice()
    ok = zs['square_lattice'] == [4] and zs['triangular_lattice'] == [6] and zs['kagome_lattice'] == [4]
    ok = ok and np.allclose(gk.a1[:2], [2, 0]) and np.allclose(gk.a2[:2], [1, np.sqrt(3)]) and abs(zs['kagome_lattice_bond'] - 1) < 1e-12
    check('the coordination numbers of pyqula', ok, 'square %s, triangular %s and kagome %s first neighbors, the kagome cell '
          'a1 = (2, 0), a2 = (1, sqrt 3), bond length %.0f' % (zs['square_lattice'], zs['triangular_lattice'], zs['kagome_lattice'],
                                                              zs['kagome_lattice_bond']))

    # The dimerized chain
    nb_ = [1.0 + 0.2 * (-1) ** i for i in range(39)]
    check('the notations of the dimerized chain', abs(nb_[0] - 1.2) < 1e-12 and abs(nb_[1] - 0.8) < 1e-12 and abs(nb_[-1] - 1.2) < 1e-12
          and abs(nb_[1] / nb_[0] - 2 / 3) < 1e-12,
          "the notebook bond (i, i+1) is 1 + 0.2(-1)^i, so (0, 1) is %.1f, (1, 2) is %.1f, the last of the 39 bonds is %.1f, "
          "and J'/J = %.3f" % (nb_[0], nb_[1], nb_[-1], nb_[1] / nb_[0]))
    four = lambda Jp: sdot(0, 1, 4) + Jp * sdot(1, 2, 4) + sdot(2, 3, 4)
    S4 = stot2(range(4), 4)
    out, ok = {}, True
    for Jp in np.linspace(0, 1, 51):
        w4, v4 = np.linalg.eigh(four(Jp))
        closed = -0.5 * (1 + Jp / 2) - 0.5 * np.sqrt((2 - Jp / 2) ** 2 + 0.75 * Jp ** 2)
        ok = ok and w4[1] - w4[0] > 0.65 and abs(v4[:, 0] @ S4 @ v4[:, 0]) < 1e-9 and abs(w4[0] - closed) < 1e-12
        out[round(Jp, 2)] = w4
    sc = spinchain.Spin_Chain(["S=1/2"] * 4)
    ssd = lambda i, j: sc.Sx[i] * sc.Sx[j] + sc.Sy[i] * sc.Sy[j] + sc.Sz[i] * sc.Sz[j]
    sc.set_hamiltonian(ssd(0, 1) + 0.1 * ssd(1, 2) + ssd(2, 3))
    ed4 = np.sort(np.real(quiet(sc.get_excited, n=4, mode="ED")))
    a, b = out[0.1], out[1.0]
    ok = ok and abs(a[0] + 1.50096) < 1e-5 and np.allclose(a[1:4], -0.52749, atol=1e-5) and abs(a[1] - a[0] - 0.973) < 1e-3
    ok = ok and abs(b[1] - b[0] - 0.659) < 1e-3 and np.allclose(ed4, a[:4], atol=1e-8)
    check("the open chain of four sites J, J', J", ok,
          "J'=0.1J gives %.5f and a threefold %.5f, the gap %.3f, J'=J gives the gap %.3f, a nondegenerate singlet with the "
          "closed form for 51 values of J' from 0 to J, and dmrgpy gives the same levels" % (a[0], a[1], a[1] - a[0], b[1] - b[0]))
    gd = [ring_gap(N, [1.0, 0.1]) for N in (12, 16, 20)]
    al = 0.1
    series = 1 - al / 2 - 3 * al ** 2 / 8 + al ** 3 / 32
    go = []                                          # open chains with a strong bond at each end, as on the sheet of Session 7
    for N in (12, 16):
        b = [(i, i + 1, 1.0 if i % 2 == 0 else 0.1) for i in range(N - 1)]
        e = [eigsh(heis_sector(N, b, N // 2 + s)[0], k=1, which='SA', tol=1e-10)[0][0] for s in (0, 1)]
        go.append(e[1] - e[0])
    check("the infinite chain of dimers with J'=0.1J", max(gd) - min(gd) < 1e-6 and abs(gd[-1] - 0.9463) < 1e-4 and abs(series - gd[-1]) < 1e-4
          and abs(go[0] - 0.9517) < 5e-5 and abs(go[1] - 0.9496) < 5e-5,
          'the triplet gap is %.6f, %.6f and %.6f on rings of 12, 16 and 20 sites, and the series gives %.5f, while open '
          'chains of 12 and 16 sites give %.4f and %.4f' % (gd[0], gd[1], gd[2], series, go[0], go[1]))
    g2 = [ring_gap(N, [1.2, 0.8]) for N in (12, 16, 20)]
    g5 = [ring_gap(N, [1.05, 0.95]) for N in (12, 16, 20)]
    R['gap02'] = g2[-1]
    ok = np.allclose(g2, [0.623, 0.605, 0.600], atol=1e-3) and abs(g5[0] - 0.38) < 0.005 and abs(g5[-1] - 0.27) < 0.005 and g5[0] > g5[1] > g5[2]
    check('the dimerized chain of the notebook', ok,
          'the bonds 1.2 and 0.8 give the gap %.3f, %.3f and %.3f on rings of 12, 16 and 20 sites, and the bonds 1.05 and '
          '0.95 give %.3f, %.3f and %.3f, not converged' % (*g2, *g5))
    prof = {}
    for d in (0.0, 0.2, 0.05):
        sc = dmrg_chain(40, d, local=1.0)
        m = np.array([np.real(sc.vev(sc.Sz[i], mode="DMRG")) for i in range(40)])
        prof[d] = m
    alt = all(np.all(np.sign(prof[d][:16]) == -(-1) ** np.arange(16)) and abs(prof[d].sum()) < 1e-6 for d in prof)
    xi = {d: 10 / np.log(abs(prof[d][10]) / abs(prof[d][20])) for d in prof}
    Hed, st = heis_sector(20, [(i, i + 1, 1.0 + 0.2 * (-1) ** i) for i in range(19)], 10, field={0: 1.0})
    ved = eigsh(Hed, k=1, which='SA', tol=1e-12)[1][:, 0]
    m10_ed = abs(np.sum(np.abs(ved) ** 2 * (((st >> 10) & 1) - 0.5)))
    vel = np.pi / 2
    ok = alt and -0.43 < prof[0.0][0] < -0.40 and 0.115 < abs(prof[0.0][10]) < 0.125 and 0.075 < abs(prof[0.0][20]) < 0.085
    ok = ok and 0.0050 < abs(prof[0.2][10]) < 0.0062 and 1.0e-4 < abs(prof[0.2][20]) < 1.4e-4
    ok = ok and 0.050 < abs(prof[0.05][10]) < 0.060 and 0.012 < abs(prof[0.05][20]) < 0.016
    ok = ok and 2.4 < xi[0.2] < 2.8 and 6.8 < xi[0.05] < 7.6 and abs(vel / R['gap02'] - xi[0.2]) < 0.15 and abs(m10_ed - abs(prof[0.2][10])) < 2e-4
    R['xi'] = xi
    check('the notebook chains with the field 1 on site 0', ok,
          '<S^z_0> = %.3f, |<S^z_10>| and |<S^z_20>| are %.3f %.3f (uniform), %.4f %.1e (0.2), %.3f %.3f (0.05), the sign '
          'alternates and the total is 0, decay lengths %.2f and %.2f sites, v/Delta = (pi/2)/%.3f = %.2f, and 20 sites by '
          'Lanczos give %.4f at site 10 for 0.2' % (prof[0.0][0], abs(prof[0.0][10]), abs(prof[0.0][20]), abs(prof[0.2][10]),
                                                    abs(prof[0.2][20]), abs(prof[0.05][10]), abs(prof[0.05][20]), xi[0.2], xi[0.05],
                                                    R['gap02'], vel / R['gap02'], m10_ed))
    small, big = dmrg_chain(40, uniform=-0.01), dmrg_chain(40, uniform=-0.15)
    e0, e1 = np.real(small.gs_energy(mode="DMRG")), np.real(big.gs_energy(mode="DMRG"))
    m0 = np.array([np.real(small.vev(small.Sz[i], mode="DMRG")) for i in range(40)])
    m1 = sum(np.real(big.vev(big.Sz[i], mode="DMRG")) for i in range(40))
    gap40 = e1 + 0.15 * m1 - e0
    check('the uniform chain of 40 sites of the notebook in a field', np.abs(m0).max() < 1e-5 and abs(m1 - 1) < 1e-6 and 0.090 < gap40 < 0.100,
          'with Bz = -0.01 the largest |<S^z_i>| is %.0e, with Bz = -0.15 the ground state has S^z = %.3f, so the gap to the '
          'lowest triplet is %.4f' % (np.abs(m0).max(), m1, gap40))

    # The resonating valence bond state
    f2 = modes(2)
    n1 = sum(H_(x) @ x for x in f2)
    pg = np.real(np.diag(n1 @ (2 * np.eye(4) - n1)))
    check('the Gutzwiller projector of (8.7)', np.allclose(sorted(zip(np.real(np.diag(n1)), pg)), [(0, 0), (1, 1), (1, 1), (2, 0)]),
          'n(2-n) is %s on the states with n = %s' % (pg.astype(int).tolist(), np.real(np.diag(n1)).astype(int).tolist()))

    def cover(pairs):
        """The product of the singlets (|up dn> - |dn up>)/sqrt 2 on the ordered pairs, as a tensor of four sites."""
        s = np.array([[0, 1], [-1, 0]]) / np.sqrt(2)          # s[a, b], a on the first site of the pair
        T = np.einsum('ab,cd->abcd', s, s)                     # sites (p0, p1, q0, q1)
        order = [pairs[0][0], pairs[0][1], pairs[1][0], pairs[1][1]]
        return np.transpose(T, np.argsort(order)).reshape(16)
    Hp = sum(sdot(i, (i + 1) % 4, 4) for i in range(4))
    A, B, B2 = cover([(0, 1), (2, 3)]), cover([(1, 2), (3, 0)]), cover([(1, 2), (0, 3)])
    en = lambda p: (p @ Hp @ p) / (p @ p)
    th = np.linspace(0, np.pi, 721)
    curve = [en(np.cos(x) * A + np.sin(x) * B) for x in th]
    plus = (A + B) / np.linalg.norm(A + B)
    diag = [plus @ stot2(s, 4) @ plus for s in (range(4), [0, 2], [1, 3])]
    ok = abs(A @ B - 0.5) < 1e-12 and abs(A @ B2 + 0.5) < 1e-12 and abs(en(A) + 1.5) < 1e-12 and abs(en(A + B) + 2) < 1e-12
    ok = ok and abs(en(A - B)) < 1e-12 and abs(en(A - B2) + 2) < 1e-12 and abs(np.linalg.eigvalsh(Hp)[0] + 2) < 1e-12
    ok = ok and abs(th[np.argmin(curve)] - np.pi / 4) < 1e-9 and np.allclose(diag, [0, 2, 2]) and abs((A - B) @ stot2(range(4), 4) @ (A - B)) < 1e-12
    R['overlaps'] = (A @ B, A @ B2)
    check('the plaquette of four spins', ok, '<a|b> = %+.1f with (12)(30) and %+.1f with (12)(03), one covering %.2f, |a>+|b> '
          '%.2f at theta = pi/4, the exact ground level, with S_tot^2, S_02^2 and S_13^2 equal to %s, and |a>-|b> %.2f'
          % (A @ B, A @ B2, en(A), en(A + B), np.round(diag, 6).tolist(), en(A - B)))

    # Abrikosov fermions
    S = parton(f2[0], f2[1])
    alg = max(np.abs(S[i] @ S[j] - S[j] @ S[i] - 1j * S[k]).max() for i, j, k in ((0, 1, 2), (1, 2, 0), (2, 0, 1)))
    Ssq = np.real(np.diag(sum(x @ x for x in S)))
    occ = np.real(np.diag(n1))
    rais = np.abs(S[2] @ H_(f2[0]) - H_(f2[0]) @ S[2] - 0.5 * H_(f2[0])).max()
    check('(8.10) on the four states of a site', alg < 1e-14 and np.allclose(Ssq[occ == 1], 0.75) and np.allclose(Ssq[occ != 1], 0) and rais < 1e-14,
          'the algebra holds to %.0e on all four states, S^2 is 3/4 on one fermion and 0 on none and on two, and '
          '[S^z, f^dag_up] = f^dag_up/2' % alg)
    fz = max(abs(sum(P[a, b] * P[c_, d] for P in PAULI) - (2 * (a == d) * (b == c_) - (a == b) * (c_ == d)))
             for a, b, c_, d in itertools.product(range(2), repeat=4))
    f4 = modes(4)
    Si, Sj = parton(f4[0], f4[1]), parton(f4[2], f4[3])
    ni, nj = H_(f4[0]) @ f4[0] + H_(f4[1]) @ f4[1], H_(f4[2]) @ f4[2] + H_(f4[3]) @ f4[3]
    chi = H_(f4[0]) @ f4[2] + H_(f4[1]) @ f4[3]
    SS = sum(x @ y for x, y in zip(Si, Sj))
    X = 0.25 * np.eye(16) - 0.5 * H_(chi) @ chi
    one = np.nonzero((np.abs(np.real(np.diag(ni)) - 1) < 1e-9) & (np.abs(np.real(np.diag(nj)) - 1) < 1e-9))[0]
    on = np.abs((SS - X)[np.ix_(one, one)]).max()
    off = np.abs(SS - X).max()
    we, ve = np.linalg.eigh(SS[np.ix_(one, one)])
    cc = np.real(np.diag(H_(ve) @ (H_(chi) @ chi)[np.ix_(one, one)] @ ve))
    check('the Fierz identity and (8.12)', fz < 1e-14 and on < 1e-14 and abs(off - 0.75) < 1e-12 and np.allclose(we, [-0.75, 0.25, 0.25, 0.25])
          and np.allclose(cc, [2, 0, 0, 0]),
          'the Fierz identity on all 16 sets of indices, (8.12) to %.0e on n_i = n_j = 1 and off by up to %.2f elsewhere, '
          'chi^dag chi = %s on the singlet and the triplet' % (on, off, np.round(cc, 6).tolist()))
    Sab = lambda a, b: H_(f2[a]) @ f2[b] - 0.5 * n1 * (a == b)
    err = max(np.abs(Sab(a, b) - sum(S[k] * PAULI[k][b, a] for k in range(3))).max() for a in range(2) for b in range(2))
    tr = np.abs(np.diag(Sab(0, 0) + Sab(1, 1))).max()
    R['trace819'] = tr
    check('(8.19) is the spin as a matrix', err < 1e-14 and tr < 1e-14,
          'f^dag_a f_b - (n/2) delta_ab = (S.sigma)_ba to %.0e, and its trace is %.0e on all four states' % (err, tr))

    # The spinon mean field
    N = 98

    def step(tt):
        """One step of the loop of (8.14) on a ring, J = 1: the new coefficient of f^dag_i f_i+1 is
        -(J/2) sum_s <f^dag_i+1 f_i>, with half filling per spin."""
        M = np.zeros((N, N))
        for i in range(N):
            M[i, (i + 1) % N] = M[(i + 1) % N, i] = tt[i]
        vv = np.linalg.eigh(M)[1][:, :N // 2]
        G = vv @ vv.T                                  # G[a, b] = <f^dag_a f_b> for one spin
        corr = np.array([G[(i + 1) % N, i] for i in range(N)])
        return -corr, corr
    fixed = [step(s * np.ones(N) / np.pi)[0] for s in (1, -1)]
    from pyqula.spinon import SpinonHamiltonian
    tq = []
    for seed in (1, 2):
        np.random.seed(seed)
        hs = quiet(SpinonHamiltonian(geometry.chain()).get_mean_field_hamiltonian, J1=1.0, nk=200, decoupling="bond", integration="ed")
        hop = {tuple(int(x) for x in dd): dense(m) for dd, m in hs.get_multihopping().get_dict().items()}
        tq.append(hop[(1, 0, 0)][0, 0])
        occ1 = float(np.real(hs.local_occupation[0]))
    ok = all(np.allclose(fx, s / np.pi, atol=1e-4) for fx, s in zip(fixed, (1, -1))) and all(abs(abs(x) - 1 / np.pi) < 3e-4 for x in tq)
    check('the spinon hopping of the chain', ok and abs(occ1 - 1) < 1e-4,
          'on a ring of 98 sites +1/pi and -1/pi are both fixed points of the loop, %+.5f and %+.5f, and SpinonHamiltonian '
          'with decoupling="bond" gives %s, |t| = %.4f, with one fermion per site'
          % (fixed[0][0], fixed[1][0], ', '.join('%.3f%+.3fi' % (x.real, x.imag) for x in tq), abs(tq[0])))
    rng = np.random.default_rng(7)
    ends = []
    for s in (1, -1):
        tt = s / np.pi + 1e-3 * rng.standard_normal(N)
        for it in range(4000):
            new, corr = step(tt)
            if np.abs(new - tt).max() < 1e-12:
                break
            tt = 0.5 * new + 0.5 * tt
        ends.append((np.sort(np.abs(tt)), it, np.mean(0.25 - 0.5 * (2 * corr) ** 2)))
    Eu = 0.25 - 0.5 * (2 / np.pi) ** 2
    tb = []
    for seed in (1, 2):
        np.random.seed(seed)
        hb = quiet(SpinonHamiltonian(geometry.bichain()).get_mean_field_hamiltonian, J1=1.0, nk=100, decoupling="bond", integration="ed")
        hop = {tuple(int(x) for x in dd): dense(m)[0::2, 0::2] for dd, m in hb.get_multihopping().get_dict().items()}
        tb.append(sorted([abs(hop[(0, 0, 0)][0, 1]), max(abs(hop[(1, 0, 0)]).max(), abs(hop[(-1, 0, 0)]).max())]))
    ok = all(np.allclose(x[0][:N // 2], 0, atol=1e-6) and np.allclose(x[0][N // 2:], 0.5, atol=1e-6) and abs(x[2]) < 1e-9 for x in ends)
    ok = ok and all(abs(x[1] - 0.5) < 1e-3 and x[0] < 1e-3 for x in tb) and abs(Eu - 0.0474) < 1e-4
    R['dimerized'] = (ends[0][2], Eu)
    check('the free loop dimerizes', ok,
          'from either sign, a start within 1e-3 of the uniform chain ends after %d and %d steps at the hoppings 0.5 and 0, '
          'energy %.0e per bond against %.4f, and pyqula on bichain ends at %s' % (ends[0][1], ends[1][1], ends[0][2], Eu,
                                                                                ' and '.join('%.3f, %.3f' % (x[1], x[0]) for x in tb)))
    ht = geometry.triangular_lattice().get_hamiltonian()
    ht.set_filling(0.5, nk=60)
    k_ = (np.arange(240) + 0.5) / 240
    K1, K2 = np.meshgrid(k_, k_, indexing='ij')
    zero60 = -(np.linalg.eigvalsh(ht.get_hk_gen()([0.0, 0.0, 0.0]))[0] - 6.0)
    below = 2 * np.mean(tri_band(K1, K2) < zero60)
    check('half filling is one fermion per site', ht.intra.shape == (2, 2) and abs(below - 1) < 0.01,
          'a spinful site has %d states, and filling=0.5 leaves %.3f fermions per site below zero on a dense mesh'
          % (ht.intra.shape[0], below))
    kk = np.linspace(-np.pi, np.pi, 401)
    Ea = -2 * np.cos(kk)
    Eb = np.array([np.linalg.eigvalsh(-np.array([[0, 1 + 0.6 * np.exp(-1j * q)], [1 + 0.6 * np.exp(1j * q), 0]])) for q in kk])
    hbc = geometry.bichain().get_hamiltonian(has_spin=False)
    hbc.inter = 0.6 * hbc.inter
    gen = hbc.get_hk_gen()
    eq = np.array([np.linalg.eigvalsh(gen([q, 0.0, 0.0])) for q in np.linspace(0, 1, 401)])

    def Hfig(kx, ky):
        """The pi-flux lattice of the figure, two sites along x, -chi along x and -chi(-1)^x along y, chi = 1."""
        return np.array([[-2 * np.cos(ky), -(1 + np.exp(-2j * kx))], [-(1 + np.exp(2j * kx)), 2 * np.cos(ky)]])
    pts = np.random.default_rng(3).uniform(-np.pi, np.pi, (20, 2))
    perr = max(abs(np.linalg.eigvalsh(Hfig(*q))[1] - 2 * np.sqrt(np.cos(q[0]) ** 2 + np.cos(q[1]) ** 2)) for q in pts)
    _, i5 = open_square(5)
    pat = {(i5(x, y), i5(x + 1, y)): -1.0 for x in range(4) for y in range(5)}
    pat.update({(i5(x, y), i5(x, y + 1)): -(-1.0) ** x for x in range(5) for y in range(4)})
    Ffig = plaquette_flux(open_square(5, pat)[0], i5, 5)
    qx, qy = np.linspace(-np.pi / 2, np.pi / 2, 81)[1:], np.linspace(-np.pi, np.pi, 161)[1:]
    zz = sorted((float(round(a / np.pi, 6)), float(round(b / np.pi, 6))) for a in qx for b in qy
                if np.diff(np.linalg.eigvalsh(Hfig(a, b)))[0] < 1e-9)
    ok = np.min(np.abs(Ea)) < 1e-12 and np.allclose(kk[np.abs(Ea) < 1e-12], [-np.pi / 2, np.pi / 2])
    ok = ok and abs(Eb[:, 1].min() - Eb[:, 0].max() - 0.8) < 1e-9 and abs(eq[:, 1].min() - eq[:, 0].max() - 0.8) < 1e-9
    ok = ok and perr < 1e-12 and np.allclose(Ffig, -1) and zz == [(0.5, -0.5), (0.5, 0.5)]
    check('the three classes of the figure spinon_bands', ok,
          'the uniform chain crosses zero at k = +-pi/2, the hoppings 1 and 0.6 give the gap %.3f with numpy and %.3f with '
          'bichain, and the pi-flux lattice of the figure follows 2 sqrt(cos^2 kx + cos^2 ky) to %.0e, with Phi = -1 on all '
          '16 plaquettes of a 5x5 patch and its Dirac points at (kx, ky)/pi = %s' % (Eb[:, 1].min() - Eb[:, 0].max(),
                                                                               eq[:, 1].min() - eq[:, 0].max(), perr, zz))
    hp = geometry.square_lattice().get_supercell([1, 2]).get_hamiltonian(has_spin=False)
    hp.add_orbital_magnetic_field(0.5)
    gen = hp.get_hk_gen()
    qq = np.random.default_rng(4).uniform(0, 1, (20, 2))
    qerr = max(abs(np.linalg.eigvalsh(gen([a, b, 0.0]))[1] - 2 * np.sqrt(np.sin(2 * np.pi * a) ** 2 + np.cos(np.pi * b) ** 2)) for a, b in qq)
    ks = np.arange(40) / 40
    E2 = np.array([[np.linalg.eigvalsh(gen([a, b, 0.0])) for b in ks] for a in ks])
    dp = sorted((float(ks[i]), float(ks[j])) for i, j in np.argwhere(E2[:, :, 1] - E2[:, :, 0] < 1e-9))
    hx = {tuple(int(x) for x in t_.dir): dense(t_.m) for t_ in hp.get_multicell().hopping}
    yy = np.array(hp.geometry.r)[:, 1]
    # the plaquette between the two rows of the cell, x -> x+1 on the lower row, up, back on the upper row, down
    lo, up_ = int(np.argmin(yy)), int(np.argmax(yy))
    T10, H0 = hx[(1, 0, 0)], dense(hp.intra)
    flux_q = T10[up_, up_].conj() * H0[up_, lo] * T10[lo, lo] * H0[lo, up_]
    flux_q = flux_q / abs(flux_q)
    hz = geometry.square_lattice().get_supercell([2, 1]).get_hamiltonian(has_spin=False)
    hz.add_orbital_magnetic_field(0.5)
    Ez_ = mesh_levels(hz, 20)
    real = all(np.abs(np.imag(dense(t_.m))).max() < 1e-12 for t_ in hz.get_multicell().hopping) and np.abs(np.imag(dense(hz.intra))).max() < 1e-12
    ok = qerr < 1e-12 and dp == [(0.0, 0.5), (0.5, 0.5)] and abs(np.abs(E2).max() - np.sqrt(8)) < 1e-12 and abs(flux_q + 1) < 1e-12
    ok = ok and real and abs(Ez_.min() + 4) < 1e-9 and abs(Ez_.max() - 4) < 1e-9
    check('the pi-flux lattice of pyqula', ok,
          'get_supercell([1, 2]) with add_orbital_magnetic_field(0.5) has 2 sqrt(sin^2 2pi k1 + cos^2 pi k2) to %.0e, from '
          '-%.3f to %.3f, Phi = %+.0f, and its Dirac points at (k1, k2) = %s, while get_supercell([2, 1]) keeps every hopping '
          'real, with the bands from %.0f to %.0f' % (qerr, np.abs(E2).max(), np.abs(E2).max(), flux_q.real, dp, Ez_.min(), Ez_.max()))
    M6, i6 = open_square(6)
    flip = np.abs(np.linalg.eigvalsh(-M6) - np.linalg.eigvalsh(M6)).max()
    n = 300
    k = (np.arange(n) + 0.5) / n
    K1, K2 = np.meshgrid(k, k, indexing='ij')
    occ_ = {}
    for tij in ((1.0, 0.5), (-1.0, -0.5), (1.0, -0.5)):
        eb = tri_band(K1, K2, *tij)
        occ_[tij] = eb < np.median(eb)
    comp = np.mean(occ_[(1.0, 0.5)] != occ_[(-1.0, -0.5)])
    diff = np.mean(occ_[(1.0, 0.5)] != occ_[(1.0, -0.5)])
    check('the sign of chi', flip < 1e-12 and comp > 0.999 and abs(diff - 0.23) < 0.01,
          'chi and -chi give the same levels on the open 6x6 lattice to %.0e, tij=[1, 0.5] and [-1, -0.5] fill complementary '
          'halves of the triangular zone (they differ on %.3f of it), and tij=[1, -0.5] differs from [1, 0.5] on %.2f'
          % (flip, comp, diff))

    # The gauge structure
    th2 = (0.7, -1.3)
    chig = sum(H_(np.exp(1j * th2[0]) * f4[s]) @ (np.exp(1j * th2[1]) * f4[2 + s]) for s in range(2))
    op_phase = np.allclose(chig, np.exp(-1j * (th2[0] - th2[1])) * chi)
    th = np.random.default_rng(1).uniform(0, 2 * np.pi, 36)
    D = np.diag(np.exp(1j * th))
    pot = np.diag(np.random.default_rng(5).uniform(-0.3, 0.3, 36))       # lifts the zero modes, gauge invariant
    h1 = M6 + pot
    h2 = D @ h1 @ H_(D)                                                     # the coefficient gets e^{i(theta_i - theta_j)}
    P = lambda M: (lambda vv: vv @ H_(vv))(np.linalg.eigh(M)[1][:, :18])
    G1, G2 = P(h1).T, P(h2).T                                               # G[a, b] = <f^dag_a f_b>
    i_, j_ = i6(1, 2), i6(2, 2)
    exp_phase = G2[i_, j_] / G1[i_, j_] / np.exp(-1j * (th[i_] - th[j_]))
    coef_phase = (h2[i_, j_] / h1[i_, j_]) / np.exp(1j * (th[i_] - th[j_]))
    selfc = (np.conj(G2[i_, j_]) / np.conj(G1[i_, j_])) / np.exp(1j * (th[i_] - th[j_]))
    R['phases'] = op_phase and abs(exp_phase - 1) < 1e-9 and abs(coef_phase - 1) < 1e-12 and abs(selfc - 1) < 1e-9
    check('the gauge rotation (8.16)', R['phases'],
          'the operator chi_ij and its expectation value get e^{-i(theta_i - theta_j)}, and the coefficient -(J/2)<chi_ij>* '
          'of f^dag_i f_j gets e^{+i(theta_i - theta_j)}, checked on two sites with the angles 0.7 and -1.3 and on the 6x6 lattice')
    Mg = D @ M6 @ H_(D)
    straight = {(i6(x, 2), i6(x, 3)): -1.0 for x in range(3)}
    Mv = open_square(6, straight)[0]
    Mw = open_square(6, {(i6(2, y), i6(3, y)): -1.0 for y in range(3)})[0]
    E0, Eg, Ev, Ew = (np.linalg.eigvalsh(m) for m in (M6, Mg, Mv, Mw))
    F0, Fg, Fv, Fw = (plaquette_flux(m, i6, 6) for m in (M6, Mg, Mv, Mw))
    ok = np.allclose(Fg, F0) and np.abs(Eg - E0).max() < 1e-12 and abs(Fv[2, 2] + 1) < 1e-12 and abs(np.real(Fv).sum() - 23) < 1e-9
    ok = ok and np.allclose(Fw, Fv) and np.abs(Ew - Ev).max() < 1e-12 and abs(np.abs(Ev - E0).max() - 0.360) < 5e-4
    check('the flux and the string on the 6x6 lattice', ok,
          'a random rotation keeps every flux and every level to %.0e, the string of three vertical links from the left edge '
          'gives -1 on the central plaquette and +1 on the other 24, a string of three horizontal links from the bottom edge '
          'gives the same fluxes and levels to %.0e, and the levels move by up to %.3f'
          % (np.abs(Eg - E0).max(), np.abs(Ew - Ev).max(), np.abs(Ev - E0).max()))
    cost0, costpi = {}, {}
    for L in (6, 8, 10, 12):
        ML, iL = open_square(L)
        cc_ = L // 2 - 1
        string = {(iL(x, cc_), iL(x, cc_ + 1)): -1.0 for x in range(cc_ + 1)}
        cost0[L] = filled(open_square(L, string)[0]) - filled(ML)
        pi_links = {(iL(x, y), iL(x, y + 1)): (-1.0) ** x for x in range(L) for y in range(L - 1)}
        back = dict(pi_links)
        for key in string:
            back[key] = -back[key]
        Mp, Mq = open_square(L, pi_links)[0], open_square(L, back)[0]
        assert np.allclose(plaquette_flux(Mp, iL, L), -1) and abs(plaquette_flux(Mq, iL, L)[cc_, cc_] - 1) < 1e-12
        costpi[L] = filled(Mq) - filled(Mp)
    q = 2 * np.pi * (np.arange(600) + 0.5) / 600
    QX, QY = np.meshgrid(q, q, indexing='ij')
    eu = -2 * (np.cos(QX) + np.cos(QY))
    e_uni = np.mean(np.where(eu < 0, eu, 0))
    e_pi = 0.5 * np.mean(-2 * np.sqrt(np.cos(QX) ** 2 + np.cos(QY) ** 2))
    ok = abs(e_uni + 8 / np.pi ** 2) < 1e-4 and abs(e_pi + 0.958) < 1e-3 and abs(cost0[6] + 0.74) < 0.005 and abs(cost0[12] + 0.69) < 0.005
    ok = ok and all(c_ < 0 for c_ in cost0.values()) and all(0.19 < c_ < 0.55 for c_ in costpi.values())
    R['vison'] = (cost0[6], e_uni, e_pi)
    check('the energy of a vison', ok,
          'per site and spin the infinite lattice has %.4f with Phi = +1 and %.4f with Phi = -1, a flipped plaquette in the '
          'uniform background changes the energy by %s on the open lattices of side 6, 8, 10 and 12, and one plaquette set '
          'back to +1 in the pi-flux state by %s' % (e_uni, e_pi, ' '.join('%+.2f' % x for x in cost0.values()),
                                                     ' '.join('%+.2f' % x for x in costpi.values())))

    # The Kondo impurity and the Kondo lattice
    cu, cd, fu, fd = modes(4)
    cc4, ff = (cu, cd), (fu, fd)
    Sf = parton(fu, fd)
    csc = [sum(Pm[b, a_] * (H_(cc4[b]) @ cc4[a_]) for a_ in range(2) for b in range(2)) for Pm in PAULI]
    HK = sum(x @ y for x, y in zip(csc, Sf))
    sK = [x / 2 for x in csc]
    nc, nf = H_(cu) @ cu + H_(cd) @ cd, H_(fu) @ fu + H_(fd) @ fd
    both = np.nonzero((np.abs(np.real(np.diag(nc)) - 1) < 1e-9) & (np.abs(np.real(np.diag(nf)) - 1) < 1e-9))[0]
    lv = np.linalg.eigvalsh(HK[np.ix_(both, both)])
    R['twice'] = np.allclose(HK, 2 * sum(x @ y for x, y in zip(sK, Sf)))
    check('the Kondo coupling (8.17)', R['twice'] and np.allclose(lv, [-1.5, 0.5, 0.5, 0.5]),
          '(c^dag sigma c).S = 2 s.S on the 16 states of a site, and with one electron and J_K = 1 the singlet is at %.2f and '
          'the triplet at %.2f, a splitting 2 J_K' % (lv[0], lv[1]))
    Bo = H_(cu) @ fu + H_(cd) @ fd
    full = np.abs(HK - (-Bo @ H_(Bo) + nc - 0.5 * nc @ nf)).max()
    onef = np.nonzero(np.abs(np.real(np.diag(nf)) - 1) < 1e-9)[0]
    part = np.abs((HK - (-Bo @ H_(Bo) + 0.5 * nc))[np.ix_(onef, onef)]).max()
    check('(8.20) from (8.18)', full < 1e-14 and part < 1e-14,
          'on n_f = 1 the extra term is (J_K/2) n_c to %.0e, and on all 16 states J_K n_c - (J_K/2) n_c n_f to %.0e' % (part, full))
    ek = -2 * np.cos(np.linspace(-np.pi, np.pi, 4001))
    rows = []
    for gm in (0.1, 0.5, 0.6):
        Eh = np.array([np.linalg.eigvalsh([[x, -gm], [-gm, 0.0]]) for x in ek])
        Em = np.array([np.linalg.eigvalsh([[x, gm], [gm, 0.0]]) for x in ek])
        closed = (ek[:, None] + np.array([-1, 1]) * np.sqrt(ek[:, None] ** 2 + 4 * gm ** 2)) / 2
        rows.append((gm, (Eh[:, 1] - Eh[:, 0]).min(), Eh[:, 1].min() - Eh[:, 0].max(), 2 * (np.sqrt(1 + gm ** 2) - 1),
                     np.allclose(Eh, closed) and np.allclose(Eh, Em) and Eh[:, 0].max() < 0 < Eh[:, 1].min()))
    ok = all(abs(r[1] - 2 * r[0]) < 1e-6 and abs(r[2] - r[3]) < 1e-9 and r[4] for r in rows)
    ok = ok and np.allclose([r[2] for r in rows], [0.0100, 0.236, 0.332], atol=6e-4) and all(abs(r[2] / r[0] ** 2 - 1) < 0.1 for r in rows)
    R['gaps821'] = rows
    check('the bands of (8.21)', ok,
          'E_- < 0 < E_+ at every k, the same bands for +gamma and -gamma, the direct gap 2 gamma, and the indirect gap '
          '2(sqrt(t^2 + gamma^2) - t) = %.4f, %.3f and %.3f for gamma = 0.1, 0.5 and 0.6 against gamma^2/t = 0.01, 0.25, 0.36'
          % tuple(r[2] for r in rows))
    fwt = np.mean([np.abs(np.linalg.eigh(np.array([[x, -0.6], [-0.6, 0.0]]))[1][1, 0]) ** 2 for x in ek[:-1]])
    bdg = np.array([np.linalg.eigvalsh([[x, 0.5], [0.5, -x]]) for x in ek])
    hs_ = geometry.chain().get_hamiltonian()
    hs_.add_swave(0.5)
    sw = 2 * np.min(np.abs(hs_.get_bands(nk=400)[1]))
    check('the filling of the Kondo insulator and the BdG gap', abs(fwt - 0.5) < 1e-3 and abs(bdg[:, 1].min() - bdg[:, 0].max() - 1) < 1e-9
          and abs(sw - 1) < 1e-3,
          'the lower band holds one state per k and spin with the f weight %.3f for gamma = 0.6, the BdG gap is %.3f for '
          'Delta = 0.5, and add_swave(0.5) on the chain gives %.4f on 400 momenta' % (fwt, bdg[:, 1].min() - bdg[:, 0].max(), sw))
    rho, Dw = 0.5, 1.0
    flat = lambda J: Dw / (2 * np.sinh(1 / (4 * rho * J)))
    Ef = lambda g_, J: 2 * quad(lambda x: rho * (x - np.sqrt(x ** 2 + 4 * g_ ** 2)) / 2, -Dw, Dw)[0] + g_ ** 2 / J
    gmin = minimize_scalar(lambda g_: Ef(g_, 0.4), bounds=(0.01, 1.0), method='bounded', options={'xatol': 1e-9}).x
    chain_g = lambda JK: brentq(lambda g_: 2 * JK / np.pi * ellipk(1 / (1 + g_ ** 2)) / np.sqrt(1 + g_ ** 2) - 1, 1e-6, 10.0)
    gch = {JK: chain_g(JK) for JK in (0.3, 0.35, 0.6, 0.8)}
    from pyqula.kondolattice import KondoLatticeHamiltonian
    vq = {}
    for JK in (0.6, 0.8):
        hk2 = KondoLatticeHamiltonian(geometry.chain().get_hamiltonian(has_spin=True))
        hk2 = quiet(hk2.get_mean_field_hamiltonian, J=2 * JK, filling=0.5, nk=400, mf=([0.3 + 0j], [0.0]), T=2e-3, maxite=3000)
        vq[JK] = (abs(hk2.hybridization[0]), float(np.real(hk2.local_occupation[0])))
    ok = abs(flat(0.4) - 0.3121) < 1e-4 and abs(gmin - flat(0.4)) < 1e-5 and abs(gch[0.6] - 0.2827) < 1e-4 and abs(gch[0.8] - 0.5270) < 1e-4
    ok = ok and all(abs(vq[JK][0] - gch[JK]) < 2e-4 and abs(vq[JK][1] - 1) < 1e-6 for JK in vq)
    R['khamiltonian'] = hk2
    check('the self-consistent hybridization', ok,
          'the flat band of half width 1 gives %.4f at J_K = 0.4 from 4 rho J_K asinh(D/2 gamma) = 1 and %.4f from the minimum '
          'of the energy, the chain gives %.4f and %.4f at J_K = 0.6 and 0.8 from (2 J_K/pi) K(m)/sqrt(1 + gamma^2) = 1, and '
          'KondoLatticeHamiltonian with J = 2 J_K gives %.4f and %.4f with n_f = 1'
          % (flat(0.4), gmin, gch[0.6], gch[0.8], vq[0.6][0], vq[0.8][0]))
    gapc = lambda JK: 2 * (np.sqrt(1 + gch[JK] ** 2) - 1)
    slope = (np.log(gapc(0.35)) - np.log(gapc(0.3))) / (1 / 0.35 - 1 / 0.3)
    ratio = flat(0.1) ** 2 / Dw / (Dw * np.exp(-1 / (2 * rho * 0.1)))
    check('the Kondo scale', abs(slope + np.pi) < 0.02 and abs(ratio - 1) < 1e-3,
          'ln of the indirect gap of the chain against 1/J_K has the slope %.3f between 0.3 and 0.35, against -1/(2 rho) = -pi, '
          'and on the flat band gamma^2/D is %.4f D exp(-1/(2 rho J_K)) at J_K = 0.1' % (slope, ratio))

    # pyqula and dmrgpy
    g = geometry.triangular_lattice()
    h = g.get_hamiltonian()
    gen = h.get_hk_gen()
    qq = np.random.default_rng(6).uniform(0, 1, (10, 2))
    ferr = max(np.abs(np.linalg.eigvalsh(gen([a, b, 0.0])) - tri_band(a, b)).max() for a, b in qq)
    gen2 = g.get_hamiltonian(tij=[0.0, 1.0]).get_hk_gen()
    serr = max(np.abs(np.linalg.eigvalsh(gen2([a, b, 0.0])) - tri_band(a, b, 0.0, 1.0)).max() for a, b in qq)
    E60 = mesh_levels(h, 60)
    ok = np.allclose(g.a1[:2], [1, 0]) and np.allclose(g.a2[:2], [-0.5, np.sqrt(3) / 2]) and len(g.r) == 1 and h.intra.shape == (2, 2)
    ok = ok and ferr < 1e-12 and serr < 1e-12 and abs(E60.min() + 3) < 1e-9 and abs(E60.max() - 6) < 1e-9
    check('triangular_lattice', ok, 'a1 = (1, 0), a2 = (-1/2, sqrt3/2), one site, spinful by default, the band by hand to %.0e, '
          'from %.0f to %.0f, and tij=[0, 1] is +1 on the six second neighbors to %.0e' % (ferr, E60.min(), E60.max(), serr))
    k12 = (np.arange(1200) + 0.5) / 1200
    sf = {}
    for t2 in (0.0, -0.5, 0.5):
        eb = tri_band(*np.meshgrid(k12, k12, indexing='ij'), 1.0, t2)
        for nk in (10, 60):
            hh = g.get_hamiltonian(tij=[1.0, t2])
            hh.set_filling(0.5, nk=nk)
            z = -(np.linalg.eigvalsh(hh.get_hk_gen()([0.0, 0.0, 0.0]))[0] - tri_band(0, 0, 1.0, t2))
            sf[t2, nk] = (z, np.mean(eb < z), np.median(eb))
    want = {(0.0, 10): (-0.618, 0.529, -0.835), (-0.5, 10): (0.236, 0.513, 0.103), (0.5, 10): (-1.000, 0.495, -0.983),
            (0.0, 60): (-0.810, 0.5035, -0.835), (-0.5, 60): (0.073, 0.497, 0.103), (0.5, 60): (-1.000, 0.495, -0.983)}
    R['setfill'] = sf[0.0, 10]
    check('set_filling(0.5, nk=10)', all(np.allclose(sf[key], want[key], atol=1.5e-3) for key in want),
          ', '.join('t2=%+.1f nk=%d puts zero at %+.3f, the filling %.4f, half filling at %+.4f' % (key + sf[key]) for key in sorted(sf))
          + ', on a mesh of 1200 points per side')
    k = (np.arange(600) + 0.5) / 600
    K1, K2 = np.meshgrid(k, k, indexing='ij')
    hq = geometry.square_lattice().get_hamiltonian()
    nk, delta = 41, 0.05
    xs, ys, ws = (np.asarray(x) for x in hq.get_fermi_surface(e=0.0, delta=delta, nk=nk))
    eps_sq = 2 * (np.cos(2 * np.pi * xs) + np.cos(2 * np.pi * ys))
    werr = np.abs(ws - 2 * delta / (eps_sq ** 2 + delta ** 2)).max()
    top = ws > 0.9 * ws.max()
    first = top & (np.abs(xs) <= 0.5) & (np.abs(ys) <= 0.5)               # inside the first zone
    line = np.abs(np.abs(2 * np.pi * xs[first]) + np.abs(2 * np.pi * ys[first]) - np.pi).max()
    wrote = os.path.isfile('FERMI_MAP.OUT')
    xt, yt, wt = (np.asarray(x) for x in g.get_hamiltonian().get_fermi_surface(e=0.0, delta=0.375, nk=80))
    Wt = wt.reshape(80, 80)
    asym = np.abs(Wt - Wt.T).max() / Wt.max()
    kcart = 2 * np.pi * np.c_[xt, yt]
    av = [np.array([1.0, 0.0]), np.array([-0.5, np.sqrt(3) / 2]), np.array([0.5, np.sqrt(3) / 2])]
    et = 2 * sum(np.cos(kcart @ a_) for a_ in av)
    terr = np.abs(wt - 2 * 0.375 / (et ** 2 + 0.375 ** 2)).max()
    ok = len(xs) == nk * nk and xs[0] == xs[1] == -1 and ys[1] > ys[0] and xs.max() == 1 and werr < 1e-9 and abs(ws.max() - 2 / delta) < 1e-6
    ok = ok and line < 0.2 and wrote and asym > 0.9 and terr < 1e-9
    R['asym'] = asym
    check('get_fermi_surface', ok,
          'flat arrays of nk^2 entries from -1 to 1 in units of 2 pi over the lattice constant, the first index along kx, the '
          'weight sum delta/((e-E)^2+delta^2) over both spins to %.0e, the largest %.1f = 2/delta, the square lattice at half '
          'filling on |kx| + |ky| = pi, the triangular map %.2f away from its transpose, and it writes FERMI_MAP.OUT' % (max(werr, terr), ws.max(), asym))
    gk = geometry.kagome_lattice().get_hamiltonian(has_spin=False)
    hkk = gk.get_hk_gen()

    def kagome_bands(K1, K2):
        """The three bands of kagome_lattice() with the hopping +1, by hand, in reduced momenta."""
        M = np.zeros(np.shape(K1) + (3, 3))
        for (i, j), c_ in zip(((0, 1), (0, 2), (1, 2)), (np.cos(np.pi * K1), np.cos(np.pi * K2), np.cos(np.pi * (K2 - K1)))):
            M[..., i, j] = M[..., j, i] = 2 * c_
        return np.linalg.eigvalsh(M)
    qq = np.random.default_rng(8).uniform(0, 1, (10, 2))
    kerr = max(np.abs(np.linalg.eigvalsh(hkk([a, b, 0.0])) - kagome_bands(a, b)).max() for a, b in qq)
    k9 = (np.arange(960) + 0.5) / 960
    Ek = kagome_bands(*np.meshgrid(k9, k9, indexing='ij')).reshape(-1, 3)
    atK = np.linalg.eigvalsh(hkk([1 / 3, 2 / 3, 0.0]))
    ef_k = np.median(Ek)
    spread = [np.median(mesh_levels(gk, n, offset=o)) for n, o in ((120, 0.0), (180, 0.5))]
    check('kagome_lattice', kerr < 1e-12 and np.allclose(Ek[:, 0], -2) and np.allclose(atK, [-2, 1, 1]) and abs(ef_k + 0.4715) < 3e-4
          and Ek[:, 1].min() < ef_k < Ek[:, 1].max() and abs(np.mean(Ek < 1 - 1e-9) - 2 / 3) < 0.01 and all(abs(s_ + 0.4715) < 3e-3 for s_ in spread),
          'with the hopping +1 the flat band is the lowest, at -2, the Dirac points at K are at %.0f, the filling 2/3, and '
          'half filling puts the Fermi level at %.4f on 960 points per side, inside the middle band, and at %.4f and %.4f '
          'on meshes of 120 and 180' % (atK[1], ef_k, spread[0], spread[1]))
    hh = g.get_hamiltonian(); hh.add_onsite(-2.0); hh = H2HFH(hh, JK=0.25)
    M = dense(hh.intra)
    z = sorted(np.round(np.array(hh.geometry.r)[:, 2], 9))
    hh.add_onsite(1.0)
    M1 = np.real(np.diag(dense(hh.intra)))
    hJ = H2HFH(g.get_hamiltonian(), JK=0.0, J=0.025)
    kond = np.repeat(np.array(hJ.geometry.r)[:, 2] > 0, 2)
    fhop = [dense(t_.m)[np.ix_(kond, kond)] for t_ in hJ.get_multicell().hopping if np.abs(dense(t_.m)[np.ix_(kond, kond)]).max() > 1e-12]
    genJ = hJ.get_hk_gen()
    fl = np.array([np.linalg.eigvalsh(genJ([a, b, 0.0])[np.ix_(kond, kond)]) for a in k[::3] for b in k[::3]])
    fb_fill = np.mean(fl < 0)
    hb_ = H2HFH(g.get_hamiltonian(), JK=0.5)
    (kb, eb_, cb) = hb_.get_bands(operator="dispersive_electrons", kpath=["G", "K", "M", "G"])
    ok = z == [-0.5, 0.5] and np.allclose(M, [[-2, 0, 0.25, 0], [0, -2, 0, 0.25], [0.25, 0, 0, 0], [0, 0.25, 0, 0]])
    ok = ok and np.allclose(M1, [-1, -1, 1, 1]) and len(fhop) == 6 and all(np.allclose(np.abs(m), 0.025 * np.eye(2)) for m in fhop)
    ok = ok and abs(fb_fill - 0.529) < 1e-3 and np.min(cb) >= -1e-12 and np.max(cb) <= 1 + 1e-12 and np.min(cb) < 0.05 and np.max(cb) > 0.95
    check('H2HFH', ok,
          'the conduction site at z = -0.5 and the Kondo site at +0.5 at E = 0, JK is the hopping between them, J a hopping of '
          'the Kondo sites to six neighbors whose band set_filling puts at its filling %.3f at zero, an add_onsite after the '
          'call moves both levels, and the weight runs from %.2f to %.2f' % (fb_fill, np.min(cb), np.max(cb)))
    Ec = tri_band(K1, K2) - 2.0
    res = {}
    for JK in (0.25, 0.5, 1.0):
        E = mesh_levels(notebook_kondo(JK), 90)
        res[JK] = ((E[:, 2] - E[:, 1]).min(), E[:, 2].min() - E[:, 1].max())
    nfk = {JK: kondo_weight(notebook_kondo(JK), 60) for JK in (0.25, 0.5)}
    half = {}
    for ons in (-10.0, -2.0, 6.0):
        E = mesh_levels(notebook_kondo(0.5, onsite=ons), 30)
        half[ons] = (np.mean(E < 0), E[:, 1].max(), E[:, 2].min())
    hsq = notebook_kondo(0.5, onsite=0.0, lattice='square_lattice')
    Es = mesh_levels(hsq, 60)
    nsq = kondo_weight(hsq, 40)
    ok = abs(Ec.min() + 5) < 1e-3 and abs(Ec.max() - 4) < 1e-3 and abs(np.mean(Ec < 0) - 0.774) < 1e-3
    ok = ok and np.allclose([res[x][0] for x in res], [0.5, 1.0, 2.0], atol=2e-3) and np.allclose([res[x][1] for x in res], [0.028, 0.111, 0.429], atol=1.5e-3)
    ok = ok and all(abs(v_[0] - 0.5) < 1e-12 and v_[1] < 0 < v_[2] for v_ in half.values())
    ok = ok and abs(nfk[0.25] - 0.46) < 0.01 and abs(nfk[0.5] - 0.48) < 0.01 and abs(Es[:, 2].min() - Es[:, 1].max() - (np.sqrt(17) - 4)) < 1e-6 and abs(nsq - 1) < 1e-9
    R['kondo_cell'] = (res, nfk, half)
    check('the notebook cell of the Kondo lattice', ok,
          'the conduction band from %.0f to %.0f with %.3f below zero, JK = 0.25, 0.5 and 1.0 give the direct gaps %s and the '
          'indirect gaps %s, half of the states below zero for the onsite energies -10, -2 and 6, the Kondo sites hold %.2f '
          'and %.2f there, and the square lattice holds one with the indirect gap %.4f'
          % (Ec.min(), Ec.max(), np.mean(Ec < 0), ' '.join('%.2f' % res[x][0] for x in res), ' '.join('%.3f' % res[x][1] for x in res),
             nfk[0.25], nfk[0.5], Es[:, 2].min() - Es[:, 1].max()))
    ind = {}
    for J in (0.0, 0.025, 0.05):
        E = mesh_levels(notebook_kondo(0.5, onsite=-4.0, J=J), 90)
        ind[J] = (E[:, 2].min() - E[:, 1].max(), (E[:, 2] - E[:, 1]).min())
    ok = np.allclose([ind[J][0] for J in ind], [0.154, -0.062, -0.276], atol=1.5e-3) and all(abs(ind[J][1] - 1.0) < 3e-3 for J in ind)
    R['exchange'] = ind
    check('the notebook cell with exchange between the Kondo sites', ok,
          'the indirect gap is %+.3f at J = 0, %+.3f at J = 0.025 and %+.3f at J = 0.05, and the direct gap stays %.2f'
          % (ind[0.0][0], ind[0.025][0], ind[0.05][0], ind[0.05][1]))
    CS = sum((H_(ff[a_]) @ ff[b_] - 0.5 * nf * (a_ == b_)) @ H_(cc4[b_]) @ cc4[a_] for a_ in range(2) for b_ in range(2))
    hK = R['khamiltonian']                                           # J = 1.6, half-filled chain, T = 2e-3
    gen, T = hK.get_hk_gen(), hK.temperature
    s = 0.0
    for kq in np.arange(400) / 400:
        ee, vv = np.linalg.eigh(gen([kq, 0.0, 0.0]))
        o = expit(-ee / T)                                              # the Fermi function at the temperature T
        s += sum(np.sum(o * np.conj(vv[a_, :]) * vv[2 + a_, :]) for a_ in range(2))
    s /= 400
    Vrel = abs(hK.hybridization[0] + 0.8 * s)
    h0 = KondoLatticeHamiltonian(geometry.chain().get_hamiltonian(has_spin=True))
    h0 = quiet(h0.get_mean_field_hamiltonian, J=1.6, filling=0.5, nk=200, T=2e-3)
    h15 = KondoLatticeHamiltonian(geometry.chain().get_hamiltonian(has_spin=True))
    h15 = quiet(h15.get_mean_field_hamiltonian, J=1.5, filling=0.15, nk=150, mf=([0.3 + 0j], [0.0]))
    lam = (float(np.real(hK.constraint_lambda[0])), float(np.real(h15.constraint_lambda[0])), float(np.real(h15.local_occupation[0])))
    R['lambda'] = lam
    ok = np.allclose(CS, HK) and Vrel < 1e-4 and abs(h0.hybridization[0]) < 1e-9 and abs(lam[0]) < 1e-6 and abs(lam[1] + 1.12) < 0.01 and abs(lam[2] - 1) < 1e-4
    check('KondoLatticeHamiltonian', ok,
          'S_ab c^dag_b c_a = (c^dag sigma c).S on the 16 states, so its J is 2 J_K, the field %.4f is -(J/2) sum_s <c^dag_s f_s> '
          'to %.0e, a loop started from zero stays at %.0e, and constraint_lambda is %.0e at half filling and %.3f at the '
          'filling 0.15 with n_f = %.4f' % (np.real(hK.hybridization[0]), Vrel, abs(h0.hybridization[0]), abs(lam[0]), lam[1], lam[2]))
    sc1 = spinchain.Spin_Chain(["S=1/2"])
    sc1.set_hamiltonian(sc1.Sz[0])
    lv1 = np.sort(np.real(quiet(sc1.get_excited, n=2, mode="ED")))
    files = {}
    jobs = {'dmrgpy': lambda: dmrg_chain(8, 0.2, local=1.0).gs_energy(mode="DMRG"),
            'get_bands': lambda: geometry.chain().get_hamiltonian().get_bands(),
            'get_fermi_surface': lambda: geometry.square_lattice().get_hamiltonian().get_fermi_surface(nk=10)}
    for name, job in jobs.items():
        here = os.getcwd()
        os.chdir(tempfile.mkdtemp(dir=here))
        try:
            quiet(job)
            files[name] = sorted(os.listdir('.'))
        finally:
            os.chdir(here)
    check('dmrgpy and the files', np.allclose(lv1, [-0.5, 0.5]) and files['dmrgpy'] == [] and 'BANDS.OUT' in files['get_bands']
          and 'FERMI_MAP.OUT' in files['get_fermi_surface'],
          'Spin_Chain with "S=1/2" has S^z = %s, a DMRG run wrote %s in its folder, get_bands wrote %s and get_fermi_surface %s'
          % (lv1.tolist(), files['dmrgpy'], files['get_bands'], files['get_fermi_surface']))

    # Open points of the old text
    c6, eU, eP = R['vison']
    check('open point, the flux of the ground state', c6 < -0.7 and eP < eU,
          'the flip lowers the energy by %.2f on the 6x6 lattice, and the pi-flux state has %.3f against %.3f' % (-c6, eP, eU))
    check('open point, the caption of Figure 8.2', R['triangle'][0] == 4 and abs(R['triangle'][1] - 0.75) < 1e-12,
          'the triangle of spins one half has a ground level of %d states with S(S+1) = %.2f' % R['triangle'])
    r6 = R['gaps821'][2]
    check('open point, the gap 2 gamma_K of a quiz of Section 8.12', abs(r6[2] - 0.332) < 1e-3 and abs(r6[1] - 1.2) < 1e-6,
          'for gamma = 0.6t the indirect gap is %.3f and the direct gap %.2f' % (r6[2], r6[1]))
    res, nfk, half = R['kondo_cell']
    check('open point, the JK of the notebook in Sections 8.12 and 8.13', abs(res[0.25][0] - 0.5) < 2e-3 and abs(res[0.5][0] - 1.0) < 2e-3
          and abs(nfk[0.5] - 0.48) < 0.01 and all(v_[1] < 0 < v_[2] for v_ in half.values()),
          'JK = 0.25 and 0.5 give the direct gaps %.2f and %.2f, zero is in the gap for every onsite energy tried, and the '
          'Kondo sites hold %.2f with add_onsite(-2.0)' % (res[0.25][0], res[0.5][0], nfk[0.5]))
    check('open point, the try-it box of Section 8.13', R['exchange'][0.025][0] < -0.05 and abs(R['exchange'][0.025][1] - 1) < 3e-3,
          'at J = 0.025 the bands overlap by %.3f and the direct gap is %.2f' % (-R['exchange'][0.025][0], R['exchange'][0.025][1]))
    check('open point, the local spin density of Section 8.11', R['twice'], 'c^dag sigma c is twice the spin density s')
    check('open point, the traceless form (8.19)', R['trace819'] < 1e-14,
          'the trace of (8.19) is %.0e on the empty, the singly and the doubly occupied states' % R['trace819'])
    check('open point, the only mean-field parameter', abs(R['lambda'][1] + 1.12) < 0.01 and abs(nfk[0.5] - 0.48) < 0.01,
          'with the f level at zero the notebook band gives %.2f f fermions per site, and constraint_lambda is %.2f at the '
          'filling 0.15' % (nfk[0.5], R['lambda'][1]))
    dz, eu_ = R['dimerized']
    check('open point, the uniform spinon chain as an ansatz', abs(dz) < 1e-9 and abs(eu_ - 0.0474) < 1e-4,
          'the dimerized state has %.0e per bond and the uniform one %.4f' % (dz, eu_))
    check('open point, the phase of the bond variable in Section 8.10', R['phases'],
          'the coefficient of (8.15) gets e^{+i(theta_i - theta_j)} and the operator of (8.12) e^{-i(theta_i - theta_j)}')
    check('open point, the order of the pairs in the caption of rvb_plaquette', np.allclose(R['overlaps'], [0.5, -0.5]),
          '<a|b> is %+.1f with (30) and %+.1f with (03)' % R['overlaps'])
    check('open point, the notebook', R['asym'] > 0.9 and abs(R['setfill'][1] - 0.529) < 1e-3,
          'the triangular map differs from its transpose by %.2f of its largest value, and nk=10 gives the filling %.3f'
          % (R['asym'], R['setfill'][1]))
    print('%d checks hold, %.1f s' % (COUNT[0], time.time() - t0))


if __name__ == '__main__':
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            main()
        finally:
            os.chdir(cwd)
