"""Checks of webnotes/figures/physcheck.py, with numbers. It prints one line per check and exits 0 when all hold.

The sign of the Berry curvature is fixed here by three routes that share no code. The first is the literal definition
Omega = -2 Im <d_kx u|d_ky u> with a smooth gauge and finite differences of the eigenvector. The second is the closed
form of a two-band model, where the lower band of H = d.sigma has Omega = +(1/2) d.(d_kx d x d_ky d)/|d|^3. The third
is pyqula, whose h.get_chern() and topology.berry_phase use the same convention. The Kubo form of physcheck must agree
with the three, and the link variables with the Kubo form.

Run it from anywhere:  python3 webnotes/checks/test_physcheck.py"""
import os, sys, tempfile, time
import numpy as np

WEBNOTES = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WEBNOTES, 'figures'))
sys.path.insert(0, os.path.join(WEBNOTES, 'figures', 'session03'))
import physcheck as pc

NUMPY_ONLY = 'matplotlib' not in sys.modules and 'pyqula' not in sys.modules and 'style' not in sys.modules
import _honeycomb as hc

S0 = np.eye(2, dtype=complex); SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]]); SZ = np.diag([1.0, -1.0]).astype(complex)
SQUARE = 2 * np.pi * np.eye(2)
COUNT = [0]


def check(name, ok, detail):
    """Prints one line for a check and stops the script when it does not hold."""
    print(('ok    ' if ok else 'FAIL  ') + name + ': ' + detail, flush=True)
    assert ok, name
    COUNT[0] += 1


def dvec(k, m):
    """The vector d of the two-band model of the tests, a lattice Dirac cone with the mass m + cos kx + cos ky."""
    return np.array([np.sin(k[0]), np.sin(k[1]), m + np.cos(k[0]) + np.cos(k[1])])


def two_band(m):
    """H = d.sigma with a term along the identity, which moves the bands and leaves the eigenvectors as they are."""
    def hk(k):
        d = dvec(k, m)
        return d[0] * SX + d[1] * SY + d[2] * SZ + 0.3 * np.cos(k[0]) * S0
    return hk


def closed_form(k, m, h=1e-5):
    """Omega of the lower band of d.sigma, +(1/2) d.(d_kx d x d_ky d)/|d|^3, from the spin 1/2 in a field."""
    d = dvec(k, m)
    dx = (dvec(k + np.array([h, 0]), m) - dvec(k - np.array([h, 0]), m)) / (2 * h)
    dy = (dvec(k + np.array([0, h]), m) - dvec(k - np.array([0, h]), m)) / (2 * h)
    return 0.5 * d @ np.cross(dx, dy) / np.linalg.norm(d) ** 3


def literal(hk, k, n, h=1e-4):
    """Omega_n = -2 Im <d_kx u_n|d_ky u_n> from finite differences of the eigenvector, in the gauge where the overlap
    with the eigenvector at k is real and positive, which is smooth around k."""
    k = np.asarray(k, float)
    u0 = np.linalg.eigh(hk(k))[1][:, n]

    def u(q):
        v = np.linalg.eigh(hk(q))[1][:, n]
        return v * np.exp(-1j * np.angle(np.vdot(u0, v)))
    dx = (u(k + np.array([h, 0])) - u(k - np.array([h, 0]))) / (2 * h)
    dy = (u(k + np.array([0, h])) - u(k - np.array([0, h]))) / (2 * h)
    return -2 * np.imag(np.vdot(dx, dy))


def four_band(seed=18, amp=0.4, split=1.0):
    """A random four-band model with complex hoppings to three neighbors. The seed was searched for a pair of lower
    bands with a Chern number, since most random models have none and a sign slip would not show. With seed 18 the
    two lower bands are 0.89 below the two upper ones at every k, and the pair has C = -1, the sum of -2 and +1."""
    r = np.random.default_rng(seed)
    Rs = [(1, 0), (0, 1), (1, 1)]
    M0 = r.normal(size=(4, 4)) + 1j * r.normal(size=(4, 4))
    M0 = amp * (M0 + M0.conj().T) / 2 + np.diag([-split, -split, split, split])
    Ts = [amp * (r.normal(size=(4, 4)) + 1j * r.normal(size=(4, 4))) for R in Rs]

    def hk(k):
        H = M0.copy()
        for R, T in zip(Rs, Ts):
            p = np.exp(1j * (k[0] * R[0] + k[1] * R[1]))
            H = H + T * p + T.conj().T * np.conj(p)
        return H
    return hk


def ssh(t1, t2, m=0.0):
    """The SSH chain with the hopping t1 inside the cell and t2 between cells, lattice constant 1, every site at the
    origin of its cell. m is a staggered onsite energy, which makes it the Rice-Mele chain."""
    def hk(k):
        f = t1 + t2 * np.exp(-1j * k)
        return np.array([[m, f], [np.conj(f), -m]])
    return hk


def zak_literal(hk, G, n=0, nk=4000):
    """int i <u|d_k u> dk across the zone with finite differences, in the gauge where the first component of u is
    real and positive, which is smooth and periodic when that component never vanishes."""
    ks = np.arange(nk) * G / nk
    us = []
    for k in ks:
        v = np.linalg.eigh(hk(k))[1][:, n]
        us.append(v * np.exp(-1j * np.angle(v[0])))
    us = np.array(us)
    du = (np.roll(us, -1, axis=0) - np.roll(us, 1, axis=0)) / (2 * G / nk)
    return float(np.real(1j * np.sum(np.conj(us) * du)) * G / nk)


def circle(a, b):
    """The distance between two phases on the circle, so that pi and -pi are the same."""
    return abs(np.exp(1j * a) - np.exp(1j * b))


def main():
    """Runs every check. The pyqula calls write files, so the caller runs this in a temporary folder."""
    t0 = time.time()
    rng = np.random.default_rng(0)
    check('numpy only', NUMPY_ONLY, 'importing physcheck loads no matplotlib, no style and no pyqula')
    A = np.array([[1.5, 0.8], [-0.4, 1.1]])
    check('reciprocal vectors', np.allclose(A @ pc.reciprocal(A).T, 2 * np.pi * np.eye(2)), 'a_i.b_j = 2 pi delta_ij')

    # two-band model, the absolute sign
    pts = rng.uniform(-np.pi, np.pi, size=(5, 2))
    for m in (1.0, -1.0):
        hk = two_band(m)
        err = max(abs(pc.berry_curvature(hk, k, 0) - closed_form(k, m)) for k in pts)
        check('two bands, m=%+.0f, Kubo against the closed form' % m, err < 1e-7,
              'largest difference %.1e at 5 points, lower band' % err)
        err = max(abs(pc.berry_curvature(hk, k, n) - literal(hk, k, n)) for k in pts for n in (0, 1))
        check('two bands, m=%+.0f, Kubo against the literal definition' % m, err < 1e-6,
              'largest difference %.1e at 5 points, both bands' % err)
        ck, cl = pc.chern_kubo(hk, SQUARE, 0, nk=24), pc.chern_links(hk, SQUARE, 0, nk=24)
        check('two bands, m=%+.0f, Chern number' % m, abs(ck + m) < 1e-5 and abs(cl + m) < 1e-9,
              'Kubo %+.6f, links %+.6f, the lower band has C = %+d' % (ck, cl, -m))
    hk = two_band(1.0)
    ck, cl = pc.chern_kubo(hk, SQUARE[::-1], 0, nk=24), pc.chern_links(hk, SQUARE[::-1], 0, nk=24)
    check('two bands, b1 and b2 exchanged', abs(ck + 1) < 1e-5 and abs(cl + 1) < 1e-9,
          'Kubo %+.6f, links %+.6f, the same C with a left-handed pair' % (ck, cl))
    cu = pc.chern_links(hk, SQUARE, 1, nk=24)
    check('two bands, upper band', abs(cu - 1) < 1e-9, 'links %+.6f, the two bands add to zero' % cu)

    # one small plaquette, where the sign of the link variables comes from
    k0, a = np.array([0.7, -1.9]), 1e-3
    corners = [k0, k0 + [a, 0], k0 + [a, a], k0 + [0, a]]
    us = [np.linalg.eigh(hk(q))[1][:, 0] for q in corners]
    phase = np.angle(np.prod([np.vdot(us[i], us[(i + 1) % 4]) for i in range(4)]))
    om = pc.berry_curvature(hk, k0 + a / 2, 0)
    check('one plaquette, counterclockwise', abs(phase / a ** 2 + om) < 1e-5 * abs(om),
          'phase/area %+.6f, Omega %+.6f, so the phase is minus Omega times the area' % (phase / a ** 2, om))

    # four bands, two of them filled
    hk = four_band()
    err = max(abs(pc.berry_curvature(hk, k, n) - literal(hk, k, n)) for k in pts for n in range(4))
    check('four bands, Kubo against the literal definition', err < 1e-6,
          'largest difference %.1e at 5 points, four bands' % err)
    err = max(abs(pc.berry_curvature(hk, k, [0, 1]) - pc.berry_curvature(hk, k, 0) - pc.berry_curvature(hk, k, 1))
              for k in pts)
    check('four bands, two bands together', err < 1e-9, 'the curvature of the pair is the sum of the two, to %.1e' % err)
    g = pc.gap(hk, SQUARE, 2, nk=60, direct=True)
    ck, cl = pc.chern_kubo(hk, SQUARE, range(2), nk=48), pc.chern_links(hk, SQUARE, range(2), nk=24)
    c0, c1 = pc.chern_links(hk, SQUARE, 0, nk=24), pc.chern_links(hk, SQUARE, 1, nk=24)
    check('four bands, Chern number of two filled bands', abs(ck + 1) < 1e-4 and abs(cl + 1) < 1e-9 and g > 0.8,
          'Kubo %+.6f, determinant of the links %+.6f, direct gap %.2f' % (ck, cl, g))
    check('four bands, band by band', abs(c0 + 2) < 1e-9 and abs(c1 - 1) < 1e-9,
          'links %+.0f and %+.0f, their sum is the C of the pair' % (c0, c1))

    # the honeycomb helper of the figures
    Bh = pc.reciprocal([hc.a1, hc.a2])
    hk = lambda k: hc.bloch(k, t2=0.1)
    ck, cl = pc.chern_kubo(hk, Bh, 0, nk=24), pc.chern_links(hk, Bh, 0, nk=24)
    g = pc.gap(hk, Bh, 1, nk=60)
    check('_honeycomb.bloch, t2=0.1', abs(ck - 1) < 1e-5 and abs(cl - 1) < 1e-9 and abs(g - 3 * np.sqrt(3) * 0.2) < 1e-9,
          'Kubo %+.6f, links %+.6f, gap %.4f, which is 6 sqrt(3) t2' % (ck, cl, g))
    K = np.array([4 * np.pi / 3, 0.0])
    g50, g50K = pc.gap(hk, Bh, 1, nk=50), pc.gap(hk, Bh, 1, nk=50, points=[K, -K])
    check('gap, a mesh that misses K', g50 > g50K + 1e-3 and abs(g50K - g) < 1e-9,
          'nk=50 gives %.4f, and %.4f with K and K\' added' % (g50, g50K))
    old = hc.chern(24, t2=0.1)
    check('_honeycomb.chern', abs(old + 1) < 1e-9, 'it returns %+.0f, minus the C of the notes, as the sheet says' % old)

    # mesh convergence
    rows = [(n, pc.chern_kubo(hk, Bh, 0, nk=n), pc.chern_links(hk, Bh, 0, nk=n)) for n in (6, 12, 24, 48)]
    errs = [abs(r[1] - 1) for r in rows]
    check('mesh convergence, _honeycomb.bloch, t2=0.1',
          all(errs[i + 1] < errs[i] for i in range(3)) and errs[-1] < 1e-9 and all(abs(r[2] - 1) < 1e-9 for r in rows),
          'Kubo ' + ', '.join('nk=%d %.8f' % r[:2] for r in rows) + ', links 1 at every nk')

    # pyqula
    from pyqula import geometry, topology
    gh = geometry.honeycomb_lattice()
    h = gh.get_hamiltonian(has_spin=False)
    h.add_haldane(0.1)
    hk, Bp = pc.from_pyqula(h)
    Ap = np.array([gh.a1, gh.a2])[:, :2]
    kr = np.array([0.13, -0.27, 0.0])
    same = np.allclose(hk(kr[0] * Bp[0] + kr[1] * Bp[1]), h.get_hk_gen()(kr))
    check('from_pyqula', np.allclose(Ap @ Bp.T, 2 * np.pi * np.eye(2)) and same,
          'a_i.b_j = 2 pi delta_ij, and hk at s1 b1 + s2 b2 is the pyqula matrix at the reduced (s1, s2)')
    ck, cl, cp = pc.chern_kubo(hk, Bp, 0, nk=24), pc.chern_links(hk, Bp, 0, nk=24), h.get_chern()
    g = pc.gap(hk, Bp, 1, nk=60)
    check('pyqula honeycomb, add_haldane(0.1)',
          abs(ck - 1) < 1e-4 and abs(cl - 1) < 1e-9 and abs(cp - 1) < 1e-6 and abs(g - 0.9) < 1e-9,
          'Kubo %+.6f, links %+.6f, h.get_chern() %+.6f, gap %.4f' % (ck, cl, cp, g))
    h = gh.get_hamiltonian(has_spin=False)
    h.add_haldane(-0.1)
    hk, Bp = pc.from_pyqula(h)
    cl, cp = pc.chern_links(hk, Bp, 0, nk=24), h.get_chern()
    check('pyqula honeycomb, add_haldane(-0.1)', abs(cl + 1) < 1e-9 and abs(cp + 1) < 1e-6,
          'links %+.6f, h.get_chern() %+.6f' % (cl, cp))
    h = gh.get_hamiltonian()
    h.add_haldane(0.1)
    hk, Bp = pc.from_pyqula(h)
    ck, cl, cp = pc.chern_kubo(hk, Bp, range(2), nk=24), pc.chern_links(hk, Bp, range(2), nk=24), h.get_chern()
    check('pyqula honeycomb with spin, two degenerate filled bands',
          abs(ck - 2) < 1e-4 and abs(cl - 2) < 1e-9 and abs(cp - 2) < 1e-6,
          'Kubo %+.6f, links %+.6f, h.get_chern() %+.6f' % (ck, cl, cp))

    # Zak phase
    G = 2 * np.pi
    z1, z2 = pc.zak_phase(ssh(0.5, 1.0), G), pc.zak_phase(ssh(1.5, 1.0), G)
    check('SSH chain, Zak phase', circle(z1, np.pi) < 1e-9 and circle(z2, 0) < 1e-9,
          '%.6f with the weak hopping inside the cell, %.6f with the strong one' % (z1, z2))
    hk = ssh(0.5, 1.0, m=0.3)
    z, zl = pc.zak_phase(hk, G, nk=400), zak_literal(hk, G)
    check('Rice-Mele chain, the sign of the Zak phase', circle(z, zl) < 1e-4 and 0.1 < abs(np.sin(z)),
          'Wilson loop %+.5f, the integral of i<u|d_k u> in a smooth gauge %+.5f' % (z, zl % (2 * np.pi)))
    gb = geometry.bichain()
    out = []
    for t in (0.5, 1.5):
        h1 = gb.get_hamiltonian(has_spin=False)
        h1.intra = t * h1.intra
        hk1, G1 = pc.from_pyqula(h1)
        out.append((pc.zak_phase(hk1, G1), topology.berry_phase(h1, nk=200), pc.gap(hk1, G1, 1, nk=200)))
    check('pyqula bichain, Zak phase',
          circle(out[0][0], np.pi) < 1e-9 and circle(out[1][0], 0) < 1e-9
          and circle(out[0][0], out[0][1]) < 1e-9 and circle(out[1][0], out[1][1]) < 1e-9
          and abs(out[0][2] - 1) < 1e-9 and abs(out[1][2] - 1) < 1e-9,
          'intra 0.5 gives %.6f, intra 1.5 gives %.6f, as topology.berry_phase modulo 2 pi, both gaps 1.0'
          % (out[0][0], out[1][0]))
    h1 = gb.get_hamiltonian(has_spin=False)
    h1.intra = 0.5 * h1.intra
    h1.add_sublattice_imbalance(0.3)
    hk1, G1 = pc.from_pyqula(h1)
    z, zp = pc.zak_phase(hk1, G1), topology.berry_phase(h1, nk=200)
    check('pyqula bichain with an imbalance, the sign', circle(z, zp) < 1e-9 and 0.1 < abs(np.sin(z)),
          'physcheck %+.6f, topology.berry_phase %+.6f' % (z, zp))

    # a Hamiltonian that is not periodic over the zone is refused
    def shifted(k):
        return ssh(0.5, 1.0)(k) * np.array([[1, np.exp(0.5j * k)], [np.exp(-0.5j * k), 1]])
    try:
        pc.zak_phase(shifted, G)
        refused = False
    except ValueError:
        refused = True
    check('a gauge that is not periodic', refused, 'zak_phase raises ValueError when hk(k + B) is not hk(k)')
    print('%d checks hold, %.1f s' % (COUNT[0], time.time() - t0))


if __name__ == '__main__':
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            main()
        finally:
            os.chdir(cwd)
