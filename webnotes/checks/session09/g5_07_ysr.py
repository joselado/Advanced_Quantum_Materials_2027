"""Session 9, the numbers that page 07 (Section 9.7, magnetic impurities in a superconductor) states and that no figure
script asserts.

The caption of the figure g5_ysr_dos (the normal-state DOS, the peaks within 0.01 Delta of (9.10), the meeting at J S = 2t on
the grid of the script) is asserted in webnotes/figures/session09/g5_ysr_dos.py on the output of the pyqula script. This
script checks the opener and the key box, the lattice crossing behind "J S = 2t", the explanation of the third quiz, the
feedbacks of the three quizzes and the problem, with numpy: the local Green's function of the clean half-filled chain, the
T-matrix condition det(1 - J g(E)) = 0 of a classical spin on one site, and the block (c_up, c_dn^dag) of the BdG matrix
(5.6) of a ring, as on the conventions sheet. The lab box quotes 12 nm from its stored source, which labsource.py --check 9
shows. Since 2026-11-22 the page no longer calls (9.10) the Born approximation, and the check of the text asserts that the
lattice follows (9.10) where its first order leaves the gap.

Run it from anywhere:  python3 webnotes/checks/session09/g5_07_ysr.py"""
import sys
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def eb(a, D=1.0):
    """(9.10)."""
    return D * (1 - a * a) / (1 + a * a)


NK = 40000
K = 2 * np.pi * (np.arange(NK) + 0.5) / NK
EPS = 2 * np.cos(K)                                   # the half-filled chain of pyqula, hopping 1


def tdet(E, J, D):
    """det(1 - J g(E)) in the block (c_up, c_dn^dag) for an exchange J sigma_z on one site, s-wave Delta=D."""
    den = E ** 2 - EPS ** 2 - D ** 2
    g0, gz, gx = np.mean(E / den), np.mean(EPS / den), np.mean(D / den)
    return np.linalg.det(np.eye(2) - J * np.array([[g0 + gz, gx], [gx, g0 - gz]]))


def level(J, D):
    """The in-gap level E > -Delta of the lowest branch, from det(1 - J g) = 0, with its sign."""
    Es = np.linspace(-0.9999 * D, 0.9999 * D, 801)
    v = np.array([tdet(E, J, D) for E in Es])
    roots = [brentq(tdet, Es[i], Es[i + 1], args=(J, D)) for i in range(len(Es) - 1) if v[i] * v[i + 1] < 0]
    return roots


# ---- the opener and the key box: the state starts at the gap edge and crosses zero at alpha = 1
check('key: E_b = Delta at alpha = 0 and 0 at alpha = 1', abs(eb(0) - 1) < 1e-15 and abs(eb(1)) < 1e-15, (eb(0), eb(1)))
a = np.linspace(0, 10, 100001)
check('key: E_b decreases monotonically through the gap', np.all(np.diff(eb(a)) < 0) and np.all(np.abs(eb(a)) <= 1),
      round(eb(a).min(), 4))

# ---- the figure: nu_0 at half filling, alpha = J S/2t, and the crossing of the lattice level
nu0 = 1 / (np.pi * 2)                                 # D(E_F) per spin of the half-filled chain, 1/(2 pi t)
k = 2 * np.pi * (np.arange(200000) + 0.5) / 200000
T = 0.002
f = 0.5 * (1 - np.tanh(-2 * np.cos(k) / (2 * T)))
dos = float(np.mean(f * (1 - f) / T))
check('figure: nu_0 = 1/(2 pi t) per spin at half filling, so alpha = pi nu_0 J S = J S/2t', abs(dos - nu0) < 1e-4,
      round(dos, 5))
D = 0.2
gx0 = np.mean(-D / (EPS ** 2 + D ** 2))
Jc = 1 / abs(gx0)
check('figure: the lattice level crosses zero at J S = sqrt(4 + Delta^2) = 2.01t for Delta = 0.2t, which is 2t to 0.5 percent',
      abs(Jc - np.sqrt(4 + D ** 2)) < 1e-4 and abs(round(Jc, 2) - 2.01) < 1e-12 and abs(Jc / 2 - 1) < 0.006
      and abs(tdet(0.0, Jc, D)) < 1e-9, round(Jc, 4))
# the key box: nu_0 per spin. Counted for the two spins it would be 1/(pi t), alpha = J S/t and the crossing at J S = t, but
# the lattice level at J S = t is at 0.6 Delta, the alpha = 0.5 of nu_0 per spin, and it reaches zero only at 2.01t
r1 = level(1.0, D)
check('key: with nu_0 per spin alpha = J S/2t, since the lattice level at J S = t is at |E| = 0.6 Delta and not at zero',
      min(abs(abs(x) / D - 0.6) for x in r1) < 0.005 and min(abs(x) for x in r1) / D > 0.5, [round(x / D, 4) for x in r1])
# the caption: the notebook cell has add_onsite(1.8) and the broadening delta/10, larger than the Delta/40 of the figure
import json, os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
cells = json.load(open(os.path.join(ROOT, 'jupyter-notebooks', 'session9.ipynb')))['cells']
head = [i for i, c in enumerate(cells) if c['cell_type'] == 'markdown'
        and ''.join(c['source']).startswith('## Single magnetic impurity in a superconductor')]
src = ''.join(cells[head[0] + 1]['source'])
check('caption: the notebook cell has h.add_onsite(1.8) and the broadening delta/10, four times the Delta/40 of the figure',
      len(head) == 1 and 'h.add_onsite(1.8)' in src and 'delta=delta/10' in src and 'delta= 0.2' in src, head)
# Figure 9.3, a converted figure: its caption says "drawn for alpha = 0.6", the ALPHA of its Blender script
blend = open(os.path.join(ROOT, 'lecture_notes', 'src', 'figures', 'blender', 's09f03_ysr.py')).read()
m = re.search(r'^ALPHA = (\S+)$', blend, re.M)
check('Figure 9.3: the red peaks are drawn for alpha = 0.6, as its caption says', m is not None and float(m.group(1)) == 0.6,
      m.group(0) if m else None)

# ---- the third quiz, its explanation: on the half-filled chain with Delta = 0.2t the bound state is within 0.01 Delta of (9.10)
rows = []
for J in np.r_[0.05, 0.1, 0.2, 0.3, 0.4, np.arange(0.5, 4.01, 0.5)]:
    r = level(J, D)
    rows.append((J, min(abs(abs(x) - abs(eb(J / 2, D))) for x in r) / D))
worst = max(e for J, e in rows)
check('quiz 3: |E_b| of the lattice within 0.01 Delta of (9.10) for J S = 0.05 to 4, alpha = J S/2', worst < 0.01,
      [(J, round(e, 4)) for J, e in rows])

# ---- the first quiz
# the text before the key box: (9.10) is the classical spin to all orders in J, not its first order (the Born approximation).
# At J S = 3t, alpha = 1.5, the lattice level is within 0.01 Delta of (9.10), -0.385 Delta, while the expansion
# 1 - 2 alpha^2 of (9.10) to its lowest order in J gives -3.5 Delta, outside the gap
r3 = [J_e for J_e in rows if abs(J_e[0] - 3.0) < 1e-9][0]
check('text: at J S = 3t the lattice level is within 0.01 Delta of (9.10), -0.385 Delta, while 1 - 2 alpha^2 = -3.5 is outside the gap',
      r3[1] < 0.01 and abs(eb(1.5) + 0.3846) < 1e-3 and abs(1 - 2 * 1.5 ** 2 + 3.5) < 1e-12, (r3, round(eb(1.5), 4)))
check('quiz 1: alpha = 0.5 gives 1 - alpha^2 = 0.75 and E_b = 0.75/1.25 = 0.6 Delta',
      abs((1 - 0.25) - 0.75) < 1e-15 and abs(eb(0.5) - 0.6) < 1e-15, eb(0.5))
check('quiz 1: at alpha = 2 the wrong form 1 - alpha^2 gives -3 Delta, outside the gap, and (9.10) gives -0.6 Delta',
      abs((1 - 4) + 3) < 1e-15 and abs(eb(2) + 0.6) < 1e-15, eb(2))

# ---- the second quiz: alpha = 1.2, the ground state across the crossing, and the gap that stays
check('quiz 2: alpha = 1.2 gives -0.44/2.44 = -0.18 Delta', abs(eb(1.2) + 0.44 / 2.44) < 1e-15 and abs(round(eb(1.2), 2) + 0.18) < 1e-12,
      round(eb(1.2), 4))


def bdg_block(N, D, J=0.0, V=0.0):
    """The block (c_up, c_dn^dag) of (5.6) for a half-filled ring of N sites, hopping -1, s-wave D, an exchange J sigma_z
    and a potential V on site 0, as on the conventions sheet."""
    h = np.zeros((N, N))
    i = np.arange(N)
    h[i, (i + 1) % N] = h[(i + 1) % N, i] = -1.0
    P = np.zeros((N, N)); P[0, 0] = 1.0
    return np.block([[h + (J + V) * P, D * np.eye(N)], [D * np.eye(N), -h + (J - V) * P]])


sz = [(np.sum(np.linalg.eigvalsh(bdg_block(400, 0.1, J=J)) < 0) - 400) / 2 for J in (1.0, 3.0)]
check('quiz 2: across the crossing at J S = 2t the electronic S^z_tot goes from 0 to 1/2 in size (ring of 400, Delta = 0.1t)',
      sz[0] == 0 and abs(sz[1]) == 0.5, sz)
low = [np.min(np.abs(np.linalg.eigvalsh(bdg_block(400, 0.1, V=V)))) / 0.1 for V in (2.0, 10.0)]
check('text and quiz 2: a non-magnetic potential of 2t or 10t keeps the lowest level at Delta, the gap stays',
      all(abs(x - 1) < 1e-6 for x in low), [round(x, 8) for x in low])

# ---- the new quiz with formulas as options
alpha = np.linspace(0, 20, 200001)
away = np.abs(alpha - np.sqrt(2)) > 1e-4
check('quiz 3: 1 - alpha^2 leaves the gap exactly for alpha > sqrt 2',
      np.all((np.abs(1 - alpha[away] ** 2) > 1) == (alpha[away] > np.sqrt(2))), round(np.sqrt(2), 4))
check('quiz 3: 1/(1 + alpha^2) is positive for every alpha and 0.5 at alpha = 1, inside the gap',
      np.all(1 / (1 + alpha ** 2) > 0) and np.all(1 / (1 + alpha ** 2) <= 1) and abs(1 / 2 - 0.5) < 1e-15, 0.5)
check('quiz 3: |1 - alpha^2| <= 1 + alpha^2 for every alpha, so (9.10) never leaves the gap',
      np.all(np.abs(1 - alpha ** 2) <= 1 + alpha ** 2), True)

# ---- the problem
a0 = 1 / np.sqrt(3)
check('problem: E_b = Delta/2 at alpha = 1/sqrt 3 = 0.58, and alpha = sqrt 3 gives -Delta/2',
      abs(eb(a0) - 0.5) < 1e-15 and abs(round(a0, 2) - 0.58) < 1e-12 and abs(eb(np.sqrt(3)) + 0.5) < 1e-15, round(a0, 4))
rng = np.random.default_rng(3)
aa = rng.uniform(0.01, 50, 1000)
check('problem: E_b(1/alpha) = -E_b(alpha) for 1000 random alpha', np.allclose(eb(1 / aa), -eb(aa), atol=1e-14), True)
print('all checks of page 07 hold')
