"""Session 4, the numbers that page 08 (Section 4.8) quotes. The page has no figure script of its own, so every number
of its key box, its fold, its quizzes and its problem is asserted here, in the order of the page.

The bond phases of (4.4) are written in units of phi, the sum of the phases around one plaquette, as in Figure 4.2 and
in figures/session04/plaquette_gauge.py. In these units a phase is the line integral of A along the bond divided by
the flux B a^2 of one plaquette, so no factor of (4.4) enters. The lattice constant is a = 1. It finds the repository
from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session04/g2_08_gauges.py"""
import sys
sys.dont_write_bytecode = True

import numpy as np
import sympy as sp


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


x, y, B, s = sp.symbols('x y B s', real=True)
A_L = sp.Matrix([0, B * x])
A_S = sp.Matrix([-B * y / 2, B * x / 2])


def curl(A):
    return sp.simplify(sp.diff(A[1], x) - sp.diff(A[0], y))


# the key box: both gauges have the curl B z
check('key box, the curl of the Landau and of the symmetric gauge is B', curl(A_L) == B and curl(A_S) == B,
      (curl(A_L), curl(A_S)))


def line(A, p, q):
    """The line integral of A along the straight bond from p to q, in units of B a^2."""
    r = sp.Matrix(p) + s * (sp.Matrix(q) - sp.Matrix(p))
    integrand = (A.subs({x: r[0], y: r[1]}, simultaneous=True).T * (sp.Matrix(q) - sp.Matrix(p)))[0]
    return sp.simplify(sp.integrate(integrand, (s, 0, 1)) / B)


def plaquette(A, X, Y):
    """The four bond phases of the plaquette with the lower left corner (X, Y), counterclockwise from the bottom bond."""
    c = [(X, Y), (X + 1, Y), (X + 1, Y + 1), (X, Y + 1)]
    return [line(A, c[i], c[(i + 1) % 4]) for i in range(4)]


X, Y = sp.symbols('X Y', real=True)
landau, symmetric = plaquette(A_L, X, Y), plaquette(A_S, X, Y)
check('fold, the Landau gauge gives 0, X + 1, 0, -X with the sum 1', landau == [0, X + 1, 0, -X] and sp.simplify(sum(landau)) == 1,
      landau)
check('fold, the symmetric gauge gives -Y/2, (X+1)/2, (Y+1)/2, -X/2 with the sum 1',
      [sp.simplify(v - w) for v, w in zip(symmetric, [-Y / 2, (X + 1) / 2, (Y + 1) / 2, -X / 2])] == [0, 0, 0, 0]
      and sp.simplify(sum(symmetric)) == 1, symmetric)
at21 = ([v.subs({X: 2, Y: 1}) for v in landau], [v.subs({X: 2, Y: 1}) for v in symmetric])
check('fold, the plaquette at (2, 1): 0, 3, 0, -2 and -1/2, 3/2, 1, -1, as plaquette_gauge.py draws',
      at21 == ([0, 3, 0, -2], [sp.Rational(-1, 2), sp.Rational(3, 2), 1, -1]), at21)
# Stokes: the loop integral is the integral of the curl over the square, B a^2 for any (X, Y)
check('fold, Stokes, the integral of the curl over one plaquette is B a^2 in both gauges',
      all(sp.simplify(sp.integrate(sp.integrate(curl(A), (x, X, X + 1)), (y, Y, Y + 1)) / B) == 1 for A in (A_L, A_S)), True)

# the first quiz: H = [p_x^2 + (p_y - e B x)^2]/2m does not contain y, and it contains x
check('quiz 1, A_L does not depend on y and depends on x', all(sp.diff(c, y) == 0 for c in A_L) and sp.diff(A_L[1], x) == B, True)

# the second quiz: the flux of one plaquette of area a^2 is B a^2 in both gauges, the sum of the four line integrals
check('quiz 2, the flux through a plaquette is B a^2 in both gauges', sp.simplify(sum(landau)) == sp.simplify(sum(symmetric)) == 1, True)

# the third quiz: the curl of (-By, 0), (By, 0) and (0, By), the page says B, -B and 0
opts = {'(-By,0,0)': sp.Matrix([-B * y, 0]), '(By,0,0)': sp.Matrix([B * y, 0]), '(0,By,0)': sp.Matrix([0, B * y])}
curls = {k: curl(v) for k, v in opts.items()}
check('quiz 3, the curls are B, -B and 0', curls == {'(-By,0,0)': B, '(By,0,0)': -B, '(0,By,0)': 0}, curls)
check('quiz 3, (-By, 0, 0) differs from A_L by the gradient of -Bxy',
      sp.simplify(opts['(-By,0,0)'] - A_L - sp.Matrix([sp.diff(-B * x * y, x), sp.diff(-B * x * y, y)])) == sp.zeros(2, 1), True)
check('quiz 3, (0, By, 0) is the gradient of B y^2 / 2',
      sp.simplify(opts['(0,By,0)'] - sp.Matrix([sp.diff(B * y ** 2 / 2, x), sp.diff(B * y ** 2 / 2, y)])) == sp.zeros(2, 1), True)

# the problem: A_S = A_L + grad chi with chi = -B x y / 2
chi = -B * x * y / 2
grad = sp.Matrix([sp.diff(chi, x), sp.diff(chi, y)])
check('problem, A_S - A_L = grad(-B x y / 2)', sp.simplify(A_S - A_L - grad) == sp.zeros(2, 1), grad.T)
# each bond phase changes by chi(end) - chi(start), in units of B a^2: at (2, 1) this is -1/2, -3/2, 1, 1
corners = [(2, 1), (3, 1), (3, 2), (2, 2)]
chi_c = [sp.simplify(chi.subs({x: p[0], y: p[1]}) / B) for p in corners]
check('problem, chi/B at the corners (2,1), (3,1), (3,2), (2,2) is -1, -3/2, -3, -2',
      chi_c == [-1, sp.Rational(-3, 2), -3, -2], chi_c)
dchi =[sp.simplify((chi.subs({x: q[0], y: q[1]}) - chi.subs({x: p[0], y: p[1]})) / B)
        for p, q in zip(corners, corners[1:] + corners[:1])]
diff = [sp.simplify(a - b) for a, b in zip(at21[1], at21[0])]
check('problem, at (2, 1) the symmetric minus the Landau phases are -1/2, -3/2, 1, 1, the differences of chi, with the sum 0',
      dchi == diff == [sp.Rational(-1, 2), sp.Rational(-3, 2), 1, 1] and sum(dchi) == 0, dchi)


# the problem: a 10 x 10 island with the phase phi = pi/6 around each plaquette has the same levels in both gauges
def island(L, phi, gauge):
    pos = [(i, j) for i in range(L) for j in range(L)]
    idx = {p: n for n, p in enumerate(pos)}
    Hm = np.zeros((L * L, L * L), complex)
    for (i, j) in pos:
        for (di, dj) in ((1, 0), (0, 1)):
            q = (i + di, j + dj)
            if q not in idx:
                continue
            if gauge == 'landau':
                ph = phi * i * dj                                   # A = B (0, x): the vertical bond in column i
            else:
                ph = phi * (-j * di + i * dj) / 2                   # A = B/2 (-y, x), the line integral of a straight bond
            Hm[idx[q], idx[(i, j)]] = -np.exp(1j * ph)
            Hm[idx[(i, j)], idx[q]] = -np.exp(-1j * ph)
    return np.linalg.eigvalsh(Hm)


eL, eS = island(10, np.pi / 6, 'landau'), island(10, np.pi / 6, 'symmetric')
e0 = island(10, 0.0, 'landau')
check('problem, the 10 x 10 island with the phase phi = pi/6 around each plaquette has the same levels in both gauges, '
      'to 1e-10, and they differ from those with no field', np.max(np.abs(eL - eS)) < 1e-10 and np.max(np.abs(eL - e0)) > 0.1,
      (np.max(np.abs(eL - eS)), np.max(np.abs(eL - e0))))
print('all checks of page 08 hold')
