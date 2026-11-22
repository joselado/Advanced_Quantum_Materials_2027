"""Checks of webnotes/conventions/session06.md, with numbers. Every bullet of the sheet has one check here, in the order
of the sheet, and every number of a bullet is asserted, as a value or as the range that the bullet states. It prints
one line per check and exits 0 when all hold. It writes no file: pyqula runs in a temporary folder.

Not asserted, since they are not a number: what the cells of the notebook plot and how they label it (read from
jupyter-notebooks/session6.ipynb), and the words of the pages quoted in the last section of the sheet, whose numbers
are asserted again there. That a Hamiltonian passed as mf is taken with its hoppings was read in obj2mf of
pyqula/scftk/mfconstrains.py, and its outcome is asserted in the recipe test. The des Cloizeaux-Pearson
limit (pi/2) J |sin k| is a closed form, and only a ring of 12 spins is computed. The script needs pyqula and dmrgpy.

Run it from anywhere:  python3 webnotes/checks/session06/conventions.py"""
import os, sys, tempfile, time
from functools import reduce
import numpy as np
import scipy.sparse as sp
from scipy.optimize import brentq, minimize

sys.dont_write_bytecode = True
WEBNOTES = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(WEBNOTES, 'figures'))
sys.path.insert(0, os.path.join(WEBNOTES, 'figures', 'session06'))
import physcheck as pc
import _haldane as hd

COUNT = [0]
PAULI = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], complex)]


def check(name, ok, detail):
    """Prints one line for a check and stops the script when it does not hold."""
    print(('ok    ' if ok else 'FAIL  ') + name + ': ' + detail, flush=True)
    assert ok, name
    COUNT[0] += 1


def near(x, y, tol):
    return abs(x - y) < tol


# ---------------------------------------------------------------- closed forms of the chain, t = 1

def avg(f, nk=200000):
    """The average over the zone of the chain of f(eps_k), eps_k = -2 cos k, on a mesh that avoids the Fermi points."""
    k = 2 * np.pi * (np.arange(nk) + 0.5) / nk
    return np.mean(f(-2 * np.cos(k)))


def chain_afm(U):
    """The Neel state of the half-filled chain from 1 = (U/2) <1/E>, E = sqrt(eps^2 + Delta^2). Returns the energy per
    site <H_kin> + U <n_up><n_down>, the moment m = 2 Delta/U and Delta."""
    D = brentq(lambda D: (U / 2) * avg(lambda e: 1 / np.sqrt(e * e + D * D)) - 1, 1e-12, 10 * U, xtol=1e-15)
    m = 2 * D / U
    return avg(lambda e: -e * e / np.sqrt(e * e + D * D)) + U * (1 - m * m) / 4, m, D


def chain_uniform(U, n, m):
    """Energy per site of the uniform state of the chain at density n with n_up - n_down = m."""
    return -(4 / np.pi) * np.sin(np.pi * n / 2) * np.cos(np.pi * m / 2) + U * (n * n - m * m) / 4


def square_afm(U, nk=400):
    """The Neel state of the half-filled square lattice on a k-mesh, energy per site and moment."""
    k = 2 * np.pi * (np.arange(nk) + 0.5) / nk
    e = -2 * (np.cos(k)[:, None] + np.cos(k)[None, :])
    D = brentq(lambda D: (U / 2) * np.mean(1 / np.sqrt(e * e + D * D)) - 1, 1e-6, 5 * U)
    m = 2 * D / U
    return -np.mean(e * e / np.sqrt(e * e + D * D)) + U * (1 - m * m) / 4, m


def square_pm(U, nk=400):
    k = 2 * np.pi * (np.arange(nk) + 0.5) / nk
    e = -2 * (np.cos(k)[:, None] + np.cos(k)[None, :])
    return -np.mean(np.abs(e)) + U / 4


def hartree_fock(H0, U, ne, rng, mix=0.6, tol=1e-10, maxit=40000):
    """Unrestricted Hartree-Fock of a finite system, orbitals 2i + s, from a random direction on every site. The
    onsite field is U[(Tr rho) - rho] with rho[a, b] = <c_b^dag c_a>, and the energy is
    Tr(H0 rho) + U sum_i (<n_up><n_dn> - |<c_up^dag c_dn>|^2). Returns the energy and <sigma> of each site."""
    n = H0.shape[0] // 2
    v = rng.normal(size=(n, 3))
    v /= np.linalg.norm(v, axis=1)[:, None]
    rho = [0.5 * np.eye(2) + 0.25 * sum(v[i, a] * PAULI[a] for a in range(3)) for i in range(n)]
    for it in range(maxit):
        V = np.zeros_like(H0)
        for i in range(n):
            V[2 * i:2 * i + 2, 2 * i:2 * i + 2] = U * (np.trace(rho[i]) * np.eye(2) - rho[i])
        w = np.linalg.eigh(H0 + V)[1][:, :ne]
        P = w @ w.conj().T
        new = [P[2 * i:2 * i + 2, 2 * i:2 * i + 2] for i in range(n)]
        err = max(np.abs(new[i] - rho[i]).max() for i in range(n))
        rho = [(1 - mix) * rho[i] + mix * new[i] for i in range(n)]
        if err < tol:
            break
    E = np.real(np.trace(H0 @ P)) + U * sum(np.real(r[0, 0] * r[1, 1]) - abs(r[0, 1]) ** 2 for r in new)
    return E, np.array([[np.real(np.trace(r @ p)) for p in PAULI] for r in new]), err


def angles(M):
    """Angles in degrees between the moments of neighbors along a chain."""
    return np.array([np.degrees(np.arccos(np.clip(M[i] @ M[i + 1] / np.linalg.norm(M[i]) / np.linalg.norm(M[i + 1]),
                                                  -1, 1))) for i in range(len(M) - 1)])


# ---------------------------------------------------------------- many-body helpers

def fermions(norb):
    """Annihilation operators of norb fermionic orbitals, Jordan-Wigner, dense. The empty state is the first one."""
    a, Z, I = np.array([[0, 1], [0, 0]], float), np.diag([1.0, -1.0]), np.eye(2)
    return [reduce(np.kron, [Z] * p + [a] + [I] * (norb - p - 1)) for p in range(norb)]


def hubbard_levels(L, t, U, nel):
    """Levels of the open Hubbard chain -t sum (c^dag c + h.c.) + U sum n_up n_down with nel electrons."""
    c = fermions(2 * L)
    H = 0
    for i in range(L - 1):
        for s in (0, 1):
            H = H - t * (c[2 * i + s].T @ c[2 * i + 2 + s] + c[2 * i + 2 + s].T @ c[2 * i + s])
    for i in range(L):
        H = H + U * (c[2 * i].T @ c[2 * i]) @ (c[2 * i + 1].T @ c[2 * i + 1])
    N = np.diag(sum(x.T @ x for x in c))
    idx = np.where(np.abs(N - nel) < 1e-9)[0]
    return np.linalg.eigvalsh(H[np.ix_(idx, idx)])


def spin_matrices(S):
    """S^+, S^-, S^z of a spin S in the basis S^z = S, S-1, ..."""
    d = int(round(2 * S + 1))
    m = S - np.arange(d)
    Sp = np.zeros((d, d))
    for i in range(1, d):
        Sp[i - 1, i] = np.sqrt(S * (S + 1) - m[i] * (m[i] + 1))
    return Sp, Sp.T, np.diag(m)


def heisenberg_ring(N, S, J):
    """H = J sum S_i.S_(i+1) on a ring, and the total S^z, sparse."""
    Sp, Sm, Sz = (sp.csr_matrix(x) for x in spin_matrices(S))
    one = sp.identity(Sz.shape[0], format='csr')
    site = lambda o, i: reduce(lambda a, b: sp.kron(a, b, format='csr'), [one] * i + [o] + [one] * (N - i - 1))
    ops = [(site(Sp, i), site(Sm, i), site(Sz, i)) for i in range(N)]
    H, Mz = 0, 0
    for i in range(N):
        (pi, mi, zi), (pj, mj, zj) = ops[i], ops[(i + 1) % N]
        H = H + J * (zi @ zj + 0.5 * (pi @ mj + mi @ pj))
        Mz = Mz + zi
    return H, Mz.diagonal()


def _act(op, s, state):
    """A spin-1/2 operator on site s of a state {bits: amplitude}, bit 1 is up."""
    out = {}
    for b, a in state.items():
        up = (b >> s) & 1
        if op == 'z':
            out[b] = out.get(b, 0) + a * (0.5 if up else -0.5)
        elif op == '+' and not up:
            out[b | (1 << s)] = out.get(b | (1 << s), 0) + a
        elif op == '-' and up:
            out[b & ~(1 << s)] = out.get(b & ~(1 << s), 0) + a
    return out


def _component(c, s, state):
    if c == 'z':
        return _act('z', s, state)
    p, m = _act('+', s, state), _act('-', s, state)
    if c == 'x':
        return {k: 0.5 * (p.get(k, 0) + m.get(k, 0)) for k in set(p) | set(m)}
    return {k: (p.get(k, 0) - m.get(k, 0)) / 2j for k in set(p) | set(m)}


def one_flip(N, terms):
    """The matrix of a spin-1/2 Hamiltonian sum coef * S_i^a S_j^b in the states with one spin down, measured from
    the fully polarized state, and the largest weight that leaves these states."""
    full = (1 << N) - 1
    basis = [full & ~(1 << i) for i in range(N)]
    index = {b: i for i, b in enumerate(basis)}

    def apply(b):
        tot = {}
        for coef, ops in terms:
            st = {b: 1.0}
            for c, s in reversed(ops):
                st = _component(c, s, st)
            for k, a in st.items():
                tot[k] = tot.get(k, 0) + coef * a
        return tot
    E0 = apply(full).get(full, 0)
    H, leak = np.zeros((N, N), complex), 0.0
    for col, b in enumerate(basis):
        for k, a in apply(b).items():
            if k in index:
                H[index[k], col] += a
            else:
                leak = max(leak, abs(a))
    return H - E0 * np.eye(N), leak


def classical_chain(J, D, N=30, seeds=(1, 2, 3)):
    """Minimum of sum J S_i.S_(i+1) + D z.(S_i x S_(i+1)) for unit classical spins on an open chain. Returns the
    energy per bond, the cosine between two neighbors in the middle and the z component of their cross product."""
    def spins(x):
        th, ph = x[:N], x[N:]
        return np.stack([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)], axis=1)

    def energy(x):
        s = spins(x)
        return np.sum(J * np.sum(s[:-1] * s[1:], axis=1) + D * (s[:-1, 0] * s[1:, 1] - s[:-1, 1] * s[1:, 0]))
    best = None
    for seed in seeds:
        x0 = np.random.default_rng(seed).uniform(0, np.pi, 2 * N) * np.r_[np.ones(N), 2 * np.ones(N)]
        r = minimize(energy, x0, method='L-BFGS-B', options=dict(maxiter=20000, gtol=1e-12))
        if best is None or r.fun < best.fun:
            best = r
    s = spins(best.x)
    i = N // 2
    return best.fun / (N - 1), s[i] @ s[i + 1], s[i, 0] * s[i + 1, 1] - s[i, 1] * s[i + 1, 0]


def honeycomb_magnon_exact(L=3, J=-1.0, D=0.2):
    """The exact one-magnon Bloch matrix of a spin-1/2 honeycomb ferromagnet on an L x L torus, with
    H = J sum_<ij> S_i.S_j + D sum_<<ij>> nu_ij z.(S_i x S_j), nu_ij = +1 when the path i -> k -> j turns left.
    The lattice is the one of _haldane, A at the lattice points and B at (a1+a2)/3."""
    site = lambda n, m, s: 2 * ((n % L) * L + (m % L)) + s
    pos = lambda n, m, s: n * hd.a1 + m * hd.a2 + s * (hd.a1 + hd.a2) / 3
    terms, pairs = [], set()
    for n in range(L):
        for m in range(L):
            for dn, dm in hd.NN:
                i, j = site(n, m, 0), site(n + dn, m + dm, 1)
                terms += [(J, [(c, i), (c, j)]) for c in 'xyz']
            for s in (0, 1):
                for dn, dm in [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]:
                    i, j = site(n, m, s), site(n + dn, m + dm, s)
                    if (min(i, j), max(i, j)) in pairs:
                        continue
                    pairs.add((min(i, j), max(i, j)))
                    ri, rj = pos(n, m, s), pos(n + dn, m + dm, s)
                    rk = [pos(n + a, m + b, 1 - s) for a in range(-2, 3) for b in range(-2, 3)
                          if abs(np.linalg.norm(pos(n + a, m + b, 1 - s) - ri) - 1 / np.sqrt(3)) < 1e-9
                          and abs(np.linalg.norm(pos(n + a, m + b, 1 - s) - rj) - 1 / np.sqrt(3)) < 1e-9][0]
                    d1, d2 = rk - ri, rj - rk
                    nu = np.sign(d1[0] * d2[1] - d1[1] * d2[0])
                    terms += [(D * nu, [('x', i), ('y', j)]), (-D * nu, [('y', i), ('x', j)])]
    M, leak = one_flip(2 * L * L, terms)

    def hk(k):
        h = np.zeros((2, 2), complex)
        for s in (0, 1):
            for s2 in (0, 1):
                for n in range(L):
                    for m in range(L):
                        nn, mm = (n if n <= L // 2 else n - L), (m if m <= L // 2 else m - L)
                        h[s, s2] += M[site(n, m, s), site(0, 0, s2)] * np.exp(1j * k @ (nn * hd.a1 + mm * hd.a2))
        return h
    return hk, leak


def moments(h, nk=None):
    """The three components of n_up - n_down on each site."""
    kw = {} if nk is None else dict(nk=nk)
    return np.array([np.array(h.get_vev(o, **kw)).real for o in ('mx', 'my', 'mz')]).T


def mz(h, nk=None):
    kw = {} if nk is None else dict(nk=nk)
    return np.array(h.get_vev('mz', **kw)).real


def main():
    """Runs every check. The pyqula calls write files, so the caller runs this in a temporary folder."""
    from pyqula import geometry
    from pyqula.scftk.convergence import MeanFieldConvergenceError
    t0 = time.time()
    gb, g1 = geometry.bichain(), geometry.chain()

    # ---------------- the magnetization and the Hubbard term
    cu, cd = fermions(2)
    nup, ndn = cu.T @ cu, cd.T @ cd
    n, mop = nup + ndn, nup - ndn
    Sx, Sy, Sz = 0.5 * (cu.T @ cd + cd.T @ cu), -0.5j * (cu.T @ cd - cd.T @ cu), 0.5 * mop
    S2 = Sx @ Sx + Sy @ Sy + Sz @ Sz
    vac = np.zeros(4); vac[0] = 1
    up, xs = cu.T @ vac, (cu.T @ vac + cd.T @ vac) / np.sqrt(2)
    ev = lambda o, s: float(np.real(s @ o @ s))
    check('the m of (1.8) and (6.2)', near(ev(mop, up), 1, 1e-12) and near(ev(Sz, up), 0.5, 1e-12)
          and near(ev(mop, xs), 0, 1e-12) and near(ev(Sx, xs), 0.5, 1e-12),
          'one spin up has m = %.0f and <S^z> = %.1f, the spinor (1,1)/sqrt2 has m = %.0f and <S^x> = %.1f'
          % (ev(mop, up), ev(Sz, up), ev(mop, xs), ev(Sx, xs)))

    d1 = np.abs(nup @ ndn - (n / 2 - 2 / 3 * S2)).max()
    d2 = np.abs(nup @ ndn - 0.25 * (n @ n - mop @ mop)).max()
    d3 = np.abs(S2 - 0.75 * (n - 2 * nup @ ndn)).max()
    check('the Hubbard term in spin form', max(d1, d2, d3) < 1e-12,
          'U n_up n_down = U n/2 - (2U/3) S^2 = (U/4)(n^2 - m^2) and S^2 = (3/4)(n - 2 n_up n_down) to %.0e on the 4 states'
          % max(d1, d2, d3))

    split = []
    for direction in (2, 0):                                  # m = 0.2 along z, then along x, one electron
        rho = 0.5 * np.eye(2) + 0.5 * 0.2 * PAULI[direction]
        V = np.trace(rho) * np.eye(2) - rho                  # Hartree-Fock field for U=1
        split.append(np.ptp(np.linalg.eigvalsh(V)))
        coef = np.real(np.trace(V @ PAULI[direction])) / 2
        mean = np.real(np.trace(V)) / 2                       # the coefficient of the identity, U n/2 with n = 1
    s2route = np.ptp(np.linalg.eigvalsh(-(4 / 3) * 0.1 * PAULI[0] / 2))     # -(2U/3) 2<S>.S with <S> = m/2 = 0.1 and S = sigma/2
    check('the Hartree decoupling and the exchange splitting', near(split[0], 0.2, 1e-12) and near(split[1], 0.2, 1e-12)
          and near(coef, -0.1, 1e-12) and near(mean, 0.5, 1e-12) and near(s2route, 2 / 3 * 0.2, 1e-12),
          'with m = 0.2 the Hartree-Fock field splits the spins by %.3f U along z and %.3f U along x, the coefficient of '
          'sigma is %+.2f U = -U m/2 and of the identity %.2f U = U n/2, and the S^2 decoupling splits by %.4f U = (2/3) U m'
          % (split[0], split[1], coef, mean, s2route))

    U = 4.0
    h4, E4 = gb.get_hamiltonian().get_mean_field_hamiltonian(U=U, mf='antiferro', nk=40, return_total_energy=True)
    v4 = mz(h4, 40)
    e4, m4, D4 = chain_afm(U)
    gap4 = h4.get_gap()
    np.random.seed(1)
    hxy, Exy = gb.get_hamiltonian().get_mean_field_hamiltonian(U=U, mf='XY', mix=0.9, nk=40, return_total_energy=True)
    Mxy = moments(hxy, 40)
    check('mf="XY" gives the same magnet in the plane', near(abs(v4[0]), 0.7690, 5e-5) and np.allclose(np.linalg.norm(Mxy, axis=1), 0.7690, atol=5e-5)
          and np.abs(Mxy[:, 2]).max() < 1e-6 and near(gap4, 3.076, 1e-3) and near(hxy.get_gap(), 3.076, 1e-3) and near(Exy, E4, 2e-5),
          '|m| %.4f along z and %.4f in the plane, gaps %.4f and %.4f, energies %.6f and %.6f per cell'
          % (abs(v4[0]), np.linalg.norm(Mxy, axis=1)[0], gap4, hxy.get_gap(), E4, Exy))

    # ---------------- the half-filled chain in mean field
    sol = {u: chain_afm(u) for u in (1.0, 2.0, 4.0, 16.0)}
    h2 = gb.get_hamiltonian().get_mean_field_hamiltonian(U=2.0, mf='antiferro', nk=200)
    v2 = abs(mz(h2, 200)[0])
    h1 = gb.get_hamiltonian().get_mean_field_hamiltonian(U=1.0, mf='antiferro', nk=1001)
    v1, v1d = abs(mz(h1, 1001)[0]), abs(mz(h1)[0])
    ok = all(near(sol[u][1], x, 5e-5) for u, x in ((1.0, 0.0299), (2.0, 0.3404), (4.0, 0.7690), (16.0, 0.9844)))
    ok = ok and near(sol[4.0][0], -0.46911, 1e-5) and near(sol[1.0][2], 8 * np.exp(-2 * np.pi), 1e-4) and near(sol[1.0][2], 0.0149, 5e-5)
    ok = ok and near(v1, 0.0302, 5e-5) and near(1.0 * sol[1.0][1], 0.03, 5e-4) and near(v2, 0.3404, 5e-4) and near(gap4, U * m4, 1e-3) and near(1 - m4 ** 2, 0.409, 5e-4)
    check('the antiferromagnet of the half-filled chain', ok,
          'm = %.4f, %.4f, %.4f, %.4f at U = 1, 2, 4, 16, E = %.5f per site at 4, Delta = %.4f at 1 against 8 exp(-2 pi/U) = %.4f; '
          'pyqula %.4f at 1 with nk=1001 and %.4f at 2 with nk=200, gap %.4f = U m at 4, and 1 - m^2 = %.3f at 4'
          % (sol[1.0][1], sol[2.0][1], sol[4.0][1], sol[16.0][1], sol[4.0][0], sol[1.0][2], 8 * np.exp(-2 * np.pi), v1, v2,
             gap4, 1 - m4 ** 2))

    cross = brentq(lambda u: -4 / np.pi + u / 4, 1, 10)
    U_sat = brentq(lambda u: (-2 + u) - 2, 1, 10)          # the empty band, from -2 + U n_up, clears the full one at 2
    lower = all(chain_afm(u)[0] < min(-4 / np.pi + u / 4, 0.0) for u in (1.0, 3.0, 4.5, 6.0, 10.0, 20.0))
    seeded = []
    for u in (3.9, 4.1, 4.5):
        h = gb.get_hamiltonian()
        seed = h.copy(); seed.clean(); seed.add_zeeman([0.0, 0.0, u / 2])
        hs, Es = h.get_mean_field_hamiltonian(U=u, mf=seed, nk=40, mix=0.9, return_total_energy=True)
        seeded.append((abs(mz(hs, 40)[0]), Es))
    ok = near(cross, 16 / np.pi, 1e-9) and near(cross, 5.09, 5e-3) and near(2 * np.pi, 6.28, 5e-3) and lower
    ok = ok and near(U_sat, 4, 1e-9) and near(seeded[0][0], 0.025, 1e-3) and all(near(s[0], 1.0, 5e-4) and abs(s[1]) < 1e-6 for s in seeded[1:])
    check('the uniform states of the half-filled chain', ok,
          'the saturated state is self-consistent from U = %.0f, E_PM = -4/pi + U/4 crosses E_FM = 0 at U = %.3f = 16/pi, the paramagnet is unstable above 2 pi = %.2f, the '
          'antiferromagnet is below both at U = 1, 3, 4.5, 6, 10, 20, and the seed of the saturated field gives |m| = %.3f '
          'at 3.9 and %.3f and %.3f with the energy %.0e at 4.1 and 4.5' % (U_sat, cross, 2 * np.pi, seeded[0][0], seeded[1][0],
                                                                             seeded[2][0], seeded[1][1]))

    out = []
    for u in (20.0, 40.0):
        ha, Ea = gb.get_hamiltonian().get_mean_field_hamiltonian(U=u, mf='antiferro', nk=20, return_total_energy=True)
        hf, Ef = gb.get_hamiltonian().get_mean_field_hamiltonian(U=u, mf='ferro', nk=20, return_total_energy=True)
        out.append((u, Ef - Ea, -2 * chain_afm(u)[0]))
    ok = near(out[0][1], 0.1995, 5e-5) and near(out[1][1], 0.0999, 5e-5) and all(near(a, b, 1e-4) for u, a, b in out)
    ok = ok and near(20 * out[0][1], 3.990, 5e-4) and near(40 * out[1][1], 3.998, 1e-3)
    check('E_FM - E_AFM at large U', ok,
          ', '.join('U=%.0f gives %.4f per cell, numpy %.4f, U times it %.4f' % (u, a, b, u * a) for u, a, b in out)
          + ', so J per cell and J/2 = 2 J S^2 per bond')

    gd = geometry.bichain(); gd.dimensionality = 0
    dim = []
    for u in (1.8, 1.9, 2.1, 2.2, 2.5, 4.0, 10.0):
        hd0 = gd.get_hamiltonian().get_mean_field_hamiltonian(U=u, mf='antiferro', mix=0.9)
        dim.append((u, abs(mz(hd0)[1]), hd0.get_gap()))
    ok = all(m < 1e-3 and near(g, 2.0, 1e-3) for u, m, g in dim[:2])
    ok = ok and all(near(m, np.sqrt(1 - 4 / u ** 2), 2e-3) and near(g, u, 2e-3) for u, m, g in dim[2:])
    ok = ok and all(near(m, x, 1e-3) for (u, m, g), x in zip(dim[2:], (0.305, 0.4165, 0.600, 0.866, 0.980)))
    cdim = fermions(4)
    vac4 = np.zeros(16); vac4[0] = 1.0
    Ht = -sum(cdim[s].T @ cdim[2 + s] + cdim[2 + s].T @ cdim[s] for s in (0, 1))
    Hu = 8.0 * sum((cdim[2 * i].T @ cdim[2 * i]) @ (cdim[2 * i + 1].T @ cdim[2 * i + 1]) for i in (0, 1))
    Ntot = np.diag(sum(x.T @ x for x in cdim))
    idx = np.where(np.abs(Ntot - 2) < 1e-9)[0]
    gs = np.linalg.eigh((Ht + Hu)[np.ix_(idx, idx)])[1][:, 0]
    full = np.zeros(16); full[idx] = gs
    Stot = [sum(0.5 * sum(PAULI[k][a, b] * (cdim[2 * i + a].T @ cdim[2 * i + b]) for a in range(2) for b in range(2))
                for i in (0, 1)) for k in range(3)]
    s2gs = np.real(full @ sum(s @ s for s in Stot) @ full)
    check('the mean-field dimer', ok and abs(s2gs) < 1e-12,
          'pyqula gives %s, against sqrt(1 - 4/U^2), with the gap 2 below U = 2 and U above, and the exact ground state at '
          'U = 8 has S^2 = %.0e' % (', '.join('%.4f at %.1f' % (m, u) for u, m, g in dim), s2gs))

    # ---------------- pyqula in mean field
    updn4 = np.array(h4.get_vev('up', nk=40)).real - np.array(h4.get_vev('dn', nk=40)).real
    hst = g1.get_hamiltonian().get_mean_field_hamiltonian(U=1.8, filling=0.1, mf='ferro', mix=0.9, nk=300)
    m_loop, m_def = np.abs(mz(hst, 300)).mean(), np.abs(mz(hst)).mean()
    same30 = np.array_equal(mz(h1), mz(h1, 30))
    check('get_vev("mz") and its mesh', near(abs(v4[0]), 0.7690, 5e-5) and v4[0] * v4[1] < 0 and np.allclose(updn4, v4, atol=1e-6)
          and same30 and near(v1d, 0.0503, 5e-4) and near(v1, 0.0302, 5e-5) and near(m_def, 0.13, 5e-3) and near(m_loop, 0.087, 5e-4),
          'n_up - n_down = %+.4f %+.4f, the same as up minus dn; without nk it is the value with nk=30; at U=1 it reads %.4f '
          'without nk for %.4f on the mesh of the '
          'loop; the Stoner cell at U=1.8 reads %.3f without nk for %.3f with nk=300' % (v4[0], v4[1], v1d, v1, m_def, m_loop))

    ex4 = np.array(h4.extract('mz')).real
    check('extract("mz") is the field', np.allclose(ex4, -U * v4 / 2, atol=1e-4) and near(ex4[np.argmin(v4)], 1.538, 1e-3),
          'extract gives %+.4f %+.4f = -U m/2 for m = %+.4f %+.4f' % (ex4[0], ex4[1], v4[0], v4[1]))

    dens = []
    for fill in (0.1, 0.25, 0.5):
        hh = g1.get_hamiltonian().get_mean_field_hamiltonian(U=0.0, filling=fill, nk=200)
        dens.append((fill, float(np.real(hh.get_vev(None, nk=200))[0]), float(np.real(hh.get_vev('up', nk=200))[0])))
    h3 = g1.get_hamiltonian().get_mean_field_hamiltonian(U=3.0, filling=0.1, mf='ferro', mix=0.9, nk=300)
    m3 = mz(h3, 300)[0]
    hf20 = gb.get_hamiltonian().get_mean_field_hamiltonian(U=20.0, mf='ferro', nk=20)
    m20 = mz(hf20, 20)
    from pyqula.meanfield import guess
    zeeman = np.real(np.diag(np.array(guess(gb.get_hamiltonian(), 'ferro'))))      # orbitals (site, up), (site, down)
    ok = all(near(d, 2 * f, 1e-9) and near(u, f, 1e-9) for f, d, u in dens) and near(m3, -0.2, 1e-4) and np.allclose(m20, -1, atol=1e-3)
    ok = ok and np.allclose(zeeman, [0.1, -0.1, 0.1, -0.1], atol=1e-12)
    check('filling and the sign of the ferro guess', ok,
          ', '.join('filling %.2f gives %.2f electrons and %.2f up' % x for x in dens)
          + ', the ferro guess is the field %s on (up, down) and gives m = %+.3f at n=0.2 and U=3 and %+.3f at half filling '
            'and U=20' % (' '.join('%+.1f' % z for z in zeeman), m3, m20[0]))

    gen = g1.get_hamiltonian().get_hk_gen()
    e0, e5 = np.linalg.eigvalsh(gen([0.0, 0, 0])), np.linalg.eigvalsh(gen([0.5, 0, 0]))
    gen3 = h3.get_hk_gen()
    emin = min(np.linalg.eigvalsh(gen3([k, 0, 0]))[0] for k in np.linspace(0, 1, 801))
    efrom = -2 + 4.0 * 0.2
    ok = np.allclose(e0, 2) and np.allclose(e5, -2) and near(emin, -(2 - 2 * np.cos(0.2 * np.pi)), 1e-6) and near(emin, -0.382, 5e-4)
    ok = ok and near(-2 * np.cos(0.2 * np.pi), -1.618, 5e-4) and near(efrom, -1.2, 1e-12) and efrom > -2 * np.cos(0.2 * np.pi)
    check('the band of geometry.chain() and the zero of energy', ok,
          'E(k=0) = %+.0f and E(k=0.5) = %+.0f, the filled band of the ferromagnet with n=0.2 starts at %.4f in pyqula, and in '
          'the frame of the notes mu = %.3f and the empty band starts at %.1f for U=4' % (e0[0], e5[0], emin, -2 * np.cos(0.2 * np.pi), efrom))

    h0, E0 = gb.get_hamiltonian().get_mean_field_hamiltonian(U=0.0, nk=200, return_total_energy=True)
    check('return_total_energy', near(E0, -8 / np.pi, 2e-3) and near(E4, 2 * e4, 1e-4) and near(E4, -0.93819, 2e-5),
          'the bichain gives %.4f = -8/pi at U=0 and %.5f at U=4 per cell, numpy 2 x %.5f; the term with c+_up c_dn is '
          'checked on the Rashba chain' % (E0, E4, e4))

    stuck = {}
    for u in (6.0, 9.0, 12.0, 20.0):
        for nk in (None, 51):
            kw = {} if nk is None else dict(nk=nk)
            hp, Ep = gb.get_hamiltonian().get_mean_field_hamiltonian(U=u, mf='ferro', mix=0.9, return_total_energy=True, **kw)
            stuck[(u, nk)] = (abs(mz(hp, nk or 8)[0]), Ep)
    ok = all(near(stuck[(u, None)][0], 1 / 8, 1e-3) and near(stuck[(u, None)][1], x, 5e-3) for u, x in ((6.0, 0.44), (9.0, 1.92), (12.0, 3.39)))
    ok = ok and all(near(stuck[(u, 51)][0], 2 / 51, 1e-3) for u in (6.0, 9.0)) and near(stuck[(12.0, 51)][0], 1, 1e-4)
    ok = ok and near(stuck[(20.0, None)][0], 1, 1e-4) and abs(stuck[(20.0, None)][1]) < 1e-6
    hp, Ep = gb.get_hamiltonian().get_mean_field_hamiltonian(U=10.0, mf='ferro', mix=0.9, nk=51, return_total_energy=True)
    ok = ok and near(abs(mz(hp, 51)[0]), 1, 1e-4)
    hnb, Enb = gb.get_hamiltonian().get_mean_field_hamiltonian(U=6.0, mf='ferro', return_total_energy=True)     # the notebook call
    ok = ok and np.allclose(np.abs(mz(hnb, 8)), 1 / 8, atol=1e-3) and near(Enb, 0.44, 5e-3)
    check('the ferro guess stops at states of the mesh', ok,
          'half filling, default nk=8: |m| = %.4f, %.4f, %.4f at U = 6, 9, 12 with energies %.2f, %.2f, %.2f per cell above '
          'the saturated 0, and %.4f at U=20; nk=51: %.4f = 2/51 at 6 and 9, %.4f at 10; the call of the notebook at U=6 '
          'gives %.4f' %
          (stuck[(6.0, None)][0], stuck[(9.0, None)][0], stuck[(12.0, None)][0], stuck[(6.0, None)][1], stuck[(9.0, None)][1],
           stuck[(12.0, None)][1], stuck[(20.0, None)][0], stuck[(6.0, 51)][0], abs(mz(hp, 51)[0]), abs(mz(hnb, 8)[0])))

    gsq = geometry.square_lattice_bipartite()
    sq = []
    for nk in (8, 12, 21):
        hfm, Ef = gsq.get_hamiltonian().get_mean_field_hamiltonian(U=3.0, mf='ferro', mix=0.9, nk=nk, return_total_energy=True)
        haf, Ea = gsq.get_hamiltonian().get_mean_field_hamiltonian(U=3.0, mf='antiferro', mix=0.9, nk=nk, return_total_energy=True)
        Ma, Mf = moments(haf, nk), moments(hfm, nk)
        units = Ma / np.linalg.norm(Ma, axis=1)[:, None]
        sq.append((nk, Ef - Ea, Ea, np.linalg.norm(Ma, axis=1), Ma[:, 2], units, np.linalg.norm(Mf, axis=1).max()))
    ea, ma = square_afm(3.0)
    ep = square_pm(3.0)
    ok = len(gsq.r) == 4 and all(near(s[1], x, 1.5e-3) for s, x in zip(sq, (0.296, 0.298, 0.300)))
    ok = ok and near(4 * (ep - ea), 0.302, 1e-3) and near(ma, 0.566, 5e-4) and near(4 * ea, -3.7864, 2e-4)
    ok = ok and all(np.allclose(s[3], 0.566, atol=1e-3) and s[6] < 0.15 for s in sq)
    ok = ok and all(np.allclose(s[5][0], -s[5][1], atol=1e-4) and np.allclose(s[5][0], s[5][2], atol=1e-4) for s in sq)
    ok = ok and near(abs(sq[0][4][0]), 0.21, 5e-3) and np.allclose(np.abs(sq[0][4]), abs(sq[0][4][0]), atol=1e-4)
    check('the square lattice of the notebook', ok,
          'four sites, E_ferro - E_antiferro = %s for nk = 8, 12, 21, numpy E_PM - E_AFM = %.3f, |m| = %.3f and %.4f per '
          'cell; pyqula |m| = %.3f on every site with opposite directions on the two sublattices, m_z = %s with nk=8, and the '
          'ferro guess has |m| below %.3f' % (' '.join('%.4f' % s[1] for s in sq), 4 * (ep - ea), ma, 4 * ea, sq[0][3][0],
                                               ' '.join('%+.3f' % x for x in sq[0][4]), max(s[6] for s in sq)))

    gl = geometry.lieb_lattice()
    lieb = {}
    for u in (0.3, 1.0, 2.0):
        for nk in (None, 12, 24):
            kw = {} if nk is None else dict(nk=nk)
            hl = gl.get_hamiltonian().get_mean_field_hamiltonian(U=u, mix=0.9, mf='ferro', **kw)
            lieb[(u, nk)] = mz(hl, nk)
    hl0 = gl.get_hamiltonian()
    kl = np.array([np.linalg.eigvalsh(hl0.get_hk_gen()([a, b, 0])) for a in np.linspace(0, 1, 7) for b in np.linspace(0, 1, 7)])
    flat = np.abs(kl[:, 2:4]).max()
    m1 = lieb[(1.0, None)]
    ok = flat < 1e-12 and all(near(v.sum(), -1.0, 1e-3) for v in lieb.values())
    ok = ok and near(np.sort(m1)[0], -0.551, 5e-4) and near(np.sort(m1)[1], -0.551, 5e-4) and near(np.sort(m1)[2], 0.102, 5e-4)
    ok = ok and max(np.abs(lieb[(1.0, a)] - lieb[(1.0, b)]).max() for a in (None, 12) for b in (12, 24)) < 3e-3
    check('the flat band of the Lieb lattice', ok,
          'flat to %.0e, total moment %s per cell at U = 0.3, 1, 2, and at U=1 the sites have %s with the default nk'
          % (flat, ' '.join('%+.3f' % lieb[(u, None)].sum() for u in (0.3, 1.0, 2.0)), ' '.join('%+.4f' % x for x in m1)))

    # ---------------- the Stoner criterion
    kk = 2 * np.pi * (np.arange(200000) + 0.5) / 200000
    thr = {}
    for nden in (1.0, 0.2, 0.1, 0.4):
        Uc = 2 * np.pi * np.sin(np.pi * nden / 2)
        kF = np.pi * nden / 2
        Dnum = np.mean(np.abs(-2 * np.cos(kk) + 2 * np.cos(kF)) < 1e-3) / 2e-3              # states per site and spin per energy
        curv = [(chain_uniform(u, nden, 1e-3) - chain_uniform(u, nden, 0.0)) for u in (0.99 * Uc, 1.01 * Uc)]
        thr[nden] = (Uc, 1 / (2 * np.pi * np.sin(kF)), Dnum, curv)
    Nk, q = 200000, 2 * np.pi * 20 / 200000
    kr = 2 * np.pi * np.arange(Nk) / Nk
    ek, ekq = -2 * np.cos(kr), -2 * np.cos(kr + q)
    chi0 = np.mean(((ek < 0).astype(float) - (ekq < 0)) / np.where(np.abs(ekq - ek) > 1e-14, ekq - ek, np.inf))
    ok = all(near(thr[x][0], v, 5e-4) for x, v in ((1.0, 6.283), (0.2, 1.942), (0.1, 0.983), (0.4, 3.693)))
    ok = ok and all(near(thr[x][2], thr[x][1], 0.02 * thr[x][1]) and thr[x][3][0] > 0 > thr[x][3][1] for x in thr)
    ok = ok and near(chi0, 1 / (2 * np.pi), 1e-3) and near(1 / (2 * np.pi), 0.1592, 5e-5)
    check('the D(E_F) of (6.3) and the threshold of the chain', ok,
          'U_c = 2 pi sin(pi n/2) = %.3f, %.3f, %.3f, %.3f at n = 1, 0.2, 0.1, 0.4, D(E_F) per spin on a k-mesh %s against '
          '1/(2 pi sin k_F), E(m) bends down there, and (9.4) at q = %.1e gives %.4f at half filling'
          % (thr[1.0][0], thr[0.2][0], thr[0.1][0], thr[0.4][0], ' '.join('%.4f' % thr[x][2] for x in thr), q, chi0))

    EF = -2 * np.cos(0.1 * np.pi)
    en = np.linspace(-3, 3, 1201)
    (e2, dos2) = g1.get_hamiltonian().get_dos(energies=en, delta=0.02, nk=2000)
    (e1, dos1) = g1.get_hamiltonian(has_spin=False).get_dos(energies=en, delta=0.02, nk=2000)
    (e5, dos5) = g1.get_hamiltonian(has_spin=False).get_dos(energies=np.array([EF]), delta=0.005, nk=20000)
    e2, dos2, dos1 = np.array(e2), np.array(dos2), np.array(dos1)
    tot, at2, at1 = np.trapezoid(dos2, e2), np.interp(EF, e2, dos2), np.interp(EF, e2, dos1)
    D02 = 1 / (2 * np.pi * np.sin(0.1 * np.pi))
    ok = near(tot, 1.989, 1e-3) and near(at2, 1.015, 1e-3) and near(2 * D02, 1.030, 1e-3) and near(at1, at2 / 2, 1e-6)
    ok = ok and near(at1, 0.507, 1e-3) and near(np.array(dos5)[0], 0.5145, 5e-4) and near(D02, 0.5150, 5e-5) and near(EF, -1.902, 5e-4)
    ok = ok and near(EF + 2, 0.1, 5e-3)
    check('get_dos counts both spins', ok,
          'the spinful chain integrates to %.4f between -3 and 3 and gives %.4f at E_F = %.4f, 2 D(E_F) = %.4f; has_spin=False '
          'gives %.4f, and %.4f with delta=0.005 and nk=20000, against D(E_F) = %.4f' % (tot, at2, EF, 2 * D02, at1, np.array(dos5)[0], D02))

    fm = []
    for fill in (0.1, 0.2):
        hm = g1.get_hamiltonian().get_mean_field_hamiltonian(U=4.0, filling=fill, mf='ferro', mix=0.9, nk=1000)
        ons = np.real(np.diag(np.array(hm.intra.todense() if hasattr(hm.intra, 'todense') else hm.intra)))
        fm.append((fill, abs(mz(hm, 1000)[0]), abs(ons[1] - ons[0])))
    htrap, Etrap = g1.get_hamiltonian().get_mean_field_hamiltonian(U=4.0, filling=0.2, mf='ferro', mix=0.9, nk=300,
                                                                     return_total_energy=True)
    mtrap, above = abs(mz(htrap, 300)[0]), Etrap - chain_uniform(4.0, 0.4, 0.4)
    ok = near(fm[0][1], 0.2, 1e-4) and near(fm[0][2], 0.8, 1e-3) and near(fm[1][1], 0.4, 1e-4) and near(fm[1][2], 1.6, 1e-3)
    ok = ok and near(mtrap, 0.060, 1e-3) and near(above, 0.017, 1e-3)
    check('the ferromagnet of the chain at U=4', ok,
          'filling=0.1 gives |m| = %.3f and the splitting %.3f, filling=0.2 gives %.3f and %.3f with nk=1000, and with nk=300 '
          'it stops at %.3f, %.3f per site above the saturated energy' % (fm[0][1], fm[0][2], fm[1][1], fm[1][2], mtrap, above))

    nden = 0.2
    U_min = brentq(lambda u: -2 + u * nden + 2 * np.cos(np.pi * nden), 0.5, 4)
    U_x = brentq(lambda u: chain_uniform(u, nden, nden) - chain_uniform(u, nden, 0.0), 1.5, 2.5)
    U_c = 2 * np.pi * np.sin(np.pi * nden / 2)
    interior = 0
    for nn in np.linspace(0.05, 1.95, 39):
        mg = np.linspace(0, min(nn, 2 - nn), 201)
        for u in np.linspace(0.1, 20, 200):
            e = chain_uniform(u, nn, mg)
            i = np.argmin(e)
            interior += int(0 < i < len(mg) - 1 and e[i] < min(e[0], e[-1]) - 1e-12)
    x = np.linspace(1e-3, np.pi / 2, 500)
    decreasing = np.all(np.diff((1 - np.cos(x)) / x ** 2) < 0)
    scan = {}
    for nk, us in ((300, (1.2, 1.8, 1.9, 2.0, 2.4, 3.0)), (1000, (1.2, 1.8, 1.9, 2.0, 2.4, 3.0)), (301, (1.2,))):
        for u in us:
            hm = g1.get_hamiltonian().get_mean_field_hamiltonian(U=u, filling=0.1, mf='ferro', mix=0.9, nk=nk)
            scan[(nk, u)] = float(np.mean(np.abs(mz(hm, nk))))
    mids = [scan[(nk, u)] for nk in (300, 1000) for u in (1.8, 1.9, 2.0)]
    ok = interior == 0 and decreasing and near(U_min, 1.910, 5e-4) and near(U_x, 1.926, 5e-4) and near(U_c, 1.942, 5e-4)
    ok = ok and all(scan[(nk, 1.2)] < 0.015 for nk in (300, 301, 1000))
    ok = ok and all(near(scan[(nk, u)], 0.2, 1e-4) for nk in (300, 1000) for u in (2.4, 3.0))
    ok = ok and near(min(mids), 0.026, 1e-3) and near(max(mids), 0.2, 1e-4)
    check('the chain jumps at the threshold', ok,
          'no interior minimum of the uniform energy at 39 fillings and 200 values of U; n=0.2: saturated from %.3f, crossing '
          'at %.3f, unstable at %.3f; pyqula gives %s at 1.2 (nk 300, 301, 1000), 0.200 at 2.4 and 3, and %.3f to %.3f at 1.8 to 2'
          % (U_min, U_x, U_c, ' '.join('%.4f' % scan[(nk, 1.2)] for nk in (300, 301, 1000)), min(mids), max(mids)))

    def F(x):
        x = np.clip(x, -2, 2)
        return 0.5 + (x * np.sqrt(4 - x ** 2) / 2 + 2 * np.arcsin(x / 2)) / (2 * np.pi)

    def msc(u):
        f = lambda m: F(u * m / 2) - F(-u * m / 2) - m
        if u <= np.pi:
            return 0.0
        return 1.0 if f(1.0) >= 0 else brentq(f, 1e-9, 1.0, xtol=1e-14)
    slope = (F(1e-6) - F(-1e-6)) / 2e-6
    ms = [msc(x * np.pi) for x in (0.99, 1.0025, 1.01)] + [msc(3.2), msc(4.0)]
    lead = [np.sqrt(96 / u ** 2 * (1 - np.pi / u)) for u in (1.0001 * np.pi, 1.001 * np.pi)]
    ok = near(slope, 1 / np.pi, 1e-6) and near(slope, 0.3183, 5e-5) and ms[0] == 0 and near(ms[1], 0.155, 5e-4)
    ok = ok and near(ms[2], 0.306, 5e-4) and near(ms[3], 0.41, 5e-3) and ms[4] == 1.0
    ok = ok and all(near(msc(u), l, 2e-3 * l) for u, l in zip((1.0001 * np.pi, 1.001 * np.pi), lead))
    check('the semicircle of the widget', ok,
          'D(E_F) = %.4f, threshold pi, m = %.4f, %.4f, %.4f at 0.99, 1.0025, 1.01 pi, %.3f at 3.2 and %.0f at 4, and the '
          'leading order sqrt((96/U^2)(1 - pi/U)) within 0.2 percent at 1.0001 pi and 1.001 pi' % (slope, *ms))

    nk, T = 240, 0.1
    k = 2 * np.pi * np.arange(nk) / nk
    ex = -2 * (np.cos(k)[:, None] + np.cos(k)[None, :])
    fT = lambda e: 0.5 * (1 - np.tanh(e / (2 * T)))
    chi00 = np.mean(fT(ex) * (1 - fT(ex)) / T)
    with np.errstate(divide='ignore', invalid='ignore'):
        chiQ = np.mean(np.where(np.abs(ex) > 1e-12, (fT(ex) - fT(-ex)) / (-2 * ex), fT(ex) * (1 - fT(ex)) / T))
    ok = near(chi00, 0.264, 5e-4) and near(1 / chi00, 3.79, 5e-3) and near(chiQ, 0.677, 5e-4) and near(1 / chiQ, 1.48, 5e-3)
    check('the Stoner criterion of Section 9.5b', ok,
          'the half-filled square lattice at T=0.1 on 240 x 240 has chi_0(0,0) = %.4f, so U = %.3f, and chi_0(pi,pi) = %.4f, '
          'so U = %.3f' % (chi00, 1 / chi00, chiQ, 1 / chiQ))

    # ---------------- the Hubbard dimer and the Heisenberg model
    from dmrgpy import fermionchain, spinchain
    out = []
    for u in (4.0, 8.0, 16.0):
        ES = u / 2 - np.sqrt(u * u / 4 + 4)
        ref = np.sort([ES, 0, 0, 0, u, u / 2 + np.sqrt(u * u / 4 + 4)])
        fc = fermionchain.Spinful_Fermionic_Chain(2)
        hh = -(fc.Cdagup[0] * fc.Cup[1] + fc.Cdagup[1] * fc.Cup[0] + fc.Cdagdn[0] * fc.Cdn[1] + fc.Cdagdn[1] * fc.Cdn[0])
        hh = hh + u * (fc.Nup[0] * fc.Ndn[0] + fc.Nup[1] * fc.Ndn[1])
        Nt = fc.Nup[0] + fc.Nup[1] + fc.Ndn[0] + fc.Ndn[1]
        fc.set_hamiltonian(hh + 20.0 * (Nt - 2) * (Nt - 2))
        ld = np.sort(np.real(fc.get_excited(n=6, mode='ED')))
        out.append((-ES / (4 / u), np.abs(hubbard_levels(2, 1.0, u, 2) - ref).max(),
                    np.abs(hubbard_levels(2, -1.0, u, 2) - ref).max(), np.abs(ld - ref).max()))
    ud = cdim[0].T @ cdim[3].T @ vac4; du = cdim[1].T @ cdim[2].T @ vac4
    D0, D1 = cdim[0].T @ cdim[1].T @ vac4, cdim[2].T @ cdim[3].T @ vac4
    Sst, Dst, trip = (ud - du) / np.sqrt(2), (D0 + D1) / np.sqrt(2), (ud + du) / np.sqrt(2)
    mel, mel_t = Dst @ Ht @ Sst, np.abs(Ht @ trip).max()
    ok = all(a < 1e-10 and b < 1e-10 and c < 1e-6 for r, a, b, c in out)
    ok = ok and np.allclose([o[0] for o in out], [0.8284, 0.9443, 0.9848], atol=5e-5) and near(mel, -2, 1e-12) and mel_t < 1e-12
    check('the Hubbard dimer', ok,
          '(E_T - E_S)/(4t^2/U) = %s at U/t = 4, 8, 16, the six levels of numpy for t and -t and of dmrgpy agree with the closed '
          'form to %.0e, <D|H_t|S> = %+.0f t, and H_t gives %.0e on the triplet'
          % (', '.join('%.4f' % o[0] for o in out), max(max(o[1:]) for o in out), mel, mel_t))

    Sd = [p / 2 for p in PAULI]
    ed = np.linalg.eigvalsh(sum(np.kron(s, s) for s in Sd))
    scd = spinchain.Spin_Chain(["S=1/2"] * 2)
    scd.set_hamiltonian(scd.Sx[0] * scd.Sx[1] + scd.Sy[0] * scd.Sy[1] + scd.Sz[0] * scd.Sz[1])
    edm = np.sort(np.real(scd.get_excited(n=4, mode='ED')))
    pauli = np.linalg.eigvalsh(sum(np.kron(p, p) for p in PAULI) / 4)
    check('the Heisenberg convention', np.allclose(ed, [-0.75, 0.25, 0.25, 0.25]) and np.allclose(edm, ed, atol=1e-6)
          and np.allclose(pauli, ed),
          'J S_0.S_1 with S = sigma/2 and J=1 has %s, dmrgpy the same, and (J/4) sigma.sigma too' % ' '.join('%+.2f' % x for x in ed))

    sc = spinchain.Spin_Chain(["S=1/2"] * 4)
    hh = 0
    for i in range(3):
        hh = hh + sc.Sx[i] * sc.Sx[i + 1] + sc.Sy[i] * sc.Sy[i + 1] + sc.Sz[i] * sc.Sz[i + 1]
    sc.set_hamiltonian(hh)
    eh = np.sort(np.real(sc.get_excited(n=16, mode='ED')))
    eh = eh - eh[0]
    Hn = sum(sum(np.kron(np.kron(np.eye(2 ** i), np.kron(s, s)), np.eye(2 ** (2 - i))) for s in Sd) for i in range(3))
    en4 = np.linalg.eigvalsh(Hn)
    devs = []
    for u in (10.0, 30.0):
        e = hubbard_levels(4, 1.0, u, 4)
        exc = (e[:16] - e[0]) / (4 / u)
        devs.append(np.max(np.abs(exc[1:] - eh[1:]) / eh[1:]))
    levels = np.unique(np.round(eh, 4))
    ok = np.allclose(levels[1:], [0.659, 1.366, 1.732, 2.073, 2.366], atol=5e-4) and np.allclose(np.sort(en4 - en4[0]), eh, atol=1e-8)
    ok = ok and near(devs[0], 0.047, 5e-4) and near(devs[1], 0.0055, 5e-5)
    check('the open chain of four sites', ok,
          'Heisenberg levels %s J in dmrgpy and numpy, and the Hubbard levels differ by at most %.1f%% at U=10 and %.2f%% at U=30'
          % (' '.join('%.3f' % x for x in levels[1:]), 100 * devs[0], 100 * devs[1]))

    # ---------------- classical spins and the noncollinear mean field
    rng = np.random.default_rng(3)
    best = np.inf
    for trial in range(20):
        r = minimize(lambda x: sum(np.dot(*[np.array([np.sin(x[2 * a]) * np.cos(x[2 * a + 1]), np.sin(x[2 * a]) * np.sin(x[2 * a + 1]),
                                                     np.cos(x[2 * a])]) for a in (i, j)]) for i, j in ((0, 1), (1, 2), (0, 2))),
                     rng.uniform(0, 2 * np.pi, 6), method='BFGS')
        best = min(best, r.fun)
    coll = min(sum(s[i] * s[j] for i, j in ((0, 1), (1, 2), (0, 2))) for s in
               [(a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1)])
    check('three classical spins on a triangle', near(best, -1.5, 1e-8) and coll == -1,
          'J>0 and S=1, the minimum over all directions is %.6f J, -1/2 per bond, and the best collinear state %.0f J' % (best, coll))

    dm = [(J, D) + classical_chain(J, D) for J, D in ((1.0, 0.0), (1.0, 1.0), (1.0, 5.0), (2.0, 2.0))]
    degs = [np.degrees(np.arccos(c)) for J, D, e, c, z in dm]
    ok = all(near(c, -J / np.hypot(J, D), 1e-4) and near(e, -np.hypot(J, D), 1e-6) for J, D, e, c, z in dm)
    ok = ok and all(near(a, x, 0.05) for a, x in zip(degs, (180.0, 135.0, 101.3, 135.0))) and all(z < 0 for J, D, e, c, z in dm[1:])
    ok = ok and near(dm[1][4], -0.707, 5e-4)
    check('the classical chain with J and D along z', ok,
          ', '.join('J=%.0f, D=%.0f gives %.1f degrees' % (J, D, a) for (J, D, e, c, z), a in zip(dm, degs))
          + ', the energy per bond is -sqrt(J^2+D^2), and z.(S_i x S_(i+1)) = %.3f at D=J' % dm[1][4])

    gr = geometry.chain(); gr = gr.get_supercell(10); gr.dimensionality = 0
    hr = gr.get_hamiltonian(); hr.add_rashba(1.0)
    H0 = np.array(hr.intra.todense() if hasattr(hr.intra, 'todense') else hr.intra)
    bond = H0[0:2, 2:4]
    R = np.zeros((20, 20), complex)
    for j in range(10):
        R[2 * j:2 * j + 2, 2 * j:2 * j + 2] = np.cos(j * np.pi / 4) * np.eye(2) - 1j * np.sin(j * np.pi / 4) * PAULI[1]
    plain = np.zeros((20, 20))
    for j in range(9):
        plain[2 * j, 2 * j + 2] = plain[2 * j + 1, 2 * j + 3] = plain[2 * j + 2, 2 * j] = plain[2 * j + 3, 2 * j + 1] = 1.0
    gauge = np.abs(R.conj().T @ H0 @ R - np.sqrt(2) * plain).max()
    rot = np.sqrt(2) * (np.cos(np.pi / 4) * np.eye(2) + 1j * np.sin(np.pi / 4) * PAULI[1])
    rng = np.random.default_rng(5)
    ours = [hartree_fock(H0, 10.0, 10, rng) for s in range(3)]
    ref = hartree_fock(np.sqrt(2) * plain.astype(complex), 10.0, 10, rng)
    ang_ours = [angles(M).mean() for E, M, err in ours]
    runs = []
    for seed in (0, 1, 2, 3):
        np.random.seed(seed)
        hm, Em = hr.get_mean_field_hamiltonian(U=10.0, mf='XY', mix=0.9, maxite=4000, return_total_energy=True)
        M = moments(hm)
        ny2 = (M[:, 1] / np.linalg.norm(M, axis=1)) ** 2
        cos = np.cos(np.radians(angles(M)))
        runs.append((Em, angles(M).mean(), np.abs(cos + ny2[:-1]).max()))
    np.random.seed(0)
    try:
        hr.get_mean_field_hamiltonian(U=10.0, mf='XY', mix=0.9)
        raised = False
    except MeanFieldConvergenceError:
        raised = True
    Eref = ref[0]
    ok = np.allclose(bond, rot, atol=1e-12) and gauge < 1e-12 and near(Eref, -3.535751, 1e-6)
    ok = ok and all(near(E, Eref, 1e-7) for E, M, err in ours) and np.ptp(ang_ours) > 10 and angles(ref[1]).min() > 179.9
    ok = ok and all(near(E, Eref, 1e-5) and 95 < a < 127 and c < 0.02 for E, a, c in runs) and np.ptp([r[1] for r in runs]) > 20
    ok = ok and raised
    check('the Rashba chain of the notebook', ok,
          'the bond is sqrt2 exp(i pi sigma_y/4), the rotation of 90 degrees per site gives the plain chain with hopping sqrt2 '
          'to %.0e, our Hartree-Fock gives %.6f for three seeds with %s degrees and for the plain chain with 180 degrees, '
          'pyqula with maxite=4000 gives %s with %s degrees and cos = -n_y^2 to %.3f, and seed 0 raises with the default maxite'
          % (gauge, Eref, ' '.join('%.1f' % a for a in ang_ours), ' '.join('%.6f' % r[0] for r in runs),
             ' '.join('%.1f' % r[1] for r in runs), max(r[2] for r in runs)))

    gt = geometry.triangular_lattice(); gt = gt.get_supercell((3, 3))
    tri = []
    for seed in (1, 2):
        np.random.seed(seed)
        ht, Et = gt.get_hamiltonian().get_mean_field_hamiltonian(U=10.0, mf='XY', mix=0.9, maxite=4000, return_total_energy=True)
        M = moments(ht)
        A = [np.array(gt.a1), np.array(gt.a2)]
        angs = [np.degrees(np.arccos(np.clip(M[i] @ M[j] / np.linalg.norm(M[i]) / np.linalg.norm(M[j]), -1, 1)))
                for i in range(len(gt.r)) for j in range(i + 1, len(gt.r)) for n1 in (-1, 0, 1) for n2 in (-1, 0, 1)
                if abs(np.linalg.norm(gt.r[j] + n1 * A[0] + n2 * A[1] - gt.r[i]) - 1) < 1e-6]
        tri.append((Et, min(angs), max(angs), np.linalg.norm(M, axis=1).mean(), len(angs)))
    ok = all(abs(a - 120) < 0.2 and abs(b - 120) < 0.2 and c == 27 and near(mm, 0.922, 5e-4) for E, a, b, mm, c in tri)
    ok = ok and all(near(t[0], -3.8085, 1e-4) for t in tri)
    check('the triangular lattice in mean field', ok,
          'supercell 3x3 at U=10, mf="XY", two seeds, the 27 bonds have %.2f to %.2f degrees, |m| = %.4f, energy %.4f per cell'
          % (min(t[1] for t in tri), max(t[2] for t in tri), tri[0][3], tri[0][0]))

    # ---------------- Holstein-Primakoff and the magnons
    worst = 0.0
    for S in (0.5, 1.0, 1.5, 2.0):
        d = int(round(2 * S + 1))
        a = np.diag(np.sqrt(np.arange(1, d)), 1)
        nb = a.T @ a
        root = np.diag(np.sqrt(2 * S - np.arange(d)))
        Szb, Spl, Smi = S * np.eye(d) - nb, root @ a, a.T @ root
        P, Mi, Z = spin_matrices(S)
        worst = max(worst, np.abs(Szb @ Spl - Spl @ Szb - Spl).max(), np.abs(Spl @ Smi - Smi @ Spl - 2 * Szb).max(),
                    np.abs(Spl - P).max(), np.abs(Szb - Z).max())
    check('the Holstein-Primakoff transformation (6.6)', worst < 1e-12,
          'on the boson states n = 0 to 2S, S = 1/2 to 2, the algebra and the spin matrices hold to %.0e, and S^- adds a boson' % worst)

    errs, bonds = [], []
    for N, S in ((10, 0.5), (8, 1.0)):
        H, mzr = heisenberg_ring(N, S, -1.0)
        E0r = H.diagonal()[np.argmax(mzr)]
        idx = np.where(np.abs(mzr - (N * S - 1)) < 1e-9)[0]
        d = int(round(2 * S + 1))
        where = [[int(x) for x in np.base_repr(b, d).zfill(N)].index(1) for b in idx]
        Hs = H[idx][:, idx].toarray() - E0r * np.eye(len(idx))
        for qn in range(N):
            kq = 2 * np.pi * qn / N
            psi = np.exp(1j * kq * np.array(where)) / np.sqrt(N)
            errs.append(np.abs(Hs @ psi - 2 * S * (1 - np.cos(kq)) * psi).max())
        i0, i1 = where.index(0), where.index(1)
        bonds.append((Hs[i1, i0].real, Hs[i0, i0].real))
    terms = []
    for xx in range(4):
        for yy in range(4):
            i = 4 * xx + yy
            for j in (4 * ((xx + 1) % 4) + yy, 4 * xx + (yy + 1) % 4):
                terms += [(-1.0, [(c, i), (c, j)]) for c in 'xyz']
    Msq, leak = one_flip(16, terms)
    rs = np.array([(xx, yy) for xx in range(4) for yy in range(4)])
    pw = {}
    for name, kv in (('G', (0, 0)), ('X', (np.pi, 0)), ('M', (np.pi, np.pi))):
        psi = np.exp(1j * rs @ np.array(kv)) / 4
        pw[name] = (np.vdot(psi, Msq @ psi).real, np.abs(Msq @ psi - np.vdot(psi, Msq @ psi) * psi).max())
    small = [abs(2 * 0.5 * (1 - np.cos(1e-3)) / (0.5 * 1e-6) - 1), abs(4 * 0.5 * (1 - (np.cos(1e-3) + 1) / 2) / (0.5 * 1e-6) - 1)]
    ok = max(errs) < 1e-10 and leak == 0 and np.allclose(bonds, [(-0.5, 1.0), (-1.0, 2.0)], atol=1e-12)
    ok = ok and all(r < 1e-12 for e, r in pw.values()) and np.allclose([pw[nm][0] for nm in 'GXM'], [0, 2, 4]) and max(small) < 1e-6
    check('the ferromagnetic magnon (6.8)', ok,
          'one magnon on rings of 10 spins 1/2 and 8 spins 1 is 2|J|S(1-cos k) to %.0e, it hops with %+.1f and %+.1f and has '
          'the onsite energy %.1f and %.1f, the 4x4 torus with |J|S = 1/2 gives %.0f, %.0f, %.0f at Gamma, X, M, and the '
          'chain and the square lattice are |J|S k^2 at small k' % (max(errs), bonds[0][0], bonds[1][0], bonds[0][1], bonds[1][1],
                                                                     pw['G'][0], pw['X'][0], pw['M'][0]))

    def bogo(gam, lam=1.0):
        w, v = np.linalg.eig(np.diag([1.0, -1.0]) @ np.array([[1.0, lam * gam], [lam * gam, 1.0]]))
        i = np.argmax(w.real)
        vec = v[:, i] / np.sqrt(abs(v[0, i] ** 2 - v[1, i] ** 2))
        return w.real[i], abs(vec[1]) ** 2
    ks = np.linspace(-np.pi, np.pi, 41)[np.abs(np.sin(np.linspace(-np.pi, np.pi, 41))) > 1e-6]
    eb = max(abs(bogo(np.cos(kq))[0] - abs(np.sin(kq))) for kq in ks)
    evv = max(abs(bogo(np.cos(kq))[1] - 0.5 * (1 / abs(np.sin(kq)) - 1)) for kq in ks)
    hmag = gb.get_hamiltonian().get_mean_field_hamiltonian(U=20.0, mf='antiferro', nk=20)
    tdhf = [(Q, np.sort(np.real(hmag.get_magnon_energies(Q=[Q, 0, 0], nk=20)))) for Q in (0.0, 0.1, 0.25, 0.4)]
    ok = eb < 1e-12 and evv < 1e-12 and near(bogo(0.3, 0.0)[0], 1, 1e-12) and bogo(0.0)[1] < 1e-12
    ok = ok and near(bogo(np.cos(0.3))[1], 1.192, 5e-4)
    ok = ok and all(near(e[0], 0.2 * abs(np.sin(np.pi * Q)), 2e-4) for Q, e in tdhf)
    ok = ok and all(near(e[0], x, 5e-5) for (Q, e), x in zip(tdhf[1:], (0.0618, 0.1414, 0.1902)))
    ok = ok and all(18 < e[1] < 21 for Q, e in tdhf)
    check('the antiferromagnetic magnon (6.9)', ok,
          'the Bogoliubov diagonalization gives JSz|sin k| and v^2 = (1/|sin k| - 1)/2 to %.0e, v^2 = %.4f at k=0.3 and %.0e at '
          'pi/2, JSz without the anomalous terms, and get_magnon_energies at U=20 gives %s at k = 0, 0.1, 0.25, 0.4 pi, the '
          'next at %.1f' % (max(eb, evv), bogo(np.cos(0.3))[1], bogo(0.0)[1], ' '.join('%.4f' % e[0] for Q, e in tdhf), tdhf[1][1][1]))

    red = {}
    for nq in (2000,):
        qq = 2 * np.pi * (np.arange(nq) + 0.5) / nq
        gam = 0.5 * (np.cos(qq)[:, None] + np.cos(qq)[None, :])
        red['square'] = np.mean(0.5 * (1 / np.sqrt(1 - gam ** 2) - 1))
    for nq in (100, 1000, 10000):
        qq = 2 * np.pi * (np.arange(nq) + 0.5) / nq
        red[nq] = np.mean(0.5 * (1 / np.abs(np.sin(qq)) - 1))
    N = 12
    H, mzr = heisenberg_ring(N, 0.5, 1.0)
    dimN = 2 ** N
    perm = np.array([((b << 1) | (b >> (N - 1))) & (dimN - 1) for b in range(dimN)])
    Tr = sp.csr_matrix((np.ones(dimN), (perm, np.arange(dimN))), shape=(dimN, dimN))
    al = 1e-3 * np.exp(0.3j)
    lowest = {}
    for szs in (0, 1):
        idx = np.where(np.abs(mzr - szs) < 1e-9)[0]
        Ts = Tr[idx][:, idx].toarray()
        e, v = np.linalg.eigh(H[idx][:, idx].toarray() + al * Ts + np.conj(al) * Ts.T)
        tk = np.einsum('ij,ij->j', v.conj(), Ts @ v)
        e = e - 2 * np.real(al * tk)
        kidx = np.mod(np.round(np.angle(tk) / (2 * np.pi) * N), N)
        for kq in (0, 3):
            lowest[(szs, kq)] = e[kidx == kq].min()
    gapq = lowest[(1, 3)] - lowest[(0, 0)]
    ok = 0.195 < red['square'] < 0.197 and near(0.5 - red['square'], 0.30, 5e-3)
    ok = ok and all(near(red[nq], x, 5e-3) for nq, x in ((100, 1.23), (1000, 1.96), (10000, 2.69))) and near(gapq, 1.727, 5e-4)
    check('the limits of linear spin waves', ok,
          'the moment of a sublattice is reduced by %.4f on the square lattice, <S^z> = %.3f, and on the chain by %.3f, %.3f, %.3f '
          'with 100, 1000, 10000 k-points; the ring of 12 spins 1/2 has its lowest triplet at k=pi/2 at %.4f J, where (6.9) '
          'gives 1 and the exact chain pi/2' % (red['square'], 0.5 - red['square'], red[100], red[1000], red[10000], gapq))

    aniso = []
    for S in (0.5, 1.0, 1.5):
        lev = np.diag(-(spin_matrices(S)[2] @ spin_matrices(S)[2]))     # S^z = S, S-1, ..., so lev[1] has one magnon
        aniso.append((S, lev[1] - lev[0], 2 * S))
    ok = all(near(g, 2 * S - 1, 1e-12) for S, g, l in aniso) and np.allclose(np.diag(spin_matrices(0.5)[2] ** 2), 0.25)
    check('an easy axis -A (S^z)^2', ok,
          'one magnon on a site costs %s, so A(2S-1), against 2AS of linear spin waves, and (S^z)^2 = 1/4 for S=1/2'
          % ', '.join('%.0fA for S=%.1f' % (g, S) for S, g, l in aniso))

    # ---------------- topological magnons
    hk_ex, leakh = honeycomb_magnon_exact()
    kq = np.array([0.37, -1.21])
    same_b = np.abs(hk_ex(kq) - hd.hk(kq, 0.5, -0.1) - 1.5 * np.eye(2)).max()
    same_a = np.abs(hd.hk(kq, 0.5, 0.1, -np.pi / 2) - hd.hk(kq, 0.5, -0.1)).max()
    other = np.abs(hk_ex(kq) - hd.hk(kq, 0.5, 0.1) - 1.5 * np.eye(2)).max()
    check('the magnon Hamiltonian of the honeycomb ferromagnet', leakh == 0 and same_b < 1e-12 and same_a < 1e-12 and near(other, 0.07, 5e-3),
          'the one-magnon matrix of a 3x3 torus with S=1/2, J=-1, D=0.2 has no weight outside the one-magnon states and is '
          '3|J|S + _haldane.hk(t=|J|S, t2=-DS) to %.0e, which is t2=DS, phi=-pi/2 to %.0e, while t2=+DS misses by %.3f'
          % (same_b, same_a, other))

    B = pc.reciprocal([hd.a1, hd.a2])
    cplus = pc.chern_links(lambda k: hd.hk(k, 1.0, 0.1), B, 0, nk=24)
    cdm = [pc.chern_links(lambda k, b=b: 3 * np.eye(2) + hd.hk(k, 1.0, -0.1), B, b, nk=24) for b in (0, 1)]
    cdm_neg = pc.chern_links(lambda k: 3 * np.eye(2) + hd.hk(k, 1.0, 0.1), B, 0, nk=24)
    kubo = pc.chern_kubo(lambda k: hd.hk(k, 1.0, 0.1), B, 0, nk=48)
    K = np.array([4 * np.pi / 3, 0.0])
    gK = np.diff(np.linalg.eigvalsh(hd.hk(K, 1.0, -0.1)))[0]
    gfull = pc.gap(lambda k: hd.hk(k, 1.0, -0.1), B, 1, nk=60)
    e_gamma = np.linalg.eigvalsh(3 * np.eye(2) + hd.hk(np.zeros(2), 1.0, -0.1))[0]
    ccw = [amp for i, j, dd, amp in hd.hops(1.0, 0.1, np.pi / 2) if i == 0 and j == 0 and dd == (0, 1)][0]
    centre = hd.a2 - (hd.a1 + hd.a2) / 3
    turn = np.cross(-centre, hd.a2 - centre)
    vel = []
    for s in (1, -1):
        e, v = np.linalg.eigh(hd.ribbon(2.6, 24, 1.0, s * 0.1))
        e2 = np.linalg.eigh(hd.ribbon(2.6 + 1e-4, 24, 1.0, s * 0.1))[0]
        low = (np.abs(v) ** 2)[:10].sum(axis=0)
        j = [j for j in range(48) if abs(e[j]) < 0.4 and low[j] > 0.8]
        vel.append(np.sign((e2[j[0]] - e[j[0]]) / 1e-4) if j else 0)

    def hk_momentum(k, t2):       # the hops of _haldane with exp(-i k.d) for <R+d,i|H|R,j>, k the momentum of the state
        h = np.zeros((2, 2), complex)
        for i, j, (dn, dm), amp in hd.hops(1.0, t2, np.pi / 2):
            h[i, j] += amp * np.exp(-1j * (k @ (dn * hd.a1 + dm * hd.a2)))
        return h
    ksamp = np.random.default_rng(7).uniform(-3, 3, (4, 2))
    reversed_k = max(np.abs(hd.hk(k, 1.0, 0.1) - hk_momentum(-k, 0.1)).max() for k in ksamp)
    c_mom = pc.chern_links(lambda k: hk_momentum(k, 0.1), B, 0, nk=24)
    e, v = np.linalg.eigh(hd.ribbon(-2.6, 24, 1.0, 0.1))            # the momentum 2.6, and 2.6 + 1e-4 below
    e2 = np.linalg.eigh(hd.ribbon(-2.6 - 1e-4, 24, 1.0, 0.1))[0]
    w = np.abs(v) ** 2
    edge = lambda rows: [np.sign(e2[j] - e[j]) for j in range(48) if abs(e[j]) < 0.4 and w[rows, j].sum() > 0.8]
    vel_mom = (edge(slice(0, 10)), edge(slice(38, 48)))
    gz = geometry.honeycomb_zigzag_ribbon(20)
    hz = gz.get_hamiltonian(has_spin=False); hz.add_haldane(0.1)
    yz = np.array(gz.r)[:, 1]
    genz = hz.get_hk_gen()
    dense = lambda m: np.asarray(m.todense() if hasattr(m, 'todense') else m)
    top = []
    for kz in (0.45, 0.48, 0.55):   # not 0.5, where the states of the two edges are degenerate and eigh mixes them
        ez, vz = np.linalg.eigh(dense(genz([kz, 0, 0]))); ez2 = np.linalg.eigh(dense(genz([kz + 1e-5, 0, 0])))[0]
        yy = (np.abs(vz) ** 2).T @ yz
        top += [np.sign(ez2[j] - ez[j]) for j in range(len(ez)) if abs(ez[j]) < 0.2 and yy[j] > 0.6 * yz.max()]
    ok = near(cplus, 1, 1e-9) and near(kubo, 1, 1e-3) and near(cdm[0], -1, 1e-9) and near(cdm[1], 1, 1e-9) and near(cdm_neg, 1, 1e-9)
    ok = ok and near(gK, 6 * np.sqrt(3) * 0.1, 1e-12) and near(gK, 1.0392, 5e-5) and near(gfull, gK, 1e-9) and abs(e_gamma) < 1e-12
    ok = ok and near(np.angle(ccw), -np.pi / 2, 1e-12) and turn > 0 and vel == [1, -1]
    ok = ok and reversed_k < 1e-12 and near(c_mom, 1, 1e-9) and vel_mom == ([-1], [1]) and len(top) == 3 and set(top) == {1}
    check('the Chern numbers of the magnon bands', ok,
          '_haldane.hk with t2=+0.1 has C = %+.0f (Kubo %+.4f), so D>0 gives %+.0f and %+.0f to the two bands and D<0 gives %+.0f, '
          'the gap at K is %.4f, the full gap, the lower band is %.0e at Gamma, the counterclockwise hop on A of _haldane.hops '
          'with t2=+0.1 has the phase %.4f, and the lower edge of a ribbon of 24 cells has the slope %+.0f for t2=+0.1 and %+.0f for -0.1; '
          '_haldane.hk(k) is the Bloch matrix of the momentum -k to %.0e, with C = %+.0f, the momentum gives the slopes %s at '
          'the lower and %s at the upper edge for t2=+0.1, and the pyqula zigzag ribbon of 20 with add_haldane(0.1) has %s at '
          'the edge of positive y'
          % (cplus, kubo, cdm[0], cdm[1], cdm_neg, gK, e_gamma, np.angle(ccw), vel[0], vel[1], reversed_k, c_mom,
             [int(x) for x in vel_mom[0]], [int(x) for x in vel_mom[1]], [int(x) for x in top]))

    gh = geometry.honeycomb_lattice()
    nbk = []
    for xh in (0.1, -0.1):
        h = gh.get_hamiltonian(tij=[1.0, 0.2])
        h.add_haldane(xh)
        before = h.get_chern()
        h.set_filling(0.0); h.add_onsite(0.5)
        after = h.get_chern()
        hk, Bh = pc.from_pyqula(h)
        emin = min(np.linalg.eigvalsh(hk(kv))[0] for kv in pc.kmesh(Bh, 30))
        hs = gh.get_hamiltonian(has_spin=False, tij=[1.0, 0.2])
        hs.add_haldane(xh)
        hk1, B1 = pc.from_pyqula(hs)
        nbk.append((xh, before, after, emin, pc.chern_links(hk1, B1, 0, nk=24), pc.gap(hk1, B1, 1, nk=60)))
    hpure = gh.get_hamiltonian(has_spin=False)
    hpure.add_haldane(0.1)
    t2p = max(abs(tt.m[0, 0]) for tt in hpure.get_multicell().hopping)    # the second-neighbor hopping alone
    ok = all(abs(a) < 1e-9 and near(e, 0.499, 1e-3) and near(c, np.sign(xh), 1e-9) and near(g, 0.900, 5e-4) for xh, b, a, e, c, g in nbk)
    ok = ok and near(nbk[0][1], 1.019, 1e-3) and near(nbk[1][1], -1.019, 1e-3) and near(t2p, 0.0866, 5e-5) and near(6 * np.sqrt(3) * 0.1, 1.039, 5e-4)
    check('add_haldane and the magnon cell of the notebook', ok,
          'add_haldane(0.1) is t2 = %.4f; in the cell get_chern() gives %+.4f and %+.4f before set_filling(0.0) and %.1f and %.1f '
          'after it, the bands start at %.3f, and the spinless lower band has C = %+.0f and %+.0f with the gap %.3f'
          % (t2p, nbk[0][1], nbk[1][1], nbk[0][2], nbk[1][2], nbk[0][3], nbk[0][4], nbk[1][4], nbk[0][5]))

    # ---------------- statements of the pages that these numbers contradict
    check('Section 6.6, the rise of the moment', interior == 0 and near(U_x, 1.926, 5e-4) and ms[1] > 0 and ms[1] < ms[2],
          'the chain jumps from 0 to 0.2 at U = %.3f for n=0.2, with no interior minimum at any filling, while the semicircle '
          'rises continuously' % U_x)
    gap_at4 = 0.0 - (-4 / np.pi + 1.0)
    e_low = lambda U: min(-4 / np.pi + U / 4, 0.0)       # the lowest uniform state, paramagnet or saturated ferromagnet
    mgrid = np.linspace(0, 1, 2001)                      # the uniform energy E(m) per site of the half-filled chain
    m_low = lambda U: float(mgrid[np.argmin(-4 / np.pi * np.cos(np.pi * mgrid / 2) + U / 4 * (1 - mgrid ** 2))])
    slopes = [(e_low(cross - 1e-4) - e_low(cross - 2e-4)) / 1e-4, (e_low(cross + 2e-4) - e_low(cross + 1e-4)) / 1e-4]
    kink = np.allclose(slopes, [0.25, 0.0], atol=1e-9) and abs(e_low(cross + 1e-9) - e_low(cross - 1e-9)) < 1e-9
    check('Section 6.5 and the caption of mf_chain', near(gap_at4, 0.27, 5e-3) and near(cross, 5.09, 5e-3) and kink
          and (m_low(cross - 1e-6), m_low(cross + 1e-6)) == (0.0, 1.0),
          'at U=4 the saturated state is %.3f per site above the paramagnet, and the two cross at %.3f, where the lowest '
          'uniform energy has the slopes %.2f and %.2f and no jump, while m goes from %.0f to %.0f'
          % (gap_at4, cross, slopes[0], slopes[1], m_low(cross - 1e-6), m_low(cross + 1e-6)))
    check('Section 6.3, m and U>0', near(sol[1.0][1], 0.030, 5e-4) and near(U_x, 1.93, 5e-3) and near(ev(Sx, xs), 0.5 * 1, 1e-12),
          'm = %.3f at U=1 for the antiferromagnet, the uniform moment at n=0.2 needs U = %.2f, and <S> is half of m' % (sol[1.0][1], U_x))
    check('Section 6.4, the filling', near(fm[0][1], 0.2, 1e-4) and near(fm[1][2], 1.6, 1e-3),
          'filling=0.1 is n=0.2 with |m| = %.3f, and filling=0.2 has the splitting %.3f at U=4' % (fm[0][1], fm[1][2]))
    check('Section 6.8, the dimer cell', dim[0][1] < 1e-3 and near(dim[5][1], np.sqrt(0.75), 2e-3)
          and np.allclose([o[0] for o in out], [0.83, 0.94, 0.98], atol=5e-3),
          'the cell has m = %.4f at 1.8 and %.4f at 4, the exact ratios are %s' % (dim[0][1], dim[5][1], ' '.join('%.2f' % o[0] for o in out)))
    check('Section 6.12, the Rashba chain', gauge < 1e-12 and np.ptp(ang_ours) > 10 and raised
          and 95 < min(r[1] for r in runs) and max(r[1] for r in runs) < 127,
          'the coupling is removed by a rotation per site, the angle follows the seed, %.1f to %.1f degrees in four runs of pyqula'
          % (min(r[1] for r in runs), max(r[1] for r in runs)))
    check('Section 6.16, the Chern number of the cell', all(abs(r[2]) < 1e-9 for r in nbk),
          'h.get_chern() of the cell gives %.1f and %.1f for add_haldane(0.1) and add_haldane(-0.1)' % (nbk[0][2], nbk[1][2]))
    check('Section 6.16, no Bogoliubov form', leakh == 0, 'the ferromagnetic magnon matrix has no weight outside the one-magnon states')
    check('Section 6.17, the easy axis', near(aniso[0][1], 0, 1e-12) and near(aniso[1][1], 1, 1e-12),
          'the gap is %.0fA for S=1/2 and %.0fA for S=1' % (aniso[0][1], aniso[1][1]))
    check('the caption of afm_bogoliubov', bogo(0.0)[1] < 1e-12 and near(bogo(np.cos(0.3))[1], 1.19, 5e-3),
          'v_k^2 = %.0e at k = pi/2 and %.3f at k = 0.3' % (bogo(0.0)[1], bogo(np.cos(0.3))[1]))
    print('%d checks hold, %.1f s' % (COUNT[0], time.time() - t0))


if __name__ == '__main__':
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            main()
        finally:
            os.chdir(cwd)
