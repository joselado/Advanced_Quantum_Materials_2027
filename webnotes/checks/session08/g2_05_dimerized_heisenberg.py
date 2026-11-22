"""Session 8, the numbers that page 05 (Section 8.5) quotes, checked in the order of the page.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The figure dimerized_levels asserts some of its own numbers, and this script
asserts all of them again. The spins are S = sigma/2, the dimers of (8.4) are the bonds (0,1), (2,3), ..., and the
coupling J' of the figure and of the problem sits on the bond (1,2), as on the conventions sheet. It finds the
repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session08/g2_05_dimerized_heisenberg.py"""
import os, sys
sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
assert os.path.exists(os.path.join(REPO, 'webnotes', 'pages', 'session08'))

import numpy as np

SX = np.array([[0, 1], [1, 0]]) / 2
SY = np.array([[0, -1j], [1j, 0]]) / 2
SZ = np.diag([0.5, -0.5])


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def op(o, i, N):
    m = np.eye(1)
    for j in range(N):
        m = np.kron(m, o if j == i else np.eye(2))
    return m


def SS(i, j, N):
    return sum(op(s, i, N) @ op(s, j, N) for s in (SX, SY, SZ)).real


def multiplicities(w):
    w = np.round(w, 8)
    return {float(v): int((w == v).sum()) for v in np.unique(w)}


# the recall box: the dimer has the singlet at -3/4 and the triplet at +1/4
dimer = multiplicities(np.linalg.eigvalsh(SS(0, 1, 2)))
check('recall, the dimer has -3/4 once and +1/4 three times', dimer == {-0.75: 1, 0.25: 3}, dimer)

# the fold: two dimers have -3/2 once, -1/2 six times and +1/2 nine times
two = multiplicities(np.linalg.eigvalsh(SS(0, 1, 4) + SS(2, 3, 4)))
check('fold, two decoupled dimers have -3/2 (1), -1/2 (6), +1/2 (9)', two == {-1.5: 1, -0.5: 6, 0.5: 9}, two)

# the key box and the fold: E0 = -3NJ/8, nondegenerate, the lowest excitation costs J with 3N/2 states
for N in (4, 6, 8):
    H = sum(SS(2 * n, 2 * n + 1, N) for n in range(N // 2))
    w, v = np.linalg.eigh(H)
    m = multiplicities(w)
    levels = sorted(m)
    gs = v[:, 0]
    mag = max(abs(gs @ op(s, i, N) @ gs) for i in range(N) for s in (SX, SZ))
    check('key box and fold, N = %d sites, E0 = -3N/8, unique, gap 1 with 3N/2 states, <S_i> = 0' % N,
          abs(levels[0] + 3 * N / 8) < 1e-9 and m[levels[0]] == 1 and abs(levels[1] - levels[0] - 1) < 1e-9
          and m[levels[1]] == 3 * N // 2 and mag < 1e-12, (levels[0], m[levels[1]], mag))
    tot = [sum(op(o, i, N) for i in range(N)) for o in (SX, SY, SZ)]
    St2 = sum(t @ t for t in tot).real
    exc = v[:, 1:1 + 3 * N // 2]
    check('key box and fold, N = %d sites, the first excited level has spin 1, S(S+1) = 2' % N,
          np.allclose(exc.T @ St2 @ exc, 2 * np.eye(3 * N // 2)), 'ok')
    bond = [gs @ SS(2 * n, 2 * n + 1, N) @ gs for n in range(N // 2)]
    check('opener, N = %d sites, every bond of (8.4) is at -3/4, its lowest value, so no bond is frustrated' % N,
          max(abs(x + 0.75) for x in bond) < 1e-12 and abs(min(dimer) + 0.75) < 1e-12, bond)

# the fold: one site of the singlet is in the state 1/2 times the identity
s = np.array([0, 1, -1, 0]) / np.sqrt(2)
rho = np.einsum('ijkj->ik', np.outer(s, s).reshape(2, 2, 2, 2))
check('fold, the reduced state of one site of the singlet is 1/2', np.allclose(rho, np.eye(2) / 2), np.diag(rho))

# the caption of dimerized_levels and the second quiz: the open chain of four sites J, J', J
def chain4(Jp):
    return np.linalg.eigvalsh(SS(0, 1, 4) + SS(2, 3, 4) + Jp * SS(1, 2, 4))
e = chain4(0.1)
check('caption and second quiz, J\' = 0.1, ground level -1.501', abs(e[0] + 1.501) < 5e-4, round(e[0], 6))
check('caption and second quiz, J\' = 0.1, next level -0.527, threefold', abs(e[1] + 0.527) < 5e-4
      and abs(e[3] - e[1]) < 1e-9 and e[4] > e[1] + 1e-3, round(e[1], 6))
check('caption and second quiz, J\' = 0.1, gap 0.97', abs(e[1] - e[0] - 0.97) < 5e-3, round(e[1] - e[0], 4))
e1 = chain4(1.0)
check('caption, J\' = J, gap 0.66', abs(e1[1] - e1[0] - 0.66) < 5e-3, round(e1[1] - e1[0], 4))
Stot2 = sum((sum(op(o, i, 4) for i in range(4))) @ (sum(op(o, i, 4) for i in range(4))) for o in (SX, SY, SZ)).real
worst, gap = 0.0, 10.0
for Jp in np.linspace(0, 1, 21):
    w, v = np.linalg.eigh(SS(0, 1, 4) + SS(2, 3, 4) + Jp * SS(1, 2, 4))
    worst, gap = max(worst, abs(v[:, 0] @ Stot2 @ v[:, 0])), min(gap, w[1] - w[0])
check('caption and second quiz, the ground state is a nondegenerate singlet for J\' from 0 to J',
      worst < 1e-9 and gap > 0.6, (worst, round(gap, 4)))

# the first quiz: two spins one half have S(S+1) = 0 or 2, so S = 0 or 1 and never 1/2, and |up up> has S^z = 1
St2_two = sum((op(o, 0, 2) + op(o, 1, 2)) @ (op(o, 0, 2) + op(o, 1, 2)) for o in (SX, SY, SZ)).real
w2 = sorted(set(np.round(np.linalg.eigvalsh(St2_two), 9)))
upup = np.array([1., 0, 0, 0])
Sz_tot = op(SZ, 0, 2) + op(SZ, 1, 2)
check('first quiz, two spins one half have S(S+1) = 0 or 2 only, and |up up> has S^z = 1 and S = 1',
      w2 == [0.0, 2.0] and abs(upup @ Sz_tot @ upup - 1) < 1e-12 and abs(upup @ St2_two @ upup - 2) < 1e-12
      and np.allclose(Sz_tot @ upup, upup), (w2, upup @ Sz_tot @ upup))

# the third quiz: -3NJ/8, and the two wrong options
check('third quiz, N = 4 gives -3/2, the four-site chain at J\' = 0', abs(chain4(0.0)[0] + 1.5) < 1e-12, chain4(0)[0])
check('third quiz, -3NJ/4 at N = 2 gives -3/2, while the dimer has -3/4', -3 * 2 / 4 == -1.5 and min(dimer) == -0.75,
      min(dimer))
zz = s @ (op(SZ, 0, 2) @ op(SZ, 1, 2)) @ s
xx = s @ (op(SX, 0, 2) @ op(SX, 1, 2)) @ s
yy = (s @ (op(SY, 0, 2) @ op(SY, 1, 2)) @ s).real
check('third quiz, the Ising term gives -1/4 per dimer, so -N/8, and x and y add -1/4 each',
      abs(zz + 0.25) < 1e-12 and abs(xx + 0.25) < 1e-12 and abs(yy + 0.25) < 1e-12, (zz, xx, yy))

# the problem: second order in J', -3J'^2/(32J)
ss = np.kron(s, s)
V = SS(1, 2, 4)
check('problem, first order <V> = 0', abs(ss @ V @ ss) < 1e-12, ss @ V @ ss)
Vss = V @ ss
P_tt = np.kron(np.eye(4) - np.outer(s, s), np.eye(4) - np.outer(s, s))
check('problem, V|ss> has both dimers in a triplet, at +1/2, so the denominator is 2J',
      np.allclose(P_tt @ Vss, Vss) and abs(Vss @ (SS(0, 1, 4) + SS(2, 3, 4)) @ Vss / (Vss @ Vss) - 0.5) < 1e-12,
      Vss @ Vss)
corr = np.array([[(s @ op(a, 1, 2) @ op(b, 1, 2) @ s).real for b in (SX, SY, SZ)] for a in (SX, SY, SZ)])
check('problem, <s|S^a S^b|s> = delta_ab / 4, so the norm is 3/16', np.allclose(corr, np.eye(3) / 4)
      and abs(Vss @ Vss - 3 / 16) < 1e-12, np.diag(corr))
pt2 = -1.5 - 3 * 0.1 ** 2 / 32
check('problem, second order at J\' = 0.1J gives -1.500938', abs(pt2 + 1.500938) < 1e-6, pt2)
check('problem, exact diagonalization at J\' = 0.1J gives -1.500961', abs(e[0] + 1.500961) < 1e-6, round(e[0], 7))
check('problem, the two differ by about 2e-5', abs((pt2 - e[0]) - 2e-5) < 0.5e-5, pt2 - e[0])
Jp = 0.1
closed = -0.5 * (1 + Jp / 2) - 0.5 * np.sqrt((2 - Jp / 2) ** 2 + 0.75 * Jp ** 2)
check('problem, the closed form of the conventions sheet gives the same', abs(closed - e[0]) < 1e-12, closed)
