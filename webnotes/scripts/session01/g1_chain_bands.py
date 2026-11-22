# Bands of a chain with one site per cell and of a chain with two different sites per cell
import numpy as np
from pyqula import geometry

k = np.linspace(-np.pi, np.pi, 401)  # momentum per site, in units of the inverse distance between sites
g = geometry.chain()  # chain with one site per cell
h = g.get_hamiltonian(has_spin=False, tij=[-1.])  # first-neighbor hopping -1, the band is -2 cos k
(ik, e) = h.get_bands(kpath=[[x/(2*np.pi), 0., 0.] for x in k])  # the band, one energy per momentum
metal = np.array(e)  # the band of the metal
g2 = geometry.bichain()  # chain with two sites per cell, so the cell is twice as long
h2 = g2.get_hamiltonian(has_spin=False, tij=[-1.])  # the same hopping -1
h2.add_sublattice_imbalance(0.6)  # onsite energies +0.6 and -0.6 on the two sites of the cell
(ik, e) = h2.get_bands(kpath=[[x/np.pi, 0., 0.] for x in k])  # k covers two zones of the cell of two sites
bands = np.array(e).reshape(len(k), 2)  # valence band in the first column, conduction band in the second
gap = bands[:, 1].min() - bands[:, 0].max()  # the gap between the two bands, 1.2
