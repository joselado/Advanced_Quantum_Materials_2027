# Local density of states of three flakes of the honeycomb lattice, Section 3.1
import numpy as np
from pyqula import geometry, islands

g = islands.get_geometry(name="honeycomb", n=12, nedges=6, rot=np.pi/6) # create the flake, with armchair edges
gb = geometry.honeycomb_lattice() # the infinite lattice, for the bulk gap

h = g.get_hamiltonian(has_spin=False) # create the Hamiltonian of the flake
h.add_haldane(0.1) # add the Haldane coupling
(x, y, ldos_haldane) = h.get_ldos(e=0., delta=0.03) # local density of states at the chemical potential
hb = gb.get_hamiltonian(has_spin=False) # the same model in the bulk
hb.add_haldane(0.1)
gap_haldane = hb.get_gap() # bulk gap with the Haldane coupling

h = g.get_hamiltonian(has_spin=False) # create the Hamiltonian again
h.add_sublattice_imbalance(0.5) # add a staggered potential instead
(x, y, ldos_staggered) = h.get_ldos(e=0., delta=0.03) # local density of states at the chemical potential
hb = gb.get_hamiltonian(has_spin=False) # the same model in the bulk
hb.add_sublattice_imbalance(0.5)
gap_staggered = hb.get_gap() # bulk gap with the staggered potential

h = g.get_hamiltonian(has_spin=False) # create the Hamiltonian again
h.add_onsite(0.6) # no gap, and the chemical potential inside the band
(x, y, ldos_metal) = h.get_ldos(e=0., delta=0.03) # local density of states at the chemical potential
