# Density of states of the chain, the honeycomb lattice and the kagome lattice, on the same energies
import numpy as np
from pyqula import geometry

energies = np.linspace(-4.5, 3.5, 801)  # energies in units of the hopping
h = geometry.chain().get_hamiltonian(has_spin=False, tij=[-1.])  # chain, hopping -1, the sign of (2.5)
(e, dos_chain) = h.get_dos(energies=energies, delta=4e-2, nk=2000)  # states per cell of one site, per unit of energy
h = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False)  # graphene, hopping +1, the +t of (2.19)
(e, dos_honeycomb) = h.get_dos(energies=energies, delta=4e-2, nk=200)  # states per cell of two sites
h = geometry.kagome_lattice().get_hamiltonian(has_spin=False, tij=[-1.])  # kagome, hopping -1
(e, dos_kagome) = h.get_dos(energies=energies, delta=4e-2, nk=200)  # states per cell of three sites
