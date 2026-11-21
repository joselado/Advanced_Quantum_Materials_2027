"""Session 3, the numbers that page 05 (Section 3.5) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a lab box is an
assert, here or in the figure script that draws it. The numbers of the plateau figure are asserted in
figures/session03/hall_plateau.py, those of the three maps in _berrymap.py, and those of the mesh quiz in
chern_mesh.py. This script holds the rest. It finds the repository from its own path and writes no file."""
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
import physcheck  # noqa: E402


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# the lab box: h/e^2 = 25.8 kOhm, and 27 K as 2.3 meV
h_planck, e_charge, k_boltzmann = 6.62607015e-34, 1.602176634e-19, 1.380649e-23
r_k = h_planck / e_charge ** 2
check('h/e^2 in kOhm, the page says 25.8', abs(r_k / 1e3 - 25.8) < 0.05, round(r_k / 1e3, 3))
gap_mev = 27 * k_boltzmann / e_charge * 1e3
check('27 K in meV, the page says 2.3', abs(gap_mev - 2.3) < 0.05, round(gap_mev, 3))

# pyqula writes files, so it runs in a temporary folder
os.chdir(tempfile.mkdtemp())
from pyqula import geometry  # noqa: E402

g = geometry.honeycomb_lattice()


def model(haldane=0.0, imbalance=0.0):
    h = g.get_hamiltonian(has_spin=False)
    if haldane:
        h.add_haldane(haldane)
    if imbalance:
        h.add_sublattice_imbalance(imbalance)
    return physcheck.from_pyqula(h)


def weights(hk, B, nk=90):
    """The integral of the positive and of the negative part of Omega of the lower band over one zone, over pi."""
    area = abs(np.linalg.det(B)) / nk ** 2
    om = np.array([physcheck.berry_curvature(hk, k, 0) for k in physcheck.kmesh(B, nk)])
    return om[om > 0].sum() * area / np.pi, om[om < 0].sum() * area / np.pi


# the picture quiz, first option: the red and the blue spots of the staggered lattice give about 0.7 pi each
pos, neg = weights(*model(imbalance=0.5))
check('staggered 0.5, positive and negative weight over pi, the page says about 0.7', abs(pos - 0.7) < 0.03
      and abs(neg + 0.7) < 0.03, (round(pos, 3), round(neg, 3)))

# second option: the Haldane coupling -0.1 gives -2 pi, with nothing that cancels
pos, neg = weights(*model(haldane=-0.1))
check('Haldane -0.1, total weight over pi, the page says -2', abs(pos + neg + 2) < 0.02, round(pos + neg, 3))
hk, B = model(haldane=-0.1)
check('Haldane -0.1, Chern number, the page says sigma_xy = -e^2/h', abs(physcheck.chern_links(hk, B, 0, 24) + 1) < 1e-6, -1)

# third option: Haldane 0.1 with a staggered potential 0.8 cancels, and the gap closes at 0.45, half of the gap 0.9
pos, neg = weights(*model(haldane=0.1, imbalance=0.8))
check('Haldane 0.1 with staggered 0.8, the two weights cancel', abs(pos + neg) < 0.02, (round(pos, 3), round(neg, 3)))
hk, B = model(haldane=0.1)
gap = physcheck.gap(hk, B, 1, nk=60)
check('Haldane 0.1, gap, the page says 0.9', abs(gap - 0.90) < 0.005, round(gap, 4))
hk, B = model(haldane=0.1, imbalance=0.45)
check('gap at the staggered potential 0.45, the page says it closes', physcheck.gap(hk, B, 1, nk=60) < 0.005,
      round(physcheck.gap(hk, B, 1, nk=60), 5))
hk, B = model(haldane=0.1, imbalance=0.40)
c_below = physcheck.chern_links(hk, B, 0, 48)
hk, B = model(haldane=0.1, imbalance=0.50)
c_above = physcheck.chern_links(hk, B, 0, 48)
check('the integer goes from 1 to 0 across 0.45', abs(c_below - 1) < 1e-6 and abs(c_above) < 1e-6,
      (round(c_below, 6), round(abs(c_above), 6)))
