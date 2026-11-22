"""Session 4, the statements and numbers that page 19 (Section 4.19, the Haldane model and the quantum Hall effect without Landau
levels) gives. One check script per page is the rule. The page has no figure of its own, since the panel of s03f05_masses is a
figure of the PDF of Session 3. This script checks the Chern numbers of the text and of the second quiz, C = +1 and -1 for the
two signs of the Haldane coupling and C = 0 for a staggered potential, each from h.get_chern() and from the link variables of
physcheck; that a filled Landau level of the honeycomb lattice and the Haldane model have the same Chern number, which is the
claim of the opener; that the Haldane model has no flux through its unit cell; and that on the path of the notebook cell
"Topological equivalence between the Quantum Hall state and a Chern insulator" no bulk state comes to zero energy, so the bulk
gap stays open, for the signs of the notebook, as the conventions sheet says. It finds the repository from its own path and
writes no file, since pyqula runs in a temporary folder."""
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
import physcheck as pc  # noqa: E402


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


os.chdir(tempfile.mkdtemp())
from pyqula import geometry  # noqa: E402

# the Chern numbers of the two gapped honeycomb lattices, with the sign of the Berry curvature of the notes
for x, want in ((0.1, 1), (-0.1, -1)):
    h = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False)
    h.add_haldane(x)
    hk, B = pc.from_pyqula(h)
    Cl, Cq = pc.chern_links(hk, B, bands=0, nk=24), h.get_chern(nk=40)
    check('h.add_haldane(%+.1f) gives C = %+d, links and get_chern' % (x, want), abs(Cl - want) < 1e-6 and abs(Cq - want) < 1e-6,
          '%+.6f %+.6f' % (Cl, Cq))
h = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False)
h.add_sublattice_imbalance(0.5)
hk, B = pc.from_pyqula(h)
Cl, Cq = pc.chern_links(hk, B, bands=0, nk=24), h.get_chern(nk=40)
check('a staggered potential 0.5 gives C = 0, links and get_chern', abs(Cl) < 1e-6 and abs(Cq) < 1e-6, '%+.6f %+.6f' % (Cl, Cq))

# no flux through the unit cell of the Haldane model: its Bloch Hamiltonian is periodic on the cell of two sites, while a field
# needs a magnetic cell with a whole number of flux quanta, as in the next check
h = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False)
h.add_haldane(0.1)
hk, B = pc.from_pyqula(h)
k = np.array([0.31, -0.17])
check('the Haldane model, H(k + b) = H(k) on the cell of two sites', np.allclose(hk(k + B[0]), hk(k)) and np.allclose(hk(k + B[1]), hk(k)), 'yes')

# a filled Landau level of the honeycomb lattice and the Haldane model have the same Chern number, in the magnetic cell of the
# recipe "The Chern number of a Landau gap of the honeycomb lattice"
n = 20
g = geometry.honeycomb_lattice_square_cell().rotate(90).get_supercell((n, 1))
h = g.get_hamiltonian(has_spin=False)
h.add_orbital_magnetic_field(1 / (3 * np.sqrt(3) * n))
h.add_onsite(-0.25)
C_field = h.get_chern(nk=8)
h = g.get_hamiltonian(has_spin=False)
h.add_haldane(0.07)
C_haldane = h.get_chern(nk=8)
check('the gap above the zero level in a field and add_haldane(0.07) in the same cell, both C = +1',
      abs(C_field - 1) < 1e-3 and abs(C_haldane - 1) < 1e-3, '%+.4f %+.4f' % (C_field, C_haldane))

# the path of the notebook, from the Chern insulator to the quantum Hall state, keeps the bulk gap open
g = geometry.honeycomb_armchair_ribbon(20)
H_hall = g.get_hamiltonian(has_spin=False)
H_hall.add_orbital_magnetic_field(0.01)
H_hall.add_onsite(-0.2)
H_chern = g.get_hamiltonian(has_spin=False)
H_chern.add_haldane(0.07)
central = np.abs(g.y) < 0.5 * np.max(g.y)
closest = []
for nu in np.linspace(0., 1., 11):
    hk = (H_hall * nu + H_chern * (1 - nu)).get_hk_gen()
    e_min = 10.
    for kk in np.linspace(-0.5, 0.5, 41):
        e, v = np.linalg.eigh(np.array(hk([kk, 0., 0.])))
        bulk = np.sum(np.abs(v[central]) ** 2, axis=0) > 0.5
        e_min = min(e_min, np.min(np.abs(e[bulk])))
    closest.append(e_min)
check('on the path of the notebook no bulk state comes closer to zero energy than 0.198',
      min(closest) > 0.19 and abs(min(closest) - 0.198) < 0.0015, np.round(closest, 3))
print('all checks of page 19 hold')
