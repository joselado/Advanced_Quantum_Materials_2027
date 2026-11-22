"""Session 1, the statements and numbers that page 16 (Section 1.16, the closing summary) quotes.

One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a list is an
assert, here or in the figure script that draws it. The page has no figure script, since its only figure is the
Blender render s01f03_threechannels. This script asserts the numbers of the list of tasks and of the quiz, with the
Fock space built from the Jordan-Wigner matrices of webnotes/conventions/session01.md, and it checks that every
section and equation that the list links exists in the manifest and in the pages. It needs numpy only, finds the
repository from its own path and writes no file."""
import itertools
import json
import os
import re
from math import comb

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
PAGES = os.path.join(ROOT, 'webnotes', 'pages', 'session01')
PAGE = os.path.join(PAGES, '16-closing-summary.md')


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def fermions(n):
    """Annihilation operators of n fermionic modes in the Fock basis |n_0 n_1 ...>, with the Jordan-Wigner sign."""
    a = np.array([[0.0, 1.0], [0.0, 0.0]])
    z = np.diag([1.0, -1.0])
    one = np.eye(2)
    ops = []
    for j in range(n):
        m = np.array([[1.0]])
        for k in range(n):
            m = np.kron(m, z if k < j else (a if k == j else one))
        ops.append(m)
    return ops


def dag(m):
    return m.conj().T


def anti(x, y):
    return x @ y + y @ x


# ---- the links of the list: every section and equation exists ----------------------------------------------------
text = open(PAGE, encoding='utf-8').read()
start = text.index('After this session we can do the following tasks')
end = text.index('::: quiz', start)
tasks = [line for line in text[start:end].splitlines() if line.startswith('- ')]
check('the list has the ten tasks of the plan', len(tasks) == 10, len(tasks))
check('every task names the section that teaches it', all('This is in Section [' in t for t in tasks),
      [t[:40] for t in tasks if 'This is in Section [' not in t])
manifest = json.load(open(os.path.join(ROOT, 'webnotes', 'manifest', 'session01.json'), encoding='utf-8'))
numbers = {}
for p in manifest['pages']:
    numbers[p['id']] = p['number']
    for q in p.get('also', []):
        numbers[q['id']] = q['number']
links = re.findall(r'Section \[([0-9.ab]+)\]\(#(sec-1-[0-9a-z-]+)\)', text[start:end])
bad = [(n, i) for n, i in links if numbers.get(i) != n]
check('each linked section exists and its link text is its number in the manifest', links and not bad, bad or links)
alltext = ''.join(open(os.path.join(PAGES, f), encoding='utf-8').read() for f in os.listdir(PAGES) if f.endswith('.md'))
eqs = re.findall(r'\(#eq-1-(\d+)\)', text[start:end])
missing = [e for e in eqs if '\\tag{1.%s}' % e not in alltext]
check('each linked equation has its tag on a page of the session', eqs and not missing, missing or eqs)
# the conditions written next to the statements after the physics check, findings c1, c2, c3, c4 and c7
check('task 2 names Section 1.6 and the steps of Section 1.7',
      'Section [1.6](#sec-1-6), and the steps are in Section [1.7](#sec-1-7)' in tasks[1], tasks[1][-80:])
check('task 3 counts spinless particles', 'two spinless particles on two sites' in tasks[2], tasks[2][-90:])
check('task 4 names the full diagonalization', 'the full diagonalization of the $2^L$ states' in tasks[3], tasks[3][-90:])
check('task 6 has the range g < J', 'in a transverse field $g<J$' in tasks[5], tasks[5][:90])
check('task 10 names the pair c_i c_j and Delta of (1.9)',
      'the pair $c_ic_j$, and with it $\\Delta$ of [(1.9)](#eq-1-9)' in tasks[9], tasks[9][:90])

# ---- tasks 1 and 3: the algebra (1.3), (c^dagger)^2 = 0, and a number that fluctuates -----------------------------
c = fermions(3)
ok = all(np.allclose(anti(c[i], dag(c[j])), np.eye(8) * (i == j)) and np.allclose(anti(c[i], c[j]), 0)
         for i in range(3) for j in range(3))
check('the Jordan-Wigner matrices of three sites satisfy (1.3)', ok, ok)
sq = max(np.abs(dag(ci) @ dag(ci)).max() for ci in c)
check('(c_i^dagger)^2 = 0 on every site', sq == 0, sq)
c2 = fermions(2)
vac = np.zeros(4)
vac[0] = 1.0
num = dag(c2[0]) @ c2[0] + dag(c2[1]) @ c2[1]
psi = (vac + dag(c2[0]) @ dag(c2[1]) @ vac) / np.sqrt(2)
mean = psi @ num @ psi
var = psi @ num @ num @ psi - mean ** 2
check('the dot in a superposition of zero and two electrons has <N> = 1 and (Delta N)^2 = 1, so N is not fixed',
      np.isclose(mean, 1) and np.isclose(var, 1), (round(mean, 12), round(var, 12)))

# ---- task 2: the levels of the two-site problem (1.2), for both signs of the hopping -----------------------------
for t in (1.0, -1.0):
    h = t * (dag(c2[0]) @ c2[1] + dag(c2[1]) @ c2[0])
    one = [i for i in range(4) if np.isclose(num[i, i], 1)]
    lev = np.linalg.eigvalsh(h[np.ix_(one, one)])
    check('two sites with the hopping %+g, one electron has the levels -|t| and +|t|' % t,
          np.allclose(lev, [-abs(t), abs(t)]), lev)

# ---- task 3: two particles on two sites, one state for fermions and three for bosons ------------------------------
nf = sum(1 for occ in itertools.product((0, 1), repeat=2) if sum(occ) == 2)
nb = sum(1 for occ in itertools.product((0, 1, 2), repeat=2) if sum(occ) == 2)
check('two fermions on two sites have 1 state, two bosons have 3', (nf, nb) == (1, 3), (nf, nb))

# ---- task 4: the Fock space, 2^L and 4^L, and the limit near L = 20 ----------------------------------------------
ok = all(sum(comb(L, N) for N in range(L + 1)) == 2 ** L for L in range(1, 25))
check('sum over N of binom(L, N) is 2^L, L = 1 to 24', ok, ok)
check('three spinless sites give 2^3 = 8 states, and the matrices of three modes are 8 x 8',
      2 ** 3 == 8 and c[0].shape == (8, 8), c[0].shape)
check('three spinful sites give 4^3 = 64 = sum over N of binom(6, N)', 4 ** 3 == 64 == sum(comb(6, N) for N in range(7)),
      4 ** 3)
check('2^20 = 1 048 576, about a million states for L = 20', 2 ** 20 == 1048576, 2 ** 20)
check('4^10 = 2^20, so spinful fermions reach the same size at half the number of sites', 4 ** 10 == 2 ** 20, 4 ** 10)
# the bullet of the summary, corrected on 2026-11-22: "grows as 2^L for spinless fermions and as 4^L with spin", the
# dimension of the Jordan-Wigner matrices of L spinless modes and of 2L modes for L spinful sites
bullet = next(l for l in text.splitlines() if l.startswith('- The many-body Hilbert space grows'))
check('the summary names both growths, 2^L for spinless fermions and 4^L with spin',
      '$2^L$ for spinless fermions and as $4^L$ with spin' in bullet, bullet[:90])
check('the Fock space of L = 1, 2, 3 sites has 2^L states without spin and 4^L with spin',
      all(fermions(L)[0].shape == (2 ** L, 2 ** L) and fermions(2 * L)[0].shape == (4 ** L, 4 ** L) for L in (1, 2, 3)),
      [(2 ** L, 4 ** L) for L in (1, 2, 3)])
# what stops near L = 20 is the full diagonalization, and not the storage of one state: even the largest block of
# fixed N, N = L/2, is a dense real matrix of 1.3 GB at L = 16, 19 GB at L = 18 and 273 GB at L = 20, while one vector
# of the 2^20 coefficients is 8.4 MB
gb = {L: comb(L, L // 2) ** 2 * 8 / 1e9 for L in (16, 18, 20)}
check('largest block of fixed N, dense in 8-byte reals, 1.3 GB at L = 16, 19 GB at L = 18, 273 GB at L = 20',
      round(gb[16], 1) == 1.3 and round(gb[18]) == 19 and round(gb[20]) == 273 and comb(20, 10) == 184756,
      {L: round(v, 2) for L, v in gb.items()})
check('the whole 2^20 x 2^20 matrix is 8.8 TB, one vector of 2^20 coefficients is 8.4 MB',
      round((2 ** 20) ** 2 * 8 / 1e12, 1) == 8.8 and round(2 ** 20 * 8 / 1e6, 1) == 8.4,
      ((2 ** 20) ** 2 * 8 / 1e12, 2 ** 20 * 8 / 1e6))

# ---- task 5: the levels of a finite chain and their spacing at the center -----------------------------------------
spacing = {}
for N in (10, 100):
    h = -(np.eye(N, k=1) + np.eye(N, k=-1))
    lev = np.linalg.eigvalsh(h)
    exact = np.sort(-2 * np.cos(np.arange(1, N + 1) * np.pi / (N + 1)))
    assert np.allclose(lev, exact)
    spacing[N] = 4 * np.sin(np.pi / (2 * (N + 1)))
    gaps = np.diff(lev)
    check('the open chain of %d sites, levels inside -2t to 2t and the spacing at the center %.4f t' % (N, spacing[N]),
          lev.min() > -2 and lev.max() < 2 and np.isclose(gaps[N // 2 - 1], spacing[N]), round(gaps[N // 2 - 1], 4))
check('the spacing shrinks when the chain grows, 0.569t for 10 sites and 0.0622t for 100',
      round(spacing[10], 3) == 0.569 and round(spacing[100], 4) == 0.0622 and spacing[100] < spacing[10],
      (round(spacing[10], 4), round(spacing[100], 4)))

# ---- task 6: the two lowest states of the open Ising chain, and their splitting that falls with L ------------------
sx = np.array([[0.0, 1.0], [1.0, 0.0]])
sz = np.diag([1.0, -1.0])


def site(op, i, L):
    m = np.array([[1.0]])
    for k in range(L):
        m = np.kron(m, op if k == i else np.eye(2))
    return m


split = {}
for L in (4, 6, 8):
    J, g = 1.0, 0.3
    H = -J * sum(site(sz, i, L) @ site(sz, i + 1, L) for i in range(L - 1)) - g * sum(site(sx, i, L) for i in range(L))
    flip = np.array([[1.0]])
    for k in range(L):
        flip = np.kron(flip, sx)
    e, v = np.linalg.eigh(H)
    parity = [v[:, n] @ flip @ v[:, n] for n in (0, 1)]
    split[L] = e[1] - e[0]
    check('Ising chain of %d spins at g = 0.3J, the two lowest states are even and odd under the flip, split by %.2e J'
          % (L, split[L]), np.isclose(parity[0], 1) and np.isclose(parity[1], -1) and split[L] > 0,
          (np.round(parity, 6), split[L]))
check('the splitting falls with L, roughly as (g/J)^L', split[4] > split[6] > split[8] > 0
      and abs(np.log(split[8] / split[6]) / 2 - np.log(0.3)) < 0.15,
      (np.log(split[8] / split[6]) / 2, np.log(0.3)))


def free_fermion_split(L, g, J=1.0):
    """Gap of the open chain from its free fermions, twice the smallest singular value of the Majorana matrix."""
    M = np.diag(np.full(L, g)) + np.diag(np.full(L - 1, J), 1)
    return 2 * np.linalg.svd(M, compute_uv=False).min()


ff = {L: free_fermion_split(L, 0.3) for L in (4, 6, 8)}
check('free fermions give the splitting of the exact diagonalization at g = 0.3J, L = 4, 6, 8',
      all(abs(ff[L] / split[L] - 1) < 1e-9 for L in ff), {L: ff[L] for L in ff})
# the range g < J of task 6: below J the splitting goes to zero with L, above J it goes to 2(g - J)
below = {g: [free_fermion_split(L, g) for L in (20, 50, 100, 200)] for g in (0.5, 0.9)}
check('for g = 0.5J and 0.9J the splitting falls with L and is below 1e-9 J at L = 200',
      all(np.all(np.diff(v) < 0) and v[-1] < 1e-9 for v in below.values()), {g: v[-1] for g, v in below.items()})
above = [free_fermion_split(L, 1.5) for L in (10, 50, 400)]
check('for g = 1.5J the splitting does not vanish, it goes to 2(g - J) = 1.0J',
      above[0] > above[1] > above[2] > 1.0 and abs(above[2] - 1.0) < 1e-3, np.round(above, 4))

# ---- task 7: the test (1.4) on two spins can be done, with T = i sigma_y K on each spin -----------------------------
# the task applies the test to two spins, an even number, where T^2 = +1. Since 2026-11-22 page 11b says after (1.4)
# that equal means equal up to a phase and that the test is for an even number of electrons, which g3_11b checks, so
# this checks that the test of a state of two spins has a definite answer for the two states of Section 1.11b
isy = np.array([[0.0, 1.0], [-1.0, 0.0]])
U2 = np.kron(isy, isy)
up, dn = np.array([1.0, 0.0]), np.array([0.0, 1.0])
singlet = (np.kron(up, dn) - np.kron(dn, up)) / np.sqrt(2)
neel = np.kron(up, dn)
check('T = i sigma_y K on each spin gives T^2 = +1 on two spins and -1 on one',
      np.allclose(U2 @ U2.conj(), np.eye(4)) and np.allclose(isy @ isy.conj(), -np.eye(2)), True)
check('T of the singlet is the singlet', np.allclose(U2 @ singlet.conj(), singlet), np.round(U2 @ singlet, 6))
check('T of |up down> is -|down up>, orthogonal to |up down>',
      np.allclose(U2 @ neel.conj(), -np.kron(dn, up)) and abs(neel @ (U2 @ neel)) < 1e-12, np.round(U2 @ neel, 6))

# ---- task 8: the decoupling of a quartic term and one pass of the loop ---------------------------------------------
cs = fermions(2)  # one site with spin, modes up and down
nu, nd = dag(cs[0]) @ cs[0], dag(cs[1]) @ cs[1]
a, b = 0.37, 0.81
rest = nu @ nd - (a * nd + nu * b - a * b * np.eye(4))
fluct = (nu - a * np.eye(4)) @ (nd - b * np.eye(4))
check('n_up n_dn = <n_up> n_dn + n_up <n_dn> - <n_up><n_dn> + the fluctuations, as an operator identity',
      np.allclose(rest, fluct), np.abs(rest - fluct).max())
ring = -(np.eye(4, k=1) + np.eye(4, k=-1))
ring[0, 3] = ring[3, 0] = -1.0
V = 3.0
guess = np.array([0.6, 0.4, 0.6, 0.4])
onsite = V * (np.roll(guess, 1) + np.roll(guess, -1))
e, v = np.linalg.eigh(ring + np.diag(onsite))
new = (np.abs(v[:, :2]) ** 2).sum(axis=1)
check('one pass of the loop on the ring of four sites at V = 3t, from 0.6 and 0.4 to 0.82 and 0.18',
      np.allclose(onsite, [2.4, 3.6, 2.4, 3.6]) and np.allclose(new, [0.8218, 0.1782, 0.8218, 0.1782], atol=1e-4),
      np.round(new, 4))

# ---- task 9: the antiferromagnetic mean field of the Hubbard dimer, the moment from U = 2t -------------------------


def dimer_map(U, m):
    """One pass of the Hartree loop of the half-filled dimer, from the moment m to the new one, t = 1."""
    n_up = np.array([1 + m, 1 - m]) / 2
    n_dn = 1 - n_up
    new = []
    for dens in (n_dn, n_up):  # spin up feels U n_dn, spin down feels U n_up
        e, v = np.linalg.eigh(np.array([[U * dens[0], -1.0], [-1.0, U * dens[1]]]))
        new.append(np.abs(v[:, 0]) ** 2)
    return new[0][0] - new[1][0]


def dimer_moment(U, m=0.5, steps=20000):
    """Hartree loop of the half-filled dimer with the guess n_up = (1 +- m)/2 on the two sites, t = 1."""
    for _ in range(steps):
        m_new = dimer_map(U, m)
        if abs(m_new - m) < 1e-14:
            return m_new
        m = m_new
    return m


# the moment appears at U = 2t because the map m -> m' has the slope U/2t at m = 0, so m = 0 stops being stable there
slope = {U: (dimer_map(U, 1e-6) - dimer_map(U, -1e-6)) / 2e-6 for U in (1.0, 2.0, 3.0)}
check('the slope of the loop at m = 0 is U/2t, 0.5, 1 and 1.5 at U = t, 2t and 3t, so the moment appears at U = 2t',
      all(abs(s - U / 2) < 1e-6 for U, s in slope.items()), slope)


for U in (1.0, 1.5, 1.9):
    m = dimer_moment(U)
    check('dimer at U = %.1ft, the loop from m = 0.5 ends at m = 0' % U, abs(m) < 1e-6, m)
for U, ref in ((2.1, 0.305), (3.0, 0.745), (4.0, 0.866)):
    m = dimer_moment(U)
    check('dimer at U = %.1ft, m = sqrt(1 - 4t^2/U^2) = %.3f' % (U, ref),
          np.isclose(m, np.sqrt(1 - 4 / U ** 2), atol=1e-6) and round(m, 3) == ref, round(m, 6))

# ---- task 10: the gauge transformation (1.10) and the pairing term -------------------------------------------------
phi = 0.7
G = np.diag(np.exp(1j * phi * np.diag(num)))  # e^{i phi N} on two modes
tr = [G.conj() @ ci @ G for ci in c2]  # e^{-i phi N} c e^{i phi N}
check('e^{-i phi N} c e^{i phi N} = e^{i phi} c', all(np.allclose(x, np.exp(1j * phi) * ci) for x, ci in zip(tr, c2)), phi)
pair = c2[0] @ c2[1]
check('c_i c_j gets e^{2 i phi}, c_i^dagger c_j does not change',
      np.allclose(tr[0] @ tr[1], np.exp(2j * phi) * pair)
      and np.allclose(dag(tr[0]) @ tr[1], dag(c2[0]) @ c2[1]), phi)
check('for phi = pi/2 the pair gets e^{i pi} = -1', np.isclose(np.exp(2j * np.pi / 2), -1), np.exp(1j * np.pi))
# Delta = <c_i c_j> of (1.9), in a state where it is not zero, gets the same factor e^{2 i phi} when the operators are
# transformed as in (1.10)
D0 = psi.conj() @ pair @ psi
D1 = psi.conj() @ (tr[0] @ tr[1]) @ psi
check('Delta = <c_0 c_1> = %.2f in the dot state, and it becomes e^{2 i phi} Delta' % D0.real,
      abs(D0) > 0.4 and np.isclose(D1, np.exp(2j * phi) * D0), (D0, D1))

# ---- the quiz: a pairing term changes N by 2 and keeps the parity, and a real Delta keeps time reversal -------------
ns = nu + nd
P = np.diag((-1.0) ** np.diag(ns))
cdcd = dag(cs[0]) @ dag(cs[1])
check('[N, c_up^dagger c_dn^dagger] = 2 c_up^dagger c_dn^dagger, so the pair term joins N and N + 2',
      np.allclose(ns @ cdcd - cdcd @ ns, 2 * cdcd), True)
Hp = -0.3 * ns + 0.8 * (cdcd + dag(cdcd))
e, v = np.linalg.eigh(Hp)
g0 = v[:, 0]
varN = g0 @ ns @ ns @ g0 - (g0 @ ns @ g0) ** 2
check('the pairing term commutes with the parity (-1)^N and not with N',
      np.allclose(P @ Hp, Hp @ P) and not np.allclose(ns @ Hp, Hp @ ns), True)
check('its ground state is even, with the variance of N equal to 0.877',
      np.isclose(g0 @ P @ g0, 1) and round(varN, 3) == 0.877, round(varN, 4))
# time reversal i sigma_y K of the sheet on one site, |up> -> -|down> and |down> -> |up>, so T c_up T^-1 = -c_dn and
# T c_dn T^-1 = c_up, written as T = U K in the Fock basis |n_up n_dn>
UT = np.zeros((4, 4))
UT[0, 0] = 1.0  # |0> -> |0>
UT[1, 2] = -1.0  # |up> = |10> (index 2) -> -|down> = -|01> (index 1)
UT[2, 1] = 1.0  # |down> -> |up>
UT[3, 3] = 1.0  # |up down> = c_up^dagger c_dn^dagger|0> -> (-c_dn^dagger)(c_up^dagger)|0> = |up down>
one_electron = UT[np.ix_([2, 1], [2, 1])]  # the block of |up>, |down>, in this order
ok = (np.allclose(one_electron, isy) and np.allclose(UT @ cs[0].conj() @ UT.T, -cs[1])
      and np.allclose(UT @ cs[1].conj() @ UT.T, cs[0]))
check('this T is i sigma_y K on one electron, and it sends c_up to -c_dn and c_dn to c_up', ok, ok)


def pairing(delta):
    return -0.3 * ns + delta * cdcd + np.conj(delta) * dag(cdcd)


real_ok = np.allclose(UT @ pairing(0.8).conj() @ UT.T, pairing(0.8))
cplx_ok = np.allclose(UT @ pairing(0.8j).conj() @ UT.T, pairing(0.8j))
check('a real Delta keeps time reversal, Delta = 0.8i in this gauge does not', real_ok and not cplx_ok, (real_ok, cplx_ok))
# second route, the pairing matrix of the term sum_{s s'} D_{s s'} c_s^dagger c_s'^dagger / 2, with the singlet
# D = Delta i sigma_y, goes under time reversal to (i sigma_y) D^* (i sigma_y)^T
for delta, keeps in ((0.8, True), (0.8j, False)):
    D = delta * isy
    DT = isy @ D.conj() @ isy.T
    check('pairing matrix Delta i sigma_y with Delta = %s, time reversal gives Delta^* i sigma_y, kept: %s'
          % (delta, keeps), np.allclose(DT, np.conj(delta) * isy) and np.allclose(DT, D) == keeps, np.round(DT, 3))

# ---- the quiz on a ring of four spinful sites, t = 1, mu = 0.3 and the onsite pairing Delta ----------------------
# findings c5 and c6 of the physics check, on old text that stays: the number of electrons of the ground state takes
# every even value, not only N and N +- 2, and a uniform phase of Delta is removed by the gauge transformation (1.10)
R = 4
cr = fermions(2 * R)  # mode 2i is site i with spin up, mode 2i + 1 the same site with spin down
Nr = sum(dag(x) @ x for x in cr)
nr = np.diag(Nr)


def ring(delta, t=1.0, mu=0.3):
    H = np.zeros(Nr.shape, dtype=complex)
    for i in range(R):
        j = (i + 1) % R
        for s in (0, 1):
            H -= t * (dag(cr[2 * i + s]) @ cr[2 * j + s] + dag(cr[2 * j + s]) @ cr[2 * i + s])
        pr = dag(cr[2 * i]) @ dag(cr[2 * i + 1])
        H += -mu * (dag(cr[2 * i]) @ cr[2 * i] + dag(cr[2 * i + 1]) @ cr[2 * i + 1]) + delta * pr + np.conj(delta) * dag(pr)
    return H


e, v = np.linalg.eigh(ring(0.8))
PN = np.array([np.sum(np.abs(v[nr == n, 0]) ** 2) for n in range(2 * R + 1)])
check('ring of 4 sites at Delta = 0.8, the ground state has no weight on odd N',
      np.all(PN[1::2] < 1e-20) and np.isclose(PN.sum(), 1), np.round(PN, 4))
check('its weight is on the five even values N = 0, 2, 4, 6, 8, 0.003, 0.109, 0.423, 0.444, 0.021',
      np.allclose(PN[0::2], [0.0028, 0.1092, 0.4234, 0.4435, 0.0211], atol=1e-4), np.round(PN[0::2], 4))
check('old feedback corrected on 2026-11-22: with N = 4 the weights on N - 4 and N + 4 are nonzero too, 0.0028 and '
      '0.0211, so the state is a superposition of N, N +- 2, N +- 4',
      PN[0] > 1e-3 and PN[8] > 1e-3 and PN[2] > 1e-3 and PN[6] > 1e-3, np.round(PN[[0, 2, 6, 8]], 4))
E0 = {d: np.linalg.eigvalsh(ring(d))[0] for d in (0.8, 0.8j, 0.8 * np.exp(0.6j))}
check('the lowest level is the same, -7.2228t, for Delta = 0.8, 0.8i and 0.8 e^{0.6i}',
      max(E0.values()) - min(E0.values()) < 1e-12 and round(E0[0.8], 4) == -7.2228, E0)
Gr = np.diag(np.exp(1j * 0.3 * nr))
d = 0.8 * np.exp(0.6j)
check('e^{-i phi N} H(Delta) e^{i phi N} = H(Delta e^{-2 i phi}), so phi = arg(Delta)/2 makes Delta real',
      np.allclose(Gr.conj() @ ring(d) @ Gr, ring(d * np.exp(-0.6j))) and np.isclose(d * np.exp(-0.6j), 0.8), 0.3)

print('all checks of page 16 passed')
