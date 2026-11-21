"""Session 2, the numbers that page 09 (Sections 2.9 and 2.10) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The numbers of the chain band, its velocity and its mass are asserted in
figures/session02/cos_velocity_mass.py, those of the density of states of the square lattice (0.05, 300, 0.29, 0.08)
in g3_square_dos.py, and the nesting of the three Fermi surfaces in _g3_fermi.py. This script holds the rest: the text
on the saddle points, the masses at the two band edges in the caption of g3_square_dos, the three quizzes of Section 2.9,
the problem, the key box and the steps fold of Section 2.10, with the lower half of the cone and the logarithm of the
saddle by a count, and the quiz on the Dirac cone. The sign is the one of the page and of webnotes/conventions/session02.md, the hopping -t
with t > 0. It finds the repository from its own path, runs pyqula in a temporary folder and writes no file."""
import os
import tempfile

import numpy as np
from scipy.special import ellipk

COUNT = [0]
S3 = np.sqrt(3.0)


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name
    COUNT[0] += 1


def sq(kx, ky, t=1.0):
    return -2 * t * (np.cos(kx) + np.cos(ky))


def main():
    from pyqula import geometry

    # the text before the density of states: the corners of the square Fermi surface, X = (pi, 0) and (0, pi), are
    # saddle points where the velocity vanishes, and the density of states diverges as a logarithm there
    h = 1e-4
    grad = [(sq(p[0] + h, p[1]) - sq(p[0] - h, p[1])) / (2 * h) for p in ((np.pi, 0), (0, np.pi))]
    curv = [(sq(np.pi + h, 0) - 2 * sq(np.pi, 0) + sq(np.pi - h, 0)) / h ** 2, (sq(np.pi, h) - 2 * sq(np.pi, 0) + sq(np.pi, -h)) / h ** 2]
    check('X is on the surface at zero energy, with zero velocity and the curvatures -2t and +2t, a saddle',
          np.isclose(sq(np.pi, 0), 0) and np.isclose(sq(0, np.pi), 0) and np.allclose(grad, 0, atol=1e-8) and np.allclose(curv, [-2, 2], atol=1e-4),
          np.round(curv, 4).tolist())
    gl = [ellipk(1 - w ** 2 / 16) / (2 * np.pi ** 2) for w in (1e-2, 1e-3, 1e-4)]
    check('with no broadening the density of states at zero energy grows as ln(16t/|w|)/(2 pi^2 t), a logarithm',
          np.allclose(np.diff(gl), np.log(10) / (2 * np.pi ** 2), rtol=1e-4), np.round(gl, 4).tolist())
    # the velocity vanishes also at Gamma and M, where the band curves the same way along both axes, and the band is
    # zero along the two lines phi_x +- phi_y = pi that cross at X
    vgm = [(sq(p[0] + h, p[1]) - sq(p[0] - h, p[1])) / (2 * h) for p in ((0, 0), (np.pi, np.pi))] + \
          [(sq(p[0], p[1] + h) - sq(p[0], p[1] - h)) / (2 * h) for p in ((0, 0), (np.pi, np.pi))]
    hess = lambda x, y: [(sq(x + h, y) - 2 * sq(x, y) + sq(x - h, y)) / h ** 2, (sq(x, y + h) - 2 * sq(x, y) + sq(x, y - h)) / h ** 2,
                         (sq(x + h, y + h) - sq(x + h, y - h) - sq(x - h, y + h) + sq(x - h, y - h)) / (4 * h ** 2)]
    cG, cM = hess(0.0, 0.0), hess(np.pi, np.pi)
    s = np.linspace(-1.0, 1.0, 41)
    check('the velocity is zero at Gamma and M too, and the band is zero on both lines through X',
          np.allclose(vgm, 0, atol=1e-8) and np.allclose(sq(np.pi + s, s), 0, atol=1e-12) and np.allclose(sq(np.pi + s, -s), 0, atol=1e-12),
          'ok')
    # the caption: the band edges, curvature +2t at Gamma and -2t at M along both axes, with no cross term, so the
    # mass is hbar^2/2ta^2 at the bottom and -hbar^2/2ta^2 at the top, and |m*|/(2 pi hbar^2) = 1/(4 pi t) = 0.08/t
    m_bot, m_top = 1 / cG[0], 1 / cM[0]                               # in units of hbar^2/ta^2, with t = a = hbar = 1
    check('the band edges: m* = 1/2 at Gamma and -1/2 at M, and |m*|/(2 pi hbar^2) = 1/(4 pi t) = 0.08/t, the K(0)/(2 pi^2) of the formula',
          np.allclose(cG, [2, 2, 0], atol=1e-4) and np.allclose(cM, [-2, -2, 0], atol=1e-4)
          and np.isclose(m_bot, 0.5, rtol=1e-4) and np.isclose(m_top, -0.5, rtol=1e-4)
          and np.isclose(abs(m_bot) / (2 * np.pi), 1 / (4 * np.pi), rtol=1e-4) and np.isclose(abs(m_top) / (2 * np.pi), 1 / (4 * np.pi), rtol=1e-4)
          and np.isclose(ellipk(0.0) / (2 * np.pi ** 2), 1 / (4 * np.pi)) and round(1 / (4 * np.pi), 2) == 0.08,
          (np.round(cG, 4).tolist(), np.round(cM, 4).tolist(), round(1 / (4 * np.pi), 4)))
    # the fold of Section 2.10: the saddle gives a logarithm, by a count on 6000^2 momenta of the zone, in rows so that
    # the memory stays small, against K(1 - w^2/16)/(2 pi^2) and ln(16/w)/(2 pi^2)
    nz = 6000
    kz = (np.arange(nz) + 0.5) / nz * 2 * np.pi - np.pi
    cnt = {0.4: 0, 0.04: 0}
    bins = {0.4: 0.02, 0.04: 0.004}
    for i0 in range(0, nz, 500):
        Ez = sq(kz[i0:i0 + 500, None], kz[None, :])
        for wz in cnt:
            cnt[wz] += np.count_nonzero(np.abs(Ez - wz) < bins[wz] / 2)
    gz = {wz: cnt[wz] / nz ** 2 / bins[wz] for wz in cnt}
    kf = {wz: ellipk(1 - wz ** 2 / 16) / (2 * np.pi ** 2) for wz in cnt}
    lg = {wz: np.log(16 / wz) / (2 * np.pi ** 2) for wz in cnt}
    check('a count of the square lattice at w = 0.4 and 0.04 follows K/(2 pi^2) and grows by ln(10)/(2 pi^2) for a factor 10, a logarithm',
          all(np.isclose(gz[wz], kf[wz], rtol=5e-3) and np.isclose(kf[wz], lg[wz], rtol=5e-3) for wz in cnt)
          and np.isclose(gz[0.04] - gz[0.4], np.log(10) / (2 * np.pi ** 2), rtol=2e-2),
          ({wz: round(gz[wz], 4) for wz in gz}, {wz: round(kf[wz], 4) for wz in kf}))

    # the quiz on the velocity: 2t sin(phi), 0 at phi = 0 and 2t at pi/2
    v = lambda p: (-2 * np.cos(p + 1e-6) + 2 * np.cos(p - 1e-6)) / 2e-6
    check('the slope of -2t cos(phi) is 0 at 0 and 2t at pi/2', np.isclose(v(0), 0, atol=1e-8) and np.isclose(v(np.pi / 2), 2, atol=1e-6),
          (round(v(0), 6), round(v(np.pi / 2), 6)))

    # the quiz on the mass: -2t cos(ka) = -2t + t a^2 k^2 close to k = 0, the curvature 2ta^2, m* = hbar^2/2ta^2,
    # 1/2 for t = a = hbar = 1, and 2t - t a^2 delta^2 at the top, so the mass goes as 1/t
    for t, a in ((1.0, 1.0), (0.7, 1.3)):
        k = 1e-3
        series = -2 * t * np.cos(k * a) - (-2 * t + t * a ** 2 * k ** 2)
        c0 = (-2 * t * np.cos(a * 1e-4) * 2 + 4 * t) / 1e-8              # second derivative at k = 0
        top = -2 * t * np.cos(np.pi + a * k) - (2 * t - t * a ** 2 * k ** 2)
        ok = abs(series) < 1e-12 and np.isclose(c0, 2 * t * a ** 2, rtol=1e-5) and abs(top) < 1e-12
        check('t=%.1f, a=%.1f: the expansions at the bottom and at the top, the curvature 2ta^2' % (t, a), ok, round(c0, 5))
    c1 = ((-2 + 0.01 ** 2) - 2 * (-2.0) + (-2 + 0.01 ** 2)) / 0.01 ** 2
    check('for t = a = hbar = 1 the band -2 + k^2 has the curvature 2, so 1/m* = 2 and m* = 1/2, and not 1',
          np.isclose(c1, 2) and np.isclose(1 / c1, 0.5), round(1 / c1, 6))

    # the quiz on nesting: eps(k + Q) = -eps(k), the surfaces at -3t and -t go to the contours at +3t and +t, and the
    # point (2 pi/3, 0) at -t goes to (5 pi/3, pi) at +t
    rng = np.random.default_rng(5)
    ks = rng.uniform(-np.pi, np.pi, (100, 2))
    check('eps(k + Q) = -eps(k) with Q = (pi, pi)', np.allclose(sq(ks[:, 0] + np.pi, ks[:, 1] + np.pi), -sq(ks[:, 0], ks[:, 1])), 'ok')
    check('(2 pi/3, 0) has the energy -t, and (5 pi/3, pi) has +t',
          np.isclose(sq(2 * np.pi / 3, 0), -1) and np.isclose(sq(5 * np.pi / 3, np.pi), 1), (sq(2 * np.pi / 3, 0), sq(5 * np.pi / 3, np.pi)))
    # the right option: each flat side of the square |phi_x| + |phi_y| = pi lands on the opposite side, so the side in the
    # quadrant of signs (sx, sy) goes to the quadrant (-sx, -sy) and stays on the square, (a, pi - a) to (a - pi, -a)
    av = np.linspace(0.01, np.pi - 0.01, 60)
    wrap = lambda x: (x + np.pi) % (2 * np.pi) - np.pi
    sides = []
    for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        qx, qy = wrap(sx * av + np.pi), wrap(sy * (np.pi - av) + np.pi)
        sides.append(np.all(np.sign(qx) == -sx) and np.all(np.sign(qy) == -sy) and np.allclose(np.abs(qx) + np.abs(qy), np.pi))
    qx, qy = wrap(av + np.pi), wrap(np.pi - av + np.pi)
    check('the shift by Q takes each side of the square to the opposite side, (a, pi - a) to (a - pi, -a)',
          all(sides) and np.allclose(qx, av - np.pi) and np.allclose(qy, -av), sides)
    phi = np.linspace(0, 2 * np.pi, 400)
    # the surface at -3t is a closed line around Gamma: along every direction from Gamma it is crossed once inside the zone
    r = np.linspace(0, np.pi, 20001)
    radii = []
    for a in phi:
        e = sq(r * np.cos(a), r * np.sin(a))
        cross = np.nonzero(np.diff(np.sign(e + 3)))[0]
        radii.append(r[cross[0]] if len(cross) == 1 else np.nan)
    radii = np.array(radii)
    check('the surface at -3t is a small closed line around Gamma, of radius 1.0 to 1.05 in units of 1/a',
          np.all(np.isfinite(radii)) and radii.min() > 0.99 and radii.max() < 1.06, (round(radii.min(), 3), round(radii.max(), 3)))
    check('the shifted circle, the contour at +3t, is around M = (pi, pi)', np.isclose(sq(np.pi, np.pi), 4) and np.isclose(sq(np.pi + radii[0], np.pi), 3, atol=1e-3),
          round(sq(np.pi + radii[0], np.pi), 4))

    # the problem: g(w) = 1/(pi sqrt(4t^2 - w^2)) per site, 1/(2 pi t) = 0.16/t at w = 0, area 1, a count on a mesh and
    # pyqula with the Green function agree, and the slope 2t sin(phi_0) is sqrt(4t^2 - w^2) with 2t cos(phi_0) = -w
    w = np.array([0.0, 1.0, 1.5, 1.9])
    form = 1 / (np.pi * np.sqrt(4 - w ** 2))
    pc = np.linspace(-np.pi, np.pi, 2000001)[:-1]
    Ec = -2 * np.cos(pc)
    cnt = np.array([np.mean(np.abs(Ec - x) < 5e-3) / 1e-2 for x in w])
    hc = geometry.chain().get_hamiltonian(has_spin=False, tij=[-1.0])
    _, dg = hc.get_dos(energies=w, mode='Green', delta=1e-4)
    from scipy.integrate import quad
    area = quad(lambda x: 1 / (np.pi * np.sqrt(4 - x ** 2)), -2, 2, limit=200)[0]
    p0 = np.arccos(-w / 2)
    check('the chain: 1/(pi sqrt(4t^2-w^2)) against a count on 2e6 momenta and against pyqula with mode="Green"',
          np.allclose(cnt, form, rtol=2e-3) and np.allclose(dg, form, rtol=2e-3), (np.round(form, 4).tolist(), np.round(cnt, 4).tolist(), np.round(dg, 4).tolist()))
    check('g(0) = 1/(2 pi t) = 0.16/t, the area over the band is 1, and 2t sin(phi_0) = sqrt(4t^2 - w^2)',
          np.isclose(form[0], 1 / (2 * np.pi)) and round(form[0], 2) == 0.16 and np.isclose(area, 1, atol=1e-6)
          and np.allclose(2 * np.sin(p0), np.sqrt(4 - w ** 2)), (round(form[0], 4), round(area, 6)))
    edge = [1 / (np.pi * np.sqrt(4 - x ** 2)) * np.sqrt(2 - x) for x in (1.99, 1.999, 1.9999)]
    check('at the band edge it diverges as an inverse square root, g sqrt(2t - w) tends to 1/(2 pi sqrt(t))',
          np.allclose(edge, 1 / (2 * np.pi), rtol=1e-2), np.round(edge, 5).tolist())

    # the key box of Section 2.10, per unit area and for one spin, each checked with a count on a mesh
    n = 3000
    L = 4.0
    kx = (np.arange(n) + 0.5) / n * 2 * L - L
    KX, KY = np.meshgrid(kx, kx, indexing='ij')
    kk = np.sqrt(KX ** 2 + KY ** 2)
    dk2 = (2 * L / n) ** 2 / (2 * np.pi) ** 2                         # d^2k/(2 pi)^2 of one point
    m, hbar, vF = 0.8, 1.0, 1.3
    Ep = hbar ** 2 * kk ** 2 / (2 * m)
    Ed = hbar * vF * kk
    dE = 0.02
    gp = [np.sum(np.abs(Ep - E) < dE / 2) * dk2 / dE for E in (0.5, 1.5, 2.5)]
    gd = [np.sum(np.abs(Ed - E) < dE / 2) * dk2 / dE for E in (0.5, 1.5, 2.5)]
    check('a parabolic band E = hbar^2 k^2/2m* has g = m*/(2 pi hbar^2), constant, for E > 0',
          np.allclose(gp, m / (2 * np.pi * hbar ** 2), rtol=1e-2), (np.round(gp, 4).tolist(), round(m / (2 * np.pi), 4)))
    check('the upper half of one Dirac cone E = hbar vF k has g = E/(2 pi hbar^2 vF^2)',
          np.allclose(gd, np.array([0.5, 1.5, 2.5]) / (2 * np.pi * hbar ** 2 * vF ** 2), rtol=1e-2), np.round(gd, 4).tolist())
    # the fold: the lower half E = -hbar vF k decreases with k, so the disk of radius k = |E|/hbar vF holds the states
    # above E, k^2/4 pi per unit area, and g = -d/dE of that number is |E|/(2 pi hbar^2 vF^2), the same as a count
    El = -hbar * vF * kk
    Es = np.array([-0.5, -1.5, -2.5])
    above = [np.sum((El > E) & (El <= 0)) * dk2 for E in Es]
    disk = [(abs(E) / (hbar * vF)) ** 2 / (4 * np.pi) for E in Es]
    gl = [np.sum(np.abs(El - E) < dE / 2) * dk2 / dE for E in Es]
    gder = [-((((abs(E - dE / 2)) / (hbar * vF)) ** 2 - ((abs(E + dE / 2)) / (hbar * vF)) ** 2) / (4 * np.pi)) / (-dE) for E in Es]
    check('the lower half of the cone: the states above E fill the disk, k^2/4 pi, and g = |E|/(2 pi hbar^2 vF^2) by a count',
          np.allclose(above, disk, rtol=1e-2) and np.allclose(gl, np.abs(Es) / (2 * np.pi * hbar ** 2 * vF ** 2), rtol=1e-2)
          and np.allclose(gder, np.abs(Es) / (2 * np.pi * hbar ** 2 * vF ** 2), rtol=1e-6),
          (np.round(gl, 4).tolist(), np.round(np.abs(Es) / (2 * np.pi * vF ** 2), 4).tolist()))
    # the flat band: one state per cell, int d^2k/(2 pi)^2 over the zone = 1/A_c, here for the kagome lattice
    A = np.array([[2.0, 0.0], [1.0, S3]])
    Ac = abs(np.linalg.det(A))
    Bz = abs(np.linalg.det(2 * np.pi * np.linalg.inv(A).T))
    check('a flat band holds one state per cell, the area of the zone over (2 pi)^2 is 1/A_c', np.isclose(Bz / (2 * np.pi) ** 2, 1 / Ac),
          round(1 / Ac, 4))
    # the lattices of the session agree with the box: the square band edge and the honeycomb V with two valleys
    Ach, v_h = 3 * S3 / 2, 1.5
    check('the square lattice edge 1/(4 pi t) is m*/(2 pi hbar^2) with m* = 1/2, and the honeycomb V 2|E|/(sqrt3 pi t^2) per cell is two cones of A_c|E|/(2 pi v^2)',
          np.isclose(1 / (4 * np.pi), 0.5 / (2 * np.pi)) and np.isclose(2 / (S3 * np.pi), 2 * Ach / (2 * np.pi * v_h ** 2)),
          round(2 / (S3 * np.pi), 4))

    # the steps fold: N(E) = k^2/4 pi per unit area, and in one dimension g = (1/pi) dk/dE, which diverges as
    # 1/sqrt(E) at the bottom of a parabolic band
    k1 = (np.arange(2000000) + 0.5) / 2000000 * 8 - 4
    E1 = k1 ** 2 / (2 * m)
    g1 = [np.sum(np.abs(E1 - E) < dE / 2) * (8 / 2000000) / (2 * np.pi) / dE for E in (0.25, 1.0)]
    want1 = [(1 / np.pi) * np.sqrt(m / (2 * E)) for E in (0.25, 1.0)]
    check('in one dimension g = (1/pi) dk/dE = (1/pi) sqrt(m/2E), so g sqrt(E) is constant',
          np.allclose(g1, want1, rtol=1e-2) and np.isclose(g1[0] / g1[1], 2, rtol=2e-2), (np.round(g1, 4).tolist(), np.round(want1, 4).tolist()))
    print('%d checks hold' % COUNT[0])


if __name__ == '__main__':
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            main()
        finally:
            os.chdir(cwd)
