"""Session 8, the numbers and the algebra that page 07 (Sections 8.7 and 8.8, the failure of the Holstein-Primakoff
expansion in a spin liquid and the Abrikosov fermions) quotes, checked with matrices.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The figure hp_boson_density.py asserts its own probabilities. This script builds
the fermion operators of one and of two sites as matrices with the Jordan-Wigner signs and checks the key box of (8.9),
the two rewritten quizzes and the new one, every displayed line of the fold "From the Fierz identity to (8.12)" on all
16 states of two sites, and the problem with its solution. It finds nothing on disk and writes no file."""
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


def spin(fu, fd):
    """(8.10), S = (1/2) f^dag sigma f, from the modes up and down of one site."""
    f = (fu, fd)
    return [0.5 * sum(P[a, b] * (dag(f[a]) @ f[b]) for a in range(2) for b in range(2)) for P in PAULI]


def close(a, b, tol=1e-12):
    return np.abs(np.asarray(a) - np.asarray(b)).max() < tol


# ------------------------------------------------------------------------------------------------------------------
# Section 8.7, the key box (8.9) and its quiz
S = 0.5
up, dn = np.array([1.0, 0.0]), np.array([0.0, 1.0])
singlet = (np.kron(up, dn) - np.kron(dn, up)) / np.sqrt(2)
sz0 = np.kron(np.diag([0.5, -0.5]), np.eye(2))
nb = S - singlet @ sz0 @ singlet                      # <a^dag a> = S - <S^z> from (8.8)
check('(8.9): one site of the singlet has <S^z> = 0, so <a^dag a> = S = 1/2', abs(nb - 0.5) < 1e-12, nb)
check('quiz: zero bosons would give <S^z> = S - 0 = 1/2, the ferromagnet', abs(S - 0 - 0.5) < 1e-12, S - 0)
check('quiz: <a^dag a> = 0.05 would give <S^z> = 0.45, nearly a full moment', abs(S - 0.05 - 0.45) < 1e-12, S - 0.05)

# ------------------------------------------------------------------------------------------------------------------
# Section 8.8, one site: the problem and the new quiz on S^z
fu, fd = modes(2)
nu, nd = dag(fu) @ fu, dag(fd) @ fd
n = nu + nd
Sx, Sy, Sz = spin(fu, fd)
Sp, Sm = dag(fu) @ fd, dag(fd) @ fu
occ = np.real(np.diag(n))
vac = np.zeros(4); vac[0] = 1.0                       # the empty site, the first basis state
one_up, one_dn = dag(fu) @ vac, dag(fd) @ vac
check('quiz: S^z of (8.10) is (n_up - n_dn)/2', close(Sz, 0.5 * (nu - nd)), 'max difference %.0e' % np.abs(Sz - 0.5 * (nu - nd)).max())
half_n = 0.5 * n
check('quiz: (n_up + n_dn)/2 gives +1/2 on one fermion down, where S^z gives -1/2',
      abs(one_dn @ half_n @ one_dn - 0.5) < 1e-12 and abs(one_dn @ Sz @ one_dn + 0.5) < 1e-12,
      (np.real(one_dn @ half_n @ one_dn), np.real(one_dn @ Sz @ one_dn)))
check('quiz: f^dag_up f_dn is S^+ = S^x + i S^y, it gives 0 on one fermion up, where S^z gives +1/2',
      close(Sp, Sx + 1j * Sy) and np.abs(Sp @ one_up).max() < 1e-12 and abs(one_up @ Sz @ one_up - 0.5) < 1e-12,
      np.real(one_up @ Sz @ one_up))
check('problem: S^+ = f^dag_up f_dn and S^- = f^dag_dn f_up are those of (8.10)', close(Sm, Sx - 1j * Sy) and close(Sp, dag(Sm)), 'ok')
check('problem: [S^+, S^-] = 2 S^z', close(Sp @ Sm - Sm @ Sp, 2 * Sz), 'ok')
check('solution: S^+ S^- = n_up (1 - n_dn) and S^- S^+ = n_dn (1 - n_up)',
      close(Sp @ Sm, nu @ (np.eye(4) - nd)) and close(Sm @ Sp, nd @ (np.eye(4) - nu)), 'ok')
check('solution: (S^z)^2 = (n_up + n_dn - 2 n_up n_dn)/4, and the other two terms give twice this',
      close(Sz @ Sz, 0.25 * (nu + nd - 2 * nu @ nd)) and close(0.5 * (Sp @ Sm + Sm @ Sp), 2 * Sz @ Sz), 'ok')
S2 = Sx @ Sx + Sy @ Sy + Sz @ Sz
s2 = np.real(np.diag(S2))
check('problem: S^2 = (3/4) n (2 - n), 3/4 on one fermion and 0 on none and on two',
      close(S2, 0.75 * n @ (2 * np.eye(4) - n)) and np.allclose(s2[occ == 1], 0.75) and np.allclose(s2[occ != 1], 0),
      dict(zip(occ.astype(int).tolist(), s2.round(3).tolist())))
pg = np.real(np.diag(n @ (2 * np.eye(4) - n)))
check('solution: n (2 - n) is the projector P_G of (8.7) on one site, 1 for one fermion and 0 otherwise',
      np.allclose(pg, (occ == 1).astype(float)), pg.tolist())
# each spin state filled with the probability 1/2, independently: the four states with weight 1/4 each
rho = np.diag([0.25, 0.25, 0.25, 0.25])
check('solution: a site with each spin state filled with the probability 1/2 has one fermion half of the time and '
      '<S^2> = 3/8', abs(np.trace(rho @ np.diag((occ == 1).astype(float))) - 0.5) < 1e-12 and abs(np.trace(rho @ S2).real - 3 / 8) < 1e-12,
      np.trace(rho @ S2).real)

# ------------------------------------------------------------------------------------------------------------------
# Section 8.8, two sites: the fold "From the Fierz identity to (8.12)" and the quiz on chi^dag chi
fiu, fid, fju, fjd = modes(4)                         # site i up and down, site j up and down
fi, fj = (fiu, fid), (fju, fjd)
I16 = np.eye(16)
ni = dag(fiu) @ fiu + dag(fid) @ fid
nj = dag(fju) @ fju + dag(fjd) @ fjd
Si, Sj = spin(fiu, fid), spin(fju, fjd)
SS = sum(a @ b for a, b in zip(Si, Sj))
chi = dag(fiu) @ fju + dag(fid) @ fjd                 # chi_ij = sum_s f^dag_is f_js, (8.12)
chi_ji = dag(fju) @ fiu + dag(fjd) @ fid
check('fold: chi_ij^dag = chi_ji', close(dag(chi), chi_ji), 'ok')
fz = max(abs(sum(P[a, b] * P[c, d] for P in PAULI) - (2 * (a == d) * (b == c) - (a == b) * (c == d)))
         for a, b, c, d in itertools.product(range(2), repeat=4))
check('fold: the Fierz identity on all 16 sets of indices', fz < 1e-14, fz)
four = sum(dag(fi[a]) @ fi[b] @ dag(fj[b]) @ fj[a] for a in range(2) for b in range(2))
check('fold: S_i.S_j = (1/2) sum f^dag_ia f_ib f^dag_jb f_ja - (1/4) n_i n_j, on all 16 states',
      close(SS, 0.5 * four - 0.25 * ni @ nj), np.abs(SS - (0.5 * four - 0.25 * ni @ nj)).max())
cdc = sum(dag(fj[a]) @ fi[a] @ dag(fi[b]) @ fj[b] for a in range(2) for b in range(2))
check('fold: chi^dag chi written as sum f^dag_ja f_ia f^dag_ib f_jb', close(cdc, dag(chi) @ chi), 'ok')
check('fold: sum f^dag_ia f_ib f^dag_jb f_ja = n_j - chi^dag chi, on all 16 states', close(four, nj - dag(chi) @ chi), 'ok')
full = 0.5 * nj - 0.25 * ni @ nj - 0.5 * dag(chi) @ chi
check('fold: S_i.S_j = n_j/2 - n_i n_j/4 - chi^dag chi/2, on all 16 states', close(SS, full), np.abs(SS - full).max())
one = np.nonzero((np.abs(np.real(np.diag(ni)) - 1) < 1e-9) & (np.abs(np.real(np.diag(nj)) - 1) < 1e-9))[0]
X = 0.25 * I16 - 0.5 * dag(chi) @ chi
on = np.abs((SS - X)[np.ix_(one, one)]).max()
off = np.abs(np.linalg.eigvalsh(SS - X)).max()
check('fold: (8.12) holds on the 4 states with n_i = n_j = 1 and misses by up to 0.75 on the 16 states',
      len(one) == 4 and on < 1e-14 and abs(off - 0.75) < 1e-12, (len(one), on, off))
# the simplest case of the fold: the singlet and the triplet up-up
vac16 = np.zeros(16); vac16[0] = 1.0
s = (dag(fiu) @ dag(fjd) - dag(fid) @ dag(fju)) @ vac16 / np.sqrt(2)
double_i = dag(fiu) @ dag(fid) @ vac16
t_uu = dag(fiu) @ dag(fju) @ vac16
check('fold: chi|s> = sqrt2 f^dag_iup f^dag_idn|0>, and chi^dag chi|s> = 2|s>',
      close(chi @ s, np.sqrt(2) * double_i) and close(dag(chi) @ chi @ s, 2 * s), 'ok')
check('fold: chi|up up> = 0, so chi^dag chi = 0 on the triplet', np.abs(chi @ t_uu).max() < 1e-14, 'ok')
check('fold: S_i.S_j is -3/4 on the singlet and +1/4 on the triplet, as 1/4 - chi^dag chi/2 gives',
      abs(s @ SS @ s + 0.75) < 1e-12 and abs(t_uu @ SS @ t_uu - 0.25) < 1e-12
      and abs(0.25 - 0.5 * 2 + 0.75) < 1e-12 and abs(0.25 - 0.5 * 0 - 0.25) < 1e-12,
      (np.real(s @ SS @ s), np.real(t_uu @ SS @ t_uu)))
we, ve = np.linalg.eigh(SS[np.ix_(one, one)])
cc = np.real(np.diag(dag(ve) @ (dag(chi) @ chi)[np.ix_(one, one)] @ ve))
check('quiz: on the constrained bond S_i.S_j has only -3/4 and +1/4, with chi^dag chi = 2 and 0',
      np.allclose(we, [-0.75, 0.25, 0.25, 0.25]) and np.allclose(cc, [2, 0, 0, 0]), (we.round(3).tolist(), cc.round(3).tolist()))
check('quiz: chi^dag chi = 1 would need S_i.S_j = 1/4 - 1/2 = -1/4, and the triplet gives 2(1/4 - 1/4) = 0',
      abs(0.25 - 0.5 * 1 + 0.25) < 1e-12 and abs(2 * (0.25 - 0.25)) < 1e-12, 'ok')
print('all checks of page 07 hold')
