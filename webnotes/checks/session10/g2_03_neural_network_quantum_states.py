"""Session 10, the numbers that page 03 (Section 10.3a, neural network quantum states) quotes.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The figure memory.py and the three pictures of the quiz on the memory,
g2_quiz_memory_*.py with _g2_memoryquiz.py, assert what they draw, and this script asserts the same numbers again,
since the figure scripts run only when their SVG is stale. Memory is counted in decimal units, 1 GB = 1e9 bytes and
1 TB = 1e12 bytes, with 16 bytes for a complex number in double precision. The spin operators are S = sigma/2, so the
two-site Heisenberg model J S1.S2 has the singlet at -3J/4 and the triplet at +J/4. It finds the repository from its
own path, imports nothing of it, and writes no file."""
import numpy as np

BYTES = 16
GB, TB, MB = 1e9, 1e12, 1e6


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def table(L):
    return BYTES * 2.0 ** L


def mps(L, d=2, D=10):
    return BYTES * L * d * D ** 2


def largest_L(limit):
    L = 1
    while table(L + 1) <= limit:
        L += 1
    return L


def configurations(L):
    """s_i = +1 for up, in the order of np.kron with site 0 first and up first."""
    b = np.arange(2 ** L)
    return 1 - 2 * ((b[:, None] >> np.arange(L - 1, -1, -1)) & 1)


def heisenberg(L, J=1.0):
    """The open chain J sum S_i.S_i+1 with S = sigma/2 in the basis of (10.2)."""
    S, n = configurations(L), 2 ** L
    H = np.zeros((n, n))
    for i in range(L - 1):
        H[np.arange(n), np.arange(n)] += J / 4 * S[:, i] * S[:, i + 1]
        anti = np.nonzero(S[:, i] != S[:, i + 1])[0]
        H[anti, anti ^ ((1 << (L - 1 - i)) | (1 << (L - 2 - i)))] += J / 2
    return H


# ------------------------------------------------------------------ the text and the figure memory, decimal units
check('L=30 needs 17.2 GB and L=40 needs 17.6 TB, the "much bigger than 30 or 40" of the text',
      abs(table(30) / GB - 17.2) < 0.05 and abs(table(40) / TB - 17.6) < 0.05, (table(30) / GB, table(40) / TB))
check('16 GB hold the table up to L=29, the caption of memory', largest_L(16 * GB) == 29, largest_L(16 * GB))
check('1 TB holds the table up to L=35, the caption of memory', largest_L(TB) == 35, largest_L(TB))
check('the marks of memory, L=29 at 8.6e9 bytes and L=35 at 5.5e11 bytes',
      abs(table(29) / 1e9 - 8.6) < 0.05 and abs(table(35) / 1e11 - 5.5) < 0.05, (table(29), table(35)))
check('the MPS with D=10 and d=2 at L=300 is 960000 bytes, below a megabyte', mps(300) == 960000 and mps(300) < MB,
      mps(300))
check('the MPS stays below 1e6 bytes up to L=312 and passes it at 313', mps(312) < MB < mps(313), (mps(312), mps(313)))
check('the mark L=40 of memory, 1.8e13 bytes', abs(table(40) / 1e13 - 1.76) < 0.01, table(40))

# ------------------------------------------------------------------------------------ the quiz on L=40 spins
rng_p = np.random.default_rng(3)
local = [rng_p.normal(size=2) + 1j * rng_p.normal(size=2) for _ in range(12)]
prod = local[0]
for v in local[1:]:
    prod = np.kron(prod, v)
S12 = configurations(12)
from_local = np.prod([np.where(S12[:, i] > 0, local[i][0], local[i][1]) for i in range(12)], axis=0)
ranks = [np.linalg.matrix_rank(prod.reshape(2 ** c, 2 ** (12 - c))) for c in range(1, 12)]
check('a product state of 12 spins built from 12 local vectors: C(s) = prod_i a_i(s_i) on all 4096 s, rank 1 at '
      'every cut, so the L d = 24 numbers of the vectors fix it', np.allclose(prod, from_local) and ranks == [1] * 11
      and sum(v.size for v in local) == 24, (np.max(np.abs(prod - from_local)), ranks[:3]))
local40 = [rng_p.normal(size=2) + 1j * rng_p.normal(size=2) for _ in range(40)]
s40 = rng_p.integers(0, 2, size=40)
c40 = np.prod([local40[i][s40[i]] for i in range(40)])
check('a product state of 40 spins is 40 local vectors with 80 numbers in all, and one of its 2^40 coefficients is '
      'their product', sum(v.size for v in local40) == 80 and np.isfinite(c40), sum(v.size for v in local40))
check('2^40 is about 1.1e12 coefficients', abs(2.0 ** 40 / 1e12 - 1.1) < 0.01, 2.0 ** 40)
check('2^40 complex numbers take 1.8e13 bytes, which is 16 TiB', round(table(40) / 1e13, 1) == 1.8
      and table(40) == 16 * 2 ** 40, (table(40), table(40) / 2 ** 40))
check('1e6 numbers is about 2^20', abs(2 ** 20 / 1e6 - 1) < 0.05, 2 ** 20)
check('the table of 20 spins is about 16 MB', abs(table(20) / MB - 16.8) < 0.05, table(20) / MB)
# corrected on 2026-11-22: the options give the sizes in decimal units, as the figure memory and as the quiz of
# Section 7.3, which says 17.6 terabytes in its feedback
check('40^2 numbers of 16 bytes are 25.6 kB, about 26 kilobytes', BYTES * 40 ** 2 == 25600
      and round(BYTES * 40 ** 2 / 1e3) == 26, BYTES * 40 ** 2)
check('1e6 numbers of 16 bytes are 16 MB, about 16 megabytes, the "about 16 MB" of the feedback', BYTES * 1e6 / MB == 16,
      BYTES * 1e6)
check('the correct option, 2^40 numbers of 16 bytes are about 17.6 terabytes, and 16 TiB in binary units',
      round(table(40) / TB, 1) == 17.6 and table(40) / 2 ** 40 == 16, (table(40) / TB, table(40) / 2 ** 40))
check('for 40 spins 2^20 is a factor 1e6 too small', abs(np.log10(2.0 ** 40 / 2.0 ** 20) - 6) < 0.05,
      2.0 ** 20)
N = M = 40
check('a restricted Boltzmann machine with 40 visible and 40 hidden spins has a few thousand parameters, 1680',
      N + M + N * M == 1680, N + M + N * M)

# ------------------------------------------------------------------ the two-site Heisenberg model, quiz and problem
H2 = heisenberg(2)
E = np.linalg.eigvalsh(H2)
check('the two-site Heisenberg model has E0 = -3J/4 and the triplet +J/4 three times',
      np.allclose(E, [-0.75, 0.25, 0.25, 0.25]), E)
check('the quiz value -0.8J is below E0 = -3J/4', -0.8 < E[0], E[0])
E3 = np.linalg.eigvalsh(heisenberg(3))
check('the key box says "a ground state", since E0 can be degenerate, the open chain of 3 spins has E0 = -J twice',
      abs(E3[0] + 1) < 1e-12 and abs(E3[1] + 1) < 1e-12 and E3[2] > -1 + 0.5, E3[:3])
ud, du = 1, 2                                         # the configurations up-down and down-up of the basis
check('H|ud> = J(-1/4 |ud> + 1/2 |du>), the step of the solution', abs(H2[ud, ud] + 0.25) < 1e-14
      and abs(H2[du, ud] - 0.5) < 1e-14 and abs(H2[du, du] + 0.25) < 1e-14, (H2[ud, ud], H2[du, ud]))
alpha = np.linspace(-np.pi, np.pi, 2001)
Ea = []
for a in alpha:
    psi = np.zeros(4)
    psi[ud], psi[du] = np.cos(a), np.sin(a)
    Ea.append(psi @ H2 @ psi)
Ea = np.array(Ea)
check('E(alpha) = J(-1/4 + 1/2 sin 2 alpha) for cos(alpha)|ud> + sin(alpha)|du>',
      np.max(np.abs(Ea - (-0.25 + 0.5 * np.sin(2 * alpha)))) < 1e-14, np.max(np.abs(Ea - (-0.25 + 0.5 * np.sin(2 * alpha)))))
check('E(alpha) is never below E0 = -3J/4 and never above J/4', Ea.min() >= -0.75 - 1e-14 and Ea.max() <= 0.25 + 1e-14,
      (Ea.min(), Ea.max()))
psi = np.zeros(4)
psi[ud], psi[du] = np.cos(-np.pi / 4), np.sin(-np.pi / 4)
ground = np.linalg.eigh(H2)[1][:, 0]
check('the minimum at alpha = -pi/4 is the singlet (|ud> - |du>)/sqrt2 of (7.3), with energy -3J/4',
      abs(abs(ground @ psi) - 1) < 1e-12 and abs(psi @ H2 @ psi + 0.75) < 1e-14, psi @ H2 @ psi)
psi[ud], psi[du] = np.cos(np.pi / 4), np.sin(np.pi / 4)
check('the maximum at alpha = pi/4 is the triplet state (|ud> + |du>)/sqrt2, with energy +J/4',
      np.allclose(H2 @ psi, 0.25 * psi), psi @ H2 @ psi)
weight_out = []
for a, e in zip(alpha, Ea):
    psi = np.zeros(4)
    psi[ud], psi[du] = np.cos(a), np.sin(a)
    weight_out.append(e - (-0.75) - (1 - abs(ground @ psi) ** 2))
check('E(alpha) - E0 = J (1 - |<singlet|psi(alpha)>|^2), J times the weight outside the singlet',
      np.max(np.abs(weight_out)) < 1e-14, np.max(np.abs(weight_out)))

# corrected on 2026-11-22, the sentence after (10.3): the best state of an ansatz that does not contain a ground state
# stays above E0. Product states of the two-site model, two routes: a grid of the two Bloch spheres, and the formula
# <S1>.<S2> = (1/4) n1.n2 for product states, smallest at n1 = -n2
SXh, SYh, SZh = np.array([[0, 1], [1, 0]]) / 2, np.array([[0, -1j], [1j, 0]]) / 2, np.diag([1.0, -1.0]) / 2
Hs = np.real(sum(np.kron(Sa, Sa) for Sa in (SXh, SYh, SZh)))
th_, ph_ = np.meshgrid(np.linspace(0, np.pi, 61), np.linspace(0, 2 * np.pi, 61, endpoint=False))
spinors = np.stack([np.cos(th_ / 2).ravel(), (np.exp(1j * ph_) * np.sin(th_ / 2)).ravel()], axis=1)
prods = np.einsum('ai,bj->abij', spinors, spinors).reshape(len(spinors), len(spinors), 4)
Eprod = np.real(np.einsum('abi,ij,abj->ab', prods.conj(), Hs, prods))
nvec = np.real(np.stack([np.einsum('ai,ij,aj->a', spinors.conj(), Sa, spinors) for Sa in (SXh, SYh, SZh)], axis=1))
Edot = nvec @ nvec.T                                  # <S1>.<S2>, the second route
check('the product states of J S1.S2 reach at best -J/4, above E0 = -3J/4, by a grid of spins and by <S1>.<S2>',
      abs(Eprod.min() + 0.25) < 1e-12 and np.abs(Eprod - Edot).max() < 1e-12 and abs(Edot.min() + 0.25) < 1e-12
      and Eprod.min() > np.linalg.eigvalsh(Hs)[0] + 0.49, (Eprod.min(), Edot.min(), np.linalg.eigvalsh(Hs)[0]))

# ------------------------------------------------------------------------ the steps, the variational bound
E0, E1 = -1.0, 0.5
rng = np.random.default_rng(0)
c = rng.normal(size=(1000, 2)) + 1j * rng.normal(size=(1000, 2))
w = np.abs(c) ** 2
two = (w[:, 0] * E0 + w[:, 1] * E1) / w.sum(1)
check('two levels, E = E0 + |c1|^2 (E1 - E0)/(|c0|^2 + |c1|^2) is never below E0',
      np.allclose(two, E0 + w[:, 1] * (E1 - E0) / w.sum(1)) and two.min() >= E0, two.min())
H8 = heisenberg(8)
En, V = np.linalg.eigh(H8)
z = rng.normal(size=(200, 256)) + 1j * rng.normal(size=(200, 256))
Ez = np.array([np.real(np.vdot(v, H8 @ v)) / np.real(np.vdot(v, v)) for v in z])
cn = z @ V.conj()                                   # the components c_n = <n|psi> in the eigenbasis
Eeig = (np.abs(cn) ** 2 @ En) / np.sum(np.abs(cn) ** 2, axis=1)
check('the open Heisenberg chain of 8 spins, the sum over configurations of (10.3) equals sum |c_n|^2 E_n / sum |c_n|^2',
      np.max(np.abs(Ez - Eeig)) < 1e-12, np.max(np.abs(Ez - Eeig)))
check('and 200 random states stay above E0 = -3.374933', Ez.min() > En[0] and abs(En[0] + 3.374933) < 1e-6,
      (Ez.min(), En[0]))

# --------------------------------------------------------------------------- the picture quiz on the memory
check('the table passes 16 GB at L=30 and 1 TB at L=36', table(29) < 16 * GB < table(30) and table(35) < TB < table(36),
      (table(30), table(36)))
check('one spin more adds log10(2) = 0.30 to log10 of the table, a straight line on a logarithmic axis',
      abs(np.log10(table(31)) - np.log10(table(30)) - 0.30) < 0.005, np.log10(2))
check('16 L^4 at L=40 is 4.1e7 bytes', abs(16 * 40 ** 4 / 1e7 - 4.1) < 0.01, 16 * 40 ** 4)
check('the MPS with d=2 and D=10 at L=40 is 1.3e5 bytes', abs(mps(40) / 1e5 - 1.28) < 0.01, mps(40))
Ls = np.arange(2, 41)
slope = np.diff(np.log10(16.0 * Ls ** 4))
check('16 L^4 rises at every L and more and more slowly on a logarithmic axis, its slope falls with L',
      np.all(slope > 0) and np.all(np.diff(slope) < 0), slope[[0, -1]])
# The alt texts of the three pictures, on the grid of _g2_memoryquiz.py, L from 1 to 40 in 200 points.
Lq = np.linspace(1, 40, 200)
tab, pw, mp = 16 * 2.0 ** Lq, 16 * Lq ** 4, 16 * Lq * 2 * 10 ** 2
check('alt of the table, tens of bytes at small L, 32 at L=1, and above 1e13 bytes at L=40',
      tab[0] == 32 and 10 <= tab[0] < 100 and tab[-1] > 1e13, (tab[0], tab[-1]))
check('alt of the power, rises fast at small L, 1.74 decades per site at L=1, then more and more slowly, and ends '
      'below 1e8 bytes at L=40', np.all(np.diff(pw) > 0) and pw[-1] < 1e8
      and abs((np.log10(16 * (1 + 1e-7) ** 4) - np.log10(16.0)) / 1e-7 - 1.74) < 0.005, (pw[0], pw[-1]))
check('alt of the MPS, almost flat from a few thousand bytes, 3200 at L=1, to about a hundred thousand, 1.28e5 at '
      'L=40', mp[0] == 3200 and 1e3 <= mp[0] < 1e4 and abs(mp[-1] - 1.28e5) < 1 and np.log10(mp[-1] / mp[0]) < 1.7,
      (mp[0], mp[-1]))
print('all checks of page 03 hold')
