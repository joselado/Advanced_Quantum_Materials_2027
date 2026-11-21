# Bands of graphene along Gamma, K, M, Gamma, with a gapped honeycomb lattice and a triangular lattice to compare
import numpy as np
from pyqula import geometry

G = np.array([0., 0., 0.])  # Gamma, momenta in units of the reciprocal vectors
K = np.array([2/3, -1/3, 0.])  # a corner of the zone of the honeycomb lattice, the K of the notes
M = np.array([1/2, -1/2, 0.])  # the middle of the edge of the zone next to K
steps = [120, 60, 104]  # steps of the three segments, in proportion to their lengths
nodes = [G, K, M, G]  # the path Gamma, K, M, Gamma
kpath = [nodes[i] + (nodes[i+1] - nodes[i])*j/steps[i] for i in range(3) for j in range(steps[i])] + [G]

g = geometry.honeycomb_lattice()  # honeycomb lattice, bond length 1
h = g.get_hamiltonian(has_spin=False)  # first-neighbor hopping +1, the +t of (2.19)
(k, e) = h.get_bands(kpath=kpath)  # the bands along the path
bands = np.array(e).reshape(-1, 2)  # energy of band n at step i of the path

h = g.get_hamiltonian(has_spin=False)  # the same lattice again
h.add_sublattice_imbalance(0.5)  # onsite energy +0.5 on one sublattice and -0.5 on the other
(k, e) = h.get_bands(kpath=kpath)  # the bands along the same path
bands_imbalance = np.array(e).reshape(-1, 2)  # a gap opens at K

gt = geometry.triangular_lattice()  # triangular lattice, one site per cell
ht = gt.get_hamiltonian(has_spin=False, tij=[-1.])  # first-neighbor hopping -1, the sign of (2.5)
nodes_t = [G, np.array([1/3, 1/3, 0.]), np.array([1/2, 0., 0.]), G]  # Gamma, K, M, Gamma of this lattice
kpath_t = [nodes_t[i] + (nodes_t[i+1] - nodes_t[i])*j/steps[i] for i in range(3) for j in range(steps[i])] + [G]
(k, e) = ht.get_bands(kpath=kpath_t)  # the single band along the path
band_triangular = np.array(e)  # energy at step i of the path
