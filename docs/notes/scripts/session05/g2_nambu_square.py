# BdG bands of the square lattice with s-wave pairing, with the electron weight, Section 5.8
import numpy as np
from pyqula import geometry

G, X, M = np.array([0., 0., 0.]), np.array([0.5, 0., 0.]), np.array([0.5, 0.5, 0.])  # points of the zone, in units of 2 pi
segments = [(G, X), (X, M), (M, G)]  # the path Gamma, X, M, Gamma
kpath = [a + (b - a)*s for (a, b) in segments for s in np.linspace(0., 1., 150, endpoint=False)] + [G]
deltas = [0., 0.2, 0.4, 0.8]  # s-wave pairing, the values of the try-it box
energies = []  # the four BdG bands at each momentum, for each Delta
weights = []  # electron weight of each state, from 0 to 1
for delta in deltas:
    g = geometry.square_lattice()  # square lattice, first-neighbor hopping 1
    h = g.get_hamiltonian()  # Hamiltonian with the two spins
    h.set_filling(0.2, nk=20)  # Fermi level at the filling 0.2
    onsite = h.intra[0, 0].real  # the shift that set_filling adds, which is minus mu
    h.setup_nambu_spinor()  # Nambu spinor, electrons and holes
    h.add_swave(delta)  # s-wave pairing Delta
    (ik, e, c) = h.get_bands(operator="electron", kpath=kpath)  # BdG bands and their electron weight
    energies.append(np.array(e).reshape(len(kpath), -1))  # energy of band n at step i of the path
    weights.append(np.array(c).reshape(len(kpath), -1))  # electron weight of band n at step i
smallest = [np.min(np.abs(e)) for e in energies]  # smallest energy on the path, close to Delta
