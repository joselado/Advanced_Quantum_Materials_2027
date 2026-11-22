# Three classes of spinon bands of the mean-field Hamiltonian (8.15), for one spin species
import numpy as np
from pyqula import geometry

ks = np.linspace(-0.5, 0.5, 401)  # momentum in units of 2 pi over the length of the cell

h = geometry.chain().get_hamiltonian(has_spin=False)  # uniform spinon chain, hopping 1
hk = h.get_hk_gen()  # Bloch Hamiltonian
e_uniform = np.array([np.linalg.eigvalsh(hk([k, 0., 0.])) for k in ks])  # one band, 2 cos k

h = geometry.bichain().get_hamiltonian(has_spin=False)  # the same chain with two sites per cell
h.intra = 0.6*h.intra  # hopping 0.6 inside the cell and 1 between the cells
hk = h.get_hk_gen()  # Bloch Hamiltonian of the cell of two sites
e_dimerized = np.array([np.linalg.eigvalsh(hk([k, 0., 0.])) for k in ks])  # two bands with a gap

g = geometry.square_lattice().get_supercell([1, 2])  # square lattice with two sites along y in the cell
h = g.get_hamiltonian(has_spin=False)  # hopping 1
h.add_orbital_magnetic_field(0.5)  # half a flux quantum per plaquette, the pi-flux state
hk = h.get_hk_gen()  # Bloch Hamiltonian of the cell
e_piflux = np.array([np.linalg.eigvalsh(hk([k, 0.5, 0.])) for k in ks])  # the line ky = pi/2, through the Dirac points
