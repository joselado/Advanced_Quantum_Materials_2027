"""Session 7, the statements of page 02b (Section 7.2b), the Jordan-Wigner transformation (7.2).

The sites are numbered from 1 as on the page and in Figure 7.1, and site i is the index i-1 of the matrices. The
script builds the spins of 8 sites as matrices, defines the fermions with (7.2), c_i = K_i S^-_i, and checks the
anticommutation, the string of the first site, the signs of the picture quiz and of Figure 7.1, the fold on two sites,
the problem on two sites and the options of the quiz on the XX coupling. The numbers of the caption of xx_spectrum are
asserted here in numpy and in its own script from pyqula, and the closing bond of a ring in the fold here. It reads the
occupations of Figure 7.1 from lecture_notes/src/figures/blender/s07f01_jwstring.py and those of the picture quiz from
webnotes/figures/session07/g1_quiz_string_N.py. It needs numpy only and writes no file."""
import ast
import itertools
import os
import re
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def spins(L):
    """S^+, S^-, S^z and n = S^z + 1/2 of L spins 1/2, in the basis (up, down) of each site, site 1 first."""
    sp = np.array([[0., 1.], [0., 0.]])
    sz = np.diag([.5, -.5])
    def site(op, i):
        out = np.eye(1)
        for j in range(L):
            out = np.kron(out, op if j == i else np.eye(2))
        return out
    Sp = [site(sp, i) for i in range(L)]
    Sm = [m.T for m in Sp]
    Sz = [site(sz, i) for i in range(L)]
    n = [z + 0.5 * np.eye(2 ** L) for z in Sz]
    return Sp, Sm, Sz, n


d = lambda m: m.conj().T
L = 8
Sp, Sm, Sz, n = spins(L)
I = np.eye(2 ** L)
# K_i = exp(i pi sum_{j<i} n_j), with the matrix exponential of a diagonal matrix
K = []
for i in range(L):
    occ = sum((n[j] for j in range(i)), np.zeros((2 ** L, 2 ** L)))
    K.append(np.diag(np.exp(1j * np.pi * np.diag(occ))).real)
check('exp(i pi n_j) = 1 - 2 n_j, so K_i = prod_{j<i} (1 - 2 n_j)',
      all(np.allclose(K[i], np.linalg.multi_dot([I, I] + [I - 2 * n[j] for j in range(i)])) for i in range(L)), 'ok')
check('K_1 = 1, the string of the first site', np.allclose(K[0], I), 'ok')
check('K_i^2 = 1, so the eigenvalues of the string are +1 and -1',
      all(np.allclose(k @ k, I) for k in K) and set(np.unique(np.diag(K[5]))) == {-1.0, 1.0}, 'ok')
c = [K[i] @ Sm[i] for i in range(L)]
ok = True
for i, j in itertools.product(range(L), repeat=2):
    ok = ok and np.allclose(c[i] @ d(c[j]) + d(c[j]) @ c[i], (i == j) * I)
    ok = ok and np.allclose(c[i] @ c[j] + c[j] @ c[i], 0)
check('c_i = K_i S^-_i anticommute on every pair of 8 sites', ok, 'ok')
check('S^+_i = c^dag_i K_i and S^-_i = c_i K_i on every site',
      all(np.allclose(Sp[i], d(c[i]) @ K[i]) and np.allclose(Sm[i], c[i] @ K[i]) for i in range(L)), 'ok')
check('S^z_i = n_i - 1/2 with n_i = c^dag_i c_i', all(np.allclose(Sz[i], d(c[i]) @ c[i] - 0.5 * I) for i in range(L)), 'ok')
check('K_i commutes with the operators of the sites j >= i',
      all(np.allclose(K[i] @ c[j], c[j] @ K[i]) for i in range(L) for j in range(i, L)), 'ok')


def basis_state(occupied):
    """The product state with up spins (fermions) on the listed sites, numbered from 1."""
    v = np.array([1.])
    for s in range(1, L + 1):
        v = np.kron(v, [1., 0.] if s in occupied else [0., 1.])
    return v


def K6_on(occupied):
    v = basis_state(occupied)
    val = v @ K[5] @ v
    assert np.allclose(K[5] @ v, val * v)
    return val


# Figure 7.1, the occupations read from its Blender script, the chain behind on 1, 3, 4, 7 and the one in front on
# 1, 4, 7, 8, so three and two fermions to the left of site 6, as the caption says
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
blender = open(os.path.join(REPO, 'lecture_notes', 'src', 'figures', 'blender', 's07f01_jwstring.py'), encoding='utf-8').read()
OCC = ast.literal_eval(re.search(r'^OCC\s*=\s*(\{.*\})\s*$', blender, re.M).group(1))
fig = {k: {i + 1 for i, o in enumerate(v) if o} for k, v in OCC.items()}
check('Figure 7.1, the chains behind and in front hold the fermions on the sites', fig == {'back': {1, 3, 4, 7},
      'front': {1, 4, 7, 8}}, fig)
left = {k: len([i for i in v if i < 6]) for k, v in fig.items()}
check('Figure 7.1, three fermions to the left of site 6 in the chain behind and two in the chain in front, site 6 empty',
      left == {'back': 3, 'front': 2} and all(6 not in v for v in fig.values()), left)
check('Figure 7.1, K_6 = -1 for the chain behind and +1 for the chain in front',
      K6_on(fig['back']) == -1 and K6_on(fig['front']) == 1, (K6_on(fig['back']), K6_on(fig['front'])))
# the caption, corrected on 2026-11-22: the two chains differ in the occupations of the sites 3 and 8, not only to the
# left of site 6, and site 8 is to the right of site 6, so it does not enter K_6
differ = sorted(fig['back'] ^ fig['front'])
check('Figure 7.1 caption, the two chains differ in the occupations of the sites 3 and 8, and both hold four fermions',
      differ == [3, 8] and len(fig['back']) == len(fig['front']) == 4, differ)
# the picture quiz, sites 1 to 6 of the drawing, with site 6 empty, occupations that Figure 7.1 does not show
quiz = {2: {2, 5}, 3: {2, 3, 5}, 4: {1, 2, 3, 5}}
check('picture quiz, no option is a chain of Figure 7.1 on the sites 1 to 5',
      all(o != {i for i in v if i < 6} for o in quiz.values() for v in fig.values()), quiz)
drawn = {}
for N in (2, 3, 4):
    src = open(os.path.join(REPO, 'webnotes', 'figures', 'session07', f'g1_quiz_string_{N}.py'), encoding='utf-8').read()
    drawn[N] = set(ast.literal_eval(re.search(r'draw\(__file__, (\([0-9, ]+\))\)', src).group(1)))
check('picture quiz, the three scripts g1_quiz_string_N.py draw the occupations of this check', drawn == quiz, drawn)
vals = {}
for N, occ in quiz.items():
    v = basis_state(occ)
    a = Sp[5] @ v
    b = d(c[5]) @ v
    vals[N] = (K6_on(occ), round(float(a @ b) / float(b @ b), 12))
check('picture quiz, S^+_6 = -c^dag_6 for 3 fermions on the sites 1 to 5, and +c^dag_6 for 2 and 4',
      vals[3] == (-1, -1) and vals[2] == (1, 1) and vals[4] == (1, 1), vals)
check('picture quiz, c^dag_6 does not vanish on the three chains, since site 6 is empty',
      all(np.linalg.norm(d(c[5]) @ basis_state(o)) > 0.5 for o in quiz.values()), 'ok')

# the fold, two sites
Sp2, Sm2, Sz2, n2 = spins(2)
I4 = np.eye(4)
K2 = I4 - 2 * n2[0]
c1, c2 = Sm2[0], K2 @ Sm2[1]
check('two sites, K_2 = 1 - 2 n_1 and c_1, c_2 anticommute',
      np.allclose(c1 @ c2 + c2 @ c1, 0) and np.allclose(c1 @ d(c2) + d(c2) @ c1, 0), 'ok')
check('c^dag_1 (1 - 2 n_1) = c^dag_1', np.allclose(d(c1) @ K2, d(c1)), 'ok')
check('(1 - 2 n_1) c^dag_1 = -c^dag_1', np.allclose(K2 @ d(c1), -d(c1)), 'ok')
check('S^+_1 S^+_2 = S^+_2 S^+_1 = c^dag_1 c^dag_2',
      np.allclose(Sp2[0] @ Sp2[1], Sp2[1] @ Sp2[0]) and np.allclose(Sp2[0] @ Sp2[1], d(c1) @ d(c2)), 'ok')
check('S^+_1 S^-_2 = c^dag_1 c_2 and S^-_1 S^+_2 = c^dag_2 c_1',
      np.allclose(Sp2[0] @ Sm2[1], d(c1) @ c2) and np.allclose(Sm2[0] @ Sp2[1], d(c2) @ c1), 'ok')
check('neighbors of 8 sites, S^+_i S^-_{i+1} = c^dag_i c_{i+1} and S^-_i S^+_{i+1} = c^dag_{i+1} c_i',
      all(np.allclose(Sp[i] @ Sm[i + 1], d(c[i]) @ c[i + 1]) and np.allclose(Sm[i] @ Sp[i + 1], d(c[i + 1]) @ c[i])
          for i in range(L - 1)), 'ok')
check('sites 1 and 3, S^+_1 S^-_3 = c^dag_1 (1 - 2 n_2) c_3, the string of site 2 stays',
      np.allclose(Sp[0] @ Sm[2], d(c[0]) @ (I - 2 * n[1]) @ c[2]) and not np.allclose(Sp[0] @ Sm[2], d(c[0]) @ c[2]), 'ok')

# the problem, J (S^x_1 S^x_2 + S^y_1 S^y_2) on two sites
J = 1.0
sx = [(Sp2[i] + Sm2[i]) / 2 for i in range(2)]
sy = [(Sp2[i] - Sm2[i]) / 2j for i in range(2)]
Hxx = J * (sx[0] @ sx[1] + sy[0] @ sy[1])
Hf = 0.5 * J * (d(c1) @ c2 + d(c2) @ c1)
check('J (SxSx + SySy) = (J/2)(S+S- + S-S+) = (J/2)(c^dag_1 c_2 + h.c.)',
      np.allclose(Hxx, 0.5 * J * (Sp2[0] @ Sm2[1] + Sm2[0] @ Sp2[1])) and np.allclose(Hxx, Hf), 'ok')
check('the levels of the two-site XX coupling are -J/2, 0, 0, J/2', np.allclose(np.linalg.eigvalsh(Hxx), [-.5, 0, 0, .5]),
      np.round(np.linalg.eigvalsh(Hxx), 6))
N2 = d(c1) @ c1 + d(c2) @ c2
h1 = np.array([[0, .5], [.5, 0]])                        # one fermion, the hopping J/2 between the two sites
check('one fermion gives +-J/2, zero and two fermions give 0',
      np.allclose(np.linalg.eigvalsh(h1), [-.5, .5]) and all(
          np.allclose(Hf @ basis, 0) for basis in (np.kron([0, 1.], [0, 1.]), np.kron([1., 0], [1., 0]))), 'ok')
check('the ground state of the two sites is the bonding state with one fermion, S^z_tot = 0',
      np.isclose(np.linalg.eigh(Hxx)[1][:, 0] @ N2 @ np.linalg.eigh(Hxx)[1][:, 0], 1.0), 'ok')

# the quiz on the XX coupling of two neighbors, its two wrong options
Hw1 = J * (d(c1) @ c2 + d(c2) @ c1)
check('wrong option J(c^dag c + h.c.) gives the levels -J and J for one fermion, not +-J/2',
      np.allclose(np.linalg.eigvalsh(Hw1), [-1, 0, 0, 1]) and not np.allclose(Hw1, Hxx), np.round(np.linalg.eigvalsh(Hw1), 6))
Hw2 = 0.5 * J * (d(c1) @ d(c2) + c2 @ c1)
check('wrong option (J/2)(c^dag c^dag + h.c.) is J (SxSx - SySy), which changes S^z_tot by 2',
      np.allclose(Hw2, J * (sx[0] @ sx[1] - sy[0] @ sy[1])) and not np.allclose(Hw2 @ N2, N2 @ Hw2), 'ok')
check('the pairing option has the same four levels, so the levels do not separate it',
      np.allclose(np.linalg.eigvalsh(Hw2), np.linalg.eigvalsh(Hxx)), np.round(np.linalg.eigvalsh(Hw2), 6))
Szt = Sz2[0] + Sz2[1]
check('the XX coupling keeps S^z_tot, the pairing option does not',
      np.allclose(Hxx @ Szt, Szt @ Hxx) and not np.allclose(Hw2 @ Szt, Szt @ Hw2), 'ok')
pair = d(c1) @ d(c2)
check('the pairing option changes S^z_tot by 2, [S^z_tot, c^dag_1 c^dag_2] = 2 c^dag_1 c^dag_2 and the h.c. gives -2',
      np.allclose(Szt @ pair - pair @ Szt, 2 * pair) and np.allclose(Szt @ d(pair) - d(pair) @ Szt, -2 * d(pair)), 2)
# the problem, the number of fermions is N = S^z_tot + 1 on two sites, and S^z_tot + 4 on 8 sites
check('the problem, N = S^z_tot + 1 on two sites, as operators', np.allclose(N2, Szt + I4), 'ok')
check('N = S^z_tot + L/2 on 8 sites, as operators', np.allclose(sum(d(x) @ x for x in c), sum(Sz) + 4 * I), 'ok')

# second quiz, first feedback, on a chain of one site S^+ takes down to up with the matrix element +1, and K_1 = -1
# would give -1
sp1 = np.array([[0., 1.], [0., 0.]])
upv, dnv = np.array([1., 0.]), np.array([0., 1.])
check('one site, <up|S^+|down> = +1, and -S^+ would give -1', upv @ sp1 @ dnv == 1 and upv @ (-sp1) @ dnv == -1,
      (upv @ sp1 @ dnv, upv @ (-sp1) @ dnv))

# the caption of xx_spectrum, also asserted in its own script: the open XX chain of 6 spins is a 64 x 64 matrix, its
# levels are the sums of the single-particle levels J cos(pi k/7), k = 1 to 6, of the hopping J/2, with N = S^z_tot + 3
L6 = 6
Sp6, Sm6, Sz6, n6 = spins(L6)
H6 = sum(0.5 * J * (Sp6[i] @ Sm6[i + 1] + Sm6[i] @ Sp6[i + 1]) for i in range(L6 - 1))
h6 = 0.5 * J * (np.eye(L6, k=1) + np.eye(L6, k=-1))
eps6 = np.linalg.eigvalsh(h6)
check('xx_spectrum, the spin Hamiltonian of 6 sites is a 64 x 64 matrix', H6.shape == (64, 64), H6.shape)
check('xx_spectrum, the hopping J/2 on 6 open sites gives J cos(pi k/7), k = 1 to 6',
      np.allclose(np.sort(eps6), np.sort(J * np.cos(np.pi * np.arange(1, 7) / 7))), np.round(eps6, 6))
szd6 = np.round(np.diag(sum(Sz6)), 6)
ok = True
for Nf in range(L6 + 1):
    ix = np.where(np.isclose(szd6 + 3, Nf))[0]
    ok = ok and np.allclose(np.linalg.eigvalsh(H6[np.ix_(ix, ix)]),
                            np.sort([sum(cmb) for cmb in itertools.combinations(eps6, Nf)]), atol=1e-10)
check('xx_spectrum, the 64 spin levels with S^z_tot = N - 3 are the sums of N single-particle levels', ok, 'ok')
E6 = np.linalg.eigvalsh(H6)[0]
check('xx_spectrum, the ground energy is -1.7470 J, the three negative levels filled',
      abs(E6 + 1.7469796) < 1e-6 and abs(E6 - eps6[eps6 < 0].sum()) < 1e-10, round(E6, 6))

# the fold, a ring. The closing bond keeps the string of the sites 2 to L-1, S^+_L S^-_1 = -(-1)^N c^dag_L c_1, so the
# fermions are periodic for an odd N and antiperiodic for an even N
par = np.diag((-1.0) ** np.round(np.diag(sum(n))))
check('ring of 8 sites, S^+_8 S^-_1 = -(-1)^N c^dag_8 c_1', np.allclose(Sp[7] @ Sm[0], -d(c[7]) @ c[0] @ par)
      and not np.allclose(Sp[7] @ Sm[0], d(c[7]) @ c[0]), 'ok')
ok, E0 = True, {}
for Lr in (6, 8):
    Spr, Smr, Szr, nr = (Sp6, Sm6, Sz6, n6) if Lr == 6 else (Sp, Sm, Sz, n)
    Hr = sum(0.5 * J * (Spr[i] @ Smr[(i + 1) % Lr] + Smr[i] @ Spr[(i + 1) % Lr]) for i in range(Lr))
    szr = np.round(np.diag(sum(Szr)), 6)
    for Nf in range(1, Lr):
        ix = np.where(np.isclose(szr + Lr / 2, Nf))[0]
        ev = np.linalg.eigvalsh(Hr[np.ix_(ix, ix)])
        hr = 0.5 * J * (np.eye(Lr, k=1) + np.eye(Lr, k=-1))
        hr[0, Lr - 1] = hr[Lr - 1, 0] = 0.5 * J * (1 if Nf % 2 else -1)          # periodic for odd N, antiperiodic for even N
        ok = ok and np.allclose(ev, np.sort([sum(cmb) for cmb in itertools.combinations(np.linalg.eigvalsh(hr), Nf)]))
        hw = hr.copy()
        hw[0, Lr - 1] = hw[Lr - 1, 0] = -hr[0, Lr - 1]                               # the other condition is wrong
        ok = ok and not np.allclose(ev, np.sort([sum(cmb) for cmb in itertools.combinations(np.linalg.eigvalsh(hw), Nf)]))
        if Nf == Lr // 2:
            E0[Lr] = round(ev[0], 6)
check('XX rings of 6 and 8 sites, the spin levels with N fermions are free fermions, periodic for odd N, antiperiodic for even N',
      ok and E0 == {6: -2.0, 8: -2.613126}, E0)

# the quiz on the XX coupling for any pair of neighbors of 8 sites, the pairing option and the right option
sxL = [(Sp[i] + Sm[i]) / 2 for i in range(L)]
syL = [(Sp[i] - Sm[i]) / 2j for i in range(L)]
check('neighbors of 8 sites, S^+_i S^+_{i+1} = c^dag_i c^dag_{i+1}',
      all(np.allclose(Sp[i] @ Sp[i + 1], d(c[i]) @ d(c[i + 1])) for i in range(L - 1)), 'ok')
check('neighbors of 8 sites, (J/2)(c^dag_i c^dag_{i+1} + h.c.) = J (S^x_i S^x_{i+1} - S^y_i S^y_{i+1})',
      all(np.allclose(0.5 * J * (d(c[i]) @ d(c[i + 1]) + c[i + 1] @ c[i]), J * (sxL[i] @ sxL[i + 1] - syL[i] @ syL[i + 1]))
          for i in range(L - 1)), 'ok')
check('neighbors of 8 sites, J (S^x S^x + S^y S^y) = (J/2)(c^dag_i c_{i+1} + h.c.)',
      all(np.allclose(J * (sxL[i] @ sxL[i + 1] + syL[i] @ syL[i + 1]), 0.5 * J * (d(c[i]) @ c[i + 1] + d(c[i + 1]) @ c[i]))
          for i in range(L - 1)), 'ok')
