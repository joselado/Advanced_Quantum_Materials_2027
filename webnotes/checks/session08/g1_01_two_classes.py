"""Session 8, the statements of page 01 (Sections 8.1 and 8.2).

It checks the key box (one flipped spin of the ferromagnet changes S^z_tot by 1 and is no state of definite total
spin, the magnon, the flip spread with a nonzero momentum, has a total spin N/2 - 1, one less than the ground state,
an unpaired site of a singlet covering changes the total spin by 1/2, and an even number of sites has an integer
total spin), the feedback of the first quiz (four sites
have S = 0, 1, 2 and S^z_tot from -2 to 2), the second quiz (one f^dag raises S^z by 1/2, two spins 1/2 give S = 1),
the picture quiz (the three chains of six sites have S = 0, S = 1 and S^z = 2 with S >= 2, and the flip spread with a
nonzero momentum has S = 2), the problem (three sites have S = 1/2 twice and S = 3/2 once, 2*2+4 = 8), the reading
of the lab box marked as ours (from a singlet one spin operator reaches only S = 1), and that the numbers of the lab
box, 99(8)% and 71%, are in the tracked source.

Every total spin comes from the eigenvalues of S_tot^2 on the spin states, and the multiplicities also from the
binomial formula of the conventions sheet. It needs numpy only and writes no file."""
import os
from functools import reduce
from math import comb
import numpy as np

WEBNOTES = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UP, DN = np.array([1., 0.]), np.array([0., 1.])
SX, SY, SZ = np.array([[0, 1], [1, 0]]) / 2, np.array([[0, -1j], [1j, 0]]) / 2, np.diag([.5, -.5])


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def op(o, i, n):
    return reduce(np.kron, [o if j == i else np.eye(2) for j in range(n)])


def stot(n):
    tot = [sum(op(o, i, n) for i in range(n)) for o in (SX, SY, SZ)]
    return tot, sum(t @ t for t in tot)


def spins_of(s2vals):
    """The total spins S from the eigenvalues S(S+1), with the number of states of each."""
    S = np.round((-1 + np.sqrt(1 + 4 * np.round(s2vals, 9))) / 2, 6)
    vals, counts = np.unique(S, return_counts=True)
    return dict(zip(vals.tolist(), counts.tolist()))


def multiplicity(N, S):
    """How many times the total spin S appears for N spins 1/2, from the binomial formula of the sheet."""
    m = int(round(N / 2 - S))
    return comb(N, m) - (comb(N, m - 1) if m >= 1 else 0)


SINGLET = (np.kron(UP, DN) - np.kron(DN, UP)) / np.sqrt(2)

# the key box, first route: the ferromagnet of N sites has S = N/2, and a magnon of nonzero momentum S = N/2 - 1
for N in (4, 6):
    tot, S2 = stot(N)
    full = reduce(np.kron, [UP] * N)
    k = 2 * np.pi / N
    magnon = sum(np.exp(1j * k * j) * op(SX - 1j * SY, j, N) @ full for j in range(N))   # sum_j e^{ikj} S_j^- |all up>
    magnon = magnon / np.linalg.norm(magnon)
    s_full = np.vdot(full, S2 @ full).real
    s_mag = np.vdot(magnon, S2 @ magnon).real
    check(f'key box, ferromagnet of {N} sites, S = {N // 2} and the magnon of momentum 2pi/{N} has S = {N // 2 - 1}, Delta S = 1',
          np.isclose(s_full, N / 2 * (N / 2 + 1)) and np.isclose(s_mag, (N / 2 - 1) * N / 2)
          and np.allclose(S2 @ magnon, s_mag * magnon), (s_full, round(s_mag, 12)))
# the key box as written: in a ferromagnet of N sites one flipped spin changes S^z_tot by exactly 1 but has no definite
# total spin (the weights are 1/N on S = N/2 and (N-1)/N on S = N/2 - 1), and every magnon sum_j e^{ikj} S_j^- |all up>
# with k = 2 pi n/N, n = 1 to N-1, has S = N/2 - 1, one less than the S = N/2 of the ground state
for N in (4, 6, 8):
    tot, S2 = stot(N)
    full = reduce(np.kron, [UP] * N)
    ok_flip, ok_mag = True, True
    for j in range(N):
        f = op(SX - 1j * SY, j, N) @ full
        f = f / np.linalg.norm(f)
        dsz = np.vdot(full, tot[2] @ full).real - np.vdot(f, tot[2] @ f).real
        ok_flip = ok_flip and np.isclose(dsz, 1) and np.allclose(tot[2] @ f, (N / 2 - 1) * f)
        ok_flip = ok_flip and not np.allclose(S2 @ f, np.vdot(f, S2 @ f) * f)
        top = sum(op(SX - 1j * SY, i, N) for i in range(N)) @ full
        top = top / np.linalg.norm(top)                                    # the S = N/2 part of the flipped state
        w_top = abs(np.vdot(top, f)) ** 2
        ok_flip = ok_flip and np.isclose(w_top, 1 / N) and np.isclose(np.vdot(f, S2 @ f).real,
                                                                       w_top * N / 2 * (N / 2 + 1) + (1 - w_top) * (N / 2 - 1) * N / 2)
    for n in range(1, N):
        m = sum(np.exp(2j * np.pi * n * i / N) * op(SX - 1j * SY, i, N) for i in range(N)) @ full
        m = m / np.linalg.norm(m)
        ok_mag = ok_mag and np.allclose(S2 @ m, (N / 2 - 1) * (N / 2) * m) and np.allclose(tot[2] @ m, (N / 2 - 1) * m)
    check(f'key box, {N} sites: one flipped spin changes S^z_tot by 1 and has weight 1/{N} on S = {N // 2}, no definite S',
          ok_flip, round(1 / N, 6))
    check(f'key box, {N} sites: every magnon with k = 2 pi n/{N}, n = 1 to {N - 1}, has S = {N // 2 - 1}, one less than {N // 2}',
          ok_mag, (N // 2, N // 2 - 1))
# the key box, second route: singlets with one site left without a partner have S = 1/2, Delta S = 1/2
tot, S2 = stot(5)
psi = reduce(np.kron, [SINGLET, SINGLET, UP])
check('key box, two singlets and one unpaired site have S(S+1) = 3/4, so S = 1/2', np.allclose(S2 @ psi, 0.75 * psi), 0.75)
tot, S2 = stot(4)
psi = reduce(np.kron, [SINGLET, SINGLET])
check('key box, a covering of four sites by singlets has S = 0', np.allclose(S2 @ psi, 0 * psi), 0)

# even N has an integer total spin, odd N a half-integer one, and the multiplicities of the binomial formula
for N in range(1, 8):
    tot, S2 = stot(N)
    sp = spins_of(np.linalg.eigvalsh(S2))
    ok = all(float(S).is_integer() == (N % 2 == 0) for S in sp)
    ok = ok and all(sp[S] == (2 * S + 1) * multiplicity(N, S) for S in sp)
    check(f'N = {N}: total spins {sorted(sp)}, integer for even N, multiplicities of the binomial formula', ok,
          {S: sp[S] // int(2 * S + 1) for S in sp})

# quiz 1: four sites have S = 0, 1, 2 and never 1/2, and S^z_tot runs over the integers -2 to 2
tot, S2 = stot(4)
sp = spins_of(np.linalg.eigvalsh(S2))
szv = sorted(set(np.round(np.diag(tot[2].real), 9).tolist()))
check('quiz 1, four sites have S = 0, 1 or 2', sorted(sp) == [0.0, 1.0, 2.0], sorted(sp))
check('quiz 1, with four sites S^z_tot is an integer from -2 to 2', szv == [-2.0, -1.0, 0.0, 1.0, 2.0], szv)

# quiz 2: f^dag_up raises S^z = (n_up - n_dn)/2 by 1/2 on one site (Jordan-Wigner, two modes), and two spins 1/2 form S = 1
a = np.array([[0., 1.], [0., 0.]]); Z = np.diag([1., -1.])
fu, fd = np.kron(a, np.eye(2)), np.kron(Z, a)
Sz_f = 0.5 * (fu.T @ fu - fd.T @ fd)
comm = Sz_f @ fu.T - fu.T @ Sz_f
check('quiz 2, [S^z, f^dag_up] = +1/2 f^dag_up, so f^dag_up raises S^z by 1/2', np.allclose(comm, 0.5 * fu.T), 0.5)
tot, S2 = stot(2)
check('quiz 2, two spins 1/2 have S = 0 once and S = 1 once', spins_of(np.linalg.eigvalsh(S2)) == {0.0: 1, 1.0: 3},
      spins_of(np.linalg.eigvalsh(S2)))

# the picture quiz, six sites
tot, S2 = stot(6)
paired = reduce(np.kron, [SINGLET] * 3)
two = reduce(np.kron, [UP, SINGLET, SINGLET, UP])
flip = reduce(np.kron, [UP, UP, DN, UP, UP, UP])
check('picture quiz, three singlets have S_tot = 0', np.allclose(S2 @ paired, 0 * paired), 0)
check('picture quiz, two singlets and two free spins up have S_tot = 1 and S^z = 1',
      np.allclose(S2 @ two, 2 * two) and np.isclose(np.vdot(two, tot[2] @ two).real, 1), 1)
szf = np.vdot(flip, tot[2] @ flip).real
s2f = np.vdot(flip, S2 @ flip).real
check('picture quiz, five up and one down give S^z_tot = 2, and <S^2> = 7 lies between S = 2 (6) and S = 3 (12)',
      np.isclose(szf, 2) and np.isclose(s2f, 7), (szf, s2f))
# in the sector S^z = 2 of six spins, S_tot^2 has 12 once (the uniform flip) and 6 five times, so S >= 2
idx = np.where(np.isclose(np.diag(tot[2].real), 2))[0]
ev = np.round(np.linalg.eigvalsh(S2[np.ix_(idx, idx)].real), 9)
check('picture quiz, the sector S^z = 2 of six sites has S = 3 once and S = 2 five times, so never S = 1',
      sorted(ev.tolist()) == [6.0] * 5 + [12.0], sorted(ev.tolist()))
# the flip spread with a nonzero momentum on a ring of six, and the excited one-magnon states of the open chain
ok = True
for n in range(1, 6):
    k = 2 * np.pi * n / 6
    m = sum(np.exp(1j * k * j) * op(SX - 1j * SY, j, 6) for j in range(6)) @ reduce(np.kron, [UP] * 6)
    m /= np.linalg.norm(m)
    ok = ok and np.allclose(S2 @ m, 6 * m)
H = -sum(op(o, j, 6) @ op(o, j + 1, 6) for j in range(5) for o in (SX, SY, SZ))      # open ferromagnetic chain
e, v = np.linalg.eigh(H[np.ix_(idx, idx)])
for c in range(1, 6):
    w = np.zeros(64, complex); w[idx] = v[:, c]
    ok = ok and np.allclose(S2 @ w, 6 * w)
check('picture quiz, a flip spread with a nonzero momentum (ring) and the excited one-magnon states of the open chain have S = 2',
      ok, 'S(S+1) = 6')

# the problem: three sites, S = 1/2 twice and S = 3/2 once, 2*2 + 4 = 8
tot, S2 = stot(3)
sp = spins_of(np.linalg.eigvalsh(S2))
check('problem, three sites have S = 1/2 twice and S = 3/2 once', sp == {0.5: 4, 1.5: 4} and multiplicity(3, 0.5) == 2
      and multiplicity(3, 1.5) == 1, {S: sp[S] // int(2 * S + 1) for S in sp})
check('problem, 2*2 + 4 = 8 = 2^3', 2 * 2 + 4 == 8 == 2 ** 3, 8)

# the reading of the lab box, ours: from the singlet ground state of a ring of six, one spin operator S^a_q reaches only S = 1
tot, S2 = stot(6)
Hh = sum(op(o, j, 6) @ op(o, (j + 1) % 6, 6) for j in range(6) for o in (SX, SY, SZ))
e, v = np.linalg.eigh(Hh)
gs = v[:, 0]
ok = abs(e[1] - e[0]) > 1e-6 and np.allclose(S2 @ gs, 0 * gs)
for o in (SX, SY, SZ):
    for q in (np.pi / 3, np.pi):
        w = sum(np.exp(1j * q * j) * op(o, j, 6) for j in range(6)) @ gs
        w /= np.linalg.norm(w)
        ok = ok and np.allclose(S2 @ w, 2 * w)
check('lab box, ours: the ground state of the ring of six is a singlet, and S^a_q on it gives S = 1 only', ok, 'S(S+1) = 2')

# the numbers of the lab box are in the tracked source, in the arXiv abstract that it keeps whole
src = open(os.path.join(WEBNOTES, 'sources', 'session08', 'mourigal2013_nphys2652.txt')).read()
check('lab box, the tracked source holds 99(8)% and 71% and the pairs of spinons',
      'to within 99(8)%' in src and 'exhaust only 71% of the spectral weight' in src
      and 'created and detected in pairs by neutron scattering' in src
      and 'on a compound realizing the model' in src and 'macroscopic singlet entangling all spins' in src, 'ok')

# corrected on 2026-11-22, old text of the page
# Section 8.2, the paragraph and the caption (a) of Figure 8.1: one flipped spin of the ferromagnet lowers S^z_tot by
# exactly one and has no definite total spin, and the flip spread with a nonzero momentum has a total spin one less, so
# Delta S = 1 belongs to the magnon and not to the single flip (the key box checks above hold this for N = 4, 6 and 8).
# Here the weights of the single flip on the two total spins, (N-1)/N and 1/N, for the rings of the recheck.
wts = {}
for N in (4, 6, 8):
    tot, S2 = stot(N)
    f = op(SX - 1j * SY, 0, N) @ reduce(np.kron, [UP] * N)
    f = f / np.linalg.norm(f)
    s2 = np.vdot(f, S2 @ f).real
    w_low = (N / 2 * (N / 2 + 1) - s2) / (N / 2 * (N / 2 + 1) - (N / 2 - 1) * N / 2)    # weight on S = N/2 - 1
    wts[N] = round(w_low, 6)
check('corrected, paragraph and caption of 8.2: one flipped spin has the weight (N-1)/N on S = N/2 - 1 and 1/N on S = N/2',
      all(np.isclose(wts[N], (N - 1) / N) for N in wts), wts)
# Section 8.1: a ground state that keeps time reversal is entangled, since a product state of spins 1/2 has |<S_i>| = 1/2
# on every site, while the product of singlets of the valence bond solid has the entropy 0 or log 2 across every cut of
# the chains of 4, 8 and 12 sites, so its entanglement is not long-ranged. This is why the class is called entangled and
# not long-range entangled.
rng = np.random.default_rng(11)
prod_ok = True
for _ in range(200):
    a = rng.normal(size=2) + 1j * rng.normal(size=2)
    a = a / np.linalg.norm(a)
    prod_ok = prod_ok and np.isclose(np.linalg.norm([np.vdot(a, s @ a).real for s in (SX, SY, SZ)]), 0.5)
cuts = {}
for N in (4, 8, 12):
    vbs = reduce(np.kron, [SINGLET] * (N // 2))
    ents = []
    for l in range(1, N):
        sv = np.linalg.svd(vbs.reshape(2 ** l, 2 ** (N - l)), compute_uv=False) ** 2
        ents.append(round(-sum(x * np.log(x) for x in sv if x > 1e-12), 6))
    cuts[N] = sorted(set(ents))
check('corrected, Section 8.1: every spin 1/2 of a product state has |<S_i>| = 1/2, and the product of singlets has the '
      'entropy 0 or log 2 = 0.693147 across every cut of 4, 8 and 12 sites',
      prod_ok and all(c == [0.0, round(np.log(2), 6)] for c in cuts.values()), cuts)
