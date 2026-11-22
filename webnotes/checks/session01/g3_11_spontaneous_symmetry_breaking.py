"""Session 1, the numbers that page 11 (Section 1.11a, spontaneous symmetry breaking) quotes and that no figure script
asserts. One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an
assert, here or in the figure script that draws it. The figure scripts of the page assert their own numbers:
ising_splitting.py (the even ground state, the splitting that falls with L, the slope within 0.15 of log(g/J)) and
tunnel_split.py (the even and the odd state, 2 Delta = 0.92, and the smaller splitting of a higher barrier).

This script checks the key box, the fold on the splitting of the open Ising chain (with E_0 = -J(L-1), the cost 2J
of each bond of opposite spins and the two orders of L = 3 that flip from one end to the other), the feedback of the
quizzes, the solution of the problem with two biased minima, the sentence that the splitting of the chain is twice the
amplitude of the matrix of the problem, and the parameters of the caption of ising_splitting.svg, evaluated from the
syntax tree of its script. The Ising chain H = -J sum sz_i sz_{i+1} - g sum sx_i is solved by
exact diagonalization, and the fold by the sum over the orders of the spin flips, which is a second route to the
splitting. It finds nothing on disk and writes no file."""
import itertools

import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


J = 1.0
SX = np.array([[0., 1.], [1., 0.]])
SZ = np.diag([1., -1.])


def op(o, i, L):
    return np.kron(np.kron(np.eye(2 ** i), o), np.eye(2 ** (L - i - 1)))


def ising(L, g):
    """The two lowest energies of the open chain, and the parity of the ground state under the flip of all spins."""
    H = np.zeros((2 ** L, 2 ** L))
    for i in range(L - 1):
        H -= J * op(SZ, i, L) @ op(SZ, i + 1, L)
    for i in range(L):
        H -= g * op(SX, i, L)
    E, V = np.linalg.eigh(H)
    P = np.eye(1)
    for i in range(L):
        P = np.kron(P, SX)
    return E[0], E[1], V[:, 0] @ P @ V[:, 0]


def split(L, g):
    E0, E1, _ = ising(L, g)
    return E1 - E0


# the key box, the ground state is even, so symmetric, and Delta ~ 2J (g/J)^L for g << J
for g in (0.3, 0.5):
    par = [ising(L, g)[2] for L in range(1, 9)]
    check('the ground state is even under the flip of all spins, L = 1 to 8, g = %.1f J' % g,
          np.allclose(par, 1), np.round(par, 8))
g = 0.05
r = split(5, g) / (2 * J * (g / J) ** 5)
check('g << J, Delta = 2J (g/J)^L within 1 percent at g = 0.05 J and L = 5', abs(r - 1) < 0.01, r)

# the fold, the simplest cases
for g in (0.3, 0.5):
    check('L = 1, the splitting is 2g, g = %.1f J' % g, np.isclose(split(1, g), 2 * g), split(1, g))
    exact2 = np.sqrt(J ** 2 + 4 * g ** 2) - J
    check('L = 2, the splitting is sqrt(J^2 + 4g^2) - J, g = %.1f J' % g, np.isclose(split(2, g), exact2), exact2)
g = 1e-3
check('L = 2, sqrt(J^2 + 4g^2) - J is 2g^2/J for g << J', np.isclose((np.sqrt(J ** 2 + 4 * g ** 2) - J) / (2 * g ** 2 / J), 1, atol=1e-5),
      (np.sqrt(J ** 2 + 4 * g ** 2) - J) / (2 * g ** 2 / J))


def orders(L):
    """The products 1/((E_1 - E_0)(E_2 - E_0)...(E_{L-1} - E_0)), one per order of the L flips, in units of J."""
    out = []
    for perm in itertools.permutations(range(L)):
        s = np.ones(L)
        prod = 1.0
        for site in perm[:-1]:
            s[site] = -1
            prod *= -J * np.sum(s[:-1] * s[1:]) + J * (L - 1)       # E_k - E_0, 2J per bond with opposite spins
        out.append(1 / prod)
    return np.array(out)


o2 = orders(2)
check('L = 2, two orders, each through one bond of opposite spins, E_1 - E_0 = 2J', np.allclose(o2, 1 / (2 * J)), o2)
g = 0.3
t2 = (-g) ** 2 * np.sum(1 / (-1 / o2))                               # (-g)^2 / (E_0 - E_1), summed over the orders
check('L = 2, t_2 = 2 g^2 / (-2J) = -g^2/J', np.isclose(t2, -g ** 2 / J), t2)
shift2 = -np.sum(g ** 2 * o2)                                        # one flip and back, sum of g^2/(E_0 - E_1)
check('L = 2, the same order shifts both states by -g^2/J', np.isclose(shift2, -g ** 2 / J), shift2)
E0 = -J * (2 - 1)
Heff = np.array([[E0 + shift2, t2], [t2, E0 + shift2]])
w, v = np.linalg.eigh(Heff)
check('L = 2, the even combination is lower, at E_0 - 2g^2/J, the odd one at E_0, the splitting 2g^2/J',
      np.isclose(v[0, 0], v[1, 0]) and np.allclose(w, [E0 - 2 * g ** 2 / J, E0]) and np.isclose(w[1] - w[0], 2 * g ** 2 / J), w)
for g in (0.3, 0.01):
    Ee, Eo, _ = ising(2, g)
    check('L = 2, the exact energies are -sqrt(J^2 + 4g^2) and -J, g = %g J' % g, np.isclose(Ee, -np.sqrt(J ** 2 + 4 * g ** 2)) and np.isclose(Eo, -J), (Ee, Eo))
g = 0.01
Ee, Eo, _ = ising(2, g)
check('L = 2, the second order gives the exact energies up to g^4, g = 0.01 J', abs(Ee - (-J - 2 * g ** 2 / J)) < 10 * g ** 4 and abs(Eo + J) < 1e-12, Ee + J + 2 * g ** 2)
g = 0.3
for L in (3, 4):                                                     # the second order shifts all up and all down equally
    up = np.ones(L)
    sh = [sum(g ** 2 / (-J * np.sum(s[:-1] * s[1:]) - (-J * np.sum(s0[:-1] * s0[1:])))
              * -1 for s in [s0 * np.where(np.arange(L) == i, -1, 1) for i in range(L)]) for s0 in (up, -up)]
    check('L = %d, the second-order shift of all up equals the one of all down' % L, np.isclose(sh[0], sh[1]), sh)
o3 = np.sort(orders(3))
check('L = 3, the six orders give 1/(8J^2) four times and 1/(4J^2) twice, sum 1/J^2',
      np.allclose(o3, [1 / 8] * 4 + [1 / 4] * 2) and np.isclose(o3.sum(), 1 / J ** 2), o3)
by_order = dict(zip(itertools.permutations(range(3)), orders(3)))
ends = {p: v for p, v in by_order.items() if np.isclose(v, 1 / (4 * J ** 2))}
check('L = 3, the two orders with 1/(4J^2) flip the spins from one end to the other, (0,1,2) and (2,1,0)',
      set(ends) == {(0, 1, 2), (2, 1, 0)} and all(np.isclose(v, 1 / (8 * J ** 2)) for p, v in by_order.items() if p not in ends),
      sorted(ends))


def opposite_bonds(L):
    """The number of bonds between two opposite spins in each basis state, sz = +1 for the bit 0."""
    out = []
    for idx in range(2 ** L):
        s = np.array([1 - 2 * ((idx >> (L - 1 - i)) & 1) for i in range(L)])
        out.append(np.sum(s[:-1] != s[1:]))
    return np.array(out)


for L in range(2, 9):                                                # g = 0: H is diagonal, E_0 = -J(L-1), 2J per bond
    H0 = np.zeros((2 ** L, 2 ** L))
    for i in range(L - 1):
        H0 -= J * op(SZ, i, L) @ op(SZ, i + 1, L)
    diag = np.diag(H0)
    ok = np.allclose(H0, np.diag(diag)) and np.allclose(diag, -J * (L - 1) + 2 * J * opposite_bonds(L))
    ok = ok and np.isclose(diag.min(), -J * (L - 1)) and np.sum(np.isclose(diag, -J * (L - 1))) == 2
    check('g = 0, L = %d, E_0 = -J(L-1) for all up and all down, and each bond of opposite spins costs 2J' % L, ok, diag.min())
sums = [orders(L).sum() * J ** (L - 1) for L in range(2, 8)]
check('the sum over the L! orders is 1/J^(L-1), for L = 2 to 7', np.allclose(sums, 1), np.round(sums, 12))
for L in (2, 3, 5, 6):
    tL = (-g) ** L * (-1) ** (L - 1) * orders(L).sum()
    check('t_L = -g^L/J^(L-1), L = %d' % L, np.isclose(tL, -g ** L / J ** (L - 1)), tL)

# the fold, the numbers of the figure for g = 0.3 J
g = 0.3
d6, d8 = split(6, g), split(8, g)
low6, low8 = 2 * J * (g / J) ** 6, 2 * J * (g / J) ** 8
check('exact diagonalization, Delta = 1.33e-3 J at L = 6', '%.2e' % d6 == '1.33e-03', d6)
check('exact diagonalization, Delta = 1.19e-4 J at L = 8', '%.2e' % d8 == '1.19e-04', d8)
check('lowest order 2J (g/J)^L, 1.46e-3 J at L = 6', '%.2e' % low6 == '1.46e-03', low6)
check('lowest order 2J (g/J)^L, 1.31e-4 J at L = 8', '%.2e' % low8 == '1.31e-04', low8)
check('the exact values are smaller by 1 - (g/J)^2 = 0.91', '%.2f' % (d6 / low6) == '0.91' and '%.2f' % (d8 / low8) == '0.91'
      and '%.2f' % (1 - g ** 2) == '0.91', (d6 / low6, d8 / low8))
check('two more sites make Delta smaller by 11.1 = (J/g)^2, in both', '%.1f' % (d6 / d8) == '11.1' and '%.1f' % (low6 / low8) == '11.1'
      and '%.1f' % ((J / g) ** 2) == '11.1', (d6 / d8, low6 / low8))
for g in (0.3, 0.5):
    rel = split(8, g) / (2 * J * (1 - (g / J) ** 2) * (g / J) ** 8) - 1
    check('exact form 2J(1 - (g/J)^2)(g/J)^L within 1e-4 at L = 8, g = %.1f J' % g, abs(rel) < 1e-4, rel)

# the quiz with equations as options: 1/L would give 8/6 = 4/3 from L = 6 to L = 8, the chain gives 11.1
check('a splitting 1/L would fall by 4/3 from L = 6 to L = 8', np.isclose(8 / 6, 4 / 3), 8 / 6)
check('the exact chain falls by 11.1 at the same g, so Delta is not g with no L', abs(d6 / d8 - 11.1) < 0.05 and d6 / d8 > 8, d6 / d8)

# the first quiz: the matrix of the two minima, the ground state (1,1)/sqrt2 with the energy -Delta
D = 0.37
w, v = np.linalg.eigh(np.array([[0, -D], [-D, 0]]))
check('two minima with -Delta between them, ground state (1,1)/sqrt2 at -Delta', np.isclose(w[0], -D) and np.isclose(abs(v[0, 0]), abs(v[1, 0])) and v[0, 0] * v[1, 0] > 0, w)
check('two minima, the splitting at h = 0 is 2 Delta', np.isclose(w[1] - w[0], 2 * D), w[1] - w[0])
# the problem says that the Delta of the Ising chain is the splitting, twice the amplitude |t_L| of the 2x2 matrix
g, L = 0.05, 5
tL = -g ** L / J ** (L - 1)
check('Ising chain, the splitting Delta is twice the amplitude |t_L|, within 1 percent at g = 0.05 J and L = 5',
      abs(split(L, g) / (2 * abs(tL)) - 1) < 0.01, split(L, g) / abs(tL))

# the problem: the weight of the ground state on the first minimum is (1 + h/sqrt(h^2 + Delta^2))/2
for hD in (0.0, 0.3, 1.0, 10.0):
    h = hD * D
    w, v = np.linalg.eigh(np.array([[-h, -D], [-D, h]]))
    R = np.sqrt(h ** 2 + D ** 2)
    check('problem, the ground state has the energy -sqrt(h^2 + Delta^2), h = %g Delta' % hD, np.isclose(w[0], -R), w[0])
    check('problem, weight on the first minimum, h = %g Delta' % hD, np.isclose(v[0, 0] ** 2, 0.5 * (1 + h / R)), v[0, 0] ** 2)
    a = np.sqrt(0.5 * (1 + h / R))
    b = np.sqrt(0.5 * (1 - h / R))
    check('problem, (R - h) a = Delta b and Delta^2/(2R(R-h)) = (R+h)/(2R), h = %g Delta' % hD,
          np.isclose((R - h) * a, D * b) and (hD == 0 or np.isclose(D ** 2 / (2 * R * (R - h)), (R + h) / (2 * R))), (a, b))
check('problem, the weight is 0.85 at h = Delta', '%.2f' % (0.5 * (1 + 1 / np.sqrt(2))) == '0.85', 0.5 * (1 + 1 / np.sqrt(2)))
check('problem, the weight is 0.998 at h = 10 Delta', '%.3f' % (0.5 * (1 + 10 / np.sqrt(101))) == '0.998', 0.5 * (1 + 10 / np.sqrt(101)))
# the caption of the figure of the Ising chain: g = 0.3 J and 0.5 J, L = 2 to 14, exact diagonalization. The figure
# script is not changed by this page, and running it would write its SVG, so its parameters are evaluated from its
# syntax tree: the value of Ls, the tuple of the loop over g and the value of J, at the top level of the script.
import ast  # noqa: E402
import os  # noqa: E402
src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                        'figures', 'session01', 'ising_splitting.py')).read()
tree = ast.parse(src)
values = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        if node.targets[0].id in ('Ls', 'J'):
            values[node.targets[0].id] = eval(compile(ast.Expression(node.value), 'ising_splitting.py', 'eval'), {'np': np})
    if isinstance(node, ast.For) and isinstance(node.target, ast.Name) and node.target.id == 'g':
        values.setdefault('g', []).append(ast.literal_eval(node.iter))
check('caption, the figure draws g = 0.3 J and g = 0.5 J, with J = 1',
      values.get('J') == 1.0 and values.get('g') and all(tuple(v) == (0.3, 0.5) for v in values['g']), values.get('g'))
Ls = np.asarray(values.get('Ls'))
check('caption, the figure draws L = 2 to 14, chains of up to 14 spins',
      list(Ls) == list(range(2, 15)) and Ls.min() == 2 and Ls.max() == 14, [int(x) for x in Ls])
print('all checks of page 11 hold')
