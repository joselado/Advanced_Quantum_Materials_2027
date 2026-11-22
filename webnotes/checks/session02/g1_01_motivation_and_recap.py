"""Session 2, the numbers that page 01 (Sections 2.1 and 2.2) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The field of the egg of the picture quiz is asserted in
figures/session02/_g1_egg.py, and this script runs its check() too, so that --verify sees those asserts. This script
holds the rest. It needs numpy, and matplotlib for that import, and writes no file."""
import itertools
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'figures', 'session02'))
import _g1_egg


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def field(charges, p):
    """The electric field at p of unit point charges, in units of q/(4 pi eps0) with the lengths in units of a."""
    p = np.asarray(p, float)
    e = np.zeros(len(p))
    for c in charges:
        d = p - np.asarray(c, float)
        e += d / np.linalg.norm(d) ** 3
    return e


# the quiz on the square: 4 rotations and 8 operations in all, and 45 degrees is not one of them
corners = {(1, 1), (-1, 1), (-1, -1), (1, -1)}
ops = []
for perm in itertools.permutations(range(2)):
    for signs in itertools.product((1, -1), repeat=2):
        M = np.zeros((2, 2))
        for i, j in enumerate(perm):
            M[i, j] = signs[i]
        if {tuple(np.round(M @ np.array(c)).astype(int)) for c in corners} == corners:
            ops.append(M)
rot = [M for M in ops if np.isclose(np.linalg.det(M), 1)]
r45 = np.array([[np.cos(np.pi / 4), -np.sin(np.pi / 4)], [np.sin(np.pi / 4), np.cos(np.pi / 4)]])
img = r45 @ np.array([1.0, 1.0])
check('the square has 4 rotations and 8 operations, the page says 4 and 8', len(rot) == 4 and len(ops) == 8,
      (len(rot), len(ops)))
check('45 degrees moves a corner to the middle of an edge direction, (0, sqrt2)', np.allclose(img, [0, np.sqrt(2)]),
      np.round(img, 4))
# the old feedback said "to the middle of an edge", and the page now says "beyond the middle of an edge": every corner
# lands on the line from the center through the middle (0, +-1) or (+-1, 0) of an edge, farther out than it, and none
# lands on a corner or inside the square
imgs = np.array([r45 @ np.array(c, float) for c in sorted(corners)])
mids = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]], float)
beyond = all(any(np.isclose(abs(p @ m), np.linalg.norm(p)) and p @ m > 1 for m in mids) for p in imgs)
check('45 degrees: each corner lands beyond the middle of an edge, at the distance sqrt2 > 1, outside the square',
      beyond and np.allclose(np.linalg.norm(imgs, axis=1), np.sqrt(2)) and not np.any(np.all(np.abs(imgs) <= 1 + 1e-12, axis=1)),
      np.round(imgs, 4).tolist())

# the picture quiz, first option: two equal charges at (+-d, 0) and the point (0, y) on the axis x = 0
e = field([(1, 0), (-1, 0)], (0, 1.5))
check('two charges at (+-1, 0), the field at (0, 1.5) has no x component', abs(e[0]) < 1e-12 and e[1] > 0, np.round(e, 4))
# the old version of this feedback, with the axis along x
e = field([(0, 1), (0, -1)], (1.5, 0))
check('two charges at (0, +-1), the field at (1.5, 0) has no y component', abs(e[1]) < 1e-12 and e[0] > 0, np.round(e, 4))

# the problem: four charges at (+-a, +-a)
sq = [(1, 1, 0), (-1, 1, 0), (-1, -1, 0), (1, -1, 0)]
e0 = field(sq, (0, 0, 0))
check('the field at the center vanishes', np.allclose(e0, 0), e0)
R90 = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
check('the rotation by 90 degrees maps the charges onto each other', {tuple(R90 @ np.array(c)) for c in sq} == set(sq), True)
ep = field(sq, (0, 1, 0))
check('at the middle of the edge, (0, a), the field is along y and away from the square, 4/(5 sqrt5) = 0.36',
      abs(ep[0]) < 1e-12 and abs(ep[2]) < 1e-12 and np.isclose(ep[1], 4 / (5 * np.sqrt(5))) and round(ep[1], 2) == 0.36,
      np.round(ep, 4))
near = field(sq[:2], (0, 1, 0))
far = field(sq[2:], (0, 1, 0))
check('the two charges of the edge cancel, the two others at the distance sqrt5 a give all of it',
      np.allclose(near, 0) and np.allclose(far, ep) and np.isclose(np.linalg.norm(np.array([1, 2])), np.sqrt(5)),
      (np.round(near, 4), np.round(far, 4)))
ez = field(sq, (0.3, 0.7, 0))
check('in the plane of the square the field has no z component', abs(ez[2]) < 1e-12, np.round(ez, 4))

# the picture quiz: the field of the egg and the three arrows, from the figure helper, and the 45 degrees of the alt text
_g1_egg.check()
dx, dy = _g1_egg.ARROWS['tilted']
check('the tilted arrow of the picture quiz makes 45 degrees with the mirror axis x = 0',
      np.isclose(np.degrees(np.arctan2(dx, dy)), 45.0), round(float(np.degrees(np.arctan2(dx, dy))), 4))

# the last sentences of the solution: one orbital per site, every eigenvalue of the rotation has one state, so the Fourier
# modes are the eigenstates. With two orbitals per cell, as in block_diagonal of Section 2.3, the block of the eigenvalue
# 1 is h0 + h1 + h1^T, a 2 x 2 matrix with an element off the diagonal, which still has to be diagonalized
h0 = np.array([[0.6, 1.0], [1.0, -0.6]])
h1 = np.array([[-0.7, 0.4], [0.25, 0.5]])
blk = h0 + h1 + h1.T
check('two orbitals per cell: the block of the eigenvalue 1 is [[-0.8, 1.65], [1.65, 0.4]], not diagonal',
      np.allclose(blk, [[-0.8, 1.65], [1.65, 0.4]]) and abs(blk[0, 1]) > 1, blk.round(4).tolist())
L = 4
R1 = np.roll(np.eye(L), 1, axis=0)
lam = np.linalg.eigvals(R1)
check('one orbital per site on a ring of 4 sites: the 4 eigenvalues of the rotation differ, one state each',
      len(set(np.round(lam, 9))) == L, np.round(lam, 6))
print('all checks of page 01 hold')
