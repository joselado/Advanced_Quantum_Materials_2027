# Two gaps that look alike, a chain with two different sites per cell and a superconducting chain
import numpy as np
from pyqula import geometry

k = np.linspace(-np.pi, np.pi, 401)  # momentum per site, in units of the inverse distance between sites
g2 = geometry.bichain()  # chain with two sites per cell
h2 = g2.get_hamiltonian(has_spin=False, tij=[-1.])  # first-neighbor hopping -1
h2.add_sublattice_imbalance(0.6)  # onsite energies +0.6 and -0.6, so m = 0.6
(ik, e) = h2.get_bands(kpath=[[x/np.pi, 0., 0.] for x in k])  # k covers two zones of the cell of two sites
semiconductor = np.array(e).reshape(len(k), 2)  # the two bands at each momentum
g = geometry.chain()  # chain with one site per cell
h = g.get_hamiltonian(tij=[-1.])  # the band -2 cos k with the two spins, half filled
h.add_swave(0.6)  # s-wave pairing, Delta = 0.6
(ik, e) = h.get_bands(kpath=[[x/(2*np.pi), 0., 0.] for x in k])  # the Bogoliubov-de Gennes bands
superconductor = np.array(e).reshape(len(k), 4)  # four states per momentum, -E twice and +E twice
gap_semiconductor = semiconductor[:, 1].min() - semiconductor[:, 0].max()  # the gap 2m, 1.2
gap_superconductor = superconductor[:, 2].min() - superconductor[:, 1].max()  # the gap 2 Delta, 1.2
