# Bands and density of states of the kagome lattice, with the Lieb lattice to compare
import numpy as np
from pyqula import geometry

G = np.array([0., 0., 0.])  # Gamma, momenta in units of the reciprocal vectors
K = np.array([2/3, 1/3, 0.])  # a corner of the zone of the kagome lattice
M = np.array([1/2, 0., 0.])  # the middle of the edge of the zone next to K
steps = [120, 60, 104]  # steps of the three segments, in proportion to their lengths
nodes = [G, K, M, G]  # the path Gamma, K, M, Gamma
kpath = [nodes[i] + (nodes[i+1] - nodes[i])*j/steps[i] for i in range(3) for j in range(steps[i])] + [G]

g = geometry.kagome_lattice()  # kagome lattice, bond length 1, three sites per cell
h = g.get_hamiltonian(has_spin=False, tij=[-1.])  # first-neighbor hopping -1, the sign of (2.5)
(k, e) = h.get_bands(kpath=kpath)  # the bands along the path
bands_kagome = np.array(e).reshape(-1, 3)  # energy of band n at step i, the top band is flat
energies = np.linspace(-5., 3., 801)  # energies in units of the hopping
(energies, dos) = h.get_dos(energies=energies, delta=4e-2, nk=200)  # states per cell and per unit of energy, three bands

h = g.get_hamiltonian(has_spin=False, tij=[1.])  # the opposite sign of the hopping, as in the notebook
(k, e) = h.get_bands(kpath=kpath)  # the bands along the same path
bands_kagome_plus = np.array(e).reshape(-1, 3)  # now the lowest band is flat

gl = geometry.lieb_lattice()  # Lieb lattice, bond length 1, three sites per cell
hl = gl.get_hamiltonian(has_spin=False, tij=[-1.])  # first-neighbor hopping -1
X, Ml = np.array([1/2, 0., 0.]), np.array([1/2, 1/2, 0.])  # X and M of the square zone
steps_lieb = [100, 100, 141]  # steps of Gamma-X, X-M and M-Gamma
nodes_lieb = [G, X, Ml, G]  # the path Gamma, X, M, Gamma
kpath_lieb = [nodes_lieb[i] + (nodes_lieb[i+1] - nodes_lieb[i])*j/steps_lieb[i] for i in range(3) for j in range(steps_lieb[i])] + [G]
(k, e) = hl.get_bands(kpath=kpath_lieb)  # the bands along the path
bands_lieb = np.array(e).reshape(-1, 3)  # the middle band is flat
