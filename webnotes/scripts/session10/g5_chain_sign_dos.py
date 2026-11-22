# The chains with the hopping t=1 and t=-1, their bands and their density of states
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with one site per cell, a = 1
ks = np.linspace(-0.5, 0.5, 401)  # momentum in units of 2 pi, one zone
energies = np.linspace(-2.6, 2.6, 521)  # energies in units of |t|
bands, dos = {}, {}  # the band and the density of states for each sign of t
for t in (1., -1.):
    h = g.get_hamiltonian(has_spin=False, tij=[-t])  # matrix element -t between first neighbors
    (ik, bands[t]) = h.get_bands(kpath=[[k, 0., 0.] for k in ks])  # the band, -2t cos k
    (e, dos[t]) = h.get_dos(energies=energies, mode="Green", delta=1e-3)  # density of states per site
k = 2*np.pi*ks  # the momentum k, from -pi to pi
