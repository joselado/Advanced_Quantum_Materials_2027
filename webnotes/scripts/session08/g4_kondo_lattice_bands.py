# Bands of the Kondo lattice of the notebook, a triangular lattice with one Kondo site on each site
import numpy as np
from pyqula import geometry
from pyqula.specialhamiltonian import H2HFH

G, K, M = np.array([0., 0., 0.]), np.array([1/3, 1/3, 0.]), np.array([0.5, 0., 0.])  # in units of the reciprocal vectors
segments = [(G, K), (K, M), (M, G)]  # the path Gamma, K, M, Gamma
kpath = [a + (b - a)*s for (a, b) in segments for s in np.linspace(0., 1., 150, endpoint=False)] + [G]
ks = np.arange(90)/90  # mesh of the zone, a multiple of 3 holds K
couplings = [0., 0.25, 0.5]  # the values of JK of the notebook
energies = []  # the four bands at each step of the path, the two spins of c and of f
weights = []  # weight of each state on the conduction electrons, from 0 to 1
indirect = []  # lowest state of the upper bands minus highest state of the lower bands, on the mesh
for JK in couplings:
    g = geometry.triangular_lattice()  # triangular lattice
    h = g.get_hamiltonian()  # conduction electrons with hopping 1 and the two spins
    h.add_onsite(-2.0)  # onsite energy of the conduction electrons, before the Kondo sites are added
    h = H2HFH(h, JK=JK)  # one Kondo site per site with its level at zero, coupled by the hopping JK
    (k, e, c) = h.get_bands(operator="dispersive_electrons", kpath=kpath)  # bands and their weight on c
    energies.append(np.array(e).reshape(len(kpath), -1))  # energy of band n at step i, sorted
    weights.append(np.array(c).reshape(len(kpath), -1))  # weight on c of band n at step i
    hk = h.get_hk_gen()  # Bloch Hamiltonian, the momentum in units of the reciprocal vectors
    em = np.array([np.linalg.eigvalsh(hk([k1, k2, 0.])) for k1 in ks for k2 in ks])  # four energies per momentum
    indirect.append(em[:, 2].min() - em[:, 1].max())  # negative when the bands overlap
direct = [np.min(e[:, 2] - e[:, 1]) for e in energies]  # smallest gap at one step of the path, it is 2 JK
