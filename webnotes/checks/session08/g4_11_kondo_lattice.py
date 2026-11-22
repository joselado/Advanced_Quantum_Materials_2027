"""Session 8, the numbers and the signs that page 11 (Sections 8.11 and 8.12) states and that no figure script asserts.

One check script per page is the rule: every number of a fold, a quiz feedback or a solution is an assert here. The
page has no web figure of its own. The fermion operators of one site are matrices with the Jordan-Wigner signs, the
modes in the order c_up, c_dn, f_up, f_dn, and the spin is S = (1/2) f^dag sigma f of (8.10). The mean field is checked
on the half-filled chain with t = 1, by a minimization of the energy and by pyqula's KondoLatticeHamiltonian. The
script finds the repository from its own path, runs pyqula in a temporary folder and writes no file."""
import contextlib
import io
import itertools
import os
import sys
import tempfile

import numpy as np
from scipy.optimize import minimize_scalar

sys.dont_write_bytecode = True
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


# the Fierz identity of the fold, sum_a sigma^a_{beta alpha} sigma^a_{gamma delta} = 2 d_{beta delta} d_{alpha gamma} - d_{beta alpha} d_{gamma delta}
err = max(abs(sum(P[b, a] * P[g, d] for P in PAULI) - (2 * (b == d) * (a == g) - (b == a) * (g == d)))
          for b, a, g, d in itertools.product(range(2), repeat=4))
check('the Fierz identity on all 16 sets of indices', err < 1e-14, err)

# one site, the 16 states of c_up, c_dn, f_up, f_dn
cu, cd, fu, fd = modes(4)
c, f = (cu, cd), (fu, fd)
nc = dag(cu) @ cu + dag(cd) @ cd
nf = dag(fu) @ fu + dag(fd) @ fd
S = [0.5 * sum(P[a, b] * dag(f[a]) @ f[b] for a in range(2) for b in range(2)) for P in PAULI]
sc = [sum(P[b, a] * dag(c[b]) @ c[a] for a in range(2) for b in range(2)) for P in PAULI]     # c^dag sigma c
JK = 1.0
HK = JK * sum(x @ y for x, y in zip(sc, S))                                                     # the Kondo term of (8.17)
step1 = JK * sum(dag(c[b]) @ c[a] @ dag(f[a]) @ f[b] for a in range(2) for b in range(2)) - 0.5 * JK * nc @ nf
check('Fierz gives J_K c^dag_b c_a f^dag_a f_b - (J_K/2) n_c n_f', np.abs(HK - step1).max() < 1e-14, np.abs(HK - step1).max())
A = dag(fu) @ cu + dag(fd) @ cd                                                                # A = sum_a f^dag_a c_a
reorder = sum(dag(c[b]) @ c[a] @ dag(f[a]) @ f[b] for a in range(2) for b in range(2)) - (nc - dag(A) @ A)
check('c^dag_b c_a f^dag_a f_b = n_c - (c^dag f)(f^dag c)', np.abs(reorder).max() < 1e-14, np.abs(reorder).max())
one_f = np.nonzero(np.abs(np.real(np.diag(nf)) - 1) < 1e-9)[0]
diff = (HK - (-JK * dag(A) @ A + 0.5 * JK * nc))[np.ix_(one_f, one_f)]
check('with n_f = 1, H_K = -J_K (c^dag f)(f^dag c) + (J_K/2) n_c, which is (8.20) up to the potential J_K/2',
      len(one_f) == 8 and np.abs(diff).max() < 1e-14, (len(one_f), np.abs(diff).max()))
rest = HK - (-JK * dag(A) @ A + JK * nc - 0.5 * JK * nc @ nf)
check('on all 16 states the extra terms are J_K n_c - (J_K/2) n_c n_f', np.abs(rest).max() < 1e-14, np.abs(rest).max())

# the problem: one c electron and one f fermion, H_K = 2 J_K s.S with s = (1/2) c^dag sigma c
two = np.nonzero((np.abs(np.real(np.diag(nc)) - 1) < 1e-9) & (np.abs(np.real(np.diag(nf)) - 1) < 1e-9))[0]
lev = np.linalg.eigvalsh(HK[np.ix_(two, two)])
s_el = [0.5 * x for x in sc]
two_sS = 2 * JK * sum(x @ y for x, y in zip(s_el, S))
check('c^dag sigma c is twice the spin s of the electron, so H_K = 2 J_K s.S', np.abs(HK - two_sS).max() < 1e-14, np.abs(HK - two_sS).max())
check('the singlet at -3 J_K/2 once and the triplet at +J_K/2 three times, the gap 2 J_K',
      len(two) == 4 and np.allclose(lev, [-1.5, 0.5, 0.5, 0.5]) and abs(lev[1] - lev[0] - 2 * JK) < 1e-12, np.round(lev, 12))
s2 = sum(x @ x for x in s_el)[np.ix_(two, two)]
S2 = sum(x @ x for x in S)[np.ix_(two, two)]
check('s^2 = S^2 = 3/4 on these states', np.allclose(s2, 0.75 * np.eye(4)) and np.allclose(S2, 0.75 * np.eye(4)), 0.75)

# the new quiz: the quartic term keeps n_c and n_f, the hybridization does not
q = dag(A) @ A
hyb = dag(fu) @ cu + dag(fd) @ cd
hyb = hyb + dag(hyb)
check('(c^dag f)(f^dag c) commutes with n_c and n_f', np.abs(q @ nc - nc @ q).max() < 1e-14 and np.abs(q @ nf - nf @ q).max() < 1e-14, 0)
check('f^dag c + h.c. does not commute with n_c', np.abs(hyb @ nc - nc @ hyb).max() > 0.5, np.abs(hyb @ nc - nc @ hyb).max())
for g_ in (0.3, 0.6):
    lv = np.linalg.eigvalsh(np.array([[0.0, -g_], [-g_, 0.0]]))
    check('at the crossing eps = 0 the 2x2 matrix has the levels -+gamma_K, gamma_K = %g' % g_, np.allclose(lv, [-g_, g_]), lv)

# the second quiz: with gamma_K = 0 the f level stays at zero, for example where eps_k = 2
lv = np.linalg.eigvalsh(np.array([[2.0, 0.0], [0.0, 0.0]]))
check('gamma_K = 0, eps_k = 2: the levels are 0 (f) and 2 (c)', np.allclose(lv, [0, 2]), lv)
# the first quiz, second option: the Kondo coupling does not create electrons. Two sites with the hopping t = 1 and
# J_K = 0.8, the modes c0_up, c0_dn, c1_up, c1_dn, f0_up, f0_dn, f1_up, f1_dn, so 256 states.
ops = modes(8)
c2s, f2s = [(ops[0], ops[1]), (ops[2], ops[3])], [(ops[4], ops[5]), (ops[6], ops[7])]
H2 = sum(-1.0 * (dag(c2s[0][s]) @ c2s[1][s] + dag(c2s[1][s]) @ c2s[0][s]) for s in range(2))
for j in range(2):
    Sj = [0.5 * sum(P[a, b] * dag(f2s[j][a]) @ f2s[j][b] for a in range(2) for b in range(2)) for P in PAULI]
    scj = [sum(P[b, a] * dag(c2s[j][b]) @ c2s[j][a] for a in range(2) for b in range(2)) for P in PAULI]
    H2 = H2 + 0.8 * sum(x @ y for x, y in zip(scj, Sj))
Nc2 = sum(dag(x) @ x for j in range(2) for x in c2s[j])
check('two sites with hopping and Kondo coupling: [H, N_c] = 0 on all 256 states', np.abs(H2 @ Nc2 - Nc2 @ H2).max() < 1e-12,
      np.abs(H2 @ Nc2 - Nc2 @ H2).max())
dNc = np.real(np.diag(Nc2))
dnf = [np.real(np.diag(sum(dag(x) @ x for x in f2s[j]))) for j in range(2)]
sec = np.nonzero((np.abs(dNc - 1) < 1e-9) & (np.abs(dnf[0] - 1) < 1e-9) & (np.abs(dnf[1] - 1) < 1e-9))[0]
w2, v2 = np.linalg.eigh(H2[np.ix_(sec, sec)])
gs = v2[:, np.abs(w2 - w2[0]) < 1e-9]
nc_gs = np.real(np.trace(gs.conj().T @ Nc2[np.ix_(sec, sec)] @ gs)) / gs.shape[1]
check('one conduction electron for two impurities: the ground level keeps N_c = 1, 0.5 per site, enough for half of them',
      len(sec) == 16 and abs(nc_gs - 1) < 1e-12 and abs(nc_gs / 2 - 0.5) < 1e-12, round(nc_gs / 2, 12))

# the mean field of (8.20) on the half-filled chain, t = 1: the energy per site of the two spins is
# 2 <E_-(k)> + gamma^2/J_K, and its minimum must sit at gamma = J_K <sum_s c^dag_s f_s>, with the sign of (8.21)
nk = 4000
kk = 2 * np.pi * (np.arange(nk) + 0.5) / nk
eps = -2 * np.cos(kk)
JK = 0.8


def energy(g_):
    return 2 * np.mean((eps - np.sqrt(eps ** 2 + 4 * g_ ** 2)) / 2) + g_ ** 2 / JK


gmin = minimize_scalar(energy, bounds=(1e-4, 2.0), method='bounded', options=dict(xatol=1e-10)).x
cf, nf_site = 0.0, 0.0
for e_ in eps:                                                     # the filled lower band of [[eps, -gamma], [-gamma, 0]]
    w, v = np.linalg.eigh(np.array([[e_, -gmin], [-gmin, 0.0]]))
    cf += 2 * np.real(np.conj(v[0, 0]) * v[1, 0]) / nk              # sum over the two spins of <c^dag f>
    nf_site += 2 * abs(v[1, 0]) ** 2 / nk                            # f fermions per site, the two spins
check('J_K = 0.8: the minimum of the energy is gamma_K = 0.527', abs(gmin - 0.527) < 5e-4, round(gmin, 5))
check('J_K <sum_s c^dag_s f_s> is the same gamma_K, with the plus sign', cf > 0 and abs(JK * cf - gmin) < 1e-6, round(JK * cf, 5))
check('the f level at zero holds one f fermion per site here', abs(nf_site - 1) < 1e-9, round(nf_site, 9))

# the first quiz, first option: at half filling or below there is at most one conduction electron per impurity
nc_half = 2 * np.mean(eps < 0)                                     # the chain band -2 cos k filled up to zero, two spins
check('the half-filled chain has n_c = 1 per site, one per impurity, and a lower Fermi level gives fewer',
      abs(nc_half - 1) < 1e-12 and 2 * np.mean(eps < -0.5) < 1, (nc_half, 2 * np.mean(eps < -0.5)))
# the first quiz, third option: at gamma_K = 0.6 the direct gap 2 gamma_K = 1.2 at the crossing, and the Fermi level zero
# in the smaller gap between the two bands, 2(sqrt(1 + gamma^2) - 1) = 0.3324 on the chain
g6 = 0.6
lo6, up6 = (eps - np.sqrt(eps ** 2 + 4 * g6 ** 2)) / 2, (eps + np.sqrt(eps ** 2 + 4 * g6 ** 2)) / 2
lv0 = np.linalg.eigvalsh(np.array([[0.0, -g6], [-g6, 0.0]]))
ind6 = up6.min() - lo6.max()
check('the direct gap at the crossing is 2 gamma_K = 1.2, and the gap between the bands, 0.3324, is smaller and holds zero',
      abs(lv0[1] - lv0[0] - 1.2) < 1e-12 and abs(ind6 - 2 * (np.sqrt(1 + g6 ** 2) - 1)) < 1e-5 and ind6 < 1.2
      and lo6.max() < 0 < up6.min(), (round(lv0[1] - lv0[0], 6), round(ind6, 4)))
rng = np.random.default_rng(11)
worst = np.inf
for _ in range(50):                                                # 50 random bands of 300 momenta and random gamma_K
    e_, g_ = rng.uniform(-4, 4, 300), rng.uniform(0.05, 2)
    lo_, up_ = (e_ - np.sqrt(e_ ** 2 + 4 * g_ ** 2)) / 2, (e_ + np.sqrt(e_ ** 2 + 4 * g_ ** 2)) / 2
    worst = min(worst, np.min(up_ - lo_) - (up_.min() - lo_.max()))
check('for any band the gap between the two bands is not larger than the direct gap', worst >= -1e-12, round(worst, 6))

# the condition after the key box of 8.12: gamma_K is the only parameter when the f level stays at zero. On the half-
# filled chain, symmetric around zero, the f level at zero holds one f fermion per site (above). On the band of the
# notebook, 2[cos k1 + cos k2 + cos(k1+k2)] - 2 on a mesh of 90 per side, the f level at zero holds 0.46 for gamma = 0.25,
# and one f fermion per site with the lower band full needs the f level lambda far from zero.
from scipy.optimize import brentq  # noqa: E402
mk = 2 * np.pi * np.arange(90) / 90
m1, m2 = np.meshgrid(mk, mk, indexing='ij')
etri = (2 * (np.cos(m1) + np.cos(m2) + np.cos(m1 + m2)) - 2).ravel()


def nf_lower(lam, g_=0.25):
    """f fermions per site, the two spins, in the full lower band of [[eps, -g], [-g, lam]]."""
    el = (etri + lam - np.sqrt((etri - lam) ** 2 + 4 * g_ ** 2)) / 2
    return 2 * np.mean((etri - el) ** 2 / ((etri - el) ** 2 + g_ ** 2))


lam_star = brentq(lambda x: nf_lower(x) - 1, -3, 3)
check('notebook band, gamma = 0.25: the f level at zero holds 0.46, and one f fermion per site needs the f level %.2f'
      % lam_star, abs(nf_lower(0.0) - 0.4615) < 5e-4 and abs(lam_star) > 1, (round(nf_lower(0.0), 4), round(lam_star, 4)))

# pyqula takes J = 2 J_K, and gives the same gamma_K
os.chdir(tempfile.mkdtemp())
from pyqula import geometry  # noqa: E402
from pyqula.kondolattice import KondoLatticeHamiltonian  # noqa: E402
hc = geometry.chain().get_hamiltonian(has_spin=True)
with contextlib.redirect_stdout(io.StringIO()):
    hmf = KondoLatticeHamiltonian(hc).get_mean_field_hamiltonian(J=2 * JK, filling=0.5, nk=400, mf=([0.3], [0.]), T=2e-3)
gq = abs(hmf.hybridization[0])
check('KondoLatticeHamiltonian with J = 2 J_K = 1.6 gives the same gamma_K', abs(gq - gmin) < 1e-3, round(gq, 5))
check('its f level stays at zero with one f fermion per site', abs(hmf.constraint_lambda[0]) < 1e-6
      and abs(np.real(hmf.local_occupation[0]) - 1) < 1e-6, (hmf.constraint_lambda[0], np.real(hmf.local_occupation[0])))

# corrected and decided on 2026-11-22, old text of the page
# (8.19) is the spin (8.10) written as the matrix (S.sigma)_{beta alpha}, and its trace is zero on all four states of the
# f fermions of a site, also on the empty and on the doubly occupied one, so it is a form of the spin and not of the
# constraint (8.11)
Sab = [[dag(f[a]) @ f[b] - 0.5 * nf * (a == b) for b in range(2)] for a in range(2)]
form = max(np.abs(Sab[a][b] - sum(P[b, a] * S[i] for i, P in enumerate(PAULI))).max() for a in range(2) for b in range(2))
trace = np.abs(Sab[0][0] + Sab[1][1]).max()
check('corrected, (8.19) is the spin as the matrix (S.sigma)_ba, with the trace zero on all 16 states, whatever n_f is',
      form < 1e-14 and trace < 1e-14 and set(np.round(np.real(np.diag(nf)), 9)) == {0.0, 1.0, 2.0}, (form, trace))
# the range of "the only mean-field parameter": on the chain with t = 1 and gamma_K held at 0.5, the f level at zero gives
# one f fermion per site at half filling of the conduction band, and not at the filling 0.15 (n_c = 0.3 per site), where
# one f fermion per site needs the f level near -1.93. Two routes: the eigenvectors of the 2x2 matrix per k, and the
# closed form of the f weight of E_-+.
kk = 2 * np.pi * (np.arange(20000) + 0.5) / 20000
eps_c = -2 * np.cos(kk)


def nf_closed(lam, nc_site, g_=0.5):
    d = (eps_c - lam) / 2
    r = np.sqrt(d ** 2 + g_ ** 2)
    E_ = np.r_[(eps_c + lam) / 2 - r, (eps_c + lam) / 2 + r]
    W_ = np.r_[0.5 * (1 + d / r), 0.5 * (1 - d / r)]
    occ_ = np.argsort(E_)[:int(round((nc_site + 1) / 2 * len(kk)))]
    return 2 * W_[occ_].sum() / len(kk)


def nf_eig(lam, nc_site, g_=0.5):
    E_, W_ = [], []
    for e_ in eps_c[::10]:
        w_, v_ = np.linalg.eigh(np.array([[e_, -g_], [-g_, lam]]))
        E_ += list(w_)
        W_ += list(np.abs(v_[1]) ** 2)
    E_, W_ = np.array(E_), np.array(W_)
    occ_ = np.argsort(E_)[:int(round((nc_site + 1) / 2 * len(kk[::10])))]
    return 2 * W_[occ_].sum() / len(kk[::10])


lam15 = brentq(lambda l_: nf_closed(l_, 0.3) - 1, -4, 2, xtol=1e-8)
check('decided, another filling: with the f level at zero n_f = 1 at half filling and 0.36 at the filling 0.15, and one f '
      'fermion per site there needs the f level at -1.93, by two routes',
      abs(nf_closed(0, 1.0) - 1) < 1e-9 and abs(nf_eig(0, 1.0) - 1) < 1e-9 and abs(nf_closed(0, 0.3) - 0.356) < 1e-3
      and abs(nf_eig(0, 0.3) - nf_closed(0, 0.3)) < 1e-3 and abs(lam15 + 1.93) < 5e-3 and abs(nf_eig(lam15, 0.3) - 1) < 1e-3,
      (round(nf_closed(0, 0.3), 4), round(lam15, 4)))
# the second quiz: with gamma_K = 0 the flat f level holds one fermion per site only when it sits at the Fermi level, so
# zero is the chemical potential of the constraint only where the Fermi level of the conduction electrons is zero, which
# is the half-filled band symmetric around zero, and not the filling 0.15
mu_half, mu_15 = np.quantile(eps_c, 0.5), np.quantile(eps_c, 0.15)
check('decided, quiz 2: the Fermi level of the chain band is 0 at half filling and %.3f at the filling 0.15' % mu_15,
      abs(mu_half) < 1e-3 and mu_15 < -1, (round(mu_half, 6), round(mu_15, 4)))
print('all checks of page 11 hold')
