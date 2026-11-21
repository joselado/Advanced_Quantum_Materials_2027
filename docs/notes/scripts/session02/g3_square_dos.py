# Density of states of the square lattice
import numpy as np
from pyqula import geometry

g = geometry.square_lattice()  # square lattice, lattice constant 1
h = g.get_hamiltonian(has_spin=False, tij=[-1.0])  # first-neighbor hopping -1, the sign of (2.14)
energies = np.linspace(-5., 5., 501)  # energies in units of t
delta = 0.05  # half width of each level, in units of t
nk = 300  # points per side of the k-mesh
(e, dos) = h.get_dos(energies=energies, delta=delta, nk=nk)  # states per site and per unit of energy
dos = np.array(dos)  # the band is -4 to 4, the peak is at zero energy
