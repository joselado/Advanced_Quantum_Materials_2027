"""Session 1, the numbers that page 01 (Section 1.1) quotes, in the caption of gap_two_origins and in its quiz.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The figure script gap_two_origins.py asserts the pyqula bands of
webnotes/scripts/session01/g1_two_gaps.py. This script checks the same statements by a second route, the 2x2 Bloch
Hamiltonian of the chain with two sites per cell and the 2x2 Bogoliubov-de Gennes Hamiltonian of the chain written by
hand in numpy, and then the pyqula script once more. It writes no file, since pyqula runs in a temporary folder."""
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
