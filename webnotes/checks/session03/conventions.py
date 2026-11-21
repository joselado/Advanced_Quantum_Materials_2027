"""Checks of webnotes/conventions/session03.md, with numbers. Every statement of the sheet that a short calculation
reproduces is asserted here, in the order of the sheet. It prints one line per check and exits 0 when all hold.

Not asserted, since they are not a short calculation or not a number: the two other routes to the sign of sigma_xy
(the strip with a potential, the Hofstadter band against the classical drift), the decision of the lecturer on (3.4),
what style.pyqula_kmap draws, what berry_haldane.py and haldane_phase.py printed before 2026-11-21, and the open
point on the number of Dirac points of Section 3.10. The field of a ribbon is checked on the square lattice only,
and not on the triangular ribbon of Section 3.6, where the plaquette is not defined by the sheet.

Run it from anywhere:  python3 webnotes/checks/session03/conventions.py"""
import os, sys, tempfile, time
import numpy as np

WEBNOTES = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(WEBNOTES, 'figures'))
sys.path.insert(0, os.path.join(WEBNOTES, 'figures', 'session03'))
import physcheck as pc
import _honeycomb as hc

EX, EY = np.array([1.0, 0.0]), np.array([0.0, 1.0])
COUNT = [0]


def check(name, ok, detail):
    """Prints one line for a check and stops the script when it does not hold."""
    print(('ok    ' if ok else 'FAIL  ') + name + ': ' + detail, flush=True)
    assert ok, name
    COUNT[0] += 1


def literal(hk, k, n, h=1e-4):
    """Omega_n = -2 Im <d_kx u_n|d_ky u_n> from finite differences of the eigenvector, in the gauge where the overlap
    with the eigenvector at k is real and positive, which is smooth around k."""
    u0 = np.linalg.eigh(hk(k))[1][:, n]

    def u(q):
        v = np.linalg.eigh(hk(q))[1][:, n]
        return v * np.exp(-1j * np.angle(np.vdot(u0, v)))
    dx = (u(k + h * EX) - u(k - h * EX)) / (2 * h)
    dy = (u(k + h * EY) - u(k - h * EY)) / (2 * h)
    return -2 * np.imag(np.vdot(dx, dy))


def flake_bloch(t2, R=6.0):
    """The Bloch Hamiltonian of the bulk of _honeycomb.flake, built from the matrix elements of the flake around its
    central site of each sublattice, with the phases exp(i k.d) of _honeycomb.bloch, d the lattice vector between cells."""
    pts, sub, H = hc.flake(R, t2=t2)
    cell = pts - np.where(sub[:, None] == 1, hc.DELTA, 0.0)
    home = [np.argmin(np.linalg.norm(pts, axis=1) + 100 * (sub != s)) for s in (0, 1)]

    def hk(k):
        out = np.zeros((2, 2), complex)
        for s, i in enumerate(home):
            for j in np.nonzero(H[i])[0]:
                out[s, sub[j]] += H[i, j] * np.exp(1j * (k @ (cell[i] - cell[j])))
        return out
    return hk


def haldane(g, x, m=0.0, has_spin=False):
    """The pyqula honeycomb lattice with add_haldane(x) and add_sublattice_imbalance(m)."""
    h = g.get_hamiltonian(has_spin=has_spin)
    h.add_haldane(x)
    if m:
        h.add_sublattice_imbalance(m)
    return h


def anomalous_velocity(hk, k0, force=2e-3, ramp=300.0, dt=0.02):
    """A state of the lower band at k0 is evolved in time while k_y moves at the rate force, switched on slowly so
    that the state follows the band. Returns the velocity along x beyond the slope of the band, and the final k."""
    def dxH(k, s=1e-3):
        return (8 * (hk(k + s * EX) - hk(k - s * EX)) - (hk(k + 2 * s * EX) - hk(k - 2 * s * EX))) / (12 * s)
    rate = lambda t: force * np.sin(np.pi * min(t, ramp) / (2 * ramp)) ** 2
    psi = np.linalg.eigh(hk(k0))[1][:, 0]
    ky, t = k0[1], 0.0
    for i in range(int((ramp + 50) / dt)):
        e, v = np.linalg.eigh(hk(np.array([k0[0], ky + rate(t + dt / 4) * dt / 2])))
        psi = v @ (np.exp(-1j * e * dt) * (v.conj().T @ psi))
        ky += rate(t + dt / 2) * dt
        t += dt
    k = np.array([k0[0], ky])
    u = np.linalg.eigh(hk(k))[1][:, 0]
    return float(np.real(np.vdot(psi, dxH(k) @ psi) - np.vdot(u, dxH(k) @ u))), k


def main():
    """Runs every check. The pyqula calls write files, so the caller runs this in a temporary folder."""
    from pyqula import geometry, topology
    t0 = time.time()
    rng = np.random.default_rng(1)
    g = geometry.honeycomb_lattice()

    # Berry curvature, Chern number and Hall conductivity
    Bh = pc.reciprocal([hc.a1, hc.a2])
    two = lambda k: hc.bloch(k, t2=0.1)
    h4 = haldane(g, 0.1, has_spin=True)
    h4.add_rashba(0.2); h4.add_zeeman([0.0, 0.0, 0.3])
    four, B4 = pc.from_pyqula(h4)
    pts = rng.uniform(-3, 3, size=(4, 2))
    r2 = max(abs(pc.berry_curvature(two, k, n) / literal(two, k, n) - 1) for k in pts for n in range(2))
    r4 = max(abs(pc.berry_curvature(four, k, n) / literal(four, k, n) - 1) for k in pts for n in range(4))
    check('the form with no phase against the definition', r2 < 1e-6 and r4 < 1e-6,
          'largest relative difference %.0e on two bands and %.0e on four bands, at 4 points' % (r2, r4))
    k0, a = np.array([3.9, 0.35]), 1e-3
    us = [np.linalg.eigh(two(q))[1][:, 0] for q in (k0, k0 + a * EX, k0 + a * EX + a * EY, k0 + a * EY)]
    phase = np.angle(np.prod([np.vdot(us[i], us[(i + 1) % 4]) for i in range(4)]))
    om = pc.berry_curvature(two, k0 + a / 2, 0)
    check('the plaquette phase, counterclockwise', abs(phase / a ** 2 + om) < 1e-5 * abs(om),
          'phase/area %+.5f, Omega %+.5f' % (phase / a ** 2, om))
    plain, C = hc.chern(24, t2=0.1), pc.chern_kubo(two, Bh, 0, nk=24)
    check('the plaquette phases summed with no sign change', abs(plain + 1) < 1e-9 and abs(C - 1) < 1e-5,
          '_honeycomb.chern gives %+.0f where C = (1/2 pi) int Omega is %+.5f' % (plain, C))
    force = 2e-3
    v, k1 = anomalous_velocity(two, k0, force)
    om = pc.berry_curvature(two, k1, 0)
    check('sigma_xy = -(e^2/h) C for a voltage along y and a current along x', abs(v / (-force * om) - 1) < 5e-3,
          'time evolution with k_y moving at %.0e, velocity along x %+.3e, minus rate times Omega %+.3e'
          % (force, v, -force * om))

    # pyqula, the lattice
    h = g.get_hamiltonian(has_spin=False)
    a1, a2 = np.array(g.a1)[:2], np.array(g.a2)[:2]
    bond = np.linalg.norm(g.r[0] - g.r[1])
    ok = np.allclose(a1, [1.5, np.sqrt(3) / 2]) and np.allclose(a2, [-1.5, np.sqrt(3) / 2]) and abs(bond - 1) < 1e-12
    check('honeycomb_lattice', ok and abs(np.linalg.norm(a1) - np.sqrt(3)) < 1e-12,
          'a1 = (%.3f, %.3f), a2 = (%.3f, %.3f), bond length %.3f, lattice constant %.4f' % (*a1, *a2, bond, np.linalg.norm(a1)))
    tm = g.get_hamiltonian(has_spin=False, tij=[-1.0]).intra[0, 1]
    check('first-neighbor hopping', abs(h.intra[0, 1] - 1) < 1e-12 and abs(tm + 1) < 1e-12,
          'the default matrix element is %+.0f, and %+.0f with tij=[-1.]' % (h.intra[0, 1].real, tm.real))
    c1, c2 = haldane(g, 0.1).get_chern(), haldane(g, 0.1, has_spin=True).get_chern()
    check('has_spin', abs(c1 - 1) < 1e-6 and abs(c2 - 2) < 1e-6,
          'h.get_chern() is %+.4f with has_spin=False and %+.4f with the default' % (c1, c2))

    # pyqula, the Haldane coupling and the staggered potential
    out = []
    for x in (0.1, 0.05):
        h = haldane(g, x)
        hk, B = pc.from_pyqula(h)
        t2 = max(abs(t.m[0, 0]) for t in h.get_multicell().hopping)
        mass = np.linalg.eigvalsh(hk((B[0] + B[1]) / 3))[1]
        out.append((x, t2, mass, pc.gap(hk, B, 1, nk=60)))
    ok = all(abs(t2 - np.sqrt(3) / 2 * x) < 1e-12 and abs(m - 4.5 * x) < 1e-12 and abs(gp - 9 * x) < 1e-12
             for x, t2, m, gp in out)
    check('add_haldane(x)', ok, ', '.join('x=%.2f gives t2 %.4f, mass %.3f, gap %.3f' % o for o in out))
    K = np.array([4 * np.pi / 3, 0.0])
    mass, gp = np.linalg.eigvalsh(two(K))[1], pc.gap(two, Bh, 1, nk=60)
    check('_honeycomb.bloch, t2=0.1', abs(mass - 3 * np.sqrt(3) * 0.1) < 1e-12 and abs(gp - 6 * np.sqrt(3) * 0.1) < 1e-12,
          'mass %.4f, gap %.4f, C %+.5f' % (mass, gp, C))
    h = g.get_hamiltonian(has_spin=False)
    h.add_sublattice_imbalance(0.3)
    hk, B = pc.from_pyqula(h)
    on, gp = np.diag(h.intra).real, pc.gap(hk, B, 1, nk=60)
    check('add_sublattice_imbalance(m)', np.allclose(np.sort(on), [-0.3, 0.3]) and abs(gp - 0.6) < 1e-12,
          'm=0.3 gives the onsite energies %+.1f and %+.1f, gap %.3f' % (on[0], on[1], gp))
    out = []
    for m in (0.40, 0.45, 0.50):
        h = haldane(g, 0.1, m)
        hk, B = pc.from_pyqula(h)
        out.append((m, pc.gap(hk, B, 1, nk=60), pc.chern_links(hk, B, 0, nk=48) if m != 0.45 else np.nan, h.get_chern()))
    ok = abs(out[0][1] - 0.1) < 1e-9 and out[1][1] < 1e-9 and abs(out[2][1] - 0.1) < 1e-9
    ok = ok and abs(out[0][2] - 1) < 1e-9 and abs(out[2][2]) < 1e-9 and abs(out[0][3] - 1) < 1e-6 and abs(out[2][3]) < 1e-6
    check('the closing at imbalance 0.45 with add_haldane(0.1)', ok,
          ', '.join('m=%.2f gap %.3f' % o[:2] for o in out) + ', C goes from %.0f to %.0f' % (abs(out[0][2]), abs(out[2][2])))

    # pyqula, the Chern number and the Berry curvature map
    h = haldane(g, 0.1)
    hk, B = pc.from_pyqula(h)
    ck, cp = pc.chern_kubo(hk, B, 0, nk=24), h.get_chern()
    cm = haldane(g, -0.1).get_chern()
    check('h.get_chern()', abs(ck - 1) < 1e-4 and abs(cp - 1) < 1e-6 and abs(cm + 1) < 1e-6,
          '%+.5f for add_haldane(0.1), the form with no phase on h.get_hk_gen() gives %+.5f, and %+.5f for -0.1'
          % (cp, ck, cm))
    N = 60
    kx, ky, b = h.get_berry_curvature(nk=N)
    kx, ky, b = np.array(kx), np.array(ky), np.array(b)
    a = np.linalg.norm(a1)
    area = abs(np.linalg.det(B))
    side = (N * (kx[N] - kx[0]), N * (ky[1] - ky[0]))
    zones = side[0] * side[1] * (2 * np.pi / a) ** 2 / area
    ok = kx[0] == kx[1] and abs(kx[0] + side[0] / 2) < 1e-12 and abs(ky[0] + side[1] / 2) < 1e-12
    # the window is a period when its two sides are reciprocal vectors
    px, py = np.linalg.solve(B.T, 2 * np.pi / a * side[0] * EX), np.linalg.solve(B.T, 2 * np.pi / a * side[1] * EY)
    ok = ok and np.allclose(px, np.round(px)) and np.allclose(py, np.round(py))
    check('get_berry_curvature, the window', ok and abs(zones - 2) < 1e-9,
          'kx from %.4f to %.4f and ky from %.1f to %.1f, the first index runs along kx, %.0f zones, a period'
          % (kx[0], kx[0] + side[0], ky[0], ky[0] + side[1], zones))
    idx = [7, 500, 1234, 3000]
    ratio = [b[i] / (area * pc.berry_curvature(hk, 2 * np.pi / a * np.array([kx[i], ky[i]]), 0)) for i in idx]
    peak = 2 * np.pi / a * np.array([kx[np.argmax(b)], ky[np.argmax(b)]])
    corner = (B[0] + B[1]) / 3
    off = min(np.linalg.norm(peak - s * corner) for s in (1, -1))
    check('get_berry_curvature, the units', max(abs(r - 1) for r in ratio) < 5e-3 and off < 2 * np.pi / a * side[1] / N,
          'b is Omega times the area of the zone at 2 pi/a times (kx, ky), ratios %s, and the peak is %.3f from a corner'
          % (' '.join('%.4f' % r for r in ratio), off))
    check('np.mean(b)/(2 pi)', abs(np.mean(b) / (2 * np.pi) - cp) < 1e-6, '%+.6f, the Chern number with its sign'
          % (np.mean(b) / (2 * np.pi)))

    # pyqula, the Hall conductivity
    mu, T = 1.0, 0.1
    s60, s120 = (float(h.get_anomalous_hall_conductivity(fermi=mu, T=T, nk=n)) for n in (60, 120))
    tot = 0.0
    for k in pc.kmesh(B, 30):
        f = 1 / (np.exp((np.linalg.eigvalsh(hk(k)) - mu) / T) + 1)
        tot += f[0] * pc.berry_curvature(hk, k, 0) + f[1] * pc.berry_curvature(hk, k, 1)
    ref = tot / 900 * area / (2 * np.pi)
    # pyqula takes the atomic gauge and physcheck the lattice gauge, which give the same Fermi sea integral here
    # only through the threefold symmetry of the honeycomb lattice
    check('get_anomalous_hall_conductivity inside a band', abs((4 * s120 - s60) / 3 - ref) < 1e-5 and abs(s120 - ref) < 5e-4,
          'mu=%.1f, T=%.1f gives %.5f at nk=60 and %.5f at nk=120, and (1/2 pi) sum int f Omega is %.5f' % (mu, T, s60, s120, ref))
    sg = float(h.get_anomalous_hall_conductivity(fermi=0.0, T=0.02, nk=60))
    check('get_anomalous_hall_conductivity in the gap', abs(sg - cp) < 1e-6, '%+.6f at mu=0, T=0.02, h.get_chern() is %+.6f' % (sg, cp))

    # pyqula, the gap
    h = g.get_hamiltonian()
    h.add_soc(0.1); h.add_rashba(0.15)
    hk, B = pc.from_pyqula(h)
    gi, gd, gq = pc.gap(hk, B, 2, nk=240), pc.gap(hk, B, 2, nk=240, direct=True), h.get_gap()
    check('the gap with spin-orbit 0.1 and Rashba 0.15, on a k-mesh', 0.435 < gi < gd < 0.455,
          '%.3f, and %.3f at one k, with nk=240, while h.get_gap() returns %.1e' % (gi, gd, gq))

    # pyqula, the field of a ribbon
    W, flux = 12, 0.07
    gr = geometry.square_ribbon(W)
    h = gr.get_hamiltonian(has_spin=False)
    h.add_orbital_magnetic_field(flux)
    gen = h.get_hk_gen()
    err = 0.0
    for k in (0.0, 0.13, 0.37, -0.21):
        harper = np.diag(2 * np.cos(2 * np.pi * (k + flux * gr.y))) + np.diag(np.ones(W - 1), 1) + np.diag(np.ones(W - 1), -1)
        err = max(err, np.abs(np.linalg.eigvalsh(harper) - np.linalg.eigvalsh(gen([k, 0.0, 0.0]))).max())
    check('the field of a ribbon', err < 1e-10,
          'square_ribbon(%d) with the field %.2f has the levels of the Harper chain 2 cos(2 pi (k + %.2f y)), to %.0e'
          % (W, flux, flux, err))

    # pyqula, the SSH chain
    gb = geometry.bichain()
    out = []
    for name in ('intra', 'inter'):
        h = gb.get_hamiltonian(has_spin=False)
        setattr(h, name, 0.5 * getattr(h, name))
        hk, G = pc.from_pyqula(h)
        hf = h.set_finite_system(n=20)
        out.append((pc.zak_phase(hk, G), topology.berry_phase(h, nk=100), np.min(np.abs(hf.get_bands()[1])), hf.intra.shape[0]))
    ok = abs(abs(out[0][1]) - np.pi) < 1e-9 and abs(out[1][1]) < 1e-9 and abs(out[0][0] - np.pi) < 1e-9 and abs(out[1][0]) < 1e-9
    check('the SSH chain, bichain with the weak hopping in h.intra or in h.inter', ok and out[0][2] < 1e-5 and out[1][2] > 0.4
          and out[0][3] == 40,
          'Zak phase %.4f and %.4f, pyqula returns %+.4f and %+.4f, the open chain of 20 cells has its lowest |E| at %.0e and %.2f'
          % (out[0][0], abs(out[1][0]), out[0][1], out[1][1], out[0][2], out[1][2]))
    signs = []
    for t in (0.1, 0.3, 0.5, 0.7, 0.9):
        for nk in (20, 50, 100, 101):
            h = gb.get_hamiltonian(has_spin=False)
            h.intra = t * h.intra
            signs.append(topology.berry_phase(h, nk=nk))
    npos, nneg = sum(s > 0 for s in signs), sum(s < 0 for s in signs)
    check('the Zak phase of pyqula is pi modulo 2 pi', all(abs(abs(s) - np.pi) < 1e-9 for s in signs),
          'topology.berry_phase returns +pi in %d and -pi in %d of %d runs with other t and nk, so the sign is rounding'
          % (npos, nneg, len(signs)))

    # the numpy helpers
    fb, kq = flake_bloch(0.1), np.array([0.7, -1.3])
    same0 = np.allclose(flake_bloch(0.0)(kq), hc.bloch(kq))
    plus, minus = np.allclose(fb(kq), hc.bloch(kq, t2=0.1)), np.allclose(fb(kq), hc.bloch(kq, t2=0.1, phi=-np.pi / 2))
    cf = pc.chern_links(fb, Bh, 0, nk=24)
    check('_honeycomb.hops and _honeycomb.flake', same0 and minus and not plus and abs(cf + 1) < 1e-9,
          'the bulk of flake(t2=0.1) is bloch(t2=0.1, phi=-pi/2), with C %+.0f where bloch(t2=0.1) has %+.0f, so the turns are opposite'
          % (cf, C))

    # the open points of the old text
    h = gb.get_hamiltonian(has_spin=False)
    gen = h.get_hk_gen()
    e_pi, e_0 = np.linalg.eigvalsh(gen([0.5, 0, 0]))[1], np.linalg.eigvalsh(gen([0.0, 0, 0]))[1]
    h.intra = -1.0 * h.intra
    gen = h.get_hk_gen()
    f_pi, f_0 = np.linalg.eigvalsh(gen([0.5, 0, 0]))[1], np.linalg.eigvalsh(gen([0.0, 0, 0]))[1]
    check('the closing of the SSH gap', e_pi < 1e-12 and e_0 > 1.9 and f_0 < 1e-12 and f_pi > 1.9,
          't=1 closes at k=pi, and t=-1 closes at k=0, so "t=1 and k=pi" holds for t>0')
    hbar, e, me, field = 1.054571817e-34, 1.602176634e-19, 9.1093837015e-31, 10.0
    graphene, gaas = 1e6 * np.sqrt(2 * e * hbar * field) / e * 1e3, hbar * e * field / (0.067 * me) / e * 1e3
    check('the Landau levels at 10 T', 6 < graphene / gaas < 7.5,
          'graphene %.0f meV with v=10^6 m/s, GaAs %.1f meV with m=0.067, a factor %.1f and not two orders of magnitude'
          % (graphene, gaas, graphene / gaas))
    print('%d checks hold, %.1f s' % (COUNT[0], time.time() - t0))


if __name__ == '__main__':
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            main()
        finally:
            os.chdir(cwd)
