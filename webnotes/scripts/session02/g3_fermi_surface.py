# Fermi surface of the square lattice at three energies
import numpy as np
from pyqula import geometry

g = geometry.square_lattice()  # square lattice, lattice constant 1
h = g.get_hamiltonian(has_spin=False, tij=[-1.0])  # first-neighbor hopping -1, the sign of (2.14)
nk = 201  # points per side, from -2 pi to 2 pi with both ends
delta = 0.15  # half width of each level, in units of t
(x, y, w_low) = h.get_fermi_surface(e=-3.0, delta=delta, nk=nk)  # weight of the states at the energy -3t
(x, y, w_mid) = h.get_fermi_surface(e=-1.0, delta=delta, nk=nk)  # the same at -t
(x, y, w_half) = h.get_fermi_surface(e=0.0, delta=delta, nk=nk)  # the same at zero energy, half filling
kx = 2*np.pi*np.array(x)  # momentum along x
ky = 2*np.pi*np.array(y)  # momentum along y
