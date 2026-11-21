# Conductance of a clean ribbon, a quantum spin Hall insulator and an ordinary insulator, Section 3.11
import numpy as np
from pyqula import geometry, heterostructures

energies = np.linspace(-0.8, 0.8, 161) # chemical potentials, in units of the hopping
g = geometry.honeycomb_zigzag_ribbon(10) # create the ribbon, with zigzag edges

h = g.get_hamiltonian() # create the Hamiltonian
h.add_soc(0.1) # add the intrinsic spin-orbit coupling
ht = heterostructures.Heterostructure(h) # two leads and a central part, all the same ribbon
conductance_qsh = np.array([ht.landauer(energy=e) for e in energies]) # transmission, in units of e^2/h

h = g.get_hamiltonian() # create the Hamiltonian
h.add_sublattice_imbalance(0.45) # add a sublattice imbalance, with the same gap
ht = heterostructures.Heterostructure(h) # two leads and a central part, all the same ribbon
conductance_trivial = np.array([ht.landauer(energy=e) for e in energies]) # transmission, in units of e^2/h

hb = geometry.honeycomb_lattice().get_hamiltonian() # the bulk of the first model
hb.add_soc(0.1) # add the intrinsic spin-orbit coupling
gap = hb.get_gap() # bulk gap, the same for both models
