# The uniform chain described with a cell of three sites, Section 2.7
import numpy as np
from pyqula import geometry

g = geometry.chain().get_supercell(3)  # the same chain with three sites per cell, lattice constant 3
h = g.get_hamiltonian(has_spin=False, tij=[-1.])  # first-neighbor hopping -t with t = 1, the sign of (2.5)
ks = np.linspace(-0.5, 0.5, 401)  # momentum in units of 2 pi over the cell of three sites
(ik, e) = h.get_bands(kpath=[[k, 0., 0.] for k in ks])  # the bands, three energies per momentum
bands = np.array(e).reshape(len(ks), 3)  # the three folded bands
phi = 2*np.pi*ks  # the phase per cell of three sites, from -pi to pi
