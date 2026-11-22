# The change of the local density of states around one impurity in a square lattice, Section 9.6a
import numpy as np
from pyqula import geometry, embedding, potentials

g = geometry.square_lattice()  # square lattice, lattice constant 1
h = g.get_hamiltonian(has_spin=False, tij=[-1.])  # hopping -1, band -2 (cos kx + cos ky) from -4 to 4
hv = h.copy()  # the same lattice with one impurity
hv.add_onsite(potentials.impurity(g.r[0], v=3.))  # onsite energy 3 on the site at the origin

energies = [-3.8, -3.4, -3.0]  # three energies near the bottom of the band
delta = 0.05  # broadening of the levels
nk = 150  # k-mesh of the clean lattice, 150 x 150
nsuper = 25  # the map has 25 x 25 sites around the impurity
maps = []  # the change of the LDOS, one map per energy
for e in energies:
    (x, y, ldos) = embedding.Embedding(h, m=hv).get_ldos(nsuper=nsuper, energy=e, delta=delta, nk=nk)  # with the impurity
    (x0, y0, ldos0) = embedding.Embedding(h, m=h).get_ldos(nsuper=2, energy=e, delta=delta, nk=nk)  # clean, same k-mesh
    maps.append(ldos - ldos0[0])  # the change caused by the impurity
maps = np.array(maps)

kF = np.arccos(-np.array(energies) / 2 - 1)  # Fermi wavevector along kx, from -2 cos(kF) - 2 = E
period = np.pi / kF  # period of the ripples, pi/kF
