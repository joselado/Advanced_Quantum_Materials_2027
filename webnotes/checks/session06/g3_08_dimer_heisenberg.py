"""Session 6, the numbers that page 08 (Section 6.8) quotes, checked in the order of the page.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or
in the figure script that draws it. The Hubbard dimer is built with Jordan-Wigner fermions on four modes and
diagonalized in the sector of two electrons, the same construction as figures/session06/_g3_dimerquiz.py, which draws the
level diagrams of the picture quiz. The fold is checked state by state with the order of the operators that it writes,
which is the order of webnotes/conventions/session06.md. The lab box is checked against the stored source. It finds the
repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session06/g3_08_dimer_heisenberg.py"""
import os, sys
sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
assert os.path.exists(os.path.join(REPO, 'webnotes', 'pages', 'session06'))

import numpy as np
from functools import reduce
from math import comb


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


I2, Z, a = np.eye(2), np.diag([1., -1.]), np.array([[0., 1.], [0., 0.]])
c = [reduce(np.kron, [Z] * m + [a] + [I2] * (3 - m)) for m in range(4)]      # modes (0,up), (0,dn), (1,up), (1,dn)
cd = [x.T for x in c]
n = [x @ y for x, y in zip(cd, c)]
vac = np.zeros(16); vac[0] = 1.0
assert np.allclose(sum(n) @ vac, 0)


def hopping(t=1.0):
    return sum(-t * (cd[s] @ c[2 + s] + cd[2 + s] @ c[s]) for s in (0, 1))


def hubbard(U, t=1.0):
    return hopping(t) + U * (n[0] @ n[1] + n[2] @ n[3])


keep = np.where(abs(np.diag(sum(n)) - 2) < 1e-9)[0]


def levels(U, t=1.0):
    return np.linalg.eigvalsh(hubbard(U, t)[np.ix_(keep, keep)])


def ES(U, t=1.0):
    return U / 2 - np.sqrt(U ** 2 / 4 + 4 * t ** 2)


# the opening paragraph: six states at half filling
check('text, the Fock space of two sites at half filling has 6 states', comb(4, 2) == 6 and len(keep) == 6, len(keep))

# the text and the key box: the six levels, the singlet E_S, the triplet at 0 and the two levels with double occupation
for U in (4.0, 8.0, 10.0, 16.0):
    e = levels(U)
    ok = (abs(e[0] - ES(U)) < 1e-12 and np.allclose(e[1:4], 0, atol=1e-12) and abs(e[4] - U) < 1e-12
          and abs(e[5] - (U / 2 + np.sqrt(U ** 2 / 4 + 4))) < 1e-12)
    check(f'text, U={U:g}: the levels are E_S, three at 0, U and U/2 + sqrt(U^2/4 + 4t^2)', ok, np.round(e, 4))
for tt in (1.0, -1.0):
    check(f'text, t={tt:g}: the lowest level is the same for either sign of t', abs(levels(8.0, tt)[0] - ES(8.0)) < 1e-12, True)

# the Heisenberg dimer: -3J/4 for the singlet and +J/4 for the triplet, so E_T - E_S = J
sx = np.array([[0, 1], [1, 0]]) / 2; sy = np.array([[0, -1j], [1j, 0]]) / 2; sz = np.diag([1., -1.]) / 2
SS = sum(np.kron(s, s) for s in (sx, sy, sz)).real
eh = np.linalg.eigvalsh(SS)
check('text, S0.S1 has -3/4 once and +1/4 three times', np.allclose(eh, [-0.75, 0.25, 0.25, 0.25]), eh)

# the expansion E_S = -4t^2/U + O(t^4/U^3): the next term is +16 t^4/U^3
for U in (50.0, 200.0):
    r = (ES(U) + 4 / U) * U ** 3
    check(f'text, U={U:g}: (E_S + 4t^2/U) U^3/t^4 is close to 16', abs(r - 16) < 0.2, round(r, 4))

# the key box: the exact splitting is 0.83 of 4t^2/U at U=4t and 0.98 of it at U=16t (and 0.94 at 8t, the problem)
ratio = {U: (0 - ES(U)) / (4 / U) for U in (4.0, 8.0, 16.0)}
check('key box and problem, the ratio (E_T - E_S)/(4t^2/U) is 0.83, 0.94 and 0.98 at U/t = 4, 8, 16',
      [round(ratio[U], 2) for U in (4.0, 8.0, 16.0)] == [0.83, 0.94, 0.98], {k: round(v, 4) for k, v in ratio.items()})

# the fold: the basis with the operator of site 0 first, and the action of the hopping
up_dn = cd[0] @ cd[3] @ vac                    # c+_{0 up} c+_{1 dn} |0>
dn_up = cd[1] @ cd[2] @ vac                    # c+_{0 dn} c+_{1 up} |0>
dd0 = cd[0] @ cd[1] @ vac                      # c+_{0 up} c+_{0 dn} |0>
d0d = cd[2] @ cd[3] @ vac                      # c+_{1 up} c+_{1 dn} |0>
upup = cd[0] @ cd[2] @ vac
dndn = cd[1] @ cd[3] @ vac
Ht = hopping(1.0)
check('fold, H_t on up,up and on dn,dn gives zero', np.allclose(Ht @ upup, 0) and np.allclose(Ht @ dndn, 0), True)
check('fold, H_t |up,dn> = -t (|updn,0> + |0,updn>)', np.allclose(Ht @ up_dn, -(dd0 + d0d)), True)
check('fold, H_t |dn,up> = +t (|updn,0> + |0,updn>)', np.allclose(Ht @ dn_up, +(dd0 + d0d)), True)
T0 = (up_dn + dn_up) / np.sqrt(2)
S = (up_dn - dn_up) / np.sqrt(2)
D = (dd0 + d0d) / np.sqrt(2)
Dm = (dd0 - d0d) / np.sqrt(2)
check('fold, H_t |T0> = 0', np.allclose(Ht @ T0, 0), True)
check('fold, H_t |S> = -2t |D>, so <D|H_t|S> = -2t', np.allclose(Ht @ S, -2 * D) and abs(D @ Ht @ S + 2) < 1e-12, D @ Ht @ S)
H10 = hubbard(10.0)
check('fold, the antisymmetric doubly occupied state is an eigenstate at U', np.allclose(H10 @ Dm, 10.0 * Dm), True)
check('fold, the 2x2 matrix in {S, D} is [[0, -2t], [-2t, U]]',
      np.allclose([[S @ H10 @ S, S @ H10 @ D], [D @ H10 @ S, D @ H10 @ D]], [[0, -2], [-2, 10]]), True)
check('fold, the triplet states up,up and T0 are eigenstates at 0 of the full Hamiltonian',
      np.allclose(H10 @ upup, 0) and np.allclose(H10 @ T0, 0), True)
# another order of the operators only changes signs of basis states, so the sign of -2t can change and the levels do not
dn_up2 = cd[2] @ cd[1] @ vac                   # c+_{1 up} c+_{0 dn} |0> = -|dn,up>
check('fold, reordering only |dn,up> turns the written minus combination into T0, with the element 0',
      np.allclose(dn_up2, -dn_up) and np.allclose((up_dn - dn_up2) / np.sqrt(2), T0)
      and abs(D @ Ht @ ((up_dn - dn_up2) / np.sqrt(2))) < 1e-12, True)
up_dn3 = cd[3] @ cd[0] @ vac                   # c+_{1 dn} c+_{0 up} |0> = -|up,dn>, both antiparallel states with site 1 first
S3 = (up_dn3 - dn_up2) / np.sqrt(2)
dd0r, d0dr = cd[1] @ cd[0] @ vac, cd[3] @ cd[2] @ vac   # the doubly occupied states with the spin down operator first
D4 = (dd0r + d0dr) / np.sqrt(2)
el3, el4 = D @ Ht @ S3, D4 @ Ht @ S
check('fold, with both antiparallel states in the order of site 1 first the element is +2t, and with the doubly occupied '
      'states written spin down first it is +2t too', abs(el3 - 2) < 1e-12 and abs(el4 - 2) < 1e-12, (el3, el4))
lev = np.linalg.eigvalsh([[0, -2], [-2, 10]])
check('fold, the 2x2 matrices with -2t and with +2t have the same eigenvalues, at U=10t',
      np.allclose(lev, np.linalg.eigvalsh([[S3 @ H10 @ S3, S3 @ H10 @ D], [D @ H10 @ S3, D @ H10 @ D]]))
      and np.allclose(lev, np.linalg.eigvalsh([[S @ H10 @ S, S @ H10 @ D4], [D4 @ H10 @ S, D4 @ H10 @ D4]])), np.round(lev, 4))

# the text: the mean-field energy difference per bond is one half of J, the classical Neel state of S = 1/2
J, Sc = 1.0, 0.5
check('text, per bond E_FM - E_Neel = J S^2 - (-J S^2) = J/2 for S = 1/2', abs((J * Sc ** 2 + J * Sc ** 2) - J / 2) < 1e-12, J / 2)

# the first quiz: U = 10, t = 1 gives J = 0.4, t = 2 gives 1.6, four times larger
check('quiz 1, J = 0.4 for t=1 and 1.6 for t=2 at U=10', abs(4 * 1 / 10 - 0.4) < 1e-12 and abs(4 * 4 / 10 - 1.6) < 1e-12, (0.4, 1.6))
check('quiz 1, a doubled J would be 0.8, which is not the 1.6 of t=2, four times 0.4',
      abs(2 * (4 * 1 / 10) - 0.8) < 1e-12 and abs(4 * 4 / 10 - 0.8) > 0.1 and abs(4 * 4 / 10 - 4 * 0.4) < 1e-12, 2 * 0.4)

# the second quiz: E_S at U=10t, the eigenvalues +-2t at U=0, the wrong formula with t, and -4t^2/U at U=4t
check('quiz 2, E_S = -0.385t at U=10t', round(ES(10.0), 3) == -0.385, round(ES(10.0), 5))
check('quiz 2, at U=0 the matrix has the eigenvalues -2t and 2t', np.allclose(np.linalg.eigvalsh([[0, -2], [-2, 0]]), [-2, 2]), True)
check('quiz 2, the formula with t instead of 2t gives -t at U=0', abs(0 - np.sqrt(0 + 1) + 1) < 1e-12, -1.0)
check('quiz 2, at U=4t the lower eigenvalue is 2t - sqrt8 t = -0.828t, while -4t^2/U = -t',
      abs(ES(4.0) - (2 - np.sqrt(8))) < 1e-12 and round(ES(4.0), 3) == -0.828 and abs(-4 / 4.0 + 1) < 1e-12, round(ES(4.0), 4))

# the picture quiz: E_S = 5t - sqrt29 t = -0.385t, close to -4t^2/U = -0.4t, and the triplet at 0
check('quiz 3, E_S = 5 - sqrt29 = -0.385 at U=10t and -4t^2/U = -0.4',
      abs(ES(10.0) - (5 - np.sqrt(29))) < 1e-12 and abs(-4 / 10 + 0.4) < 1e-12, round(5 - np.sqrt(29), 4))
sys.path.insert(0, os.path.join(REPO, 'webnotes', 'figures', 'session06'))
import _g3_dimerquiz
_g3_dimerquiz.check()
check('quiz 3, the helper of the pictures agrees (singlet at -0.385 with S=0, triplet at 0 with S=1)', True, round(_g3_dimerquiz.ES, 4))

# the problem: the expansion to the next order, at U = 8t
U = 8.0
first, second = 4 / U, -16 / U ** 3
check('problem, at U=8t the terms are 0.5t and -0.031t, and the expansion gives 0.469t',
      first == 0.5 and round(second, 3) == -0.031 and round(first + second, 3) == 0.469, first + second)
exact = -ES(U)
check('problem, the exact splitting is sqrt20 t - 4t = 0.472t, which is 0.944 of 4t^2/U',
      abs(exact - (np.sqrt(20) - 4)) < 1e-12 and round(exact, 3) == 0.472 and round(exact / first, 3) == 0.944, round(exact, 5))
x = 16 / U ** 2
check('problem, U/2 (x/2 - x^2/8) = 4t^2/U - 16t^4/U^3', abs(U / 2 * (x / 2 - x ** 2 / 8) - (first + second)) < 1e-12, True)
check('problem, the expansion is closer to the exact value than 4t^2/U', abs(first + second - exact) < abs(first - exact), True)

# the lab box: the stored source. The tracked file holds the quotation of the 23 meV, the full copy the whole abstract
src = os.path.join(REPO, 'webnotes', 'sources', 'session06', 'mishra2020_s41565-019-0577-9.txt')
tracked = ' '.join(open(src, encoding='utf-8').read().split())
check('lab box, the tracked file quotes the exchange-coupling strength of 23 meV',
      'antiferromagnetic order with an exchange-coupling strength of 23 meV' in tracked, 'found')
full = os.path.join(REPO, 'webnotes', 'sources', '.full', 'session06', 'mishra2020_s41565-019-0577-9.txt')
if os.path.exists(full):
    txt = ' '.join(open(full, encoding='utf-8').read().split())
    check('lab box, the abstract says STM and spin excitation spectroscopy of individual molecules on a gold surface',
          'Scanning tunnelling microscopy and spin excitation spectroscopy of individual molecules on a gold surface reveal a '
          'robust antiferromagnetic order with an exchange-coupling strength of 23 meV' in txt, 'found')
    check('lab box, the abstract names C38H18, Clar\'s goblet, the Kekulé structure and unpaired electrons',
          'C38H18' in txt and "Clar's goblet" in txt and 'classical Kekulé structure without leaving unpaired electrons' in txt
          and 'π-electron network' in txt, 'found')
else:
    print('SKIPPED lab box, the full copy of the source is not on this machine (it is ignored by git)')

# corrected on 2026-11-22, the notebook box and the try-it box, rewritten to match the cells. "(Reminder) The spectra of a
# dimer" gives the single-particle levels +-t, each twice with the spin. "The interacting Hubbard dimer" is a mean-field
# loop, with mf="antiferro" and mix=0.9 for Us = np.linspace(0.,10.,50): the moment n_up - n_dn of a site is zero up to
# U = 2t and sqrt(1 - 4t^2/U^2) above, 0.87 at 4t and 0.98 at 10t, and the gap is 2t below and U above, by pyqula and
# by the closed form. The exact dimer has no moment, since its ground state is the singlet, asserted here with S^2 = 0
# and <n_up - n_dn> = 0 on each site at U = 2.5t, 4t and 10t. "Gap opening in the Hubbard model" is the mean-field chain over U, and "The strongly
# interacting limit" compares E_FE - E_AF at large U, whose 1/U law g2_04 asserts.
import json, tempfile
spin_op = lambda i: [0.5 * (cd[2 * i] @ c[2 * i + 1] + cd[2 * i + 1] @ c[2 * i]),
                     0.5 * (-1j * cd[2 * i] @ c[2 * i + 1] + 1j * cd[2 * i + 1] @ c[2 * i]), 0.5 * (n[2 * i] - n[2 * i + 1])]
Stot = [a_ + b_ for a_, b_ in zip(spin_op(0), spin_op(1))]
S2 = sum(x @ x for x in Stot)
gsm = []
for U in (2.5, 4.0, 10.0):
    w_, v_ = np.linalg.eigh(hubbard(U)[np.ix_(keep, keep)])
    g_ = np.zeros(16, complex); g_[keep] = v_[:, 0]
    gsm.append((abs(g_.conj() @ S2 @ g_), abs(g_.conj() @ (n[0] - n[1]) @ g_), abs(g_.conj() @ (n[2] - n[3]) @ g_)))
check('try-it, the exact dimer has the singlet as ground state, S^2 = 0, and no ordered moment on either site, at 2.5t, 4t '
      'and 10t', np.allclose(gsm, 0, atol=1e-12), np.round(gsm, 12))
# corrected after the independent check of 2026-11-22 (k6): <n_up - n_dn> = 0 on each site is no ordered moment, while the
# local moment <(n_up - n_dn)^2> of a site is the weight of the singly occupied states in the singlet. Two routes: the
# ground state of the six states, and the closed form 1/(1 + E_S^2/4t^2) from the 2x2 block [[0, -2t], [-2t, U]] of the
# covalent and the ionic singlet. It is 0.765, 0.854 and 0.964 at 2.5t, 4t and 10t.
loc = []
for U in (2.5, 4.0, 10.0):
    w_, v_ = np.linalg.eigh(hubbard(U)[np.ix_(keep, keep)])
    g_ = np.zeros(16, complex); g_[keep] = v_[:, 0]
    ES = U / 2 - np.sqrt(U * U / 4 + 4)
    loc.append((np.real(g_.conj() @ (n[0] - n[1]) @ (n[0] - n[1]) @ g_), np.real(g_.conj() @ (n[2] - n[3]) @ (n[2] - n[3]) @ g_),
                1 / (1 + ES * ES / 4)))
check('try-it, the local moment <(n_up - n_dn)^2> of the exact dimer is 0.85 at 4t on each site, by the six states and by '
      'the closed form, and 0.765 and 0.964 at 2.5t and 10t', all(abs(a - c) < 1e-12 and abs(b - c) < 1e-12 for a, b, c in loc)
      and round(loc[1][0], 2) == 0.85 and round(loc[0][0], 3) == 0.765 and round(loc[2][0], 3) == 0.964,
      np.round(loc, 4).tolist())
nb = json.load(open(os.path.join(REPO, 'jupyter-notebooks', 'session6.ipynb')))['cells']


def cell_code(title):
    i = [j for j, c in enumerate(nb) if c['cell_type'] == 'markdown' and ''.join(c['source']).startswith('## ' + title)]
    return len(i), next(''.join(c['source']) for c in nb[i[0] + 1:] if c['cell_type'] == 'code')


cells = {t: cell_code(t) for t in ('The spectra of a dimer', 'The interacting Hubbard dimer', 'Gap opening in the Hubbard model',
                                    'The strongly interacting limit')}
check('notebook box, the four cells exist, the dimer cell is a mean-field loop over Us = np.linspace(0.,10.,50), the gap '
      'cell runs the chain over U, the last one compares E_FE and E_AF',
      all(n == 1 for n, c in cells.values()) and 'get_mean_field_hamiltonian(U=U,mf="antiferro",mix=0.9)' in cells['The interacting Hubbard dimer'][1]
      and 'np.linspace(0.,10.,50)' in cells['The interacting Hubbard dimer'][1] and 'g.dimensionality = 0' in cells['The interacting Hubbard dimer'][1]
      and 'get_mean_field_hamiltonian' in cells['Gap opening in the Hubbard model'][1]
      and 'return_total_energy=True,mf="ferro"' in cells['The strongly interacting limit'][1]
      and 'return_total_energy=True,mf="antiferro"' in cells['The strongly interacting limit'][1], 'ok')
os.chdir(tempfile.mkdtemp())
from pyqula import geometry
g = geometry.bichain(); g.dimensionality = 0
(ks, es) = g.get_hamiltonian(has_spin=True).get_bands()
check('notebook box, the cell of the spectra of a dimer gives the single-particle levels -t and +t, each twice',
      np.allclose(sorted(np.real(es)), [-1, -1, 1, 1]), np.round(sorted(np.real(es)), 6))
# corrected after the independent check of 2026-11-22 (k6): the first cell has no interaction, and the other three call
# the mean-field loop
check('notebook box, the first cell has no interaction and the other three use mean field',
      'get_mean_field_hamiltonian' not in cells['The spectra of a dimer'][1] and 'U' not in cells['The spectra of a dimer'][1]
      and all('get_mean_field_hamiltonian' in cells[t][1] for t in ('The interacting Hubbard dimer',
                                                                      'Gap opening in the Hubbard model', 'The strongly interacting limit')),
      'ok')
g = geometry.bichain(); g = g.get_supercell(1); g.dimensionality = 0
h0 = g.get_hamiltonian()
mf = {}
for U in (1.8, 1.9, 2.5, 4.0, 10.0):
    hU = h0.get_mean_field_hamiltonian(U=U, mf="antiferro", mix=0.9)
    mf[U] = (abs(float(np.real(hU.get_vev("mz")[1]))), hU.get_gap())
closed = lambda U: np.sqrt(max(0.0, 1 - 4 / U ** 2))
check('try-it, the mean-field dimer has no moment below 2t and sqrt(1 - 4t^2/U^2) above, 0.87 at 4t and 0.98 at 10t, '
      'and the gap is 2t below and U above',
      mf[1.8][0] < 1e-3 and mf[1.9][0] < 1e-3 and all(abs(mf[U][0] - closed(U)) < 1e-3 for U in (2.5, 4.0, 10.0))
      and round(mf[4.0][0], 2) == 0.87 and round(mf[10.0][0], 2) == 0.98 and abs(mf[1.8][1] - 2) < 1e-6
      and all(abs(mf[U][1] - U) < 1e-3 for U in (2.5, 4.0, 10.0)), {U: (round(m, 5), round(e, 5)) for U, (m, e) in mf.items()})
