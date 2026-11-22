# The lowest eigenstate of the Aubry-Andre ring for three strengths of the potential, Section 9.10a
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with one site per cell
h0 = g.get_hamiltonian(has_spin=False, tij=[-1.])  # spinless, hopping -t with t=1
phi = 0.3  # phase of the potential
V0s = [1., 2., 3.]  # strengths of the potential, in units of t
weight = {}  # |psi_n|^2 of the lowest state, for each size and strength
ipr = {}  # its inverse participation ratio
spacing = {}  # the distance to the next level, so the lowest state is not degenerate
for (N, q) in [(55, 34/55), (233, 144/233), (987, 610/987)]:  # rings, q a ratio of Fibonacci numbers
    ring = h0.set_finite_system(n=N, periodic=True)  # ring of N sites
    for V0 in V0s:
        h = ring.copy()  # the clean ring
        h.add_onsite(V0*np.cos(2*np.pi*q*np.arange(N) + phi))  # quasiperiodic onsite energy
        (energies, vectors) = h.get_eigenvectors()  # eigenstates as rows
        order = np.argsort(energies)  # from the lowest level up
        w = np.abs(vectors[order[0]])**2  # weight of the lowest state on each site
        weight[(N, V0)] = w
        ipr[(N, V0)] = np.sum(w**2)
        spacing[(N, V0)] = energies[order[1]] - energies[order[0]]

print(ipr[(233, 3.)], ipr[(987, 3.)])  # a localized state keeps its IPR as the ring grows
