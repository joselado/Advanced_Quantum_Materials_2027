# Band of the square lattice, along a path and over the Brillouin zone
import numpy as np
from pyqula import geometry

g = geometry.square_lattice()  # square lattice, lattice constant 1
h = g.get_hamiltonian(has_spin=False, tij=[-1.0])  # first-neighbor hopping -1, the sign of (2.14)

nodes = np.array([[0., 0., 0.], [0.5, 0., 0.], [0.5, 0.5, 0.], [0., 0., 0.]])  # Gamma, X, M, Gamma, in units of 2 pi
kpath = [nodes[i] + (nodes[i+1] - nodes[i])*j/100 for i in range(3) for j in range(100)] + [nodes[3]]  # 301 momenta
(k, e) = h.get_bands(kpath=kpath)  # the band along the path, -4 at Gamma, 0 at X, 4 at M

nk = 80  # points per side of the map
(kxy, band) = h.get_bands_map(n=0, nk=nk)  # the band on a square of two zones per side
kx = 2*np.pi*np.array(kxy)[:, 0]  # momentum along x, from -2 pi to 2 pi
ky = 2*np.pi*np.array(kxy)[:, 1]  # momentum along y
band = np.array(band)  # the energy at each point, in units of t
