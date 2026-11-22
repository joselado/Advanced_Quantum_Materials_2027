"""Session 2, the numbers that page 05 (Section 2.5) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a box is an
assert, here or in the figure script that draws it. The numbers of the figure chain_eta are asserted in
figures/session02/chain_eta.py, those of band_sign_t in band_sign_t.py, and those of the three pictures of the quiz on
the band (2.9) in _g2_etaband.py. This script holds the rest, in the order of the page. It finds the repository from
its own path and writes no file in it, since pyqula runs in a temporary folder.

Run it from anywhere:  python3 webnotes/checks/session02/g2_05_bloch_chain.py"""
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def band(p, t=1.0, eta=0.0):
    """The band (2.9), which is (2.8) for eta = 0."""
    return -2 * t * np.cos(p) - 2 * eta * np.cos(2 * p)


p = np.linspace(-np.pi, np.pi, 200001)

# the key box: for t>0 the bottom -2t at phi=0, the top 2t at phi=pi, the width 4t
for t in (1.0, 0.7):
    e = band(p, t)
    check(f'key box, t={t}: bottom -2t at 0, top 2t at pi, width 4t',
          np.isclose(e.min(), -2 * t) and np.isclose(p[np.argmin(e)], 0, atol=1e-4)
          and np.isclose(e.max(), 2 * t) and np.isclose(abs(p[np.argmax(e)]), np.pi) and np.isclose(np.ptp(e), 4 * t),
          (e.min(), e.max()))

# the text: -2t + t phi^2 close to 0 and 2t - t delta^2 close to pi
d = 1e-3
check('-2t + t phi^2 at the bottom and 2t - t delta^2 at the top', abs(band(d) - (-2 + d ** 2)) < 1e-10
      and abs(band(np.pi + d) - (2 - d ** 2)) < 1e-10, (band(d), band(np.pi + d)))

# (2.7) with the factor 1/sqrt(L), the lecturer's decision of 2026-11-22, on a ring of L sites with phi = 2 pi m/L.
# The orthogonality sum is L delta, the transform is unitary, its inverse gives back c_n^+, Psi_phi^+|0> is the state
# (2.6) divided by sqrt(L) and so normalized, the substitution display with 1/L gives sum_phi e^{i phi} Psi^+ Psi, and
# H of (2.5) becomes (2.8) with no factor. Without the 1/sqrt(L) the same steps give L times (2.8).
for L in (5, 8, 12):
    ph = 2 * np.pi * np.arange(L) / L
    E = np.exp(1j * np.outer(np.arange(L), ph))                       # E[n, phi] = e^{i n phi}
    U = E / np.sqrt(L)                                                 # column phi is Psi_phi^+ on the sites, (2.7)
    orth = E.conj().T @ E                                              # sum_n e^{i n (phi' - phi)}
    inverse = (U.conj() @ U.T)                                         # c_n^+ = (1/sqrt L) sum_phi e^{-i n phi} Psi_phi^+
    hop = np.roll(np.eye(L), 1, axis=1)                                # c_n^+ c_{n+1}, row n and column n+1
    D = U.conj().T @ hop @ U
    H = -(hop + hop.T)
    ok = np.allclose(orth, L * np.eye(L)) and np.allclose(U.conj().T @ U, np.eye(L)) and np.allclose(inverse, np.eye(L))
    ok = ok and np.allclose(np.linalg.norm(E, axis=0) / np.sqrt(L), 1) and np.allclose(np.linalg.norm(U, axis=0), 1)
    ok = ok and np.allclose(D, np.diag(np.exp(1j * ph))) and np.allclose(U.conj().T @ H @ U, np.diag(-2 * np.cos(ph)))
    ok = ok and np.allclose(E.conj().T @ H @ E, L * np.diag(-2 * np.cos(ph)))
    check(f'(2.7) with 1/sqrt(L), L={L}: the sum is L delta, the transform is unitary and inverts, Psi^+|0> is (2.6) '
          'normalized, the 1/L display gives e^(i phi), and (2.8) has no factor, while with no 1/sqrt(L) it is L times',
          ok, round(float(abs(np.linalg.det(U))), 12))

# the steps fold: on a ring of L sites the hopping to the neighbor at distance m is diagonal in the Fourier modes,
# with e^{i m phi}, so a hopping -t_m adds -2 t_m cos(m phi), with the normalized transform (2.7)
L = 12
phis = 2 * np.pi * np.arange(L) / L
F = np.exp(1j * np.outer(np.arange(L), phis)) / np.sqrt(L)          # column j is the mode e^{i n phi_j}
for m in (1, 2, 3):
    S = np.roll(np.eye(L), m, axis=1)                                  # (c_n^dagger c_{n+m}) as a matrix, row n col n+m
    D = F.conj().T @ S @ F
    check(f'fold: sum_n c_n^dagger c_(n+m) gives e^(i m phi), m={m}', np.allclose(D, np.diag(np.exp(1j * m * phis))),
          np.round(np.diag(D)[:3], 3))
tm = (1.0, 0.3, 0.2)
H = sum(-t_ * (np.roll(np.eye(L), m, axis=1) + np.roll(np.eye(L), m, axis=1).T) for m, t_ in enumerate(tm, 1))
ref = sum(-2 * t_ * np.cos(m * phis) for m, t_ in enumerate(tm, 1))
check('fold: hoppings -t_m give the band sum of -2 t_m cos(m phi), ring of 12 sites',
      np.allclose(np.sort(np.linalg.eigvalsh(H)), np.sort(ref)), np.round(np.sort(ref), 3))

# pyqula: the place m of tij is the hopping to the neighbor at distance m, so tij=[-1,-eta] gives (2.9) with t = 1
os.chdir(tempfile.mkdtemp())
from pyqula import geometry  # noqa: E402

g = geometry.chain()
ks = np.linspace(-0.5, 0.5, 101)
for tij in ([-1., -0.3], [-1., -0.3, -0.2]):
    hk = g.get_hamiltonian(has_spin=False, tij=tij).get_hk_gen()
    e = np.array([np.linalg.eigvalsh(hk([k, 0., 0.]))[0] for k in ks])
    ref = sum(2 * t_ * np.cos(m * 2 * np.pi * ks) for m, t_ in enumerate(tij, 1))
    check(f'fold: pyqula tij={tij} gives 2 sum_m tij[m] cos(m phi)', np.allclose(e, ref), round(float(e[50]), 4))
hk = g.get_hamiltonian(has_spin=False, tij=[-1., -0.5]).get_hk_gen()
e = np.array([np.linalg.eigvalsh(hk([k, 0., 0.]))[0] for k in ks])
check('fold: tij=[-1.0,-eta] is (2.9) with t=1, eta=0.5', np.allclose(e, band(2 * np.pi * ks, 1.0, 0.5)), e[0])

# the first quiz: for t<0 the band is +2|t| cos(phi), its minimum -2|t| at pi; t=-1 gives +2 at 0 and -2 at pi,
# and 0 at pi/2 for either sign
for t in (-1.0, -0.6):
    e = band(p, t)
    check(f'quiz 1, t={t}: band is 2|t| cos(phi), minimum -2|t| at pi', np.allclose(e, 2 * abs(t) * np.cos(p))
          and np.isclose(e.min(), -2 * abs(t)) and np.isclose(abs(p[np.argmin(e)]), np.pi), e.min())
check('quiz 1: t=-1 gives +2 at 0 and -2 at pi', np.isclose(band(0., -1.), 2) and np.isclose(band(np.pi, -1.), -2),
      (band(0., -1.), band(np.pi, -1.)))
check('quiz 1: energy 0 at pi/2 for both signs', abs(band(np.pi / 2, 1.)) < 1e-12 and abs(band(np.pi / 2, -1.)) < 1e-12, 0)

# the first notebook box: the cell "One dimensional chain" has tij=[1.0,0.], the hopping +1, which is t=-1 of (2.5),
# so its band is +2 cos(phi), the band of (2.8) upside down. The cell is spinful, so each level comes twice.
hn = g.get_hamiltonian(tij=[1.0, 0.]).get_hk_gen()
en = np.array([np.linalg.eigvalsh(hn([k, 0., 0.])) for k in ks])
check('notebook box: tij=[1.0,0.] gives +2 cos(phi), which is (2.8) with t=-1, each level twice',
      np.allclose(en, np.repeat(2 * np.cos(2 * np.pi * ks)[:, None], 2, axis=1))
      and np.allclose(en[:, 0], band(2 * np.pi * ks, -1.0)) and np.isclose(en[50, 0], 2) and np.isclose(en[0, 0], -2),
      (en[50, 0], en[0, 0]))

# the second quiz: the energy at pi/2 is 2 eta, and for t=1, eta=0.2 it is -0.4 cos(pi) = +0.4
for t, eta in ((1.0, 0.2), (0.8, 0.35)):
    check(f'quiz 2: energy at pi/2 is 2 eta, t={t} eta={eta}', np.isclose(band(np.pi / 2, t, eta), 2 * eta),
          band(np.pi / 2, t, eta))
check('quiz 2: -0.4 cos(pi) = +0.4 for eta=0.2', np.isclose(-0.4 * np.cos(np.pi), 0.4)
      and np.isclose(band(np.pi / 2, 1.0, 0.2), 0.4), band(np.pi / 2, 1.0, 0.2))

# the picture quiz, the feedback of the option eta=0: the band -2 cos(phi) has its maximum 2 at pi, curvature -2 there
check('picture quiz: eta=0 has its maximum 2 at phi=pi and the curvature -2 there',
      np.isclose(band(np.pi), 2) and np.isclose(band(p).max(), 2)
      and abs((band(np.pi + 1e-4) - 2 * band(np.pi) + band(np.pi - 1e-4)) / 1e-8 - (-2)) < 1e-4, band(np.pi))

# the problem: the derivative, the curvature -2t + 8 eta at pi, the threshold t/4, the two ends and the width 4t
# below it, the new maxima at cos(phi) = -t/4 eta with 2 eta + t^2/4 eta, and 1.5 t, -3 t, 4.5 t for eta = 0.5 t
t = 1.0
for eta in (0.0, 0.1, 0.2, 0.249, 0.26, 0.3, 0.5, 0.9):
    e = band(p, t, eta)
    de = np.gradient(e, p)
    ok = np.allclose(de[1:-1], (2 * np.sin(p) * (t + 4 * eta * np.cos(p)))[1:-1], atol=1e-6)   # central differences
    curv = (band(np.pi + 1e-4, t, eta) - 2 * band(np.pi, t, eta) + band(np.pi - 1e-4, t, eta)) / 1e-8
    ok = ok and abs(curv - (-2 * t + 8 * eta)) < 1e-4
    local_min_at_pi = curv > 0
    ok = ok and (local_min_at_pi == (eta > t / 4))
    if eta < t / 4:
        ok = ok and np.isclose(e.min(), -2 * t - 2 * eta) and np.isclose(e.max(), 2 * t - 2 * eta) \
            and np.isclose(np.ptp(e), 4 * t)
    else:
        c = -t / (4 * eta)
        ok = ok and np.isclose(e.max(), 2 * eta + t ** 2 / (4 * eta), atol=1e-8) \
            and np.isclose(np.cos(p[np.argmax(e)]), c, atol=1e-4) and np.isclose(e.min(), -2 * t - 2 * eta)
    check(f'problem, eta={eta}: derivative, curvature -2t+8eta, minimum at pi only above t/4, extrema and width',
          ok, (round(curv, 4), round(float(np.ptp(e)), 4)))
e = band(p, 1.0, 0.5)
check('problem, eta=0.5t: cos(phi)=-1/2 at the maxima, 1.5t, bottom -3t, width 4.5t',
      np.isclose(np.cos(p[np.argmax(e)]), -0.5, atol=1e-4) and np.isclose(e.max(), 1.5) and np.isclose(e.min(), -3)
      and np.isclose(np.ptp(e), 4.5), (e.max(), e.min(), np.ptp(e)))
# the try-it, corrected on 2026-11-22 from tij=[1.0,0.3,0.0] to tij=[1.0,0.2,0.0]: with the sign of the notebook,
# pyqula with tij=[1.0,0.2,0.0] has only the two extrema 0 and pi, while tij=[1.0,0.5,0.0] has two more, so the band
# gets an extra extremum, and its energies give one more van Hove peak inside the band, at -1 between -1.5 and 3.
# 0.3 is above t/4 and already has the extra extremum, 0.033 deep, which is why it was replaced. The page no longer
# quotes 0.3, so it has no assert here, and the fact stays in conventions.py.
def notebook_extrema(eta, n=4001):
    hk_ = g.get_hamiltonian(has_spin=False, tij=[1.0, eta, 0.0]).get_hk_gen()
    kk = np.linspace(-0.5, 0.5, n)
    e_ = np.array([np.linalg.eigvalsh(hk_([k, 0., 0.]))[0] for k in kk])
    ok_ = np.allclose(e_, -band(2 * np.pi * kk, 1.0, eta))                  # (2.9) turned upside down
    de_ = np.diff(e_)
    idx = np.where(np.sign(de_[1:]) != np.sign(de_[:-1]))[0] + 1          # interior turning points on (-pi, pi)
    energies = sorted(set(np.round(np.r_[e_[idx], e_[0]], 3)))             # with the end point phi = -pi
    return ok_, len(idx), energies
ok2, n2, en2 = notebook_extrema(0.2)
ok5, n5, en5 = notebook_extrema(0.5)
check('try-it: tij=[1.0,0.2,0.0] gives (2.9) upside down with the extrema at 0 and pi only, the energies 2.4 and -1.6',
      ok2 and n2 == 1 and np.allclose(en2, [-1.6, 2.4]), (n2, en2))
check('try-it: tij=[1.0,0.5,0.0] gets the extra extremum at pi, and the extrema -1.5, -1 and 3 give one more van Hove '
      'energy inside the band', ok5 and n5 == 3 and np.allclose(en5, [-1.5, -1.0, 3.0]), (n5, en5))

# the second notebook box, decided on 2026-11-22: the cell "One dimensional chain, with longer range hopping" changes
# the third-neighbor hopping t3, in the third place of tij, as tij=[1.0,0.,t3], and pyqula puts the place m of tij on
# the neighbor at the distance m, so the third place adds 2 t3 cos(3 phi)
import json  # noqa: E402
import re  # noqa: E402
nb = json.load(open(os.path.join(HERE, '..', '..', '..', 'jupyter-notebooks', 'session2.ipynb'), encoding='utf-8'))
head, calls = None, []
for c in nb['cells']:
    s = ''.join(c['source'])
    if c['cell_type'] == 'markdown' and s.lstrip().startswith('#'):
        head = s.strip().split('\n')[0].lstrip('#').split('(')[0].strip()
    elif c['cell_type'] == 'code' and head == 'One dimensional chain, with longer range hopping':
        calls += [m.replace(' ', '') for m in re.findall(r'get_hamiltonian\(([^)]*)\)', s)]
t3_ok = calls and all(a == 'tij=[1.0,0.,t3]' for a in calls)
for t3 in (0.0, 1 / 3, 2 / 3):
    hk3 = g.get_hamiltonian(has_spin=False, tij=[1.0, 0., t3]).get_hk_gen()
    e3 = np.array([np.linalg.eigvalsh(hk3([k, 0., 0.]))[0] for k in ks])
    t3_ok = t3_ok and np.allclose(e3, 2 * np.cos(2 * np.pi * ks) + 2 * t3 * np.cos(3 * 2 * np.pi * ks))
check('notebook box 2: the cell calls get_hamiltonian(tij=[1.0,0.,t3]), and the third place of tij is the third-neighbor '
      'hopping, 2 cos(phi) + 2 t3 cos(3 phi) for t3 = 0, 1/3, 2/3', bool(t3_ok), calls)

# the condition eta >= 0 is needed: for a negative eta the extra extremum is at phi = 0, not at pi
e = band(p, 1.0, -0.5)
check('problem: for eta=-0.5 the extra extremum sits at phi=0, so the problem states eta >= 0',
      (band(1e-4, 1, -0.5) - 2 * band(0, 1, -0.5) + band(-1e-4, 1, -0.5)) / 1e-8 < 0, round(float(e[100000]), 3))
