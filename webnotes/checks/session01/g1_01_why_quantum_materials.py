"""Session 1, the numbers that page 01 (Section 1.1) quotes, in the caption of gap_two_origins and in its quiz.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The figure script gap_two_origins.py asserts the pyqula bands of
webnotes/scripts/session01/g1_two_gaps.py. This script checks the same statements by a second route, the 2x2 Bloch
Hamiltonian of the chain with two sites per cell and the 2x2 Bogoliubov-de Gennes Hamiltonian of the chain written by
hand in numpy, and then the pyqula script once more. Since 2026-11-22 it also checks the sentence of the caption that
Delta is an energy, the pair amplitude of (1.9) times the attraction, and that the paragraph on the goals of the
United Nations has no number. It writes no file, since pyqula runs in a temporary folder."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
import style


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


t, m, Delta = 1.0, 0.6, 0.6
k = np.linspace(-np.pi, np.pi, 801)                  # momentum per site, the distance between sites is 1


def two_sites(kk, m):
    """Bloch Hamiltonian of the chain with the onsite energies +m and -m and the hopping -t, with k per site. The cell
    has the length 2, so the bond to the next cell carries the phase exp(-2ik)."""
    off = -t * (1 + np.exp(-2j * kk))
    return np.array([[m, off], [np.conj(off), -m]])


def bdg(kk, Delta):
    """Bogoliubov-de Gennes Hamiltonian of the half-filled chain, xi = -2t cos k, with the s-wave pairing Delta,
    in the basis (c_k_up, c^dag_-k_down)."""
    xi = -2 * t * np.cos(kk)
    return np.array([[xi, Delta], [Delta, -xi]])


semi = np.array([np.linalg.eigvalsh(two_sites(x, m)) for x in k])
sc = np.array([np.linalg.eigvalsh(bdg(x, Delta)) for x in k])
gap_semi = semi[:, 1].min() - semi[:, 0].max()
gap_sc = sc[:, 1].min() - sc[:, 0].max()
check('the chain with two sites per cell and m = 0.6t has the gap 2m = 1.2t', abs(gap_semi - 1.2) < 1e-12, gap_semi)
check('the superconducting chain with Delta = 0.6t has the gap 2 Delta = 1.2t', abs(gap_sc - 1.2) < 1e-12, gap_sc)
at = k[np.isclose(semi[:, 1], semi[:, 1].min(), atol=1e-12)]
at_sc = k[np.isclose(sc[:, 1], sc[:, 1].min(), atol=1e-12)]
check('both gaps sit at k = +-pi/2', np.allclose(np.sort(at), [-np.pi / 2, np.pi / 2]) and
      np.allclose(np.sort(at_sc), [-np.pi / 2, np.pi / 2]), (at, at_sc))
check('for m = Delta the two spectra are the same curves', np.allclose(semi, sc, atol=1e-12),
      np.abs(semi - sc).max())
semi0 = np.array([np.linalg.eigvalsh(two_sites(x, 0.)) for x in k])
sc0 = np.array([np.linalg.eigvalsh(bdg(x, 0.)) for x in k])
grey = np.sort(np.array([2 * t * np.cos(k), -2 * t * np.cos(k)]).T, axis=1)
check('the grey lines, the bands without the gap, are +-2t cos k in both panels',
      np.allclose(semi0, grey, atol=1e-12) and np.allclose(sc0, grey, atol=1e-12), np.abs(semi0 - grey).max())
check('the bands of the chain with two sites per cell repeat with the period pi, outside the zone from -pi/2 to pi/2',
      np.allclose(np.linalg.eigvalsh(two_sites(0.3, m)), np.linalg.eigvalsh(two_sites(0.3 + np.pi, m))), True)
check('the gap 2m opens at the zone edge k = pi/2 of the cell of two sites, with no interaction',
      np.allclose(np.linalg.eigvalsh(two_sites(np.pi / 2, m)), [-m, m]), np.linalg.eigvalsh(two_sites(np.pi / 2, m)))
check('without the pairing the half-filled chain has no gap, -2t cos k crosses zero at k = +-pi/2',
      abs(gap_sc0 := sc0[:, 1].min() - sc0[:, 0].max()) < 1e-12, gap_sc0)

# the pyqula script that the student downloads gives the same bands
d = style.run_script('session01/g1_two_gaps.py')
kp = np.array(d['k'])
E = np.sqrt(m ** 2 + 4 * t ** 2 * np.cos(kp) ** 2)
check('pyqula, the chain with two sites per cell, +-sqrt(m^2 + 4t^2 cos^2 k)',
      np.allclose(d['semiconductor'], np.array([-1, 1]) * E[:, None], atol=1e-12), d['gap_semiconductor'])
check('pyqula, the BdG bands of h.add_swave(0.6), +-sqrt(xi^2 + Delta^2) twice, gap 1.2',
      np.allclose(d['superconductor'], np.array([-1, -1, 1, 1]) * E[:, None], atol=1e-12)
      and abs(d['gap_superconductor'] - 1.2) < 1e-12, d['gap_superconductor'])

# the alt text: the bands of both panels reach +-2.09 = +-sqrt(m^2 + 4t^2), at k = 0 and k = +-pi, and k runs from -pi to pi
top = np.sqrt(m ** 2 + 4 * t ** 2)
check('the closed form of the band top, sqrt(m^2 + 4t^2), rounds to 2.09', round(top, 2) == 2.09, top)
check('numpy, both panels reach +-2.09', all(abs(b.max() - top) < 1e-12 and abs(b.min() + top) < 1e-12 for b in (semi, sc)),
      (semi.max(), sc.max()))
check('pyqula, both panels reach +-2.09',
      all(abs(np.max(d[x]) - top) < 1e-12 and abs(np.min(d[x]) + top) < 1e-12 for x in ('semiconductor', 'superconductor')),
      (np.max(d['semiconductor']), np.max(d['superconductor'])))
check('the momentum of the pyqula script runs from -pi to pi', abs(kp[0] + np.pi) < 1e-12 and abs(kp[-1] - np.pi) < 1e-12,
      (kp[0], kp[-1]))

# the caption, sentence added on 2026-11-22: "Here Delta is an energy, the pair amplitude of (1.9) times the attraction,
# as in Session 5." The mean field of U n_up n_dn = U c_up^+ c_dn^+ c_dn c_up in the pairing channel is the term
# U <c_dn c_up> c_up^+ c_dn^+ + h.c., so the energy Delta of the pairing term is U <c_dn c_up>, the Delta_n of (5.3).
# Route 1: each pair (k up, -k down) is a Fock space of two modes, solved exactly, and the onsite amplitude is the mean
# of <c_-k_dn c_k_up> over k. Route 2: the closed form <c_dn c_up> = -mean(Delta / 2E_k). For Delta > 0 the amplitude is
# negative, so Delta = U <c_dn c_up> needs U < 0, an attraction, and the self-consistent chain at U = -3t has
# |Delta| = 0.931 = 3 |<c_dn c_up>|.
from scipy import optimize
a2, Z2, I2 = np.array([[0., 1.], [0., 0.]]), np.diag([1., -1.]), np.eye(2)
ca, cb = np.kron(a2, I2), np.kron(Z2, a2)                    # c_k_up and c_-k_dn, Jordan-Wigner on two modes
kk = (np.arange(4000) + 0.5) / 4000 * 2 * np.pi - np.pi


def pair_amplitude(D):
    amp = []
    for x in kk:
        xi = -2 * t * np.cos(x)
        H2 = xi * (ca.T @ ca + cb.T @ cb) + D * (ca.T @ cb.T + cb @ ca)
        w, v = np.linalg.eigh(H2)
        g0 = v[:, 0]
        amp.append(g0 @ (cb @ ca) @ g0)
    return np.mean(amp)


F06 = pair_amplitude(0.6)
closed06 = -np.mean(0.6 / (2 * np.sqrt((2 * t * np.cos(kk)) ** 2 + 0.6 ** 2)))
check('caption: for the pairing Delta = 0.6t the onsite amplitude <c_dn c_up> is negative, the same by the two routes',
      F06 < 0 and abs(F06 - closed06) < 1e-12, (F06, closed06))
U06 = 0.6 / F06
check('caption: Delta = U <c_dn c_up> then needs U < 0, an attraction, here U = Delta / <c_dn c_up>', U06 < 0, U06)
Dsc = optimize.brentq(lambda D: D - (-3.0) * (-np.mean(D / (2 * np.sqrt((2 * t * np.cos(kk)) ** 2 + D ** 2)))), 0.05, 3.0)
Fsc = pair_amplitude(Dsc)
check('caption: the self-consistent chain at U = -3t has |Delta| = 0.931, |<c_dn c_up>| = 0.310, and Delta = U <c_dn c_up>',
      abs(Dsc - 0.931) < 1e-3 and abs(abs(Fsc) - 0.310) < 1e-3 and abs(Dsc - (-3.0) * Fsc) < 1e-9, (Dsc, Fsc))
check('caption: so the energy Delta is |U| = 3 times the pair amplitude of (1.9)', abs(Dsc / abs(Fsc) - 3.0) < 1e-9,
      Dsc / abs(Fsc))
s5 = open(os.path.join(HERE, '..', '..', 'pages', 'session05',
                       '04-the-interacting-hamiltonian-and-the-origin-of-attractive-interactions.md'), encoding='utf-8').read()
check('caption: Session 5 defines Delta_n = U <c_dn c_up> in (5.3)',
      r'\Delta_n \equiv U\langle c_{n\downarrow}c_{n\uparrow}\rangle, \tag{5.3}' in s5, '(5.3)')

# the paragraph on the goals of the United Nations, corrected on 2026-11-22: the numbers of the goals had no stored
# source, so the paragraph names the goals and quotes no number
page = open(os.path.join(HERE, '..', '..', 'pages', 'session01', '01-why-quantum-materials-and-why-now.md'),
            encoding='utf-8').read()
para = next(p for p in page.split('\n\n') if 'Sustainable Development Goals' in p)
check('the paragraph on the goals of the United Nations quotes no number', not any(ch.isdigit() for ch in para),
      [w for w in para.split() if any(ch.isdigit() for ch in w)])
