"""Session 5, the numbers and the algebra that page 11 (Section 5.11) states and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or
in the figure script that draws it. The pair amplitudes of the figure pair_function and of the picture quiz, and the
Fourier transforms that the feedback quotes, 2 Delta0 cos k and a pairing proportional to sin k, are asserted in
figures/session05/_g3_pairfun.py. This script holds the rest, in the order of the page: the fold from the
anticommutation to (5.11) and (5.12), checked as operators on the Fock space of a ring, the two counterexamples of the
first quiz, and the problem on the bond pairing, whose phase is left open since it is the open point on (5.20). It
finds the repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session05/g3_11_pairing_symmetry.py"""
import os, sys
sys.dont_write_bytecode = True
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')        # the self-consistent loop of Anderson's theorem is small, one thread is enough
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
assert os.path.exists(os.path.join(REPO, 'webnotes', 'pages', 'session05'))

import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def fermions(M):
    """Annihilation operators of M fermionic modes, Jordan-Wigner, as dense matrices of size 2^M."""
    a = np.array([[0., 1.], [0., 0.]]); z = np.diag([1., -1.]); one = np.eye(2)
    ops = []
    for j in range(M):
        m = np.array([[1.]])
        for i in range(M):
            m = np.kron(m, z if i < j else (a if i == j else one))
        ops.append(m)
    return ops


rng = np.random.default_rng(7)

# ---------------------------------------------------------------------------------------------------------------
# the fold: a ring of N=4 sites with two spins, c_k^dag = N^-1/2 sum_n e^{-ikn} c_n^dag, the sum over all k of the zone
N = 4
c = fermions(2 * N)                                  # mode index 2 n + s, s = 0 for up and 1 for down
ks = 2 * np.pi * np.arange(N) / N
minus = [(-i) % N for i in range(N)]                 # the index of -k
cd_k = [[sum(np.exp(-1j * k * n) * c[2 * n + s].T for n in range(N)) / np.sqrt(N) for s in (0, 1)] for k in ks]


def pairing(D):
    """sum_k sum_{s1 s2} D[k, s1, s2] c_{k s1}^dag c_{-k s2}^dag."""
    return sum(D[i, s1, s2] * cd_k[i][s1] @ cd_k[minus[i]][s2] for i in range(N) for s1 in (0, 1) for s2 in (0, 1))


def T(D):
    """The operation of (5.11): D[k, s1, s2] -> -D[-k, s2, s1]."""
    return -np.transpose(D[minus], (0, 2, 1))


D = rng.normal(size=(N, 2, 2)) + 1j * rng.normal(size=(N, 2, 2))
O = pairing(D)
check('fold, a random pairing on a ring of 4 sites: only the part (D + T[D])/2 enters, that is (D_k,s1s2 - D_-k,s2s1)/2',
      np.abs(O - pairing((D + T(D)) / 2)).max() < 1e-13, np.abs(O - pairing((D + T(D)) / 2)).max())
check('fold, the part (D - T[D])/2, with D_k,s1s2 = +D_-k,s2s1, gives the operator zero',
      np.abs(pairing((D - T(D)) / 2)).max() < 1e-13, np.abs(pairing((D - T(D)) / 2)).max())
check('fold, the operator of a random pairing is not zero, so the check is not empty', np.abs(O).max() > 0.1, np.abs(O).max())
# the simplest case, one spin: the even part of D_k,upup gives zero, the odd part does not
Du = np.zeros((N, 2, 2), complex); Du[:, 0, 0] = rng.normal(size=N)
even = Du.copy(); even[:, 0, 0] = (Du[:, 0, 0] + Du[minus, 0, 0]) / 2
odd = Du.copy(); odd[:, 0, 0] = (Du[:, 0, 0] - Du[minus, 0, 0]) / 2
check('fold, one spin: the even part of D_k,upup gives zero and the odd part gives the whole operator',
      np.abs(pairing(even)).max() < 1e-13 and np.abs(pairing(odd) - pairing(Du)).max() < 1e-13, True)
# the split into A, antisymmetric in spin, and S, symmetric: for D = T[D], A is even in k and S is odd in k
Dp = (D + T(D)) / 2
A = (Dp - np.transpose(Dp, (0, 2, 1))) / 2
S = (Dp + np.transpose(Dp, (0, 2, 1))) / 2
check('fold, a pairing that satisfies (5.11): its spin-antisymmetric part is even in k and its spin-symmetric part is odd',
      np.allclose(A, A[minus], atol=1e-14) and np.allclose(S, -S[minus], atol=1e-14) and np.abs(S).max() > 0.1 and np.abs(A).max() > 0.1, True)

# ---------------------------------------------------------------------------------------------------------------
# the first quiz: sum_k sin k (c_k,up c_-k,dn - c_k,dn c_-k,up) = 0 and sum_k (c_k,up c_-k,dn + c_k,dn c_-k,up) = 0
c_k = [[m.T.conj() for m in row] for row in cd_k]
singlet_odd = sum(np.sin(k) * (c_k[i][0] @ c_k[minus[i]][1] - c_k[i][1] @ c_k[minus[i]][0]) for i, k in enumerate(ks))
triplet_even = sum(c_k[i][0] @ c_k[minus[i]][1] + c_k[i][1] @ c_k[minus[i]][0] for i in range(N))
check('quiz, the singlet with sin k_x is exactly zero as an operator', np.abs(singlet_odd).max() < 1e-13, np.abs(singlet_odd).max())
check('quiz, the triplet with a constant is exactly zero as an operator', np.abs(triplet_even).max() < 1e-13, np.abs(triplet_even).max())
partner = sum(np.sin(k) * (c_k[i][0] @ c_k[minus[i]][1] + c_k[i][1] @ c_k[minus[i]][0]) for i, k in enumerate(ks))
check('quiz, the triplet with sin k_x is not zero', np.abs(partner).max() > 0.1, np.abs(partner).max())

# ---------------------------------------------------------------------------------------------------------------
# the problem: c_n c_n = 0, and the bond pairing of one spin on a ring
check('problem, c c = 0 for one mode', np.abs(c[0] @ c[0]).max() == 0, 0)
Nr, Delta = 6, 0.3
cr = fermions(Nr)
H = Delta * sum(cr[n] @ cr[(n + 1) % Nr] + cr[(n + 1) % Nr].T @ cr[n].T for n in range(Nr))
kr = 2 * np.pi * np.arange(Nr) / Nr
mr = [(-i) % Nr for i in range(Nr)]
A_r = {1: Delta, -1: -Delta}                                         # A(a - b) of the creation part
for s in (1, -1):                                                    # s = +1 is the transform (2.7)
    cdk = [sum(np.exp(1j * s * k * n) * cr[n].T for n in range(Nr)) / np.sqrt(Nr) for k in kr]   # c_n^dag = N^-1/2 sum_k e^{-iskn} c_k^dag
    f = np.array([sum(A * np.exp(-1j * s * k * r) for r, A in A_r.items()) for k in kr])
    Hk = sum(0.5 * f[i] * cdk[i] @ cdk[mr[i]] for i in range(Nr))
    Hk = Hk + Hk.conj().T
    check(f'problem, sign {s:+d} of the transform: H_Delta = 1/2 sum_k [f(k) c_k^dag c_-k^dag + h.c.] as an operator on 6 sites',
          np.abs(H - Hk).max() < 1e-13, np.abs(H - Hk).max())
    check(f'problem, sign {s:+d}, Delta = 0.3 > 0 as the statement asks: f(k) is odd and |f(k)| = 2 Delta |sin k|',
          np.allclose(f[mr], -f, atol=1e-14) and np.allclose(np.abs(f), 2 * Delta * np.abs(np.sin(kr)), atol=1e-14), np.round(f, 4))
# the statement asks Delta > 0: for Delta < 0 the modulus is 2 |Delta| |sin k|, which is not 2 Delta |sin k|
fneg = np.array([sum(-A * np.exp(-1j * k * r) for r, A in A_r.items()) for k in kr])
check('problem, Delta = -0.3 gives |f| = 2 |Delta| |sin k| and not 2 Delta |sin k|, so the statement needs Delta > 0',
      np.allclose(np.abs(fneg), 2 * Delta * np.abs(np.sin(kr)), atol=1e-14) and np.abs(fneg).max() > 0.1, True)
# the condition next to the shape: A(+1) = +Delta in the problem, from c_{n+1}^dag c_n^dag, while the stems of the figure
# are the transform (1/N) sum_k Delta(k) e^{ikr} of Delta(k) = 2i Delta0 sin k of (5.20). Which stem is positive flips
# with the sign of (5.20) and with the sign of the transform, and the odd shape with stems +-1 at r = +-1 stays
Nf = 64
kf = 2 * np.pi * np.arange(Nf) / Nf
signs_at_plus1 = {}
for s20 in (1, -1):                                   # the sign printed in (5.20), and the other one
    for st in (1, -1):                                # the sign of the transform
        dr = {r: np.mean(s20 * 2j * np.sin(kf) * np.exp(1j * st * kf * r)) for r in (-1, 0, 1, 2)}
        odd = abs(dr[0]) < 1e-12 and abs(dr[2]) < 1e-12 and abs(dr[1] + dr[-1]) < 1e-12 and abs(abs(dr[1]) - 1) < 1e-12
        check(f'problem, condition: (5.20) with the sign {s20:+d} and the transform with the sign {st:+d} give odd stems +-1 at r = +-1',
              odd and abs(dr[1].imag) < 1e-12, round(dr[1].real, 12))
        signs_at_plus1[(s20, st)] = np.sign(dr[1].real)
check('problem, condition: the stem at r = +1 is -1 for (5.20) as printed and the transform of the figure, while A(+1) = +Delta, and it flips with either convention',
      signs_at_plus1[(1, 1)] == -1 and signs_at_plus1[(-1, 1)] == 1 and signs_at_plus1[(1, -1)] == 1 and signs_at_plus1[(-1, -1)] == -1
      and A_r[1] > 0, signs_at_plus1)
# the spectrum: a ring of 8 sites with the hopping -t, the chemical potential mu and the bond pairing, in the BdG form
# of the basis (c_1..c_N, c_1^dag..c_N^dag), with the antisymmetric pair matrix of A(r)
t, N8 = 1.0, 8
k8 = 2 * np.pi * np.arange(N8) / N8
for mu in (0.0, 0.7, -1.3, 2.0, -2.0):
    h = np.zeros((N8, N8)); P = np.zeros((N8, N8))
    for n in range(N8):
        h[n, (n + 1) % N8] = h[(n + 1) % N8, n] = -t
        h[n, n] = -mu
        P[(n + 1) % N8, n] = Delta; P[n, (n + 1) % N8] = -Delta      # (1/2) sum P_ab c_a^dag c_b^dag + h.c.
    bdg = np.block([[h, P], [P.conj().T, -h.T]])
    exact = np.sort(np.concatenate([s * np.sqrt((2 * t * np.cos(k8) + mu) ** 2 + 4 * Delta ** 2 * np.sin(k8) ** 2) for s in (1, -1)]))
    check(f'problem, ring of 8 sites, t=1, mu={mu}, Delta=0.3: the BdG levels are +-sqrt((2t cos k + mu)^2 + 4 Delta^2 sin^2 k)',
          np.allclose(np.sort(np.linalg.eigvalsh(bdg)), exact, atol=1e-12), round(np.abs(exact).min(), 6))
    closes = np.abs(exact).min() < 1e-12
    check(f'problem, mu={mu}: the levels reach zero only for |mu| = 2t', closes == (abs(abs(mu) - 2 * t) < 1e-12), closes)

# ---------------------------------------------------------------------------------------------------------------
# decided on 2026-11-22, the sentence after (5.10): "We use (5.10) only for its symmetry, since its overall sign is the
# opposite of the one of (5.4)". On the ring of 4 sites, the onsite pairing Delta sum_n c+_nup c+_ndn of (5.4) is the
# singlet of (5.10) with D_updn = x and D_dnup = -x. With the sum over the whole zone it needs x = -Delta, and with the sum over
# half of the zone, one k of each pair (k, -k) with k != -k, it needs x = -2 Delta on that pair. Either way the sign is the
# opposite one. The half zone is not written on the page, since there an even D_upup gives an operator that is not zero, while
# the fold and "Fermionic antisymmetry imposes (5.11)" use the whole zone, where it is zero.
Dv = 0.37
onsite = Dv * sum(c[2 * n].T @ c[2 * n + 1].T for n in range(N))


def pair510(Dk, ks_used):
    """-1/2 sum_{k in ks_used} sum_{s1 s2} D[k, s1, s2] c_{k s1}^dag c_{-k s2}^dag, the creation part of (5.10)."""
    return -0.5 * sum(Dk[i, s1, s2] * cd_k[i][s1] @ cd_k[minus[i]][s2] for i in ks_used for s1 in (0, 1) for s2 in (0, 1))


def singlet(x):
    Dk = np.zeros((N, 2, 2), complex); Dk[:, 0, 1] = x; Dk[:, 1, 0] = -x
    return Dk


whole = pair510(singlet(-Dv), range(N))
check('(5.10) with the sum over the whole zone gives the onsite pairing of (5.4) for D_updn = -Delta, the opposite sign',
      np.abs(whole - onsite).max() < 1e-12 and np.abs(pair510(singlet(Dv), range(N)) - onsite).max() > 0.1, -Dv)
# the pair k = pi/2, -pi/2 (index 1 and 3) taken once
pair_once = pair510(singlet(-2 * Dv), [1])
onsite_pair = Dv * (cd_k[1][0] @ cd_k[3][1] + cd_k[3][0] @ cd_k[1][1])
check('(5.10) with the sum over half of the zone gives it for D_updn = -2 Delta on a pair k, -k, again the opposite sign',
      np.abs(pair_once - onsite_pair).max() < 1e-12, -2 * Dv)
even_upup = np.zeros((N, 2, 2), complex); even_upup[:, 0, 0] = 1.0
check('the half zone is not written: an even D_upup gives zero over the whole zone and a nonzero operator over half of it',
      np.abs(pair510(even_upup, range(N))).max() < 1e-13 and np.abs(pair510(even_upup, [1])).max() > 0.1,
      round(np.abs(pair510(even_upup, [1])).max(), 3))

# ---------------------------------------------------------------------------------------------------------------
# decided on 2026-11-22, Anderson's theorem: "A spin-singlet superconductor whose gap has one sign on the whole Fermi surface is
# essentially insensitive to non-magnetic disorder" and "this disorder suppresses the triplet channel and the singlets that change
# sign, such as d-wave, and leaves the s-wave singlet intact".
# First route, exact: a uniform onsite Delta with any real potential V_i has the BdG levels +-sqrt(eps_n^2 + Delta^2), with eps_n
# the levels of the disordered normal state, so the smallest |E| is never below |Delta|, for every realization.
# Second route, self-consistent: a square lattice of 10 x 10 sites, t = 1, mu = -1, a box disorder of width W = 3t, six
# realizations. Onsite attraction for s-wave, Delta_i = |U| <c_idn c_iup>; first-neighbor attraction for the d-wave singlet and for
# the p_x + i p_y pairing of one spin. Each order is started in its pattern and iterated to its fixed point with Anderson mixing,
# and every run, clean and disordered, has to reach the change 1e-7 of the amplitudes. The coherent average of the order (the
# d-wave or p+ip component of the bond amplitudes) keeps more than 80% of its clean value for s-wave and less than half of it for
# d-wave and for p+ip (changed after the independent check of 2026-11-22, which found more than 25% with other couplings and
# 12 x 12 sites, so the earlier bound held only for these couplings; here the six realizations give at most 0.18 for d-wave
# and 0.23 for p+ip). One thread, about a minute.
Ls = 10
Ns = Ls * Ls
site = lambda x, y: (x % Ls) * Ls + (y % Ls)
bI = np.array([site(x, y) for x in range(Ls) for y in range(Ls)] * 2)
bJ = np.array([site(x + 1, y) for x in range(Ls) for y in range(Ls)] + [site(x, y + 1) for x in range(Ls) for y in range(Ls)])
bx = np.r_[np.ones(Ns, bool), np.zeros(Ns, bool)]


def normal(V):
    h = np.diag(1.0 + V)                                   # mu = -1
    h[bI, bJ] = -1.0; h[bJ, bI] = -1.0
    return h


def gap_map(kind, h, g, D):
    """One step of the T = 0 gap equation in the basis (c_up, c_dn^dag) for the singlets and (c, c^dag) for one spin, with
    F = <Psi Psi^dag> the block of the positive levels."""
    P = np.zeros((Ns, Ns), complex)
    if kind == 's':
        P[np.arange(Ns), np.arange(Ns)] = D
    else:
        P[bI, bJ] = D; P[bJ, bI] = D if kind == 'd' else -D
    e, v = np.linalg.eigh(np.block([[h, P], [P.conj().T, -h]]))
    p = v[:, e > 0]
    F = p[:Ns] @ p[Ns:].conj().T
    return g * (np.diag(F) if kind == 's' else 0.5 * (F[bI, bJ] + (F[bJ, bI] if kind == 'd' else -F[bJ, bI]))), e


def scf(kind, h, g, it=600, tol=1e-7, m=5, beta=0.4):
    """The fixed point D = gap_map(D), with Anderson mixing of the last m steps, cleared when the change grows."""
    D = np.full(Ns, 0.5 + 0j) if kind == 's' else (np.where(bx, 0.3, -0.3) if kind == 'd' else np.where(bx, 0.3, 0.3j)).astype(complex)
    X, R, best = [], [], np.inf
    for _ in range(it):
        new, e = gap_map(kind, h, g, D)
        r = new - D
        err = np.abs(r).max()
        if err < tol:
            break
        if err > 2 * best:
            X, R = [], []
        best = min(best, err)
        X, R = (X + [D.copy()])[-m:], (R + [r.copy()])[-m:]
        if len(X) > 1:
            dR = np.array([R[i + 1] - R[i] for i in range(len(R) - 1)]).T
            dX = np.array([X[i + 1] - X[i] for i in range(len(X) - 1)]).T
            gam = np.linalg.lstsq(np.r_[dR.real, dR.imag], np.r_[r.real, r.imag], rcond=None)[0]
            D = D + beta * r - (dX + beta * dR) @ gam
        else:
            D = D + beta * r
    comp = D.mean() if kind == 's' else (np.where(bx, D, -D).mean() if kind == 'd' else np.where(bx, D, -1j * D).mean())
    return abs(comp), np.abs(e).min(), err


couplings = dict(s=2.5, d=1.5, p=2.0)
rng_a = np.random.default_rng(11)
ok_exact = True
for _ in range(5):
    V = 3.0 * (rng_a.random(Ns) - 0.5)
    h = normal(V); Dx = 0.3 * np.exp(0.4j)
    e = np.linalg.eigvalsh(np.block([[h, Dx * np.eye(Ns)], [np.conj(Dx) * np.eye(Ns), -h]]))
    en = np.linalg.eigvalsh(h)
    ok_exact = ok_exact and np.allclose(np.sort(e), np.sort(np.r_[np.sqrt(en**2 + 0.09), -np.sqrt(en**2 + 0.09)]), atol=1e-12)
    ok_exact = ok_exact and np.abs(e).min() >= 0.3 - 1e-12
check('Anderson, exact: a uniform onsite Delta=0.3 with W=3t keeps the levels +-sqrt(eps_n^2 + Delta^2), smallest |E| >= |Delta|, '
      '5 realizations', ok_exact, 5)
clean = {k: scf(k, normal(np.zeros(Ns)), g) for k, g in couplings.items()}
assert all(c[2] < 1e-7 for c in clean.values()), clean
ratios = {k: [] for k in couplings}
for seed in range(6):
    V = 3.0 * (np.random.default_rng(seed).random(Ns) - 0.5)
    for k, g in couplings.items():
        r = scf(k, normal(V), g)
        assert r[2] < 1e-7, (k, seed, r)                     # every run converged
        ratios[k].append(r[0] / clean[k][0])
check('Anderson, self-consistent, W=3t, six realizations, all converged: the s-wave order keeps more than 80% of its clean value, '
      'd-wave and p+ip keep less than half of theirs',
      min(ratios['s']) > 0.8 and max(ratios['d']) < 0.5 and max(ratios['p']) < 0.5 and max(ratios['d']) < 0.18 and max(ratios['p']) < 0.23,
      {k: [round(x, 3) for x in v] for k, v in ratios.items()})
print('all checks of page 11 hold')
