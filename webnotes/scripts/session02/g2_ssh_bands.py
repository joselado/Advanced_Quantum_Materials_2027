# The two bands of the chain with alternating hoppings, equation (2.13) of Section 2.7
import numpy as np
from pyqula import geometry

g = geometry.bichain()  # chain with two sites A and B per cell, lattice constant 2
ks = np.linspace(-0.5, 0.5, 401)  # momentum in units of 2 pi over the cell, one Brillouin zone
kpath = [[k, 0., 0.] for k in ks]  # the k-path, as reduced momenta
phi = 2*np.pi*ks  # the Bloch phase of the cell of two sites, from -pi to pi

bands = {}  # the two bands for each hopping eta between the cells
for eta in [0.6, 1.]:
    h = g.get_hamiltonian(has_spin=False)  # every hopping 1, the hopping inside the cell stays 1
    h.inter = eta*h.inter  # the hopping from B of a cell to A of the next cell becomes eta
    (ik, e) = h.get_bands(kpath=kpath)  # the bands, two energies per momentum
    bands[eta] = np.array(e).reshape(len(ks), 2)

gap = bands[0.6][0, 1] - bands[0.6][0, 0]  # the gap at the zone edge phi = pi, which is 2|1 - eta| = 0.8
