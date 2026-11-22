# BdG bands of the triangular lattice with s-wave pairing at three chemical potentials, Section 5.9
import numpy as np
from pyqula import geometry

G, K, M = np.array([0., 0., 0.]), np.array([1/3, 1/3, 0.]), np.array([0.5, 0., 0.])  # in units of the reciprocal vectors
segments = [(G, K), (K, M), (M, G)]  # the path Gamma, K, M, Gamma
kpath = [a + (b - a)*s for (a, b) in segments for s in np.linspace(0., 1., 150, endpoint=False)] + [G]
onsites = [-3., 0., 2.5]  # add_onsite(x) moves the band by x, which is the chemical potential mu=-x
energies = []  # the four BdG bands at each momentum, for each mu
weights = []  # electron weight of each state, from 0 to 1
for x in onsites:
    g = geometry.triangular_lattice()  # triangular lattice, first-neighbor hopping 1
    h = g.get_hamiltonian()  # Hamiltonian with the two spins
    h.add_onsite(x)  # chemical potential mu=-x
    h.add_pairing(mode="swave", delta=0.4)  # uniform s-wave pairing Delta=0.4
    (ik, e, c) = h.get_bands(operator="electron", kpath=kpath)  # BdG bands and their electron weight
    energies.append(np.array(e).reshape(len(kpath), -1))  # energy of band n at step i of the path
    weights.append(np.array(c).reshape(len(kpath), -1))  # electron weight of band n at step i
smallest = [np.min(np.abs(e)) for e in energies]  # smallest energy on the path, close to Delta
