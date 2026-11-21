"""Checks of webnotes/conventions/session09.md, with numbers. Every bullet of the sheet is one check here, in the
order of the sheet, also the bullets of its last section, the statements of the old text that the numbers
contradict, which assert again the numbers that they quote. It prints one line per check and exits 0 when all hold.

Not asserted, since they are not a short calculation here: the critical disorder W_c of about 8t of the figure
mobility, the correlation length of about 6 sites of the spin-1 Heisenberg chain and the logarithmic correction of
the spin-1/2 chain, which the sheet gives as values of numerical work, and the SVG of spinon_impurity.py that is not
the same twice. One statement of the notebook is read from its code and not computed: the cell "The impact of a
strong impurity" compares three systems.
The figure scripts of webnotes/figures/session09 are not imported, since they write their SVG when they run, and the
few lines that a check needs are written again here.

Run it from anywhere:  python3 webnotes/checks/session09/conventions.py"""
import os, sys, tempfile, time
sys.dont_write_bytecode = True
import numpy as np
from scipy.integrate import quad
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq
from scipy.special import ellipk

WEBNOTES = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(WEBNOTES, 'figures'))
import physcheck as pc

COUNT = [0]
SHEET = os.path.join(WEBNOTES, 'conventions', 'session09.md')
SHEET_LINES = sum(1 for line in open(SHEET, encoding='utf-8') if line.startswith('- '))    # one check per bullet


def check(name, ok, detail):
    """Prints one line for a check and stops the script when it does not hold."""
    print(('ok    ' if ok else 'FAIL  ') + name + ': ' + detail, flush=True)
    assert ok, name
    COUNT[0] += 1


def fermi(e, T):
    """The Fermi function at the temperature T, with the energy measured from the chemical potential."""
    return 0.5 * (1 - np.tanh(np.asarray(e) / (2 * T)))


def dense(m):
    """A pyqula matrix as a dense numpy array."""
    return np.asarray(m.todense() if hasattr(m, 'todense') else m)


def lindhard_chain(Q, mu, T, nk=20000):
    """chi_0(q) of (9.4) for the spinless chain eps(k) = -2 cos k - mu on a midpoint mesh of nk momenta, positive, per
    spin and per site. A pair with equal energies gives -n_F', its limit."""
    k = 2 * np.pi * (np.arange(nk) + 0.5) / nk
    e1, e2 = -2 * np.cos(k) - mu, -2 * np.cos(k + Q) - mu
    d = e2 - e1
    small = np.abs(d) < 1e-10
    f1, f2 = fermi(e1, T), fermi(e2, T)
    return float(np.mean(np.where(small, f1 * (1 - f1) / T, (f1 - f2) / np.where(small, 1.0, d))))


def lindhard_pyqula_mesh(q, nk, T, eta=0.0, w=0.0, mu=0.0):
    """(9.5) of the spinless chain 2 cos k + mu, pyqula's sign of the hopping, on the mesh k = 2 pi j/nk of pyqula,
    q in units of 2 pi. A pair with equal energies gives -n_F' at w=0."""
    k = 2 * np.pi * np.arange(nk) / nk
    e1, e2 = 2 * np.cos(k) + mu, 2 * np.cos(k + 2 * np.pi * q) + mu
    f1, f2 = fermi(e1, T), fermi(e2, T)
    d = e2 - e1
    same = np.abs(d) < 1e-12
    lim = f1 * (1 - f1) / T if w == 0 else 0.0
    return complex(np.mean(np.where(same, lim, (f1 - f2) / np.where(same, 1.0, d - w - 1j * eta))))


def ring(N, mu, T, onsite):
    """The density of a spinless ring of N sites with hopping -1, onsite energies, chemical potential mu, at T."""
    H = np.diag(onsite).astype(float)
    i = np.arange(N)
    H[i, (i + 1) % N] = H[(i + 1) % N, i] = -1.0
    e, w = np.linalg.eigh(H)
    return (np.abs(w) ** 2) @ fermi(e - mu, T)


def hartree_ring(N, mu, T, U, vup, vdn, ite=60):
    """The self-consistent Hartree densities of the Hubbard ring (1.7) with onsite energies vup and vdn for the two
    spins, relative to the ring without them, at the fixed chemical potential mu."""
    n0 = ring(N, mu, T, np.zeros(N))
    nu, nd = n0.copy(), n0.copy()
    for i in range(ite):
        nu, nd = ring(N, mu, T, U * (nd - n0) + vup), ring(N, mu, T, U * (nu - n0) + vdn)
    return nu - n0, nd - n0


def square_chis(T, nk):
    """chi_0 of (9.4) at q=0 and at Q=(pi,pi) for the half-filled square lattice, on an nk x nk mesh."""
    k = 2 * np.pi * np.arange(nk) / nk
    KX, KY = np.meshgrid(k, k, indexing='ij')
    e = -2 * (np.cos(KX) + np.cos(KY))
    f = fermi(e, T)
    small = np.abs(e) < 1e-12
    cQ = np.mean(np.where(small, 1 / (4 * T), np.tanh(e / (2 * T)) / (2 * np.where(small, 1.0, e))))
    return float(np.mean(f * (1 - f) / T)), float(cQ)


def square_dos_chis(T):
    """chi_0 at q=0 and at (pi,pi) of the half-filled square lattice from the elliptic density of states per spin."""
    dos = lambda E: ellipk(1 - E ** 2 / 16) / (2 * np.pi ** 2)
    g = 2 * quad(lambda E: dos(E) / (4 * T * np.cosh(E / (2 * T)) ** 2), 0, 4, points=[T, 10 * T], limit=400)[0]
    m = 2 * quad(lambda E: dos(E) * np.tanh(E / (2 * T)) / (2 * E), 0, 4, points=[T, 10 * T], limit=400)[0]
    return g, m


def square_hf(L, T, U, stag, m0, ite):
    """The moment of the real-space Hartree-Fock loop of the half-filled Hubbard model on a periodic L x L square
    lattice, started from the moment m0, staggered or uniform. Returns the moment of the last two iterations."""
    x, y = np.meshgrid(np.arange(L), np.arange(L), indexing='ij')
    i = (x * L + y).ravel()
    H = np.zeros((L * L, L * L))
    for dx, dy in ((1, 0), (0, 1)):
        j = (((x + dx) % L) * L + (y + dy) % L).ravel()
        H[i, j] = H[j, i] = -1.0
    s = ((-1.0) ** (x + y) if stag else np.ones_like(x, dtype=float)).ravel()
    m, last = m0, m0
    for it in range(ite):
        dens = []
        for sg in (1, -1):
            e, w = np.linalg.eigh(H + np.diag(U * (0.5 - sg * s * m / 2)))
            dens.append((w ** 2) @ fermi(e - U / 2, T))
        last, m = m, float(np.mean((dens[0] - dens[1]) * s))
    return m, last


def lindhard_3d_closed(q, w):
    """Re chi_0 of (9.5) for the 3D electron gas with the two spins, hbar = m = kF = 1, in units of N(0)."""
    z, u = q / 2, w / q
    lg = lambda a: np.log(np.abs((a + 1) / (a - 1)))
    return 0.5 + ((1 - (z - u) ** 2) * lg(z - u) + (1 - (z + u) ** 2) * lg(z + u)) / (8 * z)


def lindhard_3d_sum(q, w, nk=1200, nc=1200):
    """The same from the integral over the Fermi sea of (9.5), valid above the continuum, in units of N(0)."""
    kk = (np.arange(nk) + 0.5) / nk
    cc = -1 + 2 * (np.arange(nc) + 0.5) / nc
    K, C = np.meshgrid(kk, cc, indexing='ij')
    a = 1 / (K * q * C + q * q / 2 - w) + 1 / (-K * q * C + q * q / 2 + w)
    return 2 * np.sum(a * K ** 2) * (1 / nk) * (2 / nc) / (2 * np.pi) ** 2 * np.pi ** 2


def lattice_eps(d, L):
    k = 2 * np.pi * np.arange(L) / L
    return -2 * sum(np.cos(x) for x in np.meshgrid(*([k] * d), indexing='ij'))


def on_axis(a, d):
    return a[(slice(None),) + (0,) * (d - 1)]


def density_response(d, L, mu, T, wmax=20.0):
    """chi_0(r) of (9.4) in real space along an axis, -T sum_n G(r, i w_n)^2, so delta n(r) = -v0 chi_0(r)."""
    e = lattice_eps(d, L) - mu
    out, n = np.zeros(L), 0
    while (2 * n + 1) * np.pi * T < wmax:
        G = on_axis(np.fft.ifftn(1 / (1j * (2 * n + 1) * np.pi * T - e)), d)
        out += -2 * T * np.real(G ** 2)
        n += 1
    return out


def ldos_response(d, L, mu, eta):
    """The change of the LDOS at the energy mu along an axis, to first order, -(1/pi) Im G(r, mu + i eta)^2."""
    e = lattice_eps(d, L) - mu
    return -np.imag(on_axis(np.fft.ifftn(1 / (1j * eta - e)), d) ** 2) / np.pi


def power(f, kF, r0, r1, damp=None):
    """The power p of the best fit of f(r) by r^-p (A cos 2kF r + B sin 2kF r) on the integers from r0 to r1."""
    r = np.arange(r0, r1 + 1).astype(float)
    y = f[r0:r1 + 1]
    best = (None, np.inf)
    for p in np.arange(0.0, 4.005, 0.01):
        A = np.stack([np.cos(2 * kF * r), np.sin(2 * kF * r)], 1) * r[:, None] ** (-p)
        if damp is not None:
            A = A * damp(r)[:, None]
        c = np.linalg.lstsq(A, y, rcond=None)[0]
        err = np.sum((A @ c - y) ** 2) / np.sum(y ** 2)
        if err < best[1]:
            best = (round(float(p), 2), err)
    return best[0]


def zeta(z):
    """The root with |zeta| < 1 of zeta^2 + z zeta + 1 = 0, so the chain with hopping -1 has
    G0(n, z) = zeta^|n|/(zeta - 1/zeta)."""
    s = np.sqrt(z * z - 4 + 0j)
    a, b = (-z + s) / 2, (-z - s) / 2
    return a if abs(a) < 1 else b


def g0_chain(n, z):
    x = zeta(z)
    return x ** abs(n) / (x - 1 / x)


def ysr_det(J, mu, D, nk=20000):
    """The in-gap energies of a classical spin J sigma_z on one site of the chain 2 cos k + mu with s-wave D, from
    det(1 - J g(E)) = 0 in the block (c_up, c_dn^dag) of (5.6), g the local Green's function of the clean chain."""
    k = 2 * np.pi * (np.arange(nk) + 0.5) / nk
    e = 2 * np.cos(k) + mu

    def det(E):
        den = E ** 2 - e ** 2 - D ** 2
        g0, gz, gx = np.mean(E / den), np.mean(e / den), np.mean(D / den)
        return np.linalg.det(np.eye(2) - J * np.array([[g0 + gz, gx], [gx, g0 - gz]]))
    Es = np.linspace(-D * 0.9999, D * 0.9999, 401)
    vals = np.array([det(E) for E in Es])
    return [brentq(det, Es[i], Es[i + 1]) for i in range(len(Es) - 1) if vals[i] * vals[i + 1] < 0]


def ysr_formula(J, mu, D):
    """(9.10) with alpha = pi nu0 J S, J S the exchange energy of the site, nu0 = D(E_F) per spin of the chain."""
    a = J / np.sqrt(4 - mu ** 2)
    return D * (1 - a * a) / (1 + a * a)


def bdg_block(N, D, J=0.0, V=0.0):
    """The block (c_up, c_dn^dag) of (5.6) for a half-filled ring of N sites with hopping -1, s-wave D, an exchange
    J sigma_z and a potential V on site 0. The exchange enters both halves with +J and the potential with +V and -V."""
    h = np.zeros((N, N))
    i = np.arange(N)
    h[i, (i + 1) % N] = h[(i + 1) % N, i] = -1.0
    P = np.zeros((N, N)); P[0, 0] = 1.0
    return np.block([[h + (J + V) * P, D * np.eye(N)], [D * np.eye(N), -h + (J - V) * P]])


def honeycomb_torus(L, t2, M, phi=np.pi / 2):
    """A Haldane model of our own on a torus of L x L cells, as in the figure vacancy_dos, with first-neighbor hopping
    -1, second-neighbor t2 exp(+-i phi) and the mass +M on A and -M on B. Returns H and the index function."""
    idx = lambda x, y, s: 2 * ((x % L) * L + (y % L)) + s
    H = np.zeros((2 * L * L, 2 * L * L), dtype=complex)
    for x in range(L):
        for y in range(L):
            b = idx(x, y, 1)
            for dx, dy in ((0, 0), (1, 0), (0, 1)):
                H[idx(x + dx, y + dy, 0), b] -= 1.0
                H[b, idx(x + dx, y + dy, 0)] -= 1.0
            H[idx(x, y, 0), idx(x, y, 0)] += M
            H[b, b] -= M
            for dx, dy in ((1, 0), (-1, 1), (0, -1)):
                for s, sg in ((0, 1), (1, -1)):
                    i, j = idx(x, y, s), idx(x + dx, y + dy, s)
                    H[i, j] += t2 * np.exp(1j * sg * phi)
                    H[j, i] += t2 * np.exp(-1j * sg * phi)
    return H, idx


def torus_vacancy(L, t2, M, sub, phi=np.pi / 2):
    """The gap edges of the clean torus and the in-gap levels with the vacancy on sublattice sub (0 is A, with +M),
    each with its weight on the three neighbors of the vacancy."""
    H, idx = honeycomb_torus(L, t2, M, phi)
    e0 = np.linalg.eigvalsh(H)
    lo, hi = e0[e0 < 0].max(), e0[e0 > 0].min()
    v = idx(L // 2, L // 2, sub)
    nbr = [n for n in range(2 * L * L) if n != v and abs(H[v, n]) > 0.5]
    keep = [i for i in range(2 * L * L) if i != v]
    e, w = np.linalg.eigh(H[np.ix_(keep, keep)])
    sel = [keep.index(n) for n in nbr]
    return lo, hi, [(float(x), float((np.abs(w[sel, j]) ** 2).sum())) for j, x in enumerate(e) if lo + 1e-3 < x < hi - 1e-3]


D1 = np.array([[1, 0], [-0.5, np.sqrt(3) / 2], [-0.5, -np.sqrt(3) / 2]])      # A to B, bond length 1
NNN = np.array([D1[1] - D1[2], D1[2] - D1[0], D1[0] - D1[1]])                  # second neighbors, one turn
BH = 2 * np.pi * np.linalg.inv(np.array([D1[0] - D1[1], D1[0] - D1[2]])).T


def haldane_blocks(u1, u2, t2, M, phi):
    """h_AA, h_BB and h_AB of the Haldane model with the mass +M on A, at the reduced momenta u1, u2."""
    kx, ky = u1 * BH[0, 0] + u2 * BH[1, 0], u1 * BH[0, 1] + u2 * BH[1, 1]
    f = -sum(np.exp(1j * (kx * d[0] + ky * d[1])) for d in D1)
    haa = M + 2 * t2 * sum(np.cos(kx * v[0] + ky * v[1] + phi) for v in NNN)
    hbb = -M + 2 * t2 * sum(np.cos(kx * v[0] + ky * v[1] - phi) for v in NNN)
    return haa, hbb, f


def haldane_g(E, t2, M, phi=np.pi / 2, nk=1200, sub=0, chunk=300):
    """G_AA(E) (sub=0) or G_BB(E) (sub=1) of the infinite Haldane model at a real E inside the gap, on an nk x nk
    midpoint mesh. A vacancy on that sublattice binds a state where it vanishes."""
    u = (np.arange(nk) + 0.5) / nk
    tot = 0.0
    for s in range(0, nk, chunk):
        U1, U2 = np.meshgrid(u[s:s + chunk], u, indexing='ij')
        haa, hbb, f = haldane_blocks(U1, U2, t2, M, phi)
        tot += np.sum(((E - hbb) if sub == 0 else (E - haa)) / ((E - haa) * (E - hbb) - np.abs(f) ** 2))
    return float(tot / nk ** 2)


def haldane_edges(t2, M, phi=np.pi / 2, nk=300):
    """The edges of the gap at half filling, on a mesh that holds the two valleys."""
    u = np.arange(nk) / nk
    U1, U2 = np.meshgrid(u, u, indexing='ij')
    haa, hbb, f = haldane_blocks(U1, U2, t2, M, phi)
    avg, dif = (haa + hbb) / 2, np.sqrt(((haa - hbb) / 2) ** 2 + np.abs(f) ** 2)
    return float((avg - dif).max()), float((avg + dif).min())


def spinon_figure(chi2, N=2000, h=0.1, driver='auto'):
    """The moment <S^z_n> of the figure spinon_impurity, an open chain of N sites with hoppings -1 and -chi2 in turn,
    half filling for each spin and -h S^z on the central site, whose bond to the right is the strong one."""
    hop = np.array([1.0 if i % 2 == 0 else chi2 for i in range(N - 1)])
    c, m = N // 2, np.zeros(N)
    for sg in (1, -1):
        d = np.zeros(N); d[c] = -sg * h / 2
        e, w = eigh_tridiagonal(d, -hop, lapack_driver=driver)
        m += sg * (np.abs(w[:, :N // 2]) ** 2).sum(axis=1) / 2
    return m[c - 40:c + 41]


def spinon_dyson(chi2, h=0.1, nmax=40, nk=4096, nw=200):
    """The same moment in the infinite dimerized chain, exact in h, from the Dyson equation of a one-site field on
    the imaginary axis, delta n_n = (1/pi) int_0^inf dw Re[G_n0(iw)^2 V/(1 - V G_00(iw))], with no subtraction of two
    densities. G is a sum over the Bloch momenta of the cells (2j, 2j+1), joined inside by the bond 1."""
    k = 2 * np.pi * (np.arange(nk) + 0.5) / nk
    off = -(1.0 + chi2 * np.exp(-1j * k))
    n = np.arange(-nmax, nmax + 1)
    cell, sub = np.divmod(n, 2)
    ph = np.exp(1j * np.outer(cell, k))
    x, wq = np.polynomial.legendre.leggauss(nw)
    t = 0.5 * (x + 1)
    m = np.zeros(len(n))
    for ti, qi in zip(t, wq):
        w, jac = ti / (1 - ti), 0.5 / (1 - ti) ** 2
        z = 1j * w
        det = z * z - np.abs(off) ** 2
        G = np.where(sub[:, None] == 0, ph * (z / det), ph * (np.conj(off) / det)).mean(axis=1)
        g00 = G[nmax]
        for sg in (1, -1):
            V = -sg * h / 2
            m += sg * qi * jac * np.real(G ** 2 * V / (1 - V * g00)) / np.pi / 2
    return m


def spinon_uniform(n, h=0.1):
    """The moment of the infinite uniform spinon chain at distance n, from the same Dyson equation, with the closed
    form of the Green's function of the chain."""
    def dn(v0):
        f = lambda w: (g0_chain(n, 1j * w) ** 2 * v0 / (1 - v0 * g0_chain(0, 1j * w))).real
        return (quad(f, 0, 50, limit=2000, epsabs=1e-14)[0] + quad(f, 50, np.inf, limit=200)[0]) / np.pi
    return (dn(-h / 2) - dn(h / 2)) / 2


def lyapunov(W, L, seed, E=0.0):
    """The localization length xi = 1/gamma of the random chain with w_n uniform in [-W, W] at the energy E, from the
    transfer matrix, so that |psi| ~ e^{-x/xi}."""
    rng = np.random.default_rng(seed)
    w = W * (2 * rng.random(L) - 1)
    p0, p1, ly = 1.0, 0.3, 0.0
    for n in range(L):
        p0, p1 = (w[n] - E) * p0 - p1, p0
        if n % 50 == 49:
            s = np.hypot(p0, p1)
            ly += np.log(s); p0 /= s; p1 /= s
    return L / ly


def log_transmission(W, L, rng):
    """ln T of a random segment of L sites between two clean leads at E=0, T = 4 |G_1L|^2 with the self-energy -i."""
    d = -(W * (2 * rng.random(L) - 1)).astype(complex)
    d[0] += 1j; d[-1] += 1j
    D1_, D0, logdet = d[0], 1.0, 0.0
    for n in range(1, L):
        D1_, D0 = d[n] * D1_ - D0, D1_
        s = abs(D1_)
        logdet += np.log(s); D1_ /= s; D0 /= s
    return float(np.log(4.0) - 2 * (logdet + np.log(abs(D1_))))


def aah_nipr(N, V0, phi=0.3):
    """N times the mean IPR (9.12) of the Aubry-Andre ring of the figure aah_ipr, q = F_{k-1}/F_k."""
    q = {55: 34, 233: 144, 987: 610}[N] / N
    H = np.diag(V0 * np.cos(2 * np.pi * q * np.arange(N) + phi))
    i = np.arange(N)
    H[i, (i + 1) % N] = H[(i + 1) % N, i] = -1.0
    return float(N * (np.abs(np.linalg.eigh(H)[1]) ** 4).sum(axis=0).mean())


def main():
    """Runs every check. The pyqula calls write files, so the caller runs this in a temporary folder."""
    from pyqula import geometry, embedding, potentials, tails
    t0 = time.time()
    R = {}

    # The definitions shared with Sessions 5 and 6
    T = 0.005
    k = 2 * np.pi * (np.arange(200000) + 0.5) / 200000
    D = float(np.mean(fermi(-2 * np.cos(k), T) * (1 - fermi(-2 * np.cos(k), T)) / T))
    g = geometry.chain()
    d1 = g.get_hamiltonian(has_spin=False).get_dos(energies=np.array([0.0]), delta=0.02, nk=4000)[1][0]
    d2 = g.get_hamiltonian().get_dos(energies=np.array([0.0]), delta=0.02, nk=4000)[1][0]
    cu = np.kron(np.array([[0, 1], [0, 0]]), np.eye(2)); cd = np.kron(np.diag([1, -1]), np.array([[0, 1], [0, 0]]))
    nu, nd = cu.T @ cu, cd.T @ cd
    ident = np.allclose(nu @ nd, ((nu + nd) @ (nu + nd) - (nu - nd) @ (nu - nd)) / 4) and np.allclose(cu @ cd + cd @ cu, 0)
    check('D(E_F) per spin and per site, and the Hubbard term', abs(D - 1 / (2 * np.pi)) < 1e-4 and abs(d1 - D) < 2e-4
          and abs(d2 - 2 * D) < 4e-4 and ident,
          'half-filled chain, -sum n_F\'/N = %.4f = 1/(2 pi t), h.get_dos() gives %.4f with has_spin=False and %.4f with the '
          'two spins; n_up n_dn = (n^2 - m^2)/4 on the four states of one site' % (D, d1, d2))
    h = g.get_hamiltonian()
    h.add_exchange([0.0, 0.0, 0.3]); h.add_swave(0.1)
    m = dense(h.intra)
    hop = dense([x.m for x in h.get_multicell().hopping if tuple(x.dir) == (1, 0, 0)][0])
    nambu = np.array([[0.3, 0, 0.1, 0], [0, -0.3, 0, 0.1], [0.1, 0, 0.3, 0], [0, 0.1, 0, -0.3]])
    hs_ = g.get_hamiltonian(); hs_.add_swave(0.3)
    gap_s = hs_.get_gap()
    check('the Nambu basis of pyqula is (5.6)', np.allclose(m, nambu) and np.allclose(hop, np.diag([1, 1, -1, -1]))
          and abs(gap_s - 0.6) < 1e-6,
          'add_exchange([0,0,0.3]) and add_swave(0.1) give the onsite diagonal %s and 0.1 at (0,2) and (1,3), the hopping +1 '
          'is -1 in the hole block, and add_swave(0.3) has h.get_gap() = %.3f = 2 Delta' % (np.round(np.diag(m).real, 2).tolist(), gap_s))

    # The classical magnet and perturbation theory
    def chi_mf(T, sgn, J=1.0, hf=1e-6):
        mA = mB = 0.0
        for it in range(4000):
            mA, mB = np.tanh((hf + sgn * J * mB) / T), np.tanh((hf + sgn * J * mA) / T)
        return (mA + mB) / 2 / hf
    rows = [(T, 1 / chi_mf(T, 1, 0.0), 1 / chi_mf(T, 1), 1 / chi_mf(T, -1)) for T in (1.5, 3.0)]
    ok = all(abs(p - T) < 1e-4 and abs(f - (T - 1)) < 1e-4 and abs(a - (T + 1)) < 1e-4 for T, p, f, a in rows)
    check('(9.1) in mean field, zJ = T_c = 1', ok and (60 + 30) == 90,
          ', '.join('T=%.1f gives 1/chi = %.4f, %.4f and %.4f for the paramagnet, the ferromagnet and the antiferromagnet' % r
                    for r in rows) + ', and the quiz line T+30 gives 90 at 60 K')
    En, Em, V = 0.0, np.array([0.35, 1.2, -0.8, -2.0]), 1e-4
    H = np.diag(np.concatenate([[En], Em])) + V * (np.ones((5, 5)) - np.eye(5))
    vec = np.linalg.eigh(H)[1]
    vec = vec[:, np.argmax(np.abs(vec[0]))]
    vec = vec * np.sign(vec[0])
    check('the sign of (9.3)', np.allclose(vec[1:] / V, 1 / (En - Em), rtol=1e-3),
          'levels %s around E_n=0 with <m|V|n> = %.0e, the exact eigenvector has %s times V, and 1/(E_n - E_m) is %s'
          % (Em.tolist(), V, np.round(vec[1:] / V, 3).tolist(), np.round(1 / (En - Em), 3).tolist()))

    # The sign of the response
    N, mu, T, v = 400, -1.0, 0.05, 1e-4
    x = np.arange(N)
    n0 = ring(N, mu, T, np.zeros(N))
    out = []
    for j in (10, 40, 120):
        Q = 2 * np.pi * j / N
        dn = ring(N, mu, T, v * np.cos(Q * x)) - n0
        out.append((Q, 2 * np.mean(dn * np.cos(Q * x)) / v, lindhard_chain(Q, mu, T, nk=N)))
    R['dn_q'] = out
    check('delta n(q) = -chi_0(q) v(q) for an onsite energy v', all(abs(a + c) < 2e-3 * c and c > 0 for Q, a, c in out),
          'ring of %d sites, mu=%.0f, T=%.2f, potential v cos(qx): ' % (N, mu, T)
          + ', '.join('q=%.3f gives dn/v %+.4f and chi_0 %.4f' % o for o in out))
    dn = ring(N, mu, T, v * (x == 0)) - n0
    chiq = np.array([lindhard_chain(Q, mu, T, nk=N) for Q in 2 * np.pi * np.arange(N) / N])
    born = -np.real(np.fft.ifft(chiq))
    err = np.abs(dn / v - born).max()
    R['dn0'] = dn[0] / v
    check('one impurity, delta n(x) = -v0 int dq/2pi e^{iqx} chi_0(q)', err < 1e-5 and dn[0] < 0 and abs(dn[0] / v + 0.250) < 5e-4,
          'v0=+%.0e on one site of the same ring, delta n(0)/v0 = %+.4f, and the Fourier sum with the minus sign agrees to %.0e'
          % (v, dn[0] / v, err))
    hs = g.get_hamiltonian(has_spin=False)
    worst, rows = 0.0, []
    for q in (0.1, 0.3):
        e, c = hs.get_chi(energies=np.array([0.0, 0.5, 1.0]), q=[q, 0, 0], nk=600, delta=0.05, T=0.05)
        page = np.array([lindhard_pyqula_mesh(q, 600, 0.05, 0.05, w) for w in (0.0, 0.5, 1.0)])
        worst = max(worst, np.abs(np.array(c) + np.conj(page)).max())
        rows.append((q, page[1].real, page[1].imag, c[1].real, c[1].imag))
    e, c1 = hs.get_chi(energies=np.array([0.0]), q=[0.1, 0, 0], nk=600, delta=0.05, T=0.05)
    e, c2 = g.get_hamiltonian().get_chi(energies=np.array([0.0]), q=[0.1, 0, 0], nk=600, delta=0.05, T=0.05)
    e, c3 = hs.get_chi(energies=np.array([0.0, 0.5]), q=[0.1, 0, 0], nk=600, delta=0.05)
    e, c4 = hs.get_chi(energies=np.array([0.0, 0.5]), q=[0.1, 0, 0], nk=600, delta=0.05, T=0.05)
    ok = worst < 1e-6 and all(r[2] > 0 and r[4] > 0 for r in rows) and abs(c2[0] - 2 * c1[0]) < 1e-9 and c1[0].real < 0
    ok = ok and np.abs(np.array(c3) - np.array(c4)).max() < 1e-12
    check('h.get_chi() is minus the complex conjugate of (9.5)', ok,
          'chain with has_spin=False, T=delta=0.05, nk=600, at omega=0.5: '
          + ', '.join('q=%.1f (9.5) %+.4f%+.4fi, pyqula %+.4f%+.4fi' % r for r in rows)
          + ', largest difference to -conj %.0e; at omega=0 %+.4f with has_spin=False and %+.4f with the two spins; '
          'with no T it is the same as T=delta' % (worst, c1[0].real, c2[0].real))

    # The Lindhard function
    small = lindhard_chain(2 * np.pi / 20000, -1.0, 0.01)
    quarter = lindhard_chain(2 * np.pi / 20000, -np.sqrt(2), 0.005)
    pq0 = -float(hs.get_chi(energies=[0.0], q=[0.01, 0., 0.], nk=400, delta=1e-3, T=0.02)[1][0].real)
    ok = abs(small - 1 / (np.pi * np.sqrt(3))) < 2e-4 and abs(quarter - 1 / (np.pi * np.sqrt(2))) < 2e-4 and abs(pq0 - 1 / (2 * np.pi)) < 1e-3
    check('chi_0(q -> 0) = D(E_F)', ok,
          'chain at mu=-t %.4f and 1/(pi v_F) = %.4f, quarter filling %.4f and %.4f, pyqula at half filling %.4f and 1/(2 pi) = %.4f'
          % (small, 1 / (np.pi * np.sqrt(3)), quarter, 1 / (np.pi * np.sqrt(2)), pq0, 1 / (2 * np.pi)))
    kF = 1.0
    qq = np.array([0.3, 1.0, 1.7, 2.6])
    closed = 1 / (np.pi * qq) * np.log(np.abs((2 * kF + qq) / (2 * kF - qq)))
    kgrid = np.linspace(-kF, kF, 400001)[:-1] + kF / 400000
    num = []
    for q in qq:
        a = 1 / ((kgrid + q) ** 2 / 2 - kgrid ** 2 / 2)
        b = 1 / ((kgrid - q) ** 2 / 2 - kgrid ** 2 / 2)
        num.append(np.sum(a + b) * (2 * kF / 400000) / (2 * np.pi))
    num = np.array(num)
    check('the closed form of the 1D free-electron gas', np.abs(num / closed - 1).max() < 1e-3 and abs(closed[0] * np.pi * kF - 1) < 0.02,
          'spinless, per unit length, m = hbar = kF = 1, against the sum over the Fermi sea at q/kF = %s: %s'
          % (qq.tolist(), ' '.join('%.4f/%.4f' % (a, b) for a, b in zip(num, closed))))
    sl = []
    for mu in (0.0, -np.sqrt(2), -1.0):
        kf = np.arccos(-mu / 2)
        a, b = lindhard_chain(2 * kf, mu, 0.01, nk=400000), lindhard_chain(2 * kf, mu, 0.005, nk=400000)
        sl.append(((b - a) / np.log(2), 1 / (2 * np.pi * np.sin(kf))))
    c02, c01 = lindhard_chain(np.pi, 0.0, 0.02, nk=200000), lindhard_chain(np.pi, 0.0, 0.01, nk=200000)
    pqpi = -float(hs.get_chi(energies=[0.0], q=[0.5, 0., 0.], nk=400, delta=1e-3, T=0.02)[1][0].real)
    ok = abs(sl[0][0] / sl[0][1] - 1) < 1e-3 and all(abs(s / d - 0.5) < 1e-3 for s, d in sl[1:])
    ok = ok and abs(c02 - 0.863) < 1e-3 and abs(c01 - 0.974) < 1e-3 and abs(pqpi - c02) < 2e-3
    R['slopes'] = sl
    check('chi_0(2k_F) grows as ln(1/T)', ok,
          'd chi_0(2kF)/d ln(1/T) between T=0.01 and 0.005 is %.4f at half filling, D(E_F) = %.4f, and %.4f and %.4f at '
          'quarter filling and at mu=-t, where D(E_F)/2 = %.4f and %.4f; chi_0(pi) of the half-filled chain is %.4f at '
          'T=0.02 and %.4f at 0.01, and pyqula gives %.4f at 0.02' % (sl[0][0], sl[0][1], sl[1][0], sl[2][0], sl[1][1] / 2,
                                                                    sl[2][1] / 2, c02, c01, pqpi))
    qs = 2 * np.pi * np.arange(1, 200) / 400
    prof = [lindhard_chain(Q, -np.sqrt(2), 0.01, nk=4000) for Q in qs]
    check('quarter filling', abs(qs[int(np.argmax(prof))] - np.pi / 2) < 1e-9 and abs(-2 * np.cos(np.pi / 4) + np.sqrt(2)) < 1e-12,
          'k_F = pi/4 puts the Fermi level at -sqrt2 t = %.4f, and chi_0(q) at T=0.01 is largest at q = %.4f = pi/2'
          % (-np.sqrt(2), qs[int(np.argmax(prof))]))
    a, b = square_chis(0.1, 120), square_chis(0.1, 240)
    dg, dm = square_dos_chis(0.1)
    c5, d5 = square_chis(0.05, 240), square_dos_chis(0.05)
    ok = abs(a[0] - b[0]) < 1e-6 and abs(a[1] - b[1]) < 1e-6 and abs(b[0] - dg) < 1e-6 and abs(b[1] - dm) < 1e-6
    ok = ok and abs(b[0] - 0.264) < 1e-3 and abs(b[1] - 0.677) < 1e-3 and abs(b[1] / b[0] - 2.57) < 0.005
    ok = ok and abs(c5[0] - 0.299) < 1e-3 and abs(c5[1] - 0.872) < 1e-3 and abs(c5[0] - d5[0]) < 1e-5
    R['sq'] = (b, c5)
    check('chi_0 at Gamma and at M of the half-filled square lattice', ok,
          'T=0.1t: %.4f/t and %.4f/t on k-meshes of 120 and 240, %.4f and %.4f from the elliptic density of states, ratio '
          '%.3f, thresholds %.3ft and %.3ft; T=0.05t: %.4f and %.4f, thresholds %.3ft and %.3ft'
          % (b[0], b[1], dg, dm, b[1] / b[0], 1 / b[1], 1 / b[0], c5[0], c5[1], 1 / c5[1], 1 / c5[0]))
    Ts = [0.2, 0.1, 0.05, 0.025, 0.0125]
    ch = np.array([square_dos_chis(T) for T in Ts])
    st, sd = np.diff(ch[:, 0]), np.diff(ch[:, 1], 2)
    ok = np.all(np.abs(st - np.log(2) / (2 * np.pi ** 2)) < 5e-4) and np.all(np.abs(sd - np.log(2) ** 2 / (2 * np.pi ** 2)) < 5e-4)
    R['ln2'] = (st, sd)
    check('chi_0(0,0) grows as ln(1/T) and chi_0(pi,pi) as ln^2(1/T)', ok,
          'from the elliptic density of states, for each halving of T from 0.2t to 0.0125t chi_0(0,0) grows by %s, and '
          'ln2/(2 pi^2) = %.4f, and chi_0(pi,pi) has the second differences %s, and ln^2 2/(2 pi^2) = %.4f'
          % (np.round(st, 4).tolist(), np.log(2) / (2 * np.pi ** 2), np.round(sd, 4).tolist(), np.log(2) ** 2 / (2 * np.pi ** 2)))
    nk, T = 200, 0.1
    kk = 2 * np.pi * np.arange(nk) / nk
    KX, KY = np.meshgrid(kk, kk, indexing='ij')
    E = -2 * (np.cos(KX) + np.cos(KY))

    def chi_map(mu, i, j):
        f = fermi(E - mu, T)
        Eq = np.roll(np.roll(E, -i, 0), -j, 1); fq = np.roll(np.roll(f, -i, 0), -j, 1)
        de = Eq - E
        sm = np.abs(de) < 1e-9
        return float(np.mean(np.where(sm, f * (1 - f) / T, (f - fq) / np.where(sm, 1.0, de))))
    half = chi_map(0.0, 100, 100) / chi_map(0.0, 0, 0)
    kF = np.sqrt(4 * np.pi * np.mean(E < -3.0))
    prof = [chi_map(-3.0, int(round(s * 2 * kF * nk / (2 * np.pi))), 0) for s in (0.0, 0.5, 0.9, 1.2, 1.5)]
    prof = [p / prof[0] for p in prof]
    ok = abs(half - 2.57) < 0.005 and abs(kF - 1.035) < 0.001 and abs(np.arccos(0.5) - 1.047) < 1e-3
    ok = ok and abs(np.sqrt(2) * np.arccos(0.75) - 1.022) < 1e-3 and max(abs(p - 1) for p in prof[1:3]) < 0.06
    ok = ok and abs(prof[3] - 0.68) < 0.01 and abs(prof[4] - 0.56) < 0.01
    check('the maps of chi_0 over the zone of q, T=0.1t', ok,
          'half filling, chi_0(pi,pi)/chi_0(0) = %.3f on a 200x200 mesh. At mu=-3t, kF = %.3f from the area, %.3f along the '
          'diagonal and %.3f along the axes, and chi_0 at q_x = 0.5, 0.9, 1.2 and 1.5 times 2kF is %.3f, %.3f, %.3f and %.3f '
          'of its value at q=0' % (half, kF, np.sqrt(2) * np.arccos(0.75), np.arccos(0.5), *prof[1:]))
    out = []
    for mu in (0.0, 1.0):
        hc = geometry.chain().get_hamiltonian(has_spin=False)
        hc.add_onsite(mu)
        kp = np.linspace(0, 1, 2401)
        ek = np.asarray(hc.get_bands(kpath=[[xx, 0, 0] for xx in kp])[1])
        cross = kp[1:][np.sign(ek[1:]) != np.sign(ek[:-1])]
        stat = [-float(hc.get_chi(energies=[0.0], q=[q, 0., 0.], nk=300, delta=1e-3, T=0.03)[1][0].real) for q in (0.25, 1 / 3, 0.4, 0.5)]
        out.append((cross, (cross[1] - cross[0]) % 1, stat))
    dos1 = float(np.real(hc.get_dos(energies=[0.0], delta=0.005, nk=20000, write=False)[1][0]))   # hc has mu = 1
    ok = abs(out[0][1] - 0.5) < 2e-3 and abs(out[1][1] - 1 / 3) < 2e-3 and int(np.argmax(out[1][2])) == 1
    ok = ok and abs(dos1 - 0.1838) < 3e-4 and abs(lindhard_chain(1e-4, -1.0, 0.002) - 0.1838) < 3e-4
    check('the try-it of Section 9.4b, add_onsite(mu) raises the band', ok,
          'mu=0: Fermi points %s, vector %.3f; mu=1: Fermi points %s, vector %.3f and its mirror %.3f, in units of 2 pi; '
          'the static pyqula chi_0 at q = 0.25, 1/3, 0.4, 0.5 is %s for mu=1, and get_dos at zero energy is %.4f, the '
          'D(E_F) of mu = -t of the notes' % (np.round(out[0][0], 3).tolist(), out[0][1], np.round(out[1][0], 3).tolist(),
                                             out[1][1], 1 - out[1][1], np.round(out[1][2], 3).tolist(), dos1))

    # The random phase approximation and the Stoner instability
    N, mu, T, U, v = 200, -1.0, 0.1, 1.0, 1e-4
    x = np.arange(N)
    Q = 2 * np.pi * 30 / N
    c0 = lindhard_chain(Q, mu, T, nk=N)
    pot = v * np.cos(Q * x)
    du, dd = hartree_ring(N, mu, T, U, pot, pot)
    charge = 2 * np.mean((du + dd) * np.cos(Q * x)) / v
    du, dd = hartree_ring(N, mu, T, U, -pot, pot)
    spin = 2 * np.mean((du - dd) * np.cos(Q * x)) / v
    ok = abs(charge + 2 * c0 / (1 + U * c0)) < 1e-3 * c0 and abs(spin - 2 * c0 / (1 - U * c0)) < 1e-3 * c0
    R['rpa'] = (charge, spin, c0)
    check('the RPA denominators, 1+U chi_0 for the charge and 1-U chi_0 for the spin', ok,
          'Hubbard ring of %d sites, U=%.0f, mu=%.0f, T=%.1f, q=%.3f, chi_0 per spin %.4f: the self-consistent Hartree '
          'response of the density to an onsite energy is %.4f, -2chi_0/(1+U chi_0) = %.4f, and of n_up-n_down to '
          '-h(n_up-n_down) %.4f, 2chi_0/(1-U chi_0) = %.4f' % (N, U, mu, T, Q, c0, charge, -2 * c0 / (1 + U * c0), spin,
                                                               2 * c0 / (1 - U * c0)))
    hp = g.get_hamiltonian()
    (e, cdn) = hp.get_densitychi_RPA(U=1., energies=np.array([0.]), q=[0.25, 0., 0.], nk=400, delta=1e-2)
    cdn = np.array(cdn).ravel()[0].real
    hmf = hp.get_mean_field_hamiltonian(U=1., nk=200, filling=0.5, mf=hp.copy())
    para = np.abs(np.diag(dense(hmf.intra))[0::2] - np.diag(dense(hmf.intra))[1::2]).max()
    rows = []
    for q in (0.25, 0.5):
        (e, bare) = hmf.get_spinchi_ladder(energies=np.array([0.]), q=[q, 0., 0.], nk=400, imode="mesh", RPA=False, delta=1e-2)
        (e, rpa) = hmf.get_spinchi_ladder(energies=np.array([0.]), q=[q, 0., 0.], nk=400, imode="mesh", RPA=True, delta=1e-2)
        x0 = lindhard_pyqula_mesh(q, 400, 1e-2, 1e-2).real
        xs = -float(hs.get_chi(energies=[0.0], q=[q, 0., 0.], nk=400, delta=1e-2)[1][0].real)
        rows.append((q, x0, -np.trace(bare[0]).real, xs, (np.trace(rpa[0]) / np.trace(bare[0])).real, 1 / (1 - x0)))
    ok = para < 1e-9 and abs(cdn + 2 * rows[0][1] / (1 + rows[0][1])) < 1e-6 and abs(cdn + 0.331) < 1e-3
    ok = ok and all(abs(b - x0) < 1e-6 and abs(s - x0) < 1e-6 and abs(r - f) < 1e-4 * f for q, x0, b, s, r, f in rows)
    ok = ok and abs(rows[0][1] - 0.198) < 1e-3 and abs(rows[1][1] - 0.970) < 1e-3 and abs(rows[1][4] - 33.7) < 0.05
    check('the RPA calls of pyqula', ok,
          'paramagnetic chain, U=1, delta=0.01, chi_0 of (9.4) on the mesh of pyqula %.4f at q=pi/2 and %.4f at q=pi: '
          'get_densitychi_RPA at pi/2 is %.4f = -2chi_0/(1+U chi_0); minus the trace of get_spinchi_ladder with RPA=False '
          'is %.4f and %.4f, and RPA=True multiplies it by %.4f and %.2f, 1/(1-U chi_0) = %.4f and %.2f'
          % (rows[0][1], rows[1][1], cdn, rows[0][2], rows[1][2], rows[0][4], rows[1][4], rows[0][5], rows[1][5]))
    L = 16
    g0, gQ = square_chis(0.1, L)
    rs = square_hf(L, 0.1, 1.0, True, 1e-5, 1)
    ru = square_hf(L, 0.1, 1.0, False, 1e-5, 1)
    b1, b0 = square_hf(L, 0.1, 1.70, True, 0.27, 12)
    kL = 2 * np.pi * np.arange(L) / L
    E2 = (2 * (np.cos(kL)[:, None] + np.cos(kL)[None, :])) ** 2
    Dg = brentq(lambda D: 1.70 * np.mean(np.tanh(np.sqrt(E2 + D * D) / 0.2) / (2 * np.sqrt(E2 + D * D))) - 1, 1e-6, 3)
    ok = abs(rs[0] / rs[1] - gQ) < 1e-3 * gQ and abs(ru[0] / ru[1] - g0) < 1e-3 * g0 and abs(b1 - 2 * Dg / 1.70) < 1e-4
    check('(9.8) from a real-space mean field', ok,
          'Hartree-Fock of (1.7) on a %dx%d torus at T=0.1t with U=t, one step multiplies a small staggered moment by %.4f '
          'and a uniform one by %.4f, which are chi_0(pi,pi) and chi_0(0) on the same mesh, %.4f and %.4f. At U=1.7t the loop '
          'converges to the moment %.4f, which the gap equation gives as %.4f' % (L, L, rs[0] / rs[1], ru[0] / ru[1], gQ, g0, b1, 2 * Dg / 1.70))
    check('the quiz numbers of Sections 9.5a and 9.5b', abs(0.68 / 1.68 - 0.405) < 1e-3 and abs(1 / 1.68 - 0.595) < 1e-3
          and abs(1 / 0.32 - 3.125) < 1e-9 and abs(1.5 * 0.26 - 0.39) < 1e-12,
          'U chi_0 = 0.68 gives chi = %.3f/t, chi/chi_0 = %.3f for the charge and %.3f for the spin, and 1.5 x 0.26 = %.2f'
          % (0.68 / 1.68, 1 / 1.68, 1 / 0.32, 1.5 * 0.26))
    hb = geometry.bichain().get_hamiltonian()
    ib = dense(hb.intra)
    eb = np.linalg.eigvalsh(dense(hb.get_hk_gen()([0.5, 0, 0])))
    spl = []
    for amp in (0.5, 0.2):
        guess = hb.copy(); guess.add_antiferromagnetism(amp)
        hm = hb.get_mean_field_hamiltonian(U=2.0, nk=200, mf=guess, filling=0.5)
        dgl = np.diag(dense(hm.intra)).real
        spl.append(abs(dgl[0] - dgl[1]))
    kk = 2 * np.pi * (np.arange(4000) + 0.5) / 4000
    gapeq = 2 * brentq(lambda D: 2.0 * np.mean(1 / (2 * np.sqrt((2 * np.cos(kk)) ** 2 + D ** 2))) - 1, 1e-6, 5)
    hopb = [np.abs(ib[0, 2]), np.abs(dense([t_.m for t_ in hb.get_multicell().hopping if tuple(t_.dir) == (1, 0, 0)][0])).max()]
    ok = np.allclose(hopb, 1.0) and np.min(np.abs(eb)) < 1e-12 and abs(spl[0] - spl[1]) < 1e-3 and abs(spl[0] - gapeq) < 2e-3
    R['bichain'] = (hopb, spl, gapeq)
    check('geometry.bichain() is not dimerized, and the guess of its loop', ok,
          'both hoppings are %.0f and %.0f, the bands touch at zero energy at k=pi, %s; the loop at U=2t started from '
          'add_antiferromagnetism(0.5) and (0.2) ends at the splittings %.4f and %.4f, and the gap equation gives %.4f'
          % (hopb[0], hopb[1], np.round(eb, 3).tolist(), spl[0], spl[1], gapeq))

    # The plasmon
    n, wp = 1 / (3 * np.pi ** 2), 1.0
    e2 = wp ** 2 / (4 * np.pi * n)
    vq = lambda q: 4 * np.pi * e2 / q ** 2
    s1, s2 = lindhard_3d_closed(0.1, 1.2), lindhard_3d_sum(0.1, 1.2)
    lead = -n * 0.1 ** 2 / 1.2 ** 2 * np.pi ** 2
    coef = []
    for q in (0.02, 0.04):
        root = brentq(lambda w: 1 + vq(q) * lindhard_3d_closed(q, w) / np.pi ** 2, q + q * q / 2 + 1e-3, 5.0)
        coef.append((root ** 2 - wp ** 2) / q ** 2)
    extrap = (4 * coef[0] - coef[1]) / 3
    grid = np.linspace(0.05 + 0.05 ** 2 / 2 + 1e-3, 5, 400)
    neg = np.all(lindhard_3d_closed(0.05, grid) < 0)
    ok = s1 < 0 and abs(s1 - s2) < 1e-4 * abs(s1) and abs(s1 / lead - 1) < 0.01 and abs(extrap - 0.6) < 0.002 and neg
    R['plasmon'] = (s1, neg, extrap)
    check('the plasmon is the zero of 1 + v(q) chi_0', ok,
          'q=0.1kF, omega=1.2 hbar kF^2/m, Re chi_0 = %.6f N(0) from the closed form and %.6f from the sum, -n q^2/(m omega^2) '
          '= %.6f N(0); omega_p = 1, (omega^2 - omega_p^2)/(v_F q)^2 = %.4f at q=0.02kF and %.4f at 0.04kF, %.4f at q -> 0, '
          'and chi_0 < 0 at every omega above the continuum, so 1 - v(q) chi_0 has no zero there' % (s1, s2, lead, coef[0], coef[1], extrap))
    rng = np.random.default_rng(3)
    kv = rng.normal(size=(400000, 3))
    kv *= (rng.random(400000) ** (1 / 3) / np.linalg.norm(kv, axis=1))[:, None]
    out = []
    for q in (0.5, 1.5, 2.5):
        kq = kv + np.array([q, 0, 0])
        empty = np.linalg.norm(kq, axis=1) > 1
        de = (np.sum(kq ** 2, axis=1) - np.sum(kv ** 2, axis=1))[empty] / 2
        out.append((q, de.min(), max(q * q / 2 - q, 0), de.max(), q + q * q / 2))
    check('the edges of the particle-hole continuum', all(abs(a - b) < 0.005 and abs(c - d) < 0.005 for q, a, b, c, d in out),
          'm = kF = vF = 1, sampling the Fermi sphere: ' + ', '.join(
              'q=%.1f from %.3f (edge %.3f) to %.3f (edge %.3f)' % o for o in out))

    # Friedel oscillations
    from scipy.special import j0, j1, y0, y1, sici
    r = np.arange(400).astype(float); r[0] = 1e-9
    kF = np.pi / 3
    xr = 2 * kF * r
    cont = [sici(xr)[0] - np.pi / 2, j0(kF * r) * y0(kF * r) + j1(kF * r) * y1(kF * r), (np.sin(xr) - xr * np.cos(xr)) / xr ** 4]
    pcs = [power(cont[0], kF, 20, 150), power(cont[1], kF, 5, 30), power(cont[2], kF, 5, 30)]
    lat = []
    for d, L, mu, T, rr in ((1, 4096, -1.0, 0.002, (20, 150)), (2, 256, -3.0, 0.005, (5, 30))):
        kx = np.arccos((-mu - 2 * (d - 1)) / 2)
        LT = 2 * np.sin(kx) / (2 * np.pi * T)
        lat.append(power(density_response(d, L, mu, T), kx, *rr, damp=lambda r: (r / LT) / np.sinh(r / LT)))
    ok = abs(pcs[0] - 1) < 0.03 and abs(pcs[1] - 2) < 0.03 and abs(pcs[2] - 3) < 0.05 and abs(lat[0] - 1) < 0.05 and abs(lat[1] - 2) < 0.08
    check('the density decays as 1/r^d', ok,
          'fitted power of r^-p (A cos 2kF r + B sin 2kF r), %.2f, %.2f and %.2f for the continuum forms in d = 1, 2, 3, and '
          '%.2f and %.2f for the first-order density of the chain at mu=-t and of the square lattice at mu=-3t'
          % (pcs[0], pcs[1], pcs[2], lat[0], lat[1]))
    pl = []
    for d, L, mu, eta, rr in ((1, 16384, -1.0, 0.001, (20, 300)), (2, 1024, -3.0, 0.005, (5, 40)), (3, 160, -5.0, 0.03, (5, 30))):
        kx = np.arccos((-mu - 2 * (d - 1)) / 2)
        pl.append(power(ldos_response(d, L, mu, eta), kx, *rr, damp=lambda r: np.exp(-2 * eta * r / (2 * np.sin(kx)))))
    z = -1.0 + 0.01j
    xs2 = np.arange(1, 400)
    ld = np.array([-np.imag(g0_chain(xx, z) ** 2 / (1 - g0_chain(0, z))) / np.pi for xx in xs2])
    pk = np.array([i for i in range(1, len(ld) - 1) if abs(ld[i]) >= abs(ld[i - 1]) and abs(ld[i]) >= abs(ld[i + 1])])
    rate = -np.polyfit(xs2[pk], np.log(np.abs(ld[pk])), 1)[0]
    ok = abs(pl[0]) < 0.05 and abs(pl[1] - 1) < 0.08 and abs(pl[2] - 2) < 0.1 and abs(rate - 0.02 / np.sqrt(3)) < 5e-4
    check('the LDOS at one energy decays as 1/r^(d-1)', ok,
          'fitted power %.2f, %.2f and %.2f for d = 1, 2, 3 at the Fermi energy, with the damping of the broadening divided '
          'out; in the chain at mu=-t with delta=0.01 the LDOS change of an impurity t falls as exp(-%.4f x), and '
          '2 delta/v_F = %.4f' % (pl[0], pl[1], pl[2], rate, 0.02 / np.sqrt(3)))
    N, c = 4001, 2000
    out = []
    for mu in (-1.6, -1.0):
        dns = []
        for v0 in (1.0, 0.0):
            dd = np.zeros(N); dd[c] = v0
            e, w = eigh_tridiagonal(dd, -np.ones(N - 1))
            dns.append((np.abs(w[:, e < mu]) ** 2).sum(axis=1))
        y = np.zeros(400); y[1:] = (dns[0] - dns[1])[c + 1:c + 400]
        kx = np.arccos(-mu / 2)
        out.append((mu, np.pi / kx, power(y, kx, 6, 200), (dns[0] - dns[1])[c]))
    ok = all(abs(p - 1) < 0.05 and d0 < 0 for mu, per, p, d0 in out) and abs(out[0][1] - 4.88) < 0.005 and abs(out[1][1] - 3) < 1e-9
    ok = ok and abs(out[0][3] + 0.147) < 1e-3 and abs(out[1][3] + 0.188) < 1e-3
    check('the figure friedel, one impurity v0=t in a chain of 4001 sites', ok,
          ', '.join('mu=%.1f gives the period pi/kF = %.2f, the power %.2f, and delta n(0) = %+.3f' % o for o in out))
    out = []
    for mu in (1.95, 1.7, 1.0):
        hq = geometry.chain().get_hamiltonian(has_spin=False, tij=[1])
        hq.add_onsite(mu)
        hv = hq.copy(); hv.add_onsite(potentials.impurity(hq.geometry.r[0], v=0.2))
        xs, ys, ds = embedding.Embedding(hq, m=hv).get_ldos(nsuper=101, energy=0., delta=1e-2, nk=400)
        xs, ds = np.array(xs), np.array(ds)
        o = np.argsort(xs); xs, ds = xs[o], ds[o]
        s = xs >= 2
        qs = np.linspace(0.1, np.pi, 6000)
        qb = qs[np.argmax([abs(np.sum((ds[s] - ds[s].mean()) * np.exp(-1j * qq * xs[s]))) for qq in qs])]
        out.append((mu, np.pi / (np.pi - np.arccos(-mu / 2)), 2 * np.pi / qb))
    sq = []
    for mu, ns in ((3.8, 41), (3.0, 31)):
        hq = geometry.square_lattice().get_hamiltonian(has_spin=False)
        hq.add_onsite(mu)
        hv = hq.copy(); hv.add_onsite(potentials.impurity(hq.geometry.r[0], v=10.))
        xs, ys, ds = embedding.Embedding(hq, m=hv).get_ldos(nsuper=ns, energy=0., delta=1e-2, nk=100)
        xs, ys, ds = np.array(xs), np.array(ys), np.array(ds)
        line = (np.abs(ys) < 1e-6) & (xs >= 1)
        xl, dl_ = xs[line], ds[line]
        o = np.argsort(xl); xl, dl_ = xl[o], dl_[o]
        mx = [xl[i] for i in range(1, len(xl) - 1) if dl_[i] > dl_[i - 1] and dl_[i] > dl_[i + 1]]
        sq.append((mu, float(np.mean(np.diff(mx))), np.pi / np.arccos(mu / 2 - 1)))
    ok = all(abs(a - b) / a < 0.03 for mu, a, b in out) and all(abs(a - b) / b < 0.05 for mu, a, b in sq)
    ok = ok and abs(out[0][1] - 14.02) < 0.01 and abs(out[1][1] - 5.66) < 0.01 and abs(out[2][1] - 3) < 1e-9
    check('the try-its of Sections 9.6a and 9.6b, the periods in pyqula', ok,
          ', '.join('chain mu=%.2f: pi/kF from the band bottom %.2f, pyqula LDOS period %.2f' % o for o in out) + ', '
          + ', '.join('square lattice mu=%.1f: LDOS maxima along x every %.2f sites, pi/kF %.2f' % o for o in sq))
    kf2 = np.arccos(3.4 / 2 - 1)
    check('the figure friedel2d and the quiz of Section 9.6a', abs(kf2 - 0.795) < 5e-4 and abs(np.pi / kf2 - 3.95) < 0.005
          and abs(2 * np.pi / (2 * np.pi / 4) - 4) < 1e-12,
          'E=-3.4t on the square lattice has kF = %.4f along the axes and pi/kF = %.2f sites, and kF = pi/4 gives the period 4'
          % (kf2, np.pi / kf2))
    gb = geometry.bichain().get_hamiltonian(has_spin=False, tij=[1])
    rows = []
    for mm in (0.1, 0.3):
        hm = gb.copy(); hm.add_sublattice_imbalance(mm)
        on = np.sort(np.diag(dense(hm.intra)).real)
        e = np.asarray(hm.get_bands(nk=400)[1])
        Nn = 1201; c = Nn // 2
        H = np.diag(mm * (-1.0) ** np.arange(Nn)); i = np.arange(Nn - 1); H[i, i + 1] = H[i + 1, i] = 1.0
        G = np.linalg.solve(1e-9j * np.eye(Nn) - H, np.eye(Nn)[:, c])
        rt = -np.polyfit(np.arange(22, 60, 2), np.log(np.abs(G[c + 22:c + 60:2]) ** 2), 1)[0]
        rows.append((mm, on[0], on[1], e[e > 0].min() - e[e < 0].max(), rt, 2 * np.arcsinh(mm / 2), 1 / rt))
    ok = all(abs(a + m_) < 1e-12 and abs(b - m_) < 1e-12 and abs(gp - 2 * m_) < 2e-3 and abs(rt - ref) < 1e-3
             for m_, a, b, gp, rt, ref, ln in rows)
    ok = ok and abs(rows[0][6] - 10.0) < 0.05 and abs(rows[1][6] - 3.35) < 0.01
    R['insulator'] = rows
    check('the impurity in the insulating chain of the notebook', ok,
          ', '.join('add_sublattice_imbalance(%.1f) gives the onsite energies %+.1f and %+.1f and the gap %.3f, and the LDOS '
                    'change at E=0, |G(0,x;0)|^2, decays at the rate %.4f = 2 asinh(m/2) = %.4f, a length of %.2f sites' % rw
                    for rw in rows))

    # Yu-Shiba-Rusinov states
    rows = []
    for mu, D in ((0.0, 0.02), (0.0, 0.2), (1.8, 0.2)):
        rows.append((mu, D, max(abs(abs(ysr_det(J, mu, D)[0]) - abs(ysr_formula(J, mu, D))) / D for J in (0.5, 1.0, 3.0))))
    first = 1 - 2 * 0.5 ** 2
    e_half = abs(ysr_det(1.0, 0.0, 0.02)[0]) / 0.02
    ok = rows[0][2] < 1e-3 and rows[1][2] < 0.006 and rows[2][2] > 0.1 and abs(e_half - 0.6) < 1e-3 and abs(first - 0.5) < 1e-12
    R['born'] = (first, e_half)
    check('(9.10) holds to all orders in J for a small Delta', ok,
          'largest |E_b - (9.10)| over J S = 0.5, 1, 3, from det(1 - J g(E)) = 0 on the chain: '
          + ', '.join('%.3f Delta at mu=%.1f, Delta=%.2f' % (e, m_, d) for m_, d, e in rows)
          + '; at alpha=0.5 the lattice gives %.4f and the first order 1-2 alpha^2 gives %.2f' % (e_half, first))
    out = []
    for J in (1.0, 3.0):
        hy = geometry.chain().get_supercell(300).get_hamiltonian()
        mm = np.zeros((300, 3)); mm[0, 2] = J
        hy.add_exchange(mm); hy.add_swave(0.1)
        e = np.linalg.eigvalsh(dense(hy.get_hk_gen()([0., 0., 0.])))
        out.append((J, np.sort(np.abs(e))[0] / 0.1, abs(ysr_det(J, 0.0, 0.1)[0]) / 0.1, abs(ysr_formula(J, 0.0, 0.1)) / 0.1))
    ok = all(abs(a - b) < 1e-3 and abs(a - c) < 3e-3 for J, a, b, c in out) and abs(out[0][1] - 0.6005) < 2e-4 and abs(out[1][1] - 0.3837) < 2e-4
    check('the same state in a pyqula supercell', ok,
          'ring of 300 sites, add_exchange with J S on one site, add_swave(0.1), half filling, alpha = J S/2: '
          + ', '.join('J S=%.0f gives |E_b| = %.4f Delta, the T-matrix %.4f, (9.10) %.4f' % o for o in out))
    k = 2 * np.pi * (np.arange(20000) + 0.5) / 20000
    e = 2 * np.cos(k) + 1.8
    gz, gx = np.mean(-e / (e ** 2 + 0.2 ** 2)), np.mean(-0.2 / (e ** 2 + 0.2 ** 2))
    Jc, Jf = 1 / np.hypot(gz, gx), np.sqrt(4 - 1.8 ** 2)
    check('the crossing of the notebook cell', abs(Jc - 1.04) < 0.005 and abs(Jf - 0.872) < 1e-3,
          'chain with add_onsite(1.8) and Delta=0.2, E_b crosses zero at J = %.3f on the lattice, where alpha=1 gives J = '
          '1/(pi nu0) = v_F = %.3f' % (Jc, Jf))
    sz = []
    for J in (1.0, 3.0):
        el = np.linalg.eigvalsh(bdg_block(400, 0.1, J=J))
        sz.append((np.sum(el < 0) - 400) / 2)
    check('the ground state across the crossing', sz[0] == 0 and sz[1] == -0.5,
          'block (c_up, c_dn^dag) of a ring of 400 sites, Delta=0.1, S^z_tot = (negative levels - N)/2 is %+.1f for J S = t '
          'and %+.1f for 3t, on the two sides of the crossing at 2t' % tuple(sz))
    low = [np.min(np.abs(np.linalg.eigvalsh(bdg_block(400, 0.1, V=V)))) / 0.1 for V in (2.0, 10.0)]
    f = lambda a: (1 - a * a) / (1 + a * a)
    ok = all(abs(x_ - 1) < 1e-6 for x_ in low) and abs(f(0.5) - 0.6) < 1e-12 and abs(f(2) + 0.6) < 1e-12 and abs(f(1.2) + 0.18) < 0.001
    check('a non-magnetic impurity leaves the gap', ok,
          'a potential 2t and 10t on one site of the same ring: the lowest |E| is %.7f and %.7f Delta; (9.10) gives %.2f at '
          'alpha=0.5, %.2f at 2 and %.3f at 1.2' % (low[0], low[1], f(0.5), f(2), f(1.2)))

    # Vacancies in topological matter
    lo, hi, ing_c = torus_vacancy(18, 0.15, 0.0, 0)
    lo2, hi2, ing_t = torus_vacancy(18, 0.0, 3 * np.sqrt(3) * 0.15, 0)
    ok = abs(hi - lo - 1.559) < 1e-3 and abs(hi2 - lo2 - 1.559) < 1e-3 and len(ing_c) == 1 and abs(ing_c[0][0]) < 1e-9
    ok = ok and abs(ing_c[0][1] - 0.45) < 0.005 and len(ing_t) == 0
    check('the figure vacancy_dos, a vacancy on an 18x18 torus', ok,
          'Haldane t2=0.15t, gap %.3f, one level in the gap at %+.1e with %.3f of its weight on the three neighbors; mass '
          'M=0.779t, gap %.3f, no level in the gap' % (hi - lo, ing_c[0][0], ing_c[0][1], hi2 - lo2))
    zs = {}
    for M in (0.3, 0.4):
        el, eh = haldane_edges(0.1, M)
        zs[M] = (el, eh, brentq(lambda E: haldane_g(E, 0.1, M, nk=600), el + 1e-4, eh - 1e-4, xtol=1e-7))
    zb = brentq(lambda E: haldane_g(E, 0.1, 0.3, nk=600, sub=1), zs[0.3][0] + 1e-4, zs[0.3][1] - 1e-4, xtol=1e-7)
    zm = brentq(lambda E: haldane_g(E, 0.1, 0.3, phi=-np.pi / 2, nk=600), zs[0.3][0] + 1e-4, zs[0.3][1] - 1e-4, xtol=1e-7)
    t18 = torus_vacancy(18, 0.1, 0.3, 0)[2]
    hh = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False)
    hh.add_haldane(0.2 / np.sqrt(3)); hh.add_sublattice_imbalance(0.3)
    hv = hh.copy(); hv.add_onsite(potentials.impurity(hh.geometry.r[0], v=1e3))
    em, dm_ = embedding.Embedding(hh, m=hv).multidos(es=np.linspace(-0.2, 0.2, 41), delta=0.004, nk=100)
    peak = float(np.array(em)[np.argmax(dm_)])
    ok = abs(zs[0.3][1] - 0.2196) < 1e-4 and abs(zs[0.3][0] + 0.2196) < 1e-4 and abs(zs[0.3][2] + 0.1353) < 5e-4
    ok = ok and abs(zb - 0.1353) < 5e-4 and abs(zm - zs[0.3][2]) < 1e-6 and len(t18) == 1 and abs(t18[0][0] + 0.130) < 1e-3
    ok = ok and abs(peak + 0.14) < 0.006 and abs(zs[0.4][1] - 0.1196) < 1e-4 and abs(zs[0.4][2] + 0.1164) < 5e-4
    R['m03'] = (zs[0.3][2], zb)
    check('the vacancy in the Haldane model at M=0.3t and 0.4t', ok,
          't2=0.1t, M=0.3t: gap edges %+.4f and %+.4f, zero of G_AA of the infinite lattice at %+.4f for the vacancy on A '
          '(onsite +M), of G_BB at %+.4f, and %+.4f with the phase -pi/2; the 18x18 torus gives %+.4f and the pyqula embedding '
          '%+.2f. M=0.4t: edge %.4f, state %+.4f' % (zs[0.3][0], zs[0.3][1], zs[0.3][2], zb, zm, t18[0][0], peak, zs[0.4][1], zs[0.4][2]))
    el, eh = haldane_edges(0.1, 0.5)
    Es = np.array([el + 1e-4, -0.016, 0.0, eh - 1e-4])
    G5 = np.array([haldane_g(E_, 0.1, 0.5, nk=1200) for E_ in Es])
    scan = np.array([haldane_g(E_, 0.1, 0.5, nk=600) for E_ in np.linspace(el + 1e-4, eh - 1e-4, 21)])
    kpt = (BH[0] + 2 * BH[1]) / 3
    best = None
    for kv_ in (kpt, (2 * BH[0] + BH[1]) / 3):
        u1, u2 = np.linalg.solve(BH.T, kv_)
        haa, hbb, ff = haldane_blocks(np.array(u1), np.array(u2), 0.1, 0.5, np.pi / 2)
        ev, vv = np.linalg.eigh(np.array([[haa, ff], [np.conj(ff), hbb]]))
        if best is None or ev[1] - ev[0] < best[0]:
            best = (ev[1] - ev[0], ev[0], abs(vv[0, 0]) ** 2)
    h5 = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False)
    h5.add_haldane(0.2 / np.sqrt(3)); h5.add_sublattice_imbalance(0.5)
    hk5, B5 = pc.from_pyqula(h5)
    c5 = pc.chern_links(hk5, B5, 0, nk=60)
    t5 = torus_vacancy(18, 0.1, 0.5, 0)[2]
    gb5 = haldane_g(-0.016, 0.1, 0.5, nk=1200, sub=1)
    scan_b = np.array([haldane_g(E_, 0.1, 0.5, nk=600, sub=1) for E_ in np.linspace(el + 1e-4, eh - 1e-4, 21)])
    ok = abs(eh - el - 0.0392) < 1e-4 and np.all(scan < -0.15) and np.all(G5 < -0.15) and abs(G5[1] + 0.197) < 0.002
    ok = ok and abs(best[1] - el) < 1e-6 and best[2] > 0.999 and abs(c5 - 1) < 1e-6 and len(t5) == 1 and abs(t5[0][0] + 0.006) < 5e-4
    ok = ok and abs(t5[0][1] - 0.014) < 0.001 and abs(scan.min() + 0.24) < 0.005 and abs(G5[0] + 0.18) < 0.005
    ok = ok and abs(gb5 - 0.236) < 0.002 and np.all(scan_b > 0.15)
    R['m05'] = (G5[1], gb5, t5[0][0])
    check('no vacancy state separated from the band at M=0.5t', ok,
          't2=0.1t, M=0.5t: C = %+.4f from the link variables of add_haldane, gap %.4f, G_AA of the infinite lattice is '
          '%s at E = %s, and between %.3f and %.3f over the gap, with no zero; the top of the valence band at the valley of '
          'the small gap is at %+.4f with %.4f of its weight on A; G_BB is %+.3f at E=-0.016 and between %.3f and %.3f over '
          'the gap; the 18x18 torus has one level at %+.4f with %.3f of its weight on the neighbors'
          % (c5, eh - el, np.round(G5, 3).tolist(), np.round(Es, 4).tolist(), scan.min(), scan.max(), best[1], best[2],
             gb5, scan_b.min(), scan_b.max(), t5[0][0], t5[0][1]))
    out = []
    Ns = 80
    for first in (0.5, 1.0):
        hop_ = np.array([first if i % 2 == 0 else 1.5 - first for i in range(Ns)])
        H = np.zeros((Ns, Ns))
        for i in range(Ns):
            H[i, (i + 1) % Ns] = H[(i + 1) % Ns, i] = hop_[i]
        Hv = H[1:, 1:]
        e, w = np.linalg.eigh(Hv)
        zi = np.argmin(np.abs(e))
        strong = 0 if hop_[0] > hop_[-1] else Ns - 2       # the index of the neighbor joined by the strong bond
        weak = Ns - 2 if strong == 0 else 0
        res = []
        for idx in (strong, weak):
            Hp = Hv.copy(); Hp[idx, idx] += 2.0
            ep = np.linalg.eigvalsh(Hp)
            res.append(ep[np.abs(ep) < 0.5 - 1e-3])
        out.append((abs(e[zi]), w[strong, zi] ** 2, w[weak, zi] ** 2, res))
    ok = all(o[0] < 1e-12 and abs(o[1] - 0.75) < 1e-6 and o[2] < 1e-12 and len(o[3][0]) == 0 and len(o[3][1]) == 2 for o in out)
    ok = ok and abs(np.sort(out[0][3][1])[0] + 0.308) < 1e-3
    R['ssh'] = out
    check('a vacancy in the SSH ring', ok,
          'hoppings 0.5t and t on a ring of 80 sites, for either order the vacancy leaves a level at %.0e with %.3f of its '
          'weight on the neighbor joined by the strong bond and %.0e on the other; 2t on the first leaves no level in the '
          'gap +-0.5t, 2t on the second leaves %s' % (out[0][0], out[0][1], out[0][2], np.round(out[0][3][1], 3).tolist()))
    out = {}
    for mode in ('chiral_pwave', 'swave'):
        hpw = geometry.triangular_lattice().get_hamiltonian()
        hpw.add_onsite(-4.0); hpw.add_pairing(mode=mode, delta=0.1)
        gen = hpw.get_hk_gen()
        nk = 240
        u = np.arange(nk) / nk
        Hs = np.array([dense(gen([a_, b_, 0.])) for a_ in u for b_ in u])
        ev, vv = np.linalg.eigh(Hs)
        edge = float(np.min(np.abs(ev)))
        A = vv.transpose(1, 0, 2).reshape(4, -1)

        def lowest(E):
            G = (A * (1 / (E - ev)).reshape(1, -1)) @ A.conj().T / len(ev)
            return np.linalg.eigvalsh(G)
        grid = edge * np.linspace(-0.995, 0.995, 200)
        vals = np.array([lowest(E_) for E_ in grid])
        roots = []
        for j in range(4):
            for i in np.nonzero(np.diff(np.sign(vals[:, j])))[0]:
                roots.append(brentq(lambda E_: lowest(E_)[j], grid[i], grid[i + 1], xtol=1e-9) / edge)
        out[mode] = (edge, hpw.get_gap() / 2, np.sort(roots))
        if mode == 'chiral_pwave':
            hk_, B_ = pc.from_pyqula(hpw)
            out['chern'] = (pc.chern_links(hk_, B_, bands=range(2), nk=48), hpw.get_chern())
    rp = out['chiral_pwave'][2]
    h22 = geometry.triangular_lattice().get_supercell((2, 2)).get_hamiltonian()      # the cell of the notebook
    h22.add_onsite(-4.0); h22.add_pairing(mode='chiral_pwave', delta=0.1)
    g22 = h22.get_gap()
    ok = abs(out['chiral_pwave'][0] - 0.2996) < 5e-4 and abs(out['chiral_pwave'][1] - 0.2996) < 1e-4
    ok = ok and abs(g22 - 0.5992) < 1e-4 and abs(g22 / 2 - out['chiral_pwave'][1]) < 1e-6
    ok = ok and len(rp) == 4 and np.allclose(np.abs(rp), 0.714, atol=0.002) and abs(out['swave'][0] - 0.1) < 1e-4
    ok = ok and len(out['swave'][2]) == 0 and abs(out['chern'][0] + 2) < 1e-6 and abs(out['chern'][1] + 2) < 1e-6
    check('a vacancy in the chiral p-wave and in the s-wave superconductor of the notebook', ok,
          'triangular lattice, add_onsite(-4), delta=0.1: chiral_pwave has the gap edge %.4f on a 240 mesh and get_gap()/2 = '
          '%.5f, the 2x2 cell of the notebook has get_gap() = %.5f, C = %+.4f from the link variables and %+.4f from '
          'get_chern(), and the eigenvalues of the 4x4 local Green\'s function vanish at E/edge = %s; swave has the edge %.4f '
          'and no zero' % (out['chiral_pwave'][0], out['chiral_pwave'][1], g22, out['chern'][0], out['chern'][1],
                           np.round(rp, 4).tolist(), out['swave'][0]))

    # Screening in a quantum magnet
    fu = spinon_figure(1.0)
    i0 = 40
    ns_ = np.arange(2, 32)
    nm_fig = np.array([n_ * abs(fu[i0 + n_]) for n_ in ns_])
    nm_inf = np.array([n_ * abs(spinon_uniform(n_)) for n_ in ns_])
    dev = np.abs(nm_fig / nm_inf - 1)
    alt = all(fu[i0 + n_] * fu[i0 + n_ + 1] < 0 for n_ in range(0, 31))
    ok = alt and abs(nm_fig.min() - 0.00377) < 5e-5 and abs(nm_fig.max() - 0.00448) < 5e-5 and nm_inf.min() > 0.00375 and nm_inf.max() < 0.00400
    ok = ok and abs(dev.max() - 0.13) < 0.01 and ns_[np.argmax(dev)] == 31
    check('the figure spinon_impurity, the uniform chain', ok,
          'the moment changes sign on every site, n|m_n| is between %.5f and %.5f for n = 2 to 31 in the open chain of the '
          'figure, and between %.5f and %.5f in the infinite chain, from the Dyson equation; the largest difference is %.3f, '
          'at n=%d' % (nm_fig.min(), nm_fig.max(), nm_inf.min(), nm_inf.max(), dev.max(), ns_[np.argmax(dev)]))
    fd = spinon_figure(0.6)
    md = spinon_dyson(0.6)
    rel = np.abs(fd / md - 1)
    gap = 2 * np.min(np.abs(1.0 + 0.6 * np.exp(1j * np.linspace(-np.pi, np.pi, 2001))))
    part, other = md[i0 + 1] / md[i0], md[i0 - 1] / md[i0]
    share = abs(md[i0 + 1]) / (np.abs(md).sum() - abs(md[i0]))
    rates = [-np.polyfit(np.arange(10 + p, 41, 2), np.log(np.abs(md[i0 + 10 + p:i0 + 41:2])), 1)[0] for p in (0, 1)]
    first = [next(j for j in range(p, 41, 2) if abs(md[i0 + j]) < 1e-11) for p in (0, 1)]
    shown = [j for j in range(41) if abs(md[i0 + j]) >= 1e-11]          # the points above the lower end of the panel
    worst = max(rel[i0 + j] for j in shown)
    ok = abs(gap - 0.8) < 1e-6 and abs(part + 0.806) < 0.002 and abs(other + 0.053) < 0.002 and abs(share - 0.655) < 0.005
    ok = ok and abs(rates[0] - 0.573) < 0.005 and abs(rates[1] - 0.532) < 0.005 and first == [32, 39] and worst < 1e-3
    check('the figure spinon_impurity, the dimerized chain', ok,
          'gap %.3f; from the Dyson equation of the infinite chain the partner of site 0 has %.3f of its moment, %.3f of all '
          'the moment off site 0, and the other neighbor %.3f; rates %.3f and %.3f per site on the two sublattices from n=10 '
          'to 40, ln(1/0.6) = %.3f; |m_n| < 1e-11 from n=%d on the sublattice of site 0 and from n=%d on the other; at the '
          'points above 1e-11 the diagonalization of the figure differs from it by at most %.0e, and by %.0e at n=38'
          % (gap, part, share, other, rates[0], rates[1], np.log(1 / 0.6), first[0], first[1], worst, rel[i0 + 38]))

    # Anderson localization
    xi = {W: [lyapunov(W, 100000, s) for s in range(6)] for W in (0.25, 0.5, 1.0)}
    xw = np.array([np.array(vv_) * W * W for W, vv_ in xi.items()])
    ok = xw.min() > 23 and xw.max() < 29.5 and min(xi[0.5]) > 95 and max(xi[0.5]) < 110
    check('the localization length of the random chain at E=0', ok,
          'w_n uniform in [-W, W], transfer matrix of 10^5 sites, 6 seeds, xi W^2 from %.1f to %.1f for W = 0.25, 0.5, 1, and '
          '105/4 = 26.25 at the band center; xi(0.5t) is %.0f to %.0f sites' % (xw.min(), xw.max(), min(xi[0.5]), max(xi[0.5])))
    rng = np.random.default_rng(3)
    x1 = np.mean(xi[1.0])
    lt = {L: np.mean([log_transmission(1.0, L, rng) for _ in range(200)]) for L in (200, 400)}
    slope = (lt[200] - lt[400]) / 200
    R['cond'] = (slope, 2 / x1)
    check('the conductance falls as e^{-2L/xi}', abs(slope * x1 / 2 - 1) < 0.15,
          'W=t, <ln T> is %.1f and %.1f for segments of 200 and 400 sites, 200 samples each, a slope %.4f per site, and '
          '2/xi = %.4f with xi = %.1f from the transfer matrix' % (lt[200], lt[400], slope, 2 / x1, x1))
    gc = geometry.chain(200); gc.dimensionality = 0
    hc = gc.get_hamiltonian(has_spin=False)
    hc.add_onsite(2.0 * (np.arange(200) == 100))
    es, ls = hc.get_tails()
    i = int(np.argmax(es))
    kap = np.arccosh(es[i] / 2)
    wv = np.exp(-np.abs(np.arange(400) - 200) / 5.0); wv /= np.linalg.norm(wv)
    l5 = tails.loclength([wv])
    gc = geometry.chain(400); gc.dimensionality = 0
    aa = []
    for v_ in (1.0, 3.0, 4.0):
        ha = gc.get_hamiltonian(has_spin=False)
        ha.add_onsite(v_ * np.cos(np.sqrt(2) * np.pi * gc.r[:, 0]))
        aa.append(float(np.mean(ha.get_tails()[1])))
    ok = abs(ls[i] - 2 * kap) < 1e-6 and abs(l5 - 0.4) < 1e-9 and abs(aa[0]) < 0.01
    ok = ok and abs(aa[1] / (2 * np.log(1.5)) - 1) < 0.1 and abs(aa[2] / (2 * np.log(2)) - 1) < 0.05
    check('h.get_tails() is the decay rate of |psi|^2', ok,
          'the bound state of an impurity 2t in a chain of 200 sites has |psi| ~ e^{-kappa n} with kappa = %.4f, and get_tails '
          'gives %.4f = 2 kappa; a state e^{-|n|/5} gives %.3f; on the notebook chain of 400 sites with v cos(sqrt2 pi x) the '
          'mean is %.3f, %.3f and %.3f for v = 1, 3, 4, against 0, 2 ln(v/2) = %.3f and %.3f'
          % (kap, ls[i], l5, aa[0], aa[1], aa[2], 2 * np.log(1.5), 2 * np.log(2)))
    hq = gc.get_hamiltonian(has_spin=False)
    np.random.seed(11)
    hq.add_onsite(lambda r_: 2.0 * (np.random.random() - 0.5))
    on = np.diag(dense(hq.intra)).real
    check('the random potential of the notebook', on.min() >= -1.0 and on.max() <= 1.0 and on.max() - on.min() > 1.9,
          'v*(np.random.random()-0.5) with v=2 gives onsite energies from %.3f to %.3f, so v is 2W' % (on.min(), on.max()))
    ip = {(N, V0): aah_nipr(N, V0) for N in (55, 233, 987) for V0 in (0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0)}
    kpw = 2 * np.pi * np.arange(987) / 987
    plane = np.mean([987 * np.sum(np.abs(np.exp(1j * kk_ * np.arange(987)) / np.sqrt(987)) ** 4) for kk_ in kpw[:50]])
    big = lambda V0: [ip[N, V0] for N in (55, 233, 987)]
    ok = all(abs(x_ - 1.5) < 0.01 for x_ in big(0.0)) and abs(plane - 1) < 1e-9 and all(1.65 < x_ < 1.75 for x_ in big(0.5))
    ok = ok and all(1.99 < x_ < 2.11 for x_ in big(1.0)) and all(2.6 < x_ < 2.95 for x_ in big(1.5)) and all(4.4 < x_ < 6.0 for x_ in big(1.9))
    ipr25 = [ip[N, 2.5] / N for N in (55, 233, 987)]
    ipr30 = [ip[N, 3.0] / N for N in (55, 233, 987)]
    ok = ok and max(ipr25) - min(ipr25) < 0.01 and max(ipr30) - min(ipr30) < 0.01
    R['aah'] = (big(0.0), big(1.0), big(1.9))
    fmt = lambda V0, d: ' '.join(('%.' + str(d) + 'f') % x_ for x_ in big(V0))
    check('the figure aah_ipr', ok,
          'N IPR for N = 55, 233, 987 is %s at V0=0, where a plane wave gives %.2f, %s at 0.5t, %s at t, %s at 1.5t and %s '
          'at 1.9t; the IPR is %s at 2.5t and %s at 3t' % (fmt(0.0, 3), plane, fmt(0.5, 2), fmt(1.0, 2), fmt(1.5, 2), fmt(1.9, 2),
                                                          ' '.join('%.3f' % x_ for x_ in ipr25), ' '.join('%.3f' % x_ for x_ in ipr30)))
    L3, W3 = 10, 20.0
    dens, ext = [], []
    x3, y3, z3 = np.meshgrid(np.arange(L3), np.arange(L3), np.arange(L3), indexing='ij')
    i3 = (x3 * L3 * L3 + y3 * L3 + z3).ravel()
    for s in range(4):
        rng = np.random.default_rng(10 + s)
        H = np.diag(W3 * (2 * rng.random(L3 ** 3) - 1))
        for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            j3 = ((((x3 + dx) % L3) * L3 + (y3 + dy) % L3) * L3 + (z3 + dz) % L3).ravel()
            H[i3, j3] = H[j3, i3] = -1.0
        ee = np.linalg.eigvalsh(H)
        dens.append(np.sum(np.abs(ee) < 2.0) / (4.0 * L3 ** 3)); ext.append(np.abs(ee).max())
    R['dos3'] = (min(dens), max(dens))
    check('the density of states of the 3D Anderson model at W=20t', 0.02 < min(dens) and max(dens) < 0.03 and max(ext) < 26,
          'cubes of 10^3 sites, 4 seeds, states per site and per unit of energy in |E| < 2t, from %.4f to %.4f, and 1/(2W) = '
          '%.3f; the largest |E| is %.1f, inside 6t+W = 26t' % (min(dens), max(dens), 1 / (2 * W3), max(ext)))
    check('the numbers of the quizzes of Sections 9.6, 9.9 and 9.10', abs(10 * 0.1 ** 2 - 0.1) < 1e-12 and abs(2 ** -0.5 - 0.71) < 0.005
          and abs(np.exp(-4) - 0.018) < 0.0005 and np.allclose(np.cos(np.pi * np.arange(8) / 2), np.cos(np.pi * (np.arange(8) + 4) / 2)),
          'the IPR of ten equal sites is %.2f, 2^-0.5 = %.3f so tau = 0.5, e^-4 = %.4f, and cos(pi x/2) has the period 4'
          % (10 * 0.1 ** 2, 2 ** -0.5, np.exp(-4)))

    # The statements of the old text that these numbers contradict, each with the numbers of its line above
    check('wrong: the plasmon of Figure 9.2', R['plasmon'][0] < 0 and R['plasmon'][1],
          'chi_0 = %.6f N(0) < 0 above the continuum, so the zero is of 1 + v chi_0 and not of 1 - v chi_0' % R['plasmon'][0])
    check('wrong: the sign of delta n(x) in Section 9.6a', R['dn0'] < 0 and all(a < 0 < c for Q, a, c in R['dn_q']),
          'delta n(0)/v0 = %+.4f for a repulsive impurity, delta n(q) = -chi_0(q) v(q)' % R['dn0'])
    check('wrong: "in the Born approximation" in Section 9.7', abs(R['born'][1] - 0.6) < 1e-3 and abs(R['born'][0] - 0.5) < 1e-12,
          'the lattice gives %.4f Delta at alpha=0.5, (9.10) 0.6000, the first order %.2f' % (R['born'][1], R['born'][0]))
    check('wrong: the state at -0.016t of the quiz of Section 9.8', abs(R['m05'][0] + 0.197) < 0.002 and R['m05'][1] > 0.2,
          'G_AA(-0.016t) = %.3f and G_BB(-0.016t) = %+.3f, neither is zero, and the 18x18 torus level is at %+.4f' % R['m05'])
    rows = R['insulator']
    check('wrong: the gaps 0.1 and 0.3 of the try-it of Section 9.9', abs(rows[0][3] - 0.2) < 2e-3 and abs(rows[1][3] - 0.6) < 2e-3,
          'the gaps are %.3f and %.3f' % (rows[0][3], rows[1][3]))
    check('wrong: "within one or two sites" in the notebook box of Section 9.6b', rows[0][6] > 9 and rows[1][6] > 3,
          'the LDOS change decays over %.2f and %.2f sites' % (rows[0][6], rows[1][6]))
    hopb, spl, gapeq = R['bichain']
    check('wrong: bichain as a dimerized chain, Sections 9.5b and 9.9', np.allclose(hopb, 1.0),
          'the two hoppings are %.0f and %.0f' % (hopb[0], hopb[1]))
    check('wrong: 1/W for the density of states in the quiz of Section 9.10b', R['dos3'][1] < 0.03,
          'from %.4f to %.4f per site and per unit of energy, 1/(2W) = 0.025 and not 1/W = 0.05' % R['dos3'])
    check('depends: the state at -0.14t of the quiz of Section 9.8', R['m03'][0] < 0 < R['m03'][1],
          '%+.4f for the vacancy on the sublattice with +M and %+.4f on the other' % R['m03'])
    check('depends: the guaranteed in-gap mode of Section 9.8 and Figure 9.4', abs(R['m05'][0] + 0.197) < 0.002,
          'at M=0.5t with C=1 G_AA has no zero in the gap away from the edge')
    o = R['ssh'][0]
    check('depends: the SSH quiz of Section 9.8', len(o[3][0]) == 0 and len(o[3][1]) == 2,
          'the onsite energy 2t removes the zero level only on the neighbor joined by the strong bond')
    (b, c5_), (st, sd) = R['sq'], R['ln2']
    check('depends: D(E_F) of the caption of stoner, and "logarithmically enhanced"', abs(b[0] - 0.264) < 1e-3 and c5_[0] > b[0] + 0.03
          and np.all(sd > 0.02),
          '0.264 at T=0.1t grows to %.3f at 0.05t, and chi_0(pi,pi) has the second differences %s in ln(1/T)'
          % (c5_[0], np.round(sd, 4).tolist()))
    check('depends: e^{-L/xi} in the quiz of Section 9.10b', abs(R['cond'][0] / R['cond'][1] - 1) < 0.15,
          'the slope of <ln T> is %.4f per site, 2/xi = %.4f' % R['cond'])
    check('depends: N IPR about 2 below V0=2t in the caption of aah_ipr', all(abs(x_ - 1.5) < 0.01 for x_ in R['aah'][0])
          and all(x_ > 4.4 for x_ in R['aah'][2]),
          'N IPR is %s at V0=0, %s at t and %s at 1.9t' % tuple(np.round(a_, 2).tolist() for a_ in R['aah']))
    check('lecturer: chi_A of Section 9.3 for the density and an onsite energy', all(a < 0 for Q, a, c in R['dn_q']),
          'dn/dv = %s, so chi_A = -chi_0' % ', '.join('%.4f' % a for Q, a, c in R['dn_q']))
    ch_, sp_, c0_ = R['rpa']
    check('lecturer: (9.6) without the factor 2 of the spins', abs(-ch_ / (2 * c0_) - 1 / (1 + c0_)) < 1e-3,
          'the density response %.4f is 2 chi_0 = %.4f times 1/(1 + U chi_0) = %.4f' % (-ch_, 2 * c0_, 1 / (1 + c0_)))

    print('%d checks hold, %.1f s' % (COUNT[0], time.time() - t0))
    assert COUNT[0] == SHEET_LINES, 'the sheet has %d bullets, the script made %d checks' % (SHEET_LINES, COUNT[0])


if __name__ == '__main__':
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            main()
        finally:
            os.chdir(cwd)
