"""Session 8, the numbers and the algebra that page 10 (Section 8.10, the emergent gauge symmetry and the flux) quotes,
checked with matrices.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. gauge_levels.py asserts the numbers of its caption (36 levels, 1e-12 after a
gauge rotation, the shift 0.36 with one flipped plaquette, the fluxes that add up to 23), and _g3_plaquette.py the flux
of each picture of the new quiz. This script checks the key box and the fold "Why the flux does not change under
(8.16)" on the fermion operators of two sites and on the hopping matrix of a lattice, the feedback of the three
quizzes, and the problem of the string for every n and every pair of rows on lattices of side 3 to 9. It writes no file."""
import itertools

import numpy as np

PAULI = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], complex)]


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def modes(m):
    """Annihilation operators of m fermion modes, with the Jordan-Wigner strings."""
    a, z = np.array([[0.0, 1.0], [0.0, 0.0]]), np.diag([1.0, -1.0])
    out = []
    for k in range(m):
        o = np.eye(1)
        for j in range(m):
            o = np.kron(o, z if j < k else (a if j == k else np.eye(2)))
        out.append(o.astype(complex))
    return out


def dag(x):
    return x.conj().T


def close(a, b, tol=1e-12):
    return np.abs(np.asarray(a) - np.asarray(b)).max() < tol


# ------------------------------------------------------------------------------------------------------------------
# (8.16) on the operators of two sites. The unitary W = exp(i sum_i theta_i n_i) gives W^dag f_i W = e^{i theta_i} f_i.
fiu, fid, fju, fjd = modes(4)
fi, fj = (fiu, fid), (fju, fjd)
ni = dag(fiu) @ fiu + dag(fid) @ fid
nj = dag(fju) @ fju + dag(fjd) @ fjd
th_i, th_j = 0.7, -1.9
W = np.diag(np.exp(1j * (th_i * np.real(np.diag(ni)) + th_j * np.real(np.diag(nj)))))
rot = lambda O: dag(W) @ O @ W
check('(8.16): W^dag f_i W = e^{i theta_i} f_i and W^dag f^dag_i W = e^{-i theta_i} f^dag_i',
      all(close(rot(f), np.exp(1j * th_i) * f) for f in fi) and all(close(rot(dag(f)), np.exp(-1j * th_i) * dag(f)) for f in fi)
      and all(close(rot(f), np.exp(1j * th_j) * f) for f in fj), 'ok')
spin = lambda fu, fd: [0.5 * sum(P[a, b] * (dag((fu, fd)[a]) @ (fu, fd)[b]) for a in range(2) for b in range(2)) for P in PAULI]
Si = spin(fiu, fid)
check('key box and fold: the spin (8.10) and the number of fermions of (8.11) do not change',
      all(close(rot(s), s) for s in Si) and close(rot(ni), ni), 'ok')
check('fold: every pair f^dag_ia f_ib of one site is unchanged, and f^dag_is f_js gets e^{-i(theta_i - theta_j)}',
      all(close(rot(dag(fi[a]) @ fi[b]), dag(fi[a]) @ fi[b]) for a in range(2) for b in range(2))
      and all(close(rot(dag(fi[s]) @ fj[s]), np.exp(-1j * (th_i - th_j)) * dag(fi[s]) @ fj[s]) for s in range(2)), 'ok')
SS = sum(a @ b for a, b in zip(Si, spin(fju, fjd)))
check('fold: the Heisenberg bond S_i.S_j does not change', close(rot(SS), SS), 'ok')
check('quiz: for theta_i = pi/2, f^dag_iup f_idn gets (-i)(i) = 1', abs((-1j) * (1j) - 1) < 1e-15, (-1j) * (1j))

# the hopping of (8.15) on a lattice: the coefficient gets e^{+i(theta_i - theta_j)} and the levels stay
L = 5
idx = lambda x, y: x + L * y
rng = np.random.default_rng(11)
M = np.zeros((L * L, L * L), complex)
for x, y in itertools.product(range(L), repeat=2):
    for dx, dy in ((1, 0), (0, 1)):
        if x + dx < L and y + dy < L:
            i, j = idx(x, y), idx(x + dx, y + dy)
            M[i, j] = rng.uniform(0.5, 1.5) * np.exp(1j * rng.uniform(0, 2 * np.pi))
            M[j, i] = np.conj(M[i, j])
theta = rng.uniform(0, 2 * np.pi, L * L)
Mp = np.exp(1j * (theta[:, None] - theta[None, :])) * M          # chi_ij -> e^{i(theta_i - theta_j)} chi_ij
U = np.diag(np.exp(1j * theta))
check('fold: with chi_ij -> e^{i(theta_i - theta_j)} chi_ij the hopping matrix is U M U^dag, and the levels do not change',
      close(Mp, U @ M @ dag(U)) and close(np.linalg.eigvalsh(Mp), np.linalg.eigvalsh(M), 1e-10), 'ok')


def flux(H, x, y):
    """The product of the hoppings around the plaquette with the lower left corner (x, y), counterclockwise, 1 2 3 4."""
    a, b, c, d = idx(x, y), idx(x + 1, y), idx(x + 1, y + 1), idx(x, y + 1)
    return H[a, b] * H[b, c] * H[c, d] * H[d, a]


ph = lambda z: np.angle(z)
fl = np.array([[flux(M, x, y) for x in range(L - 1)] for y in range(L - 1)])
flp = np.array([[flux(Mp, x, y) for x in range(L - 1)] for y in range(L - 1)])
check('key box and fold: the flux of every plaquette does not change, for random hoppings and random angles',
      close(flp, fl, 1e-10), np.abs(flp - fl).max())
# the expectation value of the bond operator of (8.12) gets the opposite phase, and its plaquette product stays
G = lambda H: (lambda v: v.conj() @ v.T)(np.linalg.eigh(H)[1][:, :len(H) // 2])       # G[i, j] = <f^dag_i f_j>
Gm, Gp = G(M), G(Mp)
check('fold: <f^dag_i f_j> in the ground state gets e^{-i(theta_i - theta_j)}, the opposite phase',
      close(Gp, np.exp(-1j * (theta[:, None] - theta[None, :])) * Gm, 1e-10), 'ok')
fg = np.array([[flux(Gm, x, y) for x in range(L - 1)] for y in range(L - 1)])
fgp = np.array([[flux(Gp, x, y) for x in range(L - 1)] for y in range(L - 1)])
check('fold: the product of <f^dag_i f_j> around a plaquette does not change either', close(fgp, fg, 1e-10), np.abs(fgp - fg).max())
t1, t2, t3, t4 = rng.uniform(0, 2 * np.pi, 4)
check('fold: (theta_1 - theta_2) + (theta_2 - theta_3) + (theta_3 - theta_4) + (theta_4 - theta_1) = 0',
      abs((t1 - t2) + (t2 - t3) + (t3 - t4) + (t4 - t1)) < 1e-12, 'ok')

# the quiz on the flux: the same angle on four sites, and theta_1 = pi/2
ts = np.full(4, 0.9)
same = np.array([np.exp(1j * (ts[a] - ts[(a + 1) % 4])) for a in range(4)])
check('quiz: the same angle theta = 0.9 on the four sites gives theta - theta = 0 on every link, while the sum of the '
      'four angles would be 4 theta = 3.6', close(same, 1) and abs(ts.sum() - 3.6) < 1e-12, same.round(12).tolist())
th = np.array([np.pi / 2, 0, 0, 0])
links = [np.exp(1j * (th[a] - th[(a + 1) % 4])) for a in range(4)]          # links 12, 23, 34, 41
check('quiz: theta_1 = pi/2 gives the link 12 the factor i and the link 41 the factor -i, with the product 1',
      abs(links[0] - 1j) < 1e-15 and abs(links[3] + 1j) < 1e-15 and abs(np.prod(links) - 1) < 1e-15, np.round(links, 6).tolist())

# the picture quiz: the plaquettes with two and four links at -1 are gauge rotations of the one with all +1
gauge = lambda t: np.round([np.exp(1j * (t[a] - t[(a + 1) % 4])).real for a in range(4)], 12)
check('quiz: theta = pi on the two sites of the left side, 1 and 4, gives -1 on the links 12 and 34',
      np.allclose(gauge([np.pi, 0, 0, np.pi]), [-1, 1, -1, 1]), gauge([np.pi, 0, 0, np.pi]).tolist())
check('quiz: theta = pi on two opposite corners, 1 and 3, gives -1 on all four links',
      np.allclose(gauge([np.pi, 0, np.pi, 0]), [-1, -1, -1, -1]), gauge([np.pi, 0, np.pi, 0]).tolist())
check('quiz: one link at -1 has the flux -1, which no rotation changes', np.prod([1, 1, 1, -1]) == -1
      and all(abs(np.prod([np.exp(1j * (t[a] - t[(a + 1) % 4])) for a in range(4)]) - 1) < 1e-12
              for t in rng.uniform(0, 2 * np.pi, (20, 4))), 'ok')

# ------------------------------------------------------------------------------------------------------------------
# the problem: n vertical links at -1 between the rows y0 and y0 + 1, from the left edge


def string_lattice(L, n, y0):
    """The hopping matrix of the open L x L lattice with chi = 1, and -1 on the vertical links (x, y0)-(x, y0+1), x < n."""
    ix = lambda x, y: x + L * y
    H = np.zeros((L * L, L * L))
    for x, y in itertools.product(range(L), repeat=2):
        for dx, dy in ((1, 0), (0, 1)):
            if x + dx < L and y + dy < L:
                s = -1.0 if (dx == 0 and y == y0 and x < n) else 1.0
                H[ix(x, y), ix(x + dx, y + dy)] = H[ix(x + dx, y + dy), ix(x, y)] = s
    F = np.array([[H[ix(x, y), ix(x + 1, y)] * H[ix(x + 1, y), ix(x + 1, y + 1)] * H[ix(x + 1, y + 1), ix(x, y + 1)]
                   * H[ix(x, y + 1), ix(x, y)] for x in range(L - 1)] for y in range(L - 1)])
    return H, F


ok, cases = True, 0
for L_ in range(3, 10):
    for y0 in range(L_ - 1):
        for n in range(1, L_ + 1):
            H, F = string_lattice(L_, n, y0)
            neg = [tuple(p) for p in np.argwhere(F < 0)]                   # (row y, column x) of the plaquettes
            if n <= L_ - 1:
                # the plaquette number m = n, counted from 1 at the edge, is the column x = n - 1
                ok = ok and neg == [(y0, n - 1)] and np.sum(F) == (L_ - 1) ** 2 - 2
            else:
                ok = ok and neg == []
            cases += 1
check('problem: for 1 <= n <= L-1 only the plaquette at the end of the string has Phi = -1, and for n = L none, '
      'on every lattice of side 3 to 9 and every pair of rows', ok, '%d cases' % cases)
H6, F6 = string_lattice(6, 3, 2)
check('problem: on the 6x6 lattice with n = 3 one of the 25 plaquettes has Phi = -1, and the fluxes add up to 23',
      F6.size == 25 and np.sum(F6 < 0) == 1 and np.sum(F6) == 23 and tuple(np.argwhere(F6 < 0)[0]) == (2, 2), np.sum(F6))
# the horizontal string from the bottom edge to the same plaquette, and the gauge rotation between the two strings
ix6 = lambda x, y: x + 6 * y
Hh = np.zeros((36, 36))
for x, y in itertools.product(range(6), repeat=2):
    for dx, dy in ((1, 0), (0, 1)):
        if x + dx < 6 and y + dy < 6:
            s = -1.0 if (dy == 0 and x == 2 and y <= 2) else 1.0
            Hh[ix6(x, y), ix6(x + dx, y + dy)] = Hh[ix6(x + dx, y + dy), ix6(x, y)] = s
Fh = np.array([[Hh[ix6(x, y), ix6(x + 1, y)] * Hh[ix6(x + 1, y), ix6(x + 1, y + 1)] * Hh[ix6(x + 1, y + 1), ix6(x, y + 1)]
                * Hh[ix6(x, y + 1), ix6(x, y)] for x in range(5)] for y in range(5)])
S = np.diag([-1.0 if (x <= 2 and y <= 2) else 1.0 for y in range(6) for x in range(6)])
check('solution: a horizontal string from the bottom edge to the same plaquette gives the same fluxes and levels, and '
      'theta = pi on the sites x, y <= 2 maps one string to the other',
      close(Fh, F6) and close(S @ H6 @ S, Hh) and close(np.linalg.eigvalsh(Hh), np.linalg.eigvalsh(H6), 1e-10),
      np.abs(np.linalg.eigvalsh(Hh) - np.linalg.eigvalsh(H6)).max())

# corrected on 2026-11-22, old text of the page: which flux is the ground state. Spinons at half filling on the square
# lattice with |chi| = 1, one spin, the energy of the filled levels per site. Route one, the infinite lattice on a k-mesh,
# -2(cos kx + cos ky) filled below zero for Phi = +1, and -2 sqrt(cos^2 kx + cos^2 ky) per two sites for Phi = -1. Route
# two, a periodic 24x24 lattice in real space, with the hopping (-1)^x along y for Phi = -1.
q_ = 2 * np.pi * (np.arange(600) + 0.5) / 600
QX, QY = np.meshgrid(q_, q_, indexing='ij')
eu_ = -2 * (np.cos(QX) + np.cos(QY))
e_zero = np.mean(np.where(eu_ < 0, eu_, 0))
e_pi = 0.5 * np.mean(-2 * np.sqrt(np.cos(QX) ** 2 + np.cos(QY) ** 2))


def torus_energy(L, pi_flux):
    idx = lambda x, y: (x % L) + L * (y % L)
    M = np.zeros((L * L, L * L))
    for x in range(L):
        for y in range(L):
            M[idx(x, y), idx(x + 1, y)] = M[idx(x + 1, y), idx(x, y)] = 1.0
            sy = (-1.0) ** x if pi_flux else 1.0
            M[idx(x, y), idx(x, y + 1)] = M[idx(x, y + 1), idx(x, y)] = sy
    w = np.linalg.eigvalsh(M)
    return w[:L * L // 2].sum() / (L * L)


t0, tp = torus_energy(24, False), torus_energy(24, True)
check('corrected, the flux of the ground state: per site and spin -8/pi^2 = -0.811 for Phi = +1 and -0.958 for Phi = -1, on '
      'a k-mesh and on a periodic 24x24 lattice, so the flux pi is lower',
      abs(e_zero + 8 / np.pi ** 2) < 1e-4 and abs(e_pi + 0.958) < 1e-3 and abs(t0 - e_zero) < 0.01 and abs(tp - e_pi) < 0.01
      and tp < t0 and e_pi < e_zero, (round(e_zero, 4), round(e_pi, 4), round(t0, 4), round(tp, 4)))


def open_lattice(L, links):
    """The coefficients of f^dag_i f_j on an open L x L lattice, 1 on every link except those given."""
    idx = lambda x, y: x + L * y
    M = np.zeros((L * L, L * L))
    for x in range(L):
        for y in range(L):
            for x2, y2 in ((x + 1, y), (x, y + 1)):
                if x2 < L and y2 < L:
                    v_ = links.get((idx(x, y), idx(x2, y2)), 1.0)
                    M[idx(x, y), idx(x2, y2)] = M[idx(x2, y2), idx(x, y)] = v_
    return M, idx


def filled(M):
    w = np.linalg.eigvalsh(M)
    return w[:len(w) // 2].sum()


cost_zero, cost_pi = {}, {}
for L in (6, 8, 10, 12):
    _, iL = open_lattice(L, {})
    c_ = L // 2 - 1
    string = {(iL(x, c_), iL(x, c_ + 1)): -1.0 for x in range(c_ + 1)}
    pi_links = {(iL(x, y), iL(x, y + 1)): (-1.0) ** x for x in range(L) for y in range(L - 1)}
    back = dict(pi_links)
    for key in string:
        back[key] = -back[key]
    cost_zero[L] = filled(open_lattice(L, string)[0]) - filled(open_lattice(L, {})[0])
    cost_pi[L] = filled(open_lattice(L, back)[0]) - filled(open_lattice(L, pi_links)[0])
check('corrected, the vison: on open lattices of side 6 to 12 one flipped plaquette lowers the energy of the uniform '
      'background and one plaquette set back to +1 raises the energy of the pi-flux background, so the vison is an excitation '
      'against the flux of the ground state',
      all(v_ < -0.5 for v_ in cost_zero.values()) and all(v_ > 0.15 for v_ in cost_pi.values()),
      ({L: round(v_, 3) for L, v_ in cost_zero.items()}, {L: round(v_, 3) for L, v_ in cost_pi.items()}))
# among the uniform fluxes 2 pi m / 24 per plaquette, m = 0 to 12, on the periodic 24x24 lattice in the Landau gauge, the
# energy of the half-filled spinons is lowest at m = 12, the flux pi
def flux_energy(m, L=24):
    idx = lambda x, y: (x % L) + L * (y % L)
    M = np.zeros((L * L, L * L), complex)
    for x in range(L):
        for y in range(L):
            M[idx(x, y), idx(x + 1, y)] += np.exp(2j * np.pi * m * y / L)
            M[idx(x, y), idx(x, y + 1)] += 1.0
    M = M + M.conj().T
    w = np.linalg.eigvalsh(M)
    return w[:L * L // 2].sum() / (L * L)


scan = [flux_energy(m) for m in range(13)]
check('corrected, among the uniform fluxes 2 pi m/24 the half-filled spinons have the lowest energy at the flux pi',
      int(np.argmin(scan)) == 12 and abs(scan[12] - tp) < 1e-9 and abs(scan[0] - t0) < 1e-9, [round(e_, 4) for e_ in scan[::3]])
print('all checks of page 10 hold')
