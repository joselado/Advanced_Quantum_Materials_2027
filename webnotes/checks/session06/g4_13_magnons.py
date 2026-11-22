"""Session 6, the numbers that page 13 (Sections 6.13 and 6.14) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The ring of 10 spins 1/2 and of 8 spins 1 of the caption of one_magnon are
asserted in figures/session06/one_magnon.py, and the bands of the three picture options in _g4_onemagnon.py. This
script holds the rest: the exactness of (6.6), the linear form (6.7) and the counting of the key box, the two-site
bond and the lattice of the steps fold (onsite |J|S per bond, z|J|S per site, hopping -|J|S, E_0 = -|J|S^2 N z/2),
the problem on a ring of eight spins 1/2, the numbers of the three quizzes with the condition S = 1 of the second,
the 4t^2/U of the recall box from the exact Hubbard dimer, and the widths of one_magnon. The spin matrices are built from
S^z and S^+ with the usual matrix elements, and the many-body Hamiltonians are exact diagonalizations, so the
bosonic results are checked against a route that does not use them. The sign is the one of
webnotes/conventions/session06.md, H = J sum_<ij> S_i . S_j with each bond once and J < 0 for the ferromagnet. It
finds the repository from its own path, needs numpy and scipy only, and writes no file."""
import numpy as np
import scipy.sparse as sp

COUNT = [0]


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name
    COUNT[0] += 1


def spin(S):
    """S^z and S^+ of a spin S in the basis m = S, S-1, ..., -S."""
    m = np.arange(S, -S - 1, -1)
    sz = np.diag(m)
    splus = np.zeros((len(m), len(m)))
    for i in range(1, len(m)):
        splus[i - 1, i] = np.sqrt(S * (S + 1) - m[i] * (m[i] + 1))
    return sz, splus


def holstein_primakoff(S):
    """S^z, S^+ and S^- of (6.6) on the boson states n = 0 ... 2S, and the boson a on the same states."""
    d = int(round(2 * S)) + 1
    a = np.diag(np.sqrt(np.arange(1, d)), 1)
    n = np.diag(np.round(np.diag(a.T @ a)))           # 0, 1, ..., 2S, rounded so that the root is never negative
    root = np.diag(np.sqrt(2 * S - np.diag(n)))
    out = (S * np.eye(d) - n, root @ a, a.T @ root, a)
    assert all(np.isfinite(x).all() for x in out)
    return out


def many_body(S, bonds, N, J):
    """The sparse H = J sum_bonds S_i . S_j on N spins S, and the operators S^-_i and S^z_i."""
    sz, splus = spin(S)
    d = sz.shape[0]

    def site(op, i):
        return sp.kron(sp.kron(sp.identity(d ** i), sp.csr_matrix(op)), sp.identity(d ** (N - i - 1)), format='csr')

    H = sp.csr_matrix((d ** N, d ** N))
    for i, j in bonds:
        H = H + J * (site(sz, i) @ site(sz, j) + 0.5 * (site(splus, i) @ site(splus.T, j) + site(splus.T, i) @ site(splus, j)))
    return H, [site(splus.T, i) for i in range(N)], [site(sz, i) for i in range(N)]


def one_magnon_block(S, bonds, N, J):
    """E_0 and the matrix of H on the N states S^-_j|FM>, normalized, with the check that H keeps them closed."""
    H, sminus, _ = many_body(S, bonds, N, J)
    d = int(round(2 * S)) + 1
    full = np.zeros(d ** N)
    full[0] = 1.0                                       # all spins at m = S
    E0 = full @ (H @ full)
    P = np.array([v / np.linalg.norm(v) for v in (s @ full for s in sminus)])
    HP = H @ P.T
    closed = np.abs(HP - P.T @ (P @ HP)).max()
    return E0, P @ HP, closed, H, full


def main():
    # (6.6) is exact: the spin algebra on the boson states n = 0 ... 2S, and the spin matrices themselves
    worst = 0.0
    for S in (0.5, 1.0, 1.5, 2.0):
        z, p, m, a = holstein_primakoff(S)
        sz, splus = spin(S)
        worst = np.max([worst, np.abs(z - sz).max(), np.abs(p - splus).max(), np.abs(m - splus.T).max(),
                        np.abs(z @ p - p @ z - p).max(), np.abs(p @ m - m @ p - 2 * z).max()])
    check('(6.6) gives the spin matrices and [S^z,S^+]=S^+, [S^+,S^-]=2S^z for S = 1/2 to 2', worst < 1e-12, worst)

    # (6.7) and the key box: S^+ = sqrt(2S) a on the states with at most one boson, S^- adds a boson and lowers S^z
    ok = True
    for S in (0.5, 1.0, 2.0):
        z, p, m, a = holstein_primakoff(S)
        ok &= np.isclose(p[0, 1], np.sqrt(2 * S)) and np.isclose((np.sqrt(2 * S) * a)[0, 1], p[0, 1])
        ok &= np.isclose(m[1, 0], np.sqrt(2 * S)) and np.isclose(z[1, 1], S - 1) and np.isclose(z[0, 0], S)
        ok &= np.allclose(p[:, 0], 0)                    # S^+ on the saturated site gives zero
    check('(6.7): S^+ = sqrt(2S) a and S^- = sqrt(2S) a^dagger on one boson, S^- lowers S^z by one, S^+|S> = 0', ok, 'ok')

    # the key box: sum_i S^z_i = NS - number of magnons, on a ring of 4 spins 1 with one and two lowering operators
    H, sminus, szs = many_body(1.0, [(i, (i + 1) % 4) for i in range(4)], 4, -1.0)
    full = np.zeros(3 ** 4); full[0] = 1
    Sz = sum(szs)
    one = sminus[1] @ full; two = sminus[3] @ (sminus[1] @ full)
    vals = [(v @ (Sz @ v)) / (v @ v) for v in (full, one, two)]
    check('sum_i S^z_i = NS - number of magnons, 4, 3, 2 for N = 4 and S = 1', np.allclose(vals, [4, 3, 2]), np.round(vals, 12))

    # the steps fold, two sites: the linear 2x2 matrix and the exact pair give the excitations 0 and 2|J|S,
    # E_0 = -|J|S^2, and J/2 [S_tot(S_tot+1) - 2S(S+1)] for S_tot = 2S and 2S - 1
    J = -1.3
    ok, rows = True, []
    for S in (0.5, 1.0, 1.5, 2.0):
        E0, h1, closed, _, _ = one_magnon_block(S, [(0, 1)], 2, J)
        exact = np.linalg.eigvalsh(h1) - E0
        lin = np.linalg.eigvalsh(abs(J) * S * np.array([[1, -1], [-1, 1]]))
        tot = [J / 2 * (St * (St + 1) - 2 * S * (S + 1)) for St in (2 * S, 2 * S - 1)]
        ok &= closed < 1e-12 and np.isclose(E0, -abs(J) * S ** 2) and np.allclose(exact, [0, 2 * abs(J) * S])
        ok &= np.allclose(lin, [0, 2 * abs(J) * S]) and np.allclose(tot, [-abs(J) * S ** 2, -abs(J) * S ** 2 + 2 * abs(J) * S])
        ok &= np.isclose(h1[0, 0] - E0, abs(J) * S) and np.isclose(h1[0, 1], -abs(J) * S)   # onsite |J|S, hopping -|J|S
        rows.append((S, np.round(exact, 10).tolist()))
    check('fold: one bond gives the onsite |J|S, the hopping -|J|S, the excitations 0 and 2|J|S, exact for S = 1/2 to 2',
          ok, rows)

    # the steps fold, a lattice: a 3x3 torus of spins 1/2 (z = 4) and a ring of 6 spins 1 (z = 2) have the onsite
    # energy z|J|S, the hopping -|J|S to each neighbor and nothing else, and E_0 = -|J|S^2 N z/2
    L = 3
    idx = lambda x, y: (x % L) * L + (y % L)
    torus = [(idx(x, y), idx(x + 1, y)) for x in range(L) for y in range(L)] + \
            [(idx(x, y), idx(x, y + 1)) for x in range(L) for y in range(L)]
    ring = [(i, (i + 1) % 6) for i in range(6)]
    ok, out = True, []
    for S, bonds, N, z in ((0.5, torus, 9, 4), (1.0, ring, 6, 2)):
        E0, h1, closed, _, _ = one_magnon_block(S, bonds, N, J)
        nb = np.zeros((N, N))
        for i, j in bonds:
            nb[i, j] = nb[j, i] = 1
        ok &= closed < 1e-12 and np.isclose(E0, -abs(J) * S ** 2 * N * z / 2)
        ok &= np.allclose(h1 - E0 * np.eye(N), z * abs(J) * S * np.eye(N) - abs(J) * S * nb)
        out.append((S, z, round(E0, 10)))
    check('fold: z|J|S on each site, -|J|S to each neighbor, E_0 = -|J|S^2 N z/2, on a 3x3 torus and a ring of 6', ok, out)

    # the problem: a ring of eight spins 1/2, E_0 = NJ/4, diagonal E_0 - J, hop J/2, the plane waves are eigenstates
    # with |J|(1 - cos k), largest 2|J| at k = pi; and the full diagonalization of the 256 states holds these values
    N, J = 8, -1.0
    E0, h1, closed, H, full = one_magnon_block(0.5, [(i, (i + 1) % N) for i in range(N)], N, J)
    j = np.arange(N)
    ks = 2 * np.pi * np.arange(N) / N
    res, ens = 0.0, []
    for k in ks:
        psi = np.exp(1j * k * j) / np.sqrt(N)
        hp = h1 @ psi
        e = np.real(np.vdot(psi, hp))
        res = max(res, np.abs(hp - e * psi).max())
        ens.append(e - E0)
    ens = np.array(ens)
    shift = (np.roll(np.eye(N), 1, axis=1) + np.roll(np.eye(N), -1, axis=1))
    ok = closed < 1e-12 and np.isclose(E0, N * J / 4) and np.allclose(h1, (E0 - J) * np.eye(N) + J / 2 * shift)
    ok &= res < 1e-12 and np.allclose(ens, abs(J) * (1 - np.cos(ks))) and np.isclose(ens.max(), 2 * abs(J))
    ok &= np.isclose(ks[np.argmax(ens)], np.pi) and np.allclose(ens, 2 * abs(J) * 0.5 * (1 - np.cos(ks)))
    w = np.linalg.eigvalsh(H.toarray())
    allE = np.round(w - w.min(), 9)
    ok &= np.isclose(w.min(), E0) and all(np.isclose(allE, x).any() for x in ens)     # E_0 is the ground state
    check('problem: ring of 8 spins 1/2, E_0 = NJ/4, plane waves with |J|(1 - cos k), top 2|J| at k = pi, in the spectrum',
          ok, (round(E0, 10), np.round(ens, 6).tolist()))

    # quiz 1: two spins 1/2, |up up> has S^z = 1 and S_1^- gives |down up> with S^z = 0
    H2, sm2, sz2 = many_body(0.5, [(0, 1)], 2, -1.0)
    up = np.array([1.0, 0, 0, 0])
    v = sm2[0] @ up
    check('quiz 1: |up up> has S^z = 1, S_1^-|up up> = |down up> with S^z = 0', np.isclose(up @ (sz2[0] + sz2[1]) @ up, 1)
          and np.allclose(v, [0, 0, 1, 0]) and np.isclose(v @ (sz2[0] + sz2[1]) @ v, 0), v)

    # quiz 2: [S^+, S^-] = 2S^z, which is 2S on the saturated state; S a would give S^2, 1 against 2 for S = 1;
    # a^dagger on the empty boson state is not zero while S^+ on the saturated spin is
    S = 1.0
    sz, splus = spin(S)
    comm = splus @ splus.T - splus.T @ splus
    z, p, m, a = holstein_primakoff(S)
    wrong = (S * a) @ (S * a.T) - (S * a.T) @ (S * a)
    ok = np.isclose(comm[0, 0], 2 * S) and np.isclose(comm[0, 0], 2) and np.isclose(wrong[0, 0], S ** 2) and np.isclose(wrong[0, 0], 1)
    ok &= np.linalg.norm(a.T[:, 0]) > 0.5 and np.allclose(splus[:, 0], 0)
    check('quiz 2: [S^+,S^-] = 2S = 2 on the saturated spin 1, S a gives S^2 = 1, a^dagger|0> is not zero', ok,
          (comm[0, 0], wrong[0, 0]))

    # quiz 2, the condition of the third option: S a is the same operator as sqrt(2S) a only when S^2 = 2S, which
    # among S = 1/2, 1, ..., 5 is S = 2 alone, so the question fixes S = 1
    Ss = np.arange(1, 11) / 2
    same = Ss[np.isclose(Ss ** 2, 2 * Ss)]
    check('quiz 2: S a = sqrt(2S) a only for S = 2 among S = 1/2 to 5, and not for the S = 1 of the question',
          same.tolist() == [2.0] and not np.isclose(1.0, np.sqrt(2.0)), same.tolist())

    # the recall box: the exact Hubbard dimer at half filling, with fermions by Jordan-Wigner, has its singlet below
    # its triplet by J = 4t^2/U for U >> t, so J > 0 is antiferromagnetic (also in checks/session06/g3_08)
    c = np.array([[0.0, 1.0], [0.0, 0.0]]); zz = np.diag([1.0, -1.0]); I2 = np.eye(2)
    ops = [np.kron(np.kron(np.kron(c, I2), I2), I2), np.kron(np.kron(np.kron(zz, c), I2), I2),
           np.kron(np.kron(np.kron(zz, zz), c), I2), np.kron(np.kron(np.kron(zz, zz), zz), c)]   # 1up, 1dn, 2up, 2dn
    num = [o.T @ o for o in ops]
    Ntot = np.round(np.diag(sum(num)))
    Sz = np.round(np.diag(0.5 * (num[0] - num[1] + num[2] - num[3])), 6)
    ratios = []
    for U in (40.0, 400.0):
        t = 1.0
        Hd = -t * sum(ops[i].T @ ops[i + 2] + ops[i + 2].T @ ops[i] for i in (0, 1)) + U * (num[0] @ num[1] + num[2] @ num[3])
        sel = (Ntot == 2) & (Sz == 0)
        w = np.linalg.eigvalsh(Hd[np.ix_(sel, sel)])
        trip = np.linalg.eigvalsh(Hd[np.ix_((Ntot == 2) & (Sz == 1), (Ntot == 2) & (Sz == 1))])[0]
        ratios.append((trip - w[0]) / (4 * t ** 2 / U))
    exact = [(np.sqrt(U ** 2 / 4 + 4) - U / 2) / (4 / U) for U in (40.0, 400.0)]       # E_T - E_S of the closed form
    check('recall box: the exact dimer has its singlet below the triplet by 4t^2/U, ratio 0.998 at U = 40t, 1.000 at 400t',
          ratios[0] > 0 and np.allclose(ratios, exact) and abs(ratios[0] - 1) < 3e-3 and abs(ratios[1] - 1) < 1e-4,
          np.round(ratios, 6).tolist())

    # quiz 3: the ring of the question, onsite 2|J|S and two hops -|J|S, S = 1, |J| = 1: 2 - 2 cos k, top 4 at pi;
    # the exact ring of 4 spins S = 1/2, 1 and 2 has its one-magnon top at 2, 4 and 8, the three pictures
    tops = []
    for S in (0.5, 1.0, 2.0):
        E0, h1, closed, _, _ = one_magnon_block(S, [(i, (i + 1) % 4) for i in range(4)], 4, -1.0)
        tops.append(np.linalg.eigvalsh(h1).max() - E0)
    ok = np.isclose(2 - 2 * np.cos(np.pi), 4) and np.allclose(tops, [2, 4, 8])
    check('quiz 3: 2 - 2 cos(pi) = 4, and the exact one-magnon tops 2, 4, 8 for S = 1/2, 1, 2', ok, np.round(tops, 10))

    # the caption of one_magnon: the band of S = 1 is twice as wide as that of S = 1/2, from the exact one-magnon
    # blocks of the two rings of the figure, 10 spins 1/2 and 8 spins 1, with J = -1
    widths = []
    for S, N in ((0.5, 10), (1.0, 8)):
        E0, h1, closed, _, _ = one_magnon_block(S, [(i, (i + 1) % N) for i in range(N)], N, -1.0)
        e = np.linalg.eigvalsh(h1) - E0
        assert closed < 1e-12
        widths.append(e.max() - e.min())
    check('one_magnon: the exact one-magnon band is 2|J| wide for 10 spins 1/2 and 4|J| for 8 spins 1, twice as wide',
          np.allclose(widths, [2, 4]) and np.isclose(widths[1] / widths[0], 2), np.round(widths, 10).tolist())

    print(f'{COUNT[0]} checks, all OK')


if __name__ == '__main__':
    main()
