# Spinon Fermi surface of the triangular lattice at half filling, for three ratios t2/t1
import numpy as np
from pyqula import geometry

g = geometry.triangular_lattice()  # triangular lattice, lattice constant 1
nk = 151  # points per side of the map
delta = 0.15  # broadening of the levels
t2s = [-0.5, 0., 0.5]  # second-neighbor hopping, the first-neighbor hopping is 1
maps = []  # one map per t2
for t2 in t2s:
    h = g.get_hamiltonian(tij=[1., t2])  # spinon hopping to first and second neighbors, with the two spins
    h.set_filling(0.5, nk=101)  # one fermion per site, the Fermi level is moved to zero
    (kx, ky, w) = h.get_fermi_surface(e=0., delta=delta, nk=nk)  # weight of the states at the Fermi level
    maps.append(np.array(w).reshape(nk, nk))  # the first index runs along kx
