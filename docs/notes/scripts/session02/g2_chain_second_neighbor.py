# Band of the chain with a first- and a second-neighbor hopping, equation (2.9) of Section 2.5
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with one site per cell, lattice constant a = 1
ks = np.linspace(-0.5, 0.5, 401)  # momentum in units of 2 pi, one Brillouin zone
kpath = [[k, 0., 0.] for k in ks]  # the k-path, as reduced momenta
phi = 2*np.pi*ks  # the Bloch phase, from -pi to pi

bands = {}  # the band for each second-neighbor hopping eta, in units of t
for eta in [0., 0.2, 0.5]:
    h = g.get_hamiltonian(has_spin=False, tij=[-1., -eta])  # hoppings -t and -eta with t = 1, the sign of (2.5)
    (ik, e) = h.get_bands(kpath=kpath)  # the band, one energy per momentum
    bands[eta] = np.array(e)

h = g.get_hamiltonian(has_spin=False, tij=[1.])  # the opposite sign of the hopping, which is t = -1
(ik, e) = h.get_bands(kpath=kpath)  # its band, the band of eta = 0 upside down
band_negative_t = np.array(e)
