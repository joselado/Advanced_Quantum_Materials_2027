"""Session 2, the numbers that page 08 (Section 2.8) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The numbers of the band and of the map of the square lattice are asserted in
figures/session02/square_bands.py and _g3_maps.py, those of the three picture options in g3_quiz_stripes_x.py,
g3_quiz_stripes_y.py and g3_quiz_square_map.py, and those of decoupled_chains in decoupled_chains.py. This script holds
the rest: the key box, the steps fold, the two quizzes, the problem, the try-it box, the zero lines in the caption of
square_bands and the color scale that the picture quiz and decoupled_chains quote. The sign is the one of the
page and of webnotes/conventions/session02.md, the hopping -t with t > 0. It finds the repository from its own path,
runs pyqula in a temporary folder and writes no file."""
import os
import tempfile

import numpy as np

COUNT = [0]
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name
    COUNT[0] += 1


def torus(L, bonds, t=1.0):
    """The Hamiltonian -t sum over bonds of a torus of L^d sites, bonds a list of unit vectors (one per direction)."""
    d = len(bonds[0])
    N = L ** d
    idx = np.arange(N).reshape((L,) * d)
    H = np.zeros((N, N))
    for b in bonds:
        j = np.roll(idx, [-s for s in b], axis=tuple(range(d)))
        H[idx.ravel(), j.ravel()] += -t
        H[j.ravel(), idx.ravel()] += -t
    return H, idx


def main():
    from pyqula import geometry

    # the key box and the steps fold: the Bloch state e^{i(n phi_x + m phi_y)} is an eigenstate with (2.14), and the
    # bonds along x alone give -2t cos(phi_x); t = 1.7 so that t is not 1
    t, L = 1.7, 12
    H, idx = torus(L, [(1, 0), (0, 1)], t)
    Hx, _ = torus(L, [(1, 0)], t)
    worst = worst_x = 0.0
    n, m = np.meshgrid(np.arange(L), np.arange(L), indexing='ij')
    for p in range(L):
        for q in range(L):
            fx, fy = 2 * np.pi * p / L, 2 * np.pi * q / L
            psi = np.exp(1j * (n * fx + m * fy)).ravel()
            worst = max(worst, np.abs(H @ psi + 2 * t * (np.cos(fx) + np.cos(fy)) * psi).max())
            worst_x = max(worst_x, np.abs(Hx @ psi + 2 * t * np.cos(fx) * psi).max())
    check('the Bloch state of the fold has the energy (2.14), and the bonds along x give -2t cos(phi_x)',
          worst < 1e-12 and worst_x < 1e-12, (worst, worst_x))
    H3, idx3 = torus(6, [(1, 0, 0), (0, 1, 0), (0, 0, 1)], t)
    n3 = np.indices((6, 6, 6))
    f = 2 * np.pi * np.array([1, 2, 4]) / 6
    psi3 = np.exp(1j * np.tensordot(f, n3, axes=1)).ravel()
    check('the cubic lattice adds -2t cos(phi_z), (2.15)', np.allclose(H3 @ psi3, -2 * t * np.cos(f).sum() * psi3), 'ok')

    # the key box and the cubic quiz: -4t and 4t at Gamma and M, widths 4t, 8t, 12t, pyqula with tij=[-1.]
    ends = {}
    for name, g in (('chain', geometry.chain()), ('square', geometry.square_lattice()), ('cubic', geometry.cubic_lattice())):
        hk = g.get_hamiltonian(has_spin=False, tij=[-1.0]).get_hk_gen()
        d = {'chain': 1, 'square': 2, 'cubic': 3}[name]
        k0, kpi = [0.0, 0.0, 0.0], [0.5 if i < d else 0.0 for i in range(3)]
        ends[name] = (np.linalg.eigvalsh(hk(k0))[0], np.linalg.eigvalsh(hk(kpi))[0])
    widths = [ends[n][1] - ends[n][0] for n in ('chain', 'square', 'cubic')]
    check('the ends -2, 2, -4, 4, -6, 6 at 0 and at pi in every direction, the widths 4, 8, 12, one 4t per direction',
          np.allclose([ends['chain'], ends['square'], ends['cubic']], [[-2, 2], [-4, 4], [-6, 6]]) and np.allclose(widths, [4, 8, 12]),
          (ends, widths))
    rng = np.random.default_rng(3)
    ph = rng.uniform(-np.pi, np.pi, size=(20000, 3))
    e3 = -2 * np.cos(ph).sum(1)
    check('-6t and +6t are the extremes of the cubic band, at 0 and at pi in every direction', e3.min() > -6 and e3.max() < 6,
          (round(e3.min(), 3), round(e3.max(), 3)))

    # the quiz on the hopping along y: decoupled chains have -2t cos(phi_x) for every phi_y, -2t at 0 and 2t at pi,
    # the full band at phi_x = 0 is -4t at phi_y = 0 and 0 at phi_y = pi
    ev_chains = np.sort(np.linalg.eigvalsh(Hx))
    ref = np.sort(np.repeat(-2 * t * np.cos(2 * np.pi * np.arange(L) / L), L))
    full = lambda fx, fy: -2 * (np.cos(fx) + np.cos(fy))
    check('the lattice with no hopping along y has -2t cos(phi_x), L times each level',
          np.allclose(ev_chains, ref), (round(ev_chains.min() / t, 3), round(ev_chains.max() / t, 3)))
    check('-2t at phi_x = 0 and +2t at phi_x = pi for the chains, -4t and 0 along phi_x = 0 for the full band',
          np.isclose(-2 * np.cos(0), -2) and np.isclose(-2 * np.cos(np.pi), 2) and np.isclose(full(0, 0), -4) and np.isclose(full(0, np.pi), 0),
          'ok')

    # the problem: the diagonal hopping -t' adds -4t' cos(phi_x) cos(phi_y)
    s = np.array([1, -1])
    fx, fy = rng.uniform(-np.pi, np.pi, 2)
    corners = sum(np.exp(1j * (a * fx + b * fy)) for a in s for b in s)
    check('the sum over the four corners factorizes into 4 cos(phi_x) cos(phi_y)', np.isclose(corners, 4 * np.cos(fx) * np.cos(fy)), 'ok')
    tp = 0.3
    band = lambda fx, fy: -2 * (np.cos(fx) + np.cos(fy)) - 4 * tp * np.cos(fx) * np.cos(fy)
    vals = [band(0, 0), band(np.pi, 0), band(np.pi, np.pi)]
    check('Gamma, X, M give -4t-4t\', 4t\', 4t-4t\', which is -5.2, 1.2, 2.8 for t\' = 0.3',
          np.allclose(vals, [-4 - 4 * tp, 4 * tp, 4 - 4 * tp]) and np.allclose(vals, [-5.2, 1.2, 2.8]), np.round(vals, 6).tolist())
    g = geometry.square_lattice()
    hk = g.get_hamiltonian(has_spin=False, tij=[-1.0, -tp]).get_hk_gen()
    pts = [[0, 0], [0.5, 0], [0.5, 0.5]] + rng.uniform(-0.5, 0.5, (6, 2)).tolist()
    pq = [np.linalg.eigvalsh(hk([a, b, 0.0]))[0] for a, b in pts]
    want = [band(2 * np.pi * a, 2 * np.pi * b) for a, b in pts]
    shells = sorted(set(np.round([np.linalg.norm(np.array([i, j])) for i in range(-2, 3) for j in range(-2, 3) if (i, j) != (0, 0)], 9)))
    check('pyqula with tij=[-1,-0.3] gives this band, -5.2, 1.2, 2.8 at Gamma, X, M, and the diagonals at sqrt2 are the second shell',
          np.allclose(pq, want, atol=1e-12) and np.isclose(shells[1], np.sqrt(2)), np.round(pq[:3], 6).tolist())

    # the try-it: the notebook takes +1, the band goes from -4 to 4 with the extremes exchanged, +4 at Gamma, -4 at M
    hn = g.get_hamiltonian(has_spin=False, tij=[1.0])
    kk, en = hn.get_bands()
    hkn = hn.get_hk_gen()
    check('with tij=[1.0] the default path of the notebook spans -4 to 4, with 4 at Gamma and -4 at M',
          np.isclose(np.min(en), -4, atol=1e-3) and np.isclose(np.max(en), 4, atol=1e-3)
          and np.isclose(np.linalg.eigvalsh(hkn([0, 0, 0]))[0], 4) and np.isclose(np.linalg.eigvalsh(hkn([0.5, 0.5, 0]))[0], -4),
          (round(float(np.min(en)), 4), round(float(np.max(en)), 4)))

    # the caption of square_bands: the black lines of zero energy are phi_x +- phi_y = pi (mod 2 pi), since
    # cos(phi_x) + cos(phi_y) = 2 cos((phi_x+phi_y)/2) cos((phi_x-phi_y)/2). Inside the first zone they are the square
    # |phi_x| + |phi_y| = pi, and in the window up to 3 pi/2 they run past its corners into the next zones
    xs = np.linspace(-1.5 * np.pi, 1.5 * np.pi, 601)
    PX, PY = np.meshgrid(xs, xs, indexing='ij')
    eps = full(PX, PY)
    check('the band is -4t cos((phi_x+phi_y)/2) cos((phi_x-phi_y)/2)', np.allclose(eps, -4 * np.cos((PX + PY) / 2) * np.cos((PX - PY) / 2)), 'ok')
    # the grid steps by pi/200, so the lines phi_x +- phi_y = pi (mod 2 pi) go through grid points, where the band is 0
    zero = np.abs(eps) < 1e-9
    inzone = (np.abs(PX) <= np.pi + 1e-12) & (np.abs(PY) <= np.pi + 1e-12)
    dsq = np.abs(np.abs(PX) + np.abs(PY) - np.pi)
    wrap = lambda x: np.abs((x + np.pi) % (2 * np.pi) - np.pi)
    online = np.minimum(wrap(PX + PY - np.pi), wrap(PX - PY - np.pi)) < 1e-9
    sa = np.linspace(-np.pi / 2, np.pi / 2, 41)
    past = [full(np.pi + a, a) for a in sa] + [full(np.pi + a, -a) for a in sa]
    check('the zeros are the lines phi_x +- phi_y = pi (mod 2 pi), the square inside the first zone, and they continue past X',
          np.array_equal(zero, online) and dsq[zero & inzone].max() < 1e-9 and (zero & ~inzone).sum() > 0
          and np.allclose(past, 0, atol=1e-12),
          (int((zero & inzone).sum()), int((zero & ~inzone).sum())))

    # the picture quiz on the hopping along y and decoupled_chains: every map goes through _g3_maps.energy_map, on one
    # scale from -4t (blue) through 0 (white) to 4t (red), and the three options and decoupled_chains call it
    import sys
    sys.dont_write_bytecode = True                                    # the check writes no file
    figdir = os.path.join(ROOT, 'webnotes', 'figures', 'session02')
    sys.path.insert(0, figdir)
    sys.path.insert(0, os.path.dirname(figdir))
    import _g3_maps as maps
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    im = maps.energy_map(ax, maps.XS, maps.XS, maps.stripes_x())
    lo, mid, hi = (np.array(im.get_cmap()(im.norm(v))[:3]) for v in (-4.0, 0.0, 4.0))
    plt.close(fig)
    srcs = {f: open(os.path.join(figdir, f), encoding='utf-8').read() for f in
            ('g3_quiz_stripes_x.py', 'g3_quiz_stripes_y.py', 'g3_quiz_square_map.py', 'decoupled_chains.py')}
    calls = all('maps.option(' in srcs[f] for f in srcs if f.startswith('g3_quiz')) and 'maps.energy_map(' in srcs['decoupled_chains.py']
    check('the color scale is -4 to 4, blue at -4t, white at 0 and red at 4t, the same in the three options and in decoupled_chains',
          im.get_clim() == (-4.0, 4.0) and np.argmax(lo) == 2 and np.argmax(hi) == 0 and mid.min() > 0.95 and calls,
          (im.get_clim(), np.round(lo, 2).tolist(), np.round(mid, 2).tolist(), np.round(hi, 2).tolist()))
    print('%d checks hold' % COUNT[0])


if __name__ == '__main__':
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            main()
        finally:
            os.chdir(cwd)
