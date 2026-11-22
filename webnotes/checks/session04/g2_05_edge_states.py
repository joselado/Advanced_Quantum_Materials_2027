"""Session 4, the numbers that page 05 (Section 4.5) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a box is an
assert, here or in the figure script that draws it. The figure scripts ribbon_three.py and _g2_qhribbon.py assert their
crossings when they draw, and build.py --verify runs only this folder, so the numbers of their caption, alt text and
options are asserted here again on the same grids. This script holds, in the order of the page: the count |C1 - C2| of
the key box, the five levels, the walls and the crossings of ribbon_three, the counts of the three options of the
picture quiz and the reversal of the field of its explanation, the ribbon with a step of the potential of the problem,
and the numbers of the lab box. It finds the repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session04/g2_05_edge_states.py"""
import os
import sys
sys.dont_write_bytecode = True

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, '..', '..', 'figures', 'session04')
sys.path.insert(0, FIG)
sys.path.insert(0, os.path.join(FIG, '..'))
import _g2_qhribbon as qh  # noqa: E402


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# the key box: N filled levels next to the vacuum give N modes at the edge, on the ribbon of the figures
ks = np.linspace(-3.5, qh.W + 3.5, 500)
E = qh.levels(ks, nlev=6)
qh.check_bulk(ks, E)
counts = {mu: qh.edge_counts(ks, E, mu) for mu in (1.0, 2.0, 3.0)}
check('key box, the edge of N filled levels has N modes at each wall, for N = 1, 2, 3',
      all(counts[mu] == (int(mu), int(mu)) for mu in counts), counts)

# the figure ribbon_three in the feedback of the second quiz, on the grid of ribbon_three.py (500 points, 6 levels).
# Its alt text says five flat levels: the levels n + 1/2 for n = 0 to 4 lie below the top 4.8 of its energy axis and the
# sixth does not. Its caption says three crossings at each edge at mu = 3, and that k_y l_B is measured from the left
# wall, so 0 and 12 are the walls: a guiding center on a wall lifts the lowest level to 1.5 hbar omega_c.
src = open(os.path.join(FIG, 'ribbon_three.py')).read()
assert 'ax.set_ylim(0, 4.8)' in src and 'np.linspace(-3.5, W + 3.5, 500)' in src and 'nlev=6' in src
ytop = 4.8
mid = np.argmin(np.abs(ks - qh.W / 2))
check('ribbon_three, five flat levels 0.5 to 4.5 below the top 4.8 of the energy axis, and the sixth above it',
      np.allclose(E[mid, :5], np.arange(5) + 0.5, atol=1e-3) and E[mid, 4] < ytop < E[mid, 5], np.round(E[mid], 3))
check('ribbon_three, three crossings at each edge at mu = 3', qh.edge_counts(ks, E, 3.0) == (3, 3), qh.edge_counts(ks, E, 3.0))
kw = np.array([0.0, qh.W])
Ew = qh.levels(kw, nlev=1)[:, 0]
check('ribbon_three, k_y l_B = 0 and 12 put the guiding center on the left and on the right wall, the walls are at 0 and 12',
      qh.W == 12.0 and np.allclose(Ew, 1.5, atol=2e-3), np.round(Ew, 4))

# the picture quiz, on the grid of the three options of _g2_qhribbon.option (400 points from -3 to 15, 5 levels):
# mu = 1, 2, 3 give 1, 2 and 3 filled levels and as many crossings at each edge
ko = np.linspace(-3.0, qh.W + 3.0, 400)
Eo = qh.levels(ko, nlev=5)
mo = np.argmin(np.abs(ko - qh.W / 2))
opt = {mu: (qh.edge_counts(ko, Eo, mu), int(np.sum(Eo[mo] < mu))) for mu in (1.0, 2.0, 3.0)}
check('picture quiz, the options with mu = 1, 2, 3 have 1, 2, 3 filled levels and as many crossings at each edge',
      all(opt[mu] == ((int(mu), int(mu)), int(mu)) for mu in opt), opt)

# the explanation of the picture quiz: when the field is reversed the modes of each edge move the other way, the number
# of modes stays, and sigma_xy changes sign. In the ribbon the reversed field puts the guiding center at x0 = -k_y l_B^2,
# so the levels at k_y are those of -k_y.
kr = -ks[::-1]
Er = qh.levels(-kr, nlev=6)


def wall_slopes(kk, EE, mu):
    """The sign of dE/dk_y of each crossing, at the left wall (x near 0) and at the right wall (x near W)."""
    out = {'left': [], 'right': []}
    for k, n in qh.crossings(kk, EE, mu):
        j = np.argmin(np.abs(kk - k))
        sgn = np.sign(EE[min(j + 1, len(kk) - 1), n] - EE[max(j - 1, 0), n])
        x0 = abs(k)                                      # the guiding center is k or -k, in units of l_B
        out['left' if x0 < qh.W / 2 else 'right'].append(int(sgn))
    return out


sl, slr = wall_slopes(ks, E, 3.0), wall_slopes(kr, Er, 3.0)
check('picture quiz, the reversed field keeps 3 modes at each wall and reverses their direction',
      sl == {'left': [-1] * 3, 'right': [1] * 3} and slr == {'left': [1] * 3, 'right': [-1] * 3}, (sl, slr))
# sigma_xy changes sign: the lowest Landau band of the square lattice with the phase (4.4) of A = (0, Bx), the flux
# +-1/12 per plaquette, has the Chern number -1 and +1 with the Omega of physcheck, the line of the conventions sheet.
# The Bloch factor of the bond from column q-1 to column 0 of the next cell is exp(-i k_x q), the same convention as the
# factor exp(-i k_y) of the vertical bonds, since H(k) = sum_d H(d) exp(-i k d) with d the displacement of the hop.
import physcheck  # noqa: E402


def harper(p, q, t=1.0):
    phi = 2 * np.pi * p / q

    def hk(k):
        H = np.diag([-2 * t * np.cos(k[1] - x * phi) for x in range(q)]).astype(complex)
        H += -t * (np.eye(q, k=1) + np.eye(q, k=-1))
        H[0, q - 1] += -t * np.exp(-1j * k[0] * q)
        H[q - 1, 0] += -t * np.exp(1j * k[0] * q)
        return H
    return hk, np.array([[2 * np.pi / q, 0.0], [0.0, 2 * np.pi]])


cs = {p: round(float(physcheck.chern_links(*harper(p, 12), bands=0, nk=24)), 6) for p in (1, -1)}
check('picture quiz, the Chern number of the lowest Landau band changes sign with the field, -1 and +1 for the flux +-1/12',
      cs == {1: -1.0, -1: 1.0}, cs)

# the problem: N = 2 on the left half and N = 5 on the right half give |5 - 2| = 3 modes along the line between them.
# The solution computes it on a ribbon of 24 l_B with a step of the potential of 3 hbar omega_c on its left half and the
# chemical potential 5 hbar omega_c, so the left half has 5 - 3 = 2 and the right half 5 filled levels.
Wd, mu, Vstep = 24.0, 5.0, 3.0
ks2 = np.linspace(-3.5, Wd + 3.5, 621)
E2 = qh.levels(ks2, width=Wd, npts=1800, nlev=9, V=lambda x: np.where(x < Wd / 2, Vstep, 0.0))
iL, iR = np.argmin(np.abs(ks2 - Wd / 4)), np.argmin(np.abs(ks2 - 3 * Wd / 4))
filled = (int(np.sum(E2[iL] < mu)), int(np.sum(E2[iR] < mu)))
check('problem, the two halves have 2 and 5 filled levels', filled == (2, 5)
      and np.allclose(E2[iL, :4], np.arange(4) + 0.5 + Vstep, atol=1e-3) and np.allclose(E2[iR, :4], np.arange(4) + 0.5, atol=1e-3),
      (filled, np.round(E2[iL, :3], 3), np.round(E2[iR, :3], 3)))
cr = qh.crossings(ks2, E2, mu)
at_left = [(k, n) for k, n in cr if k < 4]
at_step = [(k, n) for k, n in cr if Wd / 2 - 4 < k < Wd / 2 + 4]
at_right = [(k, n) for k, n in cr if k > Wd - 4]


def slope(k, n):
    j = np.argmin(np.abs(ks2 - k))
    return np.sign(E2[min(j + 1, len(ks2) - 1), n] - E2[max(j - 1, 0), n])


check('solution, crossings at the left wall, at the step and at the right wall, the page says 2, 3 and 5',
      (len(at_left), len(at_step), len(at_right)) == (2, 3, 5) and len(cr) == 10, (len(at_left), len(at_step), len(at_right)))
check('solution, the three modes at the step move in one direction, as the two at the left wall, and the five at the right wall '
      'in the other', all(slope(k, n) < 0 for k, n in at_step + at_left) and all(slope(k, n) > 0 for k, n in at_right),
      [slope(k, n) for k, n in at_left + at_step + at_right])
check('problem, |C1 - C2| with C1 = 2 and C2 = 5', abs(5 - 2) == len(at_step), abs(5 - 2))
# the solution says that the three modes move in the direction of the five modes of the right half along the line. The
# right half alone, a ribbon of 12 l_B with 5 filled levels, has at its left boundary, the line, 5 modes with dE/dk_y < 0,
# the sign of the three modes at the step.
k12 = np.linspace(-3.5, 15.5, 500)
E12 = qh.levels(k12, width=12.0, npts=1500, nlev=7)
left12 = [(k, n) for k, n in qh.crossings(k12, E12, mu) if k < 6]
sl12 = [int(np.sign(E12[min(np.argmin(np.abs(k12 - k)) + 1, 499), n] - E12[max(np.argmin(np.abs(k12 - k)) - 1, 0), n]))
        for k, n in left12]
check('solution, the right half alone has 5 modes at the line with dE/dk_y < 0, the direction of the 3 modes at the step',
      len(left12) == 5 and all(s < 0 for s in sl12) and all(slope(k, n) < 0 for k, n in at_step), sl12)

# the lab box: the abstract of arXiv 1412.3758 gives 0.00013+-0.00007 h/e2 (~3.35+-1.76 ohm); h/e^2 = 25.8 kOhm
h_planck, e_charge = 6.62607015e-34, 1.602176634e-19
rk = h_planck / e_charge ** 2
check('lab box, h/e^2 in kOhm, the page says 25.8', abs(rk / 1e3 - 25.8) < 0.05, round(rk / 1e3, 4))
check('lab box, 3.35 ohm is 0.00013 h/e^2 and 1.76 ohm is 0.00007 h/e^2, to the digits of the abstract',
      round(3.35 / rk, 5) == 0.00013 and round(1.76 / rk, 5) == 0.00007, (3.35 / rk, 1.76 / rk))
print('all checks of page 05 hold')
