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
