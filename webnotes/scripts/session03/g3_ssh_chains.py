# Levels of three open chains of 16 sites, two of them with alternating hoppings, Section 3.9b
import numpy as np
from pyqula import geometry

t = 0.5 # weak hopping, the strong hopping is 1
N = 8 # number of unit cells, with two sites each
g = geometry.bichain() # create the chain, with two sites per unit cell

h = g.get_hamiltonian(has_spin=False) # create the Hamiltonian
h.intra = t*h.intra # weak hopping inside the cell
h = h.set_finite_system(n=N) # open chain of N cells, it ends with a weak bond
levels_weak_ends = np.sort(h.get_bands()[1]) # compute the levels

h = g.get_hamiltonian(has_spin=False) # create the Hamiltonian
h.inter = t*h.inter # weak hopping between the cells
h = h.set_finite_system(n=N) # open chain of N cells, it ends with a strong bond
levels_strong_ends = np.sort(h.get_bands()[1]) # compute the levels

h = g.get_hamiltonian(has_spin=False) # create the Hamiltonian, with all the hoppings equal to 1
h = h.set_finite_system(n=N) # open chain of N cells
levels_uniform = np.sort(h.get_bands()[1]) # compute the levels
