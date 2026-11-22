"""Checks of webnotes/conventions/session04.md, with numbers. Every line of the sheet is asserted here, in the order of
the sheet, and the script prints one line per line of the sheet. It exits 0 when all hold.

The sheet was written from two drafts made apart, and the lines where they disagreed, or that only one of them had,
are computed here again with code of their own: the five percent bound of the square lattice, the rule for the flux
of a two-dimensional honeycomb cell, the first Dirac level of the armchair ribbon at the field 0.02, the edge weight
of the local density of states, the domain wall built with the function of the notebook, the plateaus of plateaus.py
and the charge and the Berry phase of the quasihole.

Not asserted, since they are not a number: the decision of the lecturer on (3.4), the words of the pages, of the
notebook and of its comments, the rotation that takes the coordinates of a pyqula ribbon to those of a page, which is a
choice, the directions in which hall_setup.py draws V_y and I_x, and what the figure scripts dirac_levels.py,
lll_radius.py, laughlin_pair.py, droplet_density.py and plaquette_gauge.py draw, which was read and agrees with the
lines of their models. The lines of the open points repeat numbers of the lines above, the ones that the old text
contradicted, and each of them was settled on 2026-11-22, which the plan of the session records. The bullet of the
caption of landau_chern was dropped that day, since the caption gives the shift of 0.30 t that the lines of the lattice
assert, and the bullets of landau_chern.py and flat_chern_band.py now check the pyqula scripts that these figures draw. The lines taken from Session 3 are asserted by webnotes/checks/session03/conventions.py, and here
only by their anchor. A figure script is not imported, since it saves its figure when it runs, and the lines of its
model are written again here.

The Monte Carlo of the Laughlin state runs with fixed seeds, so its numbers are the same at every run, and its
tolerances come from the scatter between seeds. The script took 96 s on a busy machine, half of it in the Monte
Carlo.

Run it from anywhere:  python3 webnotes/checks/session04/conventions.py"""
import os, sys, tempfile, time
sys.dont_write_bytecode = True
from math import lgamma
import numpy as np

WEBNOTES = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(WEBNOTES, 'figures'))
sys.path.insert(0, os.path.join(WEBNOTES, 'figures', 'session03'))
import physcheck as pc
import _honeycomb as hc

HBAR, E, ME, H, KB = 1.054571817e-34, 1.602176634e-19, 9.1093837015e-31, 6.62607015e-34, 1.380649e-23
S3 = np.sqrt(3)
COUNT = [0]


def check(name, ok, detail):
    """Prints one line for a check and stops the script when it does not hold."""
    print(('ok    ' if ok else 'FAIL  ') + name + ': ' + detail, flush=True)
    assert ok, name
    COUNT[0] += 1


def D(m):
    return np.asarray(m.todense() if hasattr(m, 'todense') else m)


# ------------------------------------------------------------------------------------------------ models of this file

def square_cell(q, s=1, t=-1.0):
    """The square lattice with the hopping t and the flux 1/q per plaquette, with the phase (4.4) of A = (0, s B x),
    so s=+1 is the charge +e in the field +B z. The cell holds q sites along x, the hop from (x, y) to (x, y+1) has
    the amplitude t exp(i s B x), and the Bloch state goes as exp(i k_y y) and exp(i k_x q) from one cell to the next."""
    Bf = 2 * np.pi / q

    def hk(k):
        h = np.zeros((q, q), complex)
        x = np.arange(q)
        h[x, x] = 2 * t * np.cos(k[1] - s * Bf * x)
        for j in range(q - 1):
            h[j + 1, j] = h[j, j + 1] = t
        h[q - 1, 0] += t * np.exp(1j * k[0] * q)
        h[0, q - 1] += t * np.exp(-1j * k[0] * q)
        return h
    return hk, np.array([[2 * np.pi / q, 0.0], [0.0, 2 * np.pi]])


def harper_bottom(q, nlev):
    """The lowest levels of the square lattice with t=1 and the flux 1/q, above the band bottom -4, from one period of
    the Harper chain -2 cos(2 pi (x - q/2)/q) with its minimum in the middle, open at both ends, which holds the levels
    of the magnetic cell to 1e-5 or better for q >= 12."""
    from scipy.linalg import eigh_tridiagonal
    x = np.arange(q)
    d = -2 * np.cos(2 * np.pi * (x - q / 2) / q)
    return eigh_tridiagonal(d, -np.ones(q - 1), select='i', select_range=(0, nlev - 1))[0] + 4


def island(L, flux, s=1):
    """An L x L island of the square lattice, hopping -1, with the phase (4.4) of A = (0, s B x), B = 2 pi flux.
    Returns H, with H[b, a] the amplitude of the hop from a to b, and the positions."""
    pos = np.array([(x, y) for x in range(L) for y in range(L)], float)
    Hm = np.zeros((L * L, L * L), complex)
    for i, (x, y) in enumerate(pos):
        if x + 1 < L:
            Hm[i + L, i] = Hm[i, i + L] = -1
        if y + 1 < L:
            Hm[i + 1, i] = -np.exp(1j * s * 2 * np.pi * flux * x)
            Hm[i, i + 1] = np.conj(Hm[i + 1, i])
    return Hm, pos


def loop(Hm, ids):
    """The phase of the product of the amplitudes H[b, a] along the closed path ids, taken in that order."""
    return np.angle(np.prod([Hm[ids[(k + 1) % len(ids)], ids[k]] for k in range(len(ids))]))


def oscillator_wall(x0s, W=10.0, n=3000, nlev=1):
    """The lowest levels of p^2/2 + (x - x0)^2/2 with a hard wall at x=0 and at x=W, by finite differences."""
    from scipy.linalg import eigh_tridiagonal
    x = np.linspace(0, W, n + 2)[1:-1]
    hx = x[1] - x[0]
    return np.array([eigh_tridiagonal(1 / hx ** 2 + 0.5 * (x - x0) ** 2, -0.5 / hx ** 2 * np.ones(n - 1),
                                      select='i', select_range=(0, nlev - 1))[0] for x0 in x0s])


def tiling(h, g):
    """A 3 x 3 tiling of the cell of a periodic pyqula Hamiltonian, from its multicell hoppings <i,0|H|j,R> = T_R[i,j].
    Returns the matrix, the positions and the number of sites of one cell, the middle cell being the fifth."""
    hm = h.get_multicell()
    T = {tuple(int(round(v)) for v in t.dir[:2]): D(t.m) for t in hm.hopping}
    T[(0, 0)] = D(hm.intra)
    a1, a2, n = np.array(g.a1[:2]), np.array(g.a2[:2]), len(g.r)
    cells = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1)]
    pos = np.array([g.r[s, :2] + c[0] * a1 + c[1] * a2 for c in cells for s in range(n)])
    Hb = np.zeros((9 * n, 9 * n), complex)
    for A, c1 in enumerate(cells):
        for Bc, c2 in enumerate(cells):
            R = (c2[0] - c1[0], c2[1] - c1[1])
            if R in T:
                Hb[A * n:(A + 1) * n, Bc * n:(Bc + 1) * n] = T[R]
    return Hb, pos, n


def plaquette_fluxes(g, phi, sides, bond=1.0):
    """The loop phase over 2 pi of every plaquette with its center in one cell of the geometry g with
    add_orbital_magnetic_field(phi), counterclockwise, for plaquettes of 4 sides (square) or 6 sides (honeycomb)."""
    h = g.get_hamiltonian(has_spin=False)
    h.add_orbital_magnetic_field(phi)
    Hb, pos, n = tiling(h, g)
    rad = bond / (2 * np.sin(np.pi / sides))
    dirs = np.array([[np.cos(a), np.sin(a)] for a in np.arange(24) * np.pi / 12])
    cand = np.unique(np.round((pos[:, None, :] + rad * dirs[None]).reshape(-1, 2), 6), axis=0)
    inv = np.linalg.inv(np.array([g.a1[:2], g.a2[:2]]).T)
    mid = g.r[:, :2].mean(0)
    out = []
    for c in cand:
        f = inv @ (c - mid)
        if not np.all((f > -0.5) & (f <= 0.5)):
            continue
        d = np.linalg.norm(pos - c, axis=1)
        ring = np.where(np.abs(d - rad) < 1e-6)[0]
        if len(ring) != sides or d.min() < 0.5 * rad:
            continue
        ring = ring[np.argsort(np.arctan2(pos[ring, 1] - c[1], pos[ring, 0] - c[0]))]
        z = np.prod([Hb[ring[(k + 1) % sides], ring[k]] for k in range(sides)])
        if abs(z) > 1e-9:
            out.append(np.angle(z) / (2 * np.pi))
    return np.array(out)


def central_level(g, phi, window, nk=6, frac=0.3):
    """The energy of the states of one Landau level of a pyqula ribbon that sit in the middle of the ribbon. In a
    window of energy at each k the operator y is diagonalized in the space of the eigenstates, which separates the
    guiding centers, and the energies <H> of the localized states within frac of the half width are returned, with
    their spread sqrt(<H^2> - <H>^2), which is zero for a level that the lattice does not broaden."""
    h = g.get_hamiltonian(has_spin=False)
    h.add_orbital_magnetic_field(phi)
    gen = h.get_hk_gen()
    y = g.y - g.y.mean()
    ens, spr = [], []
    for k in np.linspace(0, 0.5, nk):
        Hk = D(gen([k, 0, 0]))
        e, v = np.linalg.eigh(Hk)
        sel = (e > window[0]) & (e < window[1])
        V = v[:, sel]
        yy, U = np.linalg.eigh(V.conj().T @ (y[:, None] * V))
        L = V @ U
        en = np.real(np.einsum('ia,ij,ja->a', L.conj(), Hk, L))
        e2 = np.real(np.einsum('ia,ij,jk,ka->a', L.conj(), Hk, Hk, L))
        c = np.abs(yy) < frac * np.ptp(y) / 2
        ens += list(en[c]); spr += list(np.sqrt(np.maximum(e2 - en ** 2, 0))[c])
    return np.array(ens), np.array(spr)


def orbital_density(m, r):
    """|psi_m|^2 of (4.10), normalized, with r in units of l_B."""
    return np.exp(2 * m * np.log(np.maximum(r, 1e-300)) - r ** 2 / 2 - m * np.log(2) - lgamma(m + 1)) / (2 * np.pi)


def metropolis(N, m, holes, seed, nw=300, neq=150, nmeas=350, step=1.0, w=None, R=np.arange(0.5, 10.01, 0.5)):
    """Samples |prod_{i<j} (z_i - z_j)^m prod_i prod_h (z_i - h) exp(-sum |z_i|^2/4)|^2, lengths in l_B, with nw walkers
    that move one electron at a time. Returns the mean number of electrons inside each radius of R, the radii of all
    the samples, and with w the mean of sum_i Re[w/(z_i - w)], the Berry connection of the quasihole at w = |w| e^(i theta)."""
    rng = np.random.default_rng(seed)
    holes = np.array(holes, complex)
    z = np.sqrt(2 * m * N * rng.random((nw, N))) * np.exp(2j * np.pi * rng.random((nw, N)))
    nin, conn, rs = np.zeros(len(R)), 0.0, []
    for sweep in range(neq + nmeas):
        for i in range(N):
            zi = z[:, i]
            zn = zi + step * (rng.normal(size=nw) + 1j * rng.normal(size=nw)) / np.sqrt(2)
            o = np.concatenate([z[:, :i], z[:, i + 1:]], axis=1)
            dl = 2 * m * np.log(np.abs((zn[:, None] - o) / (zi[:, None] - o))).sum(1) - (np.abs(zn) ** 2 - np.abs(zi) ** 2) / 2
            for hh in holes:
                dl += 2 * np.log(np.abs((zn - hh) / (zi - hh)))
            ok = np.log(rng.random(nw)) < dl
            z[ok, i] = zn[ok]
        if sweep >= neq:
            r = np.abs(z)
            nin += (r[:, :, None] < R[None, None, :]).sum(1).mean(0)
            rs.append(r.ravel().copy())
            if w is not None:
                conn += np.real(w / (z - w)).sum(1).mean()
    return nin / nmeas, np.concatenate(rs), (conn / nmeas if w is not None else None)


# ------------------------------------------------------------------------------------------------ the checks

def main():
    """Runs every check. The pyqula calls write files, so the caller runs this in a temporary folder."""
    import sympy as sp
    from scipy.special import pbdv, gammainc
    from scipy.optimize import brentq
    from scipy.linalg import eigh_tridiagonal
    from pyqula import geometry, islands
    t0 = time.time()
    gh = geometry.honeycomb_lattice()

    # ---------------------------------------------------------------- from Session 3
    h = gh.get_hamiltonian(has_spin=False); h.add_haldane(0.1)
    hk, B = pc.from_pyqula(h)
    cp, ck = h.get_chern(), pc.chern_kubo(hk, B, 0, nk=24)
    check('the Berry curvature, the Chern number and the Hall conductivity of Session 3', abs(cp - 1) < 1e-6 and abs(ck - 1) < 1e-4,
          'add_haldane(0.1) has h.get_chern() %+.4f and the form with no phase %+.4f, the anchor of session03.md' % (cp, ck))
    g09 = pc.gap(hk, B, 1, nk=60)
    h7 = gh.get_hamiltonian(has_spin=False); h7.add_haldane(0.07)
    hk7, B7 = pc.from_pyqula(h7)
    g07, c7 = pc.gap(hk7, B7, 1, nk=60), h7.get_chern()
    gb = pc.gap(lambda k: hc.bloch(k, t2=0.1), pc.reciprocal([hc.a1, hc.a2]), 1, nk=60)
    check('the Haldane model of Session 3', abs(g09 - 0.9) < 1e-9 and abs(g07 - 0.63) < 1e-9 and abs(c7 - 1) < 1e-6 and abs(gb - 0.6 * S3) < 1e-9,
          'add_haldane(0.1) and (0.07) have the gaps %.3f and %.3f, C = %+.0f for 0.07, and _honeycomb.bloch(t2=0.1) has the gap %.3f'
          % (g09, g07, c7, gb))

    # ---------------------------------------------------------------- units and scales
    lB = np.sqrt(HBAR / E) * 1e9
    # the phase of (4.4) is (1/hbar) int A.dl with e = 1: the chain with the bond phase theta has its minimum at
    # k = theta/a and minimal coupling (hbar k - A)^2/2m at k = A/hbar, the same for theta = A a/hbar; and with the units
    # back (e/hbar) B a^2 is 2 pi B a^2/(h/e)
    kk_ = np.linspace(-np.pi, np.pi, 200001)
    hb_, A_, a_ = 0.37, 0.2, 1.7
    kmin = kk_[np.argmin(-np.cos(kk_ * a_ - A_ * a_ / hb_))]
    ph4 = E / HBAR * 10.0 * (5e-10) ** 2
    check('the magnetic length', abs(lB - 25.66) < 0.005 and abs(2 * np.pi * (lB * 1e-9) ** 2 / (H / E) - 1) < 1e-8
          and abs(np.sqrt(HBAR / (E * 4)) * 1e9 - lB / 2) < 1e-12 and abs(kmin - A_ / hb_) < 1e-4
          and abs(ph4 / (2 * np.pi * 10.0 * (5e-10) ** 2 / (H / E)) - 1) < 1e-9,     # hbar of 10 digits against h
          'l_B = %.2f nm at 1 T and %.2f nm at 4 T, 2 pi l_B^2 B is h/e, the chain with the bond phase A a/hbar has its minimum at '
          'k = %.4f = A/hbar, and (e/hbar) B a^2 is 2 pi times the flux in h/e' % (lB, lB / 2, kmin))
    per = E / H * 1e-12
    Lt, qt = 24, 12
    hk_t, _ = square_cell(qt)
    # the torus of Lt x Lt sites is the magnetic cell at the Lt/qt x Lt allowed momenta
    et = np.sort(np.concatenate([np.linalg.eigvalsh(hk_t(np.array([2 * np.pi * a / Lt, 2 * np.pi * b / Lt])))
                                 for a in range(Lt // qt) for b in range(Lt)]))
    nq = Lt * Lt // qt
    check('the degeneracy, one state per flux quantum', abs(per - 241.8) < 0.05 and round(per) == 242 and round(2 * per) == 484
          and abs(et[nq] - et[nq - 1] - 0.92) < 0.005 and et[nq - 1] - et[0] < 1e-4,
          'e B/h is %.1f per square micrometre at 1 T, so a sample of 1 um^2 holds %d states at 1 T and %d at 2 T, and a %d x %d torus '
          'with the flux 1/%d has %d states in its lowest level, flat to %.0e, with a gap %.2f above' % (per, round(per), round(2 * per), Lt, Lt,
                                                                                                     qt, nq, et[nq - 1] - et[0], et[nq] - et[nq - 1]))
    gaas = [HBAR * E * b / (0.067 * ME) / E * 1e3 for b in (1, 4, 10)]
    a_lat = 3e-9
    lat = 4 * np.pi * (E * a_lat ** 2 / H) * HBAR ** 2 / (2 * 0.067 * ME * a_lat ** 2) / E * 1e3     # 4 pi phi t at 1 T
    kelvin = gaas[0] * 1e-3 * E / KB
    check('the cyclotron energy of GaAs', abs(gaas[0] - 1.728) < 1e-3 and abs(gaas[1] - 6.91) < 0.005 and abs(gaas[2] - 17.28) < 0.005
          and abs(lat / gaas[0] - 1) < 1e-8 and abs(kelvin - 20.05) < 0.05,
          'hbar e B/m with m = 0.067 m_e is %.3f, %.2f and %.2f meV at 1, 4 and 10 T, 4 pi phi t with t = hbar^2/2ma^2 gives %.3f meV at 1 T, '
          'and 1.73 meV is %.1f K' % (*gaas, lat, kelvin))
    gr = [1e6 * np.sqrt(2 * HBAR * E * b) / E * 1e3 for b in (1, 4, 9, 10)]
    acc = 0.142e-9; tg = 2 * HBAR * 1e6 / (3 * acc)
    grl = 1.5 * np.sqrt(4 * np.pi * acc ** 2 * E / H) * tg / E * 1e3
    check('the first Landau level of graphene', np.allclose(gr, [36.28, 72.56, 108.84, 114.73], atol=0.01) and abs(grl / gr[0] - 1) < 1e-8,
          'v sqrt(2 hbar e B) with v = 10^6 m/s is %.1f, %.1f, %.1f and %.1f meV at 1, 4, 9 and 10 T, and (3/2) sqrt(4 pi phi) t of the '
          'honeycomb lattice with the bond 0.142 nm and t = 2 hbar v/3a gives %.1f meV at 1 T' % (*gr, grl))
    r1, r10 = gr[0] / gaas[0], gr[3] / gaas[2]
    b100 = (r1 / 100) ** 2
    check('graphene against GaAs', abs(r1 - 21.0) < 0.05 and abs(r10 - 6.64) < 0.01 and abs(r10 * np.sqrt(10) - r1) < 1e-9 and abs(b100 - 0.044) < 0.001,
          'the first level of graphene over the spacing of GaAs is %.1f at 1 T and %.2f at 10 T, it goes as 1/sqrt(B), and it is 100 at %.3f T'
          % (r1, r10, b100))
    RK = H / E ** 2
    check('the resistance quantum', abs(RK - 25812.807) < 1e-3, 'h/e^2 = %.3f Ohm, %.4f kOhm for N=2 and %.4f kOhm for N=4' % (RK, RK / 2e3, RK / 4e3))

    # ---------------------------------------------------------------- the charge, the field and the sign of C
    x, y, Bs, hb = sp.symbols('x y B hbar', positive=True)
    f = sp.Function('f')(x, y)
    pis = lambda A, q: (lambda u: -sp.I * hb * sp.diff(u, x) - q * A[0] * u, lambda u: -sp.I * hb * sp.diff(u, y) - q * A[1] * u)
    comm = []
    for A in ((0, Bs * x), (-Bs * y / 2, Bs * x / 2)):
        px, py = pis(A, 1)
        comm.append(sp.simplify((px(py(f)) - py(px(f))) / f))
    Hm, pos = island(6, 0.07)
    lp = loop(Hm, [14, 20, 21, 15]) / (2 * np.pi)       # (2,2) -> (3,2) -> (3,3) -> (2,3), counterclockwise
    check('the charge +e of (4.3) and (4.4)', all(sp.simplify(c - sp.I * hb * Bs) == 0 for c in comm) and abs(lp - 0.07) < 1e-12,
          '[pi_x, pi_y] = %s in the Landau and in the symmetric gauge, and the amplitudes of (4.4) around a plaquette, counterclockwise, '
          'have the phase 2 pi times %+.3f for the flux 0.07' % (comm[0], lp))
    z = x + sp.I * y
    lll = {}
    for q in (1, -1):
        px, py = pis((-Bs * y / 2, Bs * x / 2), q)
        for nm, base in (('z', z), ('zbar', sp.conjugate(z))):
            for mm in (0, 1, 3):
                psi = base ** mm * sp.exp(-Bs * (x ** 2 + y ** 2) / (4 * hb))
                en = sp.simplify((px(px(psi)) + py(py(psi))) / psi / (hb * Bs))       # 2 E/(hbar omega_c) with m = 1
                Lz = sp.simplify(-sp.I * hb * (x * sp.diff(psi, y) - y * sp.diff(psi, x)) / psi / hb)
                lll[(q, nm, mm)] = (en / 2, Lz)
    g_ = sp.Function('g')(x, y)
    px, py = pis((-Bs * y / 2, Bs * x / 2), 1)
    ident = sp.simplify(px(g_) + sp.I * py(g_) + 2 * sp.I * hb * ((sp.diff(g_, x) + sp.I * sp.diff(g_, y)) / 2 + z * Bs / (4 * hb) * g_))
    half = sp.Rational(1, 2)
    ok = ident == 0 and all(lll[(1, 'z', mm)] == (half, mm) and lll[(-1, 'zbar', mm)] == (half, -mm) for mm in (0, 1, 3))
    ok = ok and all(lll[(1, 'zbar', mm)][0] == mm + half and lll[(-1, 'z', mm)][0] == mm + half for mm in (1, 3))
    check('the lowest Landau level and the sign of qB', ok,
          'pi_x + i pi_y = -2i hbar (d_zbar + z/4 l_B^2) for q = +e, z^m G has the energy %s hbar omega_c and L_z = %s hbar for m = 3, '
          'zbar^3 G has %s, and for q = -e zbar^3 G has %s and L_z = %s hbar' % (lll[(1, 'z', 3)][0], lll[(1, 'z', 3)][1],
                                                                                 lll[(1, 'zbar', 3)][0], lll[(-1, 'zbar', 3)][0], lll[(-1, 'zbar', 3)][1]))
    M = 100
    bm = np.diag(np.sqrt(np.arange(1, M)), 1)
    X, P = (bm + bm.T) / np.sqrt(2), 1j * (bm.T - bm) / np.sqrt(2)
    dirac = {}
    for q in (1, -1):
        piy = 0.3 * np.eye(M) - q * X                         # hbar k_y - q B x, with hbar = B = v = 1, so l_B = 1
        Hd = np.block([[np.zeros((M, M)), P - 1j * piy], [P + 1j * piy, np.zeros((M, M))]])
        e, v = np.linalg.eigh(Hd)
        inside = (np.abs(v[M // 2:M]) ** 2).sum(0) + (np.abs(v[M + M // 2:]) ** 2).sum(0) < 1e-6
        e, v = e[inside], v[:, inside]
        i0 = np.argmin(np.abs(e))
        dirac[q] = (abs(e[i0]), (np.abs(v[:M, i0]) ** 2).sum(), np.sort(e[e > 1e-6])[:4])
    ok = dirac[1][0] < 1e-9 and abs(dirac[1][1] - 1) < 1e-9 and dirac[-1][1] < 1e-9 and np.allclose(dirac[1][2], np.sqrt(2 * np.arange(1, 5)), atol=1e-8)
    check('the Dirac levels and the sign of qB', ok,
          'v(pi_x sigma_x + pi_y sigma_y) in a basis of %d oscillator states of x, not of the ladder operators, has the levels %s hbar v/l_B, '
          'sqrt(2|n|), and its zero mode has the weight %.3f in the upper component for q = +e and %.3f for q = -e'
          % (M, ' '.join('%.4f' % a for a in dirac[1][2]), dirac[1][1], dirac[-1][1]))
    # the motion for qB > 0: the continuum ribbon of 12 l_B with hard walls, H = p^2/2 + (k - x)^2/2, and an island
    xs = np.linspace(-6, 6, 1202)[1:-1]; hx = xs[1] - xs[0]

    def rib(k, F=0.0, n=2):
        return eigh_tridiagonal(1 / hx ** 2 + 0.5 * (xs - k) ** 2 - F * xs, -0.5 / hx ** 2 * np.ones(len(xs) - 1), select='i', select_range=(0, n - 1))
    cen = []
    for k in (-2.0, 0.0, 2.0):
        w_, v_ = rib(k, n=1)
        cen.append(np.sum(xs * v_[:, 0] ** 2) / np.sum(v_[:, 0] ** 2))
    sr = (rib(6.01, n=1)[0][0] - rib(5.99, n=1)[0][0]) / 0.02
    sl = (rib(-5.99, n=1)[0][0] - rib(-6.01, n=1)[0][0]) / 0.02
    Fx = 0.03
    drift = [(rib(0.01, Fx)[0][n] - rib(-0.01, Fx)[0][n]) / 0.02 / Fx for n in (0, 1)]
    cur = {}
    for s in (1, -1):
        Hm, pos = island(14, 1 / 16, s)
        e, v = np.linalg.eigh(Hm)
        st = v[:, np.argmin(np.abs(e - (-4 + 4 * np.pi / 16)))]          # a state in the first gap
        top = bot = 0.0
        for a in range(len(pos)):
            if pos[a, 0] + 1 < 14:
                b = a + 14
                j = 2 * np.imag(np.conj(st[b]) * Hm[b, a] * st[a])             # the current from a to b, along +x
                top += j * (pos[a, 1] > 6.5); bot += j * (pos[a, 1] < 6.5)
        cur[s] = (top, bot)
    ok = np.allclose(cen, [-2, 0, 2], atol=2e-3) and sr > 1 and sl < -1 and np.allclose(drift, -1, atol=1e-3)
    ok = ok and np.allclose(cur[1], [-0.196, 0.196], atol=5e-4) and np.allclose(cur[-1], [0.196, -0.196], atol=5e-4)
    check('the motion of the charge +e in the field +B z', ok,
          'in the ribbon of 12 l_B the lowest state of k_y l_B = -2, 0, 2 sits at x = %.3f, %.3f, %.3f l_B, the right wall has dE/dk = %+.2f and '
          'the left wall %+.2f, a field E_x gives dE/dk_y = %.4f and %.4f times e E_x l_B^2 in the two lowest levels, so v_y = -E_x/B, '
          'and in an island of 14 x 14 with the flux 1/16 a state of the first gap carries %+.3f along x in its upper half and %+.3f in '
          'its lower half, counterclockwise, and %+.3f and %+.3f with the field reversed' % (*cen, sr, sl, *drift, *cur[1], *cur[-1]))
    hk12, B12 = square_cell(12)
    C12 = [pc.chern_links(hk12, B12, n, nk=12) for n in range(3)]
    Ck12 = pc.chern_kubo(hk12, B12, 0, nk=12)
    hkm, Bm = square_cell(12, s=-1)
    Cm12 = pc.chern_links(hkm, Bm, 0, nk=12)
    check('the Chern number of a Landau level for qB > 0', np.allclose(C12, -1, atol=1e-9) and abs(Ck12 + 0.9998) < 5e-5 and abs(Cm12 - 1) < 1e-9
          and np.allclose(drift, -1, atol=1e-3),
          'the flux 1/12 with the phase of (4.4) gives C = %s for the three lowest levels from the links and %+.4f from the form with no '
          'phase, and %+.0f with the field reversed, while the drift above gives j_y = -(e^2/h) E_x, so j_x = +(e^2/h) E_y, which is '
          '-(e^2/h) C' % (' '.join('%+.0f' % c for c in C12), Ck12, Cm12))
    gq9 = geometry.square_lattice().get_supercell((1, 9))
    h9 = gq9.get_hamiltonian(has_spin=False); h9.add_orbital_magnetic_field(1 / 9)
    hk9, B9 = pc.from_pyqula(h9)
    c9 = (pc.chern_links(hk9, B9, 0, nk=12), pc.chern_links(hk9, B9, 8, nk=12), pc.chern_links(hk9, B9, range(8), nk=12))
    check('the levels at the top of the band', abs(c9[0] - 1) < 1e-9 and abs(c9[1] - 1) < 1e-9 and abs(c9[2] + 1) < 1e-9,
          'with pyqula and the flux 1/9 the lowest and the highest of the nine bands have C = %+.0f and %+.0f, and the eight bands below '
          'the top have %+.0f together' % c9)

    # ---------------------------------------------------------------- pyqula and the magnetic field
    gsr = geometry.square_ribbon(5)
    out = []
    for tij in (None, [-1.0]):
        hr = gsr.get_hamiltonian(has_spin=False) if tij is None else gsr.get_hamiltonian(has_spin=False, tij=tij)
        h0 = {tuple(t.dir): D(t.m) for t in hr.get_multicell().hopping}
        hr.add_orbital_magnetic_field(0.04)
        h1 = {tuple(t.dir): D(t.m) for t in hr.get_multicell().hopping}
        r = gsr.r
        expect = np.exp(1j * 2 * np.pi * 0.04 * (r[:, 0][:, None] - (r[:, 0][None] + 1)) * (r[:, 1][:, None] + r[:, 1][None]) / 2)
        out.append(np.allclose(h1[(1, 0, 0)], h0[(1, 0, 0)] * expect))
    hf = geometry.square_lattice().get_hamiltonian(has_spin=False).set_finite_system(n=3)
    hf.add_orbital_magnetic_field(0.04)
    rf = hf.geometry.r[:, :2]
    cid = [int(np.argmin(np.linalg.norm(rf - c, axis=1))) for c in ((0, 0), (1, 0), (1, 1), (0, 1))]
    lpq = loop(D(hf.intra), cid) / (2 * np.pi)
    check('add_orbital_magnetic_field, the phase and its sign', all(out) and abs(lpq + 0.04) < 1e-12,
          'the hopping to the next cell of a square ribbon is multiplied by exp[i 2 pi phi (x_i - x_j)(y_i + y_j)/2], with either sign '
          'of the hopping, and a counterclockwise plaquette of an island has the phase 2 pi times %+.3f for phi = 0.04' % lpq)
    fh = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False).set_finite_system(n=3)
    fh.add_orbital_magnetic_field(0.01)
    rh = fh.geometry.r[:, :2]
    hexd = None
    for p0 in rh:
        for a in np.arange(12) * np.pi / 6:
            c = p0 + [np.cos(a), np.sin(a)]
            d = np.linalg.norm(rh - c, axis=1)
            if np.sum(np.abs(d - 1) < 1e-6) == 6 and d.min() > 0.5:
                hexd = c; break
        if hexd is not None:
            break
    ring = np.where(np.abs(np.linalg.norm(rh - hexd, axis=1) - 1) < 1e-6)[0]
    ring = ring[np.argsort(np.arctan2(rh[ring, 1] - hexd[1], rh[ring, 0] - hexd[0]))]
    lph = loop(D(fh.intra), list(ring)) / (2 * np.pi)
    check('the unit of the field', abs(lph + 0.01 * 1.5 * S3) < 1e-12 and abs(1 / np.sqrt(2 * np.pi * 0.01) - 3.99) < 0.005,
          'a hexagon of the honeycomb lattice, bond 1, has the loop phase 2 pi times %+.5f for phi = 0.01, so phi is the flux per unit '
          'area and a hexagon holds 2.60 phi, and l_B = 1/sqrt(2 pi phi) is %.2f bond lengths for 0.01' % (lph, 1 / np.sqrt(2 * np.pi * 0.01)))
    g15 = geometry.square_lattice().get_supercell((1, 15))
    h15 = g15.get_hamiltonian(has_spin=False); h15.add_orbital_magnetic_field(1 / 15)
    hk15, B15 = pc.from_pyqula(h15)
    lv15 = np.linalg.eigvalsh(hk15(np.array([0.1, 0.2])))[:4]
    gaps15 = 0.5 * (lv15[:-1] + lv15[1:])
    cs15 = []
    for c in gaps15[:2]:
        hh = g15.get_hamiltonian(has_spin=False); hh.add_orbital_magnetic_field(1 / 15); hh.add_onsite(-c)
        cs15.append(hh.get_chern(nk=16))
    ahc = np.array(h15.get_anomalous_hall_conductivity(fermi=np.array([lv15[0] - 0.2, *gaps15[:2]]), T=0.01, nk=16), float)
    on = g15.get_hamiltonian(has_spin=False); on.add_onsite(0.3)
    check('the Chern number of the Landau levels in pyqula', np.allclose(cs15, [1, 2], atol=1e-6) and np.allclose(ahc, [0, 1, 2], atol=2e-3)
          and np.allclose(np.diag(D(on.intra)).real, 0.3),
          'with the flux 1/15, h.get_chern() is %+.3f and %+.3f with the zero of energy in the first and in the second gap, set with '
          'add_onsite, which adds its argument to every onsite energy, and get_anomalous_hall_conductivity is %.3f, %.3f, %.3f below the '
          'lowest level and in the two gaps' % (*cs15, *ahc))
    slopes, edge = [], []
    for tij in (None, [-1.0]):
        g40 = geometry.square_ribbon(40)
        hr = g40.get_hamiltonian(has_spin=False) if tij is None else g40.get_hamiltonian(has_spin=False, tij=tij)
        hr.add_orbital_magnetic_field(0.02)
        gen = hr.get_hk_gen()
        kb = 0.5 if tij is None else 0.0                           # the band bottom, where the guiding center is in the middle
        ym = []
        for dk in (-0.02, 0.02):
            e, v = np.linalg.eigh(D(gen([kb + dk, 0, 0])))
            ym.append(np.abs(v[:, 0]) ** 2 @ g40.y)
        slopes.append((ym[1] - ym[0]) / 0.04)
        for side in (1, -1):                                       # the lowest branch with its guiding center at an edge
            k = kb + side * 0.38
            e, v = np.linalg.eigh(D(gen([k, 0, 0])))
            de = (np.linalg.eigvalsh(D(gen([k + 1e-3, 0, 0])))[0] - np.linalg.eigvalsh(D(gen([k - 1e-3, 0, 0])))[0]) / 2e-3
            edge.append((np.abs(v[:, 0]) ** 2 @ g40.y, de))
    ok = all(yv > 15 and de > 0 for yv, de in edge[0::2]) and all(yv < -15 and de < 0 for yv, de in edge[1::2])
    gz = geometry.honeycomb_zigzag_ribbon(20)                      # the Haldane model, C=+1, in a pyqula ribbon
    hz = gz.get_hamiltonian(has_spin=False); hz.add_haldane(0.1)
    yz, genz, top = np.array(gz.r)[:, 1], hz.get_hk_gen(), []
    for kz in (0.45, 0.5, 0.55):
        ez, vz = np.linalg.eigh(D(genz([kz, 0, 0]))); ez2 = np.linalg.eigvalsh(D(genz([kz + 1e-5, 0, 0])))
        yy = (np.abs(vz) ** 2).T @ yz
        top += [np.sign(ez2[j] - ez[j]) for j in range(len(ez)) if abs(ez[j]) < 0.2 and yy[j] > 0.6 * yz.max()]
    import importlib.util                                          # the numpy ribbon of Session 6, which takes -k
    spec = importlib.util.spec_from_file_location('_haldane_s06', os.path.join(WEBNOTES, 'figures', 'session06', '_haldane.py'))
    hd6 = importlib.util.module_from_spec(spec); spec.loader.exec_module(hd6)
    e6, v6 = np.linalg.eigh(hd6.ribbon(2.6, 24, 1.0, 0.1)); e6b = np.linalg.eigvalsh(hd6.ribbon(2.6 + 1e-4, 24, 1.0, 0.1))
    low6 = [np.sign(e6b[j] - e6[j]) for j in range(48) if abs(e6[j]) < 0.4 and (np.abs(v6[:10, j]) ** 2).sum() > 0.8]
    ok = ok and len(top) == 3 and set(top) == {1} and low6 == [1]
    check('the ribbon in a field', np.allclose(slopes, 50, rtol=0.01) and ok,
          'on the square ribbon of 40 the guiding center of the lowest level moves as dy0/dk = %.1f and %.1f for the hopping +1 and -1, '
          'which is 1/phi with k in units of 2 pi, and its branch has a positive slope at the edge of positive y and a negative slope at '
          'the other edge, for both hoppings; the zigzag ribbon of 20 with add_haldane(0.1) has the slopes %s at the edge of '
          'positive y for k = 0.45, 0.5, 0.55, and _haldane.ribbon of Session 6 with t2=+0.1 has %s at its lower edge'
          % (*slopes, [int(x) for x in top], [int(x) for x in low6]))
    gi = islands.get_geometry(name="square", n=5, nedges=4, rot=0.)
    lv_i = []
    for kw in ({}, {'gauge': 'symmetric'}):
        hi = gi.get_hamiltonian(has_spin=False); hi.add_orbital_magnetic_field(0.03, **kw); lv_i.append(np.linalg.eigvalsh(D(hi.intra)))
    g20 = geometry.square_ribbon(20)

    def ribbon_levels(phi, **kw):
        hr = g20.get_hamiltonian(has_spin=False); hr.add_orbital_magnetic_field(phi, **kw)
        gen = hr.get_hk_gen()
        return np.sort(np.concatenate([np.linalg.eigvalsh(D(gen([k, 0, 0]))) for k in np.linspace(0, 1, 30, endpoint=False)]))
    sym, lan, hlf = ribbon_levels(0.03, gauge='symmetric'), ribbon_levels(0.03), ribbon_levels(0.015)
    check('gauge="symmetric"', np.allclose(lv_i[0], lv_i[1], atol=1e-12) and np.abs(sym - hlf).max() < 1e-10 and np.abs(sym - lan).max() > 0.05,
          'on an island it gives the levels of the Landau gauge to %.0e, and on the square ribbon of 20 with the field 0.03 it gives the '
          'levels of the Landau gauge with 0.015, half of the field, to %.0e' % (max(np.abs(lv_i[0] - lv_i[1]).max(), 1e-16), max(np.abs(sym - hlf).max(), 1e-16)))
    sq10 = geometry.square_lattice().get_supercell((1, 10))
    fsq = [plaquette_fluxes(sq10, p, 4) for p in (0.1, 0.013)]
    rot = lambda n: geometry.honeycomb_lattice_square_cell().rotate(90).get_supercell((n, 1))
    unr = lambda n: geometry.honeycomb_lattice_square_cell().get_supercell((1, n))
    area = lambda g: abs(np.linalg.det(np.array([g.a1[:2], g.a2[:2]])))
    hexok = {}
    for name, g, F in (('rotated', rot(10), 1), ('rotated', rot(10), 0.5), ('unrotated', unr(10), 2), ('unrotated', unr(10), 1)):
        fl = plaquette_fluxes(g, F / area(g), 6)
        hexok[(name, F)] = np.allclose(fl, -F / area(g) * 1.5 * S3, atol=1e-9)
    ok = np.allclose(fsq[0], -0.1) and len(fsq[0]) == 10 and np.sum(np.abs(fsq[1] + 0.013) < 1e-9) == 9 and np.sum(np.abs(fsq[1] - 0.117) < 1e-9) == 1
    ok = ok and hexok[('rotated', 1)] and not hexok[('rotated', 0.5)] and hexok[('unrotated', 2)] and not hexok[('unrotated', 1)]
    span = {}
    for sc in ((2, 1), (1, 2)):                                    # one flux quantum per cell in both, the pi flux of Session 8
        hq = geometry.square_lattice().get_supercell(sc).get_hamiltonian(has_spin=False); hq.add_orbital_magnetic_field(0.5)
        genq = hq.get_hk_gen()
        eq = np.array([np.linalg.eigvalsh(D(genq([a_, b_, 0]))) for a_ in np.linspace(0, 1, 41) for b_ in np.linspace(0, 1, 41)])
        span[sc] = (eq.min(), eq.max(), np.abs(np.imag(D(hq.intra))).max())
    ok = ok and np.allclose(span[(2, 1)][:2], [-4, 4], atol=1e-9) and span[(2, 1)][2] == 0
    ok = ok and np.allclose(span[(1, 2)][:2], [-2 * np.sqrt(2), 2 * np.sqrt(2)], atol=1e-9)
    check('a two-dimensional cell with a field', ok,
          'the square supercell (1, 10) has the loop phase -2 pi times 0.1 on all its 10 plaquettes for the field 0.1, and with 0.013 one '
          'plaquette has %+.3f, with no warning; the supercell (2, 1) with 0.5 has the bands from %.4f to %.4f and no imaginary hopping, '
          'and (1, 2) from %.4f to %.4f; a hexagon has the right flux everywhere with 1 flux quantum per rotated cell and with 2 per '
          'cell of the other orientation, and not with 1/2 and 1' % (-fsq[1][np.argmax(np.abs(fsq[1] + 0.013))], span[(2, 1)][0],
                                                                    span[(2, 1)][1], span[(1, 2)][0], span[(1, 2)][1]))
    hd = g20.get_hamiltonian(has_spin=False); hd.add_orbital_magnetic_field(0.02)
    en = np.linspace(-4.5, 4.5, 1801)
    _, d1 = hd.get_dos(energies=en, delta=1e-2, nk=400)
    _, d2 = hd.get_dos(energies=en, delta=1e-2, nk=400, operator="bulk")
    tot, blk = np.trapezoid(d1, en), np.trapezoid(d2, en)
    win = (en > -4) & (en < -3.3)
    pk = [en[i] for i in range(1, len(en) - 1) if win[i] and d2[i] > d2[i - 1] and d2[i] >= d2[i + 1] and d2[i] > 0.2 * d2[win].max()]
    lat = harper_bottom(50, 3) - 4
    hds = g20.get_hamiltonian(); hds.add_orbital_magnetic_field(0.02)     # the spinful default
    tot_s = np.trapezoid(hds.get_dos(energies=en, delta=1e-2, nk=400)[1], en)
    check('h.get_dos of a ribbon', abs(tot - 19.96) < 0.005 and abs(blk - 15.97) < 0.005 and np.allclose(pk, [-3.875, -3.630, -3.395], atol=1e-3)
          and np.allclose(lat, [-3.876, -3.633, -3.397], atol=1e-3) and abs(tot_s - 39.92) < 0.01 and abs(tot_s - 2 * tot) < 1e-6,
          'with delta=1e-2 and nk=400 the integral over -4.5 to 4.5 is %.2f, the 20 sites of the cell less the tails of the Lorentzians, '
          'and %.2f with the spinful default, and %.2f with operator="bulk", the middle 80 percent of the width, whose peaks %s '
          'are the levels %s of the lattice'
          % (tot, tot_s, blk, ' '.join('%.3f' % p for p in pk), ' '.join('%.3f' % p for p in lat)))
    ga20 = geometry.honeycomb_armchair_ribbon(20)
    hl = ga20.get_hamiltonian(has_spin=False); hl.add_orbital_magnetic_field(0.01)
    lBh = 1 / np.sqrt(2 * np.pi * 0.01)
    frac = []
    for ew in np.linspace(0., 0.53, 4):
        xl, yl, dl = (np.array(a) for a in hl.get_ldos(e=ew, nrep=20, delta=1e-2, nk=50))
        ed = np.abs(yl - yl.mean()) > np.ptp(yl) / 2 - lBh
        frac.append(dl[ed].sum() / dl.sum())
        if abs(ew - 0.53 / 3) < 1e-9:
            npts, share, per_cell = len(xl), ed.mean(), dl.sum() / 20
    _, dd = hl.get_dos(energies=np.array([0.53 / 3]), delta=1e-2, nk=50)
    check('h.get_ldos of a ribbon', npts == 1600 and abs(per_cell - dd[0]) < 1e-3 * dd[0] and abs(share - 0.25) < 0.01
          and np.allclose(frac, [0.04, 0.57, 0.54, 0.16], atol=0.006),
          'the armchair ribbon of 20 with the field 0.01 and nrep=20 gives %d points, 20 cells of 80 sites, the sum over one cell is the '
          'density of states %.3f, and the %.0f percent of the sites within l_B = 4 of an edge hold %.0f, %.0f, %.0f and %.0f percent of the '
          'weight at E = 0, 0.177, 0.353 and 0.53' % (npts, dd[0], 100 * share, *(100 * np.array(frac))))
    hsq = geometry.square_lattice().get_hamiltonian(has_spin=False)
    gen = hsq.get_hk_gen()
    eG, eM = np.linalg.eigvalsh(D(gen([0, 0, 0])))[0], np.linalg.eigvalsh(D(gen([0.5, 0.5, 0])))[0]
    gq = geometry.square_lattice().get_supercell((1, 10))
    lvs = []
    for tij in (None, [-1.0]):
        hh = gq.get_hamiltonian(has_spin=False) if tij is None else gq.get_hamiltonian(has_spin=False, tij=tij)
        hh.add_orbital_magnetic_field(0.1)
        lvs.append(np.sort(np.linalg.eigvalsh(pc.from_pyqula(hh)[0](np.array([0.0, 0.0])))))
    g30 = geometry.square_ribbon(30)
    s1, s2 = g30.get_hamiltonian(has_spin=False), g30.get_hamiltonian()
    s1.add_orbital_magnetic_field(0.03); s2.add_orbital_magnetic_field(0.03)
    e1_, e2_ = np.linalg.eigvalsh(D(s1.get_hk_gen()([0.2, 0, 0]))), np.linalg.eigvalsh(D(s2.get_hk_gen()([0.2, 0, 0])))
    check('the spin and the sign of the hopping in the notebook', abs(eM + 4) < 1e-12 and abs(eG - 4) < 1e-12 and np.allclose(lvs[0], lvs[1])
          and np.allclose(e2_, np.repeat(e1_, 2)),
          'the default hopping +1 of square_lattice() puts the band bottom %+.0f at M and %+.0f at Gamma, the levels in the field 0.1 are '
          'the same for the hopping +1 and -1, and the default spinful ribbon has every level of the spinless one twice' % (eM, eG))

    # ---------------------------------------------------------------- the lattice against the continuum
    err, rel = [], {n: [] for n in range(6)}
    for q in (40, 60, 100):
        n = np.arange(4)
        err.append(np.abs(harper_bottom(q, 4) - (4 * np.pi / q * (n + 0.5) - (np.pi / q) ** 2 * (2 * n * n + 2 * n + 1) / 2)).max())
    for q in list(range(6, 200)) + list(range(200, 600, 20)):
        e = np.linalg.eigvalsh(square_cell(q)[0](np.zeros(2)))[:6] + 4 if q < 200 else harper_bottom(q, 6)
        for n in range(6):
            c = 4 * np.pi / q * (n + 0.5)
            if c < 1.6:
                rel[n].append((c, 1 - e[n] / c))
    eps5 = []
    for n in range(6):
        a = np.array(sorted(rel[n]))
        eps5.append(np.interp(0.05, a[:, 1], a[:, 0]))
    small = [np.array(sorted(rel[n]))[0] for n in (0, 1, 5)]
    ok = err[0] < 2e-3 and err[1] < 6e-4 and err[2] < 1.5e-4 and abs(eps5[0] - 0.41) < 0.01 and abs(eps5[1] - 0.73) < 0.01 and all(0.77 < e_ < 0.82 for e_ in eps5[2:])
    ok = ok and abs(small[0][0] / small[0][1] - 8) < 0.1 and abs(small[1][0] / small[1][1] - 14.4) < 0.2 and abs(small[2][0] / small[2][1] - 15.9) < 0.3
    check('the square lattice against (4.6)', ok,
          'the second-order form holds to %s for the flux 1/40, 1/60, 1/100 and n <= 3, the relative error is eps/%.1f t, eps/%.1f t and '
          'eps/%.1f t for n = 0, 1, 5 at small eps, and it reaches 5 percent at eps = %s t above the band bottom for n = 0 to 5'
          % (', '.join('%.0e' % e_ for e_ in err), *(s_[0] / s_[1] for s_ in small), ', '.join('%.2f' % e_ for e_ in eps5)))
    hk20, B20 = square_cell(20)
    es20 = np.array([np.linalg.eigvalsh(hk20(k))[:4] for k in pc.kmesh(B20, 6)])
    c20 = -4 + 4 * np.pi / 20 * (np.arange(4) + 0.5)
    sh = c20 - es20.mean(0)
    check('the levels of landau_chern.py', np.allclose(sh, [0.012, 0.060, 0.155, 0.295], atol=1e-3) and np.allclose(sh / (4 * np.pi / 20), [0.02, 0.10, 0.25, 0.47], atol=0.005)
          and np.ptp(es20, axis=0).max() < 1e-4,
          'at the flux 1/20 the four lowest bands sit %s t below their dashed lines, %s of the spacing 0.628 t, and they are flat to %.0e'
          % (' '.join('%.3f' % a for a in sh), ' '.join('%.2f' % a for a in sh / (4 * np.pi / 20)), np.ptp(es20, axis=0).max()))
    import json, re
    nb = json.load(open(os.path.join(WEBNOTES, '..', 'jupyter-notebooks', 'session4.ipynb'), encoding='utf-8'))
    cells, title = {}, None
    for c in nb['cells']:
        src = ''.join(c['source'])
        if c['cell_type'] == 'markdown':
            m_ = re.search(r'^#+\s*(.*)', src, re.M)
            title = m_.group(1) if m_ else title
        elif title is not None:
            cells.setdefault(title, src)
    cell = lambda name: next(v for k, v in cells.items() if k.startswith(name))
    nbok = (re.search(r'^N = 30\b', cell('Landau levels of conventional electrons'), re.M) is not None
            and re.search(r'^W = 20\b', cell('Magnetic field dependence of Landau levels'), re.M) is not None
            and re.search(r'^W = 40\b', cell('Bands in the conventional quantum Hall state'), re.M) is not None
            and all('Bs = [0.02,0.03,0.04]' in cell(n) and 'square_ribbon(' in cell(n) for n in
                    ('Landau levels of conventional electrons', 'Magnetic field dependence of Landau levels'))
            and re.search(r'^B = 0\.02\b', cell('Bands in the conventional quantum Hall state'), re.M) is not None)
    spc = {}
    for W in (20, 30, 40):
        gw = geometry.square_ribbon(W)
        spc[W] = []
        for phi in (0.02, 0.03, 0.04):
            hh = gw.get_hamiltonian(has_spin=False); hh.add_orbital_magnetic_field(phi)
            e, v = np.linalg.eigh(D(hh.get_hk_gen()([0.5, 0, 0])))
            mid = np.abs((np.abs(v) ** 2).T @ gw.y) < 2
            lv = e[mid & (e < -3)][:2]
            spc[W].append(lv[1] - lv[0])
    ok = np.allclose(spc[20], [0.2436, 0.3595, 0.4717], atol=2e-4) and all(np.allclose(spc[W], spc[20], atol=2e-4) for W in (30, 40))
    ok = ok and np.allclose([1 / np.sqrt(2 * np.pi * p) for p in (0.02, 0.03, 0.04)], [2.8, 2.3, 2.0], atol=0.03) and nbok
    check('the square ribbons of the notebook', ok and abs(spc[20][2] / spc[20][0] - 1.94) < 0.005,
          'the notebook has the ribbons of 30 and 20 sites with the field 0.02, 0.03, 0.04 and the one of 40 with 0.02 (%s); on the '
          'ribbons of 20, 30 and 40 sites the two lowest levels are %s, %s and %s apart for the field 0.02, 0.03, 0.04, a ratio %.2f from '
          '0.02 to 0.04, against 4 pi phi = 0.251, 0.377, 0.503, and l_B = %.1f, %.1f, %.1f sites'
          % (nbok, ' '.join('%.4f' % a for a in spc[20]), ' '.join('%.4f' % a for a in spc[30]), ' '.join('%.4f' % a for a in spc[40]),
             spc[20][2] / spc[20][0], *(1 / np.sqrt(2 * np.pi * p) for p in (0.02, 0.03, 0.04))))
    cs_, deg_ = [], []
    for n_ in (40, 20):
        g = rot(n_)
        phi = 1 / area(g)
        hh = g.get_hamiltonian(has_spin=False); hh.add_orbital_magnetic_field(phi)
        e = np.sort(np.linalg.eigvalsh(pc.from_pyqula(hh)[0](np.array([0.07, 0.03]))))
        mm = len(e) // 2
        lv = np.array([e[mm + 1:mm + 3].mean(), e[mm + 3:mm + 5].mean()])
        cont = 3 * np.sqrt(np.pi * phi * np.array([1, 2]))
        cs_ += list((1 - lv / cont) / lv ** 2)
        deg_.append(np.sum(np.abs(e) < 0.05) == 2 and np.sum(np.abs(e - lv[0]) < 0.02) == 2)
    ga40 = geometry.honeycomb_armchair_ribbon(40)
    rib1, spread = [], []
    for phi in (0.005, 0.01, 0.02):
        E1c = 3 * np.sqrt(np.pi * phi)
        ens, spr = central_level(ga40, phi, (0.85 * E1c, 1.05 * E1c))
        rib1.append(np.mean(ens)); spread.append((np.ptp(ens), spr.max()))
    g10 = rot(10)                                                  # one flux quantum, phi = 0.0192
    hh = g10.get_hamiltonian(has_spin=False); hh.add_orbital_magnetic_field(1 / area(g10))
    hk10, B10 = pc.from_pyqula(hh)
    e10 = np.array([np.linalg.eigvalsh(hk10(k))[21:23] for k in pc.kmesh(B10, 6)])
    band = (e10.min(), e10.max())
    ok = all(deg_) and 0.085 < min(cs_) and max(cs_) < 0.105 and np.allclose(rib1, [0.3715, 0.5185, 0.7114], atol=5e-4) and abs(rib1[2] / rib1[0] - 1.92) < 0.005
    ok = ok and all(p_[0] < 1e-3 for p_ in spread) and spread[1][1] < 1e-3 and 0.004 < spread[2][1] < 0.008 and 0.69 < band[0] < 0.695 and 0.705 < band[1] < 0.71 and abs(band[1] - band[0] - 0.017) < 0.001
    check('the honeycomb lattice against (4.7)', ok,
          'with bond 1 the cell with one flux quantum has two states in the zero level and two in the first one, the lattice levels are '
          'below sqrt(|n|) E_1 = 3 sqrt(pi phi |n|) t by c (E/t)^2 of their energy with c from %.3f to %.3f, and the armchair ribbon of 40 '
          'has E_1 = %.4f, %.4f, %.4f for the field 0.005, 0.01, 0.02, a ratio %.2f, against 0.376, 0.532, 0.752; at 0.02 a state at one '
          'guiding center has the energy spread %.4f, and the cell with phi = 0.0192 has its first level from %.3f to %.3f, so the lattice '
          'broadens the level there' % (min(cs_), max(cs_), *rib1, rib1[2] / rib1[0], spread[2][1], *band))

    # ---------------------------------------------------------------- the two gauges
    Ls = lambda X, Y: (0.0, X)
    Sy = lambda X, Y: (-Y / 2, X / 2)
    corners = [(2, 1), (3, 1), (3, 2), (2, 2)]
    tt = np.linspace(0, 1, 101)
    ph = []
    for A in (Ls, Sy):
        ph.append([np.trapezoid([np.dot(A(a[0] + s * (b[0] - a[0]), a[1] + s * (b[1] - a[1])), (b[0] - a[0], b[1] - a[1])) for s in tt], tt)
                   for a, b in zip(corners, corners[1:] + corners[:1])])
    L_ = 10
    Hl_, Hs_ = np.zeros((L_ * L_, L_ * L_), complex), np.zeros((L_ * L_, L_ * L_), complex)
    Bf = 2 * np.pi * 0.06
    for i in range(L_ * L_):
        xi, yi = divmod(i, L_)
        for j, (xj, yj) in ((i + L_, (xi + 1, yi)), (i + 1, (xi, yi + 1))):
            if xj < L_ and yj < L_:
                xm, ym = (xi + xj) / 2, (yi + yj) / 2
                Hl_[j, i] = -np.exp(1j * Bf * xm * (yj - yi)); Hs_[j, i] = -np.exp(1j * Bf * (-ym * (xj - xi) + xm * (yj - yi)) / 2)
    Hl_ += Hl_.conj().T; Hs_ += Hs_.conj().T
    check('the Landau and the symmetric gauge', np.allclose(ph[0], [0, 3, 0, -2]) and np.allclose(ph[1], [-0.5, 1.5, 1, -1])
          and np.allclose(np.linalg.eigvalsh(Hl_), np.linalg.eigvalsh(Hs_), atol=1e-10),
          'the bond phases of the plaquette with the corner (2, 1), counterclockwise in units of its flux, are %s and %s, both with the '
          'sum 1, and a 10 x 10 island has the same levels in both gauges to 1e-10' % (' '.join('%+.1f' % p for p in ph[0]), ' '.join('%+.1f' % p for p in ph[1])))

    # ---------------------------------------------------------------- the Laughlin state
    rd = np.linspace(0, 12.5, 2501)
    full = 2 * np.pi * sum(orbital_density(m, rd) for m in range(20))
    third = 2 * np.pi * sum(orbital_density(3 * m, rd) for m in range(20))
    flat = np.abs(full[rd < np.sqrt(40) - 2] - 1).max()
    halfr = rd[np.argmin(np.abs(full - 0.5))]
    radii = [np.sqrt(2 * (n - 1)) for n in (26, 52, 100, 200)]
    check('the filled lowest level', flat < 0.002 and abs(halfr - 6.27) < 0.01 and np.allclose(radii, [7.07, 10.10, 14.07, 19.95], atol=0.005),
          'the orbitals m = 0 to 19 give the filling 1 within %.4f up to sqrt(2N) - 2 l_B and 1/2 at %.2f l_B, against sqrt(2N) = %.2f, and '
          'sqrt(2(N-1)) is %.2f, %.2f, %.2f, %.2f l_B for N = 26, 52, 100, 200' % (flat, halfr, np.sqrt(40), *radii))
    sel = (rd > 2) & (rd < np.sqrt(120) - 2)
    check('every third orbital', abs(third[sel].min() - 0.324) < 0.001 and abs(third[sel].max() - 0.333) < 0.001 and abs(third[0] - 1) < 1e-12,
          'the orbitals m = 0, 3, ..., 57 give the filling between %.3f and %.3f for 2 l_B < r < sqrt(6N) - 2 l_B, and %.2f at the center'
          % (third[sel].min(), third[sel].max(), third[0]))
    gg = np.linspace(-9, 9, 721)
    XX, YY = np.meshgrid(gg, gg)
    pair = []
    for m in (1, 3, 5):
        rr = np.linspace(0.05, 14, 1400)
        wgt = np.array([(np.exp(-(np.abs(XX + 1j * YY + r_ / 2) ** 2 + np.abs(XX + 1j * YY - r_ / 2) ** 2) / 2)).sum() * r_ ** (2 * m + 1) for r_ in rr[::20]])
        form = rr[::20] ** (2 * m + 1) * np.exp(-rr[::20] ** 2 / 4)
        pform = rr ** (2 * m + 1) * np.exp(-rr ** 2 / 4)
        pair.append((np.ptp(wgt / form) / np.mean(wgt / form), rr[np.argmax(pform)]))
    check('two electrons in the state (z1 - z2)^m', all(p[0] < 1e-9 for p in pair) and np.allclose([p[1] for p in pair], np.sqrt([6, 14, 22]), atol=0.01),
          'the integral of |Psi|^2 over the center of mass on a grid is r^(2m+1) exp(-r^2/4) to %.0e, with the maximum at %.2f, %.2f, %.2f l_B '
          'for m = 1, 3, 5' % (max(p[0] for p in pair), *(p[1] for p in pair)))
    zs = sp.symbols('z1:5')
    lap = lambda Nn, mm: sp.prod([(zs[i] - zs[j]) ** mm for i in range(Nn) for j in range(i + 1, Nn)])
    degs = [sp.Poly(sp.expand(lap(Nn, 3)), zs[0]).degree() for Nn in (3, 4)]
    swap = lambda e_: e_.subs({zs[0]: zs[1], zs[1]: zs[0]}, simultaneous=True)
    anti = sp.expand(swap(lap(3, 3)) + lap(3, 3)) == 0 and sp.expand(swap(lap(3, 2)) - lap(3, 2)) == 0
    dq = sp.Poly(sp.expand(lap(4, 3) * sp.prod(zs[:4])), zs[0]).degree()
    zr = np.random.default_rng(5).normal(size=6) + 1j * np.random.default_rng(6).normal(size=6)
    vdm = np.linalg.det(np.vander(zr, increasing=True)) / np.prod([zr[j] - zr[i] for i in range(6) for j in range(i + 1, 6)])
    check('the counting of the Laughlin state', degs == [6, 9] and anti and dq == 10 and abs(vdm - 1) < 1e-12,
          'the highest power of z1 in prod (z_i - z_j)^3 is %d for N = 3 and %d for N = 4, m(N-1), m = 3 is antisymmetric and m = 2 '
          'symmetric, prod z_i raises the highest power to %d, and det(z_i^(j-1)) = prod_(i<j) (z_j - z_i) holds to %.0e at 6 random points'
          % (degs[0], degs[1], dq, abs(vdm - 1)))
    R = np.arange(0.5, 10.01, 0.5)
    e_ = np.linspace(0, 14, 57); shl = np.pi * (e_[1:] ** 2 - e_[:-1] ** 2); rc = (e_[1:] + e_[:-1]) / 2
    fill, bump, Q = [], [], []
    for s in (1, 2):
        a, rs, _ = metropolis(20, 3, [], s)
        b, _, _ = metropolis(20, 3, [0j], s + 50)
        nu = 2 * np.pi * np.histogram(rs, e_)[0] / (len(rs) / 20) / shl
        fill.append(nu[rc < 5].mean()); bump.append(3 * nu.max() - 1)
        Q.append(a - b)
    Q = np.array(Q)
    check('the filling of the Laughlin state', all(abs(f_ - 1 / 3) < 0.01 for f_ in fill) and np.allclose(bump, [0.32, 0.31], atol=0.006),
          'Metropolis on N = 20 electrons with m = 3, two seeds, gives the filling %.3f and %.3f for r < 5 l_B, and the largest filling, at '
          'the edge, %.0f and %.0f percent above 1/3 with bins of 0.25 l_B' % (*fill, *(100 * np.array(bump))))
    a1, _, _ = metropolis(20, 1, [], 7, nmeas=200)
    b1, _, _ = metropolis(20, 1, [0j], 8, nmeas=200)
    ex1 = gammainc(1, R ** 2 / 2) - gammainc(21, R ** 2 / 2)
    test1 = np.abs((a1 - b1) - ex1)[R <= 5].max()
    far, near_, at4 = Q[:, (R >= 5) & (R <= 8)].mean(1), Q[:, R <= 4].max(1), Q[:, np.argmin(np.abs(R - 4))]
    check('the charge of a quasihole', test1 < 0.04 and np.allclose(far, [0.325, 0.321], atol=0.003) and np.allclose(near_, 0.42, atol=0.006)
          and np.allclose(R[R <= 4][np.argmax(Q[:, R <= 4], 1)], [2.5, 3.0]) and np.all(np.abs(at4 - 1 / 3) < 0.03),
          'for m = 1 the Monte Carlo follows the exact orbital sums to %.3f up to R = 5 l_B; for m = 3 the factor prod z_i removes %.3f '
          'and %.3f electrons from the discs of radius 5 to 8 l_B, on average, and up to %.2f and %.2f inside 4 l_B, at R = %.1f and %.1f'
          % (test1, *far, *near_, *(R[R <= 4][np.argmax(Q[:, R <= 4], 1)])) + ', and %.3f and %.3f at R = 4 l_B' % tuple(at4))
    wq = 6.0 + 0j
    br = []
    for s in (3, 4):
        _, _, c1 = metropolis(20, 3, [wq], s, w=wq)
        _, _, c2 = metropolis(20, 3, [wq, 0j], s + 50, w=wq)
        br.append(c2 - c1)
    check('the braid phase', np.allclose(br, [0.289, 0.337], atol=0.003),
          'the Berry connection <sum_i Re w/(z_i - w)> of a quasihole on the loop |w| = 6 l_B grows by %.3f and %.3f, two seeds, when a '
          'second quasihole sits at the origin, so the Berry phase of the loop changes by 2 pi/3 to the noise' % tuple(br))

    # ---------------------------------------------------------------- the Haldane model and the field
    g = rot(20)
    phi = 1 / area(g)
    hh = g.get_hamiltonian(has_spin=False); hh.add_orbital_magnetic_field(phi)
    hkr, Br = pc.from_pyqula(hh)
    mm = hkr(np.zeros(2)).shape[0] // 2
    Cg = [pc.chern_links(hkr, Br, range(nf), nk=6) for nf in (mm - 1, mm + 1, mm + 3)]
    hh = g.get_hamiltonian(has_spin=False); hh.add_haldane(0.07)
    Chal = hh.get_chern(nk=8)
    check('the Haldane coupling and the field have the same sign of C', np.allclose(Cg, [-1, 1, 3], atol=1e-9) and abs(Chal - 1) < 1e-6,
          'in the rotated cell of 80 sites with one flux quantum, phi = %.5f, the gap below the zero level has C = %+.0f, the gap above it '
          '%+.0f and the gap above the first level %+.0f, and add_haldane(0.07) in the same cell has %+.3f' % (phi, *Cg, Chal))
    mid = np.abs(ga20.y) < 0.25 * np.ptp(ga20.y)
    res = {}
    for name, hal, fl, onsite in (('notebook', 0.07, 0.01, -0.2), ('haldane -0.07', -0.07, 0.01, -0.2), ('field -0.01', 0.07, -0.01, -0.2),
                                  ('onsite +0.2', 0.07, 0.01, 0.2)):
        Hq = ga20.get_hamiltonian(has_spin=False); Hq.add_orbital_magnetic_field(fl); Hq.add_onsite(onsite)
        Hc = ga20.get_hamiltonian(has_spin=False); Hc.add_haldane(hal)
        g1, g2 = Hq.get_hk_gen(), Hc.get_hk_gen()
        best = np.full(11, 9.0)
        for k in np.linspace(-0.5, 0.5, 41):
            m1, m2 = D(g1([k, 0, 0])), D(g2([k, 0, 0]))
            for i, nu in enumerate(np.linspace(0, 1, 11)):
                ev, vv = np.linalg.eigh(nu * m1 + (1 - nu) * m2)
                bulk = (np.abs(vv) ** 2)[mid].sum(0) > 0.5
                best[i] = min(best[i], np.abs(ev[bulk]).min())
        res[name] = best
    Hq = ga20.get_hamiltonian(has_spin=False); Hq.add_orbital_magnetic_field(0.01)
    mix = D((Hq * 0.5 + ga20.get_hamiltonian(has_spin=False) * 0.5).intra)
    top = int(np.argmax(ga20.y))
    nbm = sorted(abs(mix[top, j]) for j in range(len(ga20.r)) if abs(np.linalg.norm(ga20.r[j] - ga20.r[top]) - 1) < 1e-6)
    ok = res['notebook'].min() > 0.19 and all(res[k].min() < 0.03 for k in ('haldane -0.07', 'field -0.01', 'onsite +0.2'))
    ok = ok and abs(np.linspace(0, 1, 11)[np.argmin(res['haldane -0.07'])] - 0.6) < 1e-9 and abs(res['notebook'].min() - 0.198) < 0.0015
    check('the path of Section 4.19', ok and np.allclose(nbm, [0.86, 0.97], atol=0.005),
          'along nu H_QH + (1 - nu) H_C of the notebook no bulk state comes closer to zero energy than %.3f, at nu = %.1f, and the gap closes, '
          'to %.3f, %.3f and %.3f, with add_haldane(-0.07) (at nu = %.1f), with the field -0.01 and with add_onsite(+0.2); at nu = 0.5 the '
          'bonds of the edge site have the moduli %s' % (res['notebook'].min(), np.linspace(0, 1, 11)[np.argmin(res['notebook'])],
                                                          res['haldane -0.07'].min(), res['field -0.01'].min(), res['onsite +0.2'].min(),
                                                          np.linspace(0, 1, 11)[np.argmin(res['haldane -0.07'])], ' '.join('%.2f' % a for a in nbm)))
    gw = geometry.square_ribbon(80); gw.center()
    hw = gw.get_hamiltonian(has_spin=False); hw.add_orbital_magnetic_field(0.02)

    def mufun(r):                                    # the function of the notebook cell "Topological domains"
        if r[1] > 0.:
            return 3.5
        else:
            return -3.5
    hw.add_onsite(mufun)
    onw = np.diag(D(hw.intra)).real
    gen = hw.get_hk_gen()
    cnt = {'wall': 0, 'top': 0, 'bottom': 0}
    kk = np.linspace(-0.5, 0.5, 801)
    Ek, Yk = [], []
    for k in kk:
        ev, vv = np.linalg.eigh(D(gen([k, 0, 0])))
        Ek.append(ev); Yk.append((np.abs(vv) ** 2).T @ gw.y)
    Ek, Yk = np.array(Ek), np.array(Yk)
    for n in range(Ek.shape[1]):
        for j in np.where(np.diff(np.sign(Ek[:, n])) != 0)[0]:
            cnt['wall' if abs(Yk[j, n]) < 15 else ('top' if Yk[j, n] > 0 else 'bottom')] += 1
    g50 = geometry.square_lattice().get_supercell((1, 50))
    cdom = []
    for c in (3.5, -3.5):
        hq = g50.get_hamiltonian(has_spin=False); hq.add_orbital_magnetic_field(0.02); hq.add_onsite(c)
        hkd, Bd = pc.from_pyqula(hq)
        nb = int((np.linalg.eigvalsh(hkd(np.array([0.01, 0.02]))) < 0).sum())
        cdom.append(pc.chern_links(hkd, Bd, range(nb), nk=6))
    ok = np.allclose(onw[gw.y > 0], 3.5) and np.allclose(onw[gw.y < 0], -3.5) and cnt == {'wall': 4, 'top': 2, 'bottom': 2} and np.allclose(cdom, [2, -2], atol=1e-9)
    check('the domains of the notebook', ok,
          'add_onsite(mufun) gives +3.5 to the sites with y > 0, a bulk with the onsite energy +3.5 or -3.5 and the field 0.02 has C = %+.0f '
          'or %+.0f, and zero energy is crossed by %d branches at the wall and by %d at each outer edge' % (*cdom, cnt['wall'], cnt['top']))

    # ---------------------------------------------------------------- the figure scripts
    q = 20
    Cf = {}
    for sg in (1, -1):                               # the model of g1_landau_levels_square.py, which landau_chern.py draws
        hq_ = geometry.square_lattice().get_supercell((1, q)).get_hamiltonian(has_spin=False, tij=[-1.])
        hq_.add_orbital_magnetic_field(sg / q)
        hkq_, Bq_ = pc.from_pyqula(hq_)
        Cf[sg] = [pc.chern_links(hkq_, Bq_, n, nk=12) for n in range(4)]
    src_lc = open(os.path.join(WEBNOTES, 'figures', 'session04', 'landau_chern.py')).read()
    check('landau_chern.py', np.allclose(Cf[1], 1, atol=1e-9) and np.allclose(Cf[-1], -1, atol=1e-9)
          and "run_script('session04/g1_landau_levels_square.py')" in src_lc,
          'it draws g1_landau_levels_square.py, where add_orbital_magnetic_field(1/20) in the cell (1, 20), the field along -z for the '
          'charge +e, has C = %s for the four lowest bands with the Omega of Session 3, and the flux -1/20 has C = %s'
          % (' '.join('%+.0f' % c for c in Cf[1]), ' '.join('%+.0f' % c for c in Cf[-1])))
    Nx, Bh, Ly = 40, 1 / 16, S3
    cellb = np.array([[0, 0], [0, 1 / S3], [0.5, S3 / 2], [0.5, S3 / 2 + 1 / S3]])
    posb = np.array([c + [i, 0] for i in range(Nx) for c in cellb])
    bonds = []
    for n in (-1, 0, 1):
        d = np.linalg.norm(posb[:, None] - (posb[None] + [0, n * Ly]), axis=-1)
        for i, j in zip(*np.where(np.abs(d - 1 / S3) < 1e-9)):
            bonds.append((i, j, posb[i, 1] - posb[j, 1] - n * Ly))

    def hb_(ky, sign):                               # panel (b) of lattice_ribbons.py with sign=+1
        Hm_ = np.zeros((len(posb), len(posb)), complex)
        for i, j, dy in bonds:
            Hm_[i, j] += -np.exp(1j * (sign * ky + Bh * 0.5 * (posb[i, 0] + posb[j, 0])) * dy)
        return Hm_
    gcs, Ky = {}, 2 * np.pi / Ly
    for sign in (1, -1):
        xm_ = []
        for ky in Ky + sign * np.array([-1.2, -1.0]):
            e, v = np.linalg.eigh(hb_(ky, sign))
            xm_.append(np.abs(v[:, np.argmin(np.abs(e))]) ** 2 @ posb[:, 0])
        gcs[sign] = (xm_[1] - xm_[0]) / (0.2 * sign) * Bh
    hsa = lambda k: np.diag(-2 * np.cos(k - 2 * np.pi / 60 * np.arange(30))) - np.eye(30, k=1) - np.eye(30, k=-1)
    xa = [np.abs(np.linalg.eigh(hsa(k))[1][:, 0]) ** 2 @ np.arange(30) for k in (1.0, 1.2)]
    ga_ = (xa[1] - xa[0]) / 0.2 * (2 * np.pi / 60)
    check('lattice_ribbons.py', abs(gcs[1] + 1) < 0.02 and abs(gcs[-1] - 1) < 0.02 and abs(ga_ - 1) < 0.02,
          'panel (a), -2 cos(k_y - B x), has the guiding center moving as %+.2f/B with k_y, the field +B z with k_y the momentum; panel (b) '
          'has the phase (4.4) of the field +B z and the Bloch phase exp(+i k_y (y_i - y_j)), and its guiding center moves as %+.2f/B, '
          'and %+.2f/B with the Bloch phase of (a), so its k_y is minus the momentum' % (ga_, gcs[1], gcs[-1]))
    ks48 = np.arange(48) / 48
    Bv = pc.reciprocal([hc.a1, hc.a2])
    rows, same = [], []
    for (t2_, ph_, t3_, M_) in ((0.1, np.pi / 2, 0., 0.), (0.3, 0.4 * np.pi, -0.2, 0.), (0.2, 0., 0., 1.5)):
        hh_ = gh.get_hamiltonian(has_spin=False, tij=[1., t2_ * np.cos(ph_), t3_])    # the models of g5_haldane_t3_bands.py
        hh_.add_haldane(2 * t2_ * np.sin(ph_) / S3)
        hh_.add_sublattice_imbalance(M_)
        hkg = hh_.get_hk_gen()
        Eg = np.array([np.linalg.eigvalsh(hkg([a, b, 0.])) for a in ks48 for b in ks48])
        hk_, B_ = pc.from_pyqula(hh_)
        rows.append((np.ptp(Eg[:, 0]), Eg[:, 1].min() - Eg[:, 0].max(), pc.chern_links(hk_, B_, 0, nk=24), hh_.get_chern(nk=40),
                     2 * t2_ * np.sin(ph_) / S3, t2_ * np.cos(ph_)))
        e_hc = np.sort(np.concatenate([np.linalg.eigvalsh(hc.bloch(a * Bv[0] + b * Bv[1], t2=t2_, phi=ph_, t3=t3_, M=M_))
                                       for a in ks48[::2] for b in ks48[::2]]))
        e_pq = np.sort(np.concatenate([np.linalg.eigvalsh(hkg([a, b, 0.])) for a in ks48[::2] for b in ks48[::2]]))
        same.append(np.abs(e_hc - e_pq).max())
    src_fc = open(os.path.join(WEBNOTES, 'figures', 'session04', 'flat_chern_band.py')).read()
    ok = all(abs(r_[2] - 1) < 1e-9 and abs(r_[3] - 1) < 1e-6 for r_ in rows[:2]) and "session04/g5_haldane_t3_bands.py" in src_fc
    ok = ok and round(rows[0][4], 4) == 0.1155 and round(rows[1][4], 4) == 0.3295 and round(rows[1][5], 4) == 0.0927
    ok = ok and abs(rows[0][0] - 2.48) < 0.005 and abs(rows[0][1] - 1.04) < 0.005 and abs(rows[1][0] - 0.212) < 0.0005
    ok = ok and abs(rows[1][1] - 2.97) < 0.005 and round(rows[1][1] / rows[1][0], 1) == 14.0
    check('flat_chern_band.py', ok,
          'it draws g5_haldane_t3_bands.py, add_haldane(%.4f) and tij=[1, %.4f, -0.2] with add_haldane(%.4f), with C = %+.0f and %+.0f '
          'from the links and %+.0f and %+.0f from get_chern; the widths are %.2f and %.3f and the gaps %.2f and %.2f, a ratio %.1f in (b)'
          % (rows[0][4], rows[1][5], rows[1][4], rows[0][2], rows[1][2], rows[0][3], rows[1][3], rows[0][0], rows[1][0], rows[0][1],
             rows[1][1], rows[1][1] / rows[1][0]))
    same_h = []
    for xh in (0.05, 0.1, 0.1155, 0.2):
        hh_ = gh.get_hamiltonian(has_spin=False); hh_.add_haldane(xh)
        hkg = hh_.get_hk_gen()
        e_pq = np.sort(np.concatenate([np.linalg.eigvalsh(hkg([a, b, 0.])) for a in ks48[::2] for b in ks48[::2]]))
        e_hc = np.sort(np.concatenate([np.linalg.eigvalsh(hc.bloch(a * Bv[0] + b * Bv[1], t2=xh * S3 / 2, phi=np.pi / 2))
                                       for a in ks48[::2] for b in ks48[::2]]))
        same_h.append(np.abs(e_hc - e_pq).max())
    check('tij=[1, a, b] and add_haldane(c) of pyqula against _honeycomb.bloch', max(same_h + same) < 2e-15 + 1e-15,
          'the spectra on a mesh of the zone agree to %.0e for add_haldane of 0.05, 0.1, 0.1155 and 0.2 alone, and to %.0e for the '
          'three models of g5_haldane_t3_bands.py, with a = t2 cos phi, b = t3 and c = 2 t2 sin phi/sqrt 3' % (max(same_h), max(same)))
    check('the flat band with C = 0', abs(rows[2][0] - 0.200) < 5e-4 and abs(rows[2][1] - 3.000) < 5e-4 and abs(rows[2][2]) < 1e-9
          and abs(rows[2][3]) < 1e-6,
          'the real t2 = 0.2 with add_sublattice_imbalance(1.5) has the width %.3f, the gap %.3f and C = %.0f' % (rows[2][0], rows[2][1], abs(rows[2][2])))
    xb = np.linspace(0.1, 1.55, 145001)
    Rb = 1 / sum(0.5 * (1 + np.tanh((1 / xb - (n - 0.5)) / 0.05)) for n in range(1, 40))
    plat = []
    for N in (1, 2, 3):
        on_ = np.abs(Rb - 1 / N) < 1e-3
        plat.append((xb[on_].min(), xb[on_].max(), 0.5 * (xb[on_].min() + xb[on_].max()), 0.5 * (1 / xb[on_].min() + 1 / xb[on_].max())))
    ok = all(abs(p[3] - N) < 1e-3 for p, N in zip(plat, (1, 2, 3))) and abs(plat[0][2] - 1.12) < 0.005 and abs(plat[1][2] - 0.517) < 0.002 and abs(plat[2][2] - 0.339) < 0.002
    hw2 = 0.5 * (1 / plat[1][0] - 1 / plat[1][1])
    check('plateaus.py', ok and abs(hw2 - 0.36) < 0.01,
          'the flat part of the plateau N spans the filling N - %.2f to N + %.2f, its middle in 1/B is %.3f, %.3f, %.3f, where the classical '
          'line crosses it, and its middle in B is %.3f, %.3f, %.3f against the crossing at 1, 0.5, 0.333' % (hw2, hw2, *(p[3] for p in plat), *(p[2] for p in plat)))
    wall = oscillator_wall([3.0, 1.0, 0.0])[:, 0]
    exact = [brentq(lambda En: pbdv(En - 0.5, -np.sqrt(2) * x0)[0], lo, hi) for x0, lo, hi in ((3.0, 0.45, 1.0), (1.0, 0.5, 1.2), (0.0, 1.2, 1.8))]
    x12 = np.linspace(0, 12, 1202)[1:-1]; h12 = x12[1] - x12[0]
    kk = np.linspace(-3.5, 15.5, 381)
    E12 = np.array([eigh_tridiagonal(1 / h12 ** 2 + 0.5 * (x12 - k) ** 2, -0.5 / h12 ** 2 * np.ones(len(x12) - 1), select='i', select_range=(0, 5))[0] for k in kk])
    cross = {mu: int(np.sum(np.diff(np.sign(E12 - mu), axis=0) != 0)) for mu in (2.0, 3.0)}
    check('wall_squeeze.py and ribbon_three.py', np.allclose(wall, exact, atol=2e-3) and np.allclose(exact, [0.5002, 0.7342, 1.5], atol=2e-4)
          and cross == {2.0: 4, 3.0: 6},
          'a hard wall at 3, 1 and 0 l_B from the center of the well gives the lowest level %.3f, %.3f, %.3f hbar omega_c, and the zero of '
          'the parabolic cylinder function %.4f, %.4f, %.4f; the ribbon of 12 l_B has %d crossings at mu = 3 and %d at mu = 2 hbar omega_c'
          % (*wall, *exact, cross[3.0], cross[2.0]))
    Hm, pos = island(14, 1 / 16, -1)                   # the charge +e in a field into the page
    e, v = np.linalg.eigh(Hm)
    st = v[:, np.argmin(np.abs(e - (-4 + 4 * np.pi / 16)))]
    jt = sum(2 * np.imag(np.conj(st[a + 14]) * Hm[a + 14, a] * st[a]) for a in range(len(pos)) if pos[a, 0] + 1 < 14 and pos[a, 1] > 6.5)
    check('hall_setup.py', abs(jt - 0.196) < 5e-4 and abs(cur[1][0] + 0.196) < 5e-4,
          'with the field into the page the charge +e carries %+.3f along x in the upper half of the island, clockwise, and an electron '
          'carries the opposite, counterclockwise as the figure draws it' % jt)

    # ---------------------------------------------------------------- the open points of the old text, settled on 2026-11-22
    hk10_, B10_ = square_cell(10)
    hkm10, Bm10 = square_cell(10, s=-1)
    cpl, cmi = pc.chern_links(hk10_, B10_, 0, nk=10), pc.chern_links(hkm10, Bm10, 0, nk=10)
    check('Sections 4.4, 4.14 and 4.21, "C = 1" for every level', abs(cpl + 1) < 1e-9 and abs(cmi - 1) < 1e-9,
          'the lowest level of the flux 1/10 has C = %+.0f for the charge +e in the field +B z of Sections 4.8 and 4.9, and %+.0f for an '
          'electron, so "C = 1" is |C| or the sign of an electron' % (cpl, cmi))
    check('Section 4.9, "nothing else changes"', lll[(-1, 'zbar', 3)][0] == half and dirac[-1][1] < 1e-9 and abs(Cm12 - 1) < 1e-9,
          'for the charge -e the lowest level is zbar^m G with L_z = %s hbar for m = 3, the Dirac zero mode has the weight %.0f in the upper '
          'component, and C is %+.0f per level' % (lll[(-1, 'zbar', 3)][1], dirac[-1][1], Cm12))
    check('Section 4.2 and hall_setup.py, the geometry', jt > 0 and np.allclose(drift, -1, atol=1e-3),
          'a current along x for a voltage along y is +N e^2/h when qB > 0, the opposite order of (3.4), and the charge +e with the field '
          'into the page goes around clockwise, %+.3f along x in the upper half, while the figure draws counterclockwise arrows' % jt)
    g10t = 1e6 * np.sqrt(2 * HBAR * E * 10) / E * 1e3
    s10t = HBAR * E * 10 / (0.067 * ME) / E * 1e3
    check('Sections 4.1 and 4.10, the energy scales', abs(g10t / s10t - 6.64) < 0.01 and abs(g10t - 114.7) < 0.05 and abs(s10t - 17.28) < 0.01,
          'at 10 T the first level of graphene is %.0f meV and the spacing of GaAs %.1f meV, a factor %.1f, and not one or two orders of '
          'magnitude, and the GaAs scale is 1.73 meV per tesla' % (g10t, s10t, g10t / s10t))
    check('Section 4.16, "lumps"', np.abs(3 * third[sel] - 1).max() < 0.03,
          'every third orbital gives a density within %.1f percent of 1/3 for r > 2 l_B, so the lumps are only near the center'
          % (100 * np.abs(3 * third[sel] - 1).max()))
    check('the notebook box of Section 4.19', np.allclose(cdom, [2, -2], atol=1e-9),
          'the cell "Topological domains" has a field and the onsite energies +3.5 and -3.5, with C = %+.0f and %+.0f, and no Haldane coupling' % tuple(cdom))
    check('Section 4.19, the gap along the path', res['notebook'].min() > 0.19 and res['haldane -0.07'].min() < 0.03,
          'the gap stays open, %.3f, only with the two signs of the notebook, and it closes, %.3f, with the other sign of the Haldane coupling'
          % (res['notebook'].min(), res['haldane -0.07'].min()))
    check('the caption of plateaus', abs(plat[0][2] - 1.12) < 0.005,
          'in B the classical line crosses the plateau N = 1 at 1.00, and the middle of its flat part is at %.2f' % plat[0][2])
    print('%d checks hold, %.1f s' % (COUNT[0], time.time() - t0))


if __name__ == '__main__':
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            main()
        finally:
            os.chdir(cwd)
