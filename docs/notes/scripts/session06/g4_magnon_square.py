# Magnon band of a ferromagnet on the square lattice, in linear spin-wave theory
import numpy as np
from pyqula import geometry

g = geometry.square_lattice()  # square lattice, lattice constant 1
h = g.get_hamiltonian(has_spin=False, tij=[-1.])  # magnon hopping -|J|S, with |J|S = 1
h.add_onsite(4.)  # the onsite energy z|J|S with z = 4, so that the band starts at zero

nodes = np.array([[0., 0., 0.], [0.5, 0., 0.], [0.5, 0.5, 0.], [0., 0., 0.]])  # Gamma, X, M, Gamma, in units of 2 pi
kpath = [nodes[i] + (nodes[i+1] - nodes[i])*j/100 for i in range(3) for j in range(100)] + [nodes[3]]  # 301 momenta
(k, e) = h.get_bands(kpath=kpath)  # the magnon band, 0 at Gamma, 4 at X and 8 at M
