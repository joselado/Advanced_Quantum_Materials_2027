# Density of states of graphene
import numpy as np
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice, bond length 1
h = g.get_hamiltonian(has_spin=False)  # spinless, first-neighbor hopping +1, the +t of (2.19)
energies = np.linspace(-3.5, 3.5, 701)  # energies in units of the hopping
(e, dos) = h.get_dos(energies=energies, delta=4e-2, nk=200)  # each level a Lorentzian of half width 0.04, on 200 x 200 momenta
states = np.sum(dos)*(e[1] - e[0])  # states per cell in the window, close to 2, one for each band
