"""Checks of webnotes/conventions/session07.md, with numbers. Every line of the sheet is asserted here, in the order of
the sheet, and the script prints one line per line of the sheet and exits 0 when all hold.

The routes are numpy and scipy (exact diagonalization with site i as bit i of the basis index, correlation matrices
of free fermions, the Bogoliubov-de Gennes matrix of the transverse-field Ising chain, a one-site variational sweep,
counting), pyqula (free fermions) and dmrgpy (matrix product states). The dmrgpy numbers come from a variational
calculation, so they are asserted with a margin, and a number that changes from run to run is asserted as a range or
as a bound. The figure scripts of webnotes/figures/session07/ and the notebooks are read, not run.

Not asserted: what the figures s07f02 to s07f06 draw (the tetramers of s07f02 on the 2 x 2 blocks, with the squares
offset by one site, were read from its image), the times that the notebook cells measure, the scan of the transverse-field Ising chain on the 50 fields of the notebook (three fields
are run), and the cause of the wrong spinful entropy of pyqula on a ring of 300 cells.

Run it from anywhere:  python3 webnotes/checks/session07/conventions.py"""
import contextlib, io, itertools, json, os, re, sys, tempfile, time, warnings
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spl
from scipy.sparse.linalg import expm_multiply

warnings.filterwarnings('ignore')
WEBNOTES = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO = os.path.dirname(WEBNOTES)
FIGS = os.path.join(WEBNOTES, 'figures', 'session07')
if os.environ.get('DMRGROOT'):
    sys.path.append(os.environ['DMRGROOT'])
LN2 = np.log(2)
COUNT = [0]
R = {}      # numbers kept for the last section of the sheet


def check(name, ok, detail):
    """Prints one line for a check and stops the script when it does not hold."""
    print(('ok    ' if ok else 'FAIL  ') + name + ': ' + detail, flush=True)
    assert ok, name
    COUNT[0] += 1


def source(name, folder=FIGS):
    return open(os.path.join(folder, name), encoding='utf-8').read()


def notebook(n):
    """The code and text of the cells of jupyter-notebooks/sessionN.ipynb, as a list of strings."""
    nb = json.load(open(os.path.join(REPO, 'jupyter-notebooks', 'session%d.ipynb' % n), encoding='utf-8'))
    return [''.join(c['source']) for c in nb['cells']]


def cell(cells, heading):
    """The first code cell after the markdown cell that starts with this heading."""
    i = next(i for i, c in enumerate(cells) if c.lstrip('# ').startswith(heading.lstrip('# ')))
    return cells[i + 1]


# ------------------------------------------------------------------ exact diagonalization, site i is bit i

SX, SY, SZ = np.array([[0, 1], [1, 0]]) / 2, np.array([[0, -1j], [1j, 0]]) / 2, np.diag([0.5, -0.5])
SP, SM = np.array([[0, 1], [0, 0.]]), np.array([[0, 0], [1, 0.]])          # basis (up, down)


def kron_site(o, i, L):
    """The one-site operator o on site i of L sites as a dense matrix, site 0 is the first factor of np.kron."""
    m = np.eye(1)
    for j in range(L):
        m = np.kron(m, o if j == i else np.eye(len(o)))
    return m


def states(L, nup=None):
    s = np.arange(2 ** L, dtype=np.int64)
    return s if nup is None else s[np.bitwise_count(s) == nup]


def heis(L, bonds, nup=None, field=None):
    """Sparse sum of J S_i.S_j over the bonds (i, j, J), plus sum_i field_i S^z_i, on the states with nup up spins
    (all states if None). Site i is bit i of the index, and the bit 1 is an up spin."""
    st = states(L, nup)
    diag = np.zeros(len(st))
    rows, cols, vals = [], [], []
    for i, j, J in bonds:
        a, b = (st >> i) & 1, (st >> j) & 1
        diag += J * np.where(a == b, 0.25, -0.25)
        f = np.nonzero(a != b)[0]
        rows.append(f); cols.append(np.searchsorted(st, st[f] ^ ((1 << i) | (1 << j)))); vals.append(np.full(len(f), 0.5 * J))
    if field is not None:
        for i, B in enumerate(field):
            diag += B * (((st >> i) & 1) - 0.5)
    H = sps.csr_matrix((np.concatenate(vals) if vals else [], (np.concatenate(rows) if rows else [],
                        np.concatenate(cols) if cols else [])), shape=(len(st), len(st)))
    return (H + sps.diags(diag)).tocsr(), st


def chain_bonds(J):
    return [(i, i + 1, Jb) for i, Jb in enumerate(J)]


def lowest(H, k=1):
    """The k lowest levels and their states."""
    if H.shape[0] <= 1500:
        w, v = np.linalg.eigh(H.toarray())
        return w[:k], v[:, :k]
    w, v = spl.eigsh(H, k=k, which='SA', tol=1e-13, v0=np.random.default_rng(0).normal(size=H.shape[0]))
    o = np.argsort(w)
    return w[o], v[:, o]


def full(v, st, L):
    out = np.zeros(2 ** L, dtype=v.dtype)
    out[st] = v
    return out


def dense(m):
    return m.toarray() if sps.issparse(m) else np.asarray(m)


def vn(w):
    w = np.asarray(w)
    w = w[w > 1e-16]
    return float(-np.sum(w * np.log(w)))


def ent(psi, L, sites):
    """Entropy of a set of sites, for a full vector with site i as bit i."""
    t = psi.reshape((2,) * L)                   # axis a is the bit L-1-a
    ax = [L - 1 - s for s in sites]
    m = np.transpose(t, ax + [a for a in range(L) if a not in ax]).reshape(2 ** len(sites), -1)
    return vn(np.linalg.svd(m, compute_uv=False) ** 2)


def cuts(psi, L):
    """Entropy of the first l sites for l = 1 to L-1."""
    return np.array([vn(np.linalg.svd(psi.reshape(2 ** (L - l), 2 ** l), compute_uv=False) ** 2) for l in range(1, L)])


def ground(L, J, nup=None):
    """Ground energy and full ground vector of the open chain with the bonds J, in the sector S^z = 0."""
    H, st = heis(L, chain_bonds(J), L // 2 if nup is None else nup)
    e, v = lowest(H)
    return e[0], full(v[:, 0], st, L)


def dimerized(L, J1, J2):
    """The couplings of the dimerized chain, J1 on the bonds (0,1), (2,3), ... and J2 on (1,2), (3,4), ..."""
    return [J1 if i % 2 == 0 else J2 for i in range(L - 1)]


# ------------------------------------------------------------------ free fermions

def corr(hop):
    """Correlation matrix <c_i^dag c_j> of the levels below zero of a single-particle matrix."""
    w, v = np.linalg.eigh(hop)
    occ = v[:, w < 0]
    return occ.conj() @ occ.T


def ff(C, sites):
    nu = np.linalg.eigvalsh(C[np.ix_(sites, sites)])
    nu = nu[(nu > 1e-13) & (nu < 1 - 1e-13)]
    return float(-np.sum(nu * np.log(nu) + (1 - nu) * np.log(1 - nu)))


def hop_chain(t, ring=False):
    """Single-particle matrix with the hopping t[i] on the bond (i, i+1), and on (N-1, 0) for a ring."""
    N = len(t) + (0 if ring else 1)
    h = np.zeros((N, N))
    for i, ti in enumerate(t):
        h[i, (i + 1) % N] = h[(i + 1) % N, i] = ti
    return h


def infinite_corr(n):
    """C_ij of the infinite chain with hopping 1 at half filling, for n consecutive sites."""
    d = np.arange(n)[:, None] - np.arange(n)[None, :]
    with np.errstate(all='ignore'):
        return np.where(d == 0, 0.5, np.sin(np.pi * d / 2) / (np.pi * d))


def ring_corr(n, N):
    """The same on a ring of N = 2 mod 4 sites, with the N/2 levels |k| < pi/2 filled."""
    d = np.arange(n)[:, None] - np.arange(n)[None, :]
    with np.errstate(all='ignore'):
        return np.where(d == 0, 0.5, np.sin(np.pi * d / 2) / (N * np.sin(np.pi * d / N)))


def tfim(L, Bx, J=0.25, field=None):
    """The open chain -J sum sigma^z sigma^z + (Bx/2) sum sigma^x, the notebook form for J=1/4, by Jordan-Wigner with
    sigma^x = 1 - 2n. Returns the ground energy and G = <Psi Psi^dag> for Psi = (c, c^dag)."""
    g = Bx / 2 if field is None else field
    A = np.diag(np.full(L, -2 * g)) + np.diag(np.full(L - 1, -J), 1) + np.diag(np.full(L - 1, -J), -1)
    D = np.diag(np.full(L - 1, -J), 1) - np.diag(np.full(L - 1, -J), -1)
    M = np.block([[A, D], [-D.conj(), -A.conj()]])
    w, v = np.linalg.eigh(M)
    pos = v[:, w > 0]
    return -0.5 * np.sum(w[w > 0]) + 0.5 * np.trace(A) + g * L, pos @ pos.conj().T


def tfim_entropy(G, L, l):
    idx = list(range(l)) + [L + i for i in range(l)]
    g = np.linalg.eigvalsh(G[np.ix_(idx, idx)])
    g = g[(g > 1e-14) & (g < 1 - 1e-14)]
    return float(-0.5 * np.sum(g * np.log(g) + (1 - g) * np.log(1 - g)))


# ------------------------------------------------------------------ dmrgpy

def spin_chain(L, J=None, field=None, maxm=None):
    """A dmrgpy chain of spins 1/2 with sum_i J_i S_i.S_{i+1} + sum_i field_i S^z_i, and its Hamiltonian."""
    from dmrgpy import spinchain
    sc = spinchain.Spin_Chain(["S=1/2"] * L)
    J = [1.0] * (L - 1) if J is None else J
    h = 0
    for i, Jb in enumerate(J):
        h = h + Jb * (sc.Sx[i] * sc.Sx[i + 1] + sc.Sy[i] * sc.Sy[i + 1] + sc.Sz[i] * sc.Sz[i + 1])
    if field is not None:
        for i, B in enumerate(field):
            h = h + B * sc.Sz[i]
    sc.set_hamiltonian(h)
    if maxm:
        sc.maxm = maxm
    return sc, h


def bond_entropies(wf, L):
    """get_bond_entropy(i, i+1) for i = 0 to L-2, the entropy of the first i+1 sites."""
    return np.array([wf.get_bond_entropy(i, i + 1) for i in range(L - 1)])


def quiet(f, *a, **k):
    """Calls f with the messages of dmrgpy and ITensor kept out of the output."""
    with contextlib.redirect_stdout(io.StringIO()):
        return f(*a, **k)


# ------------------------------------------------------------------ matrix product states

def mps_full(A):
    """The full vector of an open MPS, a list of tensors (left, physical, right), site 0 first in np.kron order."""
    T = A[0]
    for B in A[1:]:
        T = np.einsum('xsa,atb->xstb', T, B).reshape(1, -1, B.shape[2])
    return T.reshape(-1)


def random_mps(L, M, rng, d=2):
    D = [1] + [min(M, d ** min(k, L - k)) for k in range(1, L)] + [1]
    return [rng.normal(size=(D[k], d, D[k + 1])) + 1j * rng.normal(size=(D[k], d, D[k + 1])) for k in range(L)]


def heis_mpo():
    """The MPO tensor W[a, b] of the Heisenberg chain, bond dimension 5, with I, S+, S-, Sz in the first column and
    S-/2, S+/2, Sz, I in the last row. The left end is the last row and the right end the first column."""
    W = np.zeros((5, 5, 2, 2), complex)
    W[0, 0] = W[4, 4] = np.eye(2)
    W[1, 0], W[2, 0], W[3, 0] = SP, SM, SZ
    W[4, 1], W[4, 2], W[4, 3] = SM / 2, SP / 2, SZ
    return W


def sweeps(H, L, M, seed, nsweeps=3):
    """A one-site variational sweep from the random start of dmrg_sweeps.py, written again: each update is the exact
    minimum of the energy over one tensor with the others fixed. Returns the energy after every update."""
    rng = np.random.default_rng(seed)
    D = [1] + [min(M, 2 ** min(k, L - k)) for k in range(1, L)] + [1]
    A = [rng.normal(size=(D[k], 2, D[k + 1])) for k in range(L)]
    out = []
    for k in itertools.chain.from_iterable([list(range(L)) + list(range(L - 2, 0, -1))] * nsweeps):
        left = np.ones((1, 1))
        for j in range(k):
            left = np.einsum('xa,asb->xsb', left, A[j]).reshape(-1, D[j + 1])
        right = np.ones((1, 1))
        for j in range(L - 1, k, -1):
            right = np.einsum('asb,by->asy', A[j], right).reshape(D[j], -1)
        B = np.einsum('la,st,br->lsratb', left, np.eye(2), right).reshape(2 ** L, -1)
        U, sv, Vt = np.linalg.svd(B, full_matrices=False)
        keep = sv > 1e-11 * sv[0]
        U = U[:, keep]                                                 # the states that this tensor can reach
        e, y = np.linalg.eigh(U.T @ (H @ U))
        A[k] = (Vt[keep].T @ (y[:, 0] / sv[keep])).reshape(D[k], 2, D[k + 1])
        out.append(e[0])
    return np.array(out)


def main():
    from pyqula import geometry, pyqula2dmrgpy
    t0 = time.time()
    nb7 = notebook(7)

    # ---------------------------------------------------------------- spins, units and the numbering of sites
    dimer = sum(kron_site(s, 0, 2) @ kron_site(s, 1, 2) for s in (SX, SY, SZ)).real
    lev = np.linalg.eigvalsh(dimer)
    th = np.linspace(0, np.pi, 7)
    prod = []
    for a in th:
        u, w = np.array([np.cos(a / 2), np.sin(a / 2)]), np.array([1, 0.])
        psi = np.kron(w, u)
        prod.append(psi @ dimer @ psi)
    sing = np.array([0, 1, -1, 0]) / np.sqrt(2)
    sz0 = sing @ kron_site(SZ, 0, 2) @ sing
    sc, h = spin_chain(2)
    e2 = quiet(sc.gs_energy)
    s00 = quiet(sc.vev, sc.Sx[0] * sc.Sx[0] + sc.Sy[0] * sc.Sy[0] + sc.Sz[0] * sc.Sz[0]).real
    check('spins and the dimer', np.allclose(lev, [-0.75, 0.25, 0.25, 0.25]) and np.allclose(prod, np.cos(th) / 4)
          and abs(sz0) < 1e-15 and abs(e2 + 0.75) < 1e-9 and abs(s00 - 0.75) < 1e-9,
          'S0.S1 has %s, a product state at the angle a has cos(a)/4 from -0.25 to +0.25, the singlet <S^z_0> = %.0f, '
          'dmrgpy gives %.4f for two sites and <S_0.S_0> = %.4f' % (lev.round(4), sz0, e2, s00))

    f = lambda t: vn([np.cos(t) ** 2, np.sin(t) ** 2])
    vals = [f(0), f(np.pi / 8), f(np.pi / 4)]
    psi = np.array([0, 1, -1, 0]) / np.sqrt(2)                         # kron order, (up down) - (down up)
    s_sing = vn(np.linalg.svd(psi.reshape(2, 2), compute_uv=False) ** 2)
    check('the natural logarithm and the two-spin states', np.allclose(vals, [0, 0.4165, LN2], atol=5e-5)
          and abs(s_sing - LN2) < 1e-12 and abs(f(-np.pi / 4) - LN2) < 1e-12,
          'S = %.4f, %.4f, %.4f at t = 0, pi/8, pi/4, and the singlet, t = -pi/4, has %.4f = ln 2' % (*vals, s_sing))

    L = 10
    e10, psi10 = ground(L, [1.0] * (L - 1))
    S_ed = cuts(psi10, L)
    sc, h = spin_chain(L)
    wf = quiet(sc.get_gs, mode="DMRG")
    S_dm = bond_entropies(wf, L)
    nbcut = 'get_bond_entropy(L//2,L//2+1)' in cell(nb7, '## Size dependence').replace(' ', '')
    plotcut = 'get_bond_entropy(i-1,i)foriinrange(1,L)' in cell(nb7, '## Entanglement entropy of the ground').replace(' ', '')
    check('sites from 0 and the cut of get_bond_entropy', np.abs(S_ed - S_dm).max() < 1e-7 and nbcut and plotcut,
          'Heisenberg chain of 10 sites, the entropy of the first i+1 sites by ED %s, dmrgpy get_bond_entropy(i, i+1) '
          'agrees to %.0e, and the notebook calls get_bond_entropy(L//2, L//2+1) and plots get_bond_entropy(j, j+1) at j'
          % (S_ed.round(4), np.abs(S_ed - S_dm).max()))
    R['heis10'] = S_ed

    kron_scripts = ['schmidt_spectrum.py', 'dmrg_sweeps.py', 'quench_entropy.py', 'xx_spectrum.py', 'dimer_entropy.py']
    bit_scripts = ['random_vs_gapped.py', 'matrix_vs_vector.py']
    ok = all('kron' in source(s) and '>>' not in source(s) for s in kron_scripts)
    ok = ok and all('>> i' in source(s) and 'kron' not in source(s) for s in bit_scripts)
    ok = ok and 'reshape(2 ** (L - l), 2 ** l)' in source('random_vs_gapped.py')
    L, l = 8, 3
    Hk = sum(kron_site(s, i, L) @ kron_site(s, i + 1, L) for i in range(L - 1) for s in (SX, SY, SZ)).real + 0.3 * kron_site(SZ, 0, L)
    vk = np.linalg.eigh(Hk)[1][:, 0]
    Hb, st = heis(L, chain_bonds([1.0] * (L - 1)), field=[0.3] + [0] * (L - 1))
    vb = np.linalg.eigh(Hb.toarray())[1][:, 0]
    sk = vn(np.linalg.svd(vk.reshape(2 ** l, -1), compute_uv=False) ** 2)
    sb = vn(np.linalg.svd(vb.reshape(-1, 2 ** l), compute_uv=False) ** 2)
    wrong = vn(np.linalg.svd(vb.reshape(2 ** l, -1), compute_uv=False) ** 2)
    check('the two storage orders of the figure scripts', ok and abs(sk - sb) < 1e-12 and abs(wrong - sb) > 0.01,
          'np.kron with site 0 first in %s, bit i in %s; with a field 0.3 on site 0 of 8 sites the first 3 sites give '
          '%.4f with reshape(2**l, -1) on the kron state and %.4f with reshape(-1, 2**l) on the bit state, and %.4f with '
          'the wrong reshape' % (', '.join(kron_scripts), ', '.join(bit_scripts), sk, sb, wrong))

    # ---------------------------------------------------------------- the Jordan-Wigner transformation
    L = 5
    n = np.diag([1.0, 0.0])                                            # up is occupied
    Kd = [np.eye(2 ** L)]
    for i in range(1, L):
        Kd.append(Kd[-1] @ kron_site(np.eye(2) - 2 * n, i - 1, L))
    N = [kron_site(n, i, L) for i in range(L)]
    c = [Kd[i] @ kron_site(SM, i, L) for i in range(L)]
    err = max(np.abs(c[i] @ c[j].T + c[j].T @ c[i] - (i == j) * np.eye(2 ** L)).max() + np.abs(c[i] @ c[j] + c[j] @ c[i]).max()
              for i in range(L) for j in range(L))
    err2 = max(np.abs(c[i].T @ Kd[i] - kron_site(SP, i, L)).max() + np.abs(kron_site(SZ, i, L) - N[i] + 0.5 * np.eye(2 ** L)).max()
               for i in range(L))
    import scipy.linalg as sla
    err3 = max(np.abs(sla.expm(1j * np.pi * sum(N[:i], np.zeros((2 ** L, 2 ** L)))) - Kd[i]).max() for i in range(L))
    k6 = [np.prod([1 - 2 * x for x in occ]) for occ in ([1, 0, 1, 1, 0, 0], [0, 1, 0, 0, 1, 0])]
    check('the string of (7.2)', err < 1e-12 and err2 < 1e-12 and err3 < 1e-12 and k6 == [-1, 1] and np.allclose(Kd[0], np.eye(2 ** L)),
          'on 5 sites c_i = K_i S^-_i anticommute to %.0e, c_i^dag K_i = S^+_i and S^z_i = n_i - 1/2 to %.0e, '
          'exp(i pi sum n) = prod(1 - 2n) to %.0e, K_6 = %+d with three fermions on the sites 0 to 5 and %+d with two, '
          'K_0 = 1' % (err, err2, err3, k6[0], k6[1]))

    nb_err = max(np.abs(kron_site(SP, i, L) @ kron_site(SM, i + 1, L) - c[i].T @ c[i + 1]).max()
                 + np.abs(kron_site(SM, i, L) @ kron_site(SP, i + 1, L) - c[i + 1].T @ c[i]).max() for i in range(L - 1))
    L, J = 6, 1.0
    Hs = sum(J * (kron_site(SX, i, L) @ kron_site(SX, i + 1, L) + kron_site(SY, i, L) @ kron_site(SY, i + 1, L))
             for i in range(L - 1)).real
    ups = np.array([L - bin(x).count('1') for x in range(2 ** L)])     # kron order, the bit 0 is up
    eps = J * np.cos(np.pi * np.arange(1, L + 1) / (L + 1))
    eps_m = np.linalg.eigvalsh(hop_chain([-J / 2] * (L - 1)))
    hf = geometry.chain().get_hamiltonian(has_spin=False).set_finite_system(n=L)
    hf.intra = 0.5 * J * hf.intra
    eps_q = np.linalg.eigvalsh(dense(hf.intra))
    sec = 0.0
    for Nf in range(L + 1):
        sel = np.nonzero(ups == Nf)[0]
        spin = np.linalg.eigvalsh(Hs[np.ix_(sel, sel)])
        free = np.sort([sum(x) for x in itertools.combinations(eps, Nf)])
        sec = max(sec, np.abs(spin - free).max())
    check('neighbors and the XX chain', nb_err < 1e-12 and sec < 1e-12 and np.allclose(np.sort(eps), eps_m)
          and np.allclose(np.sort(eps), eps_q),
          'S^+_i S^-_(i+1) = c^dag_i c_(i+1) and S^-_i S^+_(i+1) = c^dag_(i+1) c_i to %.0e, the 64 levels of 6 spins are '
          'the sums of J cos(pi k/7) in each sector N = S^z_tot + 3 to %.0e, and the hopping -J/2 and pyqula chain() '
          'with the hopping 1/2 give the same levels' % (nb_err, sec))

    L = 8
    eH, _ = ground(L, [1.0] * (L - 1))
    exx = np.sum(np.linalg.eigvalsh(hop_chain([0.5] * (L - 1)))[:L // 2])
    hf = geometry.chain().get_hamiltonian(has_spin=False).set_finite_system(n=L)
    hf.intra = 0.5 * hf.intra
    fc = quiet(pyqula2dmrgpy.generate_fermionic_chain, hf)
    exx_dm = quiet(fc.gs_energy, mode="ED")
    V = sum((fc.N[i] - 0.5) * (fc.N[i + 1] - 0.5) for i in range(L - 1))
    fc.set_hamiltonian(fc.hamiltonian + V)
    eH_dm = quiet(fc.gs_energy, mode="ED")
    check('the Heisenberg chain is not free', abs(eH + 3.374933) < 1e-6 and abs(eH_dm - eH) < 1e-8 and abs(exx + 2.379385) < 1e-6
          and abs(exx_dm - exx) < 1e-8,
          '8 sites, the spins give %.6f, the dmrgpy fermions with (n_i - 1/2)(n_(i+1) - 1/2) %.6f, the free part alone '
          '%.6f, and the dmrgpy fermions of pyqula2dmrgpy without the interaction %.6f' % (eH, eH_dm, exx, exx_dm))

    L = 10
    Hxx, st = heis(L, [(i, i + 1, 1.0) for i in range(L - 1)], L // 2)
    Hxx = Hxx - sps.diags(Hxx.diagonal())                              # the XX chain, without S^z S^z
    e, v = lowest(Hxx)
    pxx = full(v[:, 0], st, L)
    S_sp = cuts(pxx, L)
    Cxx = corr(hop_chain([0.5] * (L - 1)))
    S_ff = np.array([ff(Cxx, list(range(l))) for l in range(1, L)])
    hf = geometry.chain().get_hamiltonian(has_spin=False).set_finite_system(n=L)
    hf.intra = 0.5 * hf.intra
    fc = quiet(pyqula2dmrgpy.generate_fermionic_chain, hf)
    wf = quiet(fc.get_gs, mode="DMRG")
    S_dm = bond_entropies(wf, L)
    e_dm = quiet(fc.gs_energy, mode="DMRG")
    L2 = 12
    H12, st12 = heis(L2, [(i, i + 1, 1.0) for i in range(L2 - 1)], L2 // 2)
    H12 = H12 - sps.diags(H12.diagonal())
    p12 = full(lowest(H12)[1][:, 0], st12, L2)
    C12 = corr(hop_chain([0.5] * (L2 - 1)))
    mid = (ent(p12, L2, [3, 4, 5, 6]), ff(C12, [3, 4, 5, 6]))
    mid5 = (ent(p12, L2, [3, 4, 5, 6, 7]), ff(C12, [3, 4, 5, 6, 7]))
    two = (ent(p12, L2, [1, 2, 3, 8, 9]), ff(C12, [1, 2, 3, 8, 9]))
    check('the entropy in the two languages', abs(e[0] + 3.01334) < 1e-5 and abs(e_dm - e[0]) < 1e-6
          and np.abs(S_sp - S_ff).max() < 1e-9 and np.abs(S_dm - S_ff).max() < 1e-5 and abs(S_sp[0] - LN2) < 1e-12
          and abs(S_sp[4] - 0.7578) < 5e-5 and abs(mid[0] - mid[1]) < 1e-9 and abs(mid[0] - 1.2666) < 5e-5
          and abs(mid5[0] - mid5[1]) < 1e-9 and abs(two[0] - 1.7365) < 5e-5 and abs(two[1] - 1.8007) < 5e-5,
          'XX chain of 10 sites, the energy %.5f from the spins and %.5f from the dmrgpy fermions, the first sites give '
          'the same entropies with spins, the fermion correlation matrix and dmrgpy, %.4f at the first cut and %.4f at '
          'the center; 12 sites, the sites 3 to 6 give %.4f and %.4f, the sites 3 to 7 %.4f and %.4f, and the sites 1 to '
          '3 with 8 and 9 give %.4f with spins and %.4f with fermions'
          % (e[0], e_dm, S_sp[0], S_sp[4], *mid, *mid5, *two))

    L = 5
    wrap = kron_site(SP, L - 1, L) @ kron_site(SM, 0, L)
    jw = c[L - 1].T @ c[0]
    Nf_op = np.diag(sum(N)).real
    ok = all(np.allclose(wrap[:, Nf_op == Nf], -(-1) ** Nf * jw[:, Nf_op == Nf]) for Nf in range(L + 1))
    rings = []
    for L in (6, 8):
        Hr, st = heis(L, [(i, (i + 1) % L, 1.0) for i in range(L)], L // 2)
        Hr = Hr - sps.diags(Hr.diagonal())
        espin = lowest(Hr)[0][0]
        k = 2 * np.pi * (np.arange(L) + (0.5 if (L // 2) % 2 == 0 else 0)) / L
        efree = np.sum(np.sort(np.cos(k))[:L // 2])
        rings.append((L, espin, efree))
    check('the bond that closes a ring', ok and all(abs(a - b) < 1e-10 for _, a, b in rings),
          'S^+_(L-1) S^-_0 = -(-1)^N c^dag_(L-1) c_0 in every sector of 5 sites, and the XX rings of %d and %d sites '
          'have %.6f and %.6f, the free fermions with periodic conditions for N = 3 and antiperiodic for N = 4 give '
          '%.6f and %.6f' % (rings[0][0], rings[1][0], rings[0][1], rings[1][1], rings[0][2], rings[1][2]))

    # ---------------------------------------------------------------- the size of the Hilbert space and the memory
    dims = [2 ** L for L in (2, 3, 4)]
    check('the dimension', dims == [4, 8, 16] and 2 ** 11 - 2 ** 10 == 1024,
          '2^L is %s for L = 2, 3, 4, and the step from 10 to 11 sites adds %d' % (dims, 2 ** 11 - 2 ** 10))

    b = 16
    first = next(L for L in range(1, 60) if b * 2 ** L > 1e9)
    dense_L = next(L for L in range(1, 60) if b * 4 ** L > 1e9)
    lines = all('1e9 / 16' in source(s) for s in ('memory_scaling.py', 'matrix_vs_vector.py'))
    b30, b40 = b * 2 ** 30, b * 2 ** 40
    check('bytes', np.zeros(1, complex).itemsize == 16 and lines and first == 26 and b * 2 ** 26 == 2 ** 30 and dense_L == 13
          and abs(b30 / 1e9 - 17.18) < 0.01 and b30 == 16 * 2 ** 30 and abs(b40 / 1e12 - 17.59) < 0.01 and b40 == 16 * 2 ** 40,
          'a complex number is 16 bytes, the dashed lines are 1e9/16 numbers, the state passes 1e9 bytes at L = %d with '
          '2^30 = %.3e bytes, the dense matrix at L = %d, L = 30 needs %.3e bytes = %.1f GB = 16 GiB, L = 40 needs %.3e '
          'bytes = %.1f TB = 16 TiB' % (first, 2.0 ** 30, dense_L, b30, b30 / 1e9, b40, b40 / 1e12))

    nnz = {}
    for L in (4, 5, 6, 7, 8, 10, 12):
        H, st = heis(L, chain_bonds([1.0] * (L - 1)))
        H.eliminate_zeros()
        nnz[L] = H.nnz
    Hk8 = sum(kron_site(s, i, 8) @ kron_site(s, i + 1, 8) for i in range(7) for s in (SX, SY, SZ)).real
    even = all(nnz[L] == (L + 1) * 2 ** (L - 1) for L in (4, 6, 8, 10, 12))
    check('the nonzero elements', even and np.count_nonzero(np.abs(Hk8) > 1e-14) == nnz[8] and nnz[5] == 84 and nnz[7] == 472,
          'the open Heisenberg chain in the S^z basis has %s nonzero elements for L = 4, 6, 8, 10, 12, which is (L+1) 2^(L-1), '
          'the np.kron matrix of 8 sites has the same, and L = 5, 7 have %d and %d against 96 and 512'
          % ([nnz[L] for L in (4, 6, 8, 10, 12)], nnz[5], nnz[7]))

    # ---------------------------------------------------------------- matrix product states
    def count(L, M, d=2, cap=True):
        D = [1] + [min(M, d ** min(k, L - k)) if cap else M for k in range(1, L)] + [1]
        return sum(d * D[k] * D[k + 1] for k in range(L)), D
    n100, _ = count(100, 10)
    n100u, _ = count(100, 10, cap=False)
    n1 = count(100, 1)[0], count(40, 1)[0]
    nex, Dex = count(10, 2 ** 10)
    draws = 'L * M ** 2.0' in source('memory_scaling.py')
    trace = sum(2 * 10 * 10 for k in range(100))      # the trace form (10.6) of Session 10, a D x D matrix on every site
    check('the number of numbers of an MPS', n100 == 18888 and n100u == 19640 and 2 * 100 * 10 ** 2 == 20000 and n1 == (200, 80)
          and draws and trace == 20000, 'L = 100 and M = 10 give %d with every bond capped at min(M, 2^k, 2^(L-k)) and %d '
          'with vectors at the ends, 2 L M^2 = 20000, the trace form of Session 10 with D = 10 has %d, M = 1 gives %d for '
          '100 sites and %d for 40, and memory_scaling.py draws L M^2' % (n100, n100u, trace, *n1))
    R['mps'] = (n100, n100u)

    rng = np.random.default_rng(7)
    L = 10
    psi = mps_full(random_mps(L, 4, rng))
    rk = [int(np.linalg.matrix_rank(psi.reshape(2 ** l, -1), tol=1e-10 * np.abs(psi).max())) for l in range(1, L)]
    rr = rng.normal(size=2 ** L)
    rk2 = [int(np.linalg.matrix_rank(rr.reshape(2 ** l, -1))) for l in range(1, L)]
    check('the Schmidt rank', rk == [2, 4, 4, 4, 4, 4, 4, 4, 2] and rk2 == [2, 4, 8, 16, 32, 16, 8, 4, 2] and nex == 2728,
          'a random MPS with M = 4 on 10 sites has the ranks %s, a random state %s, and an MPS with these bonds stores %d '
          'numbers against 1024' % (rk, rk2, nex))

    s16 = vn(np.full(16, 1 / 16))
    check('the bound (7.10)', abs(s16 - 4 * LN2) < 1e-12 and abs(s16 - 2.7726) < 5e-5,
          '16 equal weights give %.4f = 4 ln 2, and fewer or unequal weights give less' % s16)

    W = heis_mpo()
    L = 6
    T = W[4:5]                                                         # the left end
    for i in range(L - 1):
        T = np.einsum('xaij,abkl->xbikjl', T, W).reshape(1, 5, 2 ** (i + 2), 2 ** (i + 2))
    Hmpo = T[0, 0]
    Hk6 = sum(kron_site(s, i, L) @ kron_site(s, i + 1, L) for i in range(L - 1) for s in (SX, SY, SZ))
    opr = np.linalg.matrix_rank(Hk6.reshape(8, 8, 8, 8).transpose(0, 2, 1, 3).reshape(64, 64), tol=1e-10)
    L = 10
    A = random_mps(L, 4, np.random.default_rng(3))
    B = []
    for i in range(L):
        Wi = W[4:5] if i == 0 else (W[:, 0:1] if i == L - 1 else W)
        Bi = np.einsum('abst,xty->axsby', Wi, A[i])
        B.append(Bi.reshape(Bi.shape[0] * Bi.shape[1], 2, Bi.shape[3] * Bi.shape[4]))
    Hk10 = sum(kron_site(s, i, L) @ kron_site(s, i + 1, L) for i in range(L - 1) for s in (SX, SY, SZ))
    psi = mps_full(A)
    errH = np.abs(mps_full(B) - Hk10 @ psi).max() / np.abs(Hk10 @ psi).max()
    bonds = [B[i].shape[2] for i in range(L - 1)]
    check('the MPO of the Heisenberg chain', np.allclose(Hmpo, Hk6) and opr == 5 and errH < 1e-12 and bonds[1:-1] == [20] * 7,
          'the MPO with bond dimension 5 gives the dense matrix of 6 sites, whose operator Schmidt rank at the center is %d, '
          'and on a random MPS with M = 4 of 10 sites it gives H|psi> to %.0e with the bonds %s, M D before any truncation'
          % (opr, errH, bonds))

    entries = [np.zeros((4, 4, 4)).size, np.zeros((2, 2, 2)).size, np.zeros((4, 4, 4, 4)).size]
    check('the entries of a tensor', entries == [64, 8, 256], 'three legs of 4 give %d, three legs of 2 give %d, four legs '
          'of 4 give %d' % tuple(entries))

    s1z = np.diag([1.0, 0, -1])
    s1p = np.sqrt(2) * np.diag([1.0, 1], 1)
    s1x, s1y = (s1p + s1p.T) / 2, (s1p - s1p.T) / 2j
    SS = sum(np.kron(a, a) for a in (s1x, s1y, s1z))
    bond = (SS + SS @ SS / 3).real
    L = 8
    Ha = sps.csr_matrix((3 ** L, 3 ** L))
    for i in range(L - 1):
        Ha = Ha + sps.kron(sps.kron(sps.identity(3 ** i), sps.csr_matrix(bond)), sps.identity(3 ** (L - i - 2)), format='csr')
    wa = np.sort(spl.eigsh(Ha, k=6, which='SA', tol=1e-12, v0=np.random.default_rng(0).normal(size=3 ** L))[0])
    sp_ = np.array([[0, 1], [0, 0.]])
    Am = [np.sqrt(2 / 3) * sp_, -np.sqrt(1 / 3) * np.diag([1.0, -1]), -np.sqrt(2 / 3) * sp_.T]   # m = +1, 0, -1
    res = []
    for vl, vr in itertools.product(np.eye(2), np.eye(2)):
        T = [np.einsum('a,sab->sb', vl, np.array(Am))[None, :, :]] + [np.array(Am).transpose(1, 0, 2)] * (L - 2) \
            + [np.einsum('sab,b->as', np.array(Am), vr)[:, :, None]]
        p = mps_full(T)
        p = p / np.linalg.norm(p)
        res.append(np.linalg.norm(Ha @ p + 2 / 3 * (L - 1) * p))
    check('the AKLT chain', np.allclose(wa[:4], -2 / 3 * (L - 1), atol=1e-9) and wa[4] > wa[0] + 0.1 and max(res) < 1e-10,
          'S.S + (S.S)^2/3 on 8 spins 1 has %.6f four times and then %.4f, and the four MPS with M = 2 of the matrices '
          'sqrt(2/3) sigma+, -sqrt(1/3) sigma^z, -sqrt(2/3) sigma- are eigenstates at -(2/3)(L-1) to %.0e'
          % (wa[0], wa[4], max(res)))

    flops = {}
    d, D = 2, 5
    for M in (100, 200, 256):
        ops = [np.empty((M, D, M)), np.empty((D, D, d, d)), np.empty((M, D, M)), np.empty((M, d, M))]
        info = np.einsum_path('aib,ijst,cjd,btd->asc', *ops, optimize=('optimal', 1e12))[1]
        flops[M] = float(re.search(r'Optimized FLOP count:\s*([0-9.eE+-]+)', info).group(1))
    formula = {M: 4 * d * D * M ** 3 + 2 * d * d * D * D * M ** 2 for M in flops}
    from dmrgpy import spinchain
    method = spinchain.Spin_Chain(["S=1/2"] * 4).dmrg_method
    check('the cost of DMRG', all(abs(flops[M] / formula[M] - 1) < 0.01 for M in flops) and method == 'TWO_SITE'
          and r'O(N\chi^3)' in nb7[5],
          'the local problem has d M^2 numbers in the bulk, d M at an end and d^2 M^2 for two sites, one product of the '
          'effective Hamiltonian costs %.2e, %.2e and %.2e operations at M = 100, 200, 256 by np.einsum_path, which is '
          '4dDM^3 + 2d^2D^2M^2 with d = 2 and D = 5, a factor %.2f from 100 to 200, dmrgpy uses %s, and the notebook '
          'writes O(N chi^3)'
          % (flops[100], flops[200], flops[256], flops[200] / flops[100], method))

    # ---------------------------------------------------------------- the entanglement entropy of the solvable states
    L = 12
    singlet = np.array([0, 1, -1, 0]) / np.sqrt(2)
    pd = np.ones(1)
    for _ in range(L // 2):
        pd = np.kron(pd, singlet)
    t = pd.reshape((2,) * L)                                            # kron order, axis a is site a

    def kent(sites):
        rest = [a for a in range(L) if a not in sites]
        return vn(np.linalg.svd(np.transpose(t, list(sites) + rest).reshape(2 ** len(sites), -1), compute_uv=False) ** 2) / LN2
    from1 = [float(round(kent(list(range(1, l + 1))), 9)) for l in range(1, 11)]
    from0 = [float(round(kent(list(range(l))), 9)) for l in range(1, 11)]
    quiz = [float(round(kent(list(range(a, b + 1))), 9)) for a, b in ((1, 3), (1, 4), (2, 5), (3, 6))]
    sc, h = spin_chain(8, dimerized(8, 1.0, 0.0))
    Sd = bond_entropies(quiet(sc.get_gs, mode="DMRG"), 8) / LN2
    check('the dimer product state (7.8)', from1 == [1, 2] * 5 and from0 == [1, 0] * 5 and quiz == [1, 2, 0, 2]
          and np.allclose(Sd, [1, 0, 1, 0, 1, 0, 1], atol=1e-6),
          'S/ln 2 of the sites 1 to l is %s, of the sites 0 to l-1 is %s, the sites 1-3, 1-4, 2-5, 3-6 give %s, and dmrgpy '
          'with J2 = 0 on 8 sites gives %s' % (from1, from0, quiz, Sd.round(3)))

    Hp, st = heis(4, [(i, (i + 1) % 4, 1.0) for i in range(4)])
    ep, vp = np.linalg.eigh(Hp.toarray())
    pp = full(vp[:, 0], st, 4)
    rho = np.transpose(pp.reshape(2, 2, 2, 2), (3, 2, 1, 0)).reshape(4, 4)   # sites (0,1) against (2,3)
    wside = np.sort(np.linalg.svd(rho, compute_uv=False) ** 2)[::-1]
    plaq = {s: ent(pp, 4, list(s)) for s in ((0,), (0, 1), (0, 2), (0, 1, 2))}
    check('the plaquette of four spins', abs(ep[0] + 2) < 1e-12 and ep[1] > ep[0] + 0.5 and abs(plaq[(0,)] - LN2) < 1e-12
          and np.allclose(wside, [0.75, 1 / 12, 1 / 12, 1 / 12]) and abs(plaq[(0, 1)] - 0.8370) < 5e-5
          and abs(plaq[(0, 2)] - np.log(3)) < 1e-12 and abs(plaq[(0, 1, 2)] - LN2) < 1e-12,
          'the ring of 4 sites has the singlet at %.4f, one site %.4f = ln 2, two sites on a side %.4f = %.4f ln 2 from the '
          'weights %s, two opposite sites %.4f = ln 3, three sites ln 2' % (ep[0], plaq[(0,)], plaq[(0, 1)],
                                                                           plaq[(0, 1)] / LN2, wside.round(4), plaq[(0, 2)]))
    R['side'] = plaq[(0, 1)] / LN2

    def crossing(block, dim):
        """Nearest-neighbor bonds of the hypercubic lattice with one end in the block [0, l)^dim, counted."""
        l = block
        pts = np.array(list(itertools.product(range(l), repeat=dim)))
        out = 0
        for ax in range(dim):
            for s in (1, -1):
                q = pts.copy(); q[:, ax] += s
                out += np.sum((q[:, ax] < 0) | (q[:, ax] >= l))
        return int(out)
    cnt = [crossing(2, 2), crossing(4, 2), crossing(2, 3), crossing(4, 3)]
    big = crossing(100, 3)

    def tetramers(r0, side, n=8):
        """The tetramers on the 2 x 2 blocks of an n x n lattice, as in s07f02, and the square of sites [r0, r0+side)^2:
        the entropy in units of ln 2 and the number of cut bonds inside the tetramers."""
        ring = [(0, 0), (0, 1), (1, 1), (1, 0)]                          # the plaquette order of the ring above
        S, cutb = 0.0, 0
        for a, b in itertools.product(range(0, n, 2), repeat=2):
            inside = [k for k, (x, y) in enumerate(ring) if r0 <= a + x < r0 + side and r0 <= b + y < r0 + side]
            if 0 < len(inside) < 4:
                S += ent(pp, 4, inside) / LN2
            cutb += sum((k in inside) != ((k + 1) % 4 in inside) for k in range(4))
        return S, cutb
    off2, off4, al2, al4 = tetramers(1, 2), tetramers(1, 4), tetramers(2, 2), tetramers(2, 4)
    check('the bonds that a boundary cuts', cnt == [8, 16, 24, 96] and big == 60000 and abs(off2[0] - 4) < 1e-9 and off2[1] == 8 and off4[1] == 16
          and abs(off4[0] - 8.830) < 5e-4 and al2[0] < 1e-9 and al4[0] < 1e-9 and al2[1] == al4[1] == 0,
          'squares of side 2 and 4 cut %d and %d bonds, cubes %d and %d, 6 l^2 = %d for l = 100; with the tetramers of '
          's07f02, squares offset by one site give %.3f and %.3f ln 2 with %d and %d cut bonds, a factor %.2f, and squares '
          'aligned with the tetramers give 0' % (*cnt, big, off2[0], off4[0], off2[1], off4[1], off4[0] / off2[0]))
    R['tetramer'] = (off2[0], off4[0])

    L = 14
    page = lambda m, n: (sum(1 / k for k in range(n + 1, m * n + 1)) - (m - 1) / (2 * n)) / LN2
    half, site0 = [], []
    for seed in range(10):
        r = np.random.default_rng(100 + seed)
        p = r.normal(size=2 ** L) + 1j * r.normal(size=2 ** L)
        p /= np.linalg.norm(p)
        half.append(vn(np.linalg.svd(p.reshape(2 ** 7, -1), compute_uv=False) ** 2) / LN2)
        site0.append(vn(np.linalg.svd(p.reshape(-1, 2), compute_uv=False) ** 2) / LN2)
    p7, p5 = page(2 ** 7, 2 ** 7), page(2 ** 5, 2 ** 9)
    check('a random state of 14 spins', abs(p7 - 6.279) < 5e-4 and abs(5 - p5 - 0.045) < 5e-4 and min(half) > 6.27
          and max(half) < 6.29 and min(site0) > 0.9995,
          'the Page value of the half is %.3f bits, 0.72 below 7, ten random states give %.3f to %.3f, five sites have a '
          'deficit of %.3f bits, and one site has at least %.4f bits' % (p7, min(half), max(half), 5 - p5, min(site0)))

    # ---------------------------------------------------------------- the dimerized Heisenberg chain
    c8 = cell(notebook(8), '## Magnetization of a dimerized Heisenberg')
    nb8 = 'J = 1.0 + .2*(-1)**i' in c8 and 'h = h + J*sc.Sx[i]*sc.Sx[i+1]' in c8
    rvg = 'J1, J2 = 1.0, 0.5' in source('random_vs_gapped.py') and 'J1 if i % 2 == 0 else J2' in source('random_vs_gapped.py')
    ssp = 'weights(0.5)' in source('schmidt_spectrum.py')
    wid = 'J = 1.0 if i % 2 == 0 else J2' in source('dimerentropy.py', os.path.join(WEBNOTES, 'widgets', 'defs'))
    e0, _ = ground(12, dimerized(12, 1.0, 0.0))
    J8 = [1.0 + 0.2 * (-1) ** i for i in range(11)]
    check('the labels of the dimerized chain', nb8 and rvg and ssp and wid and abs(e0 + 4.5) < 1e-10
          and np.allclose(J8, dimerized(12, 1.2, 0.8)),
          'the notebook of Session 8 has J = 1 + 0.2(-1)^i on the bond (i, i+1), which is J1 = 1.2 and J2 = 0.8, the widget, '
          'random_vs_gapped.py and schmidt_spectrum.py put J1 on the even i, and at J2 = 0 the chain of 12 sites has %.4f'
          % e0)

    e12, p12 = ground(12, J8)
    S12 = cuts(p12, 12)
    sc, h = spin_chain(12, J8)
    S12d = bond_entropies(quiet(sc.get_gs, mode="DMRG"), 12)
    strong, weak = S12[0::2], S12[1::2]
    check('the chain of the Session 8 notebook on 12 sites', np.abs(S12 - S12d).max() < 1e-6 and strong.min() > 0.692
          and strong.max() < 0.700 and weak.min() > 0.169 and weak.max() < 0.187,
          'J1 = 1.2 and J2 = 0.8, the cuts after an odd number of sites give %.3f to %.3f, after an even number %.3f to '
          '%.3f, and dmrgpy agrees to %.0e' % (strong.min(), strong.max(), weak.min(), weak.max(), np.abs(S12 - S12d).max()))

    pert = []
    for J2 in (0.1, 0.5):
        for L in (12, 16):
            Jb = dimerized(L, 1.0, J2)
            H0, _ = heis(L, chain_bonds(Jb), L // 2)
            H1, _ = heis(L, chain_bonds(Jb), L // 2 + 1)
            E0, Et = lowest(H0)[0][0], lowest(H1)[0][0]
            Ept = -0.75 * L / 2 - 3 / 32 * J2 ** 2 * (L / 2 - 1)
            pert.append((J2, L, E0, Ept, Et - E0))
    a, b_, c_, d_ = pert
    rings = []                                       # the same chain closed into a ring by one more J2 bond
    for L in (12, 16):
        bonds = chain_bonds(dimerized(L, 1.0, 0.1)) + [(L - 1, 0, 0.1)]
        rings.append(lowest(heis(L, bonds, L // 2 + 1)[0])[0][0] - lowest(heis(L, bonds, L // 2)[0])[0][0])
    series = 1 - 0.1 / 2 - 3 * 0.1 ** 2 / 8 + 0.1 ** 3 / 32
    check('the dimerized chain in perturbation', abs(a[2] - a[3]) < 2.5e-4 and abs(b_[2] - b_[3]) < 2.5e-4
          and abs(a[4] - 0.9517) < 5e-5 and abs(b_[4] - 0.9496) < 5e-5 and abs(c_[3] - c_[2] - 0.017) < 5e-4
          and abs(d_[3] - d_[2] - 0.024) < 5e-4 and abs(c_[4] - 0.70) < 5e-3 and abs(d_[4] - 0.68) < 5e-3
          and np.allclose(rings, 0.9463, atol=5e-5) and abs(rings[1] - series) < 1e-5,
          'J1 = 1, J2 = 0.1: the energy of 12 and 16 sites is %.5f and %.5f against %.5f and %.5f, the gap %.4f and %.4f '
          'against J1 - J2/2 = 0.95, and %.5f and %.5f on rings of 12 and 16 sites, against the series %.5f; J2 = 0.5: the '
          'energy is %.3f and %.3f below the formula, the gap %.3f and %.3f against 0.75'
          % (a[2], b_[2], a[3], b_[3], a[4], b_[4], rings[0], rings[1], series, c_[3] - c_[2], d_[3] - d_[2], c_[4], d_[4]))

    e14, p14 = ground(14, dimerized(14, 1.0, 0.5))
    S14 = cuts(p14, 14) / LN2
    sc, h = spin_chain(14, dimerized(14, 1.0, 0.5))
    S14d = bond_entropies(quiet(sc.get_gs, mode="DMRG"), 14) / LN2
    check('J1 = 1 and J2 = 0.5 on 14 sites', np.abs(S14 - S14d).max() < 1e-6 and 0.9999 < S14[0::2].min() and S14[0::2].max() < 1.0025
          and 0.1385 < S14[1::2].min() and S14[1::2].max() < 0.1455,
          'S/ln 2 is %.4f to %.4f at the cuts through a J1 bond and %.3f to %.3f through a J2 bond, by ED and by dmrgpy '
          'to %.0e, which the caption of random_vs_gapped rounds to about 0.15'
          % (S14[0::2].min(), S14[0::2].max(), S14[1::2].min(), S14[1::2].max(), np.abs(S14 - S14d).max()))
    R['weak'] = (S14[1::2].min(), S14[1::2].max())

    tails = []
    for J2 in (1.0, 0.5):
        _, p16 = ground(16, dimerized(16, 1.0, J2))
        w = np.sort(np.linalg.svd(p16.reshape(256, 256), compute_uv=False) ** 2)[::-1]
        tails.append((np.sum(w[16:]), vn(w)))
    check('the Schmidt weights of 16 sites', abs(tails[0][0] / 1.95e-7 - 1) < 0.01 and abs(tails[1][0] / 2.75e-11 - 1) < 0.01
          and abs(tails[0][1] - 0.5923) < 5e-5 and abs(tails[1][1] - 0.1005) < 5e-5,
          'beyond the 16 largest weights at the center, a J2 bond, there is %.3e for J2 = 1 and %.3e for J2 = 0.5, and '
          'the entropy is %.4f and %.4f' % (tails[0][0], tails[1][0], tails[0][1], tails[1][1]))

    four = []
    for Jp in (0.1, 1.0):
        H0, _ = heis(4, chain_bonds([1.0, Jp, 1.0]), 2)
        H1, _ = heis(4, chain_bonds([1.0, Jp, 1.0]), 3)
        four.append((lowest(H0)[0][0], lowest(H1)[0][0]))
    sc, h = spin_chain(4, [1.0, 0.1, 1.0])
    e4d = quiet(sc.gs_energy, mode="DMRG")
    check('four sites with the bonds J, J\', J', abs(four[0][0] + 1.50096) < 5e-6 and abs(four[0][1] + 0.52749) < 5e-6
          and abs(four[1][1] - four[1][0] - 0.6589) < 5e-5 and abs(e4d - four[0][0]) < 1e-6,
          'J\' = 0.1 J gives %.5f J and the triplet at %.5f J, a gap of %.4f J, J\' = J gives %.5f J and a gap of %.4f J, '
          'dmrgpy %.5f J' % (four[0][0], four[0][1], four[0][1] - four[0][0], four[1][0], four[1][1] - four[1][0], e4d))

    ends = []
    for L in (10, 14):
        Jb = [0.5 if i % 2 == 0 else 1.0 for i in range(L - 1)]
        lv = [lowest(heis(L, chain_bonds(Jb), L // 2 + m)[0], k)[0] for m, k in ((0, 3), (1, 2), (2, 1))]
        allv = np.sort(np.concatenate(lv))
        ends.append((L, lv[1][0] - lv[0][0], np.min([lv[0][2], lv[1][1], lv[2][0]]) - lv[0][0], abs(lv[0][1] - lv[1][0])))
    check('weak bonds at the ends', abs(ends[0][1] - 7.8e-3) < 1e-4 and abs(ends[1][1] - 7.9e-4) < 1e-5 and ends[0][3] < 1e-9
          and all(0.60 < x[2] < 0.64 for x in ends),
          'J1 = 1 and J2 = 0.5 with J2 on the end bonds: the triplet is %.1e above the singlet for 10 sites and %.1e for 14, '
          'and the next level is %.3f and %.3f above' % (ends[0][1], ends[1][1], ends[0][2], ends[1][2]))

    # ---------------------------------------------------------------- critical chains and the central charge
    C = infinite_corr(1000)
    Sinf = {l: ff(C, list(range(l))) for l in (10, 20, 50, 100, 200, 500, 1000)}
    fit = np.polyfit(np.log(list(Sinf)), list(Sinf.values()), 1)
    const = Sinf[1000] - np.log(1000) / 3
    hq = geometry.chain().get_hamiltonian(has_spin=False)
    q10, q100 = (hq.get_entanglement_entropy(region=list(range(l)), nsuper=2002) for l in (10, 100))
    r10, r100 = (ff(ring_corr(l, 2002), list(range(l))) for l in (10, 100))
    chord = np.log(2002 / np.pi * np.sin(np.pi * 100 / 2002)) / 3 + const
    term = (np.log(10) / 3, np.log(1000) / 3)
    check('(7.12) with two ends', abs(Sinf[10] - 1.4934) < 5e-5 and abs(Sinf[100] - 2.2611) < 5e-5 and abs(Sinf[1000] - 3.0287) < 5e-5
          and abs(fit[0] - 1 / 3) < 2e-3 and abs(const - 0.7261) < 5e-5 and abs(const - np.log(2) / 3 - 0.4950) < 5e-5
          and abs(q10 - r10) < 1e-8 and abs(q100 - r100) < 1e-8 and abs(q10 - 1.4934) < 5e-5 and abs(q100 - 2.2598) < 5e-5
          and abs(chord - q100) < 3e-4 and abs(term[0] - 0.768) < 5e-4 and abs(term[1] - 2.303) < 5e-4
          and abs(Sinf[1000] - Sinf[10] - np.log(100) / 3) < 2e-3 and round(np.log2(1024)) == 10,
          'free fermions with the hopping 1 at half filling: S = %.4f, %.4f, %.4f at l = 10, 100, 1000, the slope %.4f, '
          'S(1000) - ln(1000)/3 = %.4f = ln(2)/3 + %.4f, pyqula on a ring of 2002 sites %.4f and %.4f as the numpy ring, '
          'which is the infinite chain at (N/pi) sin(pi l/N) to %.0e, the term ln(l)/3 alone %.3f and %.3f, the growth '
          '%.3f, and 1024 sites have 10 layers' % (Sinf[10], Sinf[100], Sinf[1000], fit[0], const, const - np.log(2) / 3,
                                                   q10, q100, abs(chord - q100), *term, Sinf[1000] - Sinf[10]))
    R['crit'] = (Sinf[10], Sinf[1000], term)

    def half_open(L):
        return ff(corr(hop_chain([1.0] * (L - 1))), list(range(L // 2)))
    Ls = [100, 200, 400, 800]
    Sh = [half_open(L) for L in Ls]
    slope = np.polyfit(np.log(Ls), Sh, 1)[0]
    odd = (half_open(402) - half_open(202)) / np.log(402 / 202)
    ev = (Sh[2] - Sh[1]) / np.log(2)
    q400 = geometry.chain().get_hamiltonian(has_spin=False).set_finite_system(n=400).get_entanglement_entropy()
    nbtext = r'\frac{c}{6}\ln L' in nb7[17]
    check('half of an open chain', np.allclose(Sh, [1.0492, 1.1677, 1.2848, 1.4011], atol=5e-5) and abs(slope - 0.169) < 5e-4
          and abs(q400 - Sh[2]) < 1e-8 and abs(q400 - 1.284805) < 5e-7 and abs(odd - 0.163) < 1e-3 and abs(ev - 0.169) < 1e-3
          and nbtext,
          'free fermions, the left half of L = 100, 200, 400, 800 has %s, a slope %.4f, between 200 and 400 the slope is '
          '%.3f and between 202 and 402, with an odd number of sites in the half, %.3f, pyqula gives %.6f for L = 400, and '
          'the notebook writes (c/6) ln L' % (np.round(Sh, 4).tolist(), slope, ev, odd, q400))

    t = [1.0 if i % 2 == 0 else 0.6 for i in range(1000)]
    Cd = corr(hop_chain(t, ring=True))
    blocks = {'weak': ff(Cd, list(range(40))), 'weak10': ff(Cd, list(range(10))), 'mixed': ff(Cd, list(range(41))),
              'strong': ff(Cd, list(range(1, 41)))}
    gap = 2 * np.min(np.abs(1 + 0.6 * np.exp(1j * np.linspace(-np.pi, np.pi, 2001))))
    hb = geometry.bichain().get_hamiltonian(has_spin=False)
    hb.inter = 0.6 * hb.inter
    qw = hb.get_entanglement_entropy(region=list(range(40)), nsuper=100)
    qs = hb.get_entanglement_entropy(region=list(range(1, 41)), nsuper=100)
    red = 't1, t2 = 1.0, 0.6' in source('critical_entropy.py') and '-(t1 if i % 2 == 0 else t2)' in source('critical_entropy.py')
    check('the dimerized chain of free fermions', abs(gap - 0.8) < 1e-9 and abs(blocks['weak'] - 0.4992) < 5e-5
          and abs(blocks['weak10'] - 0.4983) < 5e-5 and abs(blocks['mixed'] - 0.9554) < 5e-5 and abs(blocks['strong'] - 1.4117) < 5e-5
          and abs(qw - blocks['weak']) < 1e-6 and abs(qs - blocks['strong']) < 1e-6 and red,
          'hoppings 1 and 0.6, the gap %.3f, on a ring of 1000 sites a block whose two ends cut a 0.6 bond has %.4f, and %.4f '
          'with 10 sites, one end of each kind %.4f, two ends on a bond 1 %.4f, pyqula bichain %.4f and %.4f, and '
          'critical_entropy.py takes the hopping 1 on the bonds (2n, 2n+1)' % (gap, blocks['weak'], blocks['weak10'],
                                                                               blocks['mixed'], blocks['strong'], qw, qs))

    # ---------------------------------------------------------------- pyqula
    gc = geometry.chain()
    hc = gc.get_hamiltonian(has_spin=False)
    h7 = hc.set_finite_system(n=7)
    lev7 = np.sort(np.linalg.eigvalsh(dense(h7.intra)))
    x7 = np.array(h7.geometry.r)[:, 0]
    gb = geometry.bichain()
    hb = gb.get_hamiltonian(has_spin=False)
    xb = np.array(gb.r)[:, 0]
    ok = np.allclose(lev7, np.sort(2 * np.cos(np.pi * np.arange(1, 8) / 8))) and np.all(np.diff(x7) > 0)
    ok = ok and np.allclose(xb, [-0.5, 0.5]) and np.allclose(gb.a1, [2, 0, 0]) and abs(hc.intra[0, 0]) < 1e-12
    ok = ok and abs(dense(hb.intra)[0, 1] - 1) < 1e-12 and abs(dense(hb.inter)[1, 0] - 1) < 1e-12
    check('chain() and bichain()', ok,
          'chain() has one site and the hopping +1, set_finite_system(n=7) is ordered along x with the levels 2 cos(pi k/8), '
          'bichain() has the sites at x = %s, the period 2, h.intra joins the two sites of a cell and h.inter the second '
          'site to the first of the next cell' % xb.tolist())

    ring10 = hq.get_entanglement_entropy(region=list(range(10)), nsuper=102)
    ring40 = hq.get_entanglement_entropy(region=list(range(40, 50)), nsuper=102)
    two_s = geometry.chain().get_hamiltonian(has_spin=False).set_finite_system(n=2).get_entanglement_entropy()
    mine = ff(ring_corr(10, 102), list(range(10)))
    check('get_entanglement_entropy', abs(ring10 - mine) < 1e-8 and abs(ring40 - mine) < 1e-8 and abs(ring10 - 1.48818495) < 1e-8
          and abs(two_s - LN2) < 1e-9,
          'a block of 10 sites of a ring of 102 cells gives %.8f, the numpy ring %.8f, the sites 40 to 49 the same, two '
          'sites with no region give %.6f, and the left half of 400 sites is in the line on the open chain'
          % (ring10, mine, two_s))

    msgs = []
    for make in (lambda: hq.get_entanglement_entropy(region=list(range(10)), nsuper=1000),
                 lambda: geometry.chain().get_hamiltonian(has_spin=False).set_finite_system(n=11).get_entanglement_entropy()):
        try:
            make()
            msgs.append('')
        except ValueError as err:
            msgs.append(str(err))
    check('a level at the Fermi energy', all('A level sits at the Fermi energy' in m for m in msgs),
          'a ring of 1000 sites and an open chain of 11 sites raise ValueError: "%s..."' % msgs[0][:40])

    sp100 = []
    for ncell in (100, 300):
        g = geometry.bichain()
        hs = g.get_hamiltonian(); hs.inter = 0.6 * hs.inter
        h0 = g.get_hamiltonian(has_spin=False); h0.inter = 0.6 * h0.inter
        sp100.append((hs.get_entanglement_entropy(region=list(range(10)), nsuper=ncell),
                      h0.get_entanglement_entropy(region=list(range(10)), nsuper=ncell)))
    gch = geometry.chain()
    c602 = (gch.get_hamiltonian().get_entanglement_entropy(region=list(range(10)), nsuper=602),
            gch.get_hamiltonian(has_spin=False).get_entanglement_entropy(region=list(range(10)), nsuper=602))
    wrong300 = abs(sp100[1][0] - 2 * sp100[1][1]) > 1e-6
    check('the spinful entropy of pyqula', abs(sp100[0][0] - 2 * sp100[0][1]) < 1e-8 and abs(sp100[0][1] - 0.49835) < 5e-6
          and abs(sp100[1][1] - sp100[0][1]) < 1e-8 and abs(c602[0] - 2 * c602[1]) < 1e-8,
          'the dimerized bichain, 10 sites of a ring of 100 cells: %.5f with the default spins and %.5f with '
          'has_spin=False; on 300 cells has_spin=False gives %.5f again and the default %.3f, %s in this run; chain() '
          'on 602 cells gives %.5f, twice %.5f' % (sp100[0][0], sp100[0][1], sp100[1][1], sp100[1][0],
                                                   'wrong' if wrong300 else 'right', c602[0], c602[1]))

    hf = geometry.chain().get_hamiltonian(has_spin=False).set_finite_system(n=8)
    hf.intra = 0.5 * hf.intra
    hf2 = geometry.chain().get_hamiltonian(has_spin=False).set_finite_system(n=8)
    hf2.intra = 0.5 * hf2.intra
    pot = np.zeros((8, 8)); pot[0, 0] = 5e-6
    hf2.intra = dense(hf2.intra) + pot
    e_a = quiet(quiet(pyqula2dmrgpy.generate_fermionic_chain, hf).gs_energy, mode="ED")
    e_b = quiet(quiet(pyqula2dmrgpy.generate_fermionic_chain, hf2).gs_energy, mode="ED")
    w_a = np.linalg.eigvalsh(dense(hf.intra)); w_b = np.linalg.eigvalsh(dense(hf2.intra))
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        try:
            pyqula2dmrgpy.generate_fermionic_chain(geometry.chain().get_hamiltonian(has_spin=False))
        except Exception:
            pass
    check('pyqula2dmrgpy', abs(e_a - e_b) < 1e-12 and abs(np.sum(w_b[w_b < 0]) - np.sum(w_a[w_a < 0]) - 2.5e-6) < 2e-7
          and 'Only implemented for 0d dimensional Hamiltonians' in out.getvalue(),
          'an onsite energy 5e-6 on one site changes the free energy by %.1e and the dmrgpy energy by %.0e, and a chain '
          'with a period prints "Only implemented for 0d dimensional Hamiltonians"'
          % (np.sum(w_b[w_b < 0]) - np.sum(w_a[w_a < 0]), abs(e_a - e_b)))

    # ---------------------------------------------------------------- the transverse-field Ising chain
    c24 = cell(nb7, '## The entanglement entropy as a signal')
    nbising = 'J = -1' in c24 and 'h = h + J*sc.Sz[i]*sc.Sz[i+1]' in c24 and 'h = h + Bx*sc.Sx[i]' in c24
    L = 10
    Hi = sum(-kron_site(SZ, i, L) @ kron_site(SZ, i + 1, L) for i in range(L - 1)) + 0.37 * sum(kron_site(SX, i, L) for i in range(L))
    wi, vi = np.linalg.eigh(Hi)
    eb, Gb = tfim(L, 0.37)
    sb = [tfim_entropy(Gb, L, l) for l in range(1, L)]
    se = [vn(np.linalg.svd(vi[:, 0].reshape(2 ** l, -1), compute_uv=False) ** 2) for l in range(1, L)]
    gaps = []
    for Bx in (0.8, 1.0):
        Lr = 12
        Hr = sum(-kron_site(SZ, i, Lr) @ kron_site(SZ, (i + 1) % Lr, Lr) for i in range(Lr)) + Bx * sum(kron_site(SX, i, Lr) for i in range(Lr))
        w = spl.eigsh(sps.csr_matrix(Hr), k=2, which='SA', tol=1e-12, v0=np.random.default_rng(0).normal(size=2 ** Lr))[0]
        gaps.append(np.diff(np.sort(w))[0])
    quench = 'g = 1.0' in source('quench_entropy.py') and '- g * sum(op(sx, i)' in source('quench_entropy.py')
    L8 = 8                                            # the ring of 8 sites of the sheet of Session 10, at Bx = 0.5
    H8 = sum(-kron_site(SZ, i, L8) @ kron_site(SZ, (i + 1) % L8, L8) for i in range(L8)) + 0.5 * sum(kron_site(SX, i, L8) for i in range(L8))
    H10 = sum(-4 * kron_site(SZ, i, L8) @ kron_site(SZ, (i + 1) % L8, L8) for i in range(L8)) + 2 * sum(kron_site(SX, i, L8) for i in range(L8))
    e8 = np.linalg.eigvalsh(H8)[0]
    same10 = np.abs(H8 - H10 / 4).max()              # -J sigma sigma - h sigma^x with J = 1 and h = -2 Bx = -1
    check('the Ising chain of the notebook', nbising and abs(eb - wi[0]) < 1e-10 and np.abs(np.array(sb) - se).max() < 1e-9
          and abs(gaps[0] - 0.3004) < 5e-5 and abs(gaps[1] - 0.5000) < 5e-5
          and abs(e8 + 2.562915) < 1e-6 and abs(4 * e8 + 2 / np.sin(np.pi / 16)) < 1e-10 and same10 < 1e-12,
          'the cell is -sum S^z S^z + Bx sum S^x, the Bogoliubov-de Gennes ground state of 10 sites at Bx = 0.37 has the '
          'energy and the entropies of ED to %.0e, a ring of 12 sites has the gap %.4f at Bx = 0.8 and %.4f at Bx = 1, and a '
          'ring of 8 sites at Bx = 0.5 has %.6f, one quarter of %.6f, the form -sum sigma^z sigma^z - h sum sigma^x of '
          'Session 10 with h = -2 Bx' % (max(abs(eb - wi[0]), np.abs(np.array(sb) - se).max()), *gaps, e8, 4 * e8))

    S160 = tfim_entropy(tfim(160, 0.5)[1], 160, 80)
    S320 = tfim_entropy(tfim(320, 0.5)[1], 320, 160)
    exact = {L: tfim_entropy(tfim(L, 0.5)[1], L, L // 2 + 1) for L in (20, 40)}
    dm = {}
    for L in (20, 40):
        from dmrgpy import spinchain as _s
        sc = _s.Spin_Chain(["S=1/2"] * L)
        hI = 0
        for i in range(L - 1):
            hI = hI - sc.Sz[i] * sc.Sz[i + 1]
        for i in range(L):
            hI = hI + 0.5 * sc.Sx[i]
        sc.set_hamiltonian(-sum(sc.Sz)); guess = quiet(sc.get_gs, mode="DMRG")
        sc.set_hamiltonian(hI)
        dm[L] = quiet(sc.get_gs, mode="DMRG", wf0=guess).get_bond_entropy(L // 2, L // 2 + 1)
    check('the critical Ising chain', abs(S320 - S160 - 0.0582) < 2e-4 and abs(np.log(2) / 12 - 0.0578) < 1e-4
          and abs(exact[20] - 0.4427) < 5e-5 and abs(exact[40] - 0.5050) < 5e-5 and abs(dm[20] - exact[20]) < 2e-3
          and abs(dm[40] - exact[40]) < 2e-3,
          'at Bx = 0.5 the half of an open chain grows by %.4f from 160 to 320 sites, (1/12) ln 2 = %.4f for c = 1/2, the '
          'exact entropy at the cut of the notebook is %.4f and %.4f for 20 and 40 sites, and the cell gives %.4f and %.4f'
          % (S320 - S160, np.log(2) / 12, exact[20], exact[40], dm[20], dm[40]))
    R['ising_exact'] = exact

    scan = {}
    for L in (20, 40):
        Bs = np.round(np.arange(0.30, 0.701, 0.01), 2)
        S = np.array([tfim_entropy(tfim(L, B)[1], L, L // 2 + 1) for B in Bs])
        scan[L] = (Bs[np.argmax(S)], S.max(), S[0], dict(zip(Bs, S)))
    from dmrgpy import spinchain as _s
    sc = _s.Spin_Chain(["S=1/2"] * 20)
    hI = 0
    for i in range(19):
        hI = hI - sc.Sz[i] * sc.Sz[i + 1]
    for i in range(20):
        hI = hI + 0.3 * sc.Sx[i]
    sc.set_hamiltonian(-sum(sc.Sz)); guess = quiet(sc.get_gs, mode="DMRG")
    sc.set_hamiltonian(hI)
    wf = quiet(sc.get_gs, mode="DMRG", wf0=guess)
    s03 = wf.get_bond_entropy(10, 11)
    m03 = abs(wf.dot(sum(sc.Sz) * wf).real) / 20
    broken = s03 < 0.05 and m03 > 0.4
    check('the exact curve and the scan of the notebook', scan[20][2] > 0.69 and scan[40][2] > 0.69
          and 0.36 <= scan[20][0] <= 0.38 and 0.43 <= scan[40][0] <= 0.45 and scan[20][1] > exact[20] + 0.2
          and scan[40][1] > exact[40] + 0.2 and (broken or abs(s03 - scan[20][2]) < 2e-3),
          'the exact entropy at the cut of the notebook is %.4f and %.4f at Bx = 0.30, has its largest value %.4f at %.2f '
          'for 20 sites and %.4f at %.2f for 40 sites, and falls to %.4f and %.4f at 0.5; dmrgpy from the ferromagnetic '
          'guess at Bx = 0.30 on 20 sites gives %.3f with %.2f per site, the %s state' % (
              scan[20][2], scan[40][2], scan[20][1], scan[20][0], scan[40][1], scan[40][0], exact[20], exact[40], s03, m03,
              'broken' if broken else 'symmetric'))
    R['scan'] = scan

    L = 12
    sx = sps.csr_matrix(np.array([[0, 1], [1, 0.]])); szp = sps.csr_matrix(np.diag([1.0, -1]))
    op = lambda o, i: sps.kron(sps.kron(sps.identity(2 ** i), o), sps.identity(2 ** (L - i - 1)), format='csr')
    Hq = -sum(op(szp, i) @ op(szp, i + 1) for i in range(L - 1)) - sum(op(sx, i) for i in range(L))
    p0 = np.zeros(2 ** L, complex); p0[0] = 1
    ts = np.linspace(0, 5, 2001)
    traj = expm_multiply(-1j * Hq, p0, start=0, stop=5, num=2001, endpoint=True)
    Sq = np.array([vn(np.linalg.svd(p.reshape(64, 64), compute_uv=False) ** 2) for p in traj]) / LN2
    tc = [float(np.interp(k, Sq[:np.argmax(Sq)], ts[:np.argmax(Sq)])) for k in (1, 2, 3)]
    wq, vq = np.linalg.eigh(Hq.toarray())
    pt = vq @ (np.exp(-1j * wq * ts[1600]) * (vq.T @ p0))
    at = [vn(np.linalg.svd((vq @ (np.exp(-1j * wq * x) * (vq.T @ p0))).reshape(64, 64), compute_uv=False) ** 2) / LN2 for x in tc]
    grid = ts[::20]
    first = [float(grid[np.argmax(Sq[::20] > k)]) for k in (1, 2, 3)]
    check('the quench of quench_entropy.py', np.allclose(tc, [1.463, 2.539, 3.518], atol=2e-3) and abs(ts[np.argmax(Sq)] - 4.0) < 0.01
          and abs(Sq.max() - 3.289) < 1e-3 and np.abs(pt - traj[1600]).max() < 1e-10 and quench
          and np.allclose(at, [1, 2, 3], atol=1e-3) and np.allclose(first, [1.5, 2.55, 3.55]),
          '12 sites from all spins up with -sum sigma^z sigma^z - sum sigma^x, S/ln 2 of the half passes 1, 2, 3 at t = '
          '%.3f, %.3f, %.3f, where the full diagonalization gives %.4f, %.4f, %.4f, and has its maximum %.3f at t = %.3f; '
          'on the grid of 0.05 of the figure the first points above are %s' % (*tc, *at, Sq.max(), ts[np.argmax(Sq)], first))

    # ---------------------------------------------------------------- DMRG and dmrgpy
    L = 10
    Hs = sps.csr_matrix(sum(kron_site(s, i, L) @ kron_site(s, i + 1, L) for i in range(L - 1) for s in (SX, SY, SZ)).real)
    E0 = np.linalg.eigvalsh(Hs.toarray())[0]
    runs = {M: [sweeps(Hs, L, M, seed) for seed in (seeds)] for M, seeds in ((2, (1, 2, 3)), (4, range(1, 9)), (8, (1, 2)))}
    mono = max(np.max(np.diff(r)) for rr in runs.values() for r in rr)
    end = {M: [r[-1] - E0 for r in rr] for M, rr in runs.items()}
    ndm = {}
    for M in (2, 4, 8):
        sc, h = spin_chain(L, maxm=M)
        ndm[M] = quiet(sc.gs_energy, mode="DMRG") - E0
    fig = 'def run(M, nsweeps=3, seed=1)' in source('dmrg_sweeps.py')
    check('the one-site sweep and dmrgpy', len(runs[2][0]) == 54 and mono < 1e-10 and abs(E0 + 4.258035) < 1e-6 and fig
          and np.allclose(end[2], 0.2017, atol=3e-4) and abs(end[4][0] - 6.1e-3) < 1e-4 and max(end[4]) < 1e-2
          and np.allclose(end[8], 1.461e-5, rtol=0.01) and abs(ndm[2] - 0.2157) < 1e-3 and abs(ndm[4] - 6.1e-3) < 2e-4
          and abs(ndm[8] - 1.5e-5) < 2e-6,
          'Heisenberg chain of 10 sites, E0 = %.6f, three sweeps of 18 updates, the energy never goes up (largest step '
          '%.0e), E - E0 = %.4f to %.4f for M = 2, %.2e from the start of dmrg_sweeps.py (seed 1) and %.2e to %.2e over '
          'the seeds 1 to 8 for M = 4, %.3e for M = 8, and dmrgpy with maxm = 2, 4, 8 gives %.4f, %.2e, %.2e'
          % (E0, mono, min(end[2]), max(end[2]), end[4][0], min(end[4]), max(end[4]), end[8][0], ndm[2], ndm[4], ndm[8]))
    R['sweeps'] = end

    sc6 = _s.Spin_Chain(["S=1/2"] * 6)
    sc, h = spin_chain(2)
    wf2 = quiet(sc.get_gs, mode="DMRG")
    try:
        wf2.get_bond_entropy(0, 1)
        fallback = ''
    except AttributeError as err:
        fallback = str(err)
    site_s = quiet(sc.get_site_entropy, wf2, 0)
    check('the settings of dmrgpy', sc6.maxm == 30 and sc6.nsweeps == 15 and sc6.cutoff == 1e-12 and sc6.dmrg_method == 'TWO_SITE'
          and "has no attribute 'get_bond_entropy'" in fallback and abs(site_s - LN2) < 1e-6 and 'DMRGROOT' in nb7[0],
          'maxm = %d, nsweeps = %d, cutoff %.0e and %s by default, two sites fall back to exact diagonalization and '
          'get_bond_entropy raises AttributeError, sc.get_site_entropy(wf, 0) gives %.5f, and the notebook finds dmrgpy '
          'through DMRGROOT' % (sc6.maxm, sc6.nsweeps, sc6.cutoff, sc6.dmrg_method, site_s))

    ering = {}
    for L in (16, 18):
        H, _ = heis(L, [(i, (i + 1) % L, 1.0) for i in range(L)], L // 2)
        ering[L] = lowest(H)[0][0] / L
    corr_ = {L: ering[L] + np.pi ** 2 / (12 * L ** 2) for L in ering}
    einf = 0.25 - np.log(2)
    sc, h = spin_chain(20, maxm=40)
    e20 = quiet(sc.gs_energy, mode="DMRG") / 20
    check('the energy per site', abs(einf + 0.443147) < 1e-6 and all(abs(corr_[L] - einf) < 1e-4 for L in corr_)
          and abs(e20 + 0.43412) < 1e-5 and e20 > einf and abs(e2 / 2 + 0.375) < 1e-9,
          '1/4 - ln 2 = %.6f, rings of 16 and 18 sites give %.5f and %.5f, and %.5f and %.5f with pi^2/(12 L^2), the open '
          'chain has %.3f for 2 sites and %.5f for 20' % (einf, ering[16], ering[18], corr_[16], corr_[18], e2 / 2, e20))

    # ---------------------------------------------------------------- the notebook cells
    c3 = cell(nb7, '## Energy of the Heisenberg model')
    check('the cell on the energy against the size', 'gs_energy(mode="DMRG")' in c3 and 'range(2,40,4)' in c3,
          'it calls sc.gs_energy(mode="DMRG") for N = 2, 6, ..., 38')

    flu, en = {}, {}
    for M in (3, 11, 23):
        sc, h = spin_chain(20, maxm=M)
        wf = quiet(sc.get_gs, mode="DMRG")
        e = wf.dot(h * wf).real
        flu[M] = np.sqrt(abs(wf.dot(h * (h * wf)).real - e ** 2)) / 20
        en[M] = e / 20
    check('the cell on the role of the bond dimension', flu[3] > flu[11] > flu[23] and flu[23] < 1e-5
          and abs(en[11] - en[23]) < 2e-5,
          '20 sites, the fluctuation per site is %.1e, %.1e, %.1e at maxm = 3, 11, 23 and the energy per site %.6f, '
          '%.6f, %.6f' % (flu[3], flu[11], flu[23], en[3], en[11], en[23]))
    R['flu'] = (flu, en)

    sc, h = spin_chain(20, maxm=20)
    S20 = bond_entropies(quiet(sc.get_gs, mode="DMRG"), 20)
    sc, h = spin_chain(20, maxm=2)
    S20m2 = bond_entropies(quiet(sc.get_gs, mode="DMRG"), 20)
    odd = S20[0::2]                                                    # the cuts after 1, 3, ..., 19 sites
    check('the cell on the entropy of the ground state', abs(S20[9] - 0.635) < 1e-3 and abs(S20[8] - 0.792) < 1e-3
          and abs(S20[10] - 0.792) < 1e-3 and np.argmax(S20) in (8, 10) and S20[9] < odd.min() and S20m2.max() < LN2,
          '20 sites, maxm = 20: the cut after 10 sites has %.4f, after 9 and 11 sites %.4f and %.4f, the largest, every '
          'cut after an odd number of sites has at least %.4f; maxm = 2 gives at most %.4f < ln 2'
          % (S20[9], S20[8], S20[10], odd.min(), S20m2.max()))
    R['S20'] = S20

    size = {}
    for L in (10, 20, 30, 40):
        sc, h = spin_chain(L)
        wf = quiet(sc.get_gs, mode="DMRG")
        size[L] = (wf.get_bond_entropy(L // 2, L // 2 + 1), wf.get_bond_entropy(L // 2 - 1, L // 2))
    nbv = [size[L][0] for L in size]
    cen = [size[L][1] for L in size]
    check('the cell on the size', 'range(10,50,2)' in cell(nb7, '## Size dependence') and np.allclose(nbv, [0.492, 0.792, 0.709, 0.867], atol=1e-3)
          and np.allclose(cen, [0.738, 0.635, 0.835, 0.762], atol=1e-3) and abs(cen[3] - cen[1] - 0.127) < 2e-3,
          'the cut of the cell gives %s for L = 10, 20, 30, 40, the center %s, and the centers of 20 and 40 sites differ '
          'by %.3f against (1/6) ln 2 = %.3f' % (np.round(nbv, 3).tolist(), np.round(cen, 3).tolist(), cen[3] - cen[1], np.log(2) / 6))
    R['size'] = nbv

    bd = {}
    for L in (10, 30):
        for M in (2, 8, 19):
            sc, h = spin_chain(L, maxm=M)
            bd[(L, M)] = quiet(sc.get_gs, mode="DMRG").get_bond_entropy(L // 2, L // 2 + 1)
    check('the cell on the bond dimension', np.allclose([bd[(10, M)] for M in (2, 8, 19)], [0.271, 0.492, 0.492], atol=1e-3)
          and np.allclose([bd[(30, M)] for M in (2, 8, 19)], [0.360, 0.686, 0.708], atol=1e-3),
          'chi = 2, 8, 19 give %.3f, %.3f, %.3f for 10 sites and %.3f, %.3f, %.3f for 30, against ln chi = 0.693, 2.079, 2.944'
          % tuple(bd[(L, M)] for L in (10, 30) for M in (2, 8, 19)))
    R['bd'] = bd

    sc = _s.Spin_Chain(["S=1/2"] * 20)
    hz = 0
    for i in range(19):
        hz = hz + sc.Sz[i] * sc.Sz[i + 1]
    sc.set_hamiltonian(hz)
    wf = quiet(sc.get_gs, mode="DMRG")
    ez = wf.dot(hz * wf).real
    sz_ = bond_entropies(wf, 20)
    s = np.arange(2 ** 20, dtype=np.int64)
    al = np.ones(len(s), bool)
    for i in range(19):
        al &= ((s >> i) & 1) != ((s >> (i + 1)) & 1)
    check('the Ising chain of the quiz of the notebook', abs(ez + 4.75) < 1e-8 and sz_.max() < 1e-8 and al.sum() == 2,
          'sum S^z S^z on 20 sites, dmrgpy gives %.4f and the largest bond entropy %.0e, and the ground level has %d '
          'states, whose symmetric combination has ln 2 at every cut' % (ez, sz_.max(), al.sum()))

    L = 12
    H0, st0 = heis(L, chain_bonds([1.0] * (L - 1)), L // 2)
    Hm, stm = heis(L, chain_bonds([1.0] * (L - 1)), L // 2 - 1)
    (eg,), vg = lowest(H0)
    (et,), vt = lowest(Hm)
    g0, t1 = full(vg[:, 0], st0, L), full(vt[:, 0], stm, L)
    idx = np.arange(2 ** L)
    prof = np.array([abs(0.5 * np.dot(t1[idx ^ (1 << i)], g0)) for i in range(L)])   # |<1,-1|S^x_i|0>|
    profiles = {}
    for Bz in (0.03, 0.0):
        sc, h = spin_chain(L, field=[Bz] * L)
        _, wfs = quiet(sc.get_excited_states, mode="DMRG", n=2)
        w0, w1 = wfs[0], wfs[1]
        px = np.array([abs(w1.dot(sc.Sx[i] * w0)) for i in range(L)])
        tot = np.array([sum(abs(w1.dot(o[i] * w0)) ** 2 for o in (sc.Sx, sc.Sy, sc.Sz)) for i in range(L)])
        profiles[Bz] = (px, tot)
    px, tot = profiles[0.0]
    scale = px @ prof / (prof @ prof)
    check('the cell on the excited state', abs(et - eg - 0.2809) < 5e-5 and abs(prof.max() - 0.179) < 5e-4
          and np.abs(profiles[0.03][0] - prof).max() < 2e-3 and np.abs(px - scale * prof).max() < 3e-3
          and scale < np.sqrt(2) + 0.02 and np.abs(tot - 2 * prof ** 2).max() < 2e-3,
          '12 sites, the triplet is %.4f above the singlet, %.4f with Bz = 0.03 and S^z = -1, the largest |<1|S^x_i|0>| '
          'is %.4f and dmrgpy with Bz = 0.03 agrees to %.0e; with Bz = 0 this run gave the same profile times %.3f, and '
          'the sum over x, y, z is 2 |<1|S^x_i|0>|^2 of the field, %.4f at its largest' % (et - eg, et - eg - 0.03,
                                                                                         prof.max(), np.abs(profiles[0.03][0] - prof).max(), scale, tot.max()))

    # ---------------------------------------------------------------- statements of the pages
    check('7.3, sixteen gigabytes', abs(b30 / 1e9 - 17.2) < 0.05, 'L = 30 is %.1f GB with the 1e9 bytes of the dashed line' % (b30 / 1e9))
    check('7.3 and 7.4, the product state', count(40, 1)[0] == 80 and count(100, 1)[0] == 200,
          'the MPS with M = 1 stores 2 numbers per site, 80 for 40 sites, 1280 bytes')
    check('7.3, exact diagonalization in the first cell', 'mode="DMRG"' in c3 and 'mode="ED"' not in c3,
          'the cell runs DMRG')
    check('7.5 and 7.8a, L M^2', abs(flops[200] / flops[100] - 7.81) < 0.01,
          'the time of a local step grows by %.2f from M = 100 to 200, so as M^3' % (flops[200] / flops[100]))
    check('7.8a, the central bonds', S20[9] < odd.min() and S20[9] < LN2,
          'the center has %.3f, below every odd cut and below the %.3f of the first cut' % (S20[9], S20[0]))
    check('7.8a and 7.8b, the saturation', flu[23] < flu[11] and abs(en[11] - en[23]) < 2e-5 and S20.max() < np.log(3),
          'the fluctuation still falls from maxm = 11 to 23 while the energy changes by %.0e, and the 20 sites need at most '
          '%.3f < ln 3' % (abs(en[11] - en[23]), S20.max()))
    check('7.8b, the area law in a gapless chain', cen[3] - cen[1] > 0.1 and nbv[1] > nbv[2],
          'the center grows by %.3f from 20 to 40 sites, and the cut of the cell zigzags' % (cen[3] - cen[1]))
    check('7.8b, ln chi at small chi', bd[(10, 2)] < 0.5 * LN2 and bd[(30, 2)] < 0.6 * LN2,
          'maxm = 2 gives %.3f and %.3f against ln 2 = %.3f' % (bd[(10, 2)], bd[(30, 2)], LN2))
    check('7.11, 0.77 and 2.3', abs(R['crit'][2][0] - 0.77) < 0.005 and abs(R['crit'][1] - 3.03) < 0.005,
          'the term ln(l)/3 is %.2f and %.2f, the entropy %.2f and %.2f' % (R['crit'][2][0], R['crit'][2][1], R['crit'][0], R['crit'][1]))
    check('7.11, the peak of the scan', scan[40][0] < 0.5 and scan[40][1] > exact[40] + 0.2,
          'the exact entropy of 40 sites is largest at %.2f, %.3f, and %.3f at 0.5' % (scan[40][0], scan[40][1], exact[40]))
    print('%d checks hold, %.1f s' % (COUNT[0], time.time() - t0))


if __name__ == '__main__':
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            main()
        finally:
            os.chdir(cwd)
