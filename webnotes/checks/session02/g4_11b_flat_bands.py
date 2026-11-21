"""Session 2, the numbers that page 11b (Section 2.11b, flat bands of the Lieb and kagome lattices) quotes and that no
figure script asserts. One check script per page is the rule: every number of a caption, a feedback, a fold, a
solution or a lab box is an assert, here or in the figure script that draws it. The figure scripts of the page assert
their own numbers: kagome_dos.py (the flat band at 2t, the range -4t to 2t, the peaks at -2t and 0, the V at -t) and
_g4_bands.py (the bands of the three pictures of the quiz). This script checks the key box and the fold, the hexagon
state of the kagome lattice and the plaquette state of the Lieb lattice, on a torus built here from the positions of
pyqula with its own bonds, which is a second route to the Hamiltonian of pyqula. It also checks the one third, the
solution of the problem by the formula and by pyqula, and the numbers of the feedback of the quizzes. It finds the
repository from its own path and writes no file, since pyqula runs in a temporary folder."""
import os
import tempfile

import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


os.chdir(tempfile.mkdtemp())
from pyqula import geometry  # noqa: E402


def torus(g, n, t):
    """Positions and the Hamiltonian -t sum over the bonds of length 1 of n x n cells of the geometry g, periodic."""
    a1, a2 = np.asarray(g.a1, float)[:2], np.asarray(g.a2, float)[:2]
    r = np.array([np.asarray(x, float)[:2] + i * a1 + j * a2 for i in range(n) for j in range(n) for x in g.r])
    L = np.array([n * a1, n * a2])
    H = np.zeros((len(r), len(r)))
    for i in range(len(r)):
        dr = r - r[i]
        c = np.linalg.solve(L.T, dr.T).T            # minimum image on the torus
        dr = (c - np.round(c)) @ L
        H[i, np.abs(np.linalg.norm(dr, axis=1) - 1) < 1e-6] = -t
    return r, H, L


def ring(r, L, center, radius):
    """The sites at the distance radius from center on the torus, ordered by their angle around it."""
    dr = r - center
    c = np.linalg.solve(L.T, dr.T).T
    dr = (c - np.round(c)) @ L
    idx = np.where(np.abs(np.linalg.norm(dr, axis=1) - radius) < 1e-6)[0]
    return idx[np.argsort(np.arctan2(dr[idx, 1], dr[idx, 0]))]


# the kagome lattice: the state +1,-1,+1,-1,+1,-1 around one hexagon has H psi = 2t psi for t = 1 and t = 2
gk = geometry.kagome_lattice()
for t in (1.0, 2.0):
    r, H, L = torus(gk, 6, t)
    check('kagome torus of 108 sites, every site has four neighbors', np.all((H != 0).sum(1) == 4), len(r))
    center = None
    for i in range(len(r)):                                    # a hexagon center is 1 away from six sites
        for v in (np.array([1.0, 0.0]), np.array([0.5, np.sqrt(3) / 2]), np.array([-0.5, np.sqrt(3) / 2])):
            p = r[i] + v
            if len(ring(r, L, p, 1.0)) == 6 and len(ring(r, L, p, 0.0)) == 0:
                center = p
                break
        if center is not None:
            break
    hexa = ring(r, L, center, 1.0)
    psi = np.zeros(len(r)); psi[hexa] = [1, -1, 1, -1, 1, -1]
    Hpsi = H @ psi
    check('kagome, H psi = 2t psi on the hexagon state, t = %g' % t, np.allclose(Hpsi, 2 * t * psi), np.round(Hpsi[hexa], 6))
    out = [i for i in range(len(r)) if i not in hexa and np.any(H[i, hexa] != 0)]
    check('kagome, six sites outside touch the hexagon, each through two bonds, and get zero',
          len(out) == 6 and all((H[i, hexa] != 0).sum() == 2 for i in out) and np.allclose(Hpsi[out], 0), len(out))
    check('kagome, each site of the hexagon has two neighbors on it and two outside',
          all((H[i, hexa] != 0).sum() == 2 for i in hexa), [(H[i, hexa] != 0).sum() for i in hexa])
r, H, L = torus(gk, 6, -1.0)
check('kagome, with the default +1 of pyqula the same state has the energy -2', np.allclose(H @ psi, -2 * psi), -2)

# the Lieb lattice: the state +1,-1,+1,-1 on the four edge sites around one plaquette has H psi = 0
gl = geometry.lieb_lattice()
for t in (1.0, -1.0):
    r, H, L = torus(gl, 6, t)
    deg = (H != 0).sum(1)
    corner = np.where(deg == 4)[0][0]
    center = r[corner] + np.array([1.0, 1.0])
    edge = ring(r, L, center, 1.0)
    check('Lieb, the four sites around a plaquette center are edge sites with two neighbors', len(edge) == 4 and np.all(deg[edge] == 2),
          deg[edge])
    psi = np.zeros(len(r)); psi[edge] = [1, -1, 1, -1]
    check('Lieb, H psi = 0 on the plaquette state, t = %g' % t, np.allclose(H @ psi, 0), np.abs(H @ psi).max())


def mesh_bands(h, n=60):
    hk = h.get_hk_gen()
    ks = np.arange(n) / n
    return np.array([np.linalg.eigvalsh(hk([a, b, 0.])) for a in ks for b in ks])


# one third of the states: the kagome flat band at 2t and the Lieb flat band at 0
ek = mesh_bands(gk.get_hamiltonian(has_spin=False, tij=[-1.]))
frac = np.mean(np.abs(ek.ravel() - 2) < 1e-9)
check('kagome with -t, the fraction of states at 2t is one third', abs(frac - 1 / 3) < 0.003, round(frac, 4))
check('kagome with -t, the other two bands from -4t to 2t', np.isclose(ek[:, :2].min(), -4) and ek[:, 1].max() <= 2 + 1e-9,
      (round(ek.min(), 6), round(ek[:, 1].max(), 6)))
el = mesh_bands(gl.get_hamiltonian(has_spin=False, tij=[-1.]))
check('Lieb, the middle band is 0 at every momentum, one third of the states', np.allclose(el[:, 1], 0, atol=1e-9), 1 / 3)
ek2 = mesh_bands(gk.get_hamiltonian(has_spin=False, tij=[-2.]))
check('kagome with t = 2, the flat band is at 4', np.allclose(ek2[:, 2], 4), 4)

# the problem: H(k) = -2t [[0, cos kx, cos ky], [cos kx, 0, 0], [cos ky, 0, 0]], with k in units of the inverse bond
# length, has 0 and +-2t sqrt(cos^2 kx + cos^2 ky)


def lieb_formula(k, t=1.0):
    cx, cy = np.cos(k[0]), np.cos(k[1])
    return -2 * t * np.array([[0, cx, cy], [cx, 0, 0], [cy, 0, 0]])


rng = np.random.default_rng(2)
ok = True
for k in rng.uniform(-np.pi, np.pi, size=(6, 2)):
    e = np.linalg.eigvalsh(lieb_formula(k))
    s = 2 * np.sqrt(np.cos(k[0]) ** 2 + np.cos(k[1]) ** 2)
    v = np.array([0, np.cos(k[1]), -np.cos(k[0])])
    ok &= np.allclose(e, [-s, 0, s]) and np.allclose(lieb_formula(k) @ v, 0)
check('the formula of the solution, energies 0 and +-2t sqrt(cos^2 kx + cos^2 ky), and the vector of the flat band', ok, 6)
eG, eM = np.linalg.eigvalsh(lieb_formula([0, 0])), np.linalg.eigvalsh(lieb_formula([np.pi / 2, np.pi / 2]))
check('Lieb at Gamma, +-2 sqrt2 t = +-2.83 t and 0', np.allclose(eG, [-2 * np.sqrt(2), 0, 2 * np.sqrt(2)]) and abs(2 * np.sqrt(2) - 2.83) < 0.005,
      np.round(eG, 4))
check('Lieb at M = (pi/2, pi/2), three times 0', np.allclose(eM, 0, atol=1e-12), np.round(eM, 12))
# the same with pyqula, the lattice constant 2, so M = (1/2, 1/2) in reduced momenta, and the formula at random points
hk = gl.get_hamiltonian(has_spin=False, tij=[-1.]).get_hk_gen()
A = np.array([gl.a1[:2], gl.a2[:2]])
ok = True
for k in rng.uniform(-np.pi, np.pi, size=(6, 2)):
    kr = A @ k / (2 * np.pi)
    ok &= np.allclose(np.linalg.eigvalsh(hk([kr[0], kr[1], 0.])), np.linalg.eigvalsh(lieb_formula(k)))
check('pyqula Lieb with tij=[-1.] has the bands of the formula', ok, 6)
check('pyqula Lieb at Gamma and at (1/2, 1/2)', np.allclose(np.linalg.eigvalsh(hk([0., 0., 0.])), eG)
      and np.allclose(np.linalg.eigvalsh(hk([0.5, 0.5, 0.])), 0, atol=1e-9), np.round(np.linalg.eigvalsh(hk([0.5, 0.5, 0.])), 9))

# ---- added after the physics check of the group, findings c8 and c9 and the numbers with no assert ----
import sys  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# c9, the solution of the problem: the Lieb energies at Gamma and M are the same for t and -t, so they do not test the
# sign of the hopping, while the kagome flat band moves from +2t to -2t
hk_minus = gl.get_hamiltonian(has_spin=False, tij=[-1.]).get_hk_gen()
hk_plus = gl.get_hamiltonian(has_spin=False, tij=[1.]).get_hk_gen()
same = all(np.allclose(np.linalg.eigvalsh(hk_minus(k)), np.linalg.eigvalsh(hk_plus(k)), atol=1e-9)
           for k in ([0., 0., 0.], [0.5, 0.5, 0.], [0.5, 0., 0.], [0.13, 0.37, 0.]))
check('Lieb, the energies at Gamma, M, X and a generic point are the same for t and -t', same,
      np.round(np.linalg.eigvalsh(hk_plus([0., 0., 0.])), 4))
ekp = mesh_bands(gk.get_hamiltonian(has_spin=False, tij=[1.]), n=24)
check('kagome, the flat band is at +2t for -t and at -2t for +t, so it tests the sign', np.allclose(ekp[:, 0], -2) and np.allclose(ek[:, 2], 2),
      (-2, 2))

# the caption of kagome_dos and the picture quiz, run in --verify from the pyqula script of the figure
sys.dont_write_bytecode = True                                     # the check writes no file
os.environ.setdefault('MPLBACKEND', 'Agg')
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures', 'session02'))
import style  # noqa: E402
import _g4_bands  # noqa: E402
d = style.run_script('session02/g4_kagome_bands.py')
iK, iM, iX, iMl = _g4_bands.check_flat(d)
km, kp, li = d['bands_kagome'], d['bands_kagome_plus'], d['bands_lieb']
check('quiz pictures, kagome with -t has -4t, 2t, 2t at Gamma', np.allclose(km[0], [-4, 2, 2]), np.round(km[0], 6))
check('quiz pictures, kagome with -t has the crossing at -t at K, and the flat band 2t there', np.allclose(km[iK], [-1, -1, 2]),
      np.round(km[iK], 6))
check('quiz pictures, kagome with -t runs from -4t to 2t', np.isclose(km.min(), -4) and np.isclose(km.max(), 2), (km.min(), km.max()))
check('quiz pictures, kagome with +t has the flat band at -2t and runs from -2t to 4t',
      np.allclose(kp[:, 0], -2) and np.isclose(kp.min(), -2) and np.isclose(kp.max(), 4), (kp.min(), kp.max()))
check('quiz pictures, Lieb flat band at 0 and the three bands meet at M', np.allclose(li[:, 1], 0) and np.allclose(li[iMl], 0, atol=1e-9),
      np.round(li[iMl], 9))
e, dos = np.array(d['energies']), np.array(d['dos'])
de = e[1] - e[0]
check('kagome dos, the flat band at 2t is a narrow peak, about 8.1, that the plot cuts at 1',
      abs(e[np.argmax(dos)] - 2) < 1e-9 and abs(dos.max() - 8.10) < 0.02, round(dos.max(), 3))
for E0 in (-2.0, 0.0):
    w = np.abs(e - E0) < 0.4
    check('kagome dos, a peak at %g t from the bands at M, about 0.70' % E0, abs(e[w][np.argmax(dos[w])] - E0) < 0.02
          and abs(dos[w].max() - 0.70) < 0.01, round(dos[w].max(), 4))
w = np.abs(e + 1) < 0.4
check('kagome dos, the V at -t from the crossing at K, about 0.042', abs(e[w][np.argmin(dos[w])] + 1) < 0.02
      and abs(dos[w].min() - 0.042) < 0.002, round(dos[w].min(), 4))
check('kagome dos, three states per cell less the tails, 2.97 in the window', abs(dos.sum() * de - 2.97) < 0.01, round(dos.sum() * de, 4))
check('kagome dos, the dispersive bands start at -4t, nothing below but the tails', dos[e < -4.3].max() < 0.03, round(dos[e < -4.3].max(), 4))

# c8 and the lab box: the words of the box against the stored texts of kang2020. The arXiv abstract is in the tracked file
# whole. The published abstract, from Crossref, is only in the full copy, which git ignores, so on a machine without it
# that part is not checked and the script says so.
src = os.path.join(HERE, '..', '..', 'sources')
tracked = ' '.join(open(os.path.join(src, 'session02', 'kang2020_s41467-020-17465-1.txt'), encoding='utf-8').read().split())
for phrase in ('arxiv: 2002.01452', 'frustrated kagome system CoSn, using angle-resolved photoemission spectroscopy',
               'dispersionless electronic excitation along the G-M high symmetry direction',
               'with an order of magnitude lower bandwidth (below 150 meV) compared to the Dirac bands originating from the same orbitals'):
    check('lab box kang2020, the preprint says "%s"' % phrase, phrase in tracked, 'found')
full = os.path.join(src, '.full', 'session02', 'kang2020_s41467-020-17465-1.txt')
if os.path.exists(full):
    blocks = open(full, encoding='utf-8').read().split('\n[')
    pub = ' '.join(next(b for b in blocks if b.startswith('abstract, from https://api.crossref.org')).split())
    check('lab box kang2020, the published abstract says "Throughout the entire Brillouin zone, the bandwidth of the flat band '
          'is suppressed by an order of magnitude"', 'Throughout the entire Brillouin zone, the bandwidth of the flat band is '
          'suppressed by an order of magnitude compared to the Dirac bands originating from the same orbitals' in pub, 'found')
    check('lab box kang2020, the published abstract gives no width in meV, its only meV is the gap of 80 meV',
          '150' not in pub and pub.count('meV') == 1 and 'gap of 80 meV' in pub, pub.count('meV'))
else:
    print('NOT CHECKED the published abstract of kang2020, no full copy of the source on this machine', flush=True)
