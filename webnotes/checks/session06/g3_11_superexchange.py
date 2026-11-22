"""Session 6, the numbers that page 11 (Sections 6.11 and 6.12) quotes, checked in the order of the page.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or
in the figure script that draws it. The classical spin chain with the Dzyaloshinskii-Moriya term is checked in two ways.
The first is the bond alone: J S_i.S_j + D z.(S_i x S_j) is a bilinear form s_i^T M s_j, whose minimum over all pairs
of unit vectors is minus the largest singular value of M, so the minimum over all directions is found with no grid. The
second is the angle in the plane, from the helper of the picture quiz, figures/session06/_g3_spiral.py, which minimizes
over the full circle and holds the sense of rotation of webnotes/conventions/session06.md. A uniform spiral puts every
bond at this minimum, so it is the ground state of the chain. The lab box is checked against the stored source. It finds
the repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session06/g3_11_superexchange.py"""
import os, sys
sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
assert os.path.exists(os.path.join(REPO, 'webnotes', 'pages', 'session06'))

import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


zhat = np.array([0., 0., 1.])


def bond(J, D):
    """The matrix M of the bond energy s_i^T M s_j = J s_i.s_j + D z.(s_i x s_j), with z.(a x b) = a.(b x z)."""
    A = np.array([np.cross(e, zhat) for e in np.eye(3)]).T          # A b = b x z
    return J * np.eye(3) + D * A


def energy(J, D, a, b):
    return J * a @ b + D * zhat @ np.cross(a, b)


def angle(a, b):
    return np.degrees(np.arccos(np.clip(a @ b / np.linalg.norm(a) / np.linalg.norm(b), -1, 1)))


# the key box and the fold: the minimum over all directions of two unit spins, and where it is
for J, D, deg in ((1.0, 0.0, 180.0), (1.0, 1.0, 135.0), (1.0, 5.0, 101.3), (2.0, 2.0, 135.0)):
    M = bond(J, D)
    u, s, vt = np.linalg.svd(M)
    a, b = u[:, 0], -vt[0]                                           # the pair that gives -s_max
    ok = abs(energy(J, D, a, b) + s[0]) < 1e-12 and abs(s[0] - np.hypot(J, D)) < 1e-12
    if D > 0:
        ok = ok and abs(a[2]) < 1e-12 and abs(b[2]) < 1e-12 and s[1] > s[2] + 1e-9   # in the plane normal to z, and unique plane
        ok = ok and zhat @ np.cross(a, b) < 0                        # clockwise from S_i to S_j seen from +z
    ok = ok and round(angle(a, b), 1) == deg
    check(f'key box and fold, J={J:g}, D={D:g}: the minimum over all directions is -S^2 sqrt(J^2+D^2) at {deg} degrees'
          + (', in the plane normal to z and clockwise seen from +z' if D > 0 else ''), ok, (round(-s[0], 4), round(angle(a, b), 2)))
    check(f'key box, J={J:g}, D={D:g}: cos theta = -J/sqrt(J^2+D^2)', abs(a @ b + J / np.hypot(J, D)) < 1e-12, round(a @ b, 5))

# the fold: a uniform spiral puts every bond at its minimum, so the chain has -S^2 sqrt(J^2+D^2) per bond and no frustration
for J, D in ((1.0, 1.0), (1.0, 5.0)):
    th = -np.arccos(-J / np.hypot(J, D))                             # clockwise seen from +z
    spins = np.array([[np.cos(i * th), np.sin(i * th), 0.] for i in range(30)])
    per = [energy(J, D, spins[i], spins[i + 1]) for i in range(29)]
    check(f'fold, J={J:g}, D={D:g}: the uniform spiral has -sqrt(J^2+D^2) on every bond', np.allclose(per, -np.hypot(J, D)), round(per[0], 5))
# for D >> J the angle goes to 90 degrees
check('fold, the angle goes to 90 degrees when D >> J', abs(np.degrees(np.arccos(-1 / np.hypot(1, 1000))) - 90) < 0.1,
      round(np.degrees(np.arccos(-1 / np.hypot(1, 1000))), 3))
# the existing text: the term alone (J = 0) favors 90 degrees
u, s, vt = np.linalg.svd(bond(0.0, 1.0))
check('text, the Dzyaloshinskii-Moriya term alone favors 90 degrees between neighbors', round(angle(u[:, 0], -vt[0]), 6) == 90.0,
      angle(u[:, 0], -vt[0]))

# the schematic dm_spiral and the picture quiz: the helper minimizes over the full circle
sys.path.insert(0, os.path.join(REPO, 'webnotes', 'figures', 'session06'))
import _g3_spiral
_g3_spiral.check()
check('schematic dm_spiral and picture quiz, 180, 135.0 and 101.3 degrees for D = 0, J, 5J (helper _g3_spiral)', True, 'asserted')

# the first quiz: a global rotation changes the Dzyaloshinskii-Moriya term with D along z and the Kitaev term
Rx = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0.]])                   # 90 degrees about x
Ry = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0.]])                   # 90 degrees about y
rng = np.random.default_rng(1)
p, q = rng.normal(size=3), rng.normal(size=3)
# z.(Rp x Rq) = (R^T z).(p x q), and R^T z for Rx is -y: the term along z becomes a term along y
check('quiz 1, after a rotation by 90 degrees about x the term along z becomes a term along y',
      abs(zhat @ np.cross(Rx @ p, Rx @ q) - (Rx.T @ zhat) @ np.cross(p, q)) < 1e-12 and np.allclose(np.abs(Rx.T @ zhat), [0, 1, 0]),
      Rx.T @ zhat)
check('quiz 1, after a rotation by 90 degrees about y the term K Sz Sz becomes K Sx Sx',
      abs((Ry @ p)[2] * (Ry @ q)[2] - p[0] * q[0]) < 1e-12, True)
check('quiz 1, S_i.S_j does not change under a global rotation', abs((Rx @ p) @ (Rx @ q) - p @ q) < 1e-12, True)

# the second quiz: the drawn rows, seen from +z, at D = J, the energies per bond for S = 1, from the vectors of the pictures
rows = {deg: _g3_spiral.row(deg) for deg in _g3_spiral.ROWS}
eq = {deg: [energy(1, 1, r[i], r[i + 1]) for i in range(len(r) - 1)] for deg, r in rows.items()}
check('quiz 2, the drawn rows at 135 and 101.3 degrees turn clockwise seen from +z, z.(S_i x S_i+1) < 0 on every bond',
      all(np.cross(r[i], r[i + 1])[2] < 0 for deg in (135.0, 101.3) for r in [rows[deg]] for i in range(len(r) - 1)), True)
check('quiz 2, the row at 180 degrees gives -J S^2 on every bond and no energy from D', np.allclose(eq[180.0], -1.0, atol=1e-12),
      np.round(eq[180.0], 4))
check('quiz 2, the row at 135 degrees gives -sqrt2 J S^2 = -1.41 J S^2 on every bond',
      np.allclose(eq[135.0], -np.sqrt(2), atol=1e-12) and round(eq[135.0][0], 2) == -1.41, np.round(eq[135.0], 4))
check('quiz 2, cos theta = -1/sqrt2 is 135 degrees, and 101 degrees has cos theta = -1/sqrt26',
      round(np.degrees(np.arccos(-1 / np.sqrt(2))), 6) == 135.0 and round(np.degrees(np.arccos(-1 / np.sqrt(26))), 1) == 101.3, True)
check('quiz 2, the row at 101.3 degrees gives -1.18 J S^2 for D = J, above -1.41',
      np.allclose(eq[101.3], eq[101.3][0], atol=1e-12) and round(eq[101.3][0], 2) == -1.18 and eq[101.3][0] > eq[135.0][0],
      np.round(eq[101.3], 4))
# the condition of the question, the index i grows from left to right: read from right to left the same pictures turn
# counterclockwise, and the row at 135 degrees is no longer the lowest of the three
rev = {deg: [energy(1, 1, r[i + 1], r[i]) for i in range(len(r) - 1)] for deg, r in rows.items()}
check('quiz 2, condition, with i growing to the left the rows give -1, 0 and +0.785, so the answer needs the direction of i',
      np.allclose(rev[180.0], -1.0) and np.allclose(rev[135.0], 0.0, atol=1e-12) and round(rev[101.3][0], 3) == 0.785
      and min(rev, key=lambda k: rev[k][0]) == 180.0 and min(eq, key=lambda k: eq[k][0]) == 135.0,
      {k: round(v[0], 3) for k, v in rev.items()})
page = open(os.path.join(REPO, 'webnotes', 'pages', 'session06', '11-superexchange-as-the-origin-of-ferromagnetic-coupling.md'),
            encoding='utf-8').read()
check('quiz 2, the question states that the site index grows from left to right',
      'The site index $i$ grows from left to right.' in page, 'found')
check('quiz 2, the row at 101.3 degrees is the ground state for D = 5J, -sqrt26 J S^2',
      abs(energy(1, 5, rows[101.3][0], rows[101.3][1]) + np.sqrt(26)) < 1e-3, round(energy(1, 5, rows[101.3][0], rows[101.3][1]), 4))

# the third quiz: the cross product of collinear spins is zero, the other two terms are not
a = np.array([0, 0, 1.])
check('quiz 3, D.(S_i x S_j) is zero for parallel and antiparallel spins, for any D',
      all(np.allclose(np.cross(a, s * a), 0) for s in (1, -1)), True)
check('quiz 3, Lambda Sz Sz gives Lambda S^2 for parallel spins along z, and J S_i.S_j gives -J S^2 for antiparallel ones',
      a[2] * a[2] == 1 and a @ (-a) == -1, True)

# the problem: two spins with a small D, the canting and the energy gained
J, D = 1.0, 0.1
eps = np.linspace(-0.5, 0.5, 2000001)
E = -(J * np.cos(eps) + D * np.sin(eps))
k = np.argmin(E)
check('problem, the minimum is at eps = arctan(D/J), close to D/J = 0.1', abs(eps[k] - np.arctan(0.1)) < 1e-6, round(eps[k], 6))
check('problem, D/J = 0.1 rad is 5.7 degrees and arctan(0.1) is 5.71 degrees',
      round(np.degrees(0.1), 1) == 5.7 and round(np.degrees(np.arctan(0.1)), 2) == 5.71, (np.degrees(0.1), np.degrees(np.arctan(0.1))))
check('problem, the gain D^2 S^2/2J is 0.005 J S^2, and the exact gain sqrt(1.01) - 1 is 0.00499 J S^2',
      abs(D ** 2 / 2 / J - 0.005) < 1e-15 and round(np.sqrt(1.01) - 1, 5) == 0.00499 and abs(-E[k] - 1 - (np.sqrt(1.01) - 1)) < 1e-9,
      round(np.sqrt(1.01) - 1, 6))
check('problem, theta = 180 + eps has sin theta < 0, clockwise seen from +z, as the fold says', np.sin(np.pi + np.arctan(0.1)) < 0, True)
th = np.pi + np.arctan(0.1)
s1, s2 = np.array([1., 0, 0]), np.array([np.cos(th), np.sin(th), 0])
net = np.linalg.norm(s1 + s2)
check('problem, the net moment |S1 + S2| = 2S sin(eps/2), close to S eps', abs(net - 2 * np.sin(np.arctan(0.1) / 2)) < 1e-12
      and abs(net - 0.1) < 1e-3, round(net, 5))

# the lab box: the stored source, the arXiv abstract kept whole in the tracked file
src = ' '.join(open(os.path.join(REPO, 'webnotes', 'sources', 'session06', 'huang2017_nature22391.txt'),
                    encoding='utf-8').read().split())
check('lab box, MOKE microscopy shows that monolayer CrI3 is an Ising ferromagnet with out-of-plane spin orientation',
      'we use magneto-optical Kerr effect (MOKE) microscopy to demonstrate that monolayer chromium triiodide (CrI3) is an Ising '
      'ferromagnet with out-of-plane spin orientation.' in src, 'found')
check('lab box, the Curie temperature of 45 K and the 61 K of the bulk crystal',
      'Its Curie temperature of 45 K is only slightly lower than the 61 K of the bulk crystal' in src, 'found')
check('lab box, the Mermin-Wagner theorem and the anisotropy that removes the restriction',
      'magnetic order is prohibited in the 2D isotropic Heisenberg model at finite temperatures by the Mermin-Wagner theorem. '
      'However, magnetic anisotropy removes this restriction' in src, 'found')
page = open(os.path.join(REPO, 'webnotes', 'pages', 'session06', '11-superexchange-as-the-origin-of-ferromagnetic-coupling.md'),
            encoding='utf-8').read()
box = page.split('::: lab', 1)[1].split('\n:::', 1)[0]
check('lab box, the box does not call CrI3 an insulator, which this abstract does not say of CrI3', 'insulat' not in box,
      'not found')

# corrected on 2026-11-22, the text of 6.12: the term needs a bond with no inversion center, and a mirror does not forbid
# it. A symmetry with the matrix R on the positions takes an axial vector S to det(R) R S and moves the sites. For random
# spins we find the matrix T with D.(S'_i x S'_j) = (T D).(S_i x S_j), and the allowed D are those with T D = D. The
# inversion through the middle of the bond leaves none, while a mirror that contains the bond allows D normal to it,
# and a mirror normal to the bond through its middle allows D in the mirror plane.
rng = np.random.default_rng(5)


def allowed_D(R, swap):
    Sp = rng.normal(size=(40, 2, 3))
    T = np.zeros((3, 3))
    X = np.cross(Sp[:, 0], Sp[:, 1])                                    # S_i x S_j for each sample
    for a in range(3):
        e = np.eye(3)[a]
        Si2, Sj2 = (np.linalg.det(R) * Sp @ R.T).transpose(1, 0, 2)
        if swap:
            Si2, Sj2 = Sj2, Si2                                         # the symmetry exchanges the two sites
        y = np.cross(Si2, Sj2) @ e
        T[:, a] = np.linalg.lstsq(X, y, rcond=None)[0]
    w, v = np.linalg.eig(T)
    return int(np.sum(np.abs(w - 1) < 1e-9)), T


n_inv, T_inv = allowed_D(-np.eye(3), True)                             # inversion through the middle of a bond along x
n_mc, T_mc = allowed_D(np.diag([1., -1., 1.]), False)                  # the mirror y -> -y contains the bond
n_mn, T_mn = allowed_D(np.diag([-1., 1., 1.]), True)                   # the mirror x -> -x through the middle
check('text 6.12, an inversion center at the middle of the bond forbids D, a mirror that contains the bond allows D normal '
      'to it, a mirror normal to the bond allows D in its plane', n_inv == 0 and np.allclose(T_inv, -np.eye(3))
      and n_mc == 1 and np.allclose(T_mc, np.diag([-1., 1., -1.])) and n_mn == 2 and np.allclose(T_mn, np.diag([-1., 1., 1.])),
      (n_inv, n_mc, n_mn))

# decided on 2026-11-22, the caption of dm_spiral: the drawing turns each spin counterclockwise in the frame of the figure,
# by the angle arccos(-J/sqrt(J^2+D^2)) > 0. The ground state for D > 0 turns clockwise seen from +z (sin theta < 0), so the
# drawing is the view from -z, which is the view looking along D. For D < 0 the view along D is from +z, where the ground
# state turns counterclockwise, so the drawing fits both signs.
src = open(os.path.join(REPO, 'webnotes', 'figures', 'session06', 'dm_spiral.py')).read()
sinth = {s: -s / np.hypot(1, 1) for s in (1.0, -1.0)}                  # sin theta of the ground state, J = 1, D = +-1
check('caption dm_spiral, the drawing turns counterclockwise (a = pi/2 + i th, th > 0), which is the view from -z for D > 0 '
      'and from +z for D < 0, so looking along D in both cases',
      'a = np.pi / 2 + i * th' in src and 'return np.arccos(-J / np.hypot(J, D))' in src and "view along $\\mathbf{D}$" in src
      and sinth[1.0] < 0 and sinth[-1.0] > 0, sinth)

# corrected on 2026-11-22, the notebook box and the try-it box of 6.12, against the cell "Non-collinear magnetism from
# spin-orbit coupling": a chain of 10 sites with open ends, add_rashba(1.), U = 10, mf="XY", mix=0.9. The bond is sqrt 2
# times a rotation of the spin by 90 degrees about y, a turn of the spin axes by -90 degrees per site maps it onto the plain
# chain with the hopping sqrt 2, so the energy does not depend on the angle, and the random guess picks an angle between
# 90 and 180 degrees. Without the Rashba line the neighbors are antiparallel. With the default maxite=1000 some guesses do
# not converge, and maxite=4000 does.
import json, tempfile
nb = json.load(open(os.path.join(REPO, 'jupyter-notebooks', 'session6.ipynb')))['cells']
ih = [j for j, c in enumerate(nb) if c['cell_type'] == 'markdown'
      and ''.join(c['source']).startswith('## Non-collinear magnetism from spin-orbit coupling')]
code = next(''.join(c['source']) for c in nb[ih[0] + 1:] if c['cell_type'] == 'code')
check('notebook box and try-it, the cell is the open chain of 10 sites with add_rashba(1.) at U=10 and mf="XY"',
      len(ih) == 1 and 'get_supercell(10)' in code and 'h.add_rashba(1.)' in code and 'U = 10.' in code and 'mf="XY"' in code
      and 'maxite' not in code, 'ok')
os.chdir(tempfile.mkdtemp())
from pyqula import geometry


def rashba_chain(rashba=True):
    g = geometry.chain(); g = g.get_supercell(10); g.dimensionality = 0
    h = g.get_hamiltonian()
    if rashba:
        h.add_rashba(1.)
    return h


Mh = rashba_chain().intra
Mh = np.asarray(Mh.todense() if hasattr(Mh, 'todense') else Mh)
sy2 = np.array([[0, -1j], [1j, 0]])
rot = lambda th: np.cos(th / 2) * np.eye(2) + 1j * np.sin(th / 2) * sy2
Ug = np.zeros((20, 20), complex)
for j in range(10):
    Ug[2 * j:2 * j + 2, 2 * j:2 * j + 2] = rot(-np.pi / 2 * j)
Mg = Ug.conj().T @ Mh @ Ug
plain = np.zeros((20, 20))
for j in range(9):
    plain[2 * j:2 * j + 2, 2 * j + 2:2 * j + 4] = plain[2 * j + 2:2 * j + 4, 2 * j:2 * j + 2] = np.sqrt(2) * np.eye(2)
check('notebook box, the Rashba bond is sqrt 2 times a rotation by 90 degrees about y, removed by turning the spin axes '
      'by -90 degrees per site', np.allclose(Mh[2:4, 0:2], np.sqrt(2) * rot(-np.pi / 2)) and np.allclose(Mg, plain), 'ok')


INFO = {}


def run(seed, rashba=True, maxite=4000):
    np.random.seed(seed)
    kw = {} if maxite is None else dict(maxite=maxite)                  # None is the call of the cell, with no maxite
    try:
        hm, e = rashba_chain(rashba).get_mean_field_hamiltonian(U=10., mf="XY", mix=0.9, return_total_energy=True,
                                                               verbose=0, **kw)
    except Exception as ex:
        return type(ex).__name__, None
    m = np.array([np.real(hm.get_vev(c)) for c in ('mx', 'my', 'mz')]).T
    f = np.array([np.real(hm.extract(c)) for c in ('mx', 'my', 'mz')]).T
    n_ = m / np.linalg.norm(m, axis=1)[:, None]
    big = np.abs(m) > 0.05
    INFO[(seed, rashba, maxite)] = (np.max(np.abs(n_[:, 2])), (f[big] / m[big]).min(), (f[big] / m[big]).max())
    return e, [np.degrees(np.arccos(np.clip(n_[i] @ n_[i + 1], -1, 1))) for i in range(9)]


runs = [run(s) for s in range(8)]
mids = [np.mean(a[3:6]) for e, a in runs]
check('notebook box and try-it, eight random guesses give the same energy within 1e-5 and angles from run to run between '
      '90 and 180 degrees', max(e for e, a in runs) - min(e for e, a in runs) < 1e-5 and max(mids) - min(mids) > 20
      and all(90 - 1 < x < 180 for e, a in runs for x in a), ([round(e, 6) for e, a in runs], np.round(mids, 1)))
e0, a0 = run(0, rashba=False)
check('try-it, without the Rashba line the neighbors are antiparallel, within 1 degree', all(x > 179 for x in a0),
      (round(min(a0), 3), round(max(a0), 3)))
# corrected after the independent check of 2026-11-22 (k8): with the default maxite=1000 the loop stops without converging
# in most runs. Of the guesses 0 to 7, at least five raise MeanFieldConvergenceError in the development tree (seven did when
# this was written, all but the seed 1), and all eight converge with maxite=4000. The release 0.0.96 was not run.
import inspect
from pyqula.scftk import spinspin as _spinspin
fails = [run(s, maxite=None)[0] for s in range(8)]
nfail = sum(isinstance(f, str) for f in fails)
check('try-it, the default maxite of the loop is 1000, with it most of the guesses 0 to 7 do not converge in the call of '
      'the cell, at least 5 of 8, and with maxite=4000 all of them do',
      'maxite = 1000 if maxite is _MAXITE_UNSET else maxite' in inspect.getsource(_spinspin)
      and nfail >= 5 and isinstance(fails[0], str) and isinstance(fails[2], str)
      and all(not isinstance(r[0], str) for r in runs), (nfail, fails))
# corrected after the independent check of 2026-11-22 (k1): the guess mf="XY" is a random field in the plane xy, the moments
# of the solution leave this plane, and the arrows of the cell, extract("mx") and extract("my"), are the x and y components of
# the mean field -U m/2, which points opposite to the moment. In the frame turned by 90 degrees per site about y the
# staggered moment is one unit vector n, so the moments of the chain are n turned by j 90 degrees about y on site j, with
# alternating sign. They all lie in the plane xy only for n along y, the angle of 180 degrees, and for any other n half of
# them have the component n_x or n_z along z. The threshold 0.1 leaves room for runs that land close to 180 degrees.
import inspect
from pyqula import meanfield as _mfmod
gsrc = inspect.getsource(_mfmod._guess_randomXY)
Ry90 = np.array([[0, 0, 1.], [0, 1, 0], [-1, 0, 0]])
rngc = np.random.default_rng(3)
cone = []
for nvec in [np.array([0, 1., 0])] + [v / np.linalg.norm(v) for v in rngc.normal(size=(20, 3))]:
    lab = np.array([(-1) ** j * np.linalg.matrix_power(Ry90, j) @ nvec for j in range(10)])
    cone.append((abs(nvec[1]), np.abs(lab[:, 2]).max(), lab[0] @ lab[1], -nvec[1] ** 2))
zr = [INFO[(s, True, 4000)][0] for s in range(8)]
fr = [INFO[(s, True, 4000)][1:] for s in range(8)]
check('notebook box, the guess XY is random in the plane xy, the moments of the solution leave it, max |m_z|/|m| above 0.1 '
      'in each of the eight runs, the drawn mean field is -U/2 = -5 times the moment, and on the cone of the turned frame '
      'the moments are in the plane xy only for n along y',
      'np.random.random()-0.5,np.random.random()-0.5,0.' in gsrc and all(z > 0.1 for z in zr)
      and all(abs(a + 5) < 0.01 and abs(b + 5) < 0.01 for a, b in fr)
      and cone[0][1] < 1e-12 and all(c[1] > 0.05 for c in cone[1:]) and all(abs(c[2] - c[3]) < 1e-12 for c in cone),
      (np.round(zr, 3), np.round(fr, 3).tolist()[:2]))
page = open(os.path.join(REPO, 'webnotes', 'pages', 'session06', '11-superexchange-as-the-origin-of-ferromagnetic-coupling.md'),
            encoding='utf-8').read()
check('notebook box and try-it, the page says that the moments leave the plane and that most runs need maxite=4000',
      'The moments of the solution leave this plane' in page and 'stops without converging in most runs' in page
      and 'with the moments in the plane.' not in page, 'found')
