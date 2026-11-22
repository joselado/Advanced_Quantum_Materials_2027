# The open XX chain of 6 spins as free fermions, after the Jordan-Wigner transformation
import itertools
import numpy as np
from pyqula import geometry

J = 1.0  # coupling of the XX chain J sum_i (Sx_i Sx_i+1 + Sy_i Sy_i+1)
L = 6  # number of sites of the open chain
g = geometry.chain()  # chain with one site per cell and hopping 1
h = g.get_hamiltonian(has_spin=False).set_finite_system(n=L)  # open chain of L sites, spinless fermions
h.intra = 0.5*J*h.intra  # hopping J/2, what the Jordan-Wigner transformation gives
eps = np.sort(h.get_bands()[1])  # the L single-particle levels
levels = {N: np.sort([sum(c) for c in itertools.combinations(eps, N)]) for N in range(L + 1)}  # levels with N fermions
ground = np.sum(eps[eps < 0])  # ground state, all the negative levels filled
