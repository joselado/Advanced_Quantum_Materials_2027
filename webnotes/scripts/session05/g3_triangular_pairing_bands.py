# BdG bands of the triangular lattice with no pairing, s-wave and nodal f-wave pairing, Section 5.13
import numpy as np
from pyqula import geometry

G, K, M = np.array([0., 0., 0.]), np.array([1/3, 1/3, 0.]), np.array([0.5, 0., 0.])  # in units of the reciprocal vectors
segments = [(G, K), (K, M), (M, G)]  # the path Gamma, K, M, Gamma
kpath = [a + (b - a)*s for (a, b) in segments for s in np.linspace(0., 1., 300, endpoint=False)] + [G]
modes = [("swave", 0.), ("swave", 0.4), ("nodal_fwave", 0.2)]  # no pairing, s-wave and nodal f-wave
energies = []  # the four BdG bands at each momentum, for each pairing
weights = []  # electron weight of each state, from 0 to 1
for (mode, delta) in modes:
    g = geometry.triangular_lattice()  # triangular lattice, first-neighbor hopping 1
    h = g.get_hamiltonian()  # Hamiltonian with the two spins, the Fermi level at zero
    h.add_pairing(mode=mode, delta=delta)  # pairing of this symmetry, delta is the parameter of pyqula
    (ik, e, c) = h.get_bands(operator="electron", kpath=kpath)  # BdG bands and their electron weight
    energies.append(np.array(e).reshape(len(kpath), -1))  # energy of band n at step i of the path
    weights.append(np.array(c).reshape(len(kpath), -1))  # electron weight of band n at step i
smallest = [np.min(np.abs(e)) for e in energies]  # smallest energy on the path
